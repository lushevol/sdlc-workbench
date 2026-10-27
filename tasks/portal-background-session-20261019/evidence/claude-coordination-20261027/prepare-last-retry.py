"""Split the last failed diff segment into smaller authorized fragments."""
from pathlib import Path
import hashlib,json
out=Path(__file__).resolve().parent; manifest_path=out/'compact-manifest.json';m=json.loads(manifest_path.read_text())
previous=next(x for x in m['packets'] if x['name']=='retry-08-01');text=(out/'retry-08-01-prompt.txt').read_text()
segment=text.split('===== DIFF SEGMENT =====\n',1)[1].rsplit('\n===== END =====',1)[0]
chunks=[];current=[];size=0
for line in segment.splitlines(keepends=True):
    if current and size+len(line.encode())>2500:chunks.append(''.join(current));current=[];size=0
    current.append(line);size+=len(line.encode())
if current:chunks.append(''.join(current))
for i,chunk in enumerate(chunks,1):
    name=f'last-retry-{i:02d}'
    prompt=('Independently review only this partial diff for concrete introduced defects. '
            'No tools exist. Return at most one finding, 100 words maximum. '
            'State trigger, consequence, and uncertainty. Otherwise say NO CONFIRMED FINDING.\n'
            f"Candidate: {m['candidate']}\nPath: {previous['selected_paths'][0]}\nFragment {i} of {len(chunks)}\n"
            f'===== DIFF FRAGMENT =====\n{chunk}\n===== END =====\n')
    file=out/(name+'-prompt.txt');file.write_text(prompt)
    m['packets'].append({'name':name,'role':'independent','selected_paths':previous['selected_paths'],'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'context_sources':[],'fragment':i,'fragments':len(chunks)})
manifest_path.write_text(json.dumps(m,indent=2)+'\n');print(' '.join(f'last-retry-{i:02d}' for i in range(1,len(chunks)+1)))
