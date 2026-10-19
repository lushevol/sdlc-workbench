---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Portal defect: key evidence

## Necessary: start here

- [Issue intake](../intake.md): current understanding, user answers, open decisions, and proposed acceptance criteria.
- This index: useful evidence only. [The earlier task manifest](manifest.json) records the previous cleanup and deletion history.

## Important: evidence for current claims

| Evidence ID | Claim or question | Locator | Revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |
| C-003 | What happened locally? | [Run 001 events](portal/run-001/browser/browser-events-001.json), [BFF log](portal/run-001/bff/local-bff-runtime.stdout.log) | 19 October 2026 UTC; exact revisions in intake | Manifest | Freeze, late issuance, missing-refresh logout, then HTTP 401 and authentication clear. |
| C-004 | Is there another observation? | [Run 002 events](portal/run-002/browser/browser-events-001.json), [return text](portal/run-002/browser/return.ax.full.txt) | Separate local run; 19 October 2026 | Manifest | Another background run. No matching foreground control. |
| C-005 | Can the setup and observer be checked? | [Setup retention map](portal/retention-map.json), [instrumentation manifest](portal/setup/instrumented-mfe/instrumentation-manifest.json), [observer review](portal/run-001/reviews/observer-review.json) | Exact retained source and setup bytes | Manifest | Local substitutions and observer effects remain explicit. Historical paths resolve through the relocation map. |
| C-006 | Which code explains the failure? | [Source snapshots](source-snapshots), [source receipt](source-inspection.json) | MFE `f025513f`; BFF `85d7cc03`; full commits in intake | Manifest and raw source manifest | Exact source supports the local mechanism. It does not establish PROD deployment. |
| C-007 | What do existing tests cover? | [Assertion receipt](source-inspection.json), [test-engine inspection](browser-setup/test-engine-inspection.json) | Exact assertion revisions recorded in each receipt | Manifest | Inspection found coverage gaps. No new business test ran. |
| C-014 | Was the supplied patch applied? | [Application receipt](patch-application-20261020.json), [validation](patch-application-validation-20261020.json) | 20 October 2026; base revision and patch hash in receipt | Receipt | Local patch fidelity passed. Dependencies prevent test and type-check execution. |
| C-013 | How do credential paths differ? | [Expired-token fixture result](portal/run-001/expired-fixture/expired-result.json) | Separate controlled fixture on port 8089 | Manifest | Access-based refresh fails; valid-refresh relogin succeeds. No natural browser recovery assertion. |

[Verification detail](../verification.md) supplies assertion boundaries and execution limits.
Stable source IDs, revisions, and hashes remain in the [raw source manifest](../../../evidence/knowledge/manifest.yaml).
[Existing session intent](../../../knowledge/candidates/requirements/REQ-active-session-renewal.md) remains candidate knowledge with pending publication review.

## Important: authentication investigation

- [Runtime baseline](authentication/ARCH-authentication-runtime-baseline.md): earlier source and assertion investigation, with its original evidence limits.
- [Verification findings](../../../evidence/knowledge/findings/GF-session-renewal-verification-gates.md): unresolved execution and policy boundaries.
- [Migration map](../../../evidence/knowledge/migration-20261020/cleanup.json): current locators, retained hashes, removed paths, and recovery revisions.

The map resolves historical source paths inside unchanged evidence.
Task captures remain evidence. They do not establish approved domain rules or corrected behavior.

## Important: retained screenshots

- [Edge browser smoke](browser-final/edge/returned.png): synthetic interaction and two-second visibility check, after returning to the fixture.
- [Result](browser-final/edge/result.json), [snapshot](browser-final/edge/snapshot.yaml), [trace](browser-final/edge/trace.zip), and [hashes](browser-final/edge/manifest.json) preserve its execution context.
- [Portal Sign In](portal/run-001/reviews/sign-in-context.jpg): actual local portal context. Capture time and phase remain unresolved.

Neither image establishes portal unit-test execution. No attributed screenshot proves the thirty-minute returned-page result.

## Important: provenance and earlier checks

- [Historical relocation map](organization-20261020/relocation-map.json), [prior source manifest](organization-20261020/manifest-before.yaml), and [authorization](organization-20261020/request.txt): preserved unchanged.
- [Earlier document checks](defect-document-checks-20261020.json): checks before the domain-only knowledge migration.
- [Earlier task manifest](manifest.json): Necessary and Important file inventory before the domain-only knowledge migration.

## Unimportant: removed from the task

Removed material includes duplicate browser trials, unrelated harness logs, superseded reports, and repeated authoring or organization checks.
The earlier task cleanup kept 74 of 252 files and removed 178 files. It preserved registered snapshots and audit history.
The historical relocation map describes its original migration. Use the current manifest to resolve later deletions through Git.
The earlier cleanup changed no business policy or portal runtime.
C-014 records the later, explicitly requested local patch application.
