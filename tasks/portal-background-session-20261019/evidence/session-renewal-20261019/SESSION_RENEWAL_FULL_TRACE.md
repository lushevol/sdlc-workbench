---
artifact_kind: traceability-record
id: TRACE-active-session-renewal-full-20261019
version: 1
status: draft
owner: unknown
source_refs:
- REQ-active-session-renewal-v2
- SRC-session-full-ec3bcb4fe044c2b358
- SRC-session-full-c9a0c0bc463646adea
- SRC-session-uat1-9f4cb9a32667ba115
related_ids:
- TRACE-active-session-renewal-pilot
- REQ-active-session-renewal
- GF-session-renewal-verification-gates
- mfe-base
- single-ui-authentication
- single-ui-web
- single-ui-sso-token-family
- AC-1
- AC-2
- AC-3
- AC-4
- AC-5
- AC-6
- AC-7
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Full session renewal traceability

## Scope and identities

- Capability ID: single-ui-authentication.
- Requirement ID: REQ-active-session-renewal, version 2.
- Repository ID: mfe-base.
- Service ID: single-ui-web.
- Contract ID: single-ui-sso-token-family.
- Comparison base: `dddb76c8e8ba8ea66bb941feaad562740fdb8346`.
- Assessed revision: `4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8`.
- Included inventory: AC-1 through AC-7.
- Required verification level: SYSTEM for each criterion.
- Selected environment: UAT1.
- Live UAT1 execution: NOT_RUN.
- Excluded boundaries: Deployment, global revocation, cross-origin activity, and external provider policy assessment.

All seven complete criteria remain NOT_VERIFIED.
The requirement remains a candidate without recorded human approval.
The recorded reviewer and responsible owners remain unknown.
The controlled execution runs exact TypeScript after the disclosed transformation.
It does not run React, a browser, the BFF, or the identity provider.

This record succeeds [the earlier partial trace](SESSION_RENEWAL_BEHAVIOR_TRACE.md).
It preserves BEH-05, BEH-06, and BEH-07 at version 1.
It adds BEH-01 through BEH-04 at version 1.
The retained requirement predicates remain unchanged.

Scope risk: medium.
Session activity, credentials, expiry timers, interceptors, and UI state cross several interfaces.
Business source remains unchanged during this review stage.

## Requirement and criterion declarations

| Requirement ID | Criterion ID | Measurable expected behavior | Source revision | Knowledge review state |
| --- | --- | --- | --- | --- |
| REQ-active-session-renewal | AC-1 | Then at least one successful renewal occurs before the controlled interval ends | document-version:2 | candidate; pending |
| REQ-active-session-renewal | AC-2 | Then at least one successful renewal occurs before the controlled interval ends | document-version:2 | candidate; pending |
| REQ-active-session-renewal | AC-3 | Then at least one successful renewal occurs before the controlled interval ends | document-version:2 | candidate; pending |
| REQ-active-session-renewal | AC-4 | Then zero fresh SSO prompts occur solely because elapsed session time crosses an earlier maximum | document-version:2 | candidate; pending |
| REQ-active-session-renewal | AC-5 | Then the prompt has zero successful closure transitions before renewal succeeds | document-version:2 | candidate; pending |
| REQ-active-session-renewal | AC-6 | Then the prompt closes exactly once after completion | document-version:2 | candidate; pending |
| REQ-active-session-renewal | AC-7 | Then the prompt has zero successful closure transitions and permits another renewal attempt | document-version:2 | candidate; pending |

| Behavior ID | Version | Criterion ID | Actor | Required verification level |
| --- | --- | --- | --- | --- |
| REQ-active-session-renewal:BEH-01 | 1 | AC-1 | Portal user | SYSTEM |
| REQ-active-session-renewal:BEH-02 | 1 | AC-2 | Portal user | SYSTEM |
| REQ-active-session-renewal:BEH-03 | 1 | AC-3 | Portal user | SYSTEM |
| REQ-active-session-renewal:BEH-04 | 1 | AC-4 | Portal user | SYSTEM |
| REQ-active-session-renewal:BEH-05 | 1 | AC-5 | Portal user | SYSTEM |
| REQ-active-session-renewal:BEH-06 | 1 | AC-6 | Portal user | SYSTEM |
| REQ-active-session-renewal:BEH-07 | 1 | AC-7 | Portal user | SYSTEM |

These scenarios preserve the candidate requirement.
Raw intent names activity, continued renewal, and retained refresh renewal.
The detailed fixture thresholds and successful-renewal definition still require human review.

