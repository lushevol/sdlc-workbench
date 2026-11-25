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

> **Human confirmation must precede finalizing extracted learning.**
> The [latest clarification](#human-confirmation-clarification) requires a visible proposal and explicit confirmation.
> The skill and governing procedures now include that gate.
> Follow-up checks and an isolated unconfirmed scenario passed.
> The scenario retained candidate drafts and left active assets unchanged.
>
> **The initial consolidation passed its baseline checks.**
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
The initial consolidation was committed as `502856727`.

## Human confirmation clarification

Source: this Codex chat, 25 November 2026.

> one thing that add human confirmation before you finalize the learning to workbench, don't do in silence.

This clarification requires visible human confirmation before applying extracted learning to reusable Workbench assets.
Preparation, evidence retention, draft scripts, and offline checks may continue before confirmation.
Present concrete proposed changes, destinations, evidence, checks, risks, and limits for review.
Record confirmation against the reviewed scope before finalization.
Silence, continuation, broad learning requests, and automated checks cannot supply that confirmation.

The worktree was clean at this follow-up's entry.
Baseline: consolidation commit `502856727`.
Scope includes the skill and current project procedures; existing runtime operations remain unchanged.
Risk is moderate because registry checkpoint commands can activate allowlisted discoveries automatically.
Inspect that behavior and keep pre-confirmation checkpoint submissions candidate-only.
This instruction authorizes the confirmation-rule update itself.
The new confirmation requirement applies to extracted learning finalization.
The skill now separates candidate preparation from finalization.
The gate covers scripts, workflows, knowledge, preferences, instructions, domain references, packets, indexes, and active registry rules.
Specific candidate confirmation must precede finalization, including delegated extraction.
Only exact presented changes can reuse recorded confirmation.
Material revisions need confirmation of their updated proposal.

The registry guidance requires `WORKBENCH_LEARNING_PROMOTION=0` for checkpoint and promotion operations.
Confirmed manual promotion retains existing approval and independent verification requirements.
The underlying runtime and its default switches remain unchanged.
The existing candidate from the initial consolidation remains unpromoted.
Its linked skill changed; revalidate the candidate and present its current proposal before any future promotion.

The 11 capability-learning tests and 24 workspace-layout tests passed with no failures or skips.
These include candidate-only capture for an otherwise auto-eligible discovery.
Both changed skill entry points passed skill validation.
The 170 inspected local links resolved, including links to the confirmation gate.
Workspace validation remained `VALID`, with 119 documents and no findings.
The updated wheel installed outside this checkout and initialized a valid empty workspace.
It preserved all 14 session-learning files and six changed guides exactly.
See the [wheel check](evidence/confirmation-gate-wheel-smoke.json) and [follow-up verification](evidence/confirmation-gate-verification.json).

This guidance-only update did not change runtime implementation, schemas, or helper code.
The earlier full-suite result remains bound to the initial consolidation's source hashes.
The new confirmation gate is an agent procedure using the existing runtime promotion switch.
Direct commands outside that procedure can still enable automatic promotion.
The [isolated scenario](evidence/confirmation-gate-input.json) completed with no human confirmation available.
The agent prepared three candidates, an exact patch, evidence, checks, risks, and limits.
It retained an unanswered decision table and an empty confirmed scope.
All four original input hashes remained unchanged.
No active extracted script or experience packet was installed.
The [assessment](evidence/confirmation-gate-assessment.json) passed six criteria; the draft checker passed all 11 checks.
The [result archive](evidence/confirmation-gate-result.tar.gz) preserves the inspected output.
This synthetic scenario does not establish universal compliance or live client behavior.
The requested procedure update is complete.
