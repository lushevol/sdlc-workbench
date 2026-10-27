from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, time

trial = Path('/tmp/mfe-ut-remediation-20261027-qposcs1f')
main = Path('/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-base')
evidence = Path(__file__).resolve().parent
reporter = Path('/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/portal-background-session-20261019/evidence/delivery-confidence-20261026/unit/case-reporter.cjs')
node = '/Users/lushevol/.nvm/versions/node/v24.16.0/bin/node'
tests = [
    'src/pages/Home/common/sessionTimingPreservation.test.tsx',
    'src/pages/Home/common/sessionLifecycle.test.tsx',
    'src/pages/Home/common/sessionRefresh.test.tsx',
]
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def source_manifest():
    return {str(path.relative_to(trial)): digest(path) for path in sorted((trial / 'src').rglob('*')) if path.is_file()}
source_before = source_manifest()
configs = ['package.json', 'jest.config.ts', 'jest.setup.tsx', 'babel.config.json', 'tsconfig.json']
binding = {
    'recorded_at': datetime.now(timezone.utc).isoformat(),
    'baseline_commit': 'b8d4f1b837c6388452fbdc540f311257e805f932',
    'trial_checkout': str(trial),
    'application_checkout': str(main),
    'application_edits_performed': False,
    'test_files': [{'path': name, 'sha256': digest(trial / name), 'matches_application': (trial / name).read_bytes() == (main / name).read_bytes()} for name in tests],
    'source_sha256': source_before,
    'config_sha256': {name: digest(trial / name) for name in configs},
    'reporter': {'path': str(reporter), 'sha256': digest(reporter)},
    'node_version': subprocess.check_output([node, '--version'], text=True).strip(),
    'dependencies': {},
    'limits': ['The temporary checkout includes the separate isolated cancellation correction.', 'No PROD artifact or target environment is bound.'],
}
for package in ['jest', 'axios', 'react', 'react-dom', '@testing-library/react']:
    package_file = trial / 'node_modules' / package / 'package.json'
    package_data = json.loads(package_file.read_text())
    binding['dependencies'][package] = {'version': package_data['version'], 'manifest_sha256': digest(package_file)}
assert all(item['matches_application'] for item in binding['test_files'])
(evidence / 'source-binding.json').write_text(json.dumps(binding, indent=2) + '\n')
command = [node, 'node_modules/jest/bin/jest.js', '--runInBand', '--coverage=false', '--ci', '--detectOpenHandles', '--runTestsByPath', *tests, '--json', '--outputFile=' + str(evidence / 'results.json'), '--reporters=default', '--reporters=' + str(reporter)]
run_env = os.environ.copy()
run_env['BABEL_ENV'] = 'test'
run_env['RUN_EVIDENCE_DIR'] = str(evidence)
start = datetime.now(timezone.utc).isoformat()
start_clock = time.monotonic()
(evidence / 'execution.json').write_text(json.dumps({'state': 'RUNNING', 'started_at': start, 'cwd': str(trial), 'command': command, 'environment': {'BABEL_ENV': 'test', 'RUN_EVIDENCE_DIR': str(evidence)}, 'outer_timeout': False, 'force_exit': False}, indent=2) + '\n')
with (evidence / 'runner.log').open('w') as output:
    completed = subprocess.run(command, cwd=trial, env=run_env, stdout=output, stderr=subprocess.STDOUT)
end = datetime.now(timezone.utc).isoformat()
source_after = source_manifest()
result = json.loads((evidence / 'results.json').read_text())
failures = [item['fullName'] for suite in result['testResults'] for item in suite['assertionResults'] if item['status'] == 'failed']
summary = {'state': 'COMPLETED', 'started_at': start, 'ended_at': end, 'elapsed_seconds': time.monotonic() - start_clock, 'cwd': str(trial), 'command': command, 'exit_code': completed.returncode, 'outer_timeout': False, 'force_exit': False, 'source_unchanged_during_execution': source_before == source_after, 'suites': result['numTotalTestSuites'], 'passed_suites': result['numPassedTestSuites'], 'failed_suites': result['numFailedTestSuites'], 'tests': result['numTotalTests'], 'passed_tests': result['numPassedTests'], 'failed_tests': result['numFailedTests'], 'skipped_tests': result['numPendingTests'], 'case_checkpoints': len(list((evidence / 'cases').glob('*.json'))), 'failed_test_names': failures}
(evidence / 'execution.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
raise SystemExit(completed.returncode or (0 if summary['source_unchanged_during_execution'] else 2))
