"""Stop only the verified BFF and PostgreSQL processes created for this local audit."""
from pathlib import Path
import datetime
import json
import os
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[3]
BASE = WORKSPACE / '.workbench/current-bff-audit'
TARGET = ROOT / 'current-bff-build/shutdown.json'
if TARGET.exists():
    raise SystemExit('Shutdown evidence already exists; do not overwrite.')
result = {'recordedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'VERIFYING', 'checks': []}


def retain():
    TARGET.write_text(json.dumps(result, indent=2) + '\n')


def run(command):
    p = subprocess.run(command, text=True, capture_output=True)
    entry = {'command': command, 'exitCode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
    result['checks'].append(entry)
    retain()
    return p


bff_pid = json.loads((BASE / 'runtime-start.json').read_text())['pid']
pg_pid = int((BASE / 'pg-data/postmaster.pid').read_text().splitlines()[0])
bff = run(['ps', '-p', str(bff_pid), '-o', 'pid=', '-o', 'command='])
pg = run(['ps', '-p', str(pg_pid), '-o', 'pid=', '-o', 'command='])
bff_port = run(['lsof', '-nP', '-iTCP:8090', '-sTCP:LISTEN', '-t'])
pg_port = run(['lsof', '-nP', '-iTCP:54390', '-sTCP:LISTEN', '-t'])
assert bff.returncode == 0 and str(BASE / 'classes') in bff.stdout and 'local.portalsession.LocalSessionApplication' in bff.stdout
assert pg.returncode == 0 and 'postgres' in pg.stdout and '.workbench/current-bff-audit/pg-data' in pg.stdout
assert bff_port.stdout.strip() == str(bff_pid) and pg_port.stdout.strip() == str(pg_pid)
result.update(status='OWNERSHIP_VERIFIED', bffPid=bff_pid, postgresPid=pg_pid)
retain()
os.kill(bff_pid, signal.SIGTERM)
for _ in range(100):
    check = subprocess.run(['kill', '-0', str(bff_pid)], capture_output=True)
    if check.returncode != 0:
        break
    time.sleep(.1)
bff_port_after = run(['lsof', '-nP', '-iTCP:8090', '-sTCP:LISTEN', '-t'])
assert not bff_port_after.stdout.strip(), 'BFF port remains occupied; do not stop database before Java shutdown.'
stop = run(['/opt/homebrew/bin/pg_ctl', '-D', str(BASE / 'pg-data'), '-m', 'fast', '-t', '30', '-w', 'stop'])
assert stop.returncode == 0
pg_port_after = run(['lsof', '-nP', '-iTCP:54390', '-sTCP:LISTEN', '-t'])
assert not pg_port_after.stdout.strip()
result.update(status='STOPPED', endedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              limits=['Only the verified isolated audit BFF and PostgreSQL processes were targeted.',
                      'No business checkout source or existing report was deleted.'])
retain()
print(json.dumps({'status': result['status'], 'bffPid': bff_pid, 'postgresPid': pg_pid, 'evidence': str(TARGET)}, indent=2))
