"""Workspace declarations and clean initialization."""

from __future__ import annotations

import json
import re
import shutil
import uuid
from importlib.resources import files
from pathlib import Path

import yaml

from .models import Resource, WorkbenchError, validate_arguments
from .context.catalogs import CATALOG_NAMES, declaration_path, load_catalogs, read_declaration


def load_workspace(root: Path) -> tuple[dict, dict[str, Resource]]:
    try:
        path = root / "workspace.yaml"
        if not path.exists():
            path = root / "workspace.json"
        payload = read_declaration(path)
        schema = json.loads(files("ai_sdlc_workbench").joinpath("schemas", "workspace.schema.json").read_text(encoding="utf-8"))
        validate_arguments(payload, schema, "workspace")
    except (OSError, ValueError):
        raise WorkbenchError("Load a valid workspace.yaml or legacy workspace.json. Use init for a new workspace.") from None
    catalogs, tools = load_catalogs(root, payload.get("registries", {}))
    _apply_local_repository_paths(root, catalogs)
    payload["resources"] = [*payload["resources"], *tools]
    validate_arguments(payload, schema, "workspace")
    payload["_catalogs"] = catalogs
    resources = {}
    for item in payload["resources"]:
        identifier = item["id"]
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", identifier) or identifier in resources:
            raise WorkbenchError("Resource IDs must be unique names without path separators.")
        if len(set(item["allowed_operations"])) != len(item["allowed_operations"]):
            raise WorkbenchError("Resource operation grants must be unique.")
        resources[identifier] = Resource(**item)
    if len(set(payload.get("plugins", []))) != len(payload.get("plugins", [])):
        raise WorkbenchError("Plugin IDs must be unique.")
    return payload, resources


def _apply_local_repository_paths(root: Path, catalogs: dict) -> None:
    """Apply machine-local metadata without changing tool execution grants."""
    path = root / "workspace.local.yaml"
    if not path.exists() and not path.is_symlink():
        return
    local = read_declaration(declaration_path(root, "workspace.local.yaml"))
    if (set(local) != {"schema_version", "repository_paths"} or
            type(local.get("schema_version")) is not int or local["schema_version"] != 1 or
            not isinstance(local.get("repository_paths"), dict)):
        raise WorkbenchError("Local settings need schema_version 1 and repository_paths.")
    repositories = {item["id"]: item for item in catalogs.get("repositories", [])}
    for identifier, location in local["repository_paths"].items():
        if identifier not in repositories:
            raise WorkbenchError("A local path references an unknown repository.")
        if not isinstance(location, str) or not location.strip():
            raise WorkbenchError("Local repository paths must be nonempty strings.")
        try:
            candidate = Path(location).expanduser()
            resolved = (candidate if candidate.is_absolute() else root / candidate).resolve()
        except (ValueError, OSError, RuntimeError):
            raise WorkbenchError("Use a valid local repository path.") from None
        repositories[identifier]["location"] = str(resolved)


def scaffold_root() -> Path:
    package = Path(str(files("ai_sdlc_workbench")))
    bundled = package / "scaffold"
    return bundled if bundled.is_dir() else Path(__file__).resolve().parents[1]


def initialize_workspace(path: str | Path, name: str = "My SDLC workspace") -> Path:
    root = Path(path).expanduser().resolve()
    if not isinstance(name, str) or not name.strip() or len(name) > 200:
        raise WorkbenchError("Use a workspace name from 1 to 200 characters.")
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        raise WorkbenchError("Initialize an empty directory.")
    template = scaffold_root()
    manifest = json.loads((template / "scaffold.json").read_text(encoding="utf-8"))
    root.mkdir(parents=True, exist_ok=True)
    for relative in manifest["paths"]:
        source, destination = template / relative, root / relative
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    registries = {category: f"registry/{category}.yaml" for category in CATALOG_NAMES}
    for category, relative in registries.items():
        catalog = root / relative
        catalog.parent.mkdir(parents=True, exist_ok=True)
        catalog.write_text(yaml.safe_dump({"schema_version": 1, category: []}, sort_keys=False), encoding="utf-8")
    raw = root / "knowledge/raw"
    raw.mkdir(parents=True, exist_ok=True)
    (raw / "manifest.yaml").write_text(yaml.safe_dump({"schema_version": 1, "sources": []}, sort_keys=False),
                                      encoding="utf-8")
    payload = {"schema_version": 1, "id": uuid.uuid4().hex, "name": name, "timeout_seconds": 30,
               "plugins": [], "resources": [], "registries": registries}
    (root / "workspace.yaml").write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return root
