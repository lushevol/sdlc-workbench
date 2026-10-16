"""Resolve resource capabilities and retain every dispatched action."""

from __future__ import annotations

import hashlib
import json
import threading
import uuid
from datetime import datetime, timezone
from importlib.resources import files
from pathlib import Path
from typing import Any

from .models import Context, WorkbenchError, validate_arguments
from .registry import load_registry
from .store import Store
from .workspace import load_workspace, scaffold_root


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Workbench:
    def __init__(self, workspace: str | Path):
        self.root = Path(workspace).expanduser().resolve()
        self.config, self.resources = load_workspace(self.root)
        self.registry = load_registry(self.config.get("plugins", []), self.root)
        for resource in self.resources.values():
            provider = self.registry.get(resource.provider)
            if resource.kind != provider.resource_kind:
                raise WorkbenchError(f"Resource {resource.id} has an incompatible kind.")
            if set(resource.allowed_operations) - provider.operations.keys():
                raise WorkbenchError(f"Resource {resource.id} grants an unknown operation.")
        self.store = Store(self.root)
        self._lock = threading.RLock()

    def describe(self) -> dict:
        resources = []
        for resource in self.resources.values():
            provider = self.registry.get(resource.provider)
            resources.append({"id": resource.id, "kind": resource.kind, "provider": resource.provider,
                              "environment": resource.environment,
                              "allowed_operations": resource.allowed_operations,
                              "operations": [dict(operation.describe(), allowed=name in resource.allowed_operations)
                                             for name, operation in provider.operations.items()]})
        return {"schema_version": 1,
                "workspace": {"id": self.config["id"], "name": self.config["name"], "root": str(self.root)},
                "providers": self.registry.describe(), "resources": resources,
                "catalogs": {name: {"count": len(entries), "ids": [item["id"] for item in entries]}
                             for name, entries in self.config.get("_catalogs", {}).items() if name != "tools"},
                "limitations": ["Actions run locally. Remote runners require a future adapter.",
                                "Execution records do not establish approved business behavior.",
                                "Installed plugins execute trusted Python code."]}

    def call(self, resource_id: str, operation: str, arguments: dict | None = None) -> dict:
        if not isinstance(resource_id, str) or resource_id not in self.resources:
            raise WorkbenchError("The resource does not exist.")
        resource = self.resources[resource_id]
        provider = self.registry.get(resource.provider)
        if not isinstance(operation, str) or operation not in provider.operations:
            raise WorkbenchError("The operation does not exist.")
        arguments = {} if arguments is None else arguments
        try:
            arguments = json.loads(json.dumps(arguments, allow_nan=False))
        except (TypeError, ValueError):
            raise WorkbenchError("Arguments must contain JSON values.") from None
        with self._lock:
            run_id = uuid.uuid4().hex
            directory = self.store.runs_dir / run_id
            directory.mkdir()
            config_hash = hashlib.sha256(json.dumps(resource.config, sort_keys=True).encode()).hexdigest()
            record: dict[str, Any] = {
                "id": run_id, "workspace_id": self.config["id"], "resource_id": resource.id,
                "environment": resource.environment, "provider": provider.id, "provider_version": provider.version,
                "configuration_sha256": config_hash, "operation": operation, "arguments": arguments,
                "status": "RUNNING", "started_at": _now(), "finished_at": None,
                "result": None, "error": None, "evidence": [],
            }
            self.store.save(record)
            try:
                if operation not in resource.allowed_operations:
                    record.update(status="DENIED", error="The resource does not grant this operation.")
                else:
                    validate_arguments(arguments, provider.operations[operation].input_schema)
                    context = Context(self.root, directory, self.config.get("timeout_seconds", 30))
                    result = provider.invoke(operation, resource, arguments, context)
                    if (not isinstance(result, dict) or
                            result.get("status") not in {"SUCCEEDED", "FAILED", "ERROR", "TIMEOUT"}):
                        raise WorkbenchError("The provider returned an invalid result.")
                    json.dumps(result, allow_nan=False)
                    record["result"] = result
                    record["status"] = "SUCCEEDED" if result["status"] == "SUCCEEDED" else "FAILED"
            except WorkbenchError as error:
                record.update(status="FAILED", error=str(error))
            except Exception:
                record.update(status="FAILED", error="Operation failed. Inspect the resource configuration.")
            finally:
                record["finished_at"] = _now()
                try:
                    self.store.retain(record, directory)
                except Exception:
                    record.update(status="FAILED", error="The workbench could not retain the action evidence.", evidence=[])
                    self.store.save(record)
            return record

    def runs(self, limit: int = 20) -> list[dict]:
        return self.store.runs(limit)

    def run(self, run_id: str) -> dict:
        return self.store.run(run_id)

    def skill_list(self) -> list[dict]:
        result = []
        for identifier, path in sorted(self._skill_sources().items()):
            lines = path.read_text(encoding="utf-8").splitlines()
            title = next((line[2:].strip() for line in lines if line.startswith("# ")), identifier)
            result.append({"id": identifier, "title": title})
        return result

    def _skill_sources(self) -> dict:
        legacy = files("ai_sdlc_workbench").joinpath("skills")
        sources = {item.name[:-3]: item for item in legacy.iterdir() if item.name.endswith(".md")}
        for root in (scaffold_root() / ".agents/skills", self.root / ".agents/skills"):
            if not root.is_dir() or root.is_symlink():
                continue
            for directory in root.iterdir():
                path = directory / "SKILL.md"
                if directory.is_dir() and not directory.is_symlink() and path.is_file() and not path.is_symlink():
                    sources[directory.name] = path
        return sources

    def skill_read(self, skill_id: str) -> str:
        sources = self._skill_sources()
        if skill_id not in sources:
            raise WorkbenchError("The skill does not exist.")
        return sources[skill_id].read_text(encoding="utf-8")
