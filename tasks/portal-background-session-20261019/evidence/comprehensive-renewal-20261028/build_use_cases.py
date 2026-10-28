"""Render user journeys that link the canonical case definitions."""
import json
from pathlib import Path

D=Path(__file__).resolve().parent
T=D.parent.parent
core=json.loads((D/'core-cases.json').read_text())
other=json.loads((D/'workspace-transport-cases.json').read_text())
security=json.loads((D/'security-use-cases.json').read_text())
executed=json.loads((D/'new-e2e-cases.json').read_text())
titles=[
 ('UC-R01','Continue activity with each supported input','Keep eligible activity renewing the session','Mouse, keyboard, or scroll activity begins','At least 30 seconds of access remain','Generate source-defined input for 15 seconds','Assert successful renewal and protected validation','Continuous input can expose the recorded debounce defect'),
 ('UC-R02','Use mixed input and embedded application controls','Observe which input reaches the shell','User changes input method or application context','Identify same-origin and cross-origin boundaries','Exercise the named input context','Measure shell events and the applicable renewal target','Cross-origin, touch, composition, and passive activity eligibility remain unresolved'),
 ('UC-R03','Renew at the activity cutoff','Check both sides of the 25-second implementation guard','An activity callback runs','Use an isolated controlled clock','Invoke shared activity renewal at each boundary','Count outbound requests separately from renewal success','These are implementation thresholds, not business lifetime policies'),
 ('UC-R04','Use manual recovery near refresh expiry','Check the source recovery deadline','User selects manual renewal','Use a timeout controller and controlled refresh expiry','Activate renewal around refresh expiry minus 2000 milliseconds','Count accepted relogin requests','The two-second margin is source behavior'),
 ('UC-R05','Reuse or acquire refresh credentials','Check the three-hour reuse branch','The shell requests refresh acquisition','Current identity and expiry are known','Request acquisition around the reuse boundary','Count acquisition POSTs','The reuse interval is implementation behavior'),
 ('UC-R06','Recover from delayed clocks and callbacks','Separate elapsed time from callback delivery','A timer runs late or browser visibility changes','Record absolute expiry and current visibility','Deliver the callback under the named state','Observe acquisition and timeout decisions','Clock skew acceptance remains unresolved'),
 ('UC-R07','Complete manual recovery','Keep the prompt pending until usable access arrives','User selects Extend','A usable refresh credential exists','Hold, reject, or complete the renewal response','Assert prompt transitions and credential installation','Service provider behavior remains outside substituted responses'),
 ('UC-R08','Leave or replace a pending recovery','Keep old controller actions isolated','Logout, unmount, or account replacement occurs','A pending request belongs to session A','Complete the ownership transition before delivery','Assert zero obsolete credential installation','Cross-device revocation needs separate policy'),
 ('UC-R09','Validate the renewal response shape','Reject unusable access before prompt closure','The relogin response arrives','Use the real response interceptor','Deliver each concrete invalid or ambiguous response','Observe installation and closure separately','Browser header normalization and future-iat policy need review'),
 ('UC-R10','Deliver old responses after account changes','Prevent prior-session results from changing the current user','A delayed response reaches the client','A and B have distinct session generations','Change ownership before releasing the old response','Assert current identity and zero stale writes','Local isolation does not establish server revocation'),
 ('UC-R11','Share a pending operation within its actual scope','Avoid repeated same-owner acquisition or controller calls','Several callers arrive before settlement','Use one epoch and one mounted Timeout controller for manual actions','Invoke the declared number of callers','Assert the operation count and final owner','Direct relogin calls have different cancellation behavior'),
 ('UC-R12','Reorder concurrent work','Expose stale callback and completion interactions','Requests or timers finish together','Hold independently identified operations','Deliver both controlled orders','Record each final owner and state','Several same-epoch ordering policies remain unresolved'),
 ('UC-R13','Repeat recovery and lifecycle operations','Detect accumulated state and resources','The fixture starts a finite loop','Record expected mounted-resource baselines','Complete the declared cycle count','Assert pending-network settlement and stable resource counts','Finite loops do not prove unlimited lifetime or performance'),
 ('UC-R14','Continue beyond initial refresh expiry','Test the requested four-hour activity behavior','The initial refresh expiry occurs','Activity and successful renewals continue before access deadlines','Advance through four controlled hours','Assert zero prompts caused solely by elapsed lifetime','No finite test proves indefinite renewal'),
 ('UC-R15','Resume across browser and device habits','Measure identity and recovery across lifecycle boundaries','Reload, sleep, crash, network change, or another context occurs','Use distinct synthetic contexts and record real lifecycle events','Apply the named lifecycle event','Record authorization and installed state','Global logout and restoration policies remain unresolved'),
 ('UC-R16','Handle rejected or incomplete renewal','Preserve truthful pending and failure outcomes','The service rejects, times out, or returns malformed success','Refresh remains usable unless the case states otherwise','Deliver the named failure through the real client','Assert no false successful closure and applicable retry state','Maximum pending duration and service retry policy remain unresolved'),
]
usecases=[]
for uid,title,goal,trigger,pre,action,response,limit in titles:
    usecases.append(dict(id=uid,title=title,goal=goal,trigger=trigger,preconditions=[pre],
        main_flow=[dict(action=action,response=response)],alternatives=[dict(condition='The named boundary or failure occurs',outcome=limit)],limits=[limit]))
