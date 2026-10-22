# Release confidence decision model

Confidence describes the evidence supporting the stated recommendation.
It is not a production success probability.
A recommendation describes technical suitability within the declared scope.
Human authorization remains a separate decision.

## Select applicable conditions

Read the release policy and the change's actual business and operational effects.
Record each condition's source, required evidence, owner, and applicability rationale.
Separate mandatory policy conditions from analyst recommendations.
When policy is absent, identify evidence-based concerns without inventing an organizational gate.
Keep material policy ambiguity as an owner decision.
Do not invent coverage thresholds, severity cutoffs, signatories, expiry periods, or performance limits.

Consider security, privacy, performance, resilience, data integrity, compatibility, and supply-chain evidence when the change affects them.
For deployments, consider artifact provenance, effective configuration, feature flags, dependencies, and environment differences.
For data changes, consider migration order, mixed versions, backfill, recovery, and irreversible effects.
For operations, consider smoke assertions, observable signals, rollback triggers, recovery evidence, and responsible operators.
Require measured values only against sourced limits with defined conditions.
An irreversible change may need demonstrated recovery instead of a conventional rollback.
Record why any condition is inapplicable. Missing evidence is not an applicability rationale.

## Dimension status

Use these analyst statuses beside each evidence dimension or condition.
They do not replace intake, knowledge governance, or runner statuses.

| Status | Meaning |
| --- | --- |
| `SUPPORTED` | Current inspected evidence supports the stated condition within its required scope and level. |
| `LIMITED` | Evidence supports a bounded claim but leaves a disclosed boundary or indirect link. |
| `FAILED` | Evidence establishes an unmet condition or consequential release failure. |
| `UNKNOWN` | Missing, stale, conflicting, or unbound evidence prevents the condition judgment. |
| `NOT_APPLICABLE` | Source-backed change analysis explains why the condition does not apply. |

A clean review means no actionable defect was found within its inspected scope.
It does not prove the absence of defects.
Reopen findings closed without matching resolution evidence.
Treat changed assertions, skipped tests, retries, quarantines, and expected failures explicitly.
Inspect contradictory runs before accepting a later pass as resolution.
Report first-run failures and rerun conditions. Do not hide instability with a pass percentage.

## Coverage with declared denominators

Declare the inventories before counting mapped rows.
Use stable behavior and path identities, including affected regression behaviors and consequential unchanged consumers.
For each metric, show numerator, denominator, scope, source, level, exclusions, and limits.
Count each denominator item once despite many-to-many relationships.
Keep partial behavior coverage visible. All required predicates must qualify before counting the whole behavior.

| Metric | Denominator | Qualifying numerator |
| --- | --- | --- |
| Requirement implementation | Included active behavior versions | Behaviors with confirmed inspected implementation links for all required outcomes. |
| Required assertion coverage | Included active behavior versions | Behaviors with inspected assertions for all required predicates at required levels. |
| Matching passing execution | Included active behavior versions | Behaviors with matching passing actual execution and no material unresolved conformance finding. |
| Review inspection | Selected changed paths | Paths actually inspected at the selected comparison. Explain generated, binary, excluded, and unavailable paths. |
| Changed-path assertion reach | Included changed implementation paths | Paths reached by confirmed inspected assertion chains within the stated level and boundary. |
| Measured code coverage | Instrumented executable lines or branches in the declared scope | Lines or branches reached in a matching retained coverage run. |

Use `N/A` when a denominator is zero or unknown. Explain which condition applies.
Do not replace an unknown inventory with the available mapped subset.
Report required critical behaviors separately so a large low-impact set cannot hide a gap.
State criticality sources. Label analyst-selected criticality as an inference with its consequence.
Keep total repository coverage separate from changed-code coverage.
Separate line coverage from branch coverage. Neither proves assertion quality or requirement conformance.
Mark unavailable measurements as unavailable. Do not require a coverage tool without an applicable need.

