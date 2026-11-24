from pathlib import Path
import datetime,gzip,hashlib,json,os,re,signal,socket,subprocess,time,urllib.request
root=Path.cwd();out=root/'tasks/ui-test-coverage-20261022/evidence/screenshot-review-20261022/environment';launcher=25620
r=subprocess.run(['ps','-p',str(launcher),'-o','pid=','-o','command='],capture_output=True,text=True)
expected='python3 e2e/scripts/local-audit-stack.py --config tasks/ui-test-coverage-20261022/evidence/screenshot-review-20261022/environment/stack-config-03.json --output tasks/ui-test-coverage-20261022/evidence/screenshot-review-20261022/environment/launch-03'
assert r.returncode==0 and 'local-audit-stack.py --config tasks/ui-test-coverage-20261022/evidence/screenshot-review-20261022/environment/stack-config-03.json --output tasks/ui-test-coverage-20261022/evidence/screenshot-review-20261022/environment/launch-03' in r.stdout, 'Launcher identity differs; no process stopped.'
record={'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'launcherPid':launcher,'identityCheck':{'exitCode':r.returncode,'stdout':r.stdout,'stderr':r.stderr},'action':'SIGTERM to verified owned launcher; launcher stops owned groups only'}
os.kill(launcher,signal.SIGTERM)
for _ in range(60):
 d=json.loads((out/'launch-03/stack-lifecycle.json').read_text())
 if d.get('servicesStopped'):break
 time.sleep(.5)
else:raise RuntimeError('Owned launcher shutdown did not complete within30seconds')
record['lifecycleStatus']=d['status'];record['servicesStopped']=d.get('servicesStopped');record['portChecks']=[]
for port in [8122,8124,8125,8128,8129,8090,54390]:
 with socket.socket() as s:available=s.connect_ex(('127.0.0.1',port))==0
 record['portChecks'].append({'port':port,'listenerPresentAfterShutdown':available})
record['retainedLogs']=[]
logs=root/'.workbench/screenshot-review-runtime-20261022/logs-03'
for name in ['bff']:
 p=logs/(name+'.log');data=p.read_bytes();assert not re.search(rb'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+|-----BEGIN .*PRIVATE KEY-----',data), 'Sensitive material detected; retain hashes only pending review';target=out/(name+'-runtime-03.log.gz');target.write_bytes(gzip.compress(data,mtime=0));record['retainedLogs'].append({'path':str(target.relative_to(root)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'rawSha256':hashlib.sha256(data).hexdigest(),'rawBytes':len(data)})
record['finishedAt']=datetime.datetime.now(datetime.timezone.utc).isoformat();record['status']='STOPPED' if not any(x['listenerPresentAfterShutdown'] for x in record['portChecks']) else 'CHECK_REQUIRED'
(out/'shutdown-03.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':record['status'],'servicesStopped':record['servicesStopped'],'portChecks':record['portChecks']}))
