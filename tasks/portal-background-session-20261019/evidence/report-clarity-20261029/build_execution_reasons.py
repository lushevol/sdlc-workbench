"""Explain each nonpassing catalog disposition without changing execution evidence."""
from pathlib import Path
from collections import Counter
import datetime
import hashlib
import json

HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
RUN=TASK/'evidence/remaining-execution-20261029'


def read(path):
    return json.loads(path.read_text())


def main():
    inventory=read(RUN/'aggregate/final-inventory.json')
    rows_by_id={r['id']:r for r in inventory['rows']}
    groups=[]
    def group(identifier,status,title,ids,what_ran,reason,missing,impact,next_action,owner):
        groups.append({'id':identifier,'status':status,'title':title,'count':len(ids),'case_ids':ids,
            'what_ran':what_ran,'reason':reason,'missing':missing,'impact':impact,
            'next_action':next_action,'owner':owner})
    activity=['RN-A001','RN-A002','RN-A003','RN-A004','RN-A005','RN-A006','RN-A013','RN-W029','RN-W030','RN-W031']
    group('failed-activity','FAILED','Activity did not trigger renewal',activity,
        'Browser input ran for 15 seconds. Each case expected at least one renewal.',
        'Continuous mouse movement resets the five-second waiting period. Keyboard and scroll have no renewal event binding.',
        'A passing renewal during the specified input interval.',
        'Activity alone can leave the session unchanged until expiry. Later logout and lost work were not observed.',
        'Retain the recorded activity backlog. Implement and repeat the accepted input rule when scheduled.',
        'unknown application owner')
    group('failed-logout','FAILED','Logout did not prevent refresh replay',['RN-S002'],
        'The current controller processed expired-access logout, then replayed the same valid refresh credential.',
        'Logout returned success but stored zero revocations. Refresh replay returned 200 and issued access; expected status was 401.',
        'Verified same-session refresh rejection after logout.',
        'A holder of copied valid refresh credentials could regain authentication after apparent logout. Target exposure remains unknown.',
        'Correct or disprove applicable revocation failure. Retain valid and forged-credential controls.',
        'unknown authentication and security owners')
    group('failed-loading','FAILED','Loading indicator cleared too early',['RN-Q009'],
        'Request A failed during response parsing while request B remained pending.',
        'The shared error handler received no request configuration and cleared all tracked loading requests.',
        'The loading indicator must remain active for request B.',
        'Users can see a ready screen while work is still pending. Duplicate submissions and data loss were not demonstrated.',
        'Decide the minor visual-gap disposition. Preserve request ownership when correcting the error path.',
        'unknown application owner')
    group('failed-ambiguous-header','FAILED','Conflicting refresh headers were accepted',['RN-S023'],
        'The current controller received two refresh headers, identifying A and B.',
        'The controller selected the first header and issued access for A. The proposed case expected no access.',
        'Reviewed duplicate-header policy and actual gateway/header normalization behavior.',
        'Ambiguous input is accepted in the mock servlet. Cross-account takeover and deployed reachability were not demonstrated.',
        'Review the input policy and repeat the case through the actual HTTP and gateway path.',
        'unknown authentication and security owners')
    group('failed-external-header','FAILED','Access header attached to an external request',['RN-S035'],
        'The shared HTTP client created a request to an external HTTPS fixture.',
        'The interceptor attached the portal access credential. The case expected no portal credential.',
        'A verified supported-destination policy and credential containment.',
        'A reachable caller could send credentials toward an external destination. Interception prevented external delivery in this test.',
        'Trace supported callers and verify that untrusted destinations receive no portal credentials.',
        'unknown shared-client and security owners')
    group('failed-skip-header','FAILED','Configured skip header bypassed JWT validation',['RN-S037'],
        'The current SDK filter received a configured skip header without a JWT.',
        'The filter invoked the synthetic protected handler once. The case expected zero invocations.',
        'Verified trusted-header stripping and route isolation in the real composed service.',
        'An untrusted caller reaching such a route could bypass JWT validation. Actual business data exposure remains unverified.',
        'Test forged public skip headers through the actual gateway and business service.',
        'unknown SDK, gateway, and security owners')

    combination=[r['id'] for r in inventory['rows'] if r['status']=='PARTIALLY_EXECUTED' and r['group']=='combinations']
    group('partial-business-combinations','PARTIALLY_EXECUTED','Business-write checks are missing from combination tests',combination,
        '181 combinations ran bounded checks against actual React, session-state, and HTTP-client code.',
        'The local fixture has no real protected business-write service or authoritative transaction records.',
        'Proof of zero unauthorized writes. The 37 pairwise rows also need operation IDs, commit counts, and selected real transport schedules.',
        'Client-state checks cannot establish safe business authorization or prevent duplicate committed writes.',
        'Bind a named business operation, authorization service, and durable commit audit. Run each required transport schedule.',
        'unknown business-service and test owners')
    group('partial-listener-baseline','PARTIALLY_EXECUTED','Listener cleanup comparison is inconclusive',
        ['RN-L004','RN-L005','RN-L006','RN-L010'],
        'The required recovery or workspace-switch cycles completed. The longest run completed 1,000 successful recoveries.',
        'Before/after pages differed because assets, notifications, or popovers changed. Listener counts were not comparable.',
        'Equivalent page states and a comparison of the same owned listeners and timers.',
        'No leak or user failure was proved. Cleanup remains unverified; raw count assertions remain failed.',
        'Repeat the same visible state after assets and notifications settle. Compare matching listener ownership.',
        'unknown test owner')
    group('partial-signed-service','PARTIALLY_EXECUTED','Client renewal passed; actual service acceptance is missing',
        ['RN-P014','RN-P015','RN-P016','RN-P017'],
        'The browser installed the synthetic renewal credential. A controlled peer accepted the exact credential bytes.',
        'The peer does not validate the real token signature or protected-service principal.',
        'Current real BFF/SDK acceptance of each specified credential shape and identity.',
        'Client success cannot establish that the user can access a real protected service after renewal.',
        'Bind valid signed credentials and the current service for each case. A separate P018 pass does not cover these shapes.',
        'unknown authentication and test owners')
    group('partial-native-equivalence','PARTIALLY_EXECUTED','Controlled browser checks omit the real lifecycle',
        ['RN-B013','RN-H011'],
        'B013 observed timeout after controlled resume. H011 checked storage separation between isolated browser contexts.',
        'The runner did not perform actual suspension or complete renewal in normal and private windows.',
        'The exact native suspension or normal/private-window session sequence.',
        'The retained checks cannot establish the requested native-browser behavior.',
        'Repeat in the named browser lifecycle with actual session and protected-service observations.',
        'unknown browser test owner')
    group('partial-transport','PARTIALLY_EXECUTED','Transport observations omit the actual connected application',
        ['RN-A009','RN-W032','RN-S045'],
        'The runner observed no-input expiry, synthetic notification callbacks, or local renewal URLs.',
        'No actual heartbeat peer, passive-update consumer, or authenticated reconnect/referrer receiver was bound.',
        'The named real transport and consumer, with delivery, renewal, credential, and URL observations.',
        'The tests cannot establish activity policy or credential containment during real passive updates and reconnects.',
        'Load the actual consumer and isolated server. Observe the complete connection and delivery sequence.',
        'unknown transport and test owners')
    group('partial-server-state','PARTIALLY_EXECUTED','Client observations omit authoritative application or server state',
        ['RN-W016','RN-Q019','RN-D009'],
        'The runner retained unsaved synthetic form state, counted one client submission, or observed the closed renewal tab.',
        'The fixture lacks a real record version, durable financial commit audit, or source-bound server completion audit.',
        'Authoritative application/server state for the exact form, write, or closed-tab request.',
        'Client observations cannot establish saved-record integrity, one committed write, or server completion after tab close.',
        'Bind the real application and authoritative server records, then complete the missing state assertions.',
        'unknown application, service, and test owners')
    group('partial-diagnostics','PARTIALLY_EXECUTED','Diagnostic sanitization contract is unavailable',['RN-S044'],
        'An acquisition-failure console call was observed. Its arguments included a synthetic access credential.',
        'No application diagnostic exporter or sanitization contract was supplied.',
        'Actual exported diagnostics, their readers, and the required sanitization rule.',
        'Conditional credential exposure remains unresolved. A console observation does not establish export safety or unauthorized access.',
        'Identify the exporter and readers. Verify credential removal against the supported contract.',
        'unknown diagnostics and security owners')
    group('partial-four-hour','PARTIALLY_EXECUTED','Four-hour browser run used a substitute authentication peer',['RN-L011'],
        'Four controlled hours elapsed. No local login prompt appeared, and the controlled protected peer accepted installed access.',
        'The run did not use a real SSO-prompt observer or current cryptographic protected endpoint.',
        'Actual provider continuation and protected-service identity acceptance across the initial refresh expiry.',
        'The local UI continued, but real end-to-end access over four hours remains unverified.',
        'Repeat the same interval with current signed credentials, provider behavior, and protected-service validation.',
        'unknown authentication and test owners')

    streams=[f'RN-T{i:03d}' for i in list(range(1,21))+[23,24]]+['RN-S036','RN-S048','RN-S049','RN-S050','RN-S051','RN-S052','RN-S055']
    group('blocked-stream-services','BLOCKED','Live message and subscription services are unavailable',streams,
        'Required complete stream checks did not execute. Separate helper probes remain supplementary.',
        'The local portal did not load the actual connected consumer, authenticated peer, or delivery/authorization audit.',
        'Real GraphQL, STOMP, WebSocket, or SSE connections for the named case. Some cases also need reviewed expiry and replay rules.',
        'Recipient identity, reconnect safety, message loss, duplication, and revocation behavior remain unverified.',
        'Provide the named consumer and isolated protocol service. Add the stated identities, topics, and delivery observations.',
        'unknown transport, service, and security owners')
    group('blocked-business-app','BLOCKED','Required business application, identities, or host is unavailable',
        ['RN-D004','RN-D008','RN-D011','RN-D012','RN-D014','RN-W013','RN-W014','RN-W019','RN-S038','RN-S042'],
        'The required complete application-level checks did not execute.',
        'The fixture lacks a supported host, child application, separate A/B permissions, dynamic entitlement service, or protected records.',
        'The named real application composition and authoritative identity, permission, or readiness observations.',
        'Prior-user data isolation, permission removal, and host-specific behavior cannot be accepted from shell descriptors alone.',
        'Bind the stated application host and protected records. Supply separate principals and permission/readiness controls.',
        'unknown application and authorization-service owners')
    group('blocked-native-environment','BLOCKED','Required native browser, device, or desktop environment is unavailable',
        ['RN-A011','RN-A012','RN-H001','RN-H003','RN-H004','RN-H006','RN-H010','RN-H012',
         'RN-D006','RN-D007','RN-D010','RN-D013','RN-W025','RN-W028'],
        'The required native input, lifecycle, device, or desktop sequence did not execute.',
        'The isolated runner lacks the specified touch/IME, crash, sleep, VPN, duplicate-tab, multiple-window/device, persistent-profile, or OpenFin control.',
        'The exact named native environment. Some cases also need server authorization after restoration.',
        'Synthetic events or new tabs cannot prove the requested native recovery and identity behavior.',
        'Run each case in its named controlled environment with its required server or restoration observations.',
        'unknown browser and desktop test owners')
    group('blocked-http-security','BLOCKED','Current HTTP, gateway, or document security composition is unavailable',
        ['RN-S033','RN-S034','RN-S040','RN-S043','RN-S046'],
        'The required composed HTTP, cookie, framing, cross-tab revocation, or cache check did not execute.',
        'Current deployment headers, cross-origin endpoints, cookie sessions, shared revocation, or caching proxy are not bound.',
        'The case-specific current browser/server or proxy composition and its actual effective rules.',
        'Cross-origin delivery, framing, logout propagation, and cached-response isolation remain unverified.',
        'Provide an isolated current composition with the actual effective security and cache configuration.',
        'unknown gateway, authentication, and security owners')
    group('blocked-write-worker','BLOCKED','Required write, upload, progress, or worker implementation is unavailable',
        ['RN-Q020','RN-S053','RN-S054','RN-T026','RN-T027','RN-T028','RN-T029'],
        'The required complete business-write, upload, progress, or worker sequence did not execute.',
        'The scope has no bound operation endpoint, commit store, real progress producer, or declared protected worker/cache implementation.',
        'The named real implementation and authoritative commit, permission, cancellation, or cache observations.',
        'Write duplication, upload authorization, ended-session worker activity, and prior-user cached data remain unverified.',
        'Bind the actual endpoint or worker and its authoritative results. Do not substitute a fake commit counter.',
        'unknown business-service, worker, and test owners')
    group('blocked-tls','BLOCKED','Required TLS failure endpoint is unavailable',['RN-F008','RN-T030'],
        'The local stack used loopback HTTP. The specified TLS-failure check did not execute.',
        'No controlled TLS validation or interruption endpoint was configured.',
        'Actual TLS errors and credential-safe fallback observations.',
        'A generic abort cannot prove TLS rejection or absence of plaintext credential fallback.',
        'Provide a controlled TLS endpoint and the specified certificate or connection fault.',
        'unknown network and test owners')
    group('blocked-runner-binding','BLOCKED','Exact service or repeated-lifecycle test binding is missing',
        ['RN-H002','RN-H007','RN-L007','RN-L008'],
        'H002 reloaded the page. H007 observed offline expiry and reconnect. The required complete assertions did not run.',
        'Current signed-service validation or the exact 100-cycle reauthentication/mount sequence and listener comparison were not bound.',
        'Actual post-reload or post-expiry service rejection, or the full repeated lifecycle with matching resource counts.',
        'Page actions alone cannot establish protected access, expired-token rejection, or repeated lifecycle cleanup.',
        'Bind the current signed service and exact lifecycle observations, then run the missing assertions.',
        'unknown authentication and test owners')

    membership={}
    for g in groups:
        for identifier in g['case_ids']:
            assert identifier not in membership,identifier
            assert rows_by_id[identifier]['status']==g['status'],identifier
            membership[identifier]=g
    expected={r['id'] for r in inventory['rows'] if r['status']!='PASSED'}
    assert set(membership)==expected,(sorted(expected-set(membership)),sorted(set(membership)-expected))
    counts=Counter(g['status'] for r,g in membership.items())
    assert counts=={'FAILED':15,'PARTIALLY_EXECUTED':199,'BLOCKED':71},counts
    impacts={r['case_id']:r for r in read(TASK/'evidence/release-report-execution-20261029/failure-impacts.json')['cases']}
    detailed=[]
    generic=[]
    for identifier in sorted(membership):
        g=membership[identifier];r=rows_by_id[identifier];raw=read(TASK/r['result'])
        actual_reason=r.get('blocker') or r.get('error') or raw.get('blocked_reason')
        row={'id':identifier,'status':r['status'],'group_id':g['id'],'title':r['title'],
            'reason':actual_reason or g['reason'],'plain_group_reason':g['reason'],
            'what_ran':g['what_ran'],'missing':g['missing'],'impact':g['impact'],
            'next_action':g['next_action'],'owner':g['owner'],'definition':r['definition'],
            'result':r['result'],'result_sha256':r['result_sha256'],'assertions_retained':r.get('assertion_count'),
            'original_status':r.get('original_status'),'raw_assertions_failed':r.get('failed_assertions'),
            'blocked_predicates':r.get('blocked_predicates',[]),'limits':r.get('limits',[])}
        if identifier in impacts:
            f=impacts[identifier];row.update({'reason':f['failure_point'],'impact':f['observed_user_impact']+' '+f['conditional_user_impact'],
                'severity':f['severity'],'acceptability':f['acceptability'],'source_links':f['source_links'],
                'assertion_link':f['assertion_link'],'next_action':f['next_action'],'owner':f['owner']})
        if identifier=='RN-H002':
            row['what_ran']='The page reloaded during held renewal. The runner recorded stored-access presence and login visibility.'
            row['reason']='Reload observations ran, but the first post-reload protected request was not validated by the current real service.'
            row['missing']='Actual post-reload protected request and validated server principal.'
        if identifier=='RN-H007':
            row['what_ran']='The browser went offline beyond refresh expiry, then reconnected.'
            row['reason']='Offline/reconnect actions ran, but no current signed-token service checked rejection of expired credentials.'
            row['missing']='Actual signed-token protected-service rejection after reconnection.'
        if identifier in ['RN-L004','RN-L005','RN-L006','RN-L010']:
            row['reason']=g['reason']+' '+row['reason']
            generic.append({'id':identifier,'problem':'The original inventory reason names only a failed count. It does not explain unmatched page states.',
                            'clarification':row['reason']})
        if identifier in ['RN-H002','RN-H007']:
            generic.append({'id':identifier,'problem':'A BLOCKED label can be misread as no actions executed.',
                            'clarification':'Browser actions ran. No complete required protected-service assertion ran.'})
        detailed.append(row)
    data={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'Plain-language reasons for all 285 nonpassing instances. No new execution or status changes.',
        'request':'evidence/user-input-20261029-report-clarity.txt',
        'source_inventory':'evidence/remaining-execution-20261029/aggregate/final-inventory.json',
        'source_inventory_sha256':hashlib.sha256((RUN/'aggregate/final-inventory.json').read_bytes()).hexdigest(),
        'counts':dict(counts),'groups':groups,'rows':detailed,'clarifications':generic,
        'status_definitions':{
            'FAILED':'At least one expected outcome was contradicted by retained execution. A proposed expectation can still need policy review.',
            'PARTIALLY_EXECUTED':'Some required checks ran, but at least one required check or real boundary remains missing or inconclusive.',
            'BLOCKED':'A required case boundary or assertion could not execute. Setup or exploratory actions can still have occurred.'},
        'reconciliation':{'status':'PASSED','groups_exclusive':True,'nonpass_rows':len(detailed),
                          'missing_ids':sorted(expected-set(membership)),'extra_ids':sorted(set(membership)-expected),
                          'status_changes':0,'execution_reruns':0},
        'writing_review':{'standard':'ASD-STE100','automated_check':'PASSED','asd_review':'PENDING','reviewer':None,
                          'reviewed_at':None,'limitations':['Automated checks do not check the complete approved dictionary or grammar rules.']}}
    (HERE/'execution-reason-audit.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'counts':dict(counts),'group_count':len(groups),'rows':len(detailed)}))


if __name__=='__main__':
    main()
