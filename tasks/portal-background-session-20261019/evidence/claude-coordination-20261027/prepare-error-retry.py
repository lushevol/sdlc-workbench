"""Retry a packet whose successful CLI result contained no review."""
from pathlib import Path
import hashlib,json,subprocess
out=Path(__file__).resolve().parent; manifest_path=out/'compact-manifest.json'
m=json.loads(manifest_path.read_text());repo=Path.cwd()/'repos/ui/mfe-base'
path='src/hooks/service/util/error.response.handler.ts';name='retry-error-handler'
diff=subprocess.check_output(['git','-C',str(repo),'diff',m['base'],m['candidate'],'--',path],text=True)
source=subprocess.check_output(['git','-C',str(repo),'show',m['candidate']+':'+path],text=True)
prompt=('Review this change independently using only the supplied diff and final source. '
        'No tools are available. Return at most two concrete findings, 150 words maximum. '
        'State trigger, consequence, and uncertainty. If none, state NO CONFIRMED FINDING.\n'
        f"Base: {m['base']}\nCandidate: {m['candidate']}\nPath: {path}\n"
        f'===== DIFF =====\n{diff}\n===== FINAL SOURCE =====\n{source}\n===== END =====\n')
f=out/(name+'-prompt.txt');f.write_text(prompt)
m['packets'].append({'name':name,'role':'independent','selected_paths':[path],'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'context_sources':[path]})
manifest_path.write_text(json.dumps(m,indent=2)+'\n');print(name,f.stat().st_size)
