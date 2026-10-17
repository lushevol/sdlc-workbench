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
    lint = commands.add_parser("lint", help="Check authored SDLC artifacts without loading a workspace")
    lint.add_argument("paths", nargs="*", help="Markdown artifacts or artifact-only directories")
    lint.add_argument("--strict", action="store_true", help="Fail on warnings as well as errors")
    lint.add_argument("--print-schema", action="store_true", help="Print the installed authoring JSON Schema")
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
    clinic = commands.add_parser("release-clinic", help="Run Release Clinic with workspace-root settings")
    clinic_commands = clinic.add_subparsers(dest="clinic_command", required=True)
    for name in ("doctor", "path"):
        clinic_commands.add_parser(name, help="Check local setup" if name == "doctor" else "Locate installed tool assets")
    for name in ("collect", "report", "portfolio", "audit", "serve"):
        operation = clinic_commands.add_parser(name, add_help=False, prefix_chars="\x00",
                                               help=f"Run Release Clinic {name}")
        operation.add_argument("clinic_args", nargs=argparse.REMAINDER)
    assurance = commands.add_parser("assurance", help="Check behavior evidence without granting business verification")
    evidence = assurance.add_subparsers(dest="assurance_command", required=True)
    evidence.add_parser("schema", help="Print the installed behavior review schema")
    for name in ("validate", "report", "save"):
        operation = evidence.add_parser(name, help=f"{name.capitalize()} one behavior evidence baseline")
        operation.add_argument("--baseline", required=True, help="Baseline JSON inside the workspace")
        if name == "validate":
            operation.add_argument("--require-current", action="store_true", help="Also fail on stale or unknown evidence")
    compare = evidence.add_parser("compare", help="Compare retained baselines from the same story")
    compare.add_argument("--before", required=True)
    compare.add_argument("--after", required=True)
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
        if arguments.command == "release-clinic":
            from .release_clinic import run
            return run(Path(arguments.workspace), arguments.clinic_command, getattr(arguments, "clinic_args", []))
        if arguments.command == "init":
            path = initialize_workspace(arguments.path or arguments.workspace, name=arguments.name)
            _print_json({"workspace": str(path), "status": "INITIALIZED"})
            return 0
        if arguments.command == "validate":
            from .validation import validate_workspace
            result = validate_workspace(Path(arguments.workspace).expanduser().resolve())
            _print_json(result)
            return 0 if result["valid"] else 1
        if arguments.command == "lint":
            from .artifact_lint import artifact_schema, lint_artifacts
            if arguments.print_schema:
                if arguments.paths or arguments.strict:
                    raise WorkbenchError("Use --print-schema without artifact paths or --strict.")
                _print_json(artifact_schema())
                return 0
            result = lint_artifacts(arguments.paths, strict=arguments.strict)
            _print_json(result)
            return 0 if result["valid"] else 1
        if arguments.command == "assurance":
            from .assurance import analyze_baseline, compare_baselines, local_path, read_baseline, save_baseline, schema
            if arguments.assurance_command == "schema":
                _print_json(schema())
                return 0
            root = Path(arguments.workspace).expanduser().resolve()

            def baseline(value):
                path = Path(value).expanduser()
                if path.is_absolute():
                    try:
                        value = path.relative_to(root).as_posix()
                    except ValueError:
                        raise WorkbenchError("Select baseline inputs inside the workspace.") from None
                return read_baseline(local_path(root, value))

            if arguments.assurance_command == "compare":
                _print_json(compare_baselines(baseline(arguments.before), baseline(arguments.after), root))
                return 0
            payload = baseline(arguments.baseline)
            result = analyze_baseline(payload, root)
            if arguments.assurance_command == "save":
                result["saved_path"] = save_baseline(payload, root).relative_to(root).as_posix()
            _print_json(result)
            return 0 if result["valid"] and (not getattr(arguments, "require_current", False)
                                            or result["freshness"] == "CURRENT") else 1
        if arguments.command == "graph":
            from .relationships.skill import load_graph_tool
            root = Path(arguments.workspace).expanduser().resolve()
            from .workspace import load_workspace
            load_workspace(root)
            build_graph = load_graph_tool("generate_all_graphs", root).main
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
