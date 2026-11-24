---
name: sync-release-knowledge
description: Reconcile a scoped release with intended knowledge through reusable change classification, candidate preparation, governance, wiki maintenance, and report reconciliation.
---

# Synchronize release knowledge

Orchestrate the selected release, baseline, environment, cohort, and as-of scope.
Keep knowledge intent, actual implementation, deployment, observations, publication, and release authorization separate.
Use one living task synchronization record and its independent gap document.
Read [the release operation contract](references/workflow.md) for identities, retries, completion, and report parity.
Use [the report reference](references/reporting.md) for the existing change-request form and canonical row inventory.
This procedure grants no deployment, production probe, external write, or message authorization.

## Route the work

| Step | Reusable skill | Required result |
| --- | --- | --- |
| Read release and existing knowledge evidence | [retrieve-knowledge-evidence](../retrieve-knowledge-evidence/SKILL.md) | Exact evidence inventory, starting hashes, and retrieval limits. |
| Establish intended scope and versions | [assess-knowledge-applicability](../assess-knowledge-applicability/SKILL.md) | Intent-backed applicability, with deployment claims assessed separately. |
| Classify every required row | [classify-knowledge-change](../classify-knowledge-change/SKILL.md) | Changed intent, supported no-change, maintenance, independent gaps, or unresolved intent. |
| Prepare supported changed records | [compose-knowledge-records](../compose-knowledge-records/SKILL.md) | Consistent candidate successors, stable IDs, and retained predecessor bindings. |
| Review claims and unresolved questions | [review-knowledge-claims](../review-knowledge-claims/SKILL.md), [resolve-knowledge-questions](../resolve-knowledge-questions/SKILL.md) | Evidence-backed review batch and actual owner answers. |
| Prepare exact final bytes | [prepare-knowledge-transition](../prepare-knowledge-transition/SKILL.md) | Current hashes, prepared content, and explicit pending or satisfied gates. |
| Record actual governance changes | [record-knowledge-audit](../record-knowledge-audit/SKILL.md) | New immutable events for reviewed bytes and real actors. |
| Check records and retrieval | [check-knowledge-integrity](../check-knowledge-integrity/SKILL.md), [evaluate-knowledge-retrieval](../evaluate-knowledge-retrieval/SKILL.md) | Actual deterministic checks plus separate semantic support findings. |
| Reconcile affected derived pages | [llm-wiki](../llm-wiki/SKILL.md) | Verified source bindings and truthful wiki maintenance outcome. |

Run only steps required by the row dispositions. Supported no-change rows do not require successor records or wiki rewrites.
Prepare all supported diffs and checks before requesting any required human decision. Review related changes as one batch.
Never transfer a predecessor's approval to changed bytes. A continuation request supplies no missing business answer or publication approval.

Return changed IDs/versions, supported no-change rows, gap links, validation, wiki freshness, report parity, and remaining owner actions.
Candidate preparation, publication, release suitability, and synchronization completion retain separate results.
