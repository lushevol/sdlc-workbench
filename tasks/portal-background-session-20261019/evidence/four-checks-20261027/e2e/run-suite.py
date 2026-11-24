from pathlib import Path
import subprocess,json,os,re,datetime,hashlib,sys,urllib.request,time
root=Path.cwd();evidence=root/'tasks/portal-background-session-20261019/evidence/four-checks-20261027/e2e';runtime=root/'.workbench/four-checks-e2e-20261027';binding=json.loads((evidence/'source-binding.json').read_text());source=Path(binding['source'])
assert all(hashlib.sha256((source/k).read_bytes()).hexdigest()==v for k,v in binding['files'].items())
secret_source=(root/'.workbench/portal-session-real-20261019/local-bff/runner/local/portalsession/LocalSessionApplication.java').read_text();env=os.environ.copy()
for field,key in [('USER','SESSION_E2E_USERNAME'),('PASSWORD','SESSION_E2E_PASSWORD')]:env[key]=re.search(r'public static final String '+field+r'="([^"]+)"',secret_source).group(1)
label=sys.argv[1];modes=sys.argv[2:];runner=root/'.workbench/session-delivery-20261026/browser-runner.mjs'
if label=='headless':runner=root/'.workbench/session-delivery-20261026/headless-runner.mjs'
for mode in modes:
 identity=label+'-'+mode+'-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S');out=evidence/identity;out.mkdir()
 default=root/'.workbench/session-delivery-20261026/candidate/config.json'
 if label in ['natural','original']:default=root/'tasks/portal-background-session-20261019/evidence/ut-remediation-20261027/final-cancellation-browser/rerun-matching-original-fixture/config.json'
 config=json.loads(default.read_text());port=8141 if label in ['natural','original'] else 8143;config['targetUrl']=f'http://127.0.0.1:{port}/';config['loginUrl']=f'http://127.0.0.1:{port}/?show_normal_login=Y';config['artifactDir']=str(out/'artifacts');config['sourceRevisions']['mfe-base']=binding['candidate_commit'];config['timingProfile']['expectedRefreshLifetimeSeconds']=None
 if label=='headless' and mode=='cancelledLoader':
  config=json.loads((root/'tasks/portal-background-session-20261019/evidence/ut-remediation-20261027/final-cancellation-browser/rerun-matching-original-fixture/config.json').read_text());config['targetUrl']='http://127.0.0.1:8141/';config['loginUrl']='http://127.0.0.1:8141/?show_normal_login=Y';config['artifactDir']=str(out/'artifacts')
 (out/'config.json').write_text(json.dumps(config,indent=2)+'\n');env['SESSION_E2E_OUTPUT']=str(out/'native');env['SESSION_E2E_CONFIG']=str(out/'config.json')
 if mode in ['staleSuccess','staleError','delayed']:env['SESSION_EXTENSION']=str(root/'.workbench/session-minor-fixes-20261025/sessionRenewal.minor-fixes.cjs')
 else:env.pop('SESSION_EXTENSION',None)
 cmd=['node',str(runner),mode,'natural' if label in ['natural','original'] else 'fast',identity]
 meta={'id':identity,'mode':mode,'label':label,'candidate_commit':binding['candidate_commit'],'status':'RUNNING','started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'source_binding':'../source-binding.json','clock':'REAL_WALL_CLOCK','env_names':['SESSION_E2E_USERNAME','SESSION_E2E_PASSWORD','SESSION_E2E_OUTPUT','SESSION_E2E_CONFIG','SESSION_EXTENSION'],'credentials_retained':False}
 (out/'case-summary.json').write_text(json.dumps(meta,indent=2)+'\n');(evidence/'progress.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({'starting':identity}),flush=True)
 with (out/'stdout.log').open('w') as stream:completed=subprocess.run(cmd,cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT)
 record=json.loads((out/'native/run.json').read_text()) if (out/'native/run.json').exists() else {};meta.update({'status':record.get('status','EXECUTION_ERROR'),'exit_code':completed.returncode,'error':record.get('error'),'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artifacts':{str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file() and p.name!='case-summary.json'}})
 (out/'case-summary.json').write_text(json.dumps(meta,indent=2)+'\n');inventory=json.loads((evidence/'inventory.json').read_text()) if (evidence/'inventory.json').exists() else {'candidate_commit':binding['candidate_commit'],'cases':[]};inventory['cases'].append({k:meta[k] for k in ['id','mode','label','status','exit_code','error']});(evidence/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n');(evidence/'progress.json').write_text(json.dumps({'status':'CASE_RETAINED','case':identity,'outcome':meta['status']},indent=2)+'\n');print(json.dumps({'finished':identity,'status':meta['status'],'error':meta['error']}),flush=True)
 if not list((out/'artifacts').glob('*/result.json')):raise SystemExit('No retained assertion/setup result; stop for diagnosis.')
 if record.get('error') and any(x in record['error'] for x in ['Portal sign-in did not complete','timing preflight failed','Configure ']):raise SystemExit('Stop for setup diagnosis.')
