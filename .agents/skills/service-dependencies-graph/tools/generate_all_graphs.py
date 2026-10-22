#!/usr/bin/env python3
"""Build, validate, and atomically publish the standalone dependency graph."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if not __package__:
    runner = Path(__file__).resolve().parents[1] / 'scripts' / 'graph.py'
    os.execv(sys.executable, [sys.executable, str(runner), 'build', *sys.argv[1:]])

from .graph_query import service_catalog
from .architecture_context import (APPLIED_CONTEXT, PROVENANCE, DEFAULT_CONTEXT,
                                   load_context, write_context)

OUTPUT_RELATIVE = 'relationships/service-dependencies/generated'
RUNNER = Path(__file__).resolve().parents[1] / 'scripts' / 'graph.py'


def run(*parts: object, workspace: Path) -> None:
    command = [str(part) for part in parts]
    print('+', ' '.join(command), flush=True)
    subprocess.run(command, cwd=workspace, check=True,
                   env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})


def publish(candidate: Path, target: Path) -> None:
    if target.is_symlink():
        raise ValueError('Graph output must not replace a symbolic link')
    if target.exists() and any(target.iterdir()):
        manifest_path = target / 'manifest.json'
        try:
            manifest = json.loads(manifest_path.read_bytes())
            graph_path = target / 'graph.json'
            if (manifest.get('canonical_graph') != 'graph.json' or
                    hashlib.sha256(graph_path.read_bytes()).hexdigest() != manifest.get('graph_sha256')):
                raise ValueError('Unrecognized graph snapshot')
        except (OSError, ValueError, TypeError) as error:
            raise ValueError('Graph output must be empty or contain a valid graph snapshot') from error
    backup = target.with_name(f'.{target.name}.previous')
    if backup.exists():
        raise ValueError(f'Previous publication backup needs review: {backup}')
    if target.exists():
        target.replace(backup)
    try:
        candidate.replace(target)
    except Exception:
        if backup.exists():
            backup.replace(target)
        raise
    if backup.exists():
        shutil.rmtree(backup)


def write_ai_outputs(candidate: Path, descriptions: Path) -> None:
    graph = json.loads((candidate / 'graph.json').read_text(encoding='utf-8'))
    dependency_catalog = json.loads((candidate / 'dependencies.json').read_text(encoding='utf-8'))
    (candidate / 'services.json').write_text(
        json.dumps(service_catalog(graph, dependency_catalog), indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    if descriptions.is_file():
        shutil.copy2(descriptions, candidate / 'business-description-overrides.json')
    roles = {
        'graph.json': 'canonical_graph', 'services.json': 'ai_service_catalog',
        'dependencies.json': 'runtime_dependency_catalog',
        'business-description-context.json': 'ai_enrichment_context',
        'business-description-overrides.json': 'applied_business_descriptions',
        'summary.json': 'generation_summary', 'analysis-coverage.json': 'extraction_coverage',
        'coverage-declarations.json': 'source_declaration_audit',
        'repository-relationships.json': 'repository_relationship_projection',
        'analysis-report.md': 'human_analysis_report', 'relationship-viewer.html': 'interactive_visualization',
        APPLIED_CONTEXT: 'applied_user_architecture_context', PROVENANCE: 'user_architecture_context_provenance',
    }
    artifacts = []
    for path in sorted(item for item in candidate.rglob('*') if item.is_file()):
        relative = path.relative_to(candidate).as_posix()
        role = 'user_architecture_source_snapshot' if relative.startswith('architecture-context-sources/') else roles.get(relative, 'repository_projection')
        artifacts.append({'path': relative, 'role': role,
                          'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest = {
        'schema_version': graph['schema_version'], 'generated_at': graph['generated_at'],
        'graph_sha256': hashlib.sha256((candidate / 'graph.json').read_bytes()).hexdigest(),
        'canonical_graph': 'graph.json', 'ai_entry_point': 'services.json',
        'visualization': 'relationship-viewer.html', 'artifacts': artifacts,
    }
    if (candidate / APPLIED_CONTEXT).is_file():
        manifest['architecture_context'] = {'input': APPLIED_CONTEXT, 'provenance': PROVENANCE,
                                            'status': 'USER_REPORTED'}
    (candidate / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, default=Path.cwd())
    parser.add_argument('--repos', type=Path, help='Repository directory, relative to the workspace')
    parser.add_argument('--out', type=Path, help='Published bundle directory, relative to the workspace')
    parser.add_argument('--descriptions', type=Path, help='Optional reviewed description overrides')
    parser.add_argument('--context', type=Path, help='Optional user architecture context, relative to the workspace')
    parser.add_argument('--open', action='store_true', help='Open the published viewer')
    args = parser.parse_args(argv)
    workspace = args.workspace.expanduser().resolve()
    context_path = args.context or Path(DEFAULT_CONTEXT)
    captured_context = load_context(workspace, context_path, required=args.context is not None)

    def resolve(path: Path) -> Path:
        return (path if path.is_absolute() else workspace / path).resolve()

    repositories = resolve(args.repos or Path('repos'))
    supplied_output = args.out or Path(OUTPUT_RELATIVE)
    unresolved_output = supplied_output if supplied_output.is_absolute() else workspace / supplied_output
    if unresolved_output.is_symlink():
        raise ValueError('Graph output must not be a symbolic link')
    output = resolve(supplied_output)
    descriptions = resolve(args.descriptions or Path('relationships/service-dependencies/architecture-descriptions.json'))
    if (workspace.is_relative_to(output) or repositories.is_relative_to(output)
            or output.is_relative_to(repositories) or output.is_symlink()):
        raise ValueError('Graph output must be separate from workspace and repository source roots')
    if output.exists() and not output.is_dir():
        raise ValueError('Graph output must be a directory')
    if output.exists() and any(output.iterdir()) and not (output / 'manifest.json').is_file():
        raise ValueError('Graph output must be empty or contain a valid graph snapshot')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.service-dependencies-graph-', dir=output.parent) as temporary:
        candidate = Path(temporary) / 'bundle'
        run(sys.executable, RUNNER, '--workspace', workspace, 'tool', 'build_graph', '--workspace', workspace,
            '--repos', repositories, '--out', candidate, '--descriptions', descriptions, workspace=workspace)
        run(sys.executable, RUNNER, '--workspace', workspace, 'tool', 'prepare_ai_context', candidate / 'graph.json',
            '--output', candidate / 'business-description-context.json', workspace=workspace)
        if captured_context:
            graph = json.loads((candidate / 'graph.json').read_bytes())
            write_context(captured_context, candidate, {row['id'] for row in graph['repositories']})
            with (candidate / 'analysis-report.md').open('a', encoding='utf-8') as report:
                report.write('\n## User-reported architecture context\n\n')
                report.write('The viewer includes supplied layers, responsibilities, relationships, and boundaries.\n')
                report.write('These annotations do not change canonical graph facts or resolved repository links.\n')
                report.write('Read [the applied context](architecture-context.json) and [its evidence provenance](architecture-context-provenance.json).\n')
        run(sys.executable, RUNNER, '--workspace', workspace, 'tool', 'render_graph', candidate / 'graph.json',
            '--output', candidate / 'relationship-viewer.html', '--source-prefix',
            os.path.relpath(workspace, output) + '/', workspace=workspace)
        run(sys.executable, RUNNER, '--workspace', workspace, 'tool', 'validate_graph', candidate / 'graph.json',
            '--workspace', workspace, '--dependencies', candidate / 'dependencies.json',
            '--relationships', candidate / 'repository-relationships.json', workspace=workspace)
        from .repository_inventory import inventory, extraction_fingerprints
        coverage = json.loads((candidate / 'analysis-coverage.json').read_text(encoding='utf-8'))
        current = inventory(workspace, repositories)
        if extraction_fingerprints(coverage) != extraction_fingerprints(current):
            raise ValueError('Repository sources changed during graph generation; rebuild from stable inputs')
        current_context = load_context(workspace, context_path, required=captured_context is not None or args.context is not None)
        before = captured_context.fingerprints() if captured_context else {}
        after = current_context.fingerprints() if current_context else {}
        if before != after:
            raise ValueError('Architecture context changed during graph generation; rebuild from stable inputs')
        write_ai_outputs(candidate, descriptions)
        publish(candidate, output)
    if args.open:
        import webbrowser
        webbrowser.open((output / 'relationship-viewer.html').as_uri())
    graph = json.loads((output / 'graph.json').read_text(encoding='utf-8'))
    print(json.dumps({'output': str(output), 'viewer': str(output / 'relationship-viewer.html'),
                      'repositories': len(graph['repositories']), 'nodes': len(graph['nodes']),
                      'edges': len(graph['edges']), 'evidence': len(graph['evidence'])}, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
