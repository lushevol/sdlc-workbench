from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, urllib.request

root=Path.cwd(); evidence=Path(__file__).parent.resolve(); output=evidence/(sys.argv[1] if len(sys.argv)>1 else 'attempt-01')
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
readiness={}
ports=[(8154,'/base.js'),(8155,'/')] if os.environ.get('AC4_COMMIT') else [(8152,'/base.js'),(8153,'/')]
for port, route in ports:
    with opener.open('http://127.0.0.1:'+str(port)+route,timeout=30) as response:
        data=response.read();readiness[str(port)]={'status':response.status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
source=(root/'.workbench/portal-session-real-20261019/local-bff/runner/local/portalsession/LocalSessionApplication.java').read_text()
environment=dict(os.environ,AC4_OUTPUT=str(output))
for field,key in [('USER','SESSION_E2E_USERNAME'),('PASSWORD','SESSION_E2E_PASSWORD')]:
    environment[key]=re.search(r'public static final String '+field+r'="([^"]+)"',source).group(1)
command=['node',str(evidence/'run.mjs')]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (evidence/(output.name+'.log')).open('w') as stream:
    result=subprocess.run(command,cwd=root,env=environment,stdout=stream,stderr=subprocess.STDOUT)
record={'started_at':started,'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command,'exit_code':result.returncode,'environment_names':['AC4_OUTPUT','SESSION_E2E_USERNAME','SESSION_E2E_PASSWORD'],'credentials_retained':False,'readiness':readiness,'runner_sha256':hashlib.sha256((evidence/'run.mjs').read_bytes()).hexdigest()}
(evidence/(output.name+'-execution.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'exit_code':result.returncode,'output':str(output)}))
raise SystemExit(result.returncode)
