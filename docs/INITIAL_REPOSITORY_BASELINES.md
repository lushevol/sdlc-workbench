---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
- Automated checks do not check the complete approved dictionary or grammar rules.
---

# Initial repository baselines

Review date: 14 October 2026.
Workbench baseline: `3678469`.
Scope: Initial local Git repositories and revision-bound candidate contracts.

The [user clarification](../knowledge/raw/2026-10-14-initial-repositories/user-clarification.txt) selects initial repositories for the supplied copies.
Each directory now has independent Git metadata and a local initial commit.
The branch name is `codex/initial-baseline`.
No original repository history or remote URL was invented.

| Repository | Initial commit | Tracked files |
| --- | --- | --- |
| `single-ui-bff` | `091c9d16c13f285a78463ff0235c21b152844b61` | 167 |
| `mfe-base` | `99b4eda666bedf06574bc48766e4efdb339f4cc7` | 423 |
| `mfe-root-config` | `83091d85beff5306ca0cd643955d8ea6ed0a2d93` | 140 |

The [baseline inventory](../knowledge/raw/2026-10-14-initial-repositories/initial-baselines.json) records the inspected identities and limits.
Local Git exclusions keep environment files, generated output, dependencies, and credential containers outside the initial commits.
Application source bytes remain unchanged.

## Contract updates

[The contract catalog](../registry/contracts.yaml) contains eight candidate declarations.
Each source path resolves at its repository's full initial commit ID.
Repository and service records declare the corresponding provider or consumer contract IDs.
The source catalog now records three Git sources at their initial revisions.

[The architecture candidate](../knowledge/candidates/ARCH-single-ui-contracts.md) now uses version 2 and commit-bound source references.
Thirty new snapshots retain the cited bytes from the initial commits.
Earlier filesystem snapshots, manifest records, and audit events remain available.

[The provenance finding](../knowledge/findings/FND-single-ui-source-provenance.md) is resolved for local source revision binding.
Original history remains unavailable under the selected approach.
The earlier [registration report](REPOSITORY_REGISTRATION.md) describes the inventory stage before local Git initialization.

## Evidence limits

All eight contracts remain candidates because owner review and deployment evidence remain incomplete.
Gateway routing and active import-map use remain unresolved.
Git commits identify retained source bytes and do not establish business approval or passing business behavior.
No executable resources or operation grants were added.

Owner: unknown.
Next action: review the candidate interfaces and supply gateway or runtime evidence where required.

## Stage acceptance

```gherkin
Scenario: Bind contracts to initial local source revisions
  Given three supplied source copies selected as initial repositories
  When each copy receives its independent initial Git commit
  Then all three Git roots resolve to their own source directories
  And all eight contract source paths resolve at full commit IDs
  And all thirty retained business snapshots match committed source bytes
  And all eight contracts retain candidate status
```

## Validation

| Check | Result and evidence |
| --- | --- |
| Independent Git roots and clean source worktrees | PASSED. [Baseline inventory](../knowledge/raw/2026-10-14-initial-repositories/initial-baselines.json). |
| Contract revisions, source bytes, and candidate references | PASSED. [Retained checks](evidence/initial-repository-baseline-checks.json). |
| Source workspace validation | VALID. Three repositories, eight candidate contracts, and zero structural findings. |
| Runtime regression stage | PASSED: 77 tests before these data updates. [Retained execution](evidence/repository-registration-tests.txt). |
| Empty starter workspace isolation | PASSED. The newly registered source records remain outside generated starter data. |

Checks used macOS and Python 3.14.5.
Business tests and deployments were not executed.
Windows execution and ASD writing review remain pending.
