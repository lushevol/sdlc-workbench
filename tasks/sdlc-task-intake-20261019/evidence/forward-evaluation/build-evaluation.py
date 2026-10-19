from pathlib import Path
import json, hashlib, datetime, subprocess, os
source=Path('/Users/lushevol/code/github/ratan-release-impact/workbench')
root=Path('/private/tmp/workbench-intake-forward-20261019')
task=root/'tasks/portal-session-timeout-edge'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
head='84a2b84eea0cc588659fcc912f44c0705571c587'
records=[
('SRC-SKILL','.agents/skills/analyze-requirement/SKILL.md','full','Working tree; evaluated skill'),
('SRC-TASK-GUIDE','tasks/README.md','full','Working tree; task contract'),
('SRC-AUTHORING','knowledge/templates/sdlc/README.md','instructions and handoff; initial combined output truncated','Working tree; authoring contract'),
('SRC-TEMPLATE','knowledge/templates/sdlc/defect-report.md','full; Template block copied','Working tree; defect authoring form'),
('SRC-SAMPLE','knowledge/templates/sdlc/sample-context.md','full','Illustrative only; excluded from business rules'),
('SRC-BEHAVIOR','.agents/skills/verify-implementation/references/behavior-review.md','full','Procedure only'),
('SRC-LINT-GUIDE','.agents/skills/validate-sdlc-documents/SKILL.md','full','Validation procedure'),
('SRC-KINDEX','knowledge/index.md','full','Knowledge navigation'),
('SRC-CINDEX','knowledge/candidates/index.md','full','Candidate navigation and review limits'),
('SRC-RINDEX','knowledge/requirements/README.md','full','Requirement navigation'),
('SRC-TOPIC','knowledge/candidates/security/KT-authentication-and-sessions.md','topic frontmatter and session concepts; combined output truncated','Candidate documentary synthesis; not approved policy'),
('SRC-REQ','knowledge/candidates/requirements/REQ-active-session-renewal.md','full','v2; candidate; recorded intent, no human publication review'),
('SRC-INTENT','knowledge/raw/session-renewal-intent-2026-10-15.txt','full exact bytes','request-2026-10-15; retained user reply'),
('SRC-ACTIVITY','knowledge/raw/session-activity-and-idle-intent-2026-10-15.txt','full exact bytes','reply-2026-10-15; retained user reply'),
('SRC-REPOS','registry/repositories.yaml','registered repository declarations; selected matches reread','Repository identities; not runtime proof'),
('SRC-CAPS','registry/capabilities.yaml','capability declarations; authentication block reread','Capability identities; not execution grants'),
('SRC-SERVICES','registry/services.yaml','service declarations; BFF block reread','Service identities; not deployed reachability'),
('SRC-REGSOURCES','registry/sources.yaml','source declarations; selected matches reread','Exact registered baseline revisions'),
('SRC-PILOT','docs/reviews/AUTHENTICATION_SESSION_PILOT_REPORT.md','lines 1-110 and selected search matches','Secondary source; no new execution'),
('SRC-FULLTRACE','docs/reviews/SESSION_RENEWAL_FULL_TRACE.md','lines 1-80 and selected search matches','Secondary source; SYSTEM verification remains unavailable'),
('SRC-UAT','docs/reviews/SESSION_RENEWAL_UAT1_PLAN.md','lines 1-65 and selected search matches','Secondary setup plan; does not authorize this evaluation to execute'),
('SRC-PRIOR','docs/reviews/PORTAL_SESSION_DEFECT_INTAKE.md','classification, conditions, question log, findings, sources; initial full output truncated; lines 265-310 reread','v4; secondary retained prior answers; original chat unavailable here'),
('SRC-REPRO','docs/reviews/PORTAL_BACKGROUND_SESSION_REPRODUCTION.md','full','v1; historical local investigation; corrected claims require supplement'),
('SRC-HARNESS','docs/reviews/PORTAL_SESSION_HARNESS_REVIEW.md','full','v5; historical evidence corrections; not portal correction'),
('SRC-V1','knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md','lines 102-153','Historical proposal; 105/225-minute conflict; no current policy authority'),
('SRC-EVENTS','knowledge/raw/execution/portal-session-local-2026-10-19/run-001/browser/browser-events-001.json','all 28 events summarized; selected full event details inspected','local-run-001-2026-10-19; instrumented synthetic external boundaries'),
('SRC-EDGE','knowledge/raw/execution/portal-session-local-2026-10-19/setup/edge-runtime-settings.json','full','local-setup-2026-10-19; not original PROD browser settings'),
('SRC-OLDHOME','knowledge/raw/code/mfe-base/99b4eda666bedf06574bc48766e4efdb339f4cc7/src/pages/Home/common/useController.ts.L1-L31.snapshot','full fragment','99b4eda666bedf06574bc48766e4efdb339f4cc7; initial baseline declarations only'),
('SRC-OLDTIMEOUT','knowledge/raw/code/mfe-base/99b4eda666bedf06574bc48766e4efdb339f4cc7/src/components/Timeout/common/useController.ts.snapshot','full','99b4eda666bedf06574bc48766e4efdb339f4cc7; differs from reproduction revision'),
('SRC-OLDTEST','knowledge/raw/code/mfe-base/99b4eda666bedf06574bc48766e4efdb339f4cc7/src/components/Timeout/common/useController.test.tsx.L61-L77.snapshot','full assertion fragment','99b4eda666bedf06574bc48766e4efdb339f4cc7; mock logout count only; no execution claim'),
('SRC-HOME','knowledge/raw/code/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/pages/Home/common/useController.ts.snapshot','lines 65-110','f025513f696476a9cc8162681410cbd21e029bcb; retained source bytes'),
('SRC-TIMEOUT','knowledge/raw/code/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/components/Timeout/common/useController.ts.snapshot','lines 1-85','f025513f696476a9cc8162681410cbd21e029bcb; retained source bytes'),
('SRC-HTTP','knowledge/raw/code/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/src/hooks/service/index.ts.snapshot','lines 15-53','f025513f696476a9cc8162681410cbd21e029bcb; retained source bytes'),
('SRC-BFF','knowledge/raw/code/single-ui-bff/85d7cc03eb12710d6facf581987fd4ae24fc9844/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java.snapshot','lines 300-330','85d7cc03eb12710d6facf581987fd4ae24fc9844; retained source bytes'),
('SRC-ROBOT','knowledge/raw/code/ratan-test-engine/432f898f59fb06414bc14152d6e463a6a1f4eac2/Tests/ratan/workspace/ui/BAU-UI-RP.robot.L185-L204.snapshot','full fragment','432f898f59fb06414bc14152d6e463a6a1f4eac2; prompt wait and click; complete suite uninspected'),
('SRC-LOGIN','knowledge/raw/code/ratan-test-engine/432f898f59fb06414bc14152d6e463a6a1f4eac2/Resources/keywords/commonBiz.resource.L112-L153.snapshot','full fragment','432f898f59fb06414bc14152d6e463a6a1f4eac2; login uses HTTP 200/result assertion'),
('SRC-BROWSERHELPER','knowledge/raw/code/ratan-test-engine/432f898f59fb06414bc14152d6e463a6a1f4eac2/Resources/keywords/playwright.resource.L93-L142.snapshot','full fragment','432f898f59fb06414bc14152d6e463a6a1f4eac2; browser can reuse recent stored context'),
]
inventory=[]
for sid,rel,scope,authority in records:
 p=source/rel
 inventory.append({'source_id':sid,'locator':str(p),'workbench_head':head,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'inspection_scope':scope,'revision_authority_and_limits':authority})
