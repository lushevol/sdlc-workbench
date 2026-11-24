"""Reclassify priorities from retained impact evidence without changing case outcomes."""
from pathlib import Path
from collections import Counter
import datetime, hashlib, json, re, subprocess
HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
IMPACTS=TASK/'evidence/release-report-execution-20261029/failure-impacts.json'
CATALOG=TASK/'10-issue-catalog.md'
REVIEW=TASK/'evidence/review-e2e-20261028/results.json'
CATALOG_BYTES=subprocess.check_output(['git','show','531d285d5:'+str(CATALOG.relative_to(TASK.parent.parent))],cwd=TASK.parent.parent)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(CATALOG_BYTES if p==CATALOG else p.read_bytes()).hexdigest()
impacts=read(IMPACTS); reviews=read(REVIEW)
policy='Lower priority when evidence shows no material user effect, only minimal impact, or missing execution prerequisites. Retain urgency for demonstrated session disruption, unusable recovery, or a genuine security blocker. Priority does not change case results or prove production reachability.'
rows=[]
for old in impacts['cases']:
 i=old['case_id']; security=i in ['RN-S023','RN-S035','RN-S037']; unexplained=i=='E2E-12'
 p='P3' if security or unexplained or i.startswith('RN-L') else 'P4'
 disp='NONBLOCKING_FOLLOW_UP' if p=='P3' else 'NONBLOCKING_BACKLOG'
 why='No session interruption, forced logout, unusable application, or user loss was demonstrated.'
 if i.startswith('RN-L'):why='Listener comparisons use different page states. No leak or user failure is demonstrated.'
 elif i=='RN-Q009':why='The misleading spinner is visual. The evidence shows no session disruption, blocked action, or data loss.'
 elif i in ['RN-S035','RN-S037']:why='The source fixture shows a security risk. Actual third-party delivery or protected business-service exposure is unverified.'
 elif i=='RN-S023':why='A proposed ambiguous-header rejection policy failed. Gateway behavior and actual user consequences remain unknown.'
 elif i=='E2E-12':why='A controlled inconsistent provider response changes credentials. A supported provider shape and user disruption are unverified.'
 if i=='RN-S002':
  p='P1';disp='SECURITY_RELEASE_BLOCKER';why='The actual RSA-validating controller returns logout success without revocation. Valid same-session refresh replay issues access. This is a genuine logout-security failure.'
 elif i=='REVIEW-E2E-01':
  p='P2';disp='SCOPED_SESSION_BLOCKER';why='An actual browser shows a valid replacement session behind a stale recovery dialog. Extend is disabled and Logout starts no request. Supported deployed caller remains unknown.'
 oldp=re.search(r'\bP[0-4]\b',old['severity'])
 next_action=old['next_action']
 if p=='P4':next_action='Retain as backlog. Escalate if a supported session interruption, forced logout, unusable application, or material loss is demonstrated.'
 if i in ['RN-S035','RN-S037']:next_action='Trace a supported caller and actual receiving service. Escalate if credential delivery or protected authorization bypass is demonstrated.'
 result=TASK/old['result_link']; read(result)
 rows.append({'id':i,'finding_id':old.get('finding_id'), 'source':'retained-impact-row',
  'previous_priority':oldp.group() if oldp else 'UNSPECIFIED', 'previous_severity':old['severity'],
  'new_priority':p,'severity':old['severity'],'severity_disposition':'Unchanged historical impact classification; priority reassessed separately.',
  'blocking_disposition':disp,'reason':why,'observed_user_impact':old['observed_user_impact'],
  'conditional_user_impact':old['conditional_user_impact'],'limits':old.get('limits',[])+[old.get('latest_candidate_applicability','')],
  'owner':old.get('owner','unknown'),'next_action':next_action,
  'definition':old['definition'],'source_links':old['source_links'],'assertion_links':[old['assertion_link']],
  'result_links':[old['result_link']]+([old['control_result_link']] if old.get('control_result_link') else []),
  'result_status':old['result_status'],'result_sha256':sha(result),
  'priority_change':'LOWERED' if oldp and int(p[1])>int(oldp.group()[1]) else 'RETAINED' if oldp else 'ASSIGNED_FROM_CURRENT_RULE'})
