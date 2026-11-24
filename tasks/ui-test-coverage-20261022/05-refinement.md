---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# UI case refinement

> **Critical conclusions: UI bindings remain blocked**
>
> **28 cases lack verified UI action targets.**
> Action: Resolve the [listed bindings](#unresolved-ui-bindings). Consequence: These cases fail the mandatory UI gate.
> Owner: unknown. Evidence: [final quality results](evidence/refinement/quality-results.json).
>
> **All 521 cases remain NOT_RUN and lack reviewed automation bindings.**
> Action: Bind fixtures and executable assertions before execution handoff. Consequence: Business verification remains unsupported.
> Owner: unknown. Evidence: [component and step manifest](evidence/refinement/gherkin-manifest.json).

The [catalog](test-cases.md) remains the single case definition source.
The [inventory](evidence/case-inventory.json) records current versions, findings, and execution states.
The [checkpoint](evidence/refinement/progress.json) records completion of all 521 definition refinements.
All 1,596 assertions remain in the canonical catalog.
Case metadata retains review gaps, cleanup, and evidence limits.

## Request and scope

The user requested refinement of every generated UI case against the new Gherkin principles.
The scope preserves all 521 original IDs across 46 groups.
The original intake remains the historical task agreement.
This successor stage changes definitions and supporting mappings.
No browser execution or business source change occurred.

## Baseline and affected scope

The baseline is Git revision `ab0af23`, with catalog definition version 1.
The [baseline audit](evidence/refinement/baseline-quality.json) preserves its checker findings.
Its catalog SHA-256 is `73678b9a3483a1a1dd04da6ec7f43aff949de49058f09d0b6c2babf850960cfb`.
Git preserves those original definitions.
The [source manifest](evidence/source-manifest.json) identifies exact MFE, BFF, and draft knowledge fingerprints.

Changes affect case definitions, component inventories, step evidence, checker vocabulary, and handoff guidance.
The qualitative risk is moderate because invented identities can invalidate a UI procedure.
Exact source inspection replaced unsupported control names and roles.
Unknown tenant controls remain explicit gaps.

## Completed implementation

| Stage | Result | Evidence |
| --- | --- | --- |
| Preserve coverage | Retained 144 AUTH, 156 UI, 52 KNOW, 72 UX, and 97 BFF cases. | [Case inventory](evidence/case-inventory.json) |
| Separate intent | Added implementation-independent intent to every case. | [Canonical definitions](test-cases.md#coverage-navigation) |
| Refine procedures | Added source-backed component types, quoted identities, scopes, fixture data, and ordered actions. | [Component and step manifest](evidence/refinement/gherkin-manifest.json) |
| Refine assertions | Separated UI state, request observations, and persisted readback. | [Case review metadata](evidence/refinement/case-reviews.jsonl) |
| Preserve checkpoints | Saved each completed case immediately, then reconciled current metadata. | [Progress](evidence/refinement/progress.json) and [authoring cleanup](evidence/refinement/authoring-cleanup.json) |
| Correct checker defects | Supported actual components, explicit action verbs, state wording, and repeated action/assertion groups. | [Runtime validation](evidence/refinement/validation-results.json) |
| Audit quality | Mapped every case and step, then retained unresolved failures separately. | [Final quality results](evidence/refinement/quality-results.json) |

Important corrections include the expiration dialog title, Extend button, and SSO link semantics.
Input placeholders identify login fields; wrapper test IDs do not identify their descendant inputs.
Administration actions use actual row labels and dynamic dialog titles.
Header Close uses a Chip; footer Close uses a button.
Dialog closure does not establish authentication recovery or successful persistence.

The checker now preserves intermediate observations between ordered actions.
It still rejects conditions after actions and an action sequence without a final assertion.
The [writing rules](../../.agents/skills/gherkin-quality/references/writing-rules.md) document the source-backed component vocabulary.
The [command guide](../../docs/GHERKIN_QUALITY.md#deterministic-coverage-and-limits) documents supported ordering and limits.

## Quality results

| Result | Cases | Meaning |
| --- | --- | --- |
| FAIL | 28 | A required UI action target lacks sufficient type, identity, or scope evidence. |
| UNVERIFIED | 493 | Definition checks identify unresolved evidence, expectation authority, reviews, or executable bindings. |
| PASS | 0 | No case claims complete semantic review or automation readiness. |
| NOT_RUN | 521 | No matching browser execution is retained. |

The final gate returns exit code 1 because mandatory target information remains missing.
All known component mappings pass literal type, identity, and scope checks.
These checks do not establish rendered uniqueness or expectation meaning.
Some supporting ranges cover complete source files; their semantic support remains unverified.
The [manifest build receipt](evidence/refinement/manifest-build.json) confirms complete case and step reconciliation.

The authority split remains 336 implementation characterizations, 23 documented drafts, and 162 proposals.
An implementation observation does not establish approved business intent.
Proposed accessibility, compatibility, security, and layout expectations still require owner review.
The catalog does not claim coverage of every possible combination.

## Unresolved UI bindings

Each listed case retains its intended business interaction.
Its available sources do not identify a complete executable UI target.
The required action is to inspect the actual tenant or admin screen and record a unique control.
The consequence is blocked UI procedure acceptance and automation binding.
The owner is unknown for every row.

| Case and exact affected steps | Missing information | Owner and next action |
| --- | --- | --- |
| [AUTH-144](test-cases.md#auth-144): [step 5372](test-cases.md#L5372) | Verified identity, scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-015](test-cases.md#know-015): [step 10800](test-cases.md#L10800) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-017](test-cases.md#know-017): [step 10835](test-cases.md#L10835) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-011](test-cases.md#know-011): [step 10950](test-cases.md#L10950) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-012](test-cases.md#know-012): [step 10987](test-cases.md#L10987) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-016](test-cases.md#know-016): [step 11060](test-cases.md#L11060) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-018](test-cases.md#know-018): [step 11099](test-cases.md#L11099) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-019](test-cases.md#know-019): [step 11133](test-cases.md#L11133) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-020](test-cases.md#know-020): [step 11167](test-cases.md#L11167) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-021](test-cases.md#know-021): [step 11202](test-cases.md#L11202) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-022](test-cases.md#know-022): [step 11235](test-cases.md#L11235) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-023](test-cases.md#know-023): [step 11271](test-cases.md#L11271) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-024](test-cases.md#know-024): [step 11306](test-cases.md#L11306) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-025](test-cases.md#know-025): [step 11342](test-cases.md#L11342), [step 11343](test-cases.md#L11343) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-026](test-cases.md#know-026): [step 11379](test-cases.md#L11379) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-027](test-cases.md#know-027): [step 11414](test-cases.md#L11414) | Verified identity, scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-028](test-cases.md#know-028): [step 11448](test-cases.md#L11448) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-029](test-cases.md#know-029): [step 11482](test-cases.md#L11482) | Verified identity, scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-031](test-cases.md#know-031): [step 11553](test-cases.md#L11553), [step 11554](test-cases.md#L11554) | Verified identity, scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-032](test-cases.md#know-032): [step 11589](test-cases.md#L11589) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-040](test-cases.md#know-040): [step 11660](test-cases.md#L11660) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-033](test-cases.md#know-033): [step 11696](test-cases.md#L11696) | Verified identity, scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-034](test-cases.md#know-034): [step 11727](test-cases.md#L11727) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-035](test-cases.md#know-035): [step 11757](test-cases.md#L11757) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-036](test-cases.md#know-036): [step 11790](test-cases.md#L11790) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-037](test-cases.md#know-037): [step 11821](test-cases.md#L11821) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-038](test-cases.md#know-038): [step 11854](test-cases.md#L11854) | Verified scope, type. | unknown; inspect the actual target and bind its independent assertions. |
| [KNOW-049](test-cases.md#know-049): [step 12186](test-cases.md#L12186) | Verified identity, scope, type. | unknown; inspect the actual target and bind its independent assertions. |

## Remaining evidence and policy gaps

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Unreviewed automation mappings](evidence/refinement/gherkin-manifest.json) | All 521 cases remain unready for executable handoff. | unknown | Map existing Robot Browser keywords, fixture setup, selectors, and assertion helpers. |
| [Draft policy conflicts](evidence/knowledge-inspection.md#open-rule-decisions) | Conflicting entitlement expectations cannot establish acceptance together. | unknown | Select the applicable rule and complete required review. |
| [Proposed quality expectations](evidence/crosscut-inspection.md#authority-and-execution-limits) | Proposed thresholds and supported environments remain unapproved. | unknown | Review accessibility, browser, security, layout, and compatibility expectations. |
| [Component inventories](evidence/refinement/case-reviews.jsonl) | Source-derived identities do not prove live uniqueness or dependency semantics. | unknown | Inspect the rendered controls and record precise locators. |
| [Persistence and failure probes](test-cases.md#group-form-timing) | Form closure cannot establish saved values or error recovery. | unknown | Bind request-persisting fixtures and independent reload assertions. |

## Validation

The [document checks](evidence/refinement/document-checks.json) cover IDs, assertions, links, source fingerprints, and canonical checkpoints.
The [runtime receipt](evidence/refinement/validation-results.json) records tests, wheel construction, and installed workspace validation.
The final suite ran 611 tests.
Two optional connector integration tests were skipped.
The wheel uses offline build dependencies through `--no-build-isolation`.
The normal isolated dependency download remains untested in this stage.
No external connector or live business environment was used.
ASD review remains pending.

## Authority and next phase

| Named phase | Status | Evidence limit and consequence | Owner and next action |
| --- | --- | --- | --- |
| Refine existing definitions | COMPLETE | All 521 IDs have version 2 definitions and reconciled evidence mappings. | Codex; retain this stage and its validation. |
| Accept incomplete UI procedures | NEEDS_CLARIFICATION | 28 cases lack required UI targets. | unknown; resolve the listed controls. |
| Execute business cases | NEEDS_CLARIFICATION | Fixtures, executable assertions, and expectation reviews remain incomplete. | unknown; bind a selected scope and environment before execution. |

Definition completion does not grant business approval or publication authority.
The [execution binding](test-cases.md#execution-binding) remains unchanged in meaning: every case is NOT_RUN.
