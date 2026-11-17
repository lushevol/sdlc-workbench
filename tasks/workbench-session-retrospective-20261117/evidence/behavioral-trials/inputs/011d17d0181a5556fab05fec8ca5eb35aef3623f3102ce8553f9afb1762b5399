---
name: review-knowledge-claims
description: Assess claim support, authority, freshness, consistency, and completeness against inspected sources, with recorded review scope and limits.
---

# Review knowledge claims

Input: selected claims or proposed record bytes, inspected sources, applicability scope, and the requested review purpose.
Output: a claim register, supported conclusions, unresolved findings, confidence rationale, and actual reviewer evidence when review occurs.
The review result does not itself publish records or verify business execution.
Use [the knowledge contract](../../../knowledge/README.md) and shipped templates when reviewing governed record changes.

## Review

1. Use [the claim worksheet](../ingest-knowledge/references/evidence.md#claim-worksheet) for each material claim.
2. Read each cited range and necessary surrounding context. Explain which statement or predicate supports the claim.
3. Check source authority, revision, hash, freshness, conditions, exceptions, consistency, completeness, and applicable conflicting evidence.
4. Keep documented intent, inspected implementation, deployment, execution, inference, and unknown claims distinct.
5. Compare intended meaning with proposed wording. Identify unsupported additions, omitted conditions, contradictions, and unreviewed scope.
6. Make changed requirements measurable through sourced Gherkin conditions, actions, observable results, and explicit assertions.

A link establishes a destination, not semantic support. Filename patterns and symbol names cannot establish meaning.
An omitted rule does not establish its prohibition. Code can answer implementation questions while leaving policy unresolved.
Keep an intended rule unchanged when code differs or a fix restores conformance. Record actual differences in independent task gaps.
Use [change classification](../classify-knowledge-change/SKILL.md) when deciding whether new evidence changes intent.

## Record the result

Give supported answers an evidence-based confidence level and rationale using [the investigation rubric](../../../tasks/README.md#investigate-before-asking).
For each unresolved finding, record evidence, consequence, owner, and next action. Mark an unavailable owner as `unknown`.
Preserve contradictory and failed evidence. Restrict partially supported claims to the supported scope.
When recording governance findings is authorized, use `knowledge/evidence/findings/` and the shipped finding template.
Read-only reviews return findings without writing or changing records.
Record actual semantic reviewer identities, review times, reviewed hashes, and evidence limits when that review occurs.
Keep semantic review time separate from pending ASD review fields. Generated text and validator results supply no human approval.
Changed content cannot inherit an earlier review or approval without the required new review against its final bytes.

Stop the affected conclusion or transition when material support or required review is missing.
Use [question resolution](../resolve-knowledge-questions/SKILL.md) for remaining policy questions after available evidence is investigated.
