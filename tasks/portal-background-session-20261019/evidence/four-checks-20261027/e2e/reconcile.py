from pathlib import Path
import json,hashlib,datetime,subprocess
root=Path.cwd();out=Path(__file__).resolve().parent;plan=json.loads((out/'plan.json').read_text());source_binding=json.loads((out/'source-binding.json').read_text());source=Path(source_binding['source']);records=[]
for planned in plan['cases']:
 matches=[]
 for p in out.glob('*/case-summary.json'):
  d=json.loads(p.read_text())
  if d['mode']==planned['mode']:
   matches.append((p,d))
 if not matches:records.append({'case_id':planned['id'],'mode':planned['mode'],'status':'NOT_RUN','canonical_definition':planned['canonical_definition']});continue
 p,d=sorted(matches,key=lambda item:item[1]['started_at'])[-1];run=json.loads((p.parent/'native/run.json').read_text()) if (p.parent/'native/run.json').exists() else {};actual=[]
 for q in (p.parent/'artifacts').glob('*/result.json'):
  a=json.loads(q.read_text())
  if a.get('caseId')=='session-setup':continue
  actual.append({'path':str(q.relative_to(out)),'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'case_id':a.get('caseId'),'status':a.get('status'),'error':a.get('error'),'freeze_observed':a.get('freezeObserved'),'original_frozen_tab_scenario':a.get('originalFrozenTabScenario'),'verification_level':a.get('verificationLevel'),'hidden_elapsed_ms':a.get('hiddenElapsedMs'),'observation_elapsed_ms':a.get('observation',{}).get('elapsedMs'),'assertions':a.get('assertions'),'screenshots':a.get('screenshots')})
 expected=d.get('artifacts',{});mismatches=[n for n,h in expected.items() if not (p.parent/n).is_file() or hashlib.sha256((p.parent/n).read_bytes()).hexdigest()!=h]
 records.append({'case_id':planned['id'],'mode':planned['mode'],'status':d['status'],'error':d.get('error'),'exit_code':d.get('exit_code'),'label':d['label'],'canonical_definition':planned['canonical_definition'],'summary':str(p.relative_to(out)),'summary_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'candidate_commit':d['candidate_commit'],'assertion_results':actual,'artifact_hash_mismatches':mismatches,'execution_scope':run.get('executionScope','NATIVE_BROWSER')})
source_mismatches=[p for p,h in source_binding['files'].items() if hashlib.sha256((source/p).read_bytes()).hexdigest()!=h]
app=root/'repos/ui/mfe-base';head=subprocess.check_output(['git','-C',str(app),'rev-parse','HEAD'],text=True).strip()
r={'reconciled_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_commit':source_binding['candidate_commit'],'application_current_head':head,'candidate_head_matches':head==source_binding['candidate_commit'],'final_release_binding':'final-release-binding.json','runtime_equivalence_status':json.loads((out/'final-release-binding.json').read_text())['runtime_equivalence_status'],'source_hash_mismatches':source_mismatches,'declared_cases':len(records),'executed_cases':sum(c['status'] not in ['NOT_RUN','RUNNING'] for c in records),'passed_cases':sum(c['status']=='PASSED' for c in records),'failed_cases':sum(c['status']=='FAILED' for c in records),'pending_cases':sum(c['status'] in ['NOT_RUN','RUNNING'] for c in records),'original_business_cases':{'declared':19,'passed':sum(c['status']=='PASSED' and c['case_id'].startswith('E2E-') and c['case_id'] not in ['E2E-12','E2E-21','E2E-22'] for c in records),'failed':sum(c['status']=='FAILED' and c['case_id'].startswith('E2E-') and c['case_id'] not in ['E2E-12','E2E-21','E2E-22'] for c in records)},'cases':records,'limits':['A failed assertion prevents later predicates in that case from running.','A diagnostic or observation pass does not establish business acceptance.','The local prepared BFF and toolkit substitute establish no production parity.','The exact controlled-clock four-hour AC-4 result is retained separately by the root agent.','Source and runner identity do not identify an immutable production artifact.']}
(out/'reconciliation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['declared_cases','executed_cases','passed_cases','failed_cases','pending_cases','source_hash_mismatches','original_business_cases']}))
