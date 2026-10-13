"""Read local workspace declarations without relocating referenced assets."""

from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath

import yaml

from ...models import WorkbenchError, validate_arguments


ID_PATTERN = r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}"
REPOSITORY_TYPES = ("frontend", "backend", "library", "integration", "data", "deployment", "testing")
CONTRACT_TYPES = ("http", "graphql", "messaging", "ui", "data", "deployment")
SOURCE_TYPES = ("git", "filesystem", "xwiki", "confluence", "ado", "email", "teams")
CATALOG_NAMES = ("repositories", "services", "capabilities", "contracts", "sources", "tools")

_TEXT = {"type": "string", "minLength": 1}
_TEXT_LIST = {"type": "array", "items": _TEXT}
_OWNERSHIP = {
    "type": "object", "additionalProperties": False,
    "properties": {"team": _TEXT, "contact": _TEXT},
}
_COMMON = {
    "id": _TEXT, "name": _TEXT, "description": _TEXT, "location": _TEXT,
    "responsibility": _TEXT, "responsibilities": _TEXT_LIST, "ownership": _OWNERSHIP,
    "source_ids": _TEXT_LIST,
}
_CONTRACT_LINKS = {"provides_contract_ids": _TEXT_LIST, "consumes_contract_ids": _TEXT_LIST}
_ENTRY_SCHEMAS = {
    "repositories": {
        "type": "object", "required": ["id"],
        "properties": {**_COMMON, **_CONTRACT_LINKS,
                       "primary_type": {"type": "string", "enum": list(REPOSITORY_TYPES)}},
    },
    "services": {
        "type": "object", "required": ["id"],
        "properties": {**_COMMON, **_CONTRACT_LINKS, "repository_id": _TEXT,
                       "repository_ids": _TEXT_LIST, "deployment_repository_ids": _TEXT_LIST},
    },
    "capabilities": {
        "type": "object", "required": ["id"],
        "properties": {**_COMMON, "service_ids": _TEXT_LIST, "repository_ids": _TEXT_LIST},
    },
    "contracts": {
        "type": "object", "required": ["id", "type", "status", "source"],
        "additionalProperties": False,
        "properties": {
            **_COMMON, "type": {"type": "string", "enum": list(CONTRACT_TYPES)},
            "status": {"type": "string", "enum": ["documented", "candidate"]},
            "source": {
                "type": "object", "required": ["repository_id", "path", "revision"],
                "additionalProperties": False,
                "properties": {"repository_id": _TEXT, "path": _TEXT,
                               "revision": {"type": "string", "minLength": 40, "maxLength": 64}},
            },
            "documentation_gap": _TEXT, "verified_claims": _TEXT_LIST,
            "service_ids": _TEXT_LIST, "repository_ids": _TEXT_LIST,
        },
    },
    "sources": {
        "type": "object", "required": ["id", "type", "purpose", "location"],
        "additionalProperties": False,
        "properties": {
            "id": _TEXT, "name": _TEXT, "description": _TEXT, "location": _TEXT,
            "type": {"type": "string", "enum": list(SOURCE_TYPES)},
            "purpose": {"type": "string", "enum": ["technical", "context"]},
            "read_only": {"type": "boolean", "default": True}, "repository_id": _TEXT, "revision": _TEXT,
            "ownership": _OWNERSHIP,
        },
    },
}

