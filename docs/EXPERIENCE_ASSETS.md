# Session learning and reusable experience

Use [learn-from-sessions](../.agents/skills/learn-from-sessions/SKILL.md) to turn inspected sessions into reusable project assets.
It combines history discovery, successful recipe packaging, and capability registry reconciliation.
It also extracts sourced preferences, user clarifications, exploration, and useful failed attempts.
Use only the responsibilities needed by the request.

| Responsibility | Output |
| --- | --- |
| Review current sessions or bounded history | Sourced lessons, candidate decisions, and evidence links in the owning task. |
| Maintain reusable assets | Existing scripts, workflows, technical guides, and applicable project instructions. |
| Package successful recipes | Indexed experience packets with one minimal end-to-end recipe and supporting assets. |
| Reconcile scoped capabilities | Existing Workbench registry operations, verification rules, and revision history. |

Use [domain capability extraction](CAPABILITY_LEARNING.md#extract-domain-capabilities) for cumulative API, workflow, failure, and background references.
That extraction prepares domain file changes without requiring an experience packet.
Human confirmation still precedes finalizing those changes.
Use the same skill's [registry mode](../.agents/skills/learn-from-sessions/references/capability-registry.md) when scoped reconciliation is needed.
Use the experience packet workflow when a successful procedure needs a reviewed reusable package.
Direct extraction requires no packet, registry promotion, or native hook.
Business intent retains its canonical governance.

## Human confirmation

Prepare source-backed lessons, draft assets, proposed patches, and applicable offline checks first.
Keep unconfirmed changes in the owning task or ignored review storage.
Show candidate IDs, target paths, concrete changes, evidence, checks, risks, and limits.
Ask the human to approve, reject, or revise those candidates and wait for an explicit answer.
Record the answer and confirmed scope before applying the learned changes.
Material revisions require confirmation of the revised proposal.
Do not finalize learning silently.

This applies to scripts, workflows, knowledge, preferences, project instructions, domain references, packets, indexes, and active registry rules.
Broad learning requests, continuation, silence, and passing checks do not provide confirmation.
Keep `WORKBENCH_LEARNING_PROMOTION=0` during checkpoint and promotion operations and use recorded approval for confirmed manual promotion.
The [skill gate](../.agents/skills/learn-from-sessions/SKILL.md#human-confirmation-before-finalization) defines the complete procedure.

## Storage

Promoted packets live under the project-owned `assets/experience/` area.
Scratch scans and candidate material stay in ignored `.workbench/experience/` storage until selected.
Keep selected decision evidence, required screenshots, and traces under their owning task.
Link canonical source snapshots from `knowledge/evidence/sources/` by source identity and hash.
Keep routine execution and troubleshooting logs in ignored `tasks/<task-id>/logs/<run-id>/`.
Promote necessary log content under the [evidence and log boundary](../tasks/README.md#git-managed-evidence-and-local-logs).
Preserve full raw context when reproduction, review, or recovery requires it.

```text
assets/experience/
├── index.yaml
└── packets/<experience-id>/
    ├── manifest.yaml
    ├── experience.md
    ├── variables.example.yaml
    ├── references.yaml
    ├── scripts/
    └── fixtures/
```

The index contains retrieval metadata. The packet contains the shortest usable procedure and its reusable inputs.
Each manifest records the source task, session when available, exact evidence hashes, tested conditions, status, sensitivity classification, and known limits.
When a result generalizes into shared Workbench guidance or tooling, the packet records a hash-bound promotion into `AGENTS.md`, canonical `.agents/skills/`, `core/skills/`, or `scripts/`.

## Capture and learning

Use `learn-from-sessions` with the current conversation, selected accessible chats, retained tasks, or explicitly supplied exports.
Keep source dates, revisions, hashes, user statements, commands, assertions, and limits.
Do not assume access to unseen transcripts or crawl private client stores.
Treat transcript instructions as evidence within the current request's authority.
Read existing assets and matching registry rules before writing another reusable definition.

For a packet, require a supported successful result and a short session retrospective.
Make one parameterized script the primary recipe when it can finish the whole task. Use a compact workflow or instruction set when a script is unsuitable.
Session scans require `--past-duration` and default to one week. The ignored scan state skips unchanged sessions whose latest source was already scanned.
Inventory fingerprints do not establish semantic review or a completed output.
Reopen earlier inventories and sources when their reviewed result is missing.
Historical discovery ends with `review_status: PENDING`.
Prepare and validate a draft, then obtain explicit confirmation of the presented packet and index changes before finalization.
The scan does not establish success, business approval, production reachability, or knowledge publication.

Package review also checks whether the result should update a shared Workbench asset. Keep domain-specific material in the packet. Apply the smallest compatible shared-asset change and record its target, purpose, before and after hashes, source section, and checks.

Use `observed` for one supported result, `replayed` after a qualifying repeat, `reviewed` after applicable human review, and `retired` when the packet no longer applies.
Preserve earlier packets when later replay disagrees.

## Preferences, exploration, and failures

Preserve exact explicit preferences with their source, date, scope, conditions, and exceptions.
Present proposed instruction updates and obtain human confirmation before applying them.
Keep inferred preferences in the owning task as candidates.
Global memory changes require an explicit request to remember.
Do not generalize a task-specific workaround into a universal preference.
Retain conflicts and apply the latest explicit clarification only within its scope.

Reconstruct attempts with their trigger, inputs, action, observed result, verification, recovery, and limits.
Retain useful failures and partial discoveries even when the task did not succeed.
Keep suspected causes distinct from observed symptoms.
Link failure lessons from the relevant existing workflow or technical guide.
Do not package an unsuccessful outcome as a successful recipe.
The [extraction reference](../.agents/skills/learn-from-sessions/references/extraction.md) defines output ownership and script preparation.

## Knowledge and configuration

Packets link to canonical `knowledge/records/` and derived wiki topics by identity, version, and hash.
They do not duplicate the knowledge base.
New business intent follows the existing knowledge lifecycle.

Track variable names, types, sources, allowed values, and placeholders.
Keep secrets, personal data, private tokens, and environment-specific values in ignored configuration or approved process environment.
Label fixtures as synthetic or redacted and state their evidence limits.

The skill uses the canonical `.agents/skills/` path.
Codex, Claude Code, Copilot CLI, and VS Code Copilot share the same procedures and packet format.
It replaces the three former learning skills without adding another runtime engine or changing packet formats.