request=task/'evidence/request.json'
inventory.insert(0,{'source_id':'SRC-REQUEST','locator':str(request),'revision':'evaluation-request-20261019','sha256':hashlib.sha256(request.read_bytes()).hexdigest(),'inspection_scope':'full','revision_authority_and_limits':'Exact supplied evaluation scenario and restrictions'})
(task/'evidence/source-inventory.json').write_text(json.dumps({'captured_at':now,'sources':inventory},indent=2)+'\n')
lookup={r['source_id']:r for r in inventory}
events=json.loads((source/records[25][1]).read_text())
summary={'source':lookup['SRC-EVENTS'],'method':'Read retained JSON; no browser or portal execution','events':[{'sequence':e['sequence'],'event':e['event'],'timestamp':e['timestamp'],'visibility':e['visibility'],'details':e['details'] if e['sequence'] in [4,10,11,12,13,14,15,16,17,18,19,22,23] else None} for e in events['events']]}
(task/'evidence/retained-event-review.json').write_text(json.dumps(summary,indent=2)+'\n')
status=json.loads((task/'evidence/source-workspace-status.json').read_text())
resources=[{'id':r['id'],'kind':r['kind'],'environment':r.get('environment'),'allowed_operations':r.get('allowed_operations')} for r in status['resources']]
(task/'evidence/status-summary.json').write_text(json.dumps({'resources':resources,'knowledge_resources':[r for r in resources if r['kind']=='knowledge'],'operations_invoked':[],'limit':'Source workspace metadata only. No external connector or business test was invoked.'},indent=2)+'\n')
text='''---
artifact_kind: defect-report
id: DEFECT-PORTAL-SESSION-EDGE-20261019
version: 1
status: draft
owner: unknown
source_refs: [SRC-REQUEST, SRC-REQ, SRC-INTENT, SRC-ACTIVITY, SRC-PRIOR, SRC-EVENTS, SRC-HOME, SRC-TIMEOUT, SRC-HTTP, SRC-BFF]
related_ids: [REQ-active-session-renewal, single-ui-authentication, single-ui-web, single-ui-bff-api, mfe-base, single-ui-bff]
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Portal session ends after a background tab interval

## Classification and scope

- Defect ID: DEFECT-PORTAL-SESSION-EDGE-20261019.
- Confirmation: Reported incident; retained local failure inspected. This evaluation performed no reproduction.
- Requirement / criterion: REQ-active-session-renewal v2; idle-renewal description and AC-5 through AC-7.
- Affected users: Prior intake reports nearly all users, nearly every time. Measured counts remain unavailable.
- Severity: unassessed. Reported interruption and rework lack measured impact and classification rules.
- Priority: unassessed. No owner decision was found.

The request reports Microsoft Edge, another browser tab, and return after about 30 minutes.
The request reports automatic logout without an extension opportunity.
SRC-REQUEST records these supplied symptoms. It contains no observed production trace.

SRC-PRIOR retains earlier answers about the same symptom.
It records PROD, an awake computer, connected network, and active use of another Edge tab.
It excludes device sleep, network or VPN changes, and another SSO session expiry as reported conditions.
It reports frequent sign-in, workspace loss after sign-in, and rework.
These are attributed prior reports. Their original chat records were not accessed during this evaluation.

This task evaluates intake procedure. Its source workspace remains separate from this isolated task root.
The evaluation permits local source and retained evidence inspection only.
It prohibits browser execution, services, network calls, production actions, and portal fix design or implementation.

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Portal change proposal and impact analysis | NEEDS_CLARIFICATION | Deployment parity and missing-credential recovery intent remain unresolved. SRC-REQ and SRC-EVENTS support investigation only. | Change proposal, portal design, implementation, and causal PROD claims | unknown; resolve Q-NEW-1 through Q-NEW-3 |

- Assessor: agent:codex, isolated forward evaluation.
- Assessment time: ASSESSMENT_TIME.
- Expected behavior: Retain refresh-based renewal after inactivity with usable credentials. Keep the prompt open while renewal remains pending.
- Expected behavior authority: SRC-INTENT, SRC-ACTIVITY, and candidate SRC-REQ AC-5 through AC-7.
- Approval to implement: not established. The supplied evaluation explicitly excludes portal changes.
- Evidence index: evidence/index.md.
- Business review: pending. Intake readiness does not grant approval.

Continued source review remains permitted within the evaluation restrictions.
No status in this task permits a downstream SDLC phase.
Unknown deployed revisions did not prevent the completed local source inspection.

### Existing knowledge review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and retrieval limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| Knowledge index, candidate map, requirement index, session topic | SRC-KINDEX, SRC-CINDEX, SRC-RINDEX, SRC-TOPIC; exact hashes in source inventory | Linked session requirement and source navigation | Local files inspected; no registered knowledge resource in current status | Current deployment mapping |
| Requirement and original reply bytes | SRC-REQ v2; SRC-INTENT request-2026-10-15; SRC-ACTIVITY reply-2026-10-15 | Active renewal; retain idle renewal; AC-5 through AC-7 | Documented user intent exists. Publication approval remains pending | Missing-refresh and suspension recovery conditions |
| Historical V1 design lines 102-153 | SRC-V1; source inventory hash | Extend while refresh remains valid | Historical proposal contains 105-minute and 225-minute refresh duration statements | Effective token policy cannot use these examples alone |
| Prior defect intake and harness correction | SRC-PRIOR v4; SRC-HARNESS v5 | Earlier symptom answers and evidence limits | Secondary records retain prior answers. No original chat or production trace was accessed | Deployment identity and incident lifecycle |
| Registry metadata and source workspace status | SRC-REPOS, SRC-CAPS, SRC-SERVICES, SRC-REGSOURCES; retained status | Declared authentication capability, web service, BFF API, repositories, token contract | Declarations identify candidate relationships. They do not prove deployed integration | Effective environment bindings and accountable owners |

No source review found grounds to repeat the general session-policy question.
Another tab's activity does not establish portal-document activity under AC-1 through AC-4.
AC-5 through AC-7 require usable refresh credentials.
Run 001 starts without refresh credentials. This difference prevents treating that run as a failed execution of those complete criteria.

## Reproduction conditions

```yaml
repository_id: mfe-base
repository_revision: f025513f696476a9cc8162681410cbd21e029bcb
test_revision: null
environment_identity: retained-local-run-001; no new execution
reproduction_status: NOT_RUN
execution_id: null
actual_results: null
retained_execution_refs: [SRC-EVENTS]
reported_environment:
  deployment: PROD, attributed prior report
  deployed_revisions: null
  browser_version: null
  operating_system: null
timing_and_actions:
  timezone: null
  login_at: null
  last_action_at: null
  hidden_at: null
  returned_at: null
  elapsed_time: about 30 minutes, reported
  action_sequence: [Sign in, use another Edge tab, return, observe automatic logout]
browser_lifecycle:
  tab_visibility: background interval reported; original lifecycle unmeasured
  browser_sleep_or_discard: null
  device_sleep_or_lock: prior report excludes device sleep; lock unknown
  effective_settings_and_extensions: null
session_and_connectivity:
  expected_session_policy_ref: REQ-active-session-renewal v2; description and AC-5 through AC-7
  observed_token_lifetimes: null
  network_or_vpn_changes: prior report excludes changes; no production telemetry inspected
  sso_state: prior report excludes another SSO session expiry
reproduction_controls:
  foreground_control: no valid continuously visible portal control in reviewed reports
  mocks_and_instrumentation: retained local run uses instrumentation and synthetic external boundaries
  untested_differences: [Deployed revisions, effective token settings, original Edge lifecycle, identity provider state]
```

The revision above identifies retained local source. It does not identify production deployment.
Retained Run 001 records local Edge 155.0.4283.60 on macOS 26.5 arm64.
Its local settings enable sleeping tabs after 15 minutes. Original user settings remain unknown.
The local run used synthetic external services, process keys, H2, and a toolkit stub.
No new test engine, browser, service, or external connector operation ran.

| Step | Initial condition or action | Expected observable result | Actual observed result |
| --- | --- | --- | --- |
| 1 | Sign in and use another Edge tab | Record deployment, session claims, visibility, and timing | Reported sequence only; original trace unavailable |
| 2 | Return after about 30 minutes | Apply documented renewal only when credential conditions hold | Reported logout without extension |
| 3 | Inspect retained local events | Keep local outcomes separate from incident proof | Freeze, late refresh, missing refresh state, automatic logout, HTTP 401, then CLEAR |

## Hypothesis and impact

- Hypothetical mismatch: Browser suspension can bypass the expected renewal opportunity before refresh credentials become available.
- Observed impact: Retained local authentication state clears. Original production impact remains reported.
- Suspected cause: Hidden-tab suspension is plausible. Production causation remains unresolved.
- Evidence limits: No new reproduction, production mapping, valid foreground control, or incident telemetry was obtained.

| Hypothesis ID | Explanation | Supporting evidence | Contradicting evidence or missing check | Status | Owner and next action |
| --- | --- | --- | --- | --- | --- |
| H-1 | A frozen hidden tab delays refresh beyond access expiry | SRC-EVENTS sequences 10-16; SRC-HOME lines 87-100 | Production lifecycle unknown; no valid foreground portal control | Supported locally; unresolved for PROD | unknown; correlate incident lifecycle with deployed source |
| H-2 | Missing refresh state selects automatic logout before a renewal response | SRC-TIMEOUT lines 25-41; SRC-EVENTS sequences 18-22 | Candidate AC-5 assumes usable refresh credentials; recovery policy unresolved | Supported locally; policy boundary open | unknown; resolve Q-NEW-3 |
| H-3 | Network loss, device sleep, or another SSO expiry caused the reported incident | No supporting production observation inspected | SRC-PRIOR Q-007 and Q-007a exclude these conditions as reported | Unsupported in reported conditions | unknown; retain exclusions unless contrary evidence appears |
| H-4 | A 30-minute timeout policy intentionally logs users out | Only approximate elapsed time is reported | SRC-INTENT and SRC-ACTIVITY retain renewal intent; no current 30-minute policy found | Unsupported by bounded review | unknown; inspect effective settings through Q-NEW-1 |

## Resolution and regression

- Proposed investigation: Resolve deployment identity, incident lifecycle evidence, and the missing-credential recovery rule.
- Evidence plan: Compare exact deployed source with retained snapshots. Retain timestamped, redacted lifecycle and request evidence when access permits.
- Fix scope: unknown. This evaluation does not design or implement a portal correction.
- Regression test: pending. Existing prompt criteria guide investigation; background recovery lacks a complete approved predicate.
- Resolution evidence: null
- Retest status: NOT_RUN
- Closure decision: null

Future execution must separate visible and hidden portal controls with matching credential states.
Its records must disclose clocks, mocks, observers, settings, source revisions, and assertion identities.
No future execution is authorized by this evaluation.

The following scenarios restate candidate AC-5 through AC-7. They establish no passing result or publication approval.

```gherkin
Feature: Recorded idle renewal prompt behavior

  Scenario: AC-5 pending renewal
    Given an idle-expiry prompt and a usable refresh token
    When the user selects renewal and its request remains pending
    Then the prompt has zero successful closure transitions before renewal succeeds

  Scenario: AC-6 successful renewal
    Given an idle-expiry prompt and a usable refresh token
    When the requested renewal succeeds
    Then the prompt closes exactly once after completion

  Scenario: AC-7 rejected renewal
    Given an idle-expiry prompt and an unsuccessful refresh-based renewal request
    When the request rejects
    Then the prompt has zero successful closure transitions and permits another renewal attempt
```

## Facts, inferences, and unresolved questions

- Facts: SRC-REQUEST reports Edge, another tab, about 30 minutes, and logout without extension.
- Documented intent: Raw replies retain active and idle renewal. Candidate prompt criteria have explicit credential conditions.
- Retained local facts: Sequence 19 selects automatic logout at 08:23:06.398Z. Sequence 22 records HTTP 401 at 08:23:06.477Z.
- Inference: The retained local mechanism can explain the symptom. It cannot establish production causation.
- Unresolved questions: Q-NEW-1 through Q-NEW-3 remain pending. Their resolution owners are unknown.

### Answer and question log

No questions were sent to the user. Pending questions remain in this task.

| Round and ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| Supplied Q-KNOWN-1 | Browser, actions, interval, and symptom | Edge; another tab; about 30 minutes; logout without extension | SRC-REQUEST | answered | unknown | Preserve reported facts; avoid duplicate questions |
| Prior Q-KNOWN-2 | Environment, scale, and impact | PROD; nearly all users, nearly every time; workspace loss and rework | SRC-PRIOR Q-001, Q-006, Q-006a | answered qualitatively; secondary source | unknown | Preserve scale limits; no quantified severity claim |
| Prior Q-KNOWN-3 | Awake device, connected network, and active second tab | Yes, all three | SRC-PRIOR Q-007 | answered as reported; secondary source | unknown | Do not re-ask; inspect tab suspension separately |
| Prior Q-KNOWN-4 | Device sleep, VPN/network changes, another SSO session expiry | None reported | SRC-PRIOR Q-007a | answered as reported; secondary source | unknown | Retain exclusions unless contrary evidence appears |
| Review Q-KNOWN-5 | General session intent | Retain active renewal and refresh-token renewal after inactivity | SRC-INTENT; SRC-ACTIVITY; SRC-REQ | answered; publication review pending | unknown | Reuse intent; preserve credential conditions |
| Round 1 Q-NEW-1 | Which incident deployment revisions, effective token settings, and Edge version/settings apply? | unknown | Registry and report review do not resolve effective deployment | pending; not sent | unknown | Mapping can change the affected path; obtain deployment and browser records |
| Round 1 Q-NEW-2 | Which incident timestamps and redacted lifecycle/request records establish freeze, resume, credential presence, and response order? | unknown | SRC-PRIOR has no retained production trace | pending; not sent | unknown | A local mechanism cannot establish incident cause; retain operational evidence when permitted |
| Round 1 Q-NEW-3 | Which recovery outcome applies when refresh credentials are absent, or refresh remains pending after return? | unknown | SRC-REQ AC-5 through AC-7 assume usable refresh credentials | pending; not sent | unknown | Different recovery intent changes correction scope; obtain the narrow owner decision |

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| SRC-REQ and exact raw replies already record session intent | A general policy question would repeat available information | unknown | Use the known intent and ask only Q-NEW-3 |
| SRC-EVENTS and exact retained source support a local delayed-refresh chain | The mechanism supports investigation without proving production causation | unknown | Resolve Q-NEW-1 and Q-NEW-2 |
| SRC-HARNESS corrects the original report's capture attribution and test total | Original report conclusions cannot be reused without those limits | unknown | Preserve unresolved return-capture attribution and unsupported earlier count |
| Candidate criteria assume usable refresh credentials; Run 001 lacks them | That run cannot verify the complete candidate prompt criteria | unknown | Resolve Q-NEW-3 before a correction proposal |
| Robot fragments wait for the prompt and click Extend; browser setup can reuse stored context | Inspected fragments do not assert pending renewal, exact closure count, or production parity | unknown | Inspect the complete setup and assertions before any verification claim |

## Sources

All source bytes remain in their original locations.
The inventory records exact locators, hashes, inspection scopes, and authority limits.
Source checkout HEAD was `84a2b84eea0cc588659fcc912f44c0705571c587` during discovery.
Modified guide bytes require their recorded hashes; HEAD alone does not identify them.

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
SOURCE_ROWS

Full procedural and inspected-source inventory: evidence/source-inventory.json.
'''.replace('ASSESSMENT_TIME',now)
source_rows=[]
for sid in ['SRC-REQUEST','SRC-REQ','SRC-INTENT','SRC-ACTIVITY','SRC-PRIOR','SRC-EVENTS','SRC-EDGE','SRC-HOME','SRC-TIMEOUT','SRC-HTTP','SRC-BFF','SRC-HARNESS','SRC-ROBOT','SRC-BROWSERHELPER','SRC-V1']:
 r=lookup[sid]
 source_rows.append(f"| {sid} | `{r['locator']}` | {r.get('revision',r.get('revision_authority_and_limits','unknown').split(';')[0])} | `{r['sha256']}` | unknown; {r['revision_authority_and_limits']} |")
