# Business task index

> **Critical conclusion: Use the owning task's current records before relying on historical executions.**
>
> The eight retained tasks cover Portal behavior, CES entitlement migration, and SDK compatibility.
> Their evidence does not establish current production behavior or release approval.
> Owner: the owner recorded by each task, or unknown when unresolved.

## Portal sessions and UI

| Task | Scope | Current entry points |
| --- | --- | --- |
| [Background session renewal](portal-background-session-20261019/01-intake.md) | Session renewal, security, coverage, and release assessment | [Gaps](portal-background-session-20261019/09-intent-reality-gaps.md), [issues](portal-background-session-20261019/10-issue-catalog.md), [release confidence](portal-background-session-20261019/10-release-confidence.md) |
| [Portal UI coverage](ui-test-coverage-20261022/01-intake.md) | Portal business cases and their UI execution evidence | [Canonical cases](ui-test-coverage-20261022/06-test-cases.md), [execution stage](ui-test-coverage-20261022/08-execution-stage.md), [questions](ui-test-coverage-20261022/05-knowledge-questions.md) |

## Entitlements and migration

| Task | Scope | Current entry points |
| --- | --- | --- |
| [CES entitlement migration](ces-entitlement-migration-20261102/01-intake.md) | EMS2-to-CES migration, output mapping, and compatibility | [Overview](ces-entitlement-migration-20261102/02-migration-overview.md), [API mapping](ces-entitlement-migration-20261102/03-output-mapping.md), [upper-caller audit](ces-entitlement-migration-20261102/11-zero-upper-change-audit.md) |
| [CES frontend impact](ces-frontend-impact-20261105/01-intake.md) | Frontend and BFF contract impact | [Impact](ces-frontend-impact-20261105/05-impact-analysis.md), [design](ces-frontend-impact-20261105/05-solution-design.md), [cases](ces-frontend-impact-20261105/06-test-cases.md) |
| [Independent tile rollout](ces-tile-rollout-review-20261109/01-intake.md) | Tile rollout and service migration compatibility | [Rollout](ces-tile-rollout-review-20261109/09-tile-rollout.md), [review](ces-tile-rollout-review-20261109/10-change-review.md) |
| [EMS3 entitlement review](ems3-entitlement-review-20261027/01-intake.md) | Entitlement migration defects and contract review | [Review](ems3-entitlement-review-20261027/07-code-review.md), [cases](ems3-entitlement-review-20261027/06-test-cases.md) |

## Shared SDK

| Task | Scope | Current entry points |
| --- | --- | --- |
| [SDK CES migration](single-ui-sdk-ces-migration-20261101/01-intake.md) | SDK migration to CES 3.0.0 | [Change review](single-ui-sdk-ces-migration-20261101/10-change-review.md), [execution](single-ui-sdk-ces-migration-20261101/08-test-execution-report.md), [coverage](single-ui-sdk-ces-migration-20261101/09-coverage.md) |
| [SDK mapper optimization](single-ui-sdk-optimization-20261107/01-intake.md) | Permission mapper performance and conformance | [Gaps](single-ui-sdk-optimization-20261107/09-intent-reality-gaps.md), [change review](single-ui-sdk-optimization-20261107/10-change-review.md) |

## Evidence and repository baseline

Keep existing task identifiers and frozen business evidence paths stable.
Organize navigation here without changing historical case or source identities.
Apply the [task procedures](README.md) to new work.
Keep reusable system knowledge in [canonical records](../knowledge/records/).

Workbench maintenance task history was removed under the 24 November 2026 user request.
The [cleanup receipt](cleanup-manifest.json) records removed paths, hashes, provenance relocation, and the prior Git revision.
Required business-source and governance evidence remains accessible through its recorded relocation.
The new Git baseline has no parent commits. Local recovery references retain the previous history.
Routine logs belong in ignored local storage. Git retains evidence required for consequential decisions and reproducibility.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
