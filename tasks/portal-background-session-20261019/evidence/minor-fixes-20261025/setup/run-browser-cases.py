#!/usr/bin/env python3
"""Run selected local cases and retain every completed result before starting another case."""
import argparse,datetime,fcntl,hashlib,json,os,re,subprocess,urllib.request
from pathlib import Path
root=Path.cwd();stage=root/'tasks/portal-background-session-20261019/evidence/minor-fixes-20261025';runtime=root/'.workbench/session-minor-fixes-20261025';original=root/'.workbench/session-active-cutoff-fix-20261024'
parser=argparse.ArgumentParser();parser.add_argument('--stage',required=True);parser.add_argument('--ref',required=True);parser.add_argument('--binding',required=True);parser.add_argument('--execution-scope',default='NATIVE_BROWSER');parser.add_argument('modes',nargs='+');args=parser.parse_args()
native_lock=Path('/tmp/session-minor-fixes-native.lock').open('w');fcntl.flock(native_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
ref=subprocess.check_output(['git','-C',str(root/'repos/ui/mfe-base'),'rev-parse',args.ref],text=True).strip();binding_path=root/args.binding;binding=json.loads(binding_path.read_text());assert binding['candidate_ref']==ref
for name,digest in binding['files'].items():assert hashlib.sha256((root/binding['fixture_source']/name).read_bytes()).hexdigest()==digest,name
source=(root/'.workbench/session-post-change-20261020/bff-fast/runner/local/portalsession/LocalSessionApplication.java').read_text();env=os.environ.copy()
for field,key in [('USER','SESSION_E2E_USERNAME'),('PASSWORD','SESSION_E2E_PASSWORD')]:env[key]=re.search(r'public static final String '+field+r'="([^"]+)"',source).group(1)
result_root=stage/args.stage/'browser';result_root.mkdir(parents=True,exist_ok=True)
old=json.loads((root/'tasks/portal-background-session-20261019/evidence/active-cutoff-fix-20261024/case-inventory.json').read_text())
original_by_mode={c['mode']:c for c in old['cases']}
for mode in args.modes:
 identity=args.stage+'-'+mode+'-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S');out=result_root/identity;out.mkdir();profile='natural' if mode in ['natural','staleSuccess','staleError'] else 'fast'
 config=json.loads((runtime/f'config-{profile}.json').read_text());config['sourceRevisions']['mfe-base']=ref;config['artifactDir']=str(out/'artifacts');config_path=out/'config.json';config_path.write_text(json.dumps(config,indent=2)+'\n')
 metadata={'id':identity,'mode':mode,'status':'RUNNING','started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_ref':ref,'source_binding':{'path':str(binding_path.relative_to(root)),'sha256':hashlib.sha256(binding_path.read_bytes()).hexdigest()},'test_source_sha256':hashlib.sha256((runtime/'sessionRenewal.minor-fixes.cjs').read_bytes()).hexdigest(),'runner_sha256':hashlib.sha256((runtime/'browser-runner.mjs').read_bytes()).hexdigest(),'profile':profile,'clock':'REAL_WALL_CLOCK','execution_scope':args.execution_scope,'environment_limits':['Physical user UI and native lifecycle are not verified while macOS is locked.'] if args.execution_scope=='DOM_SERVICE_ONLY_LOCKED_MAC' else []}
 if mode in original_by_mode:metadata['prior_original_case']={k:original_by_mode[mode].get(k) for k in ['id','candidate_business_outcome','candidate_result','candidate_error']}
 (out/'source-binding.json').write_text(json.dumps(metadata,indent=2)+'\n')
 (stage/args.stage/'progress.json').write_text(json.dumps({'status':'RUNNING','case':identity,'mode':mode,'retained_at':str(out),'source_binding':metadata['source_binding'],'resume':'Inspect native/run.json and any artifacts/*/long-wait-checkpoint.json before resuming.'},indent=2)+'\n')
 print(json.dumps({'starting':mode,'id':identity,'profile':profile,'retained_at':str(out)}),flush=True)
 env['SESSION_E2E_OUTPUT']=str(out/'native');env['SESSION_E2E_CONFIG']=str(config_path)
 command=['node',str(runtime/'browser-runner.mjs'),mode,profile,identity]
 (out/'command.json').write_text(json.dumps({'argv':command,'cwd':str(root),'env_names':['SESSION_E2E_USERNAME','SESSION_E2E_PASSWORD','SESSION_E2E_OUTPUT','SESSION_E2E_CONFIG'],'credentials_retained':False},indent=2)+'\n')
 with (out/'stdout.txt').open('w') as stdout:run=subprocess.run(command,cwd=root,env=env,stdout=stdout,stderr=subprocess.STDOUT)
 native=out/'native/run.json';record=json.loads(native.read_text()) if native.exists() else {};results=list((out/'artifacts').glob('*/result.json')) if (out/'artifacts').exists() else []
 metadata.update({'status':record.get('status','EXECUTION_ERROR'),'exit_code':run.returncode,'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'error':record.get('error'),'results':[str(p.relative_to(stage)) for p in results],'artifacts':{str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file() and p.name!='case-summary.json'}})
 (out/'case-summary.json').write_text(json.dumps(metadata,indent=2)+'\n')
 inventory_path=stage/args.stage/'browser-inventory.json';inventory=json.loads(inventory_path.read_text()) if inventory_path.exists() else {'cases':[]};inventory['cases'].append({'id':identity,'mode':mode,'status':metadata['status'],'result':str((out/'case-summary.json').relative_to(stage))});inventory['updated_at']=metadata['completed_at'];inventory_path.write_text(json.dumps(inventory,indent=2)+'\n')
 (stage/args.stage/'progress.json').write_text(json.dumps({'status':'CASE_RETAINED','case':identity,'mode':mode,'outcome':metadata['status'],'inventory':str(inventory_path.relative_to(stage))},indent=2)+'\n')
 print(json.dumps({'finished':mode,'status':metadata['status'],'error':metadata['error'],'retained_at':str(out)}),flush=True)
 if metadata['status']!='PASSED' and (not results or 'page.waitForFunction: Timeout' in (metadata['error'] or '') or 'Portal sign-in did not complete' in (metadata['error'] or '')):
  print(json.dumps({'stopped_for_setup_review':identity,'error':metadata['error']}),flush=True)
  raise SystemExit(2)
