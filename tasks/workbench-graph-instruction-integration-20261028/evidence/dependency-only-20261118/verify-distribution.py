"""Verify dependency-only graph distribution outside the source checkout."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


root = Path(__file__).resolve().parents[4]
wheel = root / 'dist/ai_sdlc_workbench-0.1.0-py3-none-any.whl'
retired = [
    'tools/knowledge_projection.py', 'tools/knowledge_queries.py',
    'references/architecture/knowledge-graph.md',
    'tests/test_knowledge_integration.py', 'tests/test_knowledge_projection.py',
    'tests/test_knowledge_queries.py', 'tests/test_knowledge_viewer.py',
]
operations = {'coverage', 'patterns', 'relationships', 'services', 'search', 'neighborhood'}
with tempfile.TemporaryDirectory(prefix='graph-dependency-only-distribution-') as temporary:
    base = Path(temporary)
    target, workspace = base / 'installed', base / 'workspace'
    env = {**os.environ, 'PYTHONPATH': str(target), 'PYTHONDONTWRITEBYTECODE': '1'}

    def run(parts):
        result = subprocess.run(parts, cwd=base, env=env, capture_output=True, text=True, timeout=60)
        assert result.returncode == 0, result.stdout + result.stderr
        return result

    run([sys.executable, '-m', 'pip', 'install', '--no-deps', '--no-index', '--target', str(target), str(wheel)])
    run([sys.executable, '-c', '''from pathlib import Path
import ai_sdlc_workbench
assert Path(ai_sdlc_workbench.__file__).resolve().is_relative_to(Path('installed').resolve())
from ai_sdlc_workbench.workspace import initialize_workspace
initialize_workspace(Path('workspace'))
'''])
    source = root / '.agents/skills/service-dependencies-graph'
    shipped = workspace / '.agents/skills/service-dependencies-graph'
    files = [path for path in source.rglob('*') if path.is_file()
             and '__pycache__' not in path.parts and path.suffix != '.pyc']
    for path in files:
        assert path.read_bytes() == (shipped / path.relative_to(source)).read_bytes(), path
    for relative in retired:
        assert not (shipped / relative).exists(), relative
    separate_knowledge_files = [
        '.agents/skills/llm-wiki/SKILL.md', '.agents/skills/llm-wiki/scripts/wiki.py',
        '.agents/skills/query-knowledge/SKILL.md', '.agents/skills/govern-knowledge/SKILL.md',
        'core/knowledge/schemas/knowledge-topic.schema.json', 'core/knowledge/templates/knowledge-topic.md',
    ]
    for relative in separate_knowledge_files:
        assert (workspace / relative).read_bytes() == (root / relative).read_bytes(), relative
    assert (target / 'ai_sdlc_workbench/knowledge_web/__init__.py').is_file()
    assert not (workspace / 'pyproject.toml').exists()
    assert not list((workspace / 'core').rglob('*.py'))
    assert not list((workspace / 'tests').rglob('*.py'))
    run([sys.executable, '-m', 'ai_sdlc_workbench.cli', '--workspace', str(workspace), 'validate'])
    runner = [sys.executable, str(shipped / 'scripts/graph.py'), '--workspace', str(workspace)]
    run([*runner, 'build', '--no-context'])
    output = workspace / 'relationships/service-dependencies/generated'
    assert not json.loads((output / 'graph.json').read_text())['nodes']
    api = json.loads(run([sys.executable, '-c', '''import json
from pathlib import Path
from ai_sdlc_workbench.relationships.skill import load_graph_tool
snapshot = load_graph_tool('snapshot', Path('workspace'))
rejected = []
for operation in ('knowledge', 'references', 'paths'):
    try:
        snapshot.query(Path('workspace/relationships/service-dependencies/generated'), operation, {}, Path('workspace'))
    except snapshot.SnapshotError as error:
        assert error.code == 'UNKNOWN_OPERATION'
        rejected.append(operation)
    else:
        raise AssertionError(operation)
print(json.dumps({'operations': sorted(snapshot.OPERATIONS), 'rejected': rejected}))
''']).stdout)
    assert set(api['operations']) == operations
    assert set(api['rejected']) == {'knowledge', 'references', 'paths'}
    policy = workspace / 'knowledge/records/distribution-policy.md'
    policy.parent.mkdir(parents=True, exist_ok=True)
    policy.write_text('---\ninvalid: [\n')
    client = workspace / 'repos/worker/deep/transport.custom'
    client.parent.mkdir(parents=True)
    client.write_text('import solace from "solclientjs";\n'
                      'const session = solace.SolclientFactory.createSession({\n'
                      ' url: "wss://broker.example/smf", password: "distribution-secret"\n'
                      '});\n' + 'session.send(message);\n' * 25)
    run([*runner, 'build', '--layout', 'flat', '--no-context'])
    graph = json.loads((output / 'graph.json').read_text())
    assert 'knowledge' not in graph
    assert all(set(node['dimensions']) <= {'RUNTIME', 'BUSINESS'} for node in graph['nodes'])
    assert all(edge['dimension'] in {'RUNTIME', 'BUSINESS'} for edge in graph['edges'])
    assert 'knowledge' not in (shipped / 'tools/viewer.html').read_text().casefold()

    def query(operation, arguments=None):
        return json.loads(run([*runner, 'query', operation, '--args', json.dumps(arguments or {})]).stdout)

    first = query('patterns', {'service_only': True, 'include_snippets': True, 'query': 'session.send'})
    candidate = next(row for row in first['matches'] if row['family'] == 'CALL_HINT' and row['value'] == 'session.send')
    assert candidate['source_sha256'] and candidate['occurrence_count'] == 25
    assert len(candidate['occurrences']) == 10 and candidate['next_occurrence_offset'] == 10
    assert 'distribution-secret' not in json.dumps(first)
    occurrences, page_count = candidate['occurrences'][:], 1
    while candidate['next_occurrence_offset'] is not None:
        candidate = query('patterns', {'candidate_id': candidate['id'], 'include_snippets': True,
                                      'occurrence_offset': candidate['next_occurrence_offset']})['matches'][0]
        occurrences.extend(candidate['occurrences'])
        page_count += 1
    assert len(occurrences) == 25 and len({ref['start_line'] for ref in occurrences}) == 25
    assert page_count == 3 and all(ref['snippet'] for ref in occurrences)
    assert any('SOLACE' in row['protocol_hints'] for row in
               query('patterns', {'family': 'MESSAGE_CLIENT', 'service_only': True})['matches'])
    before = query('coverage')
    assert before['freshness']['status'] == 'CURRENT' and 'knowledge_freshness' not in before
    manifest = (output / 'manifest.json').read_bytes()
    policy.write_text('A separate knowledge revision.\n')
    after = query('coverage')
    assert after['freshness']['status'] == 'CURRENT' and 'knowledge_freshness' not in after
    assert (output / 'manifest.json').read_bytes() == manifest

result = {
    'status': 'PASSED', 'wheel': wheel.name, 'wheel_sha256': hashlib.sha256(wheel.read_bytes()).hexdigest(),
    'matching_graph_skill_files': len(files), 'retired_graph_files_absent': retired,
    'separate_knowledge_files_preserved': separate_knowledge_files,
    'separate_knowledge_web_runtime_preserved': True,
    'imported_installed_package_outside_checkout': True,
    'generated_workspace_omits_runtime_and_test_sources': True,
    'empty_workspace_validate_exit_code': 0, 'installed_empty_dependency_build_exit_code': 0,
    'snapshot_operations': sorted(operations), 'retired_operations_rejected': api['rejected'],
    'installed_flat_solace_build_and_snippet_query': 'PASSED', 'occurrences_retrieved': 25,
    'occurrence_pages': page_count, 'knowledge_changes_leave_dependency_freshness_current': True,
    'limits': ['Uses the existing Python environment for declared dependencies.',
               'Generated core/ and tests/ retain responsibility guides without runtime source.',
               'This verifies distribution and static discovery, not service connectivity.'],
}
Path(__file__).with_name('distribution.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
