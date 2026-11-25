# Package a successful experience

Use this mode for a requested reusable recipe with a supported successful outcome.
Keep useful failed or incomplete discoveries in their task or technical reference owner.
Never label an unsuccessful task as a successful packet to retain its lessons.
Apply [security and redaction](security-and-redaction.md) when selecting packet material.

## Build the packet

1. Confirm source revisions, assertions, observed outcome, environment, and evidence limits.
2. Record the goal, successful path, decisions, failures, recovery, and reason for reuse.
3. Select one minimal end-to-end script, workflow, or instruction set as the primary recipe.
4. Keep only supporting scripts, fixtures, variable definitions, knowledge links, and recovery steps.
5. Remove secrets and private values; preserve safe placeholders and their resolution rules.
6. Prepare a draft packet in review storage using [packet-schema.md](packet-schema.md).
7. Link canonical records and wiki topics by identity, revision, and hash without copying their meaning.
8. Assess shared guidance changes using [workbench-promotion.md](workbench-promotion.md).
9. Validate the draft and present its proposed destination, changes, checks, and limits for explicit human confirmation.
10. After confirmation, finalize the packet under `assets/experience/packets/<experience-id>/` and rebuild the index.
11. Link the packet, recorded confirmation, and actual checks from the owning task.

Validate a draft from the workspace root:

```sh
python3 .agents/skills/learn-from-sessions/scripts/validate_packet.py .workbench/experience/reviews/REVIEW_ID/packet --workspace .
```

After the human confirms the presented packet and it reaches its final destination:

```sh
python3 .agents/skills/learn-from-sessions/scripts/validate_packet.py assets/experience/packets/EXPERIENCE_ID --workspace .
python3 .agents/skills/learn-from-sessions/scripts/rebuild_index.py --root assets/experience
```

The validators check structure, references, evidence hashes, and supported promotion targets.
They do not establish successful business behavior or approval.
Use `observed` for one supported successful run and `replayed` for a qualifying repeat.
Use `reviewed` only after applicable human review and `retired` when the packet no longer applies.
Preserve failed replays and create a successor when the source or contract changes.

## Candidate decisions and reuse

Every unconfirmed packet remains a pending candidate, including packets from the current session.
Record candidate IDs, recipes, evidence, risks, limits, and the user's approve, reject, or revise decisions.
Follow the [human confirmation gate](../SKILL.md#human-confirmation-before-finalization).
Reuse an existing answer only when it explicitly confirms the exact presented changes.
A broad packaging request or continuation supplies no missing confirmation.

When a later task matches the index, read applicability, variables, prerequisites, and verification limits.
Keep the later run's evidence separate and record whether the packet was reused, adapted, or rejected.
Packet instructions supply no permission for external or destructive operations.
Use [reuse rules](reuse-rules.md) for replay, invalidation, and successor handling.