text=text.replace('SOURCE_ROWS','\n'.join(source_rows))
(task/'intake.md').write_text(text)
index='''---
standard: ASD-STE100
automated_check: NOT_RUN
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Intake evidence index

All new artifacts remain under this isolated task.
Existing raw sources and audit history remain at their original paths.
No new browser, service, or production execution occurred.

| Evidence ID | Claim or question | Locator and retained path | Exact revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |
'''
for r in inventory:
 index+=f"| {r['source_id']} | Intake source review | `{r['locator']}`; original retained path | {r.get('revision',head)}; {r['inspection_scope']} | `{r['sha256']}` | {r['revision_authority_and_limits']} |\n"
for name,claim in [('request.json','Reported symptoms and evaluation restrictions'),('source-workspace-status.json','Source resource discovery; no operations invoked'),('status-summary.json','No registered knowledge resource; direct files used'),('retained-event-review.json','Local event order; no new portal execution')]:
 p=task/'evidence'/name
 index+=f"| EVAL-{name} | {claim} | `evidence/{name}` | {now} | `{hashlib.sha256(p.read_bytes()).hexdigest()}` | Retained evaluation output; no production proof |\n"
(task/'evidence/index.md').write_text(index)
checks=[]
def run_check(label,args,out):
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
 r=subprocess.run(args,cwd=root,env=env,capture_output=True,text=True)
 (task/'evidence'/out).write_text(r.stdout)
 (task/'evidence'/(out+'.stderr.txt')).write_text(r.stderr)
 checks.append({'label':label,'argv':args,'cwd':str(root),'exit_code':r.returncode,'stdout_path':str(task/'evidence'/out),'stderr_path':str(task/'evidence'/(out+'.stderr.txt'))})
 return r
