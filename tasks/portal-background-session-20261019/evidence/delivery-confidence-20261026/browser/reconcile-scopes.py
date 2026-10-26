from pathlib import Path
import json,hashlib,datetime
root=Path.cwd();base=root/'tasks/portal-background-session-20261019/evidence/delivery-confidence-20261026/browser';rows=[]
for p in base.glob('*/*/artifacts/*/result.json'):
 d=json.loads(p.read_text())
 if d.get('caseId')=='session-setup':continue
 directory=p.parents[2];native=directory/'native/run.json';run=json.loads(native.read_text()) if native.exists() else {};ua=d.get('userAgent','');headless='HeadlessChrome/' in ua
 row={'case_id':d.get('caseId'),'result':str(p.relative_to(base)),'result_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'user_agent':ua,'browser_version':d.get('browserVersion'),'execution_scope':'DOM_SERVICE_HEADLESS' if headless else 'HEADED_EDGE_DOM_SERVICE','headless_user_agent':headless,'runner_args_include_headless':any('headless' in x for x in run.get('args',[])),'native_window_transitions_recorded':bool(run.get('nativeWindowTransitions')),'freeze_observed':bool(d.get('freezeObserved')),'physical_human_input_verified':False,'limits':['Trusted browser input and DOM screenshots do not establish physical human input.','A headed process does not establish natural suspension or observed freeze.']}
 if d.get('caseId')=='quick-visibility-refresh' and d.get('status')=='PASSED':row['asserted_visibility_transition']='PASSED: case source waits for actual document hidden and visible states. Final lifecycle array follows validation reload.'
 if headless:row['limits'].append('Headless execution does not establish native window visibility or lifecycle behavior.')
 rows.append(row)
report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'counts':{'headed':sum(x['execution_scope']=='HEADED_EDGE_DOM_SERVICE' for x in rows),'headless':sum(x['execution_scope']=='DOM_SERVICE_HEADLESS' for x in rows)},'writing_review':{'standard':'ASD-STE100','automated_check':'PASSED','asd_review':'PENDING','reviewer':None,'reviewed_at':None,'limitations':['Automated checks do not check the complete approved dictionary or grammar rules.']}}
(base/'scope-reconciliation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['counts']))
