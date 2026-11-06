# Tests-first frontend migration implementation

- Source: User message in the current Codex chat.
- Date: 2026-11-06 (Asia/Singapore).
- Priority: High-priority implementation instruction.

## Exact user input

> create test cases and e2e scripts for proposal first, then apply code changes.

## Scope and readiness

Readiness: `READY` for test-first implementation of the bounded shared adapter proposal.
Create canonical cases and executable E2E scripts before applying application changes.
Preserve upper-application APIs and independent tile provider selection.
Use the [current proposal](../../05-impact-analysis-frontend-entitlements.md#proposed-code-snippets).
The latest request authorizes implementation. It does not define missing multiple-role business rules.
Keep unresolved ownership, query, and data-profile policy visible.
Use local controlled execution. Existing restrictions on enterprise access remain applicable.

## Risk and evidence boundary

Risk: high for permission routing and provider isolation; moderate for presentation and workspace restoration.
Save focused baseline and candidate outcomes with exact source identities.
Local mock/browser results do not establish live CES parity, business acceptance, or deployment approval.