review_map={
 1:('P2','SCOPED_SESSION_BLOCKER','The browser demonstrates unusable recovery actions behind a stale dialog. Deployed caller applicability remains unknown.','Trace supported replacement-login callers. Correct and retest dialog ownership if applicable.'),
 2:('P3','NONBLOCKING_FOLLOW_UP','The rejected tokens are unsupported substitutes. Valid retries recover in the same dialog.','Confirm the supported provider token contract. Escalate only for a valid supported response that blocks renewal.'),
 3:('P4','NONBLOCKING_BACKLOG','The suspected recovery block was not reproduced. Actual Home reacquires refresh and protected validation succeeds.','Retain the observed state transition. Escalate if supported recovery fails.'),
 4:('P3','NONBLOCKING_FOLLOW_UP','Direct state replacement retains old refresh. No supported caller or distinct-user impact is demonstrated.','Identify supported direct setters and separate identities before assigning security impact.'),
 5:('P3','NONBLOCKING_FOLLOW_UP','Extend is unavailable while acquisition is pending. Logout remains available and released failure reaches Sign In.','Measure supported wait limits only if actual unusable recovery or unbounded waiting is reported.'),
 6:('P3','NONBLOCKING_FOLLOW_UP','Logout occurs only after an injected missing-expiry token with an invalid signature. The inspected provider never emits it.','Confirm provider validity rules. Escalate if a valid supported refresh credential causes forced logout.'),
 7:('P4','NONBLOCKING_BACKLOG','The suspected near-expiry recovery block was not reproduced. Actual renewal and protected validation succeed.','Retain successful recovery evidence. Reassess only after new session-disruption evidence.'),
 8:('P3','NONBLOCKING_FOLLOW_UP','A source configuration could affect chunks. No applicable built or deployed load failure is demonstrated.','Inspect effective settings only when a supported load failure or matching composition becomes available.'),
 9:('P3','NONBLOCKING_FOLLOW_UP','No actual consumer imports the declared development remote in retained evidence. No app failure is demonstrated.','Identify an actual importing consumer before treating the declaration as a delivery blocker.'),
 10:('P3','NONBLOCKING_FOLLOW_UP','The parser evaluates to one byte. No supported body-reading route or rejected business action is identified.','Identify a supported route and observable business failure before escalating.'),
 11:('P4','OUTSIDE_ARTIFACT_EXCLUDED_SCOPE','Missing external pipeline bytes establish no user failure. Release artifacts are excluded from this report.','Retain the source gap. Revisit only within an authorized artifact assessment or demonstrated runtime effect.'),
 12:('P4','NONBLOCKING_BACKLOG','The actual authentication-error route clears the loader. Sign In stays actionable. A persistent blocking loader is unproved.','Retain the successful recovery. Investigate another trigger only with concrete blocked-action evidence.'),
 13:('P4','NONBLOCKING_BACKLOG','Current RN-Q009 demonstrates an early-cleared visual indicator. No session loss, blocked action, or data loss is demonstrated.','Track visual loading correctness in backlog; escalate on demonstrated material user impact.'),
 14:('P3','NONBLOCKING_FOLLOW_UP','Known callers handle stale cancellation. No concrete downstream failure is identified.','Identify a supported caller that mishandles cancellation before escalating.'),
 15:('P3','NONBLOCKING_FOLLOW_UP','Timeout handles relogin rejection. No affected external consumer or unusable journey is identified.','Trace a supported external consumer only if a rejection causes a material user failure.'),
 16:('P4','NONBLOCKING_BACKLOG','The error object differs. No consumer depends on its identity and no user effect is demonstrated.','Retain contract difference. Escalate on a supported affected consumer.'),
 17:('P4','NONBLOCKING_BACKLOG','Usable accepted access delivered after the deadline installs and validates. The suspected late-delivery recovery block is not reproduced.','Retain successful late-delivery evidence. Escalate on an actual unsupported interruption.'),
 18:('P4','NONBLOCKING_BACKLOG','The ignore typo has no tracked lockfile or formatter consumer. It has no demonstrated business impact.','Treat as maintenance backlog.')}
