"""Provider contracts and bounded argument validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
from typing import Any, Protocol


class WorkbenchError(ValueError):
    """A workspace or operation does not satisfy its contract."""


@dataclass(frozen=True)
class Operation:
    name: str
    description: str
    input_schema: dict[str, Any]
    mutating: bool = False

    def describe(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Resource:
    id: str
    kind: str
    provider: str
    environment: str
    config: dict[str, Any]
    allowed_operations: list[str]


@dataclass(frozen=True)
class Context:
    workspace_root: Path
    run_dir: Path
    timeout_seconds: float = 30

    def resolve_path(self, value: str) -> Path:
        if not isinstance(value, str) or not value:
            raise WorkbenchError("Configure a resource path.")
        path = Path(value).expanduser()
        return (path if path.is_absolute() else self.workspace_root / path).resolve()

    def confined_path(self, base: Path, relative: str) -> Path:
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
            raise WorkbenchError("Use a relative resource path.")
        root = base.resolve()
        target = (root / relative).resolve()
        if not target.is_relative_to(root):
            raise WorkbenchError("The path leaves the resource directory.")
        return target


class Provider(Protocol):
    id: str
    version: str
    resource_kind: str
    operations: dict[str, Operation]

    def invoke(self, operation: str, resource: Resource,
               arguments: dict[str, Any], context: Context) -> dict[str, Any]: ...


def validate_schema(schema: Any) -> None:
    """Reject schemas that the small validator cannot enforce."""
    keywords = {"$schema", "title", "description", "default", "type", "properties", "required",
                "additionalProperties", "items", "enum", "minLength", "maxLength", "minItems",
                "maxItems", "minimum", "maximum"}
    if not isinstance(schema, dict) or schema.keys() - keywords:
        raise WorkbenchError("The operation schema uses an unsupported keyword.")
    try:
        json.dumps(schema, allow_nan=False)
    except (TypeError, ValueError):
        raise WorkbenchError("The operation schema must contain finite JSON values.") from None
    for key in ("$schema", "title", "description"):
        if key in schema and not isinstance(schema[key], str):
            raise WorkbenchError("The operation schema metadata must contain text.")
    if schema.get("type") not in {"object", "array", "string", "integer", "number", "boolean", "null"}:
        raise WorkbenchError("The operation schema must declare one supported type.")
    if schema["type"] == "object":
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        if (not isinstance(properties, dict) or any(not isinstance(key, str) for key in properties) or
                not isinstance(required, list) or
                any(not isinstance(key, str) for key in required) or set(required) - properties.keys() or
                type(schema.get("additionalProperties", True)) is not bool):
            raise WorkbenchError("The operation object schema is invalid.")
        for child in properties.values():
            validate_schema(child)
    if schema["type"] == "array" and "items" in schema:
        validate_schema(schema["items"])
    if "enum" in schema and (not isinstance(schema["enum"], list) or not schema["enum"]):
        raise WorkbenchError("The operation enum schema is invalid.")
    for lower, upper in (("minLength", "maxLength"), ("minItems", "maxItems"), ("minimum", "maximum")):
        for key in (lower, upper):
            if key in schema:
                bound = schema[key]
                if (isinstance(bound, bool) or not isinstance(bound, (int, float)) or
                        not math.isfinite(bound) or (key not in {"minimum", "maximum"} and
                                                   (not isinstance(bound, int) or bound < 0))):
                    raise WorkbenchError("The operation schema bound is invalid.")
        if lower in schema and upper in schema and schema[lower] > schema[upper]:
            raise WorkbenchError("The operation schema bounds conflict.")


def validate_arguments(value: Any, schema: dict[str, Any], location: str = "arguments") -> None:
    """Validate the documented JSON Schema subset used by provider operations."""
    types = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
        "boolean": lambda item: isinstance(item, bool),
        "null": lambda item: item is None,
    }
    expected = schema.get("type")
    if expected is not None and (expected not in types or not types[expected](value)):
        raise WorkbenchError(f"{location} must have type {expected}.")
    if "enum" in schema and value not in schema["enum"]:
        raise WorkbenchError(f"{location} has an unsupported value.")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                raise WorkbenchError(f"{location}.{key} is required.")
        if schema.get("additionalProperties") is False and value.keys() - properties.keys():
            raise WorkbenchError(f"{location} contains an unsupported field.")
        for key, item in value.items():
            if key in properties:
                validate_arguments(item, properties[key], f"{location}.{key}")
    if isinstance(value, list):
        for key, test in (("minItems", len(value) >= schema.get("minItems", 0)),
                          ("maxItems", len(value) <= schema.get("maxItems", len(value)))):
            if not test:
                raise WorkbenchError(f"{location} exceeds its {key} bound.")
        for item in value:
            if "items" in schema:
                validate_arguments(item, schema["items"], location + "[]")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or len(value) > schema.get("maxLength", len(value)):
            raise WorkbenchError(f"{location} exceeds its length bounds.")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if isinstance(value, float) and not math.isfinite(value):
            raise WorkbenchError(f"{location} must have a finite numeric value.")
        if value < schema.get("minimum", value) or value > schema.get("maximum", value):
            raise WorkbenchError(f"{location} exceeds its numeric bounds.")
