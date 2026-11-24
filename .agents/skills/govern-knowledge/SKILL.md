---
name: govern-knowledge
description: Orchestrate evidence investigation, knowledge review, exact-byte transitions, audit, and publication for business-domain records.
---

# Govern business-domain knowledge

Use this parent for an end-to-end governance request. Invoke individual operations for narrower authorized work.
Read [the knowledge contract](../../../knowledge/README.md) before changing records.
Harness maintenance requires no business knowledge record. Follow [the scope rules](../../../tasks/README.md#scope) for mixed work.
Keep intended rules in knowledge. Keep actual implementation, deployment, execution, and conformance gaps in independent task gap Markdown and evidence.

## Route the work

| Step | Reusable operation | Required result |
| --- | --- | --- |
| Discover | [Retrieve evidence](../retrieve-knowledge-evidence/SKILL.md) | Exact sources, relevant records, evidence classes, and retrieval limits. |
| Establish scope | [Assess applicability](../assess-knowledge-applicability/SKILL.md) | Applicable intent versions, conditions, and separate actual-behavior limits. |
| Investigate and review | [Review claims](../review-knowledge-claims/SKILL.md) | Claim support, conflicts, confidence, actual reviewers, and remaining findings. |
| Resolve material questions | [Resolve questions](../resolve-knowledge-questions/SKILL.md) | Sourced answers or a living owner-question document. |
| Prepare | [Prepare a transition](../prepare-knowledge-transition/SKILL.md) | Final proposed bytes, required review evidence, and a prepared checkpoint. |
| Audit | [Record audit events](../record-knowledge-audit/SKILL.md) | New immutable events bound to the reviewed bytes. |
| Validate | [Check integrity](../check-knowledge-integrity/SKILL.md) | Final record, provenance, retention, and prepared-hash checks. |

Run only applicable operations. A missing answer blocks its affected meaning or transition; continue independent investigation.
After a content correction, repeat affected review, preparation, audit correction, and final validation.
Publication completes only when the required review and deterministic gates pass for the final bytes.
Keep accepted records separate from candidates. Report unresolved findings and publication state explicitly.

## Apply completed clarifications

Use [question resolution](../resolve-knowledge-questions/SKILL.md) to preserve answers and affected record links before handoff.
Use [record composition](../compose-knowledge-records/SKILL.md) when an answer requires a changed candidate or successor.
Then resume review, preparation, audit, and integrity checks above.
Clarification does not provide publication approval. A fix that restores an existing rule leaves its intended meaning unchanged.

## Reconcile the compiled wiki

After authorized canonical changes, use [llm-wiki](../llm-wiki/SKILL.md) to reconcile affected derived pages and source bindings.
Preserve candidate, contested, stale, and superseded qualifications. Check wiki freshness separately from canonical publication.
Derived pages and graph relationships cannot approve a rule or establish implemented behavior.

## Handoff

Return record IDs, versions, hashes, actual review evidence, new audit paths, validation results, and unresolved owner actions.
Keep knowledge review, ASD review, human approval, publication, wiki freshness, and behavior verification separate.
The runtime checks saved evidence. It does not authenticate reviewers, decide business correctness, or run this orchestration automatically.
