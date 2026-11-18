"""Verify the built graph skill in an installed workspace outside the checkout."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[4]
wheel = root / 'dist/ai_sdlc_workbench-0.1.0-py3-none-any.whl'
with tempfile.TemporaryDirectory(prefix='graph-autonomous-distribution-') as temporary:
    base = Path(temporary)
    target, workspace = base / 'installed', base / 'workspace'
    env = {**os.environ, 'PYTHONPATH': str(target), 'PYTHONDONTWRITEBYTECODE': '1'}

    def run(parts):
        result = subprocess.run(parts, cwd=base, env=env, capture_output=True, text=True, timeout=60)
        assert result.returncode == 0, result.stdout + result.stderr

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
    assert not (workspace / 'pyproject.toml').exists()
    assert not list((workspace / 'core').rglob('*.py'))
    assert not list((workspace / 'tests').rglob('*.py'))
    run([sys.executable, '-m', 'ai_sdlc_workbench.cli', '--workspace', str(workspace), 'validate'])
    run([sys.executable, str(shipped / 'scripts/graph.py'), '--workspace', str(workspace), 'build', '--no-context'])

result = {
    'status': 'PASSED', 'wheel': wheel.name, 'wheel_sha256': hashlib.sha256(wheel.read_bytes()).hexdigest(),
    'matching_graph_skill_files': len(files), 'imported_installed_package_outside_checkout': True,
    'generated_workspace_omits_runtime_and_test_sources': True,
    'empty_workspace_validate_exit_code': 0, 'installed_source_only_graph_build_exit_code': 0,
    'limits': ['Uses the existing Python environment for declared dependencies.',
               'Generated core/ and tests/ retain responsibility guides without runtime source.',
               'This verifies distribution and empty-workspace operation, not service connectivity.'],
}
Path(__file__).with_name('distribution.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
