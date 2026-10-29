from pathlib import Path
import json,os,re,subprocess,datetime,hashlib,shutil
root=Path(__file__).resolve().parents[4];out=Path(__file__).resolve().parent
fixture=(root/'.workbench/portal-session-real-20261019/local-bff/runner/local/portalsession/LocalSessionApplication.java').read_text();env=os.environ.copy();env['PW_TEST_SCREENSHOT_NO_FONTS_READY']='1'
for field,key in [('USER','SESSION_E2E_USERNAME'),('PASSWORD','SESSION_E2E_PASSWORD')]:env[key]=re.search(r'public static final String '+field+r'="([^"]+)"',fixture).group(1)
attempt=out/os.environ.get('CORE_OUTPUT','core-browser');attempt.mkdir(exist_ok=True);shutil.copyfile(out/'core-browser.mjs',attempt/'runner.mjs')
r={'runner_sha256':hashlib.sha256((attempt/'runner.mjs').read_bytes()).hexdigest(),'selected':env.get('CASE_IDS'),'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'RUNNING','credentials_retained':False,'argv':['node',str(out/'core-browser.mjs')]};(attempt/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
with (attempt/'runner.log').open('w') as stream:p=subprocess.run(r['argv'],cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT)
r.update({'status':'COMPLETED','completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode});(attempt/'execution.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
