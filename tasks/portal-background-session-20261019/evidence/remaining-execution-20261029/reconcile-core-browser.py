from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
BASE=Path(__file__).resolve().parent
TASK=BASE.parent.parent
CATALOG=json.loads((BASE.parent/'comprehensive-renewal-20261028/core-cases.json').read_text())
INTEGRATION={f'RN-B{x:03d}' for x in range(1,10)}|{f'RN-P{x:03d}' for x in list(range(1,14))+[18]}|{f'RN-R{x:03d}' for x in range(9,15)}
DELEGATED={f'RN-R{x:03d}' for x in range(15,21)}|{'RN-M007','RN-M010'}
FOLDERS=['core-browser','core-browser-attempt2','core-browser-attempt3','core-browser-attempt4-smoke','core-browser-attempt5','core-browser-attempt5-stress','core-browser-attempt6-smoke','core-browser-attempt6-stress','core-browser-attempt7','core-browser-attempt8-final-baseline','core-browser-attempt9-validation']
SNAPSHOTS={'core-browser':'core-browser-attempt1.mjs','core-browser-attempt2':'core-browser-attempt2.mjs','core-browser-attempt3':'core-browser-attempt3.mjs'}
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
link=lambda f:str(f.relative_to(TASK))
all_attempts={}
for folder in FOLDERS:
 summary=json.loads((BASE/folder/'summary.json').read_text())
 runner=BASE/SNAPSHOTS[folder] if folder in SNAPSHOTS else BASE/folder/'runner.mjs'
 assert sha(runner)==summary['runner_sha256'],folder
 for f in (BASE/folder).glob('RN-*/result.json'):
  d=json.loads(f.read_text());cid=d['id'];assert d.get('source_revision')=='66c6411ade58e4d134e381c2baee8ad3f76a8dbf'
  all_attempts.setdefault(cid,[]).append((d,f,runner,summary))
rows=[];failures=[];limits=[]
for c in CATALOG:
 cid=c['id']
 if cid in INTEGRATION|DELEGATED:continue
 attempts=sorted(all_attempts.get(cid,[]),key=lambda x:x[0].get('completed_at',''))
 valid=[x for x in attempts if x[0].get('completed_at') and x[0]['status'] not in ['RUNNING','ERROR']]
 assert valid,cid
 d,f,runner,summary=valid[-1]
 raw=d['status'];status=raw
 unsupported_baseline=cid in ['RN-L004','RN-L005','RN-L006','RN-L010'] and raw=='FAILED' and d.get('error')=='mounted listener count returns to baseline'
 reason=None
 if unsupported_baseline:
  status='PARTIALLY_EXECUTED'
  reason='Recovery or switch cycles completed. Equivalent all-DOM listener baseline is unavailable because unrelated assets or UI states differ.'
  limits.append(cid+': '+reason)
 a=d.get('assertions',[])
 if raw=='PASSED':assert a and all(x['status']=='PASSED' for x in a),cid
 if raw=='FAILED':assert any(x['status']=='FAILED' for x in a),cid
 runner_lines=runner.read_text().splitlines()
 line=next((i for i,v in enumerate(runner_lines,1) if any(x['name'] in v for x in a if x['status']=='FAILED')),None)
 row={'id':cid,'case_id':cid,'title':c['title'],'status':status,'raw_status':raw,'assessment_reason':reason,'assertions':len(a),'failed_assertions':sum(x['status']=='FAILED' for x in a),'result':str(f.relative_to(BASE/'core-browser')) if f.is_relative_to(BASE/'core-browser') else str(Path('..')/f.relative_to(BASE)),'result_link':link(f),'result_sha256':sha(f),'runner':str(Path('..')/runner.relative_to(BASE)),'runner_link':link(runner),'runner_sha256':sha(runner),'assertion_link':link(runner)+(f'#L{line}' if line else ''),'definition':'06-test-cases.md#'+cid.lower(),'source_binding':'../execution-source-binding.json','completed_at':d['completed_at'],'blocked_predicates':d.get('blocked_predicates',[]),'error':d.get('error'),'attempts':[{'result_link':link(v[1]),'status':v[0]['status'],'sha256':sha(v[1]),'runner_link':link(v[2]),'runner_sha256':sha(v[2])} for v in attempts]}
 if cid.startswith('RN-A'):
  row['source_links']=['evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L79','evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L56']
 else:row['source_links']=[x['path']+'#L'+x['lines'].split('-')[0] for x in c.get('sources',[])]
 rows.append(row)
 if raw=='FAILED':
  if cid.startswith('RN-A'):
   kind='Continuous mouse input resets the five-second trailing debounce.' if cid=='RN-A001' else 'Continuous mixed input resets mouse debounce; keyboard and scroll have no independent renewal binding.' if cid=='RN-A004' else 'The shell has no renewal binding for this keyboard or scroll input.'
   item={'case_id':cid,'status':status,'classification':'APPLICATION_TARGET_FAILURE','failure_point':kind+' Zero successful renewals occurred during the15-second interval.','observed_user_impact':'The requested activity pattern did not renew the controlled session during15seconds.','conditional_user_impact':'Continued work can reach access expiry and require manual recovery. Logout and lost work were not observed.','severity':'S4 Minor / P4. Preserve the recorded user classification for the inherited activity gap.','acceptability':'Recorded activity backlog disposition remains. This run supplies no new acceptance or approval.','source_links':row['source_links'],'assertion_link':row['assertion_link'],'result_link':row['result_link'],'owner':'unknown portal application owner','next_action':'Implement the accepted activity rule when scheduled, then repeat the exact activity pattern and protected validation.','origin':'Inherited activity handling; this run does not establish a new release regression.','limits':['Current committed frontend executes with synthetic authentication responses and controlled browser time.','Keyboard and pointer use browser drivers. Scroll uses dispatched DOM events.','The case stops at failed renewal count. Later expiry, logout, and lost work are not asserted.']}
  else:
   o=d['observations'];
   if 'baseline_listeners' not in o: raise RuntimeError((cid,str(f),d.get('error')))
   before=o['baseline_listeners'];after=o['final_listeners']
   item={'case_id':cid,'status':status,'raw_status':raw,'classification':'VERIFICATION_BASELINE_UNRESOLVED','failure_point':f"All-DOM mounted listener equality differs: {before['count']} before; {after['count']} after.",'observed_user_impact':'No user failure was demonstrated. Required recovery or switch cycles completed.','conditional_user_impact':'Listener leakage is unverified. Count differences alone cannot establish repeated handlers, memory growth, or user interruption.','severity':'UNRATED evidence gap. No application defect severity is assigned.','acceptability':'Keep resource-baseline verification open. Preserve this failed assertion and its measurement limits.','source_links':['evidence/remaining-execution-20261029/execution-source-binding.json'],'assertion_link':row['assertion_link'],'result_link':row['result_link'],'owner':'unknown portal verification owner','next_action':'Repeat equivalent mounted UI states after assets settle and notifications close; compare the same owned listeners and timers.','origin':'The measured shell states differ. It is not a confirmed release regression.','limits':['The original raw assertion remains FAILED. The canonical case remains partially verified.','L004 completed1000 recovery cycles with2000 passing per-cycle assertions.','Error/load asset listeners disappeared for L004. L005/L006 retain a rejection notification. L010 removes popover listeners.','A later image-completion attempt blocked before cycles because shell image requests remained incomplete.']}
  failures.append(item)
