---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# EMS3 review evidence index

> **Runtime verification remains blocked.**
> Action: Restore private dependency access and execute the [focused cases](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md).
> Consequence: [source findings](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#findings) remain unverified by execution.
> Owner: unknown. Evidence: [build results](#validation).

## Current documents

- [Living intake](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/01-intake.md).
- [Review and comment locations](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md).
- [Canonical focused cases](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md).
- [Exact user input](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/user-input.md), recorded 27 October 2026.

## Source and comment evidence

| Evidence | Identity and supported claim | Limit |
| --- | --- | --- |
| [Auth context](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-context.json) | Base, candidate, fingerprint, and 63 file hashes | Selected comparison only |
| [BFF context](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-context.json) | Base, candidate, fingerprint, and 32 file hashes | Selected comparison only |
| [Auth audit](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-comment-audit.json) | Seven finding chains, exact sources, and inspected assertions | Source predictions only |
| [BFF audit](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-comment-audit.json) | Eight finding chains, exact sources, and inspected assertions | Source predictions only |
| [Comment locations](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/comment-locations.json) | 15 exact revision, side, and line bindings | Local anchors; no remote comments posted |
| [Base excerpts](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/base-source-excerpts.md) | Historical source and deleted assertions | No execution; full source hashes in [manifest](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/base-source-manifest.json) |

## Validation

Commands, timestamps, exit codes, and log hashes are in [validation.json](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/validation.json).
[Auth compilation](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-compile.log) and [BFF compilation](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-compile.log) stopped before compilation.

[Auth scan](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-scan.json) and [BFF scan](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-scan.json) reported no secret-pattern candidates.

[Auth YAML](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-yaml.log) and [BFF YAML](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-yaml.log) parsed successfully.
[Auth whitespace](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-diff-check.log) passed. [BFF whitespace](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-diff-check.log) failed.
No focused case execution passed. Automated scans do not establish business conformance.

Documentation checks: [document-checks.json](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/document-checks.json).
Source identities: [source-manifest.json](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/source-manifest.json).
Final service identity check: [final-identity.json](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/final-identity.json).
