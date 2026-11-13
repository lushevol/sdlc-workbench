"""Retain each completed real-data reference check before starting the next case."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
base = root / 'docs/evidence/conversation-improvements-implementation-20261030/stage-1'
output = base / sys.argv[2]
output.mkdir(exist_ok=False)
source = root / 'tasks/portal-background-session-20261019/evidence/remaining-execution-20261029/aggregate/final-inventory.json'
original = {r['id']: r for r in json.loads(source.read_text())['rows']}
source_paths = [root / p for p in ['core/review_index.py', 'core/schemas/review-index.schema.json', 'core/cli.py', 'core/assurance.py', 'core/models.py', 'core/workspace.py', 'core/context/catalogs.py']]
source_paths.append(Path(__file__).resolve())
progress = {'completed': [], 'pending': ['IDX-SESSION', 'IDX-CES']}
for case_id, filename in [('IDX-SESSION', 'session-refresh-index.json'), ('IDX-CES', 'ces-migration-index.json')]:
    case_dir = output / case_id
    case_dir.mkdir()
    started = datetime.now(timezone.utc).isoformat()
    path = base / filename
    payload = json.loads(path.read_text())
    command = [sys.executable, '-m', 'ai_sdlc_workbench.cli', '--workspace', str(root), 'assurance', 'index', '--input', str(path.relative_to(root)), '--require-current']
    process = subprocess.run(command, cwd=root, capture_output=True)
    (case_dir / 'stdout.json').write_bytes(process.stdout)
    (case_dir / 'stderr.txt').write_bytes(process.stderr)
    report = json.loads(process.stdout)
    checks = {'command_succeeded': process.returncode == 0, 'valid_current_references': report['valid'] and report['freshness'] == 'CURRENT', 'business_not_verified': report['verification'] == 'NOT_VERIFIED'}
    if case_id == 'IDX-SESSION':
        checks['six_real_cases'] = len(payload['executions']) == 6
        checks['original_outcomes_preserved'] = all(r['outcome'] == {'PARTIALLY_EXECUTED': 'PARTIAL'}.get(original[r['case_id']]['status'], original[r['case_id']]['status']) for r in payload['executions'])
        checks['original_status_characterization_preserved'] = all(r['original_status'] == original[r['case_id']]['original_status'] and r['characterization'] == original[r['case_id']]['characterization'] for r in payload['executions'])
        issues = {r['id']: r for r in payload['assessment']['issues']}
        checks['security_hold_preserved'] = issues['RN-S002']['release_blocking'] is True
        checks['lower_priority_preserved'] = issues['RN-A001']['priority'] == 'P4' and issues['RN-A001']['release_blocking'] is False
    else:
        checks['unknown_scope_preserved'] = set(report['inventory_completeness'].values()) == {'UNKNOWN'}
        checks['draft_criterion_preserved'] = [r['id'] for r in payload['criteria']] == ['MIG-AC-001']
        checks['no_invented_execution_or_release'] = not report['records']['executions'] and 'assessment' not in report
    paths = source_paths + [path, case_dir / 'stdout.json', case_dir / 'stderr.txt']
    receipt = {'case_id': case_id, 'status': 'PASSED' if all(checks.values()) else 'FAILED', 'started_at': started, 'completed_at': datetime.now(timezone.utc).isoformat(), 'command': command, 'exit_code': process.returncode, 'checks': checks, 'source_revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(), 'candidate_state': 'Stage source hashes bind these uncommitted checks.', 'files': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}, 'limits': ['Real retained task evidence checks harness reference behavior.', 'No new business execution, target parity, publication, or deployment approval.']}
    (case_dir / 'result.json').write_text(json.dumps(receipt, indent=2) + '\n')
    progress['completed'].append({'case_id': case_id, 'status': receipt['status'], 'result': str((case_dir / 'result.json').relative_to(root))})
    progress['pending'].remove(case_id)
    (output / 'progress.json').write_text(json.dumps(progress, indent=2) + '\n')
    print(case_id + ': ' + receipt['status'], flush=True)
    if receipt['status'] != 'PASSED':
        raise SystemExit(1)
