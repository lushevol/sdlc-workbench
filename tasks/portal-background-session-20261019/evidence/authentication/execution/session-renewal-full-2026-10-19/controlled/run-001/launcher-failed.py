from pathlib import Path
import datetime,hashlib,json,os,platform,shutil,subprocess,sys
base=Path(__file__).resolve().parent
revision='4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8'
repository=base.parents[3]/'repos/ui/mfe-base'
# This script retains original pre-run bindings. It does not edit earlier run files.
run_dir=base/'run-001'
run_dir.mkdir(exist_ok=False)
def digest(path):
 return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def artifact(path):
 return {'path':str(path),'sha256':digest(path)}
def save(path,value):
 path.write_text(json.dumps(value,indent=2)+'\n')
source=base/'source-export'
source_manifest={str(path.relative_to(source)):digest(path) for path in sorted(source.rglob('*')) if path.is_file()}
save(run_dir/'source-export-manifest.json',source_manifest)
modules=['src/hooks/service/util/getEndpoint.ts','src/hooks/service/index.ts','src/hooks/service/util/extend.ts','src/pages/Home/common/useController.ts','src/components/Timeout/common/useController.ts']
for relative in modules:
 exact=subprocess.run(['git','-C',str(repository),'show',f'{revision}:{relative}'],capture_output=True,check=True).stdout
 if hashlib.sha256(exact).hexdigest()!=source_manifest[relative]: raise ValueError('Export differs from exact Git bytes: '+relative)
node=Path(shutil.which('node')).resolve()
identity_command=[str(node),'-p','JSON.stringify({node:process.version,versions:process.versions,platform:process.platform,arch:process.arch,execPath:process.execPath})']
identity_result=subprocess.run(identity_command,capture_output=True,check=True,text=True)
(run_dir/'node-identity.stdout.txt').write_text(identity_result.stdout)
(run_dir/'node-identity.stderr.txt').write_text(identity_result.stderr)
result_path=run_dir/'characterization-result.json'
binding_path=run_dir/'original-binding.json'
argv=[str(node),'--experimental-vm-modules',str(base/'run-mfe-session-characterization-successor.cjs'),str(source),str(result_path),str(binding_path)]
original_harness=base.parents[3]/'knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs'
binding={'recorded_before_run_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repository_id':'mfe-base','repository_revision':revision,'source_export':artifact(base/'mfe-base-exact-source.tar'),'source_manifest':artifact(run_dir/'source-export-manifest.json'),'expected_executed_source_sha256':{relative:source_manifest[relative] for relative in modules},'harness':artifact(base/'run-mfe-session-characterization-successor.cjs'),'predecessor_harness':artifact(original_harness),'launcher':artifact(Path(__file__)),'input':artifact(base/'fixture-inputs.json'),'config':artifact(base/'execution-config.json'),'assertion_inventory':artifact(base/'assertion-inventory.json'),'node_binary':artifact(node),'node_identity':json.loads(identity_result.stdout),'original_argv':argv,'cwd':str(base),'environment':{'os':platform.platform(),'python':sys.version,'locale':{key:os.environ.get(key) for key in ['LANG','LC_ALL','LC_CTYPE']},'private_environment_variables':'Not captured. No network credentials are required or read.'},'source_verification':'Each executed exported module SHA256 matched git show at the recorded exact revision before run.'}
save(binding_path,binding)
start=datetime.datetime.now(datetime.timezone.utc)
with (run_dir/'stdout.txt').open('wb') as stdout,(run_dir/'stderr.txt').open('wb') as stderr:
 result=subprocess.run(argv,cwd=base,stdout=stdout,stderr=stderr)
end=datetime.datetime.now(datetime.timezone.utc)
completion={'started_at':start.isoformat(),'completed_at':end.isoformat(),'exit_code':result.returncode,'original_argv':argv,'original_binding':artifact(binding_path),'stdout':artifact(run_dir/'stdout.txt'),'stderr':artifact(run_dir/'stderr.txt'),'result':artifact(result_path) if result_path.exists() else None,'source_export_unchanged':all(digest(source/path)==sha for path,sha in source_manifest.items()),'harness_unchanged':digest(base/'run-mfe-session-characterization-successor.cjs')==binding['harness']['sha256']}
save(run_dir/'completion.json',completion)
print(json.dumps(completion,indent=2))
sys.exit(result.returncode)
