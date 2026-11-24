# Reuse retained execution identities and check current report references.
# This script does not execute business tests or alter runtime code.
from pathlib import Path
import json,re,hashlib,subprocess,urllib.parse
root=Path(__file__).resolve().parents[4];task=root/'tasks/portal-background-session-20261019';ev=task/'evidence/delivery-confidence-20261026';errors=[];links=0
files=[task/'09-delivery-coverage-20261026.md',task/'10-delivery-confidence-20261026.md',ev/'claude/claude-validation.md',ev/'user-input.md',ev/'go-live-blockers-user-input-20261027.md',ev/'user-view-network-user-input-20261027.md',ev/'step-by-step-user-input-20261027.md']
for p in files:
 for label,target in re.findall(r'(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)',p.read_text()):
  t=target.strip('<>')
  if urllib.parse.urlsplit(t).scheme:continue
  a,_,anchor=t.partition('#');q=(p.parent/urllib.parse.unquote(a)).resolve() if a else p;links+=1
  if not q.exists():errors.append({'path':str(p.relative_to(root)),'target':t,'kind':'missing_file'});continue
  if re.fullmatch(r'L\d+(?:-L\d+)?',anchor):
   n=len(q.read_text(errors='replace').splitlines())
   if any(int(i)>n or int(i)<1 for i in re.findall(r'\d+',anchor)):errors.append({'target':t,'kind':'line_bound'})
  elif anchor and q.suffix=='.md':
   content=q.read_text();slugs=[re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in re.findall(r'^#{1,6}\s+(.+)$',content,re.M)]+re.findall(r'id=[\"\']([^\"\']+)',content)
   if urllib.parse.unquote(anchor) not in slugs:errors.append({'target':t,'kind':'anchor'})
refs={'status':'PASSED' if not errors else 'FAILED','selected_documents':[str(p.relative_to(root)) for p in files],'checked_links':links,'findings':errors,'limitations':['Checks selected current report links, headings, and line bounds.','Historical catalog sections and raw external reviewer text are excluded.','Automated checks do not check the complete approved dictionary or grammar rules.']};(ev/'step-by-step-reference-checks-20261027.json').write_text(json.dumps(refs,indent=2)+'\n')
u=json.loads((ev/'unit/summary.json').read_text());runpath=root/u['current_full']['result'];r=json.loads(runpath.read_text());fail=[a['fullName'] for suite in r['testResults'] for a in suite['assertionResults'] if a['status']=='failed'];case_dir=runpath.parent/'cases';case_count=len(list(case_dir.glob('*.json')))
if (r['numTotalTests'],r['numPassedTests'],r['numFailedTests'],r['numPendingTests'])!=(457,455,2,0):errors.append({'kind':'unit_counts'})
if not(len(fail)==2 and any('[DEL-14]' in f for f in fail) and any('[DEL-20]' in f for f in fail)):errors.append({'kind':'failure_identity'})
if case_count!=457:errors.append({'kind':'checkpoint_count','actual':case_count})
binding=json.loads((ev/'unit/commit-binding.json').read_text())
if binding['unexpected_mismatches']:errors.append({'kind':'unexpected_source_mismatch'})
repo=root/'repos/ui/mfe-base';head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD']).decode().strip();expected='b8d4f1b837c6388452fbdc540f311257e805f932'
if head!=expected:errors.append({'kind':'head_changed','head':head})
changed=subprocess.check_output(['git','-C',str(repo),'diff','--name-only','f025513...c42e760','--','src']).decode().splitlines();runtime=[p for p in changed if '.test.' not in p];runtime_same=True
for p in runtime:
 if subprocess.check_output(['git','-C',str(repo),'show','c42e760:'+p])!=subprocess.check_output(['git','-C',str(repo),'show',head+':'+p]):runtime_same=False;errors.append({'kind':'runtime_changed','path':p})
b=json.loads((ev/'browser/comparison.json').read_text());bc=b['counts']
if (bc['current_original_completed'],bc['current_original_passed'],bc['current_original_failed'],bc['current_supplemental_completed'])!=(20,13,7,5):errors.append({'kind':'browser_counts'})
for p in ['independent-connected-response.json','adversarial-response.json','focused-challenge-response.json']:
 if json.loads((ev/'claude'/p).read_text()).get('is_error'):errors.append({'kind':'review_failed','file':p})
result={'status':'PASSED' if not errors else 'FAILED','unit_cases':case_count,'unit_total':457,'unit_passed':455,'unit_failed':2,'failed_tests':fail,'head':head,'runtime_paths':len(runtime),'runtime_bytes_match_reviewed_candidate':runtime_same,'matched_bound_files':binding['matched_bound_files'],'browser_counts':bc,'selected_report_links_checked':links,'errors':errors,'limits':['Validation proves retained identities and counts, not absence of undiscovered defects.','Business predicates retain their FAILED outcomes.','Full ASD writing review remains PENDING.']};(ev/'step-by-step-evidence-check-20261027.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'links':links,'cases':case_count,'runtime_paths':len(runtime),'errors':errors},indent=2))
raise SystemExit(bool(errors))