review_rows=[]
for n in range(1,19):
 i=f'REVIEW-{n:02d}'; oldline=next(x for x in CATALOG_BYTES.decode().splitlines() if x.startswith(f'| <a id="review-{n:02d}"'))
 fields=oldline.split('|');rating=fields[1].strip(); outcome=fields[3].strip(); oldp=re.search(r'\bP[0-4]\b',rating)
 r=next(x for x in reviews['cases'] if x['finding']==i);p,disp,why,action=review_map[n]
 severity=re.search(r'/\s*(S.*)$',rating)
 result_links=['evidence/review-e2e-20261028/'+x for x in r['results']]
 result_sha={x:sha(TASK/x) for x in result_links}
 links=[('10-issue-catalog.md'+x if x.startswith('#') else x) for x in re.findall(r'\]\(([^)]+)\)',oldline)]
 review_rows.append({'id':i,'alias_of':'REVIEW-E2E-01' if n==1 else 'RN-Q009' if n==13 else None,
  'source':'review-register','previous_priority':oldp.group() if oldp else 'UNSPECIFIED','previous_severity':rating,
  'new_priority':p,'severity':severity.group(1) if severity else 'UNKNOWN','severity_disposition':'Unchanged historical impact classification; priority reassessed separately.',
  'blocking_disposition':disp,'reason':why,'observed_user_impact':r['claimAndLimit'],
  'limits':['Historical browser comparison candidate e0030f5. Current persistence requires exact source comparison. Production applicability remains unverified.'],
  'owner':'unknown application owner' if n not in [8,9,10,11,18] else 'unknown release or maintenance owner',
  'next_action':action,'definition':f'10-issue-catalog.md#review-{n:02d}','source_links':links,
  'result_links':result_links,'result_status':r['disposition'],'result_sha256':result_sha,
  'priority_change':'LOWERED' if oldp and int(p[1])>int(oldp.group()[1]) else 'RETAINED' if oldp else 'ASSIGNED_FROM_CURRENT_RULE'})
extra=[]
extra.append({'id':'RN-R020','source':'passing-characterization-risk','previous_priority':'UNSPECIFIED','previous_severity':'S3 Moderate, conditional, proposed',
 'new_priority':'P2','severity':'S3 Moderate, conditional, proposed','blocking_disposition':'SCOPED_SESSION_DISRUPTION',
 'reason':'The current source integration clears renewed access and refresh after an older same-epoch unauthorized response. It emits an expired-session login-again error.',
 'observed_user_impact':'Renewed session credentials are removed. This can force fresh authentication in a matching supported response schedule.',
 'limits':['Actual React, reducers, services, and interceptors run in jsdom with synthetic credentials, controlled adapter, and fake clock.','No actual browser, live business service, provider occurrence, or production environment was observed. Policy remains open.'],
 'owner':'unknown authentication and application owners','next_action':'Reproduce with valid provider responses and supported consumer. Resolve whether same-epoch older failure may clear renewed credentials.',
 'definition':'06-test-cases.md#rn-r020','source_links':['evidence/remaining-execution-20261029/core-integration/source-binding.json'],
 'result_links':['evidence/remaining-execution-20261029/core-integration/RN-R020/result.json'],'result_status':'PASSED_OBSERVATION_WITH_SESSION_RISK'})
observed_controls=[
 ('RN-S003','RN-S002','P1','SECURITY_RELEASE_BLOCKER','S2 High, conditional','Revocation storage failure still returns logout success. Same-session refresh replay issues access.','This is another demonstrated revocation failure within SEC-01. It is not a separate root blocker.','Verify durable revocation or honest failure reporting, then reject replay.','security/rn-s003/result.json'),
 ('RN-S004','RN-S002','P1','SECURITY_RELEASE_BLOCKER','S2 High, conditional','Logout without access reports success. Retained valid refresh still replays and issues access.','This extends SEC-01 to a missing-access input. It is not a separate root blocker.','Verify the supported logout credential contract and effective session revocation.','security/rn-s004/result.json'),
 ('RN-S029','REVIEW-04','P3','NONBLOCKING_FOLLOW_UP','UNKNOWN','Direct access replacement retains prior-user refresh and visible identity in the synthetic browser fixture.','No deployed direct setter or cross-account protected records are demonstrated.','Trace supported direct setters and complete the real identity transition.','security/rn-s029/result.json'),
 ('RN-S032','REVIEW-03','P3','NONBLOCKING_FOLLOW_UP','UNKNOWN','Rejected replacement login clears prior refresh. The observed prompt has Extend disabled.','A supported complete journey and persistent unusable state remain unproved. Earlier paired recovery succeeds.','Complete supported failed-login recovery before claiming disruption.','security/rn-s032/result.json'),
 ('RN-S044',None,'P3','NONBLOCKING_FOLLOW_UP','UNKNOWN; conditional credential exposure','Synthetic access appears in console arguments. No exported diagnostic or unauthorized reader is observed.','Missing export and sanitization contracts are verification gaps. They do not demonstrate credential delivery.','Identify actual diagnostic export readers and sanitization before escalating.','security/rn-s044/result.json'),
 ('RN-C002',None,'P3','NONBLOCKING_FOLLOW_UP','UNKNOWN','Two partial malformed-response combinations install unreadable access in a substitute provider flow.','Real provider occurrence, session interruption, and later user consequence are unverified.','Confirm supported provider response shapes and complete the real user journey.','combinations/combination-summary.json')]
