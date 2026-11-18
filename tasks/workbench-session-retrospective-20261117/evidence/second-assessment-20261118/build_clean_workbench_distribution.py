from pathlib import Path
import json,subprocess,tempfile
root=Path('/Users/lushevol/code/github/ratan-release-impact/workbench')
where=Path(tempfile.mkdtemp(prefix='wb-distribution-'))
source=where/'source';source.mkdir()
archive=subprocess.Popen(['git','archive','HEAD'],cwd=root,stdout=subprocess.PIPE)
subprocess.run(['tar','-x','-C',str(source)],stdin=archive.stdout,check=True)
archive.stdout.close();assert archive.wait()==0
manifest={'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'root':str(where),'source':str(source),'output':str(where/'dist'),'python':str(root/'.venv/bin/python'),'install':str(where/'installed'),'workspace':str(where/'workspace')}
(where/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(where)
with (where/'wheel.log').open('w') as log:
 result=subprocess.run([manifest['python'],'-m','pip','wheel','.', '--no-deps','--no-build-isolation','--no-index','--wheel-dir',manifest['output']],cwd=source,stdout=log,stderr=subprocess.STDOUT)
 if result.returncode:print(log.name);raise SystemExit(result.returncode)
with (where/'sdist.log').open('w') as log:
 result=subprocess.run([manifest['python'],'setup.py','sdist','--dist-dir',manifest['output']],cwd=source,stdout=log,stderr=subprocess.STDOUT)
 if result.returncode:print(log.name);raise SystemExit(result.returncode)
print('wheel and source archive build: PASSED')
