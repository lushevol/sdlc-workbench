# Conversation improvements implementation

**Goal: complete and verify all seven improvements through real cases, one stage at a time.**
Owner: Workbench implementation agent.
Action: inspect current source, declare stage boundaries, and retain each completed verification case.
Evidence: [exact user authorization](../evidence/conversation-improvements-implementation-20261030/user-input.md).

Plan: [six implementation stages](CONVERSATION_IMPROVEMENT_PLAN_20261030.md#delivery-stages).
Recommendations: [seven improvement items](CONVERSATION_RETROSPECTIVE_20261030.md#seven-recommendations).

Status: stage 1 implemented and verified. Stage 2 is next.
Harness changes remain Workbench maintenance.
New business verification remains under its existing task and scope-specific readiness rules.

## Stage status

| Stage | Scope | State | Evidence and next action |
| --- | --- | --- | --- |
| 1 | Shared evidence references | COMPLETE | Session Refresh, CES, focused tests, runtime suite, and installed wheel checks passed. |
| 2 | Reusable release summary | PENDING | Consume the validated index without changing the existing ADO collection contract. |
| 3 | Coverage and shared case ledger | PENDING | Calculate inventories and retain original outcomes separately from verification. |
| 4 | Test plan and preflight | PENDING | Verify stopped services and actual served asset fingerprints. |
| 5 | Consequential business verification | PENDING | Reconcile exact business source composition and existing local readiness. |
| 6 | Question reconciliation and graph changes | PENDING | Reuse existing document and graph contracts. |

## Stage 1 scope and risk

Source baseline: `840e8a9b7`.
Affected interfaces: assurance CLI, installed JSON contracts, shared evidence references, and generated workspace guidance.
The existing assurance baseline and ADO release snapshot contracts retain their current consumers.
The new index references retained artifacts. It creates no competing evidence store.


Qualitative risk: medium. Incorrect joins could misstate coverage, source freshness, or execution outcomes.
Checks must reject dangling references and unsafe paths while preserving failed, partial, unknown, and characterization outcomes.

Real pilot inputs include the 467-instance Session Refresh inventory and the CES migration records.
Twelve changed Session Refresh files do not establish a complete changed-behavior denominator.
The inspected source composition differs from the historical release assessment.
Current frontend modifications are unrelated and must remain unchanged.

## Current execution prerequisites

The existing Session Refresh stage permits local evidence collection and reconciliation.
The CES intake permits understanding handoff. It does not establish implementation or business acceptance readiness.
Prepared browser assets exist. All five prepared local service ports are stopped.


The prepared BFF build has historical bindings and substituted dependencies.
It cannot establish current target parity.
Business verification will select exact revisions before reusing or starting application runs.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```

## Stage 1 verification

Both real reference pilots passed with exact source hashes.
The installed wheel initialized and validated a fresh workspace outside this checkout.
The package retained the guide and schema without copying runtime source.
The [case evidence index](../evidence/conversation-improvements-implementation-20261030/index.md) links retained results.

The runtime suite executed 687 tests with zero failures and errors.
Two optional connector integrations were initially excluded by their existing opt-in setting.
Their explicit local integration run is recorded separately.
The first package assertion incorrectly rejected responsibility guides under `core/`.
The corrected assertion checks runtime source files; its initial failed check remains retained.
