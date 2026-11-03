"""Retain bounded setup checks against the prepared isolated source fixture."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import venv

root = Path.cwd()
evidence = root / 'docs/evidence/dependency-setup-maintenance-20261103'
base = Path('/private/tmp/dependency-setup-maintenance-20261103')
source = base / 'fresh source with spaces'
shutil.copy2(root / 'core/bootstrap.py', source / 'core/bootstrap.py')
shutil.copy2(root / 'core/doctor.py', source / 'core/doctor.py')
launcher = base / 'launcher' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')


def snapshot():
    return {str(path.relative_to(source)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in source.rglob('*') if path.is_file()}


def run_case(case, flags, *, selected_python=None):
    before = snapshot()
    command = [str(launcher), '-B', str(source / 'core/bootstrap.py'), '--check', *flags]
    result = subprocess.run(command, cwd=base, text=True, capture_output=True, timeout=30,
                            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1',
                                 'AZURE_DEVOPS_PAT': 'SETUP_PROBE_PRIVATE_VALUE'})
    assert result.returncode == 1, result.stderr
    assert 'Traceback' not in result.stderr
    assert 'SETUP_PROBE_PRIVATE_VALUE' not in result.stdout + result.stderr
    assert snapshot() == before
    assert not (source / '.workbench').exists()
    assert not (source / '.env').exists()
    if '--json' in flags:
        report = json.loads(result.stdout)
        assert report['core_status'] == 'INCOMPLETE'
        assert report['diagnostic_source'] == 'source'
        checks = next(feature['checks'] for feature in report['features'] if feature['id'] == 'core')
        assert all(check['status'] == 'INCOMPLETE' for check in checks if check['id'].startswith('package:'))
        assert len([check for check in checks if check['id'].startswith('package:')]) == 5
        if selected_python:
            assert report['diagnostic_python'] == str(selected_python)
    else:
        assert 'Install PyYAML==6.0.2' in result.stdout
        assert 'Core: INCOMPLETE' in result.stdout
    record = {'case': case, 'command': command, 'exit_code': result.returncode,
              'stdout': result.stdout, 'stderr': result.stderr, 'assertions': 'PASS',
              'source_unchanged': True, 'setup_state_created': False,
              'limits': 'Isolated local fixture and synthetic credential marker; no live access or package downloads.'}
    (evidence / (case + '.json')).write_text(json.dumps(record, indent=2) + '\n')
    print(case, 'PASS')


run_case('fresh-checkout-candidate', ['--core-only'])
assert not (source / '.venv').exists()
run_case('fresh-checkout-json', ['--core-only', '--json'], selected_python=launcher)
run_case('fresh-checkout-all-json', ['--json'], selected_python=launcher)
venv.EnvBuilder(with_pip=False).create(source / '.venv')
project_python = source / '.venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
run_case('missing-installed-runtime', ['--core-only', '--json'], selected_python=project_python)
