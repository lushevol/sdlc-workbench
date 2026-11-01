# Record a release knowledge synchronization

Use one living `10-knowledge-sync.md` under the owning task.
Copy the [change-request template](../../../../core/knowledge/templates/sdlc/change-request.md#template), including its frontmatter and required headings.
This reference supplies synchronization-specific content within that form. It creates no new artifact kind or runtime schema.
Use actual identities and evidence. Keep unavailable values null or `unknown` and retain review fields as pending when required.
Lead with the required [critical-conclusion callout](../../../../tasks/README.md#critical-conclusions-in-task-documents).

## Populate the existing sections

| Change-request section | Synchronization content |
| --- | --- |
| Request and source facts | Exact request, operation identity, release, environment, as-of time, evidence fingerprint, and starting knowledge hashes. |
| Stage boundary and readiness | Named candidate-preparation or post-deployment stage; frozen intake integrity; authorized scope; limits; blocked publication or applicability. |
| Proposed change | Old meaning, intended rule, inspected implementation, deployment applicability, observed execution, and proposed reusable meaning. |
| Scope and affected artifacts | Required row inventory; knowledge IDs and versions; dependent groups; exclusions; unknown affected scope. |
| User impact | Consequences of stale knowledge, misleading applicability, or unsupported policy changes, with evidence and owners. |
| System impact | Consumers, contracts, configuration semantics, rollout combinations, and downstream knowledge references. |
| Options and consequences | Supported no change, candidate successor, eligible publication, or unresolved conflict, with decision authority. |
| Proposed acceptance and validation | Per-claim accuracy checks, source comparison, provenance, governance gates, independent retrieval review, and report parity. |
| Implementation and release proposal | Actual prepared records, versions, audit events, publication state, partial rollout or rollback, and deployment evidence limits. |
| Sources and evidence limits | Exact source revisions, artifact/configuration identities, observations, snapshots, queries, hashes, authority, and missing evidence. |
| Unknowns and blockers | Conflicts, access gaps, pending human reviews, unknown owners, decision consequences, and next actions. |
| Stage evidence and completion | Separate preparation, review, publication, synchronization, and report metrics; actual validator results and limitations. |
| Requested decision and actual disposition | Pending versus recorded decisions, exact reviewed hashes, operation status, release authorization, and remaining actions. |

## Scope and row identity

Record these values under `Request and source facts` or its operation subsection:

```yaml
operation_identity:
  workspace: null
  release: null
  deployment_or_rollout: null
  environment: null
  cohort: null
as_of: null
mode: candidate_preparation
input_evidence_fingerprint: null
starting_knowledge_refs: []
predecessor_attempt_ref: null
```

Fingerprint the exact selected evidence identities and hashes. Retain its inventory so a retry can compare the same inputs.
Use `mode: post_deployment` only when deployment applicability has supporting evidence.
Record target deployment unknowns separately from known local source and execution identities.
For mixed deployment support, record each row's mode or use linked attempts with distinct scopes.
One component's deployment receipt cannot promote another component's candidate claims.

Each required row identifies one changed or checked claim for a knowledge topic and applicability scope.
Count each row once. A dependent group closes only when its required records remain mutually consistent.

| Row ID | Topic / claim | Environment / cohort / interval | Old knowledge ID/version/hash | Proposed ID/version/hash | Disposition | Evidence | Owner / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Replace with actual row identity. | Link the exact claim. | Use actual applicability or unknowns. | Retain starting bytes. | Record prepared final bytes or null. | Updated, unchanged with rationale, or unresolved. | Link intent, source, deployment, and observations separately. | Use actual owner or unknown. |

Keep each row's preparation, review, and publication state separate from its disposition.
An `updated` candidate is not yet a synchronized published row.
For no-change rows, inspect whether both reusable meaning and applicability remain accurate.

## Applicability and accuracy

Put concise applicability beside each changed claim in the knowledge document.
Use supported frontmatter extensions or a body table. The current runtime does not select records by these values automatically.

| Claim | Evidence class | Release / deployment | Artifact / configuration | Environment / cohort | Effective interval | Review state | Evidence and limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Link the claim. | Intended, inspected implementation, deployment, observed execution, or inference. | Actual identity or unknown. | Actual digest or unknown. | Actual scope. | Known start/end or explicit unknowns. | Actual state and reviewed hash. | Link evidence separately from conclusions. |

Before publication, confirm these questions against final bytes:

- Does the new text preserve approved intent when implementation restores or contradicts that intent?
- Does each actual-behavior claim have the correct source revision, environment, rollout, and observation boundary?
- Do predecessor versions remain available where earlier deployment scopes still require them?
- Are rollout, observation, effective, and documentation times distinguished without unsupported backdating?
- Do important requirements and decisions have actual human approval for the final content hash?
- Do retained source identities, review hashes, audit events, references, and displayed report counts agree?

Retain each check's actual outcome and evidence. Record unresolved semantic questions beside their consequences.
Independent confirmation must inspect original evidence and final content. A second summary of the same draft is insufficient.

## Completion and report parity

Define `R` as the complete declared required row inventory. Keep unknown affected scope explicit.
Show the actual numerator, denominator, exclusions, evidence, and limits for each metric.

| Metric | Qualifying numerator | Denominator |
| --- | --- | --- |
| Candidate preparation | Rows with supported prepared final content or an inspected no-change rationale. | `R` |
| Required review completion | Rows with applicable completed review bound to final hashes, or a supported review-inapplicability rationale. | `R` |
| Eligible publication | Changed rows with matching published records and required review, provenance, and audit evidence. | Declared rows requiring changed published content. |
| Knowledge synchronization | Rows with applicable published content or an inspected supported no-change rationale. | `R` |
| Release-report parity | Required maintained views showing the canonical status, scope, counts, versions, conflicts, and actions correctly. | Declared required Markdown/HTML report views. |

Use `N/A` for known empty or unknown denominators, with its reason.
Do not substitute known mapped rows for an unknown complete inventory.
Keep runtime-log evidence coverage, passing behavior, release confidence, deployment authorization, and synchronization counts separate.

Maintain one canonical summary under `Stage evidence and completion`. Reports must render or reference those values consistently.

```yaml
knowledge_sync:
  operation_status: PENDING
  required_rows: null
  unknown_affected_scope: true
  prepared_rows: null
  reviewed_rows: null
  changed_rows_requiring_publication: null
  published_changed_rows: null
  supported_no_change_rows: null
  synchronized_rows: null
  open_conflicts: null
  changed_knowledge_refs: []
  unresolved_row_refs: []
  required_report_views: []
  reconciled_report_views: []
  validation_refs: []
  independent_review_ref: null
  remaining_action_refs: []
```

`COMPLETE` requires all known required rows synchronized, no unknown affected scope, and required report parity.
Publication pending means the affected changed row remains unsynchronized. Do not rename drafting success as complete post-release synchronization.
Preserve historical report conclusions. Update a maintained current view or link a successor when frozen assessment bytes must remain unchanged.
If a renderer is unavailable, name the view and pending parity action. Do not create unsupported screenshots or execution claims.

Run applicable document lint, workspace validation, final ingestion checks, link/hash checks, and report parity checks.
Retain actual results under the owning task. Automated checks do not establish semantic correctness or human approval.
Keep `writing_review.automated_check` based on actual checks and `asd_review: PENDING` until a complete writing review occurs.