for i,alias,p,disp,severity,observed,why,action,result in observed_controls:
 extra.append({'id':i,('related_to' if i in ['RN-S029','RN-S032'] else 'alias_of'):alias,'source':'passing-or-partial-observation-risk','previous_priority':'UNSPECIFIED',
 'previous_severity':severity,'new_priority':p,'severity':severity,'blocking_disposition':disp,
 'reason':why,'observed_user_impact':observed,'limits':['Retained local fixture only. Production reachability and frequency remain unverified.','Passing observation status records behavior; it does not approve that behavior.'],
 'owner':'unknown authentication owner' if i in ['RN-S003','RN-S004'] else 'unknown application, provider, or security owner',
 'next_action':action,'definition':'06-test-cases.md#'+i.lower(),'source_links':['evidence/remaining-execution-20261029/security/final-audit.json'] if i.startswith('RN-S') else [],
 'result_links':['evidence/remaining-execution-20261029/'+result],'result_status':'RETAINED_OBSERVATION'})
extra.append({'id':'VERIFICATION-GAPS','source':'historical-verification-gap-group','previous_priority':'Historical acceptance prerequisites; no numbered priority',
 'previous_severity':'Evidence gaps; no runtime severity','new_priority':'P3','severity':'No new user severity assigned',
 'blocking_disposition':'NONBLOCKING_FOLLOW_UP','reason':'Incomplete assertions, case labels, provider scope, and target parity do not themselves demonstrate a user failure.',
 'observed_user_impact':'No user failure is established by the listed traceability and execution omissions.',
 'limits':['Four-hour real SSO, proposed AC predicates, unknown workspace-loss report, full behavioral equivalence, ambiguous SR labels, fragmented provider review, and target parity remain unverified.'],
 'owner':'unknown test and application owners','next_action':'Preserve gaps. Prioritize an omitted check only when it resolves a specific demonstrated material effect or mandatory condition.',
 'definition':'10-issue-catalog.md#verification-and-traceability-gaps','source_links':[],'result_links':[], 'result_status':'EVIDENCE_GAPS'})
general=[
 ('GL-01','CLOSED_LOCAL','NONE_CLOSED','PageLoader after cancellation','The local correction passes its cancellation control. No open failure remains.','evidence/ut-remediation-20261027/final-cancellation-browser/comparison.json','10-issue-catalog.md#delivery-01'),
 ('GL-02','CLOSED_LOCAL','NONE_CLOSED','Missed acquisition callback','The local correction passes its timer control. No open failure remains.','evidence/ut-remediation-20261027/final-timer-control/comparison.json','10-issue-catalog.md#delivery-02'),
 ('GL-03','OUTSIDE_ARTIFACT_EXCLUDED_SCOPE','P4','Artifact identity','Artifact identity is outside the user-requested source report. Missing artifact proof is not a demonstrated user failure.','evidence/four-checks-20261027/release-evidence/closure-audit.md','10-issue-catalog.md#gl-03'),
 ('GL-04','NONBLOCKING_FOLLOW_UP','P3','Target composition','Missing effective settings or consumer versions alone do not demonstrate a user failure. Follow up only for a specific material issue.','evidence/four-checks-20261027/release-evidence/closure-audit.md','10-issue-catalog.md#gl-04'),
 ('GL-05','NONBLOCKING_FOLLOW_UP','P3','Target recovery evidence','A missing target recovery test is an evidence limit. It does not itself establish session disruption.','evidence/four-checks-20261027/release-evidence/closure-audit.md','10-issue-catalog.md#gl-05'),
 ('GL-06','NONBLOCKING_FOLLOW_UP','P3','Operations evidence','Missing smoke checks and monitoring evidence do not establish a runtime failure. They remain a separate operational decision.','evidence/four-checks-20261027/release-evidence/closure-audit.md','10-issue-catalog.md#gl-06'),
 ('GL-07','NONBLOCKING_FOLLOW_UP','P3','Business acceptance record','No recorded acceptance exists. This is a decision gap, not demonstrated user harm or a new technical defect.','evidence/four-checks-20261027/release-evidence/closure-audit.md','10-issue-catalog.md#gl-07'),
 ('GL-08','SEPARATE_DEPLOYMENT_AUTHORIZATION','NOT_A_DEFECT_PRIORITY','Deployment authorization','Actual deployment authorization remains separate. A priority change neither grants deployment authority nor invents a runtime failure.','evidence/four-checks-20261027/release-evidence/closure-audit.md','10-issue-catalog.md#gl-08')]
