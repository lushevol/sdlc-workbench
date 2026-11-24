from pathlib import Path
import json,os,re,subprocess,datetime,hashlib,urllib.request,time
root=Path.cwd();evidence=root/'tasks/portal-background-session-20261019/evidence/ut-remediation-20261027/final-cancellation-browser';runtime=root/'.workbench/ut-final-cancellation-20261027'
started=datetime.datetime.now(datetime.timezone.utc).isoformat();opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
ready={}
for port,path in [(8142,'/base.js'),(8143,'/')]:
 failure=None
 for attempt in range(30):
  try:
   response=opener.open('http://127.0.0.1:'+str(port)+path,timeout=5);data=response.read();ready[str(port)]={'status':response.status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()};break
  except Exception as error:failure=str(error);time.sleep(1)
 else:raise RuntimeError('Local server readiness failed on '+str(port)+': '+failure)
(evidence/'readiness.json').write_text(json.dumps({'started_at':started,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ports':ready},indent=2)+'\n')
source=(root/'.workbench/portal-session-real-20261019/local-bff/runner/local/portalsession/LocalSessionApplication.java').read_text();env=os.environ.copy()
for field,key in [('USER','SESSION_E2E_USERNAME'),('PASSWORD','SESSION_E2E_PASSWORD')]:env[key]=re.search(r'public static final String '+field+r'="([^"]+)"',source).group(1)
env['SESSION_E2E_OUTPUT']=str(evidence/'native');env['SESSION_E2E_CONFIG']=str(evidence/'config.json')
cmd=['node',str(root/'.workbench/session-delivery-20261026/headless-runner.mjs'),'cancelledLoader','natural','final-cancellation-20261027']
(evidence/'command.json').write_text(json.dumps({'argv':cmd,'cwd':str(root),'env_names':['SESSION_E2E_USERNAME','SESSION_E2E_PASSWORD','SESSION_E2E_OUTPUT','SESSION_E2E_CONFIG'],'credentials_retained':False,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
with (evidence/'stdout.log').open('w') as stream:
 result=subprocess.run(cmd,cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=100)
record=json.loads((evidence/'native/run.json').read_text()) if (evidence/'native/run.json').exists() else {}
summary={'started_at':started,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':result.returncode,'status':record.get('status','ERROR'),'error':record.get('error'),'candidate_commit':'1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303','artifacts':{str(p.relative_to(evidence)):hashlib.sha256(p.read_bytes()).hexdigest() for p in evidence.rglob('*') if p.is_file() and p.name not in ['execution.json','mfe.log','root.log']}}
(evidence/'execution.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:summary[k] for k in ['exit_code','status','error']}));raise SystemExit(result.returncode)
