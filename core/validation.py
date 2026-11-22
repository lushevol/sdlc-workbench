"""Read workspace contracts without executing providers or creating run records."""

from pathlib import Path

from .governance import validate_knowledge
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
    try:
        from .capability_learning import CapabilityRegistry

        CapabilityRegistry(root, configuration=configuration).available()
    except (OSError, WorkbenchError) as error:
        knowledge["valid"] = False
        knowledge["findings"].append({"path": "registry/capability-history",
                                      "code": "CAPABILITY_HISTORY_ERROR",
                                      "message": str(error) if isinstance(error, WorkbenchError)
                                      else "The capability history could not be read."})
    return {"schema_version": 1, "status": "VALID" if knowledge["valid"] else "INVALID",
            **knowledge,
            "catalogs": {name: len(entries) for name, entries in configuration.get("_catalogs", {}).items()}}
