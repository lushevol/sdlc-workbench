---
name: package-domain-experience
description: Package a successful task into a concise, provenance-bound domain experience packet with reusable procedures, scripts, fixtures, variable templates, and knowledge references.
metadata:
  short-description: Package successful work for reuse
---

# Package domain experience

Create a small reusable experience packet after a task has a supported successful outcome or when the user asks to promote an existing result.
Use the owning task and its evidence as the source. Preserve the task evidence and source identities before selecting reusable material.

## Workflow

1. Confirm the outcome, exact source revisions, commands, assertions, environment, and evidence limits. A passing command alone does not establish a business result.
2. Inventory useful procedures, scripts, fixtures, variable names, URL references, recovery steps, and knowledge references. Classify each item as reusable, task evidence, private configuration, or disposable scratch output.
3. Select the smallest reusable set. Remove secrets, personal data, private tokens, machine paths, and environment-specific values. Replace them with named placeholders and variable templates.
4. Write one packet under `assets/experience/packets/<experience-id>/`. Use the packet contract in [packet-schema.md](references/packet-schema.md).
5. Link canonical knowledge records and wiki topics by identity, revision, and hash. Route new business intent through the existing knowledge workflow.
6. Run `scripts/validate_packet.py`, rebuild `assets/experience/index.yaml` with `scripts/rebuild_index.py`, and inspect the resulting diff.
7. Link the packet and its disposition from the owning task record. Keep full logs, screenshots, traces, and execution history in task evidence.

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