```gherkin
Feature: Active session renewal

Scenario: AC-1
  Given a valid portal session with at least 30 seconds remaining before access expiry
  When mouse movement occurs every 100 milliseconds for 15 seconds
  Then at least one successful renewal occurs before the controlled interval ends

Scenario: AC-2
  Given a valid portal session with at least 30 seconds remaining before access expiry
  When keyboard input occurs every 100 milliseconds for 15 seconds
  Then at least one successful renewal occurs before the controlled interval ends

Scenario: AC-3
  Given a valid portal session with at least 30 seconds remaining before access expiry
  When scroll activity occurs every 100 milliseconds for 15 seconds
  Then at least one successful renewal occurs before the controlled interval ends

Scenario: AC-4
  Given successful renewal responses and accepted user activity before each access deadline
  When a controlled clock advances through four hours of continued activity
  Then zero fresh SSO prompts occur solely because elapsed session time crosses an earlier maximum

Scenario: AC-5
  Given an idle-expiry prompt and a usable refresh token
  When the user selects renewal and its request remains pending
  Then the prompt has zero successful closure transitions before renewal succeeds

Scenario: AC-6
  Given an idle-expiry prompt and a usable refresh token
  When the requested renewal succeeds
  Then the prompt closes exactly once after completion

Scenario: AC-7
  Given an idle-expiry prompt and an unsuccessful refresh-based renewal request
  When the request rejects
  Then the prompt has zero successful closure transitions and permits another renewal attempt
```

## Relationship evidence

| From ID | Relationship | To ID | Evidence | Evidence class | Limit |
| --- | --- | --- | --- | --- | --- |
| REQ-active-session-renewal | has criterion | AC-1 | [REQ-active-session-renewal.md:54–62](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L54-L62) | declaration; CONFIRMED | Candidate intent |
| REQ-active-session-renewal | has criterion | AC-2 | [REQ-active-session-renewal.md:63–71](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L63-L71) | declaration; CONFIRMED | Candidate intent |
| REQ-active-session-renewal | has criterion | AC-3 | [REQ-active-session-renewal.md:72–80](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L72-L80) | declaration; CONFIRMED | Candidate intent |
| REQ-active-session-renewal | has criterion | AC-4 | [REQ-active-session-renewal.md:81–89](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L81-L89) | declaration; CONFIRMED | Candidate intent |
| REQ-active-session-renewal | has criterion | AC-5 | [REQ-active-session-renewal.md:90–98](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L90-L98) | declaration; CONFIRMED | Candidate intent |
| REQ-active-session-renewal | has criterion | AC-6 | [REQ-active-session-renewal.md:99–107](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L99-L107) | declaration; CONFIRMED | Candidate intent |
| REQ-active-session-renewal | has criterion | AC-7 | [REQ-active-session-renewal.md:108–116](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L108-L116) | declaration; CONFIRMED | Candidate intent |
| REQ-active-session-renewal:BEH-01 | has narrower assertion | ASSERT-full-mouse-requests | [run-mfe-session-characterization-successor.cjs:152–168](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L152-L168) | inspected assertion; CONFIRMED | Controlled source predicate; SYSTEM coverage unresolved |
| REQ-active-session-renewal:BEH-02 | has narrower assertion | ASSERT-full-keyboard-requests | [run-mfe-session-characterization-successor.cjs:152–168](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L152-L168) | inspected assertion; CONFIRMED | Controlled source predicate; SYSTEM coverage unresolved |
| REQ-active-session-renewal:BEH-03 | has narrower assertion | ASSERT-full-scroll-requests | [run-mfe-session-characterization-successor.cjs:152–168](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L152-L168) | inspected assertion; CONFIRMED | Controlled source predicate; SYSTEM coverage unresolved |
| REQ-active-session-renewal:BEH-04 | has narrower assertion | ASSERT-full-four-hour-home | [run-mfe-session-characterization-successor.cjs:170–194](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L170-L194) | inspected assertion; CONFIRMED | Controlled source predicate; SYSTEM coverage unresolved |
| REQ-active-session-renewal:BEH-05 | has narrower assertion | ASSERT-session-renewal-pending | [run-mfe-session-characterization-successor.cjs:261–268](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L261-L268) | inspected assertion; CONFIRMED | Controlled source predicate; SYSTEM coverage unresolved |
| REQ-active-session-renewal:BEH-06 | has narrower assertion | ASSERT-session-renewal-success | [run-mfe-session-characterization-successor.cjs:261–268](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L261-L268) | inspected assertion; CONFIRMED | Controlled source predicate; SYSTEM coverage unresolved |
| REQ-active-session-renewal:BEH-07 | has narrower assertion | ASSERT-session-renewal-retry | [run-mfe-session-characterization-successor.cjs:269–277](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L269-L277) | inspected assertion; CONFIRMED | Controlled source predicate; SYSTEM coverage unresolved |

Grades apply to the stated narrow relationship.
They do not grant approval or complete behavior coverage.

## Inspected implementation and assertions

The source links below open retained bytes from the assessed revision.
The current checkout remains at the comparison base.

