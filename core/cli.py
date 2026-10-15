"""Command interface for a local AI-SDLC workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from .models import WorkbenchError
from .runtime import Workbench
from .workspace import initialize_workspace


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-sdlc", description=__doc__)
    parser.add_argument("--workspace", default=str(Path.cwd()), help="Workspace directory")
    commands = parser.add_subparsers(dest="command", required=True)
    initialize = commands.add_parser("init", help="Create an agent-integrated workspace")
    initialize.add_argument("path", nargs="?")
    initialize.add_argument("--name", default="My SDLC workspace")
    commands.add_parser("status", help="Describe the workspace")
    commands.add_parser("validate", help="Check catalogs and governed knowledge without changing files")
    commands.add_parser("resources", help="List configured resources and capabilities")
    commands.add_parser("plugins", help="List installed provider plugins")
    call = commands.add_parser("call", help="Run one resource operation")
    call.add_argument("resource")
    call.add_argument("operation")
    call.add_argument("--args", default="{}", help="Arguments as a JSON object")
    runs = commands.add_parser("runs", help="List retained action records")
    runs.add_argument("--limit", type=int, default=20)
    run = commands.add_parser("run", help="Read one retained action record")
    run.add_argument("id")
    skills = commands.add_parser("skills", help="List skills or read one skill")
    skills.add_argument("id", nargs="?")
    graph = commands.add_parser("graph", help="Build a validated static dependency graph")
    graph_commands = graph.add_subparsers(dest="graph_command", required=True)
    build = graph_commands.add_parser("build", help="Extract, validate, and publish one graph snapshot")
    build.add_argument("--repos", default="repos", help="Repository directory, relative to the workspace")
    build.add_argument("--out", default="relationships/service-dependencies/generated", help="Snapshot directory")
    build.add_argument("--open", action="store_true", help="Open the generated graph viewer")
    commands.add_parser("mcp", help="Serve MCP over standard input and output")
    return parser


def _print_json(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "init":
            path = initialize_workspace(arguments.path or arguments.workspace, name=arguments.name)
            _print_json({"workspace": str(path), "status": "INITIALIZED"})
            return 0
        if arguments.command == "validate":
            from .validation import validate_workspace
            result = validate_workspace(Path(arguments.workspace).expanduser().resolve())
            _print_json(result)
            return 0 if result["valid"] else 1
        if arguments.command == "graph":
            from .relationships.graph.generate_all_graphs import main as build_graph
            root = Path(arguments.workspace).expanduser().resolve()
            from .workspace import load_workspace
            load_workspace(root)
            options = ["--workspace", str(root), "--repos", arguments.repos, "--out", arguments.out]
            if arguments.open:
                options.append("--open")
            try:
                return build_graph(options)
            except (ValueError, subprocess.CalledProcessError) as error:
                raise WorkbenchError("Graph generation failed. Inspect diagnostics; the previous snapshot remains available.") from error
        workbench = Workbench(arguments.workspace)
        if arguments.command in {"status", "resources", "plugins"}:
            description = workbench.describe()
            _print_json(description if arguments.command == "status" else
                        description["resources" if arguments.command == "resources" else "providers"])
        elif arguments.command == "call":
            try:
                payload = json.loads(arguments.args)
            except json.JSONDecodeError as error:
                raise WorkbenchError("Arguments must contain valid JSON.") from error
            if not isinstance(payload, dict):
                raise WorkbenchError("Arguments must be a JSON object.")
            result = workbench.call(arguments.resource, arguments.operation, payload)
            _print_json(result)
            return 0 if result.get("status") == "SUCCEEDED" else 1
        elif arguments.command == "runs":
            if not 1 <= arguments.limit <= 100:
                raise WorkbenchError("The run limit must be between 1 and 100.")
            _print_json(workbench.runs(arguments.limit))
        elif arguments.command == "run":
            _print_json(workbench.run(arguments.id))
        elif arguments.command == "skills":
            if arguments.id:
                print(workbench.skill_read(arguments.id))
            else:
                _print_json(workbench.skill_list())
        elif arguments.command == "mcp":
            from .mcp import serve
            serve(workbench)
        return 0
    except WorkbenchError as error:
        if arguments.command == "mcp":
            print("The MCP workspace could not load. Check its configuration.", file=sys.stderr)
        else:
            _print_json({"error": {"code": "WORKBENCH_ERROR", "message": str(error)}})
        return 1
    except OSError:
        if arguments.command == "mcp":
            print("The MCP workspace could not access its resource.", file=sys.stderr)
        else:
            _print_json({"error": {"code": "IO_ERROR", "message": "The operation could not access its resource."}})
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
