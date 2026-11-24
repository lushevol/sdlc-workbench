---
name: package-domain-experience
description: Package a successful task into a concise, provenance-bound domain experience packet with one minimal end-to-end recipe plus reusable procedures, scripts, fixtures, variable templates, and knowledge references.
metadata:
  short-description: Package successful work for reuse
---

# Package domain experience

Create a small reusable experience packet after a task has a supported successful outcome or when the user asks to promote an existing result.
Use the owning task and its evidence as the source. Preserve the task evidence and source identities before selecting reusable material.

## Workflow

1. Confirm the outcome, exact source revisions, commands, assertions, environment, and evidence limits. A passing command alone does not establish a business result.
2. Perform a short session retrospective. Record the goal, successful path, decisions, failures and recovery, and the reason the result can be reused.
3. Make one minimal end-to-end recipe the primary deliverable. Prefer one safe parameterized script when it can finish the whole task. Otherwise use a compact workflow or instructions. The recipe must cover inputs through the expected result. Keep extra scripts, fixtures, and prose as supporting material.
4. Inventory useful procedures, scripts, fixtures, variable names, URL references, recovery steps, and knowledge references. Classify each item as reusable, task evidence, private configuration, or disposable scratch output.
5. Select the smallest reusable set. Remove secrets, personal data, private tokens, machine paths, and environment-specific values. Replace them with named placeholders and variable templates.
6. Write one packet under `assets/experience/packets/<experience-id>/`. Use the packet contract in [packet-schema.md](references/packet-schema.md).
7. Link canonical knowledge records and wiki topics by identity, revision, and hash. Route new business intent through the existing knowledge workflow.
8. Assess whether the reusable result belongs in a shared Workbench asset. Read [workbench-promotion.md](references/workbench-promotion.md). Promote only generalizable guidance or tooling into `AGENTS.md`, canonical `.agents/skills/`, `core/skills/`, or project `scripts/` targets. Keep domain-specific material in the packet.
9. Record every shared-asset promotion in the packet manifest with its target, action, before and after hashes, source section, purpose, and checks. Apply the smallest compatible change and preserve existing instructions.
10. Run `scripts/validate_packet.py`, rebuild `assets/experience/index.yaml` with `scripts/rebuild_index.py`, and inspect the resulting diff.
11. Link the packet and its disposition from the owning task record. Retain selected decision evidence and necessary execution payloads there. Keep routine logs in ignored local storage under the [evidence and log boundary](../../../tasks/README.md#git-managed-evidence-and-local-logs).

Use `observed` for one supported successful run, `replayed` after a qualifying repeat, `reviewed` after applicable human review, and `retired` when the packet no longer applies.
Record the tested conditions and limits beside the reusable steps. Preserve failed replays and create a successor packet when a source or contract changes.

## Reuse

When a later task matches an indexed packet, read its applicability, prerequisites, variables, verification scope, and limits before using it.
Keep the new run's evidence separate and record whether the packet was reused, adapted, or rejected.

## Boundaries

- Keep canonical business meaning in `knowledge/records/` and the derived wiki. Packets link to those records instead of copying them.
- Keep secrets and live environment values in ignored workspace configuration.
- Treat synthetic or redacted fixtures as test inputs with stated limits.
- Do not execute external or destructive commands solely because a packet contains them. Follow the current task authorization.
- Do not infer a task, session, or successful outcome from filenames, dirty files, or timestamps.

The packet format is client-neutral. Codex, Claude Code, Copilot CLI, and VS Code Copilot consume the same canonical skill and packet paths through their existing adapters.
