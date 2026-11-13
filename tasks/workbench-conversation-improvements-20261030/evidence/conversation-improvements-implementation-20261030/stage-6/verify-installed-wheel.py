"""Verify final new commands and guides from an isolated installed wheel."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys,tempfile,zipfile
root=Path.cwd();base=Path(__file__).resolve().parent;work=Path(tempfile.mkdtemp(prefix='workbench-final-improvements-')).resolve();site=work/'installed';workspace=work/'workspace'
wheel=root/'dist/ai_sdlc_workbench-0.1.0-py3-none-any.whl';env=dict(os.environ,PYTHONPATH=str(site));steps=[]
def run(args):
 p=subprocess.run(args,cwd=work,env=env,capture_output=True,text=True);steps.append({'command':args,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});(base/'wheel-commands.json').write_text(json.dumps(steps,indent=2)+'\n');assert p.returncode==0,steps[-1];return json.loads(p.stdout) if p.stdout.lstrip().startswith('{') else p.stdout
run([sys.executable,'-m','pip','install','--no-deps','--no-index','--target',str(site),str(wheel)])
command=[sys.executable,'-m','ai_sdlc_workbench.cli'];run(command+['init',str(workspace),'--name','Completed improvement verification'])
validation=run(command+['--workspace',str(workspace),'validate']);schema=run(command+['assurance','index-schema'])
manifest=workspace/'questions.json';manifest.write_text('{"schema_version":1,"questions":[]}\n');questions=run(command+['--workspace',str(workspace),'assurance','questions','--input','questions.json'])
for args in [['graph','compare','--help'],['test','plan','--help'],['assurance','coverage','--help'],['assurance','ledger','--help'],['release-report','summary','--help']]:run(command+args)
checks={'valid_fresh_workspace':validation['status']=='VALID','guide_shipping':all((workspace/'docs'/s).is_file() for s in ['REVIEW_INDEX.md','TEST_PREFLIGHT.md','QUESTION_RECONCILIATION.md']),'schema_shipping':schema['properties']['schema_version']['const']==1,'questions_command_installed':questions['status']=='REFERENCES_COMPLETE' and questions['verification']=='NOT_VERIFIED','no_runtime_source_copied':not any((workspace/p).exists() for p in ['core/cli.py','core/question_reconciliation.py','pyproject.toml']),'no_project_tasks_copied':not (workspace/'tasks/portal-background-session-20261019').exists(),'canonical_compare_helper_shipped':(workspace/'.agents/skills/service-dependencies-graph/tools/snapshot_delta.py').is_file()}
with zipfile.ZipFile(wheel) as bundle:
 for source in ['core/cli.py','core/review_index.py','core/review_coverage.py','core/release_report_render.py','core/test_preflight.py','core/question_reconciliation.py']:
  checks['exact_module:'+source]=bundle.read('ai_sdlc_workbench/'+Path(source).name)==(root/source).read_bytes()
result={'case_id':'FINAL-WHEEL','status':'PASSED' if all(checks.values()) else 'FAILED','checked_at':datetime.now(timezone.utc).isoformat(),'checks':checks,'wheel_sha256':hashlib.sha256(wheel.read_bytes()).hexdigest(),'installation':str(site),'workspace':str(workspace),'source_hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in ['core/cli.py','scaffold.json','MANIFEST.in']},'limits':['Local macOS only. Prepared dependencies reused without registry downloads.','An empty declared question scope verifies command availability only.']};(base/'wheel-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values())
