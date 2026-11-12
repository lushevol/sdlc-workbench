---
name: evaluate-knowledge-retrieval
description: Check whether a knowledge answer covers the question and whether its claims follow from inspected sources, applicable versions, and stated evidence limits.
---

# Evaluate a knowledge answer

Input: the original question and scope, draft answer, claim register, inspected evidence, and applicability assessment.
Use this for query answers and independent checks of ingestion or governance retrieval.
Keep the evaluation read-only. It grants no publication, model compilation, or record-change permission.

## Check the answer against its evidence

1. Compare each requested question with the answer. Mark answered, partly answered, or unresolved, with the reason.
2. Follow every material claim to the exact cited source section and revision or hash.
   Search snippets, wiki summaries, and graph edges locate evidence. Reopen the underlying source before accepting support.
3. Check claim class: documented intent, inspected implementation, deployment evidence, observed execution, inference, or unknown.
   Keep OKF review, publication, and passing behavior separate. Inspect assertions and retained execution for behavior claims.
4. Check actor, environment, conditions, and requested date against [applicability](../assess-knowledge-applicability/SKILL.md).
   A newer candidate cannot silently replace an applicable published rule. UAT evidence cannot establish production execution.
5. Identify omissions, contradicted claims, unsupported additions, missing qualifications, and circular citations among derived pages.
   A bounded search with no match establishes only that result within the searched scope.
6. Use the [confidence rubric](../../../tasks/README.md#investigate-before-asking) for each investigated answer.
   Base confidence on direct support, authority, freshness, contradictions, and material evidence gaps.

## Return a checkable result

Return a concise table: question or claim, outcome, supporting locator, material limit, and needed correction or next evidence.
State the actual source and search scope. Do not invent percentages when the question inventory or denominator is unknown.
Use an independent reader when it improves a material decision. Disclose self-review when no independent reader participated.
Keep unresolved questions visible; route further investigation through [resolve-knowledge-questions](../resolve-knowledge-questions/SKILL.md).
Stop a claim's acceptance when its source is unread, stale, inapplicable, contradictory, or insufficient.
Passing this check establishes answer support within the stated scope. It supplies no missing human approval or business execution.
