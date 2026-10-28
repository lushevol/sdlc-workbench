"""Use the existing synthetic identity fixture without retaining credentials."""
from pathlib import Path
import datetime, json, os, re, subprocess
ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
fixture = (ROOT / '.workbench/portal-session-real-20261019/local-bff/runner/local/portalsession/LocalSessionApplication.java').read_text()
env = os.environ.copy()
env['PW_TEST_SCREENSHOT_NO_FONTS_READY'] = '1'
for field, key in [('USER', 'SESSION_E2E_USERNAME'), ('PASSWORD', 'SESSION_E2E_PASSWORD')]:
    env[key] = re.search(r'public static final String ' + field + r'="([^"]+)"', fixture).group(1)
record = {'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'credentials_retained': False, 'status': 'RUNNING'}
with (OUT / 'new-e2e-runner.log').open('w') as stream:
    result = subprocess.run(['node', str(OUT / 'renewal-loop-e2e.mjs')], cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT)
record.update({'completed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'exit_code': result.returncode, 'status': 'COMPLETED'})
(OUT / 'new-e2e-execution.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record))
