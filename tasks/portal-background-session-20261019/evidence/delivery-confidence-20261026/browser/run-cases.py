from pathlib import Path
import subprocess,json,os,re,datetime,hashlib,argparse,fcntl
root=Path.cwd();runtime=root/'.workbench/session-delivery-20261026';stage=root/'tasks/portal-background-session-20261019/evidence/delivery-confidence-20261026/browser'
p=argparse.ArgumentParser();p.add_argument('label');p.add_argument('modes',nargs='+');a=p.parse_args()
if not os.environ.get('SESSION_RUNNER'):
 lock=Path('/tmp/session-delivery-native.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
binding=json.loads((stage/'source-bindings.json').read_text());ref=binding['refs'][a.label]['ref'];assert all(hashlib.sha256((root/binding['refs'][a.label]['source']/k).read_bytes()).hexdigest()==v for k,v in binding['refs'][a.label]['files'].items())
source=(root/'.workbench/session-post-change-20261020/bff-fast/runner/local/portalsession/LocalSessionApplication.java').read_text();env=os.environ.copy()
for field,key in [('USER','SESSION_E2E_USERNAME'),('PASSWORD','SESSION_E2E_PASSWORD')]:env[key]=re.search(r'public static final String '+field+r'="([^"]+)"',source).group(1)
rootout=stage/os.environ.get('SESSION_CASE_LABEL',a.label);rootout.mkdir(exist_ok=True)
for mode in a.modes:
 identity=a.label+'-'+mode+'-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S');out=rootout/identity;out.mkdir()
 config=json.loads(Path(os.environ.get('SESSION_CONFIG_FILE',str(runtime/a.label/'config.json'))).read_text());config['artifactDir']=str(out/'artifacts');config['timingProfile']['expectedRefreshLifetimeSeconds']=None;(out/'config.json').write_text(json.dumps(config,indent=2)+'\n')
 env['SESSION_E2E_OUTPUT']=str(out/'native');env['SESSION_E2E_CONFIG']=str(out/'config.json')
 if mode in ['staleSuccess','staleError','delayed']:env['SESSION_EXTENSION']=str(root/'.workbench/session-minor-fixes-20261025/sessionRenewal.minor-fixes.cjs')
 else:env.pop('SESSION_EXTENSION',None)
 meta={'id':identity,'label':a.label,'mode':mode,'ref':ref,'status':'RUNNING','started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'test_extension':env.get('SESSION_EXTENSION','repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/sessionRenewal.cjs'),'clock':'REAL_WALL_CLOCK','limits':['Local shortened lifetime fixture; no PROD parity claim.','Native Edge is attached through CDP.'], 'source_binding':'../../source-bindings.json'}
 (out/'case-summary.json').write_text(json.dumps(meta,indent=2)+'\n');(stage/'progress.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({'starting':identity}),flush=True)
 cmd=['node',os.environ.get('SESSION_RUNNER',str(runtime/'browser-runner.mjs')),mode,'fast',identity]
 (out/'command.json').write_text(json.dumps({'argv':cmd,'cwd':str(root),'env_names':['SESSION_E2E_USERNAME','SESSION_E2E_PASSWORD','SESSION_E2E_OUTPUT','SESSION_E2E_CONFIG','SESSION_EXTENSION'],'credentials_retained':False},indent=2)+'\n')
 with (out/'stdout.txt').open('w') as f:
  run=subprocess.run(cmd,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT)
 native=out/'native/run.json';record=json.loads(native.read_text()) if native.exists() else {};results=list((out/'artifacts').glob('*/result.json'))
 meta.update({'status':record.get('status','EXECUTION_ERROR'),'exit_code':run.returncode,'error':record.get('error'),'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':[str(x.relative_to(stage)) for x in results],'artifacts':{str(x.relative_to(out)):hashlib.sha256(x.read_bytes()).hexdigest() for x in out.rglob('*') if x.is_file() and x.name!='case-summary.json'}})
 (out/'case-summary.json').write_text(json.dumps(meta,indent=2)+'\n');inventory=rootout/'inventory.json';d=json.loads(inventory.read_text()) if inventory.exists() else {'ref':ref,'cases':[]};d['cases'].append({'id':identity,'mode':mode,'status':meta['status'],'error':meta['error'],'summary':str((out/'case-summary.json').relative_to(stage))});inventory.write_text(json.dumps(d,indent=2)+'\n');(stage/'progress.json').write_text(json.dumps({'status':'CASE_RETAINED','case':identity,'outcome':meta['status']},indent=2)+'\n');print(json.dumps({'finished':identity,'status':meta['status'],'error':meta['error']}),flush=True)
 if not results:raise SystemExit('Stopped: setup produced no retained case result.')
 if record.get('error') and ('Portal sign-in did not complete' in record['error'] or 'timing preflight failed' in record['error'] or 'Configure ' in record['error']):raise SystemExit('Stopped for setup diagnosis.')
