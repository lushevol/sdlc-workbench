---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - This proposal is based on local source inspection. Feature implementation and execution checks have not occurred.
---

# Knowledge review capability implementation plan

The [user request](implementation-plan-user-input.md#exact-user-input) asks how to implement the agreed review workflow.
The request is a high-priority reference for this proposal.
This stage records a plan. It changes no runtime code or domain knowledge.

## Current foundation

Inspected revision: `98b96c72544834f6be63a7c36e20fa9229f63220`.
The current [review document](../../../tasks/ui-test-coverage-20261022/05-knowledge-questions.md) demonstrates the selected narrative-and-options format.
The existing guides record asynchronous completion, explicit continuation, and saved user-input priority.
Reusable review rendering, response capture, and reconciliation helpers remain proposed.

| Claim | Evidence class | Inspected source | Limit |
| --- | --- | --- | --- |
| Ingestion already separates agent synthesis from deterministic evidence checks. | Inspected implementation and procedure | [Ingestion harness](../../../core/ingestion/harness.py#L507), [shared procedure](../../../.agents/skills/ingest-knowledge/SKILL.md#follow-the-checkpoints) | The harness does not create narratives or interpret business answers. |
| Search currently accepts no lifecycle scope. | Inspected implementation | [Knowledge operations](../../../core/providers/knowledge.py#L53-L82) | Existing callers can retrieve candidate records. |
| Publication checks already bind review events to exact record bytes. | Inspected implementation | [Governance checks](../../../core/governance/validation.py#L313-L338) | These checks cannot authenticate reviewers or establish business truth. |
| CLI and MCP already share resource operations. | Inspected implementation | [CLI dispatch entry](../../../core/cli.py#L39-L44), [MCP tool contract](../../../core/mcp.py#L16-L24) | New operations still require appropriate resource grants. |
| Packaging ships shared templates, schemas, skills, and guides. | Inspected implementation | [Build support](../../../setup.py#L21-L39), [scaffold manifest](../../../scaffold.json), [initialization](../../../core/workspace.py#L77-L95) | Generated workspaces receive guides and contracts without runtime source. |

## Delivery 1: Repeatable review preparation

Extend the existing ingestion skill and its workflow reference.
Ship one review template and a versioned handoff contract under `core/knowledge/`.
Keep the current living Markdown document as the sole editable answer source.

Add a small helper module at proposed path `core/ingestion/review.py`.
Its preparation operation accepts structured, agent-reviewed topics, questions, choices, and evidence references.
It renders short narratives with nearby questions, unselected options, and editable answer fields.
Stable question and option IDs bind each choice to its meaning.

An immutable handoff receipt records the document version, hash, question identities, source revisions, and affected candidate hashes.
Store this receipt under the owning task's evidence directory.
Keep retained source snapshots and domain candidates in their existing locations.
No second editable answer register is introduced.

The agent preserves each supplied input before investigation or delegation.
Capture support records exact bytes, source, date, hash, stated scope, and high reference priority.
The latest explicit clarification controls intended behavior within its stated scope.
Earlier sources remain available. Priority does not establish deployment evidence or publication approval.
Runtime helpers capture supplied input. The coding agent supplies the actual chat message and context.

## Delivery 2: Reliable asynchronous continuation

Extend the shared skill with returned-answer capture, reconciliation, and candidate-update steps.
The user completes the document independently and requests ingestion continuation.
The first continuation action preserves the returned document and the explicit continuation message.

The helper then compares returned content with the exact handoff version.
It identifies explicit answers, blank fields, unknowns, changed fields, and structurally conflicting selections.
The agent assesses semantic contradictions and intended scope.
Choice letters resolve against the handed-over option meanings.
Free-text answers retain their exact wording and require agent interpretation.
Changed questions, option meanings, source hashes, or candidate hashes produce reconciliation findings.
Formatting changes outside semantic fields do not silently change answer meaning.

Blank and unknown answers preserve unresolved questions and earlier recorded answers.
Partial completion can advance resolved topics within the agreed scope.
Ambiguous selections or conflicting explanations remain open in the same living document.
Repeated processing of identical resolved answers creates no duplicate candidate version or governance event.
After application, save an immutable receipt linking answer IDs, returned snapshot hash, resulting candidate versions, and audit events.
The receipt also identifies the handoff version and application scope.
Use this receipt when checking repeated continuation across sessions.

The agent updates candidate content, provenance, findings, and applicable measurable criteria.
Reuse the existing harness for retained-source, prepared-content, and final checks.
Reuse existing governance rules for exact-byte review and publication events.
Ingestion continuation alone supplies no publication approval.

## Delivery 3: Distinguishable gold and review retrieval

Extend the existing knowledge provider with proposed scopes `published`, `review`, and `all`.
Define `review` as active unpublished records: candidate, investigated, and verified.
Keep contested, stale, and superseded records available through explicit investigation using `all`.
Preserve the existing low-level default scope for compatibility.
Make the query skill explicitly request published scope for gold answers.

Return record identity, version, lifecycle, owner, source references, and available scope with each result.
Preserve current locators, hashes, and exact read bytes.
Apply lifecycle filtering before result limits, so draft volume cannot hide published matches.

A published label alone does not establish gold eligibility.
Reuse governance checks for the selected record's current hash and required events.
Expose failed or unavailable checks. Unrelated unresolved candidates must not block otherwise valid published results.
Show source freshness and applicability limits beside the answer.
Local hash checks cannot establish that an external source remains the latest applicable policy.
Agent review still determines semantic applicability from available evidence.

Existing CLI and MCP resource dispatch will expose retrieval schema changes.
Initially, the shared skill can call installed review helpers directly, as it calls the current harness.
Any later MCP review operation must reuse the existing provider and grant boundary.
This plan requires no dedicated service or new runtime dependency.

## Implementation ownership and risk

| Area | Proposed change | Qualitative risk and consequence | Owner and next action |
| --- | --- | --- | --- |
| Shared ingestion skill | Add preparation, handoff, capture, and reconciliation procedures. | Moderate. Wrong option interpretation could change intended knowledge. | Workbench maintainer; implement stable identities and source-preserving checks. |
| `core/ingestion/` | Add narrow deterministic review helpers. | Moderate. Capture errors could lose answer provenance. | Workbench maintainer; test exact-byte retention, confinement, stale baselines, and duplicate processing. |
| `core/knowledge/` | Ship the review template and handoff schema. | Low. Incompatible formats could prevent resumed review. | Workbench maintainer; version contracts and support the existing living document. |
| Knowledge provider and query skill | Add explicit scopes and lifecycle metadata. | Moderate. A changed default could break existing consumers or present drafts as gold. | Workbench maintainer; retain low-level compatibility and make gold scope explicit. |
| Governance validator and harness | Reuse current checks and expose selected-record results where needed. | Moderate. Whole-workspace failures must not conceal a usable bounded topic. | Workbench maintainer; inspect callers before extracting shared validation logic. |
| Packaging and initialization | Ship contracts and helpers through the existing build. | Moderate. Missing assets could break installed workspaces. | Workbench maintainer; build the wheel and initialize outside this checkout. |

Individual maintainer identity remains unknown.
Existing consumers include provider tests, CLI/MCP adapters, ingestion skills, and generated workspaces.
No code changes are included in this planning stage.

## Planned acceptance cases

These scenarios define future implementation checks. They have not run.

```gherkin
Scenario: Preserve a returned answer document
  Given a handed-over review document has a recorded SHA-256
  And the user returns an edited document with an explicit continuation instruction
  When the agent captures the response before interpretation
  Then the retained document bytes equal the returned bytes
  And the response receipt links the saved continuation instruction

Scenario: Keep incomplete answers unresolved
  Given one question has an explicit answer and another question is blank
  When the agent reconciles the returned document
  Then only the answered question can supply new intended behavior
  And the blank question remains unresolved
  And its earlier recorded answer, if present, remains retained

Scenario: Detect changed choice meanings
  Given choice A had one meaning in the handed-over document
  And the returned document changes that meaning
  When the helper checks an answer selecting A
  Then reconciliation reports the changed option
  And no automatic rule update uses that answer

Scenario: Detect a stale candidate baseline
  Given a review receipt identifies a candidate hash
  And that candidate changed after handoff
  When the response is checked
  Then the affected candidate requires reconciliation
  And unrelated unchanged topics remain independently assessable

Scenario: Avoid duplicate answer application
  Given one resolved answer set already produced a candidate update
  When the same answer set is processed again
  Then no duplicate candidate version is created
  And no duplicate governance event is created

Scenario: Exclude drafts from gold answers
  Given matching candidate and published records exist
  When the query skill requests a gold answer
  Then every accepted gold result has published state and passing applicable recorded gates
  And no candidate record supplies approved intent

Scenario: Reject changed published bytes
  Given a published record has matching review and publication events
  When its bytes change without matching events
  Then retrieval reports the recorded gate failure
  And the record is not eligible as validated gold
```

Also check invalid IDs, path traversal, ambiguous answers, CLI/MCP parity, result limits, and exact read bytes.
Check that low-level searches without a scope still return valid candidates.
Run runtime tests and build the wheel for each implementation stage that changes those interfaces.
Initialize a separate workspace from the wheel and exercise the shipped review contract and skill.
Use one current topic as the first complete review-and-resume case.
Commit each completed stage after its required checks pass.

## Planning checks

This planning stage checks local links, source line bounds, Markdown whitespace, and the staged diff.
It performs no business execution, feature test, or package build.
Full ASD writing review remains pending.
