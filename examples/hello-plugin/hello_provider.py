"""A minimal external provider; no remote service is implied."""

from ai_sdlc_workbench.models import Context, Operation, Resource


class HelloProvider:
    id = "example.hello"
    version = "0.1.0"
    resource_kind = "service"
    operations = {
        "inspect": Operation("inspect", "Read the configured example service label.",
                             {"type": "object", "properties": {}, "additionalProperties": False})
    }

    def invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        return {"status": "SUCCEEDED", "label": resource.config.get("label", "Example service"),
                "environment": resource.environment}
