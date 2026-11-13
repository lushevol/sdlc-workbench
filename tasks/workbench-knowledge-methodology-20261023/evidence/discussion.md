---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - This discussion proposes a procedure. It does not approve implementation or knowledge publication.
---

# Knowledge methodology discussion

The [user proposal](user-input.md#exact-user-input) requests discussion of raw sources, intermediate review, and a gold knowledge source.
The proposed procedure remains open for discussion.
This stage changes discussion records only. Its qualitative risk is low.

## Inspected baseline

Source revision: `53fd5d59af1ea8f4e5cb5d2581174af1edadfed0`.
The worktree was clean before recording this discussion.

| Claim | Evidence class | Source and locator | Limit |
| --- | --- | --- | --- |
| Raw evidence, candidates, and published knowledge already have separate responsibilities. | Documented design | [Knowledge standards](../../../knowledge/README.md#source-provenance-outside-knowledge), [workspace lifecycle](../../../docs/WORKSPACE_DESIGN.md#knowledge-format-and-governance) | Procedures still require agent reasoning and actual reviews. |
| The portal map labels its domain records as candidates without human approval. | Documented state | [Portal knowledge map](../../../knowledge/candidates/index.md#portal-knowledge-map) | This statement describes the index. It is not a full governance audit. |
| One living question document contains 60 entries across 11 domain records. | Documented review scope | [Current task state](../../../tasks/ui-test-coverage-20261022/05-knowledge-questions.md#current-task-state) | Entries include policy, ownership, and evidence questions. |
| Local knowledge search does not filter results by governance state. | Inspected implementation | [Operation schemas and file selection](../../../core/providers/knowledge.py#L53-L82), [search output](../../../core/providers/knowledge.py#L113-L125) | Source inspection only. No fresh retrieval execution was performed. |

## Proposed milestones

| Milestone | Agent responsibility | Human contribution | Completion evidence |
| --- | --- | --- | --- |
| Source baseline ready | Inventory sources, revisions, duplicates, missing items, and evidence limits. Preserve original bytes. | Identify authoritative sources when existing evidence cannot establish authority. | A bounded inventory links retained sources and exact revisions. |
| Review draft ready | Clean derived text. Organize topics. Reconcile terms. Trace claims to documents, code, and inspected tests. | Review a short summary, proposed rules, and unresolved decisions. | Each material claim has evidence, a clear qualifier, or an explicit question. |
| Reviewed scope ready | Preserve answers. Revise the draft. Show changed wording and measurable behavior criteria where applicable. | Resolve policy and authority questions. Review the exact proposed content within the agreed scope. | Material policy questions are resolved. Evidence limits remain explicit. Required reviews identify their actual scope. |
| Gold baseline published | Validate records. Record required reviews and publication events. Update navigation. | Supply required publication approval from the responsible authority. | Applicable gates pass for the exact published version. |

Cleaning applies to derived text. Original sources retain their bytes and conflicting statements.
Gold would provide canonical definitions with links across topic records.
It would distinguish intended behavior, inspected implementation, deployed versions, and observed execution.
An implementation gap can remain documented when intent is settled and its evidence limits are clear.

## Review experience

Keep the [existing living question document](../../../tasks/ui-test-coverage-20261022/05-knowledge-questions.md#review-and-refinement-loop).
Present bounded topic views within that scope. Preserve prior answers and unresolved questions.
Show a short summary, proposed rules, source links, contradictions, and decisions requiring human input.
The agent collects available engineering evidence. The responsible owner supplies missing business decisions and authority.
Clarification updates the draft. Publication approval applies to the exact version reviewed.
Record clarification authority from the answer source. Do not infer broader publication authority.

### Confirmed review format

The user selected [short narratives, answer options, and asynchronous document completion](../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261023/review-format-user-input.md#exact-user-input).
The [living review document](../../../tasks/ui-test-coverage-20261022/05-knowledge-questions.md) implements this format.
Ingestion continuation awaits the user's returned answers and instruction.
The user also requires [saved input as a high-priority reference](../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261023/reference-priority-user-input.md#exact-user-input).
The latest explicit clarification controls intended behavior within its stated scope. Conflicting sources remain available.

## Use and maintenance

Proposed gold answers would use published records with applicable scope and source freshness.
Draft exploration would remain available with explicit lifecycle labels and provenance.
A missing gold answer would remain a visible gap.
Changed source revisions would trigger review of affected claims and their dependent records.
Publication would proceed by bounded topic, so unrelated questions would not block every topic.

| Finding | Consequence | Owner | Proposed next action |
| --- | --- | --- | --- |
| Search includes draft records without an explicit lifecycle field in search results. | Consumers can mistake draft evidence for approved knowledge. | Workbench maintainer; individual unknown. | Agree separate retrieval behavior for gold answers and draft exploration before implementation. |
| The current question batch spans many topics. | Review requires substantial effort before each topic can become useful. | Agent for preparation; responsible domain reviewers remain scope dependent. | Present small review views inside the same living question scope. |
| Gold scope remains a discussion proposal. | Publication criteria cannot yet establish a complete domain baseline. | User for methodology direction; domain approval owners remain separate. | Choose one topic and agree its review criteria before applying the procedure. |

## Checks and limits

The installed checkout command completed workspace status discovery.
The unqualified `ai-sdlc` command was absent from the shell path. `.venv/bin/ai-sdlc` was available.
This stage does not change runtime code, domain knowledge, question batches, or governance history.
Document checks cover relative file links, Git whitespace, and the final diff.
Runtime tests and wheel builds are outside this discussion-only stage.
