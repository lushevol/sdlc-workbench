"""Load the workspace-owned dependency skill without duplicating its helpers."""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
from pathlib import Path
import sys
from types import ModuleType

from ..workspace import scaffold_root


SKILL_RELATIVE = Path(".agents/skills/service-dependencies-graph")


def graph_skill_root(workspace_root: Path | None = None) -> Path:
    """Prefer the workspace skill; use the shipped skill when it is absent."""
    candidates = []
    if workspace_root is not None:
        candidates.append(Path(workspace_root).resolve() / SKILL_RELATIVE)
    candidates.append(scaffold_root() / SKILL_RELATIVE)
    for candidate in candidates:
        if (candidate / "SKILL.md").is_file() and (candidate / "tools/__init__.py").is_file():
            return candidate.resolve()
    raise ValueError("The service-dependencies-graph skill is unavailable.")


def load_graph_tool(name: str, workspace_root: Path | None = None) -> ModuleType:
    """Load one helper from a namespace isolated by its owning skill path."""
    if not name.isidentifier() or name.startswith("_"):
        raise ValueError("Use a dependency skill helper name.")
    root = graph_skill_root(workspace_root)
    namespace = "_workbench_dependency_skill_" + hashlib.sha256(str(root).encode()).hexdigest()[:20]
    if namespace not in sys.modules:
        spec = importlib.util.spec_from_file_location(namespace, root / "tools/__init__.py",
                                                     submodule_search_locations=[str(root / "tools")])
        if spec is None or spec.loader is None:
            raise ValueError("The dependency skill tools cannot load.")
        module = importlib.util.module_from_spec(spec)
        sys.modules[namespace] = module
        try:
            spec.loader.exec_module(module)
        except BaseException:
            sys.modules.pop(namespace, None)
            raise
    return importlib.import_module(namespace + "." + name)
