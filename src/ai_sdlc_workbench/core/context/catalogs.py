"""Read local workspace declarations without relocating referenced assets."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from ...models import WorkbenchError


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject ambiguous grants or identities declared with duplicate YAML keys."""


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise WorkbenchError("YAML mapping keys must be unique strings.")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def read_declaration(path: Path) -> dict:
    try:
        with path.open("rb") as stream:
            raw = stream.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise WorkbenchError("Workspace declarations must not exceed one MiB.")
        value = yaml.load(raw.decode("utf-8"), Loader=UniqueKeyLoader)
        if not isinstance(value, dict):
            raise WorkbenchError("Workspace declarations must contain an object.")
        json.dumps(value, allow_nan=False)
        return value
    except (OSError, UnicodeError, yaml.YAMLError, TypeError, ValueError, RecursionError):
        raise WorkbenchError("Load a readable YAML declaration with JSON-compatible values.") from None


def declaration_path(root: Path, relative: str) -> Path:
    try:
        candidate = root / relative
        if Path(relative).is_absolute() or not candidate.resolve().is_relative_to(root.resolve()):
            raise WorkbenchError("Registry declarations must stay within the workspace.")
        return candidate
    except (ValueError, OSError):
        raise WorkbenchError("Use valid registry paths within the workspace.") from None


def load_catalogs(root: Path, locations: dict) -> tuple[dict, list[dict]]:
    catalogs = {}
    for category, relative in locations.items():
        payload = read_declaration(declaration_path(root, relative))
        if (set(payload) != {"schema_version", category} or
                type(payload.get("schema_version")) is not int or payload["schema_version"] != 1 or
                not isinstance(payload.get(category), list)):
            raise WorkbenchError("Each registry needs schema_version 1 and its category list.")
        entries = payload[category]
        identifiers = set()
        for item in entries:
            identifier = item.get("id") if isinstance(item, dict) else None
            if (not isinstance(identifier, str) or
                    not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", identifier) or identifier in identifiers):
                raise WorkbenchError("Registry entry IDs must be unique names without path separators.")
            identifiers.add(identifier)
            for field in ("name", "location"):
                if field in item and (not isinstance(item[field], str) or not item[field].strip()):
                    raise WorkbenchError("Registry names and locations must be nonempty strings.")
        catalogs[category] = entries
    repository_ids = {item["id"] for item in catalogs.get("repositories", [])}
    service_ids = {item["id"] for item in catalogs.get("services", [])}
    for service in catalogs.get("services", []):
        reference = service.get("repository_id")
        if reference is not None and (not isinstance(reference, str) or reference not in repository_ids):
            raise WorkbenchError("A service references an unknown repository.")
    for capability in catalogs.get("capabilities", []):
        references = capability.get("service_ids", [])
        if (not isinstance(references, list) or any(not isinstance(item, str) or item not in service_ids for item in references)
                or len(set(references)) != len(references)):
            raise WorkbenchError("A capability must reference unique registered services.")
    return catalogs, catalogs.get("tools", [])
