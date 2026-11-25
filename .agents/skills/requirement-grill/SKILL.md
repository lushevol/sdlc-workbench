---
name: requirement-grill
description: Assess ambiguous or incomplete business requirements before impact analysis or implementation, using exact Workbench sources and focused owner questions.
metadata:
  short-description: Clarify requirements with evidence and focused questions
---

# Requirement Grill

Use this skill when missing rules, competing interpretations, or incomplete acceptance criteria can change a business task's next phase.
It complements [analyze-requirement](../analyze-requirement/SKILL.md), which owns intake, entry routes, records, and phase readiness.
Use [resolve-knowledge-questions](../resolve-knowledge-questions/SKILL.md) when answers must update governed intent.
Read-only requests return findings and questions without changing task or knowledge records.

## Start with the owning task

1. Reuse or create the [owning task](../../../tasks/README.md#scope) before authorized discovery. Preserve exact input, source, date, prior answers, and scope.
2. During initial investigation, use the living intake. After intake completion, preserve its bytes and update the current stage record.
3. Extract the requested delta: each predicate added, removed, or changed. Retain unchanged predicates with exact current-behavior sources.
4. Identify the named next phase and assess only uncertainties that can change it.

Harness maintenance uses the lightweight route. Supplied implementation does not establish prior intent or approval.
For [bounded exploration](../../../tasks/README.md#start-bounded-exploration), assess the authorized experiment's question, constraints, outcomes, and stop condition.
Product criteria can remain open when they cannot change that experiment or its decision.

## Completeness gate

Extract explicit criteria from the request, linked design, and applicable decisions. Preserve their actual draft, review, and approval states.
Identify material missing cases of added or changed rules. Do not reopen unrelated, unchanged predicates because a narrow request summarizes them imprecisely.
Describe each criterion through actor or input, action, observable result, and scope.
Include negative, boundary, error, audit, or observability conditions only when relevant to the supported behavior.
Use measurable Gherkin through the existing intake contract. Keep canonical test definitions in `06-test-cases.md` and link them instead of duplicating them.

Keep this ledger in the owning intake or current stage record:

| Criterion or gap | Testable statement or missing rule | Completeness | Evidence or owner decision | Consequence |
| --- | --- | --- | --- | --- |
| Existing criterion or stable gap ID. | Actor, action, result, scope, or unresolved part. | One label below. | Exact source or unresolved owner. | Affected phase, case, contract, or proof. |

Use these local completeness labels, separately from authority, readiness, or execution:

- `EXPLICIT`: the request states the complete criterion. Explicit wording alone does not establish approval.
- `EVIDENCE_COMPLETED`: an applicable authoritative source establishes the previously absent rule.
- `PARTIAL`: the outcome exists, but a material condition, scope, data rule, or failure result remains unresolved.
- `MISSING`: no target criterion establishes a material case required by the requested change.

For `PARTIAL` and `MISSING` criteria, investigate in this order:

1. Inspect the current request, linked design, prior owner answers, and applicable decisions.
2. Read relevant knowledge indexes, canonical records, applicable versions, and cited originals using [knowledge retrieval](../retrieve-knowledge-evidence/SKILL.md).
3. Discover available resources with `ai-sdlc --workspace PATH status`. Inspect operation schemas and grants before configured calls.
4. Use exact local sources when tools are unavailable. Derived wiki pages provide discovery; reopen their canonical sources before relying on intent.
5. Inspect implementation and test assertions when they can resolve current behavior or expose a material coverage gap.

Follow [repository freshness](../../../AGENTS.md#repository-freshness-before-codebase-actions) before code inspection.
Use registered checkout locations and exact comparison refs. No particular source host, `repos/` layout, graph, index, or model endpoint is required.
Tool coverage and empty search results cannot establish that a rule or dependency is absent.

Reassess gaps after source review. Code and tests cannot supply future business intent without an applicable approved mapping.
Keep material unsupported rules unresolved, including missing-data defaults. Continue feasible investigation before asking the owner.

## Source and behavior discipline

Assess authority and applicability for each claim:

1. The latest explicit clarification controls intended behavior within its stated scope. Preserve earlier statements and conflicting sources.
2. Use applicable original requirements, designs, policies, and traceable owner decisions. Record their actual authority and review state.
3. Use exact code and retained execution for implementation or observed behavior only.
4. Use reports, summaries, and search results for discovery. Inspect their cited originals before relying on a conclusion.

An earlier report can retain an authoritative decision when it records the actual owner, date, scope, and decision evidence.
Do not create an artificial contradiction from an unapproved generated conclusion. Preserve material real conflicts and applicable versions.

For each conclusion, record source class, precise locator, revision or hash, fact established, confidence, rationale, and material limits.
Trace the actual caller and predicate, including evaluated fields, values, and operators, before asking about current behavior.
A nearby enum, helper, or field does not establish that the target flow uses it.
Inspect relevant duplicate paths and direct assertions. Distinguish found tests, inspected assertions, and executed cases with retained results.

## Focused decisions

Ask only decisions that available investigation cannot resolve and that can change the named phase.
Consider these categories when relevant:

- Identity: what makes two records the same business object and whether source keys remain.
- Discriminator: the authoritative field, valid values, normalization, and taxonomy mapping.
- Combination: which existing predicates remain, change, or are removed.
- Boundaries: inclusive dates, time zone, and valid historical or future values.
- Statuses: exact qualifying values and broader status behavior.
- Missing data: null, blank, malformed, unknown, or newly introduced values.
- Multiplicity: any match, all matches, newest match, or another selection rule.
- Consistency: duplicate clients, implementations, or workflows that must agree.
- Consequences: affected response, event, audit, notification, or control.
- Ownership: the person or role that approves each unresolved rule.

Keep short topic narratives beside questions in one editable living document.
Lead with the business choice. Use terms from the request; keep technical traces in the supporting ledger.
Split independent decisions. Offer meaningful proposed choices without forcing a false either/or choice.
Use this compact form:

```text
Decision <ID>: <one plain-language business question>
Proposed choices: <A> | <B> [| <C>] | another answer | unknown | named contact
Why asked: <one sentence explaining what changes>
Direct source: <precise source> — <fact it establishes>
Gap: <one sentence stating what the evidence cannot decide>
Owner: <named owner or unknown>
Answer:
```

Leave proposed choices unselected and preserve user answer fields.
Include only sources that create or materially change the choice. State a scoped evidence gap when no source establishes the rule.
Record searched concepts, inspected sources, provisional answer, confidence, and unresolved limits in the supporting ledger.
State when code or tests were not inspected. Identify conflicting tests as asserted behavior, separately from business authority.
Hand over the document for asynchronous answers. Continuation supplies no answer or approval.

## Decision-ready output

Reuse existing intake or stage sections for a compact decision contract:

1. Current behavior and desired behavior as separate statements.
2. A predicate table with `field`, `operator`, `value/source`, missing-data behavior, and owner or source.
3. Relevant supported examples, including positive, negative, equality, and boundary cases. Link canonical case definitions.
4. Confirmed facts, inferences, contradictions, and unresolved decisions.
5. Required data, consumer, query, observability, or ownership evidence that remains unavailable.
6. The completeness ledger with its evidence and owners.
7. Stable question IDs, source class, exact evidence, confidence, gap, owner, answer source, resolution, consequence, and next action.
8. The phase readiness decision and its evidence limits.

Use the Workbench phase labels:

- `READY` when no unresolved material uncertainty can change the named phase.
- `READY_WITH_LIMITS` only for continued evidence collection within the stated scope.
- `NEEDS_CLARIFICATION` when material intent or evidence gaps can change the named phase.

Completeness labels are review annotations, not runtime statuses or a separate readiness system.
Use [the intake phase gate](../analyze-requirement/SKILL.md#gate-the-next-phase) and state which unresolved criteria affect the named phase.
Readiness operates within existing authorization. Keep intent, implementation, assertions, execution, acceptance, publication, and deployment separate.
After an answer changes intent, reconcile candidate knowledge, provenance, versions, and the task update log through existing governance.
Keep required human review and publication pending until recorded evidence supports them.

## Stop conditions

Use `NEEDS_CLARIFICATION` when an unresolved material rule can change the dependent impact, design, or implementation phase.
Name the blocked action, owner, consequence, and exact answer or evidence needed.
Record non-material omissions with reasons instead of blocking unrelated work.
Continue independent authorized investigation and preserve the bounded-exploration route.

Static analysis, search, and controlled local execution do not establish production data quality, deployment applicability, or general business conformance.
