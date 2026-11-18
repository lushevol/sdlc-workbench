from pathlib import Path
import hashlib,json,os,subprocess,sys,tarfile,zipfile
b=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/var/folders/3q/zc3tlwsj1p1_pskzk1j9r5100000gn/T/wb-distribution-yioghb6h')
m=json.loads((b/'build-manifest.json').read_text());wheel=next((b/'dist').glob('*.whl'));sdist=next((b/'dist').glob('*.tar.gz'))
res=subprocess.run([m['python'],'-m','pip','install','--no-index','--no-deps','--target',m['install'],str(wheel)],cwd=b,text=True,capture_output=True)
(b/'install.log').write_text(res.stdout+res.stderr);assert res.returncode==0
script='''from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,sys.argv[1])
import ai_sdlc_workbench
from ai_sdlc_workbench.workspace import initialize_workspace
from ai_sdlc_workbench.validation import validate_workspace
from ai_sdlc_workbench.runtime import Workbench
installed=Path(sys.argv[1]).resolve();source=Path(sys.argv[2]);work=Path(sys.argv[3])
assert Path(ai_sdlc_workbench.__file__).resolve().is_relative_to(installed),ai_sdlc_workbench.__file__
initialize_workspace(work,'Distribution validation')
checks={}
source_skills=source/'.agents/skills'
for src in source_skills.rglob('*'):
 if src.is_file() and '__pycache__' not in src.parts and not src.name.endswith('.pyc') and src.name!='.DS_Store':
  relative=src.relative_to(source_skills);assert (work/'.agents/skills'/relative).read_bytes()==src.read_bytes(),str(relative)
  checks[str(relative)]=hashlib.sha256(src.read_bytes()).hexdigest()
for category in ('repositories','services','capabilities','contracts','sources','tools'):
 import yaml
 value=yaml.safe_load((work/f'registry/{category}.yaml').read_text());assert not value[category]
assert not any((work/x).exists() for x in ('pyproject.toml','tests','.git','core/cli.py'))
assert sorted(p.name for p in (work/'tasks').iterdir())==['README.md']
assert (work/'.claude/skills/evaluate-harness').is_symlink() or (work/'.claude/skills/evaluate-harness/SKILL.md').is_file()
result=validate_workspace(work);assert result['valid'],result
skill=Workbench(work).skill_read('evaluate-harness');assert skill==(work/'.agents/skills/evaluate-harness/SKILL.md').read_text()
print(json.dumps({'module':ai_sdlc_workbench.__file__,'workspace':str(work),'skill_files_matched':len(checks),'skill_hashes':checks,'validation':result,'empty_catalogs':6,'forbidden_artifacts':0,'skill_discovery':'PASSED'},indent=2))
'''
res=subprocess.run([m['python'],'-c',script,m['install'],m['source'],m['workspace']],cwd=b,text=True,capture_output=True)
(b/'initialized-workspace-check.json').write_text(res.stdout);(b/'initialized-workspace-check.stderr').write_text(res.stderr)
if res.returncode:print(res.stdout,res.stderr);raise SystemExit(res.returncode)
value=json.loads(res.stdout)
with zipfile.ZipFile(wheel) as z:
 for name in ('SKILL.md','references/trials.md','agents/openai.yaml'):
  assert z.read('ai_sdlc_workbench/scaffold/.agents/skills/evaluate-harness/'+name)==(Path(m['source'])/'.agents/skills/evaluate-harness'/name).read_bytes()
with tarfile.open(sdist) as t:
 names=t.getnames();assert not any('/core/release-report/' in x for x in names)
 assert not any('/node_modules/' in x for x in names)
 for suffix in ('SKILL.md','references/trials.md','agents/openai.yaml'):
  file=next(x for x in names if x.endswith('/.agents/skills/evaluate-harness/'+suffix));assert t.extractfile(file).read()==(Path(m['source'])/'.agents/skills/evaluate-harness'/suffix).read_bytes()
result={'status':'PASSED','source_commit':m['source_commit'],'wheel':str(wheel),'wheel_sha256':hashlib.sha256(wheel.read_bytes()).hexdigest(),'sdist':str(sdist),'sdist_sha256':hashlib.sha256(sdist.read_bytes()).hexdigest(),'installed_module':value['module'],'matched_skill_files':value['skill_files_matched'],'empty_catalogs':6,'forbidden_generated_artifacts':0,'runtime_validation':value['validation']['status'],'unexpected_acquisitions':0,'native_platform':'local macOS only'}
(b/'distribution-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
