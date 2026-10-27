"""Reconcile durable case receipts as the long native observations complete."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import time

root = Path.cwd()
output = Path(__file__).resolve().parent
cases = ['natural-natural-20261027T071704', 'missing-missing-20261027T071627']
seen = set()
while len(seen) < len(cases):
    for identity in cases:
        if identity in seen:
            continue
        summary = output / identity / 'case-summary.json'
        if not summary.exists():
            continue
        data = json.loads(summary.read_text())
        if data.get('status') == 'RUNNING':
            continue
        completed = subprocess.run(['python3', str(output/'reconcile.py')], cwd=root, capture_output=True, text=True)
        entry = {'recorded_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 'case': identity, 'status': data.get('status'),
                 'summary_sha256': hashlib.sha256(summary.read_bytes()).hexdigest(),
                 'reconcile_exit_code': completed.returncode,
                 'reconcile_output': completed.stdout.strip(),
                 'reconcile_error': completed.stderr.strip()}
        (output / (identity + '-completion-checkpoint.json')).write_text(json.dumps(entry, indent=2) + '\n')
        if completed.returncode:
            raise SystemExit(completed.returncode)
        seen.add(identity)
        print(json.dumps(entry), flush=True)
    if len(seen) < len(cases):
        time.sleep(5)
print('Both lifecycle cases reconciled.', flush=True)
