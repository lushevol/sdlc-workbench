"""Read workspace contracts without executing providers or creating run records."""

from pathlib import Path

from .core.governance import validate_knowledge
from .models import WorkbenchError
from .workspace import load_workspace


def validate_workspace(root: Path) -> dict:
    """Report deterministic checks; a valid record does not establish truth."""
    try:
        configuration, _ = load_workspace(root)
    except WorkbenchError as error:
        return {"schema_version": 1, "status": "INVALID", "valid": False,
                "documents": 0, "catalogs": {}, "findings": [
                    {"path": "workspace.yaml" if (root / "workspace.yaml").exists() else "workspace.json",
                     "code": "WORKSPACE_ERROR", "message": str(error)}]}
    knowledge = validate_knowledge(root)
    return {"schema_version": 1, "status": "VALID" if knowledge["valid"] else "INVALID",
            **knowledge,
            "catalogs": {name: len(entries) for name, entries in configuration.get("_catalogs", {}).items()}}