Separate unit, contract, integration, system, and browser E2E evidence when their boundaries differ.
A mocked integration cannot close a required real-service check.
A passing assertion for rejection, logout, or an expected failure cannot prove the opposite business outcome.
Do not count planned, skipped, blocked, stale, simulated, or unrun cases as passing actual execution.
Preserve partial predicates and case outcomes alongside behavior totals.
Use the existing [coverage handoff](../../verify-implementation/references/behavior-review.md#report-coverage) for additional traceability directions.

## Bind evidence to the candidate

For consequential claims, inspect the requirement, implementation, assertion chain, and original result separately.
Record full revisions or exact hashes, source locators, run IDs, configuration, inputs, and environment identity.
Check artifact-to-source provenance. A source SHA alone does not identify packaged or deployed bytes.
Assess environment parity through relevant differences. Do not assume staging is equivalent to PROD.
Keep secrets out of retained configuration evidence.

Preserve earlier evidence when it is stale.
Reuse unchanged results only after checking relevant bytes, dependencies, build provenance, and execution applicability.
Unrelated commits need not invalidate unchanged bytes.
Changed requirements need current intent review before prior approval can support conformance.
Changed code, assertions, helpers, configuration, artifacts, or dependencies require reassessment of affected claims.
Do not reconstruct a run's original bindings from later records.

Compare intended, old, and new behavior for material conformance or regression gaps.
Link the same canonical case, setup, numbered steps, and explicit assertions.
Label observed outcomes, source predictions, and unknown results separately.
An unchanged defect can still violate an applicable release condition.
Its existence before this change does not establish a waiver.

## Evidence confidence

Choose confidence for the material claims needed by the stated recommendation.
Report unassessed dimensions even when a demonstrated failure already settles a negative recommendation.
Do not average dimension statuses or infer confidence from finding counts.

| Confidence | Required explanation |
| --- | --- |
| `HIGH` | Direct, current evidence resolves the material claims supporting this recommendation within the declared scope. |
| `MODERATE` | Current evidence supports those claims, with bounded indirect evidence or nonmaterial limits. Name each limit. |
| `LOW` | Material claims rely on weak, conflicting, stale, or incomplete evidence. Name the affected conclusion. |
| `UNDETERMINED` | Missing candidate identity, scope, or foundational evidence prevents meaningful confidence assessment. |

High confidence in a demonstrated blocking failure does not establish confidence in unassessed dimensions.
For `RECOMMEND`, material required conditions must have current supporting evidence.
`MODERATE` can accompany `RECOMMEND` only when remaining limits are nonmaterial to those conditions.
Explain why each limit does not change the recommendation.
`LOW` or `UNDETERMINED` cannot support `RECOMMEND`.

## Production recommendation

Apply these rules in order. Preserve all other gaps beside the controlling conclusion.

1. Use `DO_NOT_RECOMMEND` when evidence establishes a material release failure or an unmet applicable mandatory condition.
2. Otherwise use `INSUFFICIENT_EVIDENCE` when a material unknown prevents judgment or the named intake gate remains unresolved.
3. Use `RECOMMEND` only when evidence supports applicable conditions and no unresolved material failure remains.

These rules express analyst advice. They do not implement an executable release gate.
For unresolved intake, record only a provisional finding or stop concern; do not hand off a downstream recommendation.

Use the owning repository's severity policy when available.
P0/P1 findings need an explicit stop assessment against their demonstrated consequences and the release policy.
Do not infer that every P2 permits or prevents production.
Do not let passing metrics offset a consequential correctness, security, or data-integrity failure.
When policy is missing, state the conservative technical concern and the unknown decision owner.

An exception needs retained authority, affected condition, exact scope, rationale, mitigation, and validity limits when defined.
An unsupported acceptance claim does not close a condition.
Accepted risk does not change a failed test into a pass or restore stale evidence.
Record whether policy permits the exception and whether the evidence supports its applicability.
An applicable authorized exception can dispose a policy condition. Preserve the underlying failure and residual risk.
Do not waive a demonstrated material release failure through an approval label.

Record the changes needed to alter the recommendation.
Name each blocking action, its owner, and the evidence needed to close it.
Reassess before use when relevant release inputs change.
Confidence and recommendations never grant deployment authorization.
