---
type: GovernanceFinding
id: FND-single-ui-source-provenance
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- &id001
  resource: repos/source-directory-inventory
  revision: sha256:d2949af709148cff7146f5dc9dd324cb5adc09bf7703b2687d48206ead0a67ee
  sha256: d2949af709148cff7146f5dc9dd324cb5adc09bf7703b2687d48206ead0a67ee
generated:
  by: agent:codex
  at: '2026-10-13T18:15:59.372897+00:00'
verified: []
subject:
  id: ARCH-single-ui-contracts
  version: 1
category: missing_source_revision
severity: warning
evidence:
- *id001
proposed_action: Provide original Git checkouts and full commit IDs. Compare retained
  source bytes with each identified commit.
resolution: open
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# Missing Single UI source revisions

## Subject

The supplied source copies have no independent Git metadata.
The affected repository IDs are `single-ui-bff`, `mfe-base`, and `mfe-root-config`.

## Evidence

The [retained inventory](../raw/2026-10-14-repository-registration/repository-inventory.json) records the directory checks.
Git commands from these directories inherit the Workbench repository.
Its commit identifies the Workbench, not these business sources.
Retained file hashes identify inspected bytes without establishing their originating commits.

Consequence: The contract registry requires full source commit IDs, so revisioned contract registration remains blocked.
Candidate interface observations remain available for investigation.

Owner: unknown.

## Proposed action

Provide each original Git checkout and its full source commit ID.
Compare every cited source file with the specified commit before registering its contract.
Keep incompatible or changed files unresolved.

## Resolution

open