| Criterion ID | Repository ID | Code revision | Code location | Test ID | Test revision | Assertion ID and location | Assertion contents |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC-1 | mfe-base | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | [useController.ts:58–89](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.ts.snapshot#L58-L89); [extend.ts:8–31](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/extend.ts.snapshot#L8-L31) | TEST-controlled-01 | sha256:850650239cea5037a0e51e6b72b980d0515a770ac5d05709fb1532389f17c678 | ASSERT-full-mouse-requests; [run-mfe-session-characterization-successor.cjs:152–168](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L152-L168) | Three requests occur at zero, five, and ten seconds during 150 mouse events. |
| AC-2 | mfe-base | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | [useController.ts:58–89](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.ts.snapshot#L58-L89); [extend.ts:8–31](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/extend.ts.snapshot#L8-L31) | TEST-controlled-02 | sha256:850650239cea5037a0e51e6b72b980d0515a770ac5d05709fb1532389f17c678 | ASSERT-full-keyboard-requests; [run-mfe-session-characterization-successor.cjs:152–168](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L152-L168) | Three requests occur at zero, five, and ten seconds during 150 keyboard events. |
| AC-3 | mfe-base | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | [useController.ts:58–89](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.ts.snapshot#L58-L89); [extend.ts:8–31](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/extend.ts.snapshot#L8-L31) | TEST-controlled-03 | sha256:850650239cea5037a0e51e6b72b980d0515a770ac5d05709fb1532389f17c678 | ASSERT-full-scroll-requests; [run-mfe-session-characterization-successor.cjs:152–168](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L152-L168) | Three requests occur at zero, five, and ten seconds during 150 scroll events. |
| AC-4 | mfe-base | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | [useController.ts:58–89](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.ts.snapshot#L58-L89); [extend.ts:8–31](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/extend.ts.snapshot#L8-L31) | TEST-controlled-04 | sha256:850650239cea5037a0e51e6b72b980d0515a770ac5d05709fb1532389f17c678 | ASSERT-full-four-hour-home; [run-mfe-session-characterization-successor.cjs:170–194](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L170-L194) | Zero Home timeout signals occur during four hours of mocked token and expiry replacements. |
| AC-5 | mfe-base | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | [useController.ts:29–71](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.ts.snapshot#L29-L71); [index.ts:35–46](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/index.ts.snapshot#L35-L46) | TEST-controlled-05 | sha256:850650239cea5037a0e51e6b72b980d0515a770ac5d05709fb1532389f17c678 | ASSERT-session-renewal-pending; [run-mfe-session-characterization-successor.cjs:261–268](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L261-L268) | A present refresh string arms a timer; pending renewal produces zero closures. |
| AC-6 | mfe-base | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | [useController.ts:29–71](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.ts.snapshot#L29-L71); [index.ts:35–46](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/index.ts.snapshot#L35-L46) | TEST-controlled-06 | sha256:850650239cea5037a0e51e6b72b980d0515a770ac5d05709fb1532389f17c678 | ASSERT-session-renewal-success; [run-mfe-session-characterization-successor.cjs:261–268](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L261-L268) | Controlled success produces exactly one closure and clears the refresh-expiry timer. |
| AC-7 | mfe-base | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | [useController.ts:29–71](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.ts.snapshot#L29-L71); [index.ts:35–46](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/index.ts.snapshot#L35-L46) | TEST-controlled-07 | sha256:850650239cea5037a0e51e6b72b980d0515a770ac5d05709fb1532389f17c678 | ASSERT-session-renewal-retry; [run-mfe-session-characterization-successor.cjs:269–277](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L269-L277) | Rejection keeps the prompt open; controlled retry succeeds and clears the expiry timer. |

### Jest assertion limits

| Criteria | Inspected assertions | Setup and helper limits | Execution |
| --- | --- | --- | --- |
| AC-1 through AC-3 | [useController.session.test.tsx:36–82](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.session.test.tsx.snapshot#L36-L82) | Actual Home hook calls mocked extend; assertions count helper calls. | NOT_RUN; runner setup failed |
| AC-5 and AC-6 | [useController.test.tsx:41–95](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.test.tsx.snapshot#L41-L95) | Refresh token is absent; success checks calledWith(false), without an exact count. | NOT_RUN; runner setup failed |
| AC-7 | [useController.test.tsx:98–129](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.test.tsx.snapshot#L98-L129) | Mocked rejection, retry, and expiry logout; credential validity remains unassessed. | NOT_RUN; runner setup failed |
| AC-5 through AC-7 | [relogin.test.ts:27–57](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/relogin.test.ts.snapshot#L27-L57) | Actual relogin returns controlled transport promises; refresh-header interceptor is bypassed. | NOT_RUN; runner setup failed |

No complete four-hour SYSTEM assertion was located in the inspected suites.
The selected Robot scenario observes related post-extension content.
Its assertion does not establish successful renewal, exact closure counts, or any complete criterion.
The [readiness record](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/readiness-UAT1.json) retains the exact scenario and helper scope.

### Changed and unchanged paths

| Path | Change | Behavior or maintenance rationale | Inspected assertion limit |
| --- | --- | --- | --- |
| [useController.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.ts.snapshot) | production change | BEH-05, BEH-06, BEH-07 | Only narrower controlled predicates have matching execution. |
| [index.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/index.ts.snapshot) | production change | BEH-05, BEH-06, BEH-07 | Only narrower controlled predicates have matching execution. |
| [useController.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.ts.snapshot) | production change | BEH-01, BEH-02, BEH-03, BEH-04 | Only narrower controlled predicates have matching execution. |
| [index.tsx](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/index.tsx.snapshot) | production change | BEH-01, BEH-02, BEH-03 | Selected assertions do not mount the Home view. |
| [useController.test.tsx](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.test.tsx.snapshot) | test change | Activity, prompt, promise, or rejection preservation | Jest did not execute. |
| [index2.test.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/index2.test.ts.snapshot) | test change | Activity, prompt, promise, or rejection preservation | Jest did not execute. |
| [relogin.test.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/relogin.test.ts.snapshot) | test change | Activity, prompt, promise, or rejection preservation | Jest did not execute. |
| [index.test.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/index.test.ts.snapshot) | test change | Activity, prompt, promise, or rejection preservation | Jest did not execute. |
| [useController.session.test.tsx](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.session.test.tsx.snapshot) | test change | Activity, prompt, promise, or rejection preservation | Jest did not execute. |

Unchanged interfaces remain consequential.
The [success.request.handler.ts:17–19](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/success.request.handler.ts.snapshot#L17-L19) supplies the refresh header.
The [succes.response.handler.ts:14–29](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/succes.response.handler.ts.snapshot#L14-L29) forwards renewal responses.
The [login.ts:15–39](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/utils/login.ts.snapshot#L15-L39) applies authorization and expiry state.
The [useController.ts:111–124](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.ts.snapshot#L111-L124) rearms Home expiry timers after state changes.
The controlled harness bypasses those actual response effects.

The [extend.ts:13–18](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/extend.ts.snapshot#L13-L18) aborts the preceding request before each new eligible renewal.
The activity cadence can therefore cancel a slower pending request.
The current fixtures do not assess responses slower than five seconds.
This is an unresolved integration risk, without a demonstrated deployed defect.

## Retained execution and verification

| Criterion ID | Assertion ID | Execution ID | Exact tested revision | Actual result | Execution status | Retained evidence | Verification claim and limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC-1 | ASSERT-full-mouse-requests | EXEC-session-renewal-full-run002 | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | Narrow controlled predicate PASSED | PASSED; controlled_source_characterization | [result](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) `/checks/0` | NOT_VERIFIED; approval and SYSTEM execution are absent |
| AC-2 | ASSERT-full-keyboard-requests | EXEC-session-renewal-full-run002 | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | Narrow controlled predicate PASSED | PASSED; controlled_source_characterization | [result](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) `/checks/1` | NOT_VERIFIED; approval and SYSTEM execution are absent |
| AC-3 | ASSERT-full-scroll-requests | EXEC-session-renewal-full-run002 | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | Narrow controlled predicate PASSED | PASSED; controlled_source_characterization | [result](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) `/checks/2` | NOT_VERIFIED; approval and SYSTEM execution are absent |
| AC-4 | ASSERT-full-four-hour-home | EXEC-session-renewal-full-run002 | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | Narrow controlled predicate PASSED | PASSED; controlled_source_characterization | [result](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) `/checks/3` | NOT_VERIFIED; approval and SYSTEM execution are absent |
| AC-5 | ASSERT-session-renewal-pending | EXEC-session-renewal-full-run002 | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | Narrow controlled predicate PASSED | PASSED; controlled_source_characterization | [result](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) `/checks/13` | NOT_VERIFIED; approval and SYSTEM execution are absent |
| AC-6 | ASSERT-session-renewal-success | EXEC-session-renewal-full-run002 | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | Narrow controlled predicate PASSED | PASSED; controlled_source_characterization | [result](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) `/checks/13` | NOT_VERIFIED; approval and SYSTEM execution are absent |
| AC-7 | ASSERT-session-renewal-retry | EXEC-session-renewal-full-run002 | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | Narrow controlled predicate PASSED | PASSED; controlled_source_characterization | [result](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) `/checks/14` | NOT_VERIFIED; approval and SYSTEM execution are absent |

The [successor result](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) reports sixteen passing controlled check groups.
The [original binding](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/original-binding.json) records source, harness, runtime, input, and configuration bytes before execution.
The [completion record](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/completion.json) binds retained output and the zero exit status.
Five executed source hashes match the selected Git commit.
The [independent peer review](../../knowledge/raw/execution/session-renewal-full-2026-10-19/review/peer-review.json) checked 28 integrity conditions and all sixteen assertion groups.
These checks support the recorded narrow predicates.

The short fixtures now match the three requested event types, cadence, and duration.
They assert request counts, without successful backend renewal.
The four-hour fixture manually replaces token and expiry after each request.
Its zero Home timeout count depends on those replacements.
Fresh SSO prompts, real token updates, and external maximum-session policy remain unassessed.
A finite fixture cannot prove indefinite renewal.

The prompt fixture now provides a refresh string and mocked expiry.
It checks zero pending closures and exactly one closure after controlled success.
The credential is not validated or sent through the actual refresh-header interceptor.
Pending renewal does not cross the refresh-expiry deadline.
Real credential usability and deadline precedence remain unresolved.

Earlier evidence remains historical.
The [older committed result](../../knowledge/raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json) retains twelve narrower passing checks.
Its pending and success fixtures omit refreshToken.
Its result omits original harness, configuration, and input hashes.
The successor improves future evidence without repairing those historical bindings.
The [historical fixture](../../knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs#L211-L216) remains unchanged.

### UAT1 readiness

The [UAT1 assessment](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/readiness-UAT1.json) records zero live scenarios and zero external requests.
Browser wrapper dependencies remain unavailable.
Private UAT1 bindings remain unconfirmed.
The deployed UAT1 relationship to the pilot revision remains unknown.
No human requirement reviewer is recorded.
The proposed workspace has no granted operations.

The [configuration check](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/proposed-UAT1-after-fix-verification.json) confirms local workspace loading after the timeout correction.
Its denied list operation reflects the empty grant set.
Configuration readiness does not establish business execution.
The [runbook](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/UAT1_RUNBOOK.md) records the remaining local setup actions.

### Coverage denominators

| Metric | Numerator | Denominator | Scope and evidence limit |
| --- | --- | --- | --- |
| Included criteria assessed | 7 | 7 | Each criterion has inspected evidence or an explicit gap. |
| Local direct implementation links | 6 | 7 | Partial frontend paths only; AC-4 global policy remains unresolved. |
| Required SYSTEM assertion coverage | 0 | 7 | Complete system predicates have no inspected matching assertion chain. |
| Meaningful production changes explained | 4 | 4 | Four changed production files link to scoped behavior rationale. |
| Changed production paths reached by selected assertions | 3 | 4 | Home view wiring is not mounted by selected assertion chains. |
| Controlled check groups passed | 16 | 16 | These groups contain multiple narrower predicates. |
| Approved SYSTEM behavior execution | 0 | 7 | Approval and UAT1 business execution remain absent. |

The machine baseline also maps the conditional AC-4 timer path.
Its seven source mappings include that partial path.
The direct local implementation count excludes the complete global AC-4 criterion.

The active behavior inventory contains seven criteria.
The controlled inventory contains sixteen named check groups.
Repository-wide test-case denominators remain unknown; test-to-story and test-to-code percentages are N/A.
Counts do not collapse intent, assertions, execution, or review into one verdict.

## Coverage gaps

| Missing link | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| GAP-full-human-review | All seven criteria remain candidate intent with no recorded human review. [REQ-active-session-renewal.md](../../knowledge/candidates/requirements/REQ-active-session-renewal.md) | No criterion can support approved behavior verification. | unknown | Obtain recorded human review without inventing a reviewer or approval. |
| GAP-full-fixture-authority | Raw intent names indefinite renewal, activity types, and refresh retention; detailed test thresholds are derived. [session-renewal-intent-2026-10-15.txt](../../knowledge/raw/session-renewal-intent-2026-10-15.txt); [session-activity-and-idle-intent-2026-10-15.txt](../../knowledge/raw/session-activity-and-idle-intent-2026-10-15.txt); [REQ-active-session-renewal.md](../../knowledge/candidates/requirements/REQ-active-session-renewal.md) | The 100-millisecond, 15-second, 30-second, and four-hour fixtures need review. | unknown | Confirm these fixture thresholds and the meaning of successful renewal with the requirement owner. |
| GAP-full-request-not-renewal | Exact cadence now executes; requests still lack successful-renewal assertions. [Successor assertions](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L152-L168); [result](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) | Complete AC-1 through AC-3 remain unsupported. | unknown | Assert successful service renewal and updated session state for each exact event fixture. |
| GAP-full-four-hour | Four controlled hours now execute with manual session replacements. [Successor assertion](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L170-L194); [result](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) | Fresh SSO counts and complete AC-4 remain unsupported. | unknown | Execute a four-hour browser/backend scenario and inspect policy cutoffs across provider boundaries. |
| GAP-full-usable-refresh | Successor fixtures provide a refresh string with mocked expiry. [Successor assertions](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L261-L268); [result](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) | Real credential usability and backend acceptance remain unsupported. | unknown | Use valid refresh credentials and inspect actual interceptor and backend renewal behavior. |
| GAP-full-exact-close-count | Jest checks calledWith(false); only the controlled harness checks the exact [false] list. [useController.test.tsx](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.test.tsx.snapshot); [run-mfe-session-pilot-characterization.cjs](../../knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs) | The Jest assertion permits duplicate closure calls and lacks a usable refresh credential. | unknown | Assert exactly one successful closure with valid refresh credentials and retained matching execution. |
| GAP-full-expiry-race | The refresh-expiry logout timer remains active while renewal is pending or rejected. [useController.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.ts.snapshot) | Close-transition interpretation and late renewal after logout remain unresolved. | unknown | Define deadline precedence and inspect pending, logout, and late-response integration assertions. |
| GAP-full-harness-binding | Successor original bindings are complete; older omissions remain historical. [mfe-session-pilot-characterization-committed-result.json](../../knowledge/raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json); [run-mfe-session-pilot-characterization.cjs](../../knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs) | Historical result limits cannot be removed by successor metadata. | unknown | Preserve historical results and include complete input bindings in future results. |
| GAP-full-jest-execution | The inspected local Jest attempt failed before assertions ran. [Runner diagnostic](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/mfe-jest-local-attempt.stderr.txt); [readiness](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/readiness.json) | Jest predicates have no retained matching runner result. | unknown | Run applicable Jest suites in a prepared environment and retain exact code and test hashes. |
| GAP-full-browser-backend | UAT1 has zero scenarios and unresolved environment inputs. [UAT1 readiness](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/readiness-UAT1.json); [config.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/config.ts.snapshot); [success.request.handler.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/success.request.handler.ts.snapshot); [succes.response.handler.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/succes.response.handler.ts.snapshot) | No criterion has required SYSTEM execution evidence. | unknown | Run authorized supported-environment scenarios and retain environment, source, assertions, and results. |
| GAP-full-global-policy | The inspected local activity path has no elapsed-session maximum; downstream policy remains outside this assessment. [useController.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.ts.snapshot); [extend.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/extend.ts.snapshot) | Local inspection cannot establish indefinite renewal or absence of external reauthentication limits. | unknown | Inspect exact BFF and provider policy revisions and connect their bounded execution evidence. |
| GAP-full-slow-renewal | Each accepted activity renewal aborts the preceding extend request; selected network fixtures resolve immediately. [useController.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.ts.snapshot); [extend.ts](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/extend.ts.snapshot) | Slow-response cancellation under continuous activity remains unassessed. | unknown | Inspect integration assertions with renewal responses slower than the five-second activity cadence. |
| GAP-full-view-wiring | The Home view removes its root mouse handler; selected hook assertions do not mount Home. [index.tsx](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/index.tsx.snapshot); [useController.session.test.tsx](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.session.test.tsx.snapshot) | Changed view wiring lacks a direct inspected applicable assertion chain in this selected inventory. | unknown | Retain a mounted portal integration assertion for document activity and teardown. |

## Facts, inferences, and unresolved questions

- Facts: Seven criteria remain candidate intent with no recorded human approval.
- Facts: Sixteen controlled check groups passed with original pre-run bindings.
- Facts: UAT1 business execution and applicable Jest assertion execution remain absent.
- Inferences: Local frontend changes support the requested direction within the inspected source limits.
- Inferences: Mocked four-hour state progression cannot establish external session policy.
- Unresolved questions: Which response proves successful renewal and a usable replacement session?
- Unresolved questions: Which refresh-expiry, pending-renewal, and late-response deadline takes precedence?
- Unresolved questions: Which deployed UAT1 code and provider policies apply?
- Unresolved questions: Who owns requirement approval, fixture provisioning, and SYSTEM execution?

## Findings

The [governance finding](../../knowledge/findings/GF-session-renewal-verification-gates.md) records the publication and execution gates.
It remains a candidate with unknown owner and pending review.

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Candidate requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md) and [UAT1 readiness](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/readiness-UAT1.json) | All seven complete behaviors remain NOT_VERIFIED. | unknown | Record actual human review and retain matching SYSTEM execution. |
| [run-mfe-session-characterization-successor.cjs:152–194](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L152-L194) | Request counts and mocked state cannot prove successful renewal or fresh SSO outcomes. | unknown | Assert those outcomes in the supported UAT1 environment. |
| [run-mfe-session-characterization-successor.cjs:261–283](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs#L261-L283) and [useController.ts:29–55](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.ts.snapshot#L29-L55) | Valid credentials and pending-expiry races remain unassessed. | unknown | Define deadline precedence and test real renewal, rejection, and retry. |
| [extend.ts:13–18](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/extend.ts.snapshot#L13-L18) and [useController.ts:67–75](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.ts.snapshot#L67-L75) | Slow requests can encounter repeated cancellation. | unknown | Assess responses slower than five seconds under continuous activity. |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-code-645c0e995147ba2cee0d | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | cca50a13a8bd05705127e8d25c74db57014be04068ffff59b5a7c3bd5779a272 | unknown; implementation evidence; no target-intent approval |
| SRC-code-d65c9ceae12b3c7c5496 | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/index.tsx.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/index.tsx.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 57c466a4ff3421050ba917ce98c927ba19c5193051cb94483c9b2ed43227dbf2 | unknown; implementation evidence; no target-intent approval |
| SRC-code-052150dd1cefc2cc9f1b | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/index.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/index.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 72182d3bb36584e00982377e0137dd6effb527a4c2a24a8ffd89fcaf44b6cf13 | unknown; implementation evidence; no target-intent approval |
| SRC-session-full-acc2dd6a51d2f306a5 | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/extend.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/extend.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 1643dbd7f4a124797b77bd89fdd8b965a7b5b0c1c13ee0c0a001b1362229a6ad | unknown; implementation evidence; no target-intent approval |
| SRC-session-full-b9f4261dcc13e38e2f | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/config.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/config.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | f3856b594a5930ee9f66e28e91e4a345873850f501b8768315a8e7c9ae889266 | unknown; implementation evidence; no target-intent approval |
| SRC-session-full-6902a1d561fe21f9e6 | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/getEndpoint.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/getEndpoint.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 4fad93acd98fcd34e3ed5bc3f0d1bdfb5a59d8dd1c7a9e7f62354a702e47c102 | unknown; implementation evidence; no target-intent approval |
| SRC-session-full-f83323ef41dfc619d2 | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/success.request.handler.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/success.request.handler.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 4b85639d4bf4c0b588b9c9a774a105ef74c11ea2b109092425b4a85ca87195cd | unknown; implementation evidence; no target-intent approval |
| SRC-session-full-2290ace0c9e92b110c | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/succes.response.handler.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/succes.response.handler.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 7917609f4cb9f0ef995d7846a910c91430972bb16e96f5320f5b55ed4362ba31 | unknown; implementation evidence; no target-intent approval |
| SRC-session-full-1bab517aa2e170a86c | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/error.response.handler.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/error.response.handler.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | b4e357384ccdbd33bb6ba721ba7d9bb93806c2fac55c4c6ee17df13740d92c60 | unknown; implementation evidence; no target-intent approval |
| SRC-session-full-10c2392b84c2c0f88a | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/utils/login.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/utils/login.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | e95c437c5cadb7ebb2ca450c6f2df85bcf3f60194d9ef54095fdbf7934eaa7de | unknown; implementation evidence; no target-intent approval |
| SRC-code-e9cbeed1e6e9e41eefa0 | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 9c9fed8b70bb8a5913210663a11974928d167b4e8676bf413483f3101db2c2b1 | unknown; implementation evidence; no target-intent approval |
| SRC-session-full-608fb379c40b7cb19b | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/index.tsx.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/index.tsx.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | e1b53e638523ae42786277503581c96fe197e54218a04c48dbc312badb0356c2 | unknown; implementation evidence; no target-intent approval |
| SRC-code-dbc48032baf3fe2e687f | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.session.test.tsx.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.session.test.tsx.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 6e17c8889f61770d4b0f261401fbd43f1559617731a8c038d0b08da6c67698a3 | unknown; implementation evidence; no target-intent approval |
| SRC-code-9ca360db38625ec7f8d1 | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.test.tsx.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.test.tsx.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | b6f04007994e2a77f1952cb7a4829f57bb5e7e6818ca40d03b4f6f21940dae79 | unknown; implementation evidence; no target-intent approval |
| SRC-code-d6656ad1dc43f11a4d0a | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/relogin.test.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/relogin.test.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 1dc0069cbac221d31af28e8ba93d34b7a46eec2876c151e5c6aba7f1cfeb52fc | unknown; implementation evidence; no target-intent approval |
| SRC-code-ac741ec06de6d9cc26fb | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/index2.test.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/index2.test.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 333d8532093c1f2d1cf39d1b8150b8e17c848de8b33c603416898126b961a8a6 | unknown; implementation evidence; no target-intent approval |
| SRC-code-f6720f5ae727d7968570 | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/index.test.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/index.test.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 0f237be9785558d5f809734b2746d3f2a4276e70ba210fcd4f1a1c5359e3c8b6 | unknown; implementation evidence; no target-intent approval |
| SRC-session-full-b726205cfd5ceb09da | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/success.request.handler.test.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/success.request.handler.test.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | c922c2e46c202a6ee4a0a2e32588133e70796dd22fbd11fe36ea8b3a13778d4b | unknown; implementation evidence; no target-intent approval |
| SRC-session-full-e9a414ff0c0afa3ea7 | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/succes.response.handler.test.ts.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/util/succes.response.handler.test.ts.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | e4b48fd64084db48e20221ae6fa4c48fee9df9b2deeb3cc9ac1202673dab0823 | unknown; implementation evidence; no target-intent approval |
| SRC-session-full-20c15aae57ba259cb6 | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/index.test.tsx.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/index.test.tsx.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 648678759f7c82ec40be5deb7cbc97cf28b158266c47aca9275c039610badb62 | unknown; implementation evidence; no target-intent approval |
| SRC-session-full-df34c8e2538a85e2d6 | [knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/index0.test.tsx.snapshot](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/index0.test.tsx.snapshot) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | a29c31ed67654a7ac08445220ee111e72a815f0fc0552296beb4da32b9b0c8a6 | unknown; implementation evidence; no target-intent approval |
| REQ-active-session-renewal-v2 | [knowledge/candidates/requirements/REQ-active-session-renewal.md](../../knowledge/candidates/requirements/REQ-active-session-renewal.md) | document-version:2 | 572528b0a218e20e8ccbbbf4c07a9efc2be4a66302520b957ea0b80a0fbcb4d3 | unknown; candidate evidence; human approval remains pending |
| SRC-session-renewal-intent-2026-10-15 | [knowledge/raw/session-renewal-intent-2026-10-15.txt](../../knowledge/raw/session-renewal-intent-2026-10-15.txt) | request-2026-10-15 | d3976f80aaeba02b2397d9731a142767225d2a3ee6dcd1a2de351d3d748217e9 | unknown; candidate evidence; human approval remains pending |
| SRC-session-activity-and-idle-intent | [knowledge/raw/session-activity-and-idle-intent-2026-10-15.txt](../../knowledge/raw/session-activity-and-idle-intent-2026-10-15.txt) | reply-2026-10-15 | a9654884d2ff9f2f27a3185268b251694b51145d50aa7bee6ab2d75c911e90e3 | unknown; candidate evidence; human approval remains pending |
| SRC-pilot-ac4eca4f02906add | [knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs](../../knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | c7c84a92ca652ca5e70d704fe357662dd944a2521ff8cbf823568d6b9a23dc4d | unknown; candidate evidence; human approval remains pending |
| SRC-auth-stage-e0f59ba3eabb5a6d | [knowledge/raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json](../../knowledge/raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 8ffc1eb5ebf798c9eb2793447127e852eb7dd7c2dc73749482a35311d3649fe8 | unknown; candidate evidence; human approval remains pending |
| TRACE-active-session-renewal-pilot | [docs/reviews/SESSION_RENEWAL_BEHAVIOR_TRACE.md](SESSION_RENEWAL_BEHAVIOR_TRACE.md) | retained bytes inspected 2026-10-19 | 124c7e2ff420ff7e4daa52e2e4439f179cd7ca659d3c0641f17a72a073170b8b | unknown; candidate evidence; human approval remains pending |
| SRC-session-full-c9a0c0bc463646adea | [knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-mfe-session-characterization-successor.cjs) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 850650239cea5037a0e51e6b72b980d0515a770ac5d05709fb1532389f17c678 | unknown; retained agent evidence; no human approval or business execution |
| SRC-session-full-ec3bcb4fe044c2b358 | [knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | f2c7d1008b1ef07522fffe3b7e1b37dbb13b6d377203b97ef8504a0c90edde87 | unknown; retained agent evidence; no human approval or business execution |
| SRC-session-full-696efe136b6c21b704 | [knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/original-binding.json](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/original-binding.json) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 83027b10c6154e10e442c0ddea6e1199a8345cf07f01b45cb554ebc1c3a0d0b7 | unknown; retained agent evidence; no human approval or business execution |
| SRC-session-full-5b0bc86b2846c8526a | [knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/completion.json](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/completion.json) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | e136d7d1db4d262518ced5b813588ac13e48d579bbdd94dcb21703ed2a1f8d61 | unknown; retained agent evidence; no human approval or business execution |
| SRC-session-full-768db71747b1743a77 | [knowledge/raw/execution/session-renewal-full-2026-10-19/review/peer-review.json](../../knowledge/raw/execution/session-renewal-full-2026-10-19/review/peer-review.json) | review-2026-10-19 | aaca5194803ed4e0eb345c61724a6bf0a55e60f79d9ee53bae1fccd24ccc9939 | unknown; retained agent evidence; no human approval or business execution |
| SRC-session-uat1-9f4cb9a32667ba115 | [knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/readiness-UAT1.json](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/readiness-UAT1.json) | review-2026-10-19 | 71e798fc4e298ca8dd2918b2496da75fd1cade79f60adc19a9f5975198805b3c | unknown; retained agent evidence; no human approval or business execution |
| SRC-session-full-c5406c8857e574ac1f | [knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/fixture-inputs.json](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/fixture-inputs.json) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | c8303cae9ff9df32269add34ab911708359710710ab43508f47fedb0c33dfe5f | unknown; retained agent evidence; no human approval or business execution |
| SRC-session-full-e3cb257f3c7d61fe41 | [knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/execution-config.json](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/execution-config.json) | 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8 | 1c5ec6b7e0e77dfa2e2e08063f0e6d5e357283d08d84db9eec9d672186fe5011 | unknown; retained agent evidence; no human approval or business execution |
| SRC-session-full-a44c8fd515c698ff5f | [knowledge/raw/execution/session-renewal-full-2026-10-19/retention-map.json](../../knowledge/raw/execution/session-renewal-full-2026-10-19/retention-map.json) | review-2026-10-19 | 38514a38801595b2e6ccbe2f3df113127bfdbe4a4255f350aabbbb3103b7a039 | unknown; retained agent evidence; no human approval or business execution |
| SRC-session-uat1-7579996c1b999b053 | [knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/proposed-UAT1-after-fix-verification.json](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/proposed-UAT1-after-fix-verification.json) | review-2026-10-19 | e5946c230ffa985e898f15c1da5b5d6c277d0044a6f0ee24853bf81b57a75dd6 | unknown; retained agent evidence; no human approval or business execution |
| SRC-session-uat1-5657b151404cb805c | [knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/UAT1_RUNBOOK.md](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/UAT1_RUNBOOK.md) | review-2026-10-19 | 6ff5f68b68e8abc9905551db12e8ca0e2988261036345e145be8dbdf352270a0 | unknown; retained agent evidence; no human approval or business execution |

The retained relocation map preserves original execution paths and snapshot destinations.
Original paths inside immutable results remain unchanged.
Automated source, locator, and authoring checks support review.
The complete ASD writing review remains pending.
