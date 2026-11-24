---
name: learn-domain-experience
description: Scan a bounded recent history window, skip unchanged sessions already scanned, and prepare reviewable experience candidates without packaging them.
metadata:
  short-description: Learn reusable experience from past work
---

# Learn domain experience from past work

Use this skill when the user asks to learn from prior sessions, consolidate repeated work, or discover reusable domain procedures.
It scans retained task records and explicitly supplied session exports. It does not assume access to chat history that the workspace has not retained.
Every session scan requires a bounded past duration. The default is one week (`7d`).

## Workflow

1. Read [history-scan.md](references/history-scan.md), then run `scripts/scan_history.py --past-duration 7d` against the workspace or selected task and session paths. Keep the output in ignored `.workbench/experience/` storage.
2. Inspect the listed task records, evidence indexes, source identities, execution results, and existing packets. Read claim-bearing files before drawing a pattern.
3. Group repeated procedures, inputs, variables, commands, outcomes, recovery steps, and knowledge references. Separate one-off workarounds, contradictory results, synthetic evidence, and unresolved questions.
4. Extract only patterns supported by at least one retained successful result. Prefer repeated or independently corroborated results when available. Preserve the conditions and limits of a single observation.
5. Prepare a review bundle under `.workbench/experience/reviews/<review-id>/` with candidate IDs, proposed minimal recipes, source tasks, evidence references, risks, limits, and `review_status: PENDING`.
6. Ask the user to approve, reject, or revise specific candidate IDs. A continuation request does not supply approval.
7. Only after explicit approval, invoke [package-domain-experience](../package-domain-experience/SKILL.md) for the selected candidates. Validate promoted packets and rebuild the project index after packaging.

The scan ends at a review decision. It never creates `assets/experience/packets/`, validates candidate packets, or rebuilds `assets/experience/index.yaml`.
The scan is a discovery aid. It does not establish business approval, production reachability, deployment state, or knowledge publication.

## Retention boundaries

- Read durable task evidence first. Use `.workbench/` session state only when the user supplies it or the task explicitly retains it.
- Keep source bytes, command outcomes, assertions, and limits in their owning task.
- Keep new business intent in the existing knowledge lifecycle.
- Keep secrets, private data, and environment-specific values outside promoted packets.
- Do not overwrite an existing packet when a later session disagrees. Preserve both results and review the packet status.
- Skip a session whose latest source fingerprint and scan window match the recorded scan state. Re-scan it after a source change or a changed duration.

## Client support

The skill is shared through `.agents/skills/` and works the same way in Codex, Claude Code, Copilot CLI, and VS Code Copilot. It requires no client-specific hook or command.
