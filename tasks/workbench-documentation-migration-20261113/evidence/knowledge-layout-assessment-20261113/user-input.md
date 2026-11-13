# User input: knowledge and evidence layout

- Source: user message in this Codex chat
- Date: 2026-11-13 (Asia/Singapore)
- Priority: high; intended scope is assessment of directory overlap and possible consolidation

## Exact user input

> /knowledge and /evidence/knowledge have some overlap, check if we can merge into one.

## Assessment boundary

Inspect current ownership, content, consumers, provenance, and retention constraints. Produce a concrete consolidation recommendation. This request does not authorize moving or deleting existing knowledge, source snapshots, or audit history.

## Folder-purpose follow-up

- Source: user follow-up in the same Codex chat
- Date: 2026-11-13 (Asia/Singapore)

> what the evidence folder for ?

## Documentation-directory follow-up

- Source: user follow-up in the same Codex chat
- Date: 2026-11-13 (Asia/Singapore)

> Alright, now let's look at something else: what is the docs directory for, and why are these files in there?

Scope: explain current documentation ownership, retained contents, consumers and overlap. This question does not authorize cleanup or relocation.

## Documentation optimization proposal

- Source: user follow-up in the same Codex chat
- Date: 2026-11-13 (Asia/Singapore)
- Priority: high; proposal and design scope

> how to optimize, what's your proposal

Scope: propose documentation organization, content ownership, retention and a staged migration. The earlier design-first instruction remains applicable; this request does not authorize implementing the proposed reorganization.

## Documentation and task ownership clarification

- Source: user follow-up in the same Codex chat
- Date: 2026-11-13 (Asia/Singapore)
- Priority: high; clarify ownership and refine the proposal

> what's the relationship of docs and tasks ? For a task the agent will create materials both in docs and tasks, but in tasks there is evidence folder, which confused me a ot .

Scope: explain the intended and observed ownership of documentation, task materials and supporting evidence; refine the design to avoid splitting one work scope across directories. This question does not authorize relocation, cleanup or implementation.

### Continuation

- Source: user follow-up in the same Codex chat
- Date: 2026-11-13 (Asia/Singapore)

> go on

Continue the ownership explanation and proposal refinement. No missing business answer or implementation approval is inferred from this continuation.

### Proposal recap

- Source: user follow-up in the same Codex chat
- Date: 2026-11-13 (Asia/Singapore)

> reconclude your proposal again

Scope: consolidate the existing proposed ownership and migration design for review; no implementation or relocation is requested by this recap.

## Living documentation model clarification

- Source: user follow-up in the same Codex chat
- Date: 2026-11-13 (Asia/Singapore)
- Priority: high; latest intended documentation model, superseding conflicting proposal assumptions

### Exact user input

```text
I think tasks is decentralized. These are incremental changes that migrate along a timeline. Docs, on the other hand, consists of overall, constant, real-time updated documentation. \
\
So for Docs, I don't want frequent additions of new documents. Instead, I want to maintain a series of documents that cover every lifecycle and every domain.
```

Scope: refine the design so tasks retain incremental work history and documentation provides a stable, comprehensive and continuously maintained current view. Avoid creating a new documentation page per work item or change. This clarification defines the proposal's direction; no relocation, deletion or runtime implementation is inferred.

## Documentation migration authorization

- Source: user follow-up in the same Codex chat
- Date: 2026-11-13 (Asia/Singapore)
- Priority: high; authorizes the stable-documentation migration and evidence-backed cleanup

### Exact user input

> Start the migration. During the process, please delete any documents and content that are outdated, conflicting, no longer in use, or no longer match the current state.

Scope: implement the reviewed living-documentation model, update its consumers, and remove obsolete or conflicting documentation after checking current ownership and use. Preserve unrelated work and required evidence, stable source identities and immutable audit history. Record authorized relocations/deletions, hashes, prior Git revisions, reasons and repaired active references under the existing retention rules. This authorization includes cleanup rather than merely indexing obsolete material.
