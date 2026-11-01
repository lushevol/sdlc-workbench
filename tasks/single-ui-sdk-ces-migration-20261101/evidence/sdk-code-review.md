---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Independent SDK implementation review

> **Run the corrected suite before accepting the implementation.**
> Action: execute every applicable case after both review corrections.
> Consequence: corrected source and assertions have no passing execution from this reviewer.
> Owner: Codex. Evidence: [sample assertion](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/entity/CesRoleSampleTest.java:62).

## Findings

### SDK-REV-001: [P2] Assert the complete action list from the retained sample

Trigger: execute `CesRoleSampleTest.mapsActualRetainedRoleShape` against its unchanged JSON fixture.
The test expects only `ACCESS_FMO_POST_TRADE_PORTAL` for `RATAN_TRADE_BLOTTER`.
The fixture contains four actions for that role and feature.
They are `ACCESS_FMO_POST_TRADE_PORTAL`, `F_Custom_Query_Builder`, `F_Custom_View_Builder_Private`, and `F_Export_Data`.
The mapper preserves every action in source order.
Evidence: [assertion](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/entity/CesRoleSampleTest.java:62) and [append operation](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:202).

Intended result: preserve the fixture's complete action list.
Old result: not applicable; the baseline has no retained-sample test or CES mapper.
Candidate result: source predicts assertion failure because four actions differ from one.
Classification: introduced test-expectation defect. No deployed application failure is established.
Owner: Codex. Next action: correct the expected list from the retained bytes.
Validation: root coordinates Maven. This reviewer has not executed this Java test.
Confidence: HIGH from direct JSON and source inspection.
Resolution: corrected in source by the implementation owner. The expected list now matches all four retained actions.
Affected Java execution remains pending in root coordination.

### SDK-REV-002: [P2] Filter unrelated role scopes before inspecting their grant lists

Trigger: a CES response includes a valid selected role and an unrelated application role without a grant list.
Before correction, `mapRoles` rejected every row's grant list before application selection.
The explicit call threw `INVALID_RESPONSE`. The legacy call consequently returned no grants.
The unrelated row could therefore remove the selected role's valid permissions.
Evidence: initial implementation hash `575925b259d7f2bce2faa86c4262e95990d8075b0546c59a99ab69a8979581c3` in [initial context](sdk-review-context.json).

1. Configure one selected application and legacy entity.
2. Return its valid role beside another application's role with missing or null `featureActionDtos`.
3. Request the selected user's permissions.

Intended result: retain exactly the selected role's grants.
Old transport: the baseline requested grants only after its entity filter. Equivalent CES execution is unavailable.
Candidate before correction: source predicts total failure from the unrelated missing grant list.
Candidate after correction: application and entity selection precede selected role validation.
The role allowlist also precedes grant-list validation.
Rows without routing identities still fail because their scope cannot be established.
Classification: introduced migration isolation defect, corrected before completion.
No production incidence, forced logout, or session disruption is established. Priority remains P2.

Owner: Codex. Next action: run the three added regressions through the complete suite.
Resolution: corrected under root's explicit implementation instruction.
Evidence: [routing guard](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:166) and [selected grant guard](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:181).
Assertions: [unselected application lists](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:257), [excluded roles](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:272), and [missing routing identity](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:284).
Canonical definitions: [SDK-TC-002](../06-test-cases.md#sdk-tc-002) and [SDK-TC-004](../06-test-cases.md#sdk-tc-004).
Confidence: HIGH for source control flow. Java regression execution remains pending with root.

## Comparison identity

| Field | Value |
| --- | --- |
| Repository | `single-ui-auth-sdk`; `/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter`. |
| Mode | Worktree against exact current baseline. |
| Baseline | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`. |
| Candidate | Uncommitted worktree, including untracked implementation and tests. |
| Initial fingerprint | `41513fd7ed85bd516e230197aad3d21141249d213f18fd9ae4036971ee8b5ddd`. |
| Corrected fingerprint | `ad63c068f463a1481c044653b0c38fcb07781980585d4b0ffda1ed489c3ac530`. |
| Corrected tracked diff SHA-256 | `a5f8d67e034b686d9e95e876810ab0c4ff9d71511e5393c35ea6c06f97e823c1`. Untracked source hashes remain in the context. |
| Source context | [initial context](sdk-review-context.json) and [corrected context](sdk-review-final-context.json). |
| Pattern scan | [scan result](sdk-review-scan.json). |
| Intent | [implementation clarification](user-clarification-implementation.md). |
| Stage | [current change review](../10-change-review.md). |

## Review scope and limits

Inspection covers old and new lookup flow, DTOs, properties, URI construction, bearer headers, role and feature filtering, and alias collisions.
Inspection also covers Spring wiring, retained constructors, additive interface behavior, POM changes, fixtures, and JWT/filter assertions.
The pattern scanner's credential candidate is a literal synthetic test token, not a retained live credential.
No Maven, Java test, live CES call, or deployed consumer check was executed by this reviewer.
Source predictions do not establish production reachability or frequency.
Root owns execution and reconciliation of subsequent edits.

## Validation evidence

| Check | Result | Evidence and limit |
| --- | --- | --- |
| Review context collection | Completed. | Exact selected-file hashes and fingerprint retained. |
| Pattern scan | One candidate; dismissed after inspection. | Synthetic token in `AuthorizationImplTest` only. |
| Retained sample action extraction | Completed. | Python JSON parsing established the four fixture strings above. |
| Java suite | NOT_RUN by reviewer. | Root coordinates the build. |

## Review conclusion

Both actionable findings have source corrections and meaningful assertions.
No additional actionable defect was found within the inspected scope.
The corrected context records every selected path's content hash.
Root must reconcile any later source changes and retain complete test execution evidence.
This review does not establish live CES support, production permission parity, or deployment approval.
