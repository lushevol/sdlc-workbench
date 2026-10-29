"""Use existing local fixture credentials privately for security browser cases."""
from pathlib import Path
from datetime import datetime, timezone
import json, os, re, subprocess
root=Path(__file__).resolve().parents[5]
out=Path(__file__).resolve().parent
text=(root/'.workbench/portal-session-real-20261019/local-bff/runner/local/portalsession/LocalSessionApplication.java').read_text()
env=os.environ.copy();env['PW_TEST_SCREENSHOT_NO_FONTS_READY']='1'
for field,key in [('USER','SESSION_E2E_USERNAME'),('PASSWORD','SESSION_E2E_PASSWORD')]:env[key]=re.search(r'public static final String '+field+r'="([^"]+)"',text).group(1)
record={'started_at':datetime.now(timezone.utc).isoformat(),'credentials_retained':False}
with (out/'browser-run.log').open('w') as log:
    run=subprocess.run(['node',str(out/'browser-security.mjs')],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
record.update(exit_code=run.returncode,completed_at=datetime.now(timezone.utc).isoformat())
(out/'browser-runner.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