usecases+=other['use_cases']
for s in security:
    usecases.append({**s,'preconditions':[s['preconditions']], 'main_flow':[dict(action=s['main_flow'],response=s['goal'])],
        'alternatives':[dict(condition=s['alternatives'],outcome=s['limits'])]})
for c in executed:
    usecases.append(dict(id=c['use_case'],title=c['title'],goal='Verify the stated real-browser predicate',trigger=c['when'][0],preconditions=c['given'],
        main_flow=[dict(action='Run the linked canonical browser case',response='Retain per-assertion results and source identity')],
        alternatives=[dict(condition='A predicate fails',outcome='Save the failure before continuing')],limits=[c['limits']]))
usecases += [
 dict(id='UC-C01',title='Combine declared session states',goal='Cover declared interactions with independent observable assertions',trigger='The interaction runner selects one fixture row',preconditions=['Create an isolated context for every row'],main_flow=[dict(action='Apply the selected factors in canonical order',response='Measure stale writes, authorization, and mutation uniqueness')],alternatives=[dict(condition='A guard prevents renewal',outcome='Record zero outbound requests without fabricating success')],limits=['Pairwise design coverage does not establish business correctness']),
 dict(id='UC-C02',title='Enumerate late-response event orders',goal='Keep old replies from changing a replacement identity',trigger='The runner selects one six-event ordering',preconditions=['A and B have distinct synthetic sessions'],main_flow=[dict(action='Deliver the exact canonical event sequence',response='Assert final B identity and zero obsolete writes')],alternatives=[dict(condition='The A response rejects or is malformed',outcome='B remains isolated')],limits=['Only the declared finite partial order is exhausted'])]
assert len({u['id'] for u in usecases})==len(usecases)
allcases=core+other['cases']+json.loads((D/'security-cases.json').read_text())+executed
lines=['---\nartifact_kind: use-case\nid: USE-CASES-comprehensive-session-renewal\nversion: 1\nstatus: draft\nowner: unknown\nsource_refs: [SRC-comprehensive-renewal-20261028]\nrelated_ids: [REQ-active-session-renewal]\nreview:\n  state: pending\n  reviewer: null\n  reviewed_at: null\nwriting_review:\n  standard: ASD-STE100\n  automated_check: NOT_RUN\n  asd_review: PENDING\n  reviewer: null\n  reviewed_at: null\n  limitations:\n    - Automated checks do not check the complete approved dictionary or grammar rules.\n---\n',
 '# Session renewal user journeys\n\n',
 '> **Critical conclusions: Security acceptance remains blocked by a reproduced revocation gap and missing target evidence.**\n'
 '> Action: resolve the [security findings](07-security-review-renewal.md#findings-and-actions). Consequence: these journeys cannot establish secure deployment.\n'
 '> Owner: unknown service and application owners. Evidence: [security probe](evidence/comprehensive-renewal-20261028/security-probe-execution.json).\n\n',
 '## Context and source facts\n\n'
 'The [exact user request](evidence/user-input-20261028-comprehensive-renewal.txt) defines this test-design scope.\n'
 'Primary actors are synthetic portal users A and B. Supporting actors include the shell, BFF, application containers, and transport servers.\n'
 'The system boundary includes session continuation and concurrent work. It includes authorization observations at downstream boundaries.\n'
 'The [requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) remains candidate version 5 with pending publication review.\n'
 'The [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json) identifies inspected revisions and retained bytes.\n\n',
 '## Proposed flow conditions\n\n'
 'Use the [canonical fixture and oracles](06-test-cases.md#renewal-fixture-and-oracles). Each journey states additional conditions below.\n'
 'Distinguish target behavior, source observations, proposed security invariants, and unresolved policy.\n'
 'A journey succeeds only when its linked assertions pass. A rejected or pending response cannot establish successful renewal.\n'
 'Policy-open journeys permit observation. Their acceptance remains blocked until the applicable rule is reviewed.\n\n',
 f'## Main flow\n\nThis catalog contains {len(usecases)} use cases. Detailed test steps exist only in the canonical test catalog.\n']
