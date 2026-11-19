---
name: learn-domain-experience
description: Scan retained past task and session materials, identify repeated evidence-backed workflows, and extract concise domain experience packets for later reuse.
metadata:
  short-description: Learn reusable experience from past work
---

# Learn domain experience from past work

Use this skill when the user asks to learn from prior sessions, consolidate repeated work, or discover reusable domain procedures.
It scans retained task records and explicitly supplied session exports. It does not assume access to chat history that the workspace has not retained.

## Workflow

1. Read [history-scan.md](references/history-scan.md), then run `scripts/scan_history.py` against the workspace or selected task and session paths. Keep the output in ignored `.workbench/experience/` storage.
2. Inspect the listed task records, evidence indexes, source identities, execution results, and existing packets. Read claim-bearing files before drawing a pattern.
3. Group repeated procedures, inputs, variables, commands, outcomes, recovery steps, and knowledge references. Separate one-off workarounds, contradictory results, synthetic evidence, and unresolved questions.
4. Extract only patterns supported by at least one retained successful result. Prefer repeated or independently corroborated results when available. Preserve the conditions and limits of a single observation.
5. Prepare candidate packets with [package-domain-experience](../package-domain-experience/SKILL.md). Use `observed` when one result supports the packet and `replayed` or `reviewed` only when the evidence supports that state.
6. Validate packets and rebuild the project index. Link each promoted packet to the source tasks and record rejected or evidence-only material in the current maintenance record.

The scan is a discovery aid. It does not establish business approval, production reachability, deployment state, or knowledge publication.

## Retention boundaries

- Read durable task evidence first. Use `.workbench/` session state only when the user supplies it or the task explicitly retains it.
- Keep source bytes, command outcomes, assertions, and limits in their owning task.
- Keep new business intent in the existing knowledge lifecycle.
- Keep secrets, private data, and environment-specific values outside promoted packets.
- Do not overwrite an existing packet when a later session disagrees. Preserve both results and review the packet status.

## Client support

The skill is shared through `.agents/skills/` and works the same way in Codex, Claude Code, Copilot CLI, and VS Code Copilot. It requires no client-specific hook or command.