counts={}
rawcounts={}
for r in rows:counts[r['status']]=counts.get(r['status'],0)+1;rawcounts[r['raw_status']]=rawcounts.get(r['raw_status'],0)+1
out={'recorded_at':datetime.now(timezone.utc).isoformat(),'scope':'Canonical current core browser cases. Delegated component cases are excluded to prevent duplicate counts.','revision':'66c6411ade58e4d134e381c2baee8ad3f76a8dbf','planned_browser_ids':88,'selected':len(rows),'delegated_case_ids':sorted(DELEGATED),'counts':counts,'raw_status_counts':rawcounts,'results':rows,'selection_rule':'Use latest completed non-ERROR result. Preserve setup failures and superseded assertions in attempts.','assessment_limits':limits,'source_binding':'../execution-source-binding.json','status':'RECONCILED_WITH_FAILURES_AND_LIMITS','writing_review':{'standard':'ASD-STE100','automated_check':'PASSED','asd_review':'PENDING','reviewer':None,'reviewed_at':None,'limitations':['Automated checks do not check the complete approved dictionary or grammar rules.']}}
assert len(rows)==80
for r in rows:
 assert (TASK/r['result_link']).exists() and (TASK/r['runner_link']).exists()
(BASE/'core-browser/reconciled-summary.json').write_text(json.dumps(out,indent=2)+'\n')
(BASE/'core-browser/failure-impacts.json').write_text(json.dumps({'recorded_at':out['recorded_at'],'source_summary':'reconciled-summary.json','failures':failures,'application_failure_count':sum(x['classification']=='APPLICATION_TARGET_FAILURE' for x in failures),'unresolved_failed_verification_checks':sum(x['classification']=='VERIFICATION_BASELINE_UNRESOLVED' for x in failures),'writing_review':out['writing_review']},indent=2)+'\n')
print(json.dumps({'selected':len(rows),'counts':counts,'raw_status_counts':rawcounts,'failure_impacts':len(failures)}))
