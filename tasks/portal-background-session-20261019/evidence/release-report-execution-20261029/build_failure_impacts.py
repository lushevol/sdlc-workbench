"""Combine retained historical impacts and newly demonstrated case failures."""
from pathlib import Path
import copy
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
TASK = HERE.parent.parent
RUN = TASK / 'evidence/remaining-execution-20261029'
OLD = TASK / 'evidence/release-report-20261029'


def read(path):
    return json.loads(path.read_text())


def task_link(value, base):
    path, mark, fragment = value.partition('#')
    return str((base / path).resolve().relative_to(TASK)) + (mark + fragment if mark else '')


def main():
    prior = read(OLD / 'failure-impact-audit.json')
    cases = copy.deepcopy(prior['cases'])
    for row in cases:
        row['evidence_period'] = 'prior-retained'
    security = read(RUN / 'security/new-failure-impacts.json')
    for identifier, f in security['findings'].items():
        cases.append({'case_id': identifier, 'definition':'06-test-cases.md#'+identifier.lower(),
            'failure_point':f['failure'], 'observed_user_impact':f['impact'],
            'conditional_user_impact':'Production reachability and business consequences remain unverified.',
            'severity':f['severity'], 'acceptability':
                'Resolve applicable exposure before security acceptance.' if identifier in ['RN-S035','RN-S037']
                else 'Acceptance is unknown until policy and gateway behavior are reviewed.',
            'source_links':[task_link(f['source'], RUN / 'security')],
            'assertion_link':'evidence/remaining-execution-20261029/security/' +
                {'RN-S023':'RemainingSecurityProbe.java#L148','RN-S037':'RemainingSecurityProbe.java#L153',
                 'RN-S035':'browser-security.mjs#L82-L85'}[identifier],
            'result_link':task_link(f['result'], RUN / 'security'),
            'owner':f['owner'],'next_action':f['action'],'origin':f['origin'],
            'evidence_period':'current', 'result_status':'FAILED',
            'limits':['Actual source under isolated controls; gateway and production reachability remain unknown.']})
    workspace=read(RUN/'workspace-transport/findings.json')
    for f in workspace['open_failures']:
        for i, identifier in enumerate(f['cases']):
            result=f.get('result') or f['results'][i]
            cases.append({'case_id':identifier,'definition':'06-test-cases.md#'+identifier.lower(),
                'failure_point':f['failure'], 'observed_user_impact':f['observed_impact'],
                'conditional_user_impact':
                    'Later expiry can interrupt work; actual logout and lost work remain unobserved.'
                    if identifier.startswith('RN-W') else
                    'A misleading readiness indication is observed. Repeat business submission remains unproved.',
                'severity':f['severity'], 'acceptability':
                    'Existing recorded activity backlog remains deferred within its stated scope.'
                    if identifier.startswith('RN-W') else
                    'Observed minor defect; human acceptance remains unrecorded.',
                'source_links':[task_link(v, RUN/'workspace-transport') for v in f['sources']],
                'assertion_link':task_link(f['assertions'],RUN/'workspace-transport')+
                    ('#L137' if identifier.startswith('RN-W') else '#L149'),
                'result_link':task_link(result,RUN/'workspace-transport'),
                'owner':f['owner'],'next_action':f['next_action'],'origin':f['origin'],
                'evidence_period':'current','result_status':'FAILED',
                'limits':[f.get('reachability_limit','Synthetic workspace and controlled browser time; no production-frequency claim.')]})
    core_path=RUN/'core-browser/failure-impacts.json'
    if core_path.exists():
        core=read(core_path)
        for f in core.get('cases', core.get('failures', core.get('findings', []))) if isinstance(core,dict) else core:
            for field in ['failure_point','observed_user_impact','conditional_user_impact']:
                f[field]=re.sub(r'\b(the|during|completed|with)(\d+)',r'\1 \2',f[field])
                f[field]=re.sub(r'(\d+)(seconds|cycles|passing)\b',r'\1 \2',f[field])
            f.setdefault('definition','06-test-cases.md#'+f['case_id'].lower())
            f.setdefault('evidence_period','current')
            f.setdefault('result_status',f.get('status','FAILED'))
            cases.append(f)
    inventory=read(RUN/'aggregate/final-inventory.json')
    failed={r['id'] for r in inventory['rows'] if r['status']=='FAILED'}
    covered={r['case_id'] for r in cases}
    missing=sorted(failed-covered)
    if missing:
        raise ValueError('Failure impacts are missing for '+', '.join(missing))
    assert len(covered)==len(cases),'Duplicate impact IDs'
    data={'recorded_date':'2026-10-29 Asia/Singapore','scope':'All current failed cases and ten retained historical failure or impact rows.',
          'severity_definitions':prior['severity_definitions'], 'current_failed_cases':len(failed),
          'prior_retained_rows':10,'unresolved_verification_rows':sum(f.get('classification')=='VERIFICATION_BASELINE_UNRESOLVED' for f in cases),
          'total_rows':len(cases),'cases':cases,
          'current_failure_ids':sorted(failed),'missing_current_failures':missing,
          'prior_audit_sha256':hashlib.sha256((OLD/'failure-impact-audit.json').read_bytes()).hexdigest()}
    (HERE/'failure-impacts.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'rows':len(cases),'current_failed':len(failed),'missing':missing}))


if __name__=='__main__':
    main()
