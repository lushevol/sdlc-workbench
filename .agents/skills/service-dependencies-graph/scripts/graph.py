#!/usr/bin/env python3
"""Run the dependency graph skill without a parent harness or Workbench runtime."""
from __future__ import annotations

import argparse
import importlib
import importlib.util
import sys
from pathlib import Path


TOOL_MODULES = ('build_graph', 'prepare_ai_context', 'render_graph', 'validate_graph')
PACKAGE_NAME = '_service_dependencies_graph'


def load_tool(name: str):
    """Load the tools beside this script as one independent Python package."""
    tools = Path(__file__).resolve().parents[1] / 'tools'
    if PACKAGE_NAME not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            PACKAGE_NAME, tools / '__init__.py', submodule_search_locations=[str(tools)])
        if spec is None or spec.loader is None:
            raise RuntimeError('The graph skill tools package is missing.')
        package = importlib.util.module_from_spec(spec)
        sys.modules[PACKAGE_NAME] = package
        spec.loader.exec_module(package)
    return importlib.import_module(f'{PACKAGE_NAME}.{name}')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('build', add_help=False, help='Build, validate, and publish one snapshot.')
    commands.add_parser('validate', add_help=False, help='Validate a canonical graph and its projections.')
    commands.add_parser('query', add_help=False, help='Query one validated snapshot with skill-owned operations.')
    tool = commands.add_parser('tool', add_help=False, help='Run one supported internal build tool.')
    tool.add_argument('module', choices=TOOL_MODULES)
    args, remaining = parser.parse_known_args(argv)
    workspace = args.workspace.expanduser().resolve()
    if args.command == 'build':
        return load_tool('generate_all_graphs').main(['--workspace', str(workspace), *remaining])
    if args.command == 'query':
        return load_tool('snapshot').main(['--workspace', str(workspace), *remaining])
    if args.command == 'validate':
        graph_args = remaining or ['relationships/service-dependencies/generated/graph.json']
        return load_tool('validate_graph').main(['--workspace', str(workspace), *graph_args])
    return load_tool(args.module).main(remaining)


if __name__ == '__main__':
    raise SystemExit(main())
