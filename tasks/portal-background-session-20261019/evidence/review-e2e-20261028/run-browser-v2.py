from pathlib import Path
import re,os,subprocess,json,datetime
root=Path.cwd();evidence=root/'tasks/portal-background-session-20261019/evidence/review-e2e-20261028';out=evidence/'rerun';out.mkdir();(out/'source-binding.json').write_bytes((evidence/'source-binding.json').read_bytes());env=os.environ.copy()
secret=(root/'.workbench/portal-session-real-20261019/local-bff/runner/local/portalsession/LocalSessionApplication.java').read_text()
for field,key in [('USER','SESSION_E2E_USERNAME'),('PASSWORD','SESSION_E2E_PASSWORD')]:env[key]=re.search(r'public static final String '+field+r'="([^"]+)"',secret).group(1)
cmd=['node',str(root/'repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/supplemental/reviewE2e.mjs'),str(out),'01,03,02,04,07,17']
meta={'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'credentialsRetained':False,'status':'RUNNING'};(out/'browser-execution.json').write_text(json.dumps(meta,indent=2)+'\n')
with (out/'browser.log').open('w') as f:r=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT)
meta.update({'completedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exitCode':r.returncode,'status':'COMPLETED' if r.returncode==0 else 'RUNNER_FAILED'});(out/'browser-execution.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta))
