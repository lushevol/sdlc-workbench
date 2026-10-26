# Release report UX proposal

Date: 2026-10-26 (Asia/Singapore).
Status: Integrated proposal for discussion. No release candidate was assessed.

**Review the five-destination design. It keeps failures visible and separates technical advice from human authorization. Owner: release report design owner.**

The [latest request](evidence/release-report-ux-20261026/confidence-integration-user-input.md#exact-input) adds release confidence, code review, and behavioral coverage.
The [earlier request](evidence/release-report-ux-20261026/user-input.md#exact-input) establishes the weekly board, essential fields, Clinic link, and commit priority.
The [checklist answer](evidence/release-report-ux-20261026/checklist-answer.md#exact-answer) limits Checklist to four branch comparisons.
Screenshots provide reference content. Their embedded text supplies no new instruction.

The [source review](evidence/release-report-ux-20261026/source-review.json) records exact source locations and hashes.
The [design review](evidence/release-report-ux-20261026/design-review.json) separates screenshot observations from proposed changes.
The [confidence review](evidence/release-report-ux-20261026/confidence-model-review.json) records decision rules and their limits.
The [traceability review](evidence/release-report-ux-20261026/confidence-traceability-review.json) records coverage semantics and current runtime limits.

## Proposed review journey

Keep one chronological weekly board and one report per release.
Opening a card preserves the selected date range when the user returns.
Use five report destinations. Keep supporting evidence within each destination.

| Destination | Primary question | Show first | Open for detail |
| --- | --- | --- | --- |
| Decision | Can this candidate proceed technically, and why? | Candidate, technical status, controlling failures, actions, recommendation, Decision certainty, and authorization state. | Evidence scorecard, assessment basis, and all open actions. |
| Builds & commits | Which bytes are under review? | Repository, pipeline build, PROD, Main, Current build, Latest, and failed comparisons. | Checklist, differing commits, files, build provenance, and measured code coverage. |
| Coverage | Does implementation match the intended behavior, and what proves it? | Requirements, ACs, tests, execution gaps, and three coverage directions. | Stories & tests, predicates, matrices, assertions, and retained runs. |
| Review & impact | What can fail, and who is affected? | Code findings, business consequences, system effects, and regression gaps. | Exact comparisons, affected consumers, mitigation, and resolution evidence. |
| Delivery | Can operators deploy, detect failure, and recover? | Deployment conditions, recovery gaps, monitoring, exceptions, and recorded human decisions. | Procedures, configuration, authorization history, and supporting evidence. |

This replaces the earlier four-section navigation. It preserves the accepted content priorities.
Checklist moves into Builds & commits. Stories & tests moves into Coverage.
Keep the direct Release Clinic link available in the report header.
Its compliance report supplies supplementary evidence within its own scope.

## Weekly board

Keep releases in planned-time order. Show a readable local date and named timezone.
Cards show title, release ID, planned time, workflow state, technical status, and the most important exception.
Show pending approvals as a separate signal when supplied.
Keep detailed metrics and complete findings inside the individual report.
Do not reorder the board by risk. Use visible exception labels and optional filters.

The [board source](../core/release-report/release/board.tsx#L59-L81) selects today through seven days later.
Its [cards](../core/release-report/release/board.tsx#L224-L365) expose approvals and performance-testing scope.
Performance-testing scope does not establish passing test execution.

## Decision: the first screen

Keep the decision view short. Aim for 300 words or fewer before supporting detail.
Show title, release ID, planned time, candidate build, target environment, and assessment time.
Keep artifact identity and source revision accessible beside the candidate.
Show release approach and nature of change when useful and available.
The [existing header](../core/release-report/release/details.tsx#L95-L191) supplies the current release metadata.

Use four distinct fields:

| Field | Meaning | Presentation rule |
| --- | --- | --- |
| Technical status | `GO`, `CONDITIONAL`, `NO_GO`, or `BLOCKED`. | State the controlling condition beside the status. |
| Recommendation | `RECOMMEND`, `DO_NOT_RECOMMEND`, or `INSUFFICIENT_EVIDENCE`. | Show analyst advice within the declared scope. |
| Decision certainty | Evidence support for that recommendation. | Always show the recommendation beside the score and confidence level. |
| Human decision and authorization | Actual recorded human readiness decision and deployment authorization. | Keep separate fields, sources, actors, times, scopes, and validity limits. |

Technical `GO` alone permits `can_go: true`. Other technical states require reassessment before that field changes.
Human authorization alone does not resolve failed or unknown technical conditions.
When records are absent, show “No recorded readiness decision” and “No recorded deployment authorization.”
Do not infer either decision from the assistant recommendation.

Place controlling failures directly below the status. Keep each failure reason readable without expansion or hover.
Show consequence, owner, next action, and required closure evidence together.
Use `unknown` when the owner is unavailable.
Summarize the largest business consequence and broadest supported system effect near the recommendation.
Keep other material gaps visible through a compact linked list.

The prototype demonstrates `NO_GO`, `DO_NOT_RECOMMEND`, and `HIGH` Decision certainty at `100/100`.
Its illustrative evidence directly proves a material failure. The score supports holding that candidate.
It does not mean the release is ready or likely to succeed.
Human readiness and authorization remain pending in that example.
These values describe no actual release.

Keep the full scorecard secondary. Link each summary to its detailed evidence.
Use independent signals for code review, conformance, execution, operational evidence, and compliance.
Passing totals cannot offset a controlling material failure.
A successful pipeline and a Clinic verdict do not establish complete business verification.

## Decision certainty and actions

Apply the [decision model](../.agents/skills/release-confidence/references/decision-model.md#confidence-score-and-release-status) when an actual assessment exists.
Do not average dimension scores or invent organizational thresholds.
The model scores each applicable evidence dimension from zero to five.
Decision certainty uses twenty times the lowest score among dimensions directly controlling the recommendation.
Name those dimensions, the score floor, and material limits.
A directly proved failure can score five while its condition status remains `FAILED`.
Other incomplete dimensions remain disclosed even when that failure controls a hold recommendation.

The secondary scorecard shows dimension, status, score, criticality, rationale, evidence, owner, action, and closure evidence.
Include target score, target status, expected release-status effect, and reassessment trigger for each action.
Show at least one concrete action for every non-`GO` result or score below 100.
Keep source policy conditions separate from analyst recommendations.
No new runtime gate or approval engine enters this proposal.

## Builds & commits

Keep commit comparisons a primary technical review surface.
Group information by repository and pipeline build. Open the failed repository first.
Show four identities together before raw evidence.
Use short SHAs with full-SHA access and source links in implementation.

| Reference | Exact meaning | Supporting source |
| --- | --- | --- |
| PROD | Source revision from the selected qualifying deployed build. | [Production selection](../core/release-report/ado-api/pipeline.ts#L140-L162). |
| Main | Main branch tip at collection. | [Main reference](../core/release-report/ado-api/git.ts#L338-L365). |
| Current build | Immutable source revision used by the candidate pipeline build. | [Build source revision](../core/release-report/release-report.service.ts#L199-L203). |
| Latest | Candidate branch tip at collection. | [Latest branch reference](../core/release-report/ado-api/git.ts#L287-L318). |

Keep Current build visually distinct. It identifies the candidate artifact's source.
Attach deployed build identity to PROD. Attach branch and collection time to Latest.
A newer branch commit must not relabel the selected candidate.
A source SHA alone does not establish packaged or deployed bytes.
Keep artifact digests and provenance available when supplied.

Retain Reference strip and Reference table as layout options.
The earlier prototype offers both. The integrated prototype shows the strip for this discussion.
Recommend the strip for an expanded desktop repository. The table supports long branches and larger inventories.
Use a two-by-two reference layout on narrow screens.
Reference cells show identities. Draw ancestry only when inspected parent relationships support it.
The fourth photograph establishes comparison priority. Its ideal branch model does not prove actual ancestry.

### Checklist: four branch comparisons

Show direction, observed result, reason, counts, and a direct diff action together.

1. Current build versus Latest: show commits missing from the candidate.
2. Current build versus PROD: show missing production changes and candidate additions.
3. Current build versus Main: show missing main changes and candidate additions.
4. Main versus PROD: show divergence between the collected baseline references.

The [comparison source](../core/release-report/release/components/BuildDiffStatus.tsx#L42-L145) supplies these checks.
The [recorded answer](evidence/release-report-ux-20261026/checklist-answer.md#exact-answer) resolves their Checklist scope.
Merge-comment exceptions remain a policy limit. Source styling does not establish a release-blocking rule.

Keep successful build execution separate from failed comparisons.
Open commit and file lists on request. Preserve the failed reason above those lists.
Show unit execution, line coverage, and branch coverage separately.
Show percentage-point differences against PROD only when matching measurements exist.
Use Unavailable for missing measurements. Use zero only when a numeric zero was returned.
Do not infer coverage thresholds from colors.

## Coverage

Combine Stories & tests with behavioral coverage. Keep individual stories linked to their builds and canonical cases.
Show story identity, workflow state, required test levels, observed outcomes, defects, and evidence freshness.
Do not sum repeated requirement evidence across builds.
Preserve failed, skipped, blocked, stale, simulated, and unrun results.
Show first-run failures and retry conditions beside later passes.

Declare the requirement, AC, predicate, meaningful change, canonical case, and execution inventories before calculating coverage.
A mapping table cannot supply its own denominator.
Use source-qualified AC IDs and versions. Keep equal labels from different requirements distinct.
Count each inventory item once across many-to-many relationships.
A compound AC qualifies only when every applicable predicate qualifies.

Start with gaps and a compact metric summary. Expand the complete metrics within this destination.

| Metric group | Keep separate |
| --- | --- |
| AC to tests | Canonical definitions, inspected assertions, and matching passing execution. |
| AC to implementation | Inspected implementation mappings and semantic conformance. |
| Changes to tests | Canonical definitions, inspected assertions, and matching passing execution. |
| Behavioral justification | Changed business behavior supported by sourced intent. |
| Instrumented coverage | Line, branch, total repository, and changed-code measurements. |

Each metric shows `n / d`, scope, exact versions, affected gaps, and evidence limits.
Show percentages only for complete, known, nonempty inventories.
Use `N/A` for a known empty denominator. Use `UNKNOWN` when the complete inventory is unavailable.
Neither state means success.

The [illustrative example](evidence/release-report-ux-20261026/confidence-prototype-source.html) declares six API ACs.
One unresolved predicate limits canonical test definitions and inspected implementation mappings to `5 / 6` each.
Conforming implementation qualifies `4 / 6`.
Portal's complete inventory is unavailable, so whole-release coverage remains `UNKNOWN`.
The API subset cannot supply the whole-release denominator.

Provide three switchable matrices:

| Matrix | Include | Essential row evidence |
| --- | --- | --- |
| AC → Test Case | Every applicable AC, including unmapped criteria. | Predicates, canonical cases, required levels, inspected assertions, completeness, matching execution, and gaps. |
| AC → Code Change | Every applicable AC, including relevant unchanged implementation. | Intended predicates, change IDs, exact base/head source, conformance, omissions, contradictions, additions, and limits. |
| Code Change → Test Case | Every meaningful change, including untraced changes. | Repository, full base/head, symbol or hunk, AC or maintenance rationale, direct assertions, matching execution, and gaps. |

Keep necessary existing implementation as `UNCHANGED`. It can satisfy an AC without a new code change.
Classify maintenance and test-only changes separately. Retain their rationale and proportionate checks.
An absent mapping remains `UNKNOWN` until inspection establishes its meaning.
Use `EXTRA` only after demonstrating unsupported business behavior and completing an intent search.
Keep `MISSING`, `CONTRADICTORY`, `MATCH`, and `UNKNOWN` comparisons explicit.
Complete links can coexist with incorrect implementation or failed execution.

Selecting a row opens this evidence chain:

`Requirement → AC / predicate → implementation / change → canonical case → inspected assertion → retained execution`

Use the chain for navigation. It does not prove coverage or imply one-to-one relationships.
Show endpoint versions, exact locators, evidence classes, relationship grades, and limits.
Keep definition, source, assertion, and execution links separate.
Shared AC membership does not prove direct change-to-test coverage.
Inspect setup, invocation, helpers, and assertions before confirming that relationship.

Keep unit, contract, integration, system, and E2E boundaries visible.
A mocked check cannot close a required real-service check.
A passing rejection assertion does not establish the opposite intended business outcome.
Interpret `TC >= AC = Code Change` as behavioral containment and equivalence, never equal artifact counts.
The [coverage procedure](../.agents/skills/verify-implementation/references/behavior-review.md#report-coverage) defines these distinctions.
The [traceability template](../core/knowledge/templates/sdlc/traceability-record.md#coverage-inventories-and-summary) defines the supporting inventories and matrices.

## Review & impact

Show actionable code findings before inspection statistics.
Bind every review to its repository, comparison mode, full base/head commits, and reviewed content fingerprint.
List inspected, generated, binary, excluded, and unavailable paths separately.
“No actionable defect found” applies only to the inspected scope.
It does not establish defect absence or human approval.

Use the repository's severity policy when available. Otherwise identify the [code-review priority scheme](../.agents/skills/code-review/SKILL.md#calibrate-findings).
Show the severity source beside its meaning.
Do not infer automatic production permission from a priority label.
Each finding needs a trigger, changed cause, consequence, exact source, owner, and next action.

Keep finding disposition separate from severity and technical result.
Show whether a finding remains open, lacks closure evidence, has matching resolution evidence, or has a recorded risk disposition.
These are proposed display states. Source records retain their actual values and authority.
A claimed fix needs matching resolution evidence. Accepted risk does not turn a failed test into a pass.
Keep inferred concerns separate from demonstrated defects.

Place business impact, system impact, and regression effects beside the findings they explain.

| Impact view | Essential content |
| --- | --- |
| Business | Actors, journeys, intended benefit, adverse outcome, exposure, obligations, workaround, owner, and limits. |
| System | Components, callers, consumers, contracts, dependencies, data, state, configuration, and failure propagation. |
| Regression | Consequential unchanged behavior, combined changes, mixed versions, shared state, and deployment order. |

Link each material effect to its condition, canonical case, required level, actual result, mitigation, and owner.
Compare intended, old, and candidate behavior for material gaps.
Distinguish observations, source-based predictions, and unresolved expectations.
High impact does not automatically lower evidence confidence. Small changes can still cause severe failures.
Do not invent affected populations, financial loss, or low failure likelihood.
The [impact model](../.agents/skills/release-confidence/references/decision-model.md#business-and-system-impact) defines these evidence boundaries.

## Delivery

Group deployment, recovery, monitoring, exceptions, and human decisions in one destination.
Show missing operational evidence before complete procedures.
Bind evidence to the artifact, target environment, effective configuration, and assessment time.
Keep source-only conclusions distinct from deployable-artifact conclusions.

Show applicable deployment order, compatibility, feature flags, migration, and mixed-version conditions.
Show recovery procedures, their retained evidence, and responsible operators.
A code rollback can leave data, messages, external effects, or backlogs.
Show monitoring signals, sourced stop triggers, and response owners.
Do not invent performance limits, expiry periods, or mandatory signatories.

Exceptions need recorded authority, affected condition, scope, rationale, mitigation, and applicable validity limits.
Preserve the underlying failure and residual risk.
An applicable exception can dispose a policy condition only when policy permits it.
An approval label cannot waive a demonstrated material release failure.

Read existing authorization history first. Display actual readiness decisions and deployment authorization as separate records.
Show source, actor, time, candidate, target, scope, and validity when supplied.
Keep missing records explicit. Do not add approval-writing controls in this prototype.
Actual approval capture and external writes require a separately defined workflow.
The [assessment reporting guide](../.agents/skills/release-confidence/references/reporting.md#report-content) preserves these decision boundaries.

## Release Clinic and evidence behavior

Keep the direct Clinic entry near the release header. Keep detailed compliance inside Clinic.
The prototype reserves this position without a connected external destination.
Clinic findings supplement the combined assessment. They retain their own identities, versions, scope, and limits.

Use red for observed failures and amber for warnings. Add readable labels for unknown and unavailable evidence.
Never rely on color alone. Failed reasons remain visible on narrow screens.
Show collection and assessment times so reviewers can detect stale evidence.
Keep raw hashes, complete inventories, and repeated machine fields secondary.
Every conclusion must still link to its supporting evidence.

## Current capability boundary

This proposal describes presentation and reviewed assessment data. It does not implement collection or decision logic.
The [assurance runtime guide](BEHAVIOR_REVIEW.md#interpret-the-result) defines the implemented deterministic checks.
Its existing grades and metrics do not compute full coverage matrices or semantic conformance.
The runtime provides no approval engine, assertion parser, or native test-result importer.

`current_source_execution` measures declared freshness and assertion binding availability.
It can include failed, simulated, or insufficient-level results. It is not passing behavior coverage.
`VALID` and `CURRENT` do not establish verified business behavior or deployed configuration.
Current runtime business verification remains `NOT_VERIFIED`.
The [metric limits](BEHAVIOR_REVIEW.md#interpret-metrics) remain visible wherever these existing fields enter the report.

No actual score, recommendation, release status, conformance result, or human decision was assigned during this design stage.
Any future data adapter must preserve these source and evidence distinctions.

## Evidence confidence and discussion

| Conclusion | Confidence | Supporting evidence and material limit |
| --- | --- | --- |
| The chronological board opens individual release reports. | High. | [User intent](evidence/release-report-ux-20261026/user-input.md#exact-input), photographs, and source agree. |
| Four commit references retain primary technical placement. | High. | [Source identities](evidence/release-report-ux-20261026/source-review.json) match the user's explicit priority. |
| Checklist contains only four branch comparisons. | High. | The [user answer](evidence/release-report-ux-20261026/checklist-answer.md#exact-answer) resolves this scope. |
| Clinic remains a direct supplementary report. | High. | [User intent](evidence/release-report-ux-20261026/user-input.md#exact-input) and the [confidence review](evidence/release-report-ux-20261026/confidence-model-review.json) agree. |
| Decision fields and coverage metrics require independent meanings. | High. | [Decision evidence](evidence/release-report-ux-20261026/confidence-model-review.json) and [traceability evidence](evidence/release-report-ux-20261026/confidence-traceability-review.json) support these boundaries. |
| Five destinations balance the expanded content. | Medium. | This is a layout proposal. No usability study or live endpoint verification occurred. |
| Defaulting to failures improves this review journey. | Medium. | The [design review](evidence/release-report-ux-20261026/design-review.json) and user priority support the choice. User review remains necessary. |

The proposed discussion focuses on two design choices.
First, review whether the Decision screen provides enough evidence before opening a detailed destination.
Second, review whether the coverage matrices and selected-row chain expose the missing proof clearly.
These are design questions. They do not request deployment approval or introduce unresolved business policy.

## Prototype and stage boundary

The [attachment manifest](evidence/release-report-ux-20261026/attachment-manifest.json) retains original image hashes and local source paths.
The [integrated prototype snapshot](evidence/release-report-ux-20261026/confidence-prototype-source.html) retains the discussion design.
The [integrated browser checks](evidence/release-report-ux-20261026/confidence-prototype-validation.json) record its checked interactions and presentation limits.
The live discussion fragment is named `release-confidence-prototype.html`.

Keep the [earlier snapshot](evidence/release-report-ux-20261026/prototype-source.html) and [earlier browser checks](evidence/release-report-ux-20261026/prototype-validation.json) as historical evidence.
Their four-section navigation does not define the integrated proposal.
All prototype IDs, SHAs, dates, counts, reasons, decisions, and outcomes are illustrative.
They do not describe the photographed releases.
Browser checks do not establish business conformance, source accuracy, production readiness, or human authorization.

This stage changes documentation and a discussion prototype only.
It creates no business task, domain knowledge record, runtime change, or approval workflow.
Runtime tests and wheel builds do not apply to this documentation stage.
Full ASD writing review remains pending.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - The prototype uses illustrative data and has no connected external destinations.
  - No actual release assessment, usability study, or live endpoint verification occurred.
```
