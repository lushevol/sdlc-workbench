"""Workspace declarations, clean initialization, and optional demonstration fixtures."""

from __future__ import annotations

import json
import os
import re
import shutil
import sqlite3
import subprocess
import uuid
from contextlib import closing
from importlib.resources import files
from pathlib import Path

import yaml

from .models import Resource, WorkbenchError, validate_arguments
from .core.context.catalogs import declaration_path, load_catalogs, read_declaration


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
    return bundled if bundled.is_dir() else Path(__file__).resolve().parents[2]


def initialize_workspace(path: str | Path, name: str = "My SDLC workspace", *, demo: bool = False) -> Path:
    if demo:
        return initialize_demo_workspace(path, name)
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
    payload = read_declaration(root / "workspace.yaml")
    payload.update(id=uuid.uuid4().hex, name=name)
    (root / "workspace.yaml").write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return root


def initialize_demo_workspace(path: str | Path, name: str = "My SDLC workspace") -> Path:
    root = Path(path).expanduser().resolve()
    if not isinstance(name, str) or not name.strip() or len(name) > 200:
        raise WorkbenchError("Use a workspace name from 1 to 200 characters.")
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        raise WorkbenchError("Initialize an empty directory.")
    git = shutil.which("git")
    if not git:
        raise WorkbenchError("Install Git before creating the demonstration workspace.")
    root.mkdir(parents=True, exist_ok=True)
    for directory in ("knowledge", "project/tests", "logs", "database"):
        (root / directory).mkdir(parents=True, exist_ok=True)
    (root / ".gitignore").write_text(".workbench/\n__pycache__/\n*.pyc\n.env*\n", encoding="utf-8")
    (root / "knowledge/requirements.md").write_text(
        "# Addition requirement\n\nThe addition function returns the sum of two integers.\n"
        "This sample defines a demonstration behavior. It does not define a business rule.\n", encoding="utf-8")
    (root / "project/calculator.py").write_text("def add(left, right):\n    return left + right\n", encoding="utf-8")
    (root / "project/tests/test_calculator.py").write_text(
        "import unittest\nfrom calculator import add\n\n\nclass AdditionTest(unittest.TestCase):\n"
        "    def test_positive(self):\n        self.assertEqual(add(2, 3), 5)\n\n"
        "    def test_negative(self):\n        self.assertEqual(add(-2, 1), -1)\n", encoding="utf-8")
    (root / "project/.gitignore").write_text("__pycache__/\n*.pyc\n", encoding="utf-8")
    (root / "logs/application.log").write_text(
        "2026-01-01T00:00:00Z INFO service=calculator event=started correlation_id=demo-1\n"
        "2026-01-01T00:00:01Z INFO service=calculator event=addition result=5 correlation_id=demo-1\n",
        encoding="utf-8")
    with closing(sqlite3.connect(root / "database/app.sqlite")) as db, db:
        db.execute("CREATE TABLE executions (id TEXT PRIMARY KEY, result INTEGER)")
        db.execute("INSERT INTO executions VALUES (?, ?)", ("demo-1", 5))
    environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    for args in ([git, "init", "-q", "-b", "main"], [git, "add", "--", "."],
                 [git, "-c", "user.name=Workbench Demo", "-c", "user.email=demo@example.invalid",
                  "-c", "commit.gpgsign=false", "commit", "-q", "-m", "Add demonstration project"]):
        try:
            subprocess.run(args, cwd=root / "project", env=environment, check=True, capture_output=True, timeout=15)
        except (OSError, subprocess.SubprocessError):
            raise WorkbenchError("The demonstration Git checkout could not initialize.") from None
    resources = [
        {"id": "knowledge", "kind": "knowledge", "provider": "knowledge.local", "environment": "local",
         "config": {"path": "knowledge"}, "allowed_operations": ["list", "search", "read", "ingest"]},
        {"id": "repository", "kind": "repository", "provider": "repository.git", "environment": "local",
         "config": {"path": "project"}, "allowed_operations": ["status", "diff", "branch"]},
        {"id": "tests", "kind": "testing", "provider": "testing.command", "environment": "local",
         "config": {"path": "project", "suites": {"unit": ["{python}", "-m", "unittest", "discover", "-s", "tests", "-v"]}},
         "allowed_operations": ["list", "run"]},
        {"id": "logs", "kind": "logs", "provider": "logs.file", "environment": "local",
         "config": {"path": "logs/application.log"}, "allowed_operations": ["search"]},
        {"id": "database", "kind": "database", "provider": "database.sqlite", "environment": "local",
         "config": {"path": "database/app.sqlite"}, "allowed_operations": ["tables", "query"]},
    ]
    payload = {"schema_version": 1, "id": uuid.uuid4().hex, "name": name,
               "timeout_seconds": 30, "plugins": [], "resources": resources}
    (root / "workspace.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return root
