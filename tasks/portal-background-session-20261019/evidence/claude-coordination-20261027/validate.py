"""Validate changed task documents and local links for this review stage."""
from pathlib import Path
import datetime,hashlib,json,re,subprocess,urllib.parse
root=Path.cwd();out=Path(__file__).parent
docs=['tasks/portal-background-session-20261019/10-delivery-confidence-20261026.md',
      'tasks/portal-background-session-20261019/11-behavior-traceability-20261027.md',
      'tasks/portal-background-session-20261019/evidence/index.md',
      'tasks/portal-background-session-20261019/evidence/claude-coordination-20261027/reconciliation/review.md']
lint=subprocess.run([str(root/'.venv/bin/ai-sdlc'),'lint',*docs[:2]],capture_output=True,text=True)
workspace=subprocess.run([str(root/'.venv/bin/ai-sdlc'),'--workspace',str(root),'validate'],capture_output=True,text=True)
whitespace=subprocess.run(['git','diff','HEAD','--check','--',*docs],capture_output=True,text=True)
errors=[];checked=0
for name in docs:
    path=root/name
    tracked=subprocess.run(['git','cat-file','-e','HEAD:'+name],capture_output=True).returncode==0
    if tracked:
        diff=subprocess.check_output(['git','diff','HEAD','--unified=0','--',name],text=True)
        lines=[s[1:] for s in diff.splitlines() if s.startswith('+') and not s.startswith('+++')]
    else: lines=path.read_text().splitlines()
    for number,line in enumerate(lines,1):
        if line.rstrip()!=line: errors.append({'document':name,'line':number,'reason':'trailing whitespace'})
        for target in re.findall(r'\]\(([^)]+)\)',line):
            if target.startswith(('http:','https:','mailto:')):continue
            raw,_,anchor=target.partition('#');file=(path.parent/urllib.parse.unquote(raw)) if raw else path;checked+=1
            if not file.exists():errors.append({'document':name,'target':target,'reason':'missing path'});continue
            if anchor and re.fullmatch(r'L\d+(?:-L\d+)?',anchor):
                if int(re.match(r'L(\d+)',anchor).group(1))>len(file.read_text(errors='replace').splitlines()):errors.append({'document':name,'target':target,'reason':'line beyond end'})
            elif anchor and file.suffix=='.md':
                txt=file.read_text(errors='replace');anchors=set(re.findall(r'<a\s+id=["\']([^"\']+)',txt))
                for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',txt,re.M):
                    heading=re.sub(r'<[^>]*>','',heading).lower();anchors.add(re.sub(r'[^\w\- ]','',heading).replace(' ','-'))
                if urllib.parse.unquote(anchor) not in anchors:errors.append({'document':name,'target':target,'reason':'anchor missing'})
failed=bool(lint.returncode or workspace.returncode or whitespace.returncode or errors)
result={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'documents':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in docs},
        'artifact_lint':json.loads(lint.stdout) if lint.stdout else {'error':lint.stderr},'artifact_lint_exit':lint.returncode,
        'workspace_validation':json.loads(workspace.stdout) if workspace.stdout else {'error':workspace.stderr},'workspace_validation_exit':workspace.returncode,
        'tracked_diff_check_exit':whitespace.returncode,'tracked_diff_check_output':whitespace.stdout+whitespace.stderr,
        'links_checked':checked,'link_errors':errors,'limits':['Tracked documents: new links only. New report: all links.', 'Automated checks do not check the complete ASD-STE100 dictionary or grammar rules.'],
        'writing_review':{'standard':'ASD-STE100','automated_check':'FAILED' if failed else 'PASSED','asd_review':'PENDING','reviewer':None,'reviewed_at':None}}
(out/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'lint':lint.returncode,'workspace':workspace.returncode,'whitespace':whitespace.returncode,'links':checked,'errors':errors}))
raise SystemExit(1 if failed else 0)