_REFERENCES = {
    "repositories": {"source_ids": "sources", "provides_contract_ids": "contracts",
                     "consumes_contract_ids": "contracts"},
    "services": {"repository_ids": "repositories", "deployment_repository_ids": "repositories",
                 "source_ids": "sources", "provides_contract_ids": "contracts",
                 "consumes_contract_ids": "contracts"},
    "capabilities": {"service_ids": "services", "repository_ids": "repositories", "source_ids": "sources"},
    "contracts": {"service_ids": "services", "repository_ids": "repositories", "source_ids": "sources"},
}


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
    """Validate metadata links; only the tools catalog supplies executable resources.

    Registry declarations describe authored context. Loading a contract does not
    inspect its source or establish that a consumer, provider, or deployment ran.
    """
    if not isinstance(locations, dict) or locations.keys() - set(CATALOG_NAMES):
        raise WorkbenchError("Use registered catalog categories.")
    catalogs = {}
    for category, relative in locations.items():
        if not isinstance(relative, str) or not relative.strip():
            raise WorkbenchError("Use nonempty registry declaration paths.")
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
                    not re.fullmatch(ID_PATTERN, identifier) or identifier in identifiers):
                raise WorkbenchError("Registry entry IDs must be unique names without path separators.")
            identifiers.add(identifier)
            schema = _ENTRY_SCHEMAS.get(category)
            if schema is not None:
                validate_arguments(item, schema, f"{category}.{identifier}")
                try:
                    _validate_text_fields(item, schema)
                except WorkbenchError as error:
                    raise WorkbenchError(f"{category}.{identifier}: {error}") from None
            else:
                for field in ("name", "location"):
                    if field in item and (not isinstance(item[field], str) or not item[field].strip()):
                        raise WorkbenchError("Registry names and locations must be nonempty strings.")
        catalogs[category] = entries
    identifiers = {category: {item["id"] for item in entries} for category, entries in catalogs.items()}
    for category, fields in _REFERENCES.items():
        for item in catalogs.get(category, []):
            for field, target in fields.items():
                if any(reference not in identifiers.get(target, set()) for reference in item.get(field, [])):
                    raise WorkbenchError(f"{category}.{item['id']}.{field} references an unknown {target} entry.")
    for service in catalogs.get("services", []):
        reference = service.get("repository_id")
        if reference is not None and reference not in identifiers.get("repositories", set()):
            raise WorkbenchError(f"services.{service['id']}.repository_id references an unknown repository.")
    for contract in catalogs.get("contracts", []):
        source = contract["source"]
        if source["repository_id"] not in identifiers.get("repositories", set()):
            raise WorkbenchError(f"contracts.{contract['id']}.source references an unknown repository.")
        if not re.fullmatch(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})", source["revision"]):
            raise WorkbenchError(f"contracts.{contract['id']}.source.revision must identify a full Git commit ID.")
        path = source["path"]
        if ("\x00" in path or "\\" in path or PurePosixPath(path).is_absolute() or
                PureWindowsPath(path).drive or ".." in PurePosixPath(path).parts or path in {".", ""}):
            raise WorkbenchError(f"contracts.{contract['id']}.source.path must identify a relative file within its repository.")
        if contract["status"] == "candidate":
            if not contract.get("documentation_gap") or contract.get("verified_claims"):
                raise WorkbenchError(f"contracts.{contract['id']}: A candidate needs a documentation gap and cannot have verified claims.")
    for source in catalogs.get("sources", []):
        if source["type"] == "confluence" and source.get("read_only") is not True:
            raise WorkbenchError(f"sources.{source['id']}: A Confluence source must declare read_only: true.")
        if "repository_id" in source and source["repository_id"] not in identifiers.get("repositories", set()):
            raise WorkbenchError(f"sources.{source['id']}.repository_id references an unknown repository.")
        source.setdefault("read_only", True)
    return catalogs, catalogs.get("tools", [])


def _validate_text_fields(value, schema):
    """Check nonblank text and list uniqueness beyond the schema subset."""
    if schema["type"] == "string" and not value.strip():
        raise WorkbenchError("Registry text fields must contain nonempty text.")
    if schema["type"] == "array":
        if len(set(value)) != len(value):
            raise WorkbenchError("Registry lists must contain unique values.")
        for item in value:
            _validate_text_fields(item, schema["items"])
    if schema["type"] == "object":
        for field, child in schema.get("properties", {}).items():
            if field in value:
                _validate_text_fields(value[field], child)
