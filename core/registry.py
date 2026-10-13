"""Built-in providers and explicitly enabled Python entry points."""

from __future__ import annotations

from importlib.metadata import entry_points

from .models import Operation, Provider, WorkbenchError, validate_schema


class Registry:
    def __init__(self) -> None:
        self.providers: dict[str, Provider] = {}

    def register(self, provider: Provider) -> None:
        required = ("id", "version", "resource_kind", "operations", "invoke")
        if any(not hasattr(provider, field) for field in required):
            raise WorkbenchError("The plugin does not implement the provider contract.")
        if not isinstance(provider.id, str) or not provider.id or provider.id in self.providers:
            raise WorkbenchError("The provider ID is empty or already registered.")
        if (not isinstance(provider.version, str) or not provider.version or
                not isinstance(provider.resource_kind, str) or not provider.resource_kind or
                not callable(provider.invoke)):
            raise WorkbenchError("The provider metadata or invoke method is invalid.")
        if not isinstance(provider.operations, dict) or not provider.operations:
            raise WorkbenchError("The provider must declare operations.")
        for name, operation in provider.operations.items():
            if (not isinstance(name, str) or not name or not isinstance(operation, Operation) or
                    name != operation.name or not isinstance(operation.input_schema, dict) or
                    operation.input_schema.get("type") != "object" or type(operation.mutating) is not bool or
                    not isinstance(operation.description, str) or not operation.description.strip()):
                raise WorkbenchError("The provider operation contract is invalid.")
            validate_schema(operation.input_schema)
        self.providers[provider.id] = provider

    def get(self, identifier: str) -> Provider:
        try:
            return self.providers[identifier]
        except KeyError:
            raise WorkbenchError(f"Provider {identifier} is unavailable.") from None

    def describe(self) -> list[dict]:
        return [{"id": provider.id, "version": provider.version,
                 "resource_kind": provider.resource_kind,
                 "operations": [operation.describe() for operation in provider.operations.values()]}
                for provider in self.providers.values()]


def load_registry(plugin_ids: list[str] | None = None) -> Registry:
    from .providers import builtin_providers

    registry = Registry()
    for provider in builtin_providers():
        registry.register(provider)
    enabled = plugin_ids or []
    if enabled:
        installed = entry_points(group="ai_sdlc_workbench.providers")
        for identifier in enabled:
            candidates = [item for item in installed if item.name == identifier]
            if len(candidates) != 1:
                raise WorkbenchError(f"Install one plugin entry point for {identifier}.")
            try:
                provider = candidates[0].load()()
                if provider.id != identifier:
                    raise WorkbenchError("The plugin ID does not match its entry point.")
                registry.register(provider)
            except WorkbenchError:
                raise
            except Exception:
                raise WorkbenchError(f"Plugin {identifier} failed to load.") from None
    return registry
