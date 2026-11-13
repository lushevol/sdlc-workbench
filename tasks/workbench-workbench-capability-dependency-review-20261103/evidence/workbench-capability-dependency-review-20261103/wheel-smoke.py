import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys

base=Path('/private/tmp/workbench-capability-review-20261103')
sys.path.insert(0,str(base/'installed'))
import ai_sdlc_workbench
from ai_sdlc_workbench.cli import main
assert Path(ai_sdlc_workbench.__file__).is_relative_to(base/'installed')
workspace=base/'generated-workspace-verified'
results={'package_location':ai_sdlc_workbench.__file__,'dependency_source':'Prepared .venv site-packages; no dependency download or clean dependency resolution.'}
for name,args in [('init',['init',str(workspace),'--name','capability-review']),('validate',['--workspace',str(workspace),'validate']),('doctor',['--workspace',str(workspace),'doctor','--profile','core'])]:
 out=io.StringIO()
 with contextlib.redirect_stdout(out):
  code=main(args)
 results[name]={'exit_code':code,'output':json.loads(out.getvalue())}
 assert code==0,(name,out.getvalue())
assert not (workspace/'pyproject.toml').exists()
assert not (workspace/'core/cli.py').exists()
assert sorted(p.name for p in (workspace/'tasks').iterdir())==['README.md']
assert (workspace/'repos/README.md').is_file()
assert all((workspace/p).is_file() for p in ['AGENTS.md','PRINCIPLE.md','ARCHITECTURE.md','docs/WORKSPACE_DESIGN.md','core/knowledge/schemas/requirement.schema.json'])
assert results['validate']['output']['documents']==0
assert all(v==0 for v in results['validate']['output']['catalogs'].values())
wheel=next((base/'wheels').glob('*.whl'))
results['wheel']={'name':wheel.name,'sha256':hashlib.sha256(wheel.read_bytes()).hexdigest()}
results['scaffold_assertions']='PASS: guides, schema, empty catalogs, no runtime source, no business task contents.'
print(json.dumps(results,indent=2))
