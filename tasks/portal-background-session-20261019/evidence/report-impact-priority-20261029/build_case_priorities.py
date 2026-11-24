"""Apply recorded user-impact triage without modifying case execution outcomes."""
from pathlib import Path
from collections import Counter
import datetime
import hashlib
import json

HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
SOURCE=TASK/'evidence/report-clarity-20261029/execution-reason-audit.json'
REQUEST=TASK/'evidence/user-input-20261029-impact-priority-layout.txt'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    data=json.loads(SOURCE.read_text())
    output=[]
    for row in data['rows']:
        result_path=TASK/row['result']
        actual=json.loads(result_path.read_text())
        assert sha(result_path)==row['result_sha256'], row['id']
        status=row['status']; case=row['id']; group=row['group_id']
        priority='P3';blocking=False
        observed='No disruptive user effect was demonstrated by the completed checks.'
        reason='Required proof is missing. Missing proof alone does not establish a user failure or a release blocker.'
        action=row['next_action']
        if status=='BLOCKED':
            observed='No application failure was demonstrated. The required check could not complete.'
            reason='The missing environment or observation blocks this check. It does not independently block release under the user-impact rule.'
        if group=='partial-listener-baseline':
            observed='Listener counts differed across unmatched page states. No leak, forced logout, or unusable interface was proved.'
            reason='The resource comparison is inconclusive. The retained count failure does not prove disruptive user impact.'
        if group=='partial-four-hour':
            observed='Four simulated hours completed without a local sign-in prompt. Actual identity-provider continuity remains unverified.'
        if group=='failed-activity':
            priority='P4'
            observed='The specified activity interval produced zero renewals. Subsequent logout, session interruption, and lost work were not observed.'
            reason='The renewal target failed, but retained checks did not demonstrate a disrupted or unusable session.'
            action='Retain the activity backlog. Raise priority if a supported journey demonstrates session interruption or unusable recovery.'
        elif group=='failed-loading':
            priority='P4'
            observed='The loading indicator disappeared while another request remained pending. No blocked app, forced logout, or data loss was demonstrated.'
            reason='The observed effect is a minor visual indication. The app did not become unusable in the retained check.'
            action='Keep the visual defect in the backlog. Reassess if it causes blocked interaction or repeated committed business actions.'
        elif case=='RN-S023':
            observed='The mock servlet accepted the first duplicate refresh value and issued access for that identity.'
            reason='The rejection rule is proposed. No cross-account access or disruptive user effect was demonstrated.'
            action='Review duplicate-header policy and actual gateway normalization. Raise priority only for a demonstrated consequential path.'
        elif case=='RN-S035':
            observed='A portal access header appeared on an intercepted external request. No external server received credentials.'
            reason='The fixture proves header attachment. Supported external callers, transport delivery, and user compromise remain unverified.'
            action='Trace supported external-destination callers and effective transport controls before treating this as a release blocker.'
        elif case=='RN-S037':
            observed='A configured skip header invoked a synthetic handler without a JWT. No real protected business data was exposed.'
            reason='The filter path is demonstrated in a deliberate fixture. Actual gateway access and business impact remain unverified.'
            action='Verify public reachability and gateway stripping for a real protected route. Raise priority if unauthenticated access is confirmed.'
        elif case=='RN-S002':
            priority='P1';blocking=True
            observed='Expired-access logout reported success and stored zero revocations. Valid same-session refresh then issued new access.'
            reason='This proves a broken logout authentication boundary in the assessed controller. It is a genuine security blocker, despite no forced logout.'
            action='Correct the applicable revocation path or prove it absent from the release composition. Retain replay rejection and valid-access controls.'
        output.append({
            'id':case,'status':status,'group_id':group,'title':row['title'],
            'new_priority':priority,'release_blocking':blocking,
            'blocking_scope':'Assessed local controller composition. Production reachability remains unverified.' if blocking else None,
            'observed_user_impact':observed,'unverified_consequence':row['impact'],
            'reason':reason,'execution_reason':row['reason'],'missing_check':row['missing'],
            'next_action':action,'owner':row.get('owner','unknown'),
            'definition':row['definition'],'result':row['result'],'result_sha256':sha(result_path),
            'source_links':row.get('source_links',[]),'assertion_link':row.get('assertion_link'),
            'raw_failed_assertions_retained':row.get('raw_assertions_failed',0),
            'prior_severity':row.get('severity'),
            'evidence_limits':row.get('limits',[]),
        })
    assert len(output)==len({r['id'] for r in output})==285
    assert Counter(r['status'] for r in output)=={'FAILED':15,'PARTIALLY_EXECUTED':199,'BLOCKED':71}
    groups=[]
    for group in data['groups']:
        rows=[r for r in output if r['group_id']==group['id']]
        groups.append({'id':group['id'],'title':group['title'],'status':group['status'],'count':len(rows),
            'priorities':dict(Counter(r['new_priority'] for r in rows)),
            'release_blockers':[r['id'] for r in rows if r['release_blocking']],
            'triage_reason':rows[0]['reason'],'observed_user_impact':rows[0]['observed_user_impact'],
            'next_action':rows[0]['next_action'],'case_ids':[r['id'] for r in rows]})
    out={
        'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'Priority reassessment of all 285 failed or incomplete catalog cases. No new test execution or case-status change.',
        'request':'evidence/user-input-20261029-impact-priority-layout.txt','request_sha256':sha(REQUEST),
        'source_audit':'evidence/report-clarity-20261029/execution-reason-audit.json','source_audit_sha256':sha(SOURCE),
        'criteria':[
            'Use demonstrated user consequences to set priority. A failed or incomplete check alone does not justify a release hold.',
            'Minimal visual effects and activity gaps without demonstrated session interruption remain backlog work.',
            'Missing execution environments remain verification follow-up unless they prevent resolution of a named genuine blocker.',
            'A proven broken authentication boundary can remain a genuine security blocker. Keep deployment applicability separate.',
            'Priority does not rewrite execution results, observed evidence, severity, or human deployment authorization.',
        ],
        'summary':{'cases':len(output),'statuses':dict(Counter(r['status'] for r in output)),
            'priorities':dict(Counter(r['new_priority'] for r in output)),
            'release_blocking_cases':[r['id'] for r in output if r['release_blocking']],
            'nonblocking_cases':sum(not r['release_blocking'] for r in output),
            'status_changes':0,'new_case_executions':0,'result_hashes_verified':len(output)},
        'groups':groups,'rows':output,
        'limits':[
            'No production incident, credential theft, live account compromise, or deployment reachability is established.',
            'This catalog excludes historical review observations. Those are assessed separately in the issue-priority audit.',
            'Nonblocking means no independent release hold under this rule. It does not mean the check passed or behavior is safe.',
        ],
        'writing_review':{'standard':'ASD-STE100','automated_check':'PASSED','asd_review':'PENDING','reviewer':None,'reviewed_at':None,
            'limitations':['Automated checks do not check the complete approved dictionary or grammar rules.']},
    }
    (HERE/'case-priority-audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out['summary'],indent=2))

if __name__=='__main__':
    main()
