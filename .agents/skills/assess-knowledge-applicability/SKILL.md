---
name: assess-knowledge-applicability
description: Select supported knowledge versions for an actor, environment, condition, and date while separating intended applicability from actual rollout.
---

# Assess knowledge applicability

Input: requested behavior scope, actor, environment, conditions, date or revision, and candidate predecessor or successor records.
Output: an applicability table with selected IDs, versions, hashes, intent evidence, qualifications, conflicts, and missing decisions.
This operation explains applicability. It does not promote records or change rules.

## Assess

1. Read each relevant record, its predecessors and successors, review state, authority evidence, and intended applicability sources.
2. Compare the requested actor, environment, conditions, and rule date against explicit intent evidence.
3. Preserve competing rules with their separate source dates and scopes. Publication alone does not establish universal applicability.
4. Keep newer candidates qualified. Do not replace a supported published predecessor merely because a candidate has a newer version.
5. For actual behavior, inspect separate gap documents, exact implementation, deployments, configuration, assertions, and retained observations.
6. For partial rollout or rollback, describe each evidenced component combination and its limits.

Keep rule applicability, deployment time, observation time, and documentation time separate. Unknown dates remain unknown.
Release ordering, passing tests, and working code cannot establish intended policy.
Missing deployment evidence limits actual-behavior claims. It does not erase an explicit target requirement.
The knowledge provider does not automatically resolve as-of, environment, or applicable published versions.
Do not report an automatic applicability resolver or environment filter as executed.

## Checkable result

For each requested scope, identify the applicable record or explain why selection remains unresolved.
Record source authority, selection rationale, lifecycle qualifications, applicable conditions, and independent actual-behavior evidence limits.
Link material intent-to-reality differences to their independent gap records.
When intent evidence cannot select a rule, name the missing source or owner decision and leave the affected scope unresolved.
Use [question resolution](../resolve-knowledge-questions/SKILL.md) when that missing answer blocks authorized work.
