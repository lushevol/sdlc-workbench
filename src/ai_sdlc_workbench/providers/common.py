"""Shared validation and fixed errors for the built-in providers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..models import Context, Operation, Resource


class ProviderError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def object_schema(properties: dict | None = None, required: tuple[str, ...] = ()) -> dict:
    return {"type": "object", "properties": properties or {}, "required": list(required), "additionalProperties": False}


def string_schema(*, minimum: int = 1, maximum: int = 4096) -> dict:
    return {"type": "string", "minLength": minimum, "maxLength": maximum}


def integer_schema(minimum: int, maximum: int) -> dict:
    return {"type": "integer", "minimum": minimum, "maximum": maximum}


def validate_arguments(arguments: Any, schema: dict) -> None:
    if not isinstance(arguments, dict):
        raise ProviderError("INVALID_ARGUMENT", "Arguments must be an object.")
    properties = schema["properties"]
    if set(arguments) - set(properties) or set(schema["required"]) - set(arguments):
        raise ProviderError("INVALID_ARGUMENT", "Arguments do not match the operation schema.")
    for key, value in arguments.items():
        rule = properties[key]
        if rule["type"] == "string":
            if not isinstance(value, str) or not rule.get("minLength", 0) <= len(value) <= rule.get("maxLength", 4096):
                raise ProviderError("INVALID_ARGUMENT", "A string argument has an invalid length or type.")
            if "\x00" in value:
                raise ProviderError("INVALID_ARGUMENT", "Arguments must not contain null bytes.")
        elif rule["type"] == "integer":
            if isinstance(value, bool) or not isinstance(value, int) or not rule["minimum"] <= value <= rule["maximum"]:
                raise ProviderError("INVALID_ARGUMENT", "An integer argument is outside the allowed bounds.")


def configured_path(resource: Resource, context: Context) -> Path:
    value = resource.config.get("path")
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ProviderError("INVALID_CONFIGURATION", "The resource needs a configured path.")
    return context.resolve_path(value)


def relative_path(base: Path, value: str, context: Context) -> Path:
    if Path(value).is_absolute() or "\x00" in value:
        raise ProviderError("INVALID_ARGUMENT", "The document path must be relative to its resource.")
    try:
        return context.confined_path(base, value)
    except (ValueError, OSError) as error:
        raise ProviderError("INVALID_ARGUMENT", "The document path leaves its resource.") from error


def timeout(context: Context) -> float:
    value = context.timeout_seconds
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 < value <= 3600:
        raise ProviderError("INVALID_CONFIGURATION", "The timeout must be greater than zero and at most 3600 seconds.")
    return float(value)


class BuiltinProvider:
    version = "0.1.0"
    id: str
    resource_kind: str
    operations: dict[str, Operation]

    def invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        try:
            if operation not in self.operations:
                raise ProviderError("UNKNOWN_OPERATION", "The provider does not support this operation.")
            validate_arguments(arguments, self.operations[operation].input_schema)
            return self._invoke(operation, resource, arguments, context)
        except ProviderError as error:
            return {"status": "ERROR", "code": error.code, "message": error.message}
        except FileNotFoundError:
            return {"status": "ERROR", "code": "RESOURCE_UNAVAILABLE", "message": "The configured resource is unavailable."}
        except PermissionError:
            return {"status": "ERROR", "code": "ACCESS_DENIED", "message": "The provider cannot access the configured resource."}
        except UnicodeError:
            return {"status": "ERROR", "code": "UNSUPPORTED_CONTENT", "message": "The resource does not contain valid UTF-8 text."}
        except (OSError, ValueError, TypeError):
            return {"status": "ERROR", "code": "PROVIDER_FAILURE", "message": "The provider could not complete the operation."}

    def _invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        raise NotImplementedError
