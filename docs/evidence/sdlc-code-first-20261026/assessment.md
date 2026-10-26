---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Lifecycle control when code precedes requirements

**Recommendation: Support entry from existing implementation, then require evidence for each acceptance decision.**
This assessment proposes a route. It does not change current policy or implement workflow enforcement.
No immediate user action is required for this discussion.

- Input: [Exact user question](user-input.md#exact-wording), 26 October 2026.
- Assessor: Codex, with an independent read-only source investigation.
- Source baseline: `5092cd1a1288b5129e8e124697af35c30b2731c9`.
- Scope: Workbench lifecycle procedure. No business repository assessment or production recommendation occurred.
- Evidence inventory and checks: [Validation record](checks.json).

## Current control

| Claim | Class | Confidence and rationale | Evidence | Limit |
| --- | --- | --- | --- | --- |
| C1: Business intake currently precedes implementation. | Documented intent | HIGH: Direct instruction defines this order. | [Intake procedure](../../../.agents/skills/analyze-requirement/SKILL.md#start-intake-immediately) | No explicit code-first entry route appears in the inspected guides. |
| C2: Existing records can describe implemented changes. | Documented intent | HIGH: The template explicitly supports implemented changes. | [Change request purpose](../../../core/knowledge/templates/sdlc/change-request.md#purpose), [post-change baseline](../../../.agents/skills/impact-analysis/references/post-change-review.md#preserve-the-initial-baseline) | The post-change procedure assumes completed investigation and an intake baseline. |
| C3: Task readiness is assessed by agents. | Documented intent and inspected implementation | HIGH: Architecture and operation dispatch support this distinction. | [Core workflow](../../../ARCHITECTURE.md#core-workflow), [Runtime.call](../../../core/runtime.py#L56) | Dispatch checks grants and arguments. It does not enforce task readiness. |
| C4: Validation cannot establish business conformance. | Inspected implementation | HIGH: Assurance explicitly returns NOT_VERIFIED. | [Assurance limits](../../../core/assurance.py#L20), [baseline analysis](../../../core/assurance.py#L139) | This assessment did not execute behavior assurance or business tests. |
| C5: Three coverage directions already apply. | Documented intent | HIGH: The procedure explicitly defines mappings and denominators. | [Coverage procedure](../../../.agents/skills/verify-implementation/references/behavior-review.md#report-coverage) | Mapping completeness alone cannot establish equivalent behavior. |

## Proposed entry routes

Requirements-first work retains the current intake procedure.
Code-first work needs an explicit reconciliation route.
Both routes should use the same scoped acceptance evidence.

### Existing code supplied for review

1. Create any missing intake with the actual registration date. Link the original request and available intent sources.
2. Preserve existing frozen intake bytes. Record later decisions in the current change-review record.
3. Record repository identity, base and head revisions, local changes, and available implementation dates.
4. Separate observed behavior, sourced intent, proposed requirements, inspected assertions, and retained execution results.
5. Investigate existing knowledge and request sources before asking business questions.
6. Draft missing requirements and measurable Gherkin ACs. Mark code-derived statements as proposals until intent review resolves them.
7. Record the named next stage, evidence, readiness, blocked actions, resolution owner, and next action.

Record unavailable historical intent or baseline evidence as unknown.
Do not invent earlier approval dates or imply that retrospective documentation governed the original coding decision.
Code supplied before intake remains valid implementation evidence.
Its existence establishes no business acceptance.

### Deliberate exploration before complete ACs

This route would extend current policy.
Record a goal, scope, accountable owner, constraints, and existing authorization before exploration begins.
Assess readiness for that bounded exploration stage separately.
Full acceptance criteria can follow the experiment.

The proposed route must define which coding actions exploration permits.
Unresolved rules can still block actions that depend on them.
`READY_WITH_LIMITS` retains its current meaning: intake evidence collection only.
A proposal cannot silently authorize implementation through that status.

## Proposed acceptance controls

| Decision | Required evidence | Action when evidence is missing |
| --- | --- | --- |
| Establish intended behavior | Existing authoritative sources, investigated conflicts, and recorded required review of proposed intent | Keep affected ACs proposed. Continue authorized investigation. |
| Reconcile code with intent | Exact source comparison, old/new/intended results, and justified behavior boundaries | Record missing, contradictory, unsupported additional, or unknown behavior. |
| Establish test coverage | AC-to-test, AC-to-code, and change-to-test matrices with separate inventories | Keep unmapped predicates and changes visible. |
| Claim verified behavior | Reviewed intent, inspected assertions, and matching retained execution for applicable conditions | Keep affected behavior unverified. |
| Assess release suitability | Applicable requirement, review, test, deployment, and operational evidence | Record the recommendation and limits. Keep deployment authorization separate. |

Source inspection, diff inspection, and authorized observation tests can collect intake evidence before intent is settled.
[Formal downstream review](../../../.agents/skills/code-review/references/integrations.md#workbench-task-scope) still requires `READY` for its named stage.
Investigation results cannot settle an unresolved business rule.
Reuse retained executions only when assertions, revisions, fixtures, and conditions support the current ACs.
Rerun affected cases when relevant bindings or expectations change.

Keep implementation status, intent review, execution outcome, and acceptance disposition separate.
For example, code can exist while intent review remains pending and business verification remains unestablished.
These descriptions propose no new runtime status values.

If code differs from intended behavior, correct the code or obtain an evidenced requirement change.
Preserve the prior requirement version and decision history.
Do not rewrite ACs solely to make existing implementation pass.

## Coverage and approval boundaries

Use the existing [coverage rules](../../../.agents/skills/verify-implementation/references/behavior-review.md#behavioral-equality-target).
Report each required predicate and meaningful change, including relevant unchanged implementation.
Show definition coverage, inspected assertion coverage, conformance, and passing execution separately.
An unknown AC inventory produces unknown acceptance coverage.
A known empty denominator produces N/A. Neither result establishes complete coverage.

Important requirements and decisions retain their [human publication review](../../../knowledge/README.md#review-gates).
Readiness, clarification, knowledge publication, verified execution, and deployment authorization remain separate decisions.

## Material gap and next action

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| The inspected procedure lacks explicit entry without prior requirements. | [Current order](../../../.agents/skills/analyze-requirement/SKILL.md#start-intake-immediately), [post-change assumptions](../../../.agents/skills/impact-analysis/references/post-change-review.md#preserve-the-initial-baseline) | Agents could reject supplied code or infer business intent from it. This is a procedural risk inference. | unknown | If adopted, document the reconciliation route across intake, task guidance, templates, and verification instructions. |
| Task phase transitions have no executable enforcement. | [Architecture boundary](../../../ARCHITECTURE.md#core-workflow), [operation dispatch](../../../core/runtime.py#L56) | Current readiness depends on agent procedure. | unknown | Describe current limits. Add machine enforcement only through separately scoped work. |

No material clarification blocks this design answer.
Policy adoption and any future implementation remain outside this assessment.
The qualitative risk of these evidence-only additions is low.
Existing runtime, task guidance, schemas, and business behavior remain unchanged.