def s(v):return ' '.join(v) if isinstance(v,list) else str(v)
for u in usecases:
    case_ids=[c['id'] for c in allcases if c['use_case']==u['id']]
    if u['id']=='UC-C01':case_ids=['RN-C001','RN-C002']
    if u['id']=='UC-C02':case_ids=['RN-O001']
    lines += [f"\n### {u['id']}\n\n**{u['title']}**\n\n",f"Goal: {u['goal']}.\n\nTrigger: {u['trigger']}.\n\nPreconditions: {s(u['preconditions'])}.\n\n",
        '| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |\n| --- | --- | --- | --- | --- |\n']
    refs=', '.join(f"[{cid}](06-test-cases.md#{cid.lower()})" for cid in case_ids)
    for i,flow in enumerate(u['main_flow'],1):
        lines.append(f"| {i} | {flow['action']} | {flow['response']} | See linked case evidence classes | {refs if i==1 else 'Same canonical cases'} |\n")
    lines.append(f"\nLimits: {s(u['limits'])}\n")
lines.append('\n## Alternative and exception flows\n\n| Flow ID | Branch from step | Condition | Action and response | Outcome | Criterion IDs |\n| --- | --- | --- | --- | --- | --- |\n')
for u in usecases:
    for i,a in enumerate(u['alternatives'],1):
        lines.append(f"| [{u['id']}-ALT-{i}](#{u['id'].lower()}) | 1 | {a['condition']} | Retain the linked case observations | {a['outcome']} | See each canonical case; unresolved policy stays blocked |\n")
lines += ['\n## Related artifacts\n\n| Artifact ID | Relationship | Location |\n| --- | --- | --- |\n'
    '| Test catalog | Single definition source | [Canonical cases](06-test-cases.md#comprehensive-renewal-expansion) |\n'
    '| Strategy | Scope and completion | [Test strategy](05-test-strategy-renewal.md) |\n'
    '| Security review | Threats and evidence | [Review](07-security-review-renewal.md) |\n'
    '| Coverage | Separate coverage dimensions | [Coverage](09-renewal-coverage.md) |\n',
    '\n## Sources and evidence limits\n\n| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |\n| --- | --- | --- | --- | --- |\n'
    '| SRC-comprehensive-renewal-20261028 | [Exact request](evidence/user-input-20261028-comprehensive-renewal.txt) | user-message-20261028 | [Manifest](evidence/comprehensive-renewal-20261028/source-manifest.json) | User; design and assessment authorization |\n'
    '| Requirement and inspected code | [Manifest](evidence/comprehensive-renewal-20261028/source-manifest.json) | Per-source revisions | Per-source SHA-256 | Publication review and target parity remain unproved |\n',
    '\n## Unknowns and risks\n\n| Finding or question | Evidence | Consequence | Owner | Next action |\n| --- | --- | --- | --- | --- |\n'
    '| Revocation gap | [Security result](07-security-review-renewal.md#findings-and-actions) | Logout cannot establish complete credential invalidation | unknown service owner | Correct the boundary and rerun replay cases |\n'
    '| Transport and restoration policy | [Policy register](05-test-strategy-renewal.md#policy-questions) | Several acceptance outcomes remain blocked | unknown business and security owners | Record one reviewed answer per policy scope |\n',
    '\n## Review and execution status\n\n'
    'Required review covers actors, eligibility, recovery, authorization, retention, and transport behavior. Actual human review reference: null.\n'
    'Three new browser journeys passed within their disclosed fixture. Other new journeys remain unexecuted.\n'
    'Read the [execution report](08-test-execution-renewal.md) for exact predicates, substitutions, failures, and source identity.\n']
(T/'03-use-cases-renewal.md').write_text(''.join(lines))
(D/'use-case-manifest.json').write_text(json.dumps({'use_case_count':len(usecases),'ids':[u['id'] for u in usecases]},indent=2)+'\n')
print(len(usecases))
