"""Check authored artifacts, local references, finite designs, and retained hashes."""
import hashlib
import itertools
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

D=Path(__file__).resolve().parent
T=D.parent.parent
R=T.parent.parent
docs=[T/x for x in ['03-use-cases-renewal.md','05-test-strategy-renewal.md','06-test-cases.md','07-security-review-renewal.md','08-test-execution-renewal.md','09-renewal-coverage.md']]
errors=[]
checks={}
def anchor_set(p):
    s=p.read_text()
    headings=[re.sub(r'[^\w\- ]','',x.strip().lower()).replace(' ','-') for x in re.findall(r'^#{1,6} (.*)$',s,re.M)]
    return set(headings+re.findall(r'<a id=[\"\']([^\"\']+)',s))
references=0
for p in docs:
    content=p.read_text()
    if p.name=='06-test-cases.md':content=content.split('## Comprehensive renewal expansion',1)[1]
    content=re.sub(r'```.*?```','',content,flags=re.S)
    for target in re.findall(r'\]\(([^)]+)\)',content):
        if re.match(r'^[a-z]+://',target):continue
        target=unquote(target.strip('<>'))
        dest,_,fragment=target.partition('#')
        q=(p.parent/dest).resolve() if dest else p
        references+=1
        if not q.exists():errors.append(f'{p.name}: missing {target}');continue
        if not fragment:continue
        line=re.fullmatch(r'L(\d+)(?:-L?(\d+))?',fragment)
        if line:
            count=len(q.read_text().splitlines())
            lo=int(line[1]);hi=int(line[2] or line[1])
            if not 1<=lo<=hi<=count:errors.append(f'{p.name}: invalid line locator {target}')
        elif q.suffix=='.md' and fragment not in anchor_set(q):
            errors.append(f'{p.name}: missing anchor {target}')
checks['local_references']=references
design=json.loads((D/'design-manifest.json').read_text())
assert hashlib.sha256((T/'06-test-cases.md').read_bytes()).hexdigest()==design['sha256']
assert len(design['cases'])==271
assert Counter(c['execution_status'] for c in design['cases'])=={'NOT_RUN':255,'PASSED':15,'FAILED':1}
checks['individual_definitions']=271
checks['execution_states']=dict(Counter(c['execution_status'] for c in design['cases']))
comb=json.loads((D/'combinations.json').read_text())
keys=list(comb['factors'])
expected={(a,x,b,y) for a,b in itertools.combinations(keys,2) for x in comb['factors'][a] for y in comb['factors'][b]}
actual={(a,row[a],b,row[b]) for row in comb['pairwise_rows'] for a,b in itertools.combinations(keys,2)}
assert expected==actual
assert len(comb['risk_rows'])==144 and len({tuple(r[k] for k in ['trigger','access_ms','response','ownership']) for r in comb['risk_rows']})==144
assert len(comb['order_rows'])==15
checks['pair_coverage']={'covered':len(actual),'required':len(expected)}
checked=set()
for filename in ['source-manifest.json','coverage-source-manifest.json']:
    for item in json.loads((D/filename).read_text())['sources']:
        snapshot=R/item['snapshot']
        assert hashlib.sha256(snapshot.read_bytes()).hexdigest()==item['sha256']
        checked.add(item['snapshot'])
checks['retained_source_hashes']=len(checked)
lint=subprocess.run([str(R/'.venv/bin/ai-sdlc'),'lint',*[str(p) for p in docs]],capture_output=True,text=True,cwd=R)
(D/'artifact-lint.json').write_text(lint.stdout)
ld=json.loads(lint.stdout)
checks['artifact_lint']={'status':ld['status'],'errors':sum(x['severity']=='error' for x in ld['findings']),'warnings':sum(x['severity']=='warning' for x in ld['findings'])}
if lint.returncode:errors.append('Artifact lint failed')
result={'status':'FAILED' if errors else 'PASSED','checks':checks,'errors':errors,
 'limits':['Local references, retained hashes, artifact structure, and finite design coverage only.',
 'No complete ASD-STE100 dictionary or grammar review. No passing business or security result inferred.']}
(D/'design-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(bool(errors))
