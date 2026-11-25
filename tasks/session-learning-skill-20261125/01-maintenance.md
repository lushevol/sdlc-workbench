---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
---

# Consolidate session learning skills

> **The consolidated skill is implemented and verified.**
> Use [`learn-from-sessions`](../../.agents/skills/learn-from-sessions/SKILL.md) for the three combined responsibilities and session extraction.
> All 1,166 runtime tests passed without skips; the wheel and isolated trial passed.
> See [verification.json](evidence/verification.json) for commands, source hashes, and limits.
>
> **Registry promotion and formal writing review remain pending.**
> The [registry checkpoint](evidence/learning-checkpoint.json) is a candidate, not an active learned rule.
> The skill itself is available without that promotion.
> A named registry review authority is unknown.

## User input and scope

Source: this Codex chat, session `01a20d4a-d5a0-7371-9061-bca9ad6818f9`.

Original request, 24 November 2026:

> I need a skill which learn from sessions and extract scripts, workflows, knowledge from my input my preference and agent exploration and trying, how ?

Clarification, 25 November 2026:

> Do these existing skills have an overlap? I want to combine the last three and add the capability of the new skill. Can we make a new skill with clear responsibilities out of this?

The preceding answer listed these skills in order:

1. `domain-capability-extractor`
2. `learn-domain-experience`
3. `package-domain-experience`
4. `capability-learning`

The last three are the consolidation scope.
Create `learn-from-sessions` with explicit responsibilities and reuse existing runtime operations.
Include sourced preferences, user clarifications, exploration, failures, scripts, workflows, and knowledge.
Keep `domain-capability-extractor` responsible for domain integration references.
Do not modify global memory or infer publication and execution approval.

## Baseline and affected scope

The worktree was clean at entry.
Baseline revision: `b3df0435d023330eca456414ad7b25b43935a68b`.
Inspect skill assets, their consumers, generated workspace distribution, tests, hooks, and current guides.
Risk is moderate because skill paths appear in runtime guidance and distribution tests.
Preserve existing packet formats, scan state, registry operations, and retained evidence identities.

## Work and verification

The three former skills share retrospective review, provenance, candidate decisions, and promotion guidance.
Their distinct operations are history scanning, successful recipe packaging, and registry reconciliation.
The new skill owns these operations plus sourced preferences and useful exploration attempts.
The domain extractor retains cumulative integration contracts, workflows, and knowledge.

The local `.venv/bin/ai-sdlc` provides the runtime despite the missing shell PATH entry.
Native hooks are bound to this record.
The scoped registry search returned no matching entries.

The replacement entry point and focused references are complete.
All existing helper, packet, reuse, and redaction resources moved into the replacement skill.
The three former skill entry points were retired after replacement validation.
Current guides, ADO guidance, native hooks, and generated discovery now target the replacement.
Source hashes and retirement mappings are retained in [consolidation.json](evidence/consolidation.json).

Automatic approval review rejected retiring old skills before a replacement existed.
The safer sequence creates and verifies the replacement before retirement.
No source removal occurred during the rejected operation.

The first suite encountered 39 sandbox errors while binding local test servers.
Its original result remains in [unit-suite-sandbox-failure.json](evidence/unit-suite-sandbox-failure.json).
The complete rerun enabled local sockets and the installed Node integrations.
All 1,166 tests passed with zero errors, failures, or skips.
The retained [suite output](evidence/unit-suite-passed.txt.gz) and [verification record](evidence/verification.json) bind the result to candidate source hashes.

The first wheel check exposed three remaining packet reference files under a retired folder.
That [failure](evidence/wheel-initialization-failure.json) led to their complete relocation.
The final [wheel check](evidence/wheel-smoke.json) verified all 14 replacement files and empty catalogs.
It confirmed retired skills, runtime source, and project task history were absent.
Existing dependency packages were reused; the runtime came from the installed wheel outside this checkout.

An independent agent executed one [synthetic request](evidence/forward-input.json).
The [assessment](evidence/forward-assessment.json) inspected eight criteria and seven passing script tests.
The trial preserved scoped preferences, meaningful failures, and source bytes.
It produced a reusable script and retained uncertainty around an HTTP 403.
Its [output archive](evidence/forward-result.tar.gz) preserves the inspected artifacts.
One synthetic trial does not establish general reliability or live business behavior.

Skill validation passed.
All 171 inspected local links resolved.
All 15 historical source bindings matched their prior Git bytes.
Workspace validation reported `VALID`, with 119 documents and no findings.
Diff checks passed.
The reusable workflow discovery remains `REVIEW_REQUIRED`; no registry rule was promoted.

## Documentation and handoff

Updated [agent guidance](../../AGENTS.md#learn-reusable-capabilities) and [task procedures](../README.md#promote-reusable-domain-experience).
Updated [experience documentation](../../docs/EXPERIENCE_ASSETS.md) and [registry guidance](../../docs/CAPABILITY_LEARNING.md).
Updated [hook guidance](../../docs/HOOKS.md) and [workspace ownership](../../docs/WORKSPACE_DESIGN.md#folder-construction).
The separate domain extractor retains integration library ownership.

Use `$learn-from-sessions` for current sessions, selected history, successful packets, or scoped registry work.
Read only the references needed by the requested responsibility.
Formal ASD writing review, Windows behavior, and live agent dispatch were not established.
No business publication, global memory update, deployment, or external message occurred.
The authorized consolidation is complete; the scoped commit follows staged diff review.
