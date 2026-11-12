---
name: extract-knowledge-claims
description: Extract traceable claims, proposed topics, and consequential unknowns from inspected knowledge sources without inventing target intent.
---

# Extract knowledge claims

## Inputs

Use project questions, inspected evidence, current source selections, retained original revisions, and governing context.
For generated views, verify source-page hashes, policy/context bindings, ranges, and output mappings before use.
Reopen original passages with surrounding conditions when deriving meaning.

## Extract and classify

1. Read every cited range and relevant conditions, definitions, exceptions, and linked context.
   Missing attachments remain missing; their names cannot establish contents.
2. Create one row per important claim with [the claim worksheet](../ingest-knowledge/references/evidence.md#claim-worksheet).
   Record exact source locator, revision/hash/range, evidence class, support rationale, uncertainty, and owner question.
3. Separate documented intent, inspected implementation, deployment evidence, observed execution, inference, and unknowns.
   Use the shared [evidence classes](../ingest-knowledge/references/evidence.md#evidence-classes).
4. Group supported intent into a proposed topic map by project question.
   Keep source purpose, authority, proposal status, intended applicability, and unresolved conflicts visible.
5. For implementation questions, trace callers, providers, configuration, state, and failures at exact revisions.
   Inspect assertion setup, invocation, predicates, mocks, and imported keywords when evaluating behavior claims.
   Use the [feature](../ingest-knowledge/references/evidence.md#feature-worksheet)
   and [assertion](../ingest-knowledge/references/evidence.md#assertion-and-execution-worksheet) worksheets as applicable.
6. Route remaining material questions to [resolve-knowledge-questions](../resolve-knowledge-questions/SKILL.md)
   after investigating available sources.

Intended rules feed canonical knowledge.
Implementation, deployment, observations, and intent-to-reality differences feed task evidence and gaps.
A fix that restores intent leaves the intended rule unchanged.
Missing execution environments limit execution conclusions while static inspection can continue.
Names, comments, search hits, and a working link cannot substitute for the cited statement or predicate.

## Checkable output and stop conditions

Return supported claims, conditional inferences, a proposed topic map, and consequential unresolved findings.
Every important claim needs inspected support and an explicit evidence class.
Restrict partial claims to their actual support. Keep conflicting claims with separate sources and applicability.
Stop deriving a target rule when its meaning or authority requires an unanswered material policy decision.
Continue independent supported claims and disclose unavailable dependencies, excluded secrets, and omitted evidence.
This operation does not create governed records, grant publication, or establish business execution by itself.
