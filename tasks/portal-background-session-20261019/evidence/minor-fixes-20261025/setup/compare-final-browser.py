#!/usr/bin/env python3
"""Reconcile original and new browser cases without mixing acceptance and observation counts."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import hashlib,json
root=Path.cwd();stage=root/'tasks/portal-background-session-20261019/evidence/minor-fixes-20261025';prior=root/'tasks/portal-background-session-20261019/evidence/active-cutoff-fix-20261024'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((prior/'case-inventory.json').read_text());inventory=json.loads((stage/'issue-2/browser-inventory.json').read_text());latest={}
for entry in inventory['cases']:latest[entry['mode']]=entry
integrity=stage/'setup/original-assertion-integrity.json';assert json.loads(integrity.read_text())['all_original_assertions_unchanged']

def current(entry,classification):
 summary_path=stage/entry['result'];s=json.loads(summary_path.read_text());paths=[stage/p for p in s['results']]
 if not paths:return {'status':'EXECUTION_ERROR','valid_setup':False,'summary':str(summary_path.relative_to(root)),'summary_sha256':sha(summary_path),'error':s.get('error')}
 path=paths[0];result=json.loads(path.read_text());status=result['status'];valid=entry.get('comparison_valid',True)
 if classification=='observation' and status=='PASSED':status='OBSERVATION_ONLY'
 if classification=='diagnostic':status='DIAGNOSTIC_PASSED' if status=='PASSED' else 'DIAGNOSTIC_FAILED'
 return {'status':status,'valid_setup':valid,'candidate_ref':s['candidate_ref'],'result':str(path.relative_to(root)),'result_sha256':sha(path),'summary':str(summary_path.relative_to(root)),'summary_sha256':sha(summary_path),'source_binding':s['source_binding'],'test_source_sha256':result['testSourceSha256'],'runner_sha256':s['runner_sha256'],'execution_scope':s.get('execution_scope','NATIVE_BROWSER'),'environment_limits':s.get('environment_limits',[]),'config_sha256':result['configSha256'],'error':result.get('error'),'assertions':result['assertions'],'limitations':result.get('limitations',[]),'hidden_elapsed_ms':result.get('hiddenElapsedMs'),'freeze_observed':result.get('freezeObserved'),'original_frozen_tab_scenario':result.get('originalFrozenTabScenario')}

blocked_modes={'cross','visibility','reload','late','natural','staleSuccess','staleError'}
blocker={'status':'BLOCKED_NATIVE','valid_setup':False,'reason':'The Mac locked. Native visibility setup cannot be verified until the actual unlock reply and fresh preflight.','evidence':'tasks/portal-background-session-20261019/evidence/minor-fixes-20261025/setup/cross-setup-console-check.json','owner':'user for unlock; Codex for preflight and reruns'}
rows=[]
for case in old['cases']:
 classification='diagnostic' if case['id']=='E2E-12' else 'observation' if case['id'] in ['E2E-21','E2E-22'] else 'business_acceptance';old_result=prior/case['candidate_result']['path'];assert sha(old_result)==case['candidate_result']['sha256']
 row={'id':case['id'],'mode':case['mode'],'classification':classification,'prior':{'candidate_ref':'ae8213f2963047e7c126d01f4003cee1236abc25','status':case['candidate_business_outcome'],'result':str(old_result.relative_to(root)),'result_sha256':sha(old_result),'source_commit_binding':str((prior/'commit-binding.json').relative_to(root))},'assertions_unchanged':True,'assertion_integrity':{'path':str(integrity.relative_to(root)),'sha256':sha(integrity)}}
 if case['mode']=='missing':row['current']={'status':'NOT_RERUN','valid_setup':None,'scope_record':str((stage/'issue-2/not-rerun.json').relative_to(root))};row['transition']='NOT_RERUN'
 elif case['mode'] in blocked_modes and (case['mode'] not in latest or latest[case['mode']].get('comparison_valid') is False):
  row['current']=dict(blocker)
  row['current']['retained_invalid_attempts']=[{'id':e['id'],'summary':e['result']} for e in inventory['cases'] if e['mode']==case['mode']]
  row['transition']='BLOCKED_NATIVE'
 elif case['mode'] in latest:
  row['current']=current(latest[case['mode']],classification);oldstatus=row['prior']['status'];newstatus=row['current']['status'];row['transition']='FAILED_TO_PASSED' if oldstatus=='FAILED' and newstatus=='PASSED' else 'UNCHANGED' if oldstatus==newstatus else oldstatus+'_TO_'+newstatus
 else:row['current']={'status':'NOT_RUN','valid_setup':None};row['transition']='NOT_RUN'
 rows.append(row)
new=[]
for mode,case_id,classification in [('delayed','FIX-DELAYED-BROWSER-SCHEDULED','additional_business_acceptance'),('staleSuccess','FIX-OWNERSHIP-BROWSER-SUCCESS','ownership_regression'),('staleError','FIX-OWNERSHIP-BROWSER-ERROR','ownership_regression')]:
 if mode in latest and latest[mode].get('comparison_valid',True):new.append({'id':case_id,'mode':mode,'classification':classification,'current':current(latest[mode],classification)})
 else:new.append({'id':case_id,'mode':mode,'classification':classification,'current':dict(blocker)})
missing=[r['id'] for r in rows if r['current']['status']=='NOT_RUN' or r['current'].get('valid_setup') is False];complete=not missing and len(new)==3 and all(r['current'].get('valid_setup') is True for r in new)
report={'recorded_at':datetime.now(timezone.utc).isoformat(),'status':'COMPLETED' if complete else 'PARTIAL','prior_ref':'ae8213f2963047e7c126d01f4003cee1236abc25','final_ref':'c42e7609c4e14eb53de32702e4bd3424a223988a','original_case_total':22,'original_cases':rows,'new_cases_not_counted_in_original_22':new,'original_business_counts':dict(Counter(r['current']['status'] for r in rows if r['classification']=='business_acceptance')),'original_diagnostic_counts':dict(Counter(r['current']['status'] for r in rows if r['classification']=='diagnostic')),'original_observation_counts':dict(Counter(r['current']['status'] for r in rows if r['classification']=='observation')),'original_failed_to_passed':[r['id'] for r in rows if r['transition']=='FAILED_TO_PASSED'],'not_rerun':[r['id'] for r in rows if r['current']['status']=='NOT_RERUN'],'incomplete':missing,'new_case_counts':dict(Counter(r['current']['status'] for r in new)),'limits':['Local portal/toolkit and BFF fixtures do not establish PROD configuration or deployment parity.','Held network delivery and controlled failure checks do not establish production frequency.','A passing hidden recovery without an observed freeze does not cover the original frozen-tab condition.']}
(stage/'issue-2/browser-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','original_business_counts','original_diagnostic_counts','original_observation_counts','original_failed_to_passed','new_case_counts','incomplete']}))
