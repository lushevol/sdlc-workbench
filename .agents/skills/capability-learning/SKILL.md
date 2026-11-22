---
name: capability-learning
description: Retrieve scoped Workbench capabilities and reconcile reusable engineering discoveries at task checkpoints. Use for new or changed contracts, business rules, repeatable workflows, and verified operational lessons.
---

# Capability learning

At task entry, search the central registry with `ai-sdlc --workspace . learning list --query TERMS`.
Use `learning use ID --scope JSON` for the exact task. Inspect its linked sources, skills and permission requirements.

During the task, keep evidence in its existing owning location. Prefer an exact source revision, targeted assertion, or sanitized receipt.
Record material observed behavior separately from interpretation. Keep secrets, personal data, and raw responses out of learning records.

At a meaningful checkpoint or handoff, reflect on the completed work. Skip incidental mentions and repetitive work.
For each reusable claim, find related entries first. Select the smallest change to their existing responsibility and scope.
Classify one primary category. Keep facts, conclusions, and verification method separate.
For business intent or entitlement policy, use [govern-knowledge](../govern-knowledge/SKILL.md).

Write a discovery JSON in ignored workspace storage. Pass it to `learning checkpoint --input PATH`.
Use the [learning guide](../../../docs/CAPABILITY_LEARNING.md) for the input contract and status handling.
The command validates evidence references and reconciles against the current revision.
It can promote an allowlisted independent result. Retain conflicts and unresolved discoveries for review.
Reuse an existing skill when its responsibility fits. Reference learned rules by capability ID and scope.
When a distinct procedure needs a skill, propose its canonical `SKILL.md` in the owning task.
Submit the proposed capability with its `skill_id` and independent review evidence.
Review and test changes to instructions or scripts through the workspace's skill authoring procedure before promotion.

If hooks are unavailable, run the same checkpoint from the living record.
If learning fails, record the blocker briefly and continue authorized engineering work.
Mention promoted changes and material unresolved findings in the task handoff.