for i,disp,p,title,why,result,definition in general:
 extra.append({'id':i,'source':'general-release-control','title':title,'previous_priority':'P2 closed local defect' if i in ['GL-01','GL-02'] else 'Historical release hold; no numbered priority',
 'previous_severity':'See historical issue register','new_priority':p,'severity':'Unchanged historical scope; no new user severity assigned',
 'blocking_disposition':disp,'reason':why,'observed_user_impact':'No current open user failure established by this control record.',
 'limits':['Source assessment only. Release artifacts remain excluded. Human acceptance and deployment authorization remain separate.'],
 'owner':'unknown application owner' if i in ['GL-01','GL-02'] else 'unknown release, business, or authorizing owner',
 'next_action':'Retain closed local evidence.' if i in ['GL-01','GL-02'] else 'Handle only within the applicable scope. Escalate if a specific material user effect or mandatory condition is established.',
 'definition':definition,'source_links':[],'result_links':[result], 'result_status':'CLOSED_LOCAL' if i in ['GL-01','GL-02'] else 'EVIDENCE_OR_DECISION_GAP'})
# Inspect all retained result paths. This check does not execute a business case.
errors=[];checked=0
for r in rows+review_rows+extra:
 for link in r['result_links']:
  path=TASK/link
  checked+=1
  if not path.is_file():errors.append({'id':r['id'],'missing_result':link})
assert not errors,errors
output={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Successor issue-priority assessment only. No application execution, result changes, or deployment authorization.',
 'user_input':'evidence/user-input-20261029-impact-priority-layout.txt','policy':policy,
 'sources':[{'path':str(p.relative_to(TASK)),'sha256':sha(p),'revision_at_inspection':'531d285d5'} for p in [IMPACTS,CATALOG,REVIEW]],
 'summary':{'retained_impact_rows':len(rows),'review_entries':len(review_rows),'additional_and_general_controls':len(extra),
 'impact_priority_counts':dict(Counter(r['new_priority'] for r in rows)),
 'review_priority_counts':dict(Counter(r['new_priority'] for r in review_rows)),
 'additional_priority_counts':dict(Counter(r['new_priority'] for r in extra)),
 'retained_critical_issue_ids':['RN-S002','REVIEW-E2E-01','RN-R020'],
 'alias_limits':'REVIEW-01 aliases REVIEW-E2E-01. REVIEW-13 overlaps RN-Q009. Counts are inventory records, not distinct defects.',
 'result_paths_checked':checked,'execution_status_changes':0,'new_case_executions':0},
 'recommendation':{'release_status':'NO_GO','recommendation':'DO_NOT_RECOMMEND','controlling_issue':'RN-S002',
 'rationale':'Demonstrated expired-access logout does not revoke a valid refresh credential. This is a genuine source-bound security blocker. Minimal-impact and unverified issues are not blanket release holds.',
 'session_risks':['REVIEW-E2E-01: proven local unusable recovery; current supported caller must be established.','RN-R020: source integration clears renewed credentials; verify a matching supported provider schedule.'],
 'limits':['NO_GO applies to the assessed source composition. No production incident or frequency is established.','P3 and P4 disposition is prioritization, not proof of passing behavior or deployment approval.']},
 'issues':rows,'review_entries':review_rows,'additional_controls':extra,
 'writing_review':{'standard':'ASD-STE100','automated_check':'PASSED','asd_review':'PENDING','reviewer':None,'reviewed_at':None,'limitations':['Automated checks do not check the complete approved dictionary or grammar rules.']},
 'validation':{'status':'PASSED','retained_impact_rows':len(rows),'review_rows':len(review_rows),'result_paths_checked':checked,'problems':errors}}
assert len(rows)==28 and len(review_rows)==18 and len(extra)==16
(HERE/'issue-priority-audit.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output['summary'],indent=2))