r=run_check('Artifact lint',[str(source/'.venv/bin/ai-sdlc'),'lint',str(task/'intake.md')],'artifact-lint.json')
if r.returncode==0:
 p=task/'intake.md';p.write_text(p.read_text().replace('automated_check: NOT_RUN','automated_check: PASSED',1))
 r=run_check('Final artifact lint after metadata update',[str(source/'.venv/bin/ai-sdlc'),'lint',str(task/'intake.md')],'artifact-lint-final.json')
(task/'evidence/checks.json').write_text(json.dumps(checks,indent=2)+'\n')
actions=[
 {'action':'Read evaluated skill','result':'Complete skill instructions inspected; required references followed','sources':['SRC-SKILL']},
 {'action':'Create task directory before project source discovery','result':'Created isolated tasks/portal-session-timeout-edge/evidence'},
 {'action':'Read task contract, authoring contract, and defect template','result':'Template selected for reported unexpected behavior','sources':['SRC-TASK-GUIDE','SRC-AUTHORING','SRC-TEMPLATE']},
 {'action':'Initial template-copy attempt using python','exit_code':127,'result':'python was unavailable; no file created'},
 {'action':'Inspect required references and source inventory after failed copy','result':'Task directory existed, but intake file creation was delayed until retry','procedure_deviation':'Initial source inventory ran before the intake copy succeeded. Failure was corrected immediately with python3.'},
 {'action':'Retry template copy using python3','exit_code':0,'result':'Copied only the defect Template block; retained supplied scenario in evidence/request.json'},
 {'action':'Inspect source checkout status and revision','result':'Source worktree contained existing changes; no edits, staging, or commits performed by evaluation','revision':head},
 {'action':'Find ai-sdlc runtime','result':'Not on PATH. Existing .venv/bin/ai-sdlc located; no installation performed'},
 {'action':'Review indexes, registry metadata, linked requirement, and exact raw intent','result':'Existing user intent found before any question round','sources':['SRC-KINDEX','SRC-CINDEX','SRC-RINDEX','SRC-TOPIC','SRC-REQ','SRC-INTENT','SRC-ACTIVITY','SRC-REPOS','SRC-CAPS','SRC-SERVICES','SRC-REGSOURCES']},
 {'action':'Review prior reports and retained prior answers','result':'Avoided repeat policy, impact, environment, sleep, network, VPN, and SSO questions','sources':['SRC-PRIOR','SRC-REPRO','SRC-HARNESS','SRC-PILOT','SRC-FULLTRACE','SRC-UAT']},
 {'action':'Inspect historical design and exact local source snapshots','result':'Recorded duration conflict and local missing-refresh/late-refresh path; no portal fix proposed','sources':['SRC-V1','SRC-HOME','SRC-TIMEOUT','SRC-HTTP','SRC-BFF','SRC-OLDHOME','SRC-OLDTIMEOUT']},
 {'action':'Inspect retained assertion and helper fragments','result':'Recorded narrow assertion limits; no behavior verification claimed','sources':['SRC-OLDTEST','SRC-ROBOT','SRC-LOGIN','SRC-BROWSERHELPER']},
 {'action':'Inspect retained events and local Edge settings','result':'Read all 28 event identities and selected details; derived task summary; no browser execution','sources':['SRC-EVENTS','SRC-EDGE']},
 {'action':'Source workspace status','argv':[str(source/'.venv/bin/ai-sdlc'),'--workspace',str(source),'status'],'exit_code':0,'output':str(task/'evidence/source-workspace-status.json'),'result':'Read local discovery metadata; no registered knowledge resource; no call operations invoked'},
 {'action':'Record readiness and questions','result':'NEEDS_CLARIFICATION for portal change proposal and impact analysis. Three focused pending questions retained; no real user contact'},
 {'action':'Lint intake using existing runtime','result':'See evidence/checks.json and final retained output','checks':checks}
]
limits=[
 'No new browser tests, service execution, network calls, production actions, or portal correction occurred.',
 'Prior answers are attributed through the retained intake; original chat bytes were not accessed.',
 'Local evidence uses synthetic external boundaries, instrumentation, and a toolkit stub; production parity is unknown.',
 'No valid continuously visible portal control was verified.',
 'Run 001 returned-page capture attribution and earlier test-success total remain limited by the harness correction.',
 'Source snapshot hashes identify inspected bytes; the raw manifest itself was not audited in this evaluation.',
 'Initial long combined outputs were truncated; targeted rereads and inventory inspection scopes identify the actual reviewed content.',
 'The evaluation root contains task artifacts and no initialized business workspace configuration.',
 'Business review, publication review, and complete ASD writing review remain pending.'
]
ambiguities=[
 {'issue':'Ordering of discovery and knowledge review','detail':'The skill asks for knowledge review before questions but places status discovery later under Analyze. Local files provided a permitted fallback; status later confirmed no knowledge resource.'},
 {'issue':'Boundary between READY_WITH_LIMITS and NEEDS_CLARIFICATION','detail':'Both permit more evidence collection and block downstream phases. This evaluation uses NEEDS_CLARIFICATION because a material recovery rule remains unresolved.'},
 {'issue':'Existing task reuse across an isolated evaluation','detail':'The source checkout contains a matching prior intake outside tasks/. The evaluation created a separate task because its explicit isolated-root instruction takes precedence.'},
 {'issue':'Handling missing runtime aliases','detail':'Template examples use python and ai-sdlc. This environment required python3 and the existing .venv executable. This is environment adaptation, not a skill defect.'}
]
evaluation={'evaluation_root':str(root),'task_path':str(task),'assessor':'agent:codex','assessment_time':now,'readiness':'NEEDS_CLARIFICATION','named_next_phase':'Portal change proposal and impact analysis','actions':actions,'sources_actually_inspected':inventory,'outputs':[str(p) for p in sorted(task.rglob('*')) if p.is_file()],'pending_questions':['Q-NEW-1: Which incident deployment revisions, effective token settings, and Edge version/settings apply?','Q-NEW-2: Which incident timestamps and redacted lifecycle/request records establish freeze, resume, credential presence, and response order?','Q-NEW-3: Which recovery outcome applies when refresh credentials are absent, or refresh remains pending after return?'],'evidence_limitations':limits,'skill_ambiguities':ambiguities,'writing_review':{'standard':'ASD-STE100','automated_check':'PASSED' if r.returncode==0 else 'FAILED','asd_review':'PENDING','reviewer':None,'reviewed_at':None,'limitations':['Automated checks do not check the complete approved dictionary or grammar rules.']}}
(root/'evaluation-actions.json').write_text(json.dumps(evaluation,indent=2)+'\n')
print(json.dumps({'task_path':str(task),'readiness':evaluation['readiness'],'lint_exit_code':r.returncode,'check_outputs':checks,'source_count':len(inventory),'evaluation_actions':str(root/'evaluation-actions.json')},indent=2))
