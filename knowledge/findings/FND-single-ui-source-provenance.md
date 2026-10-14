---
type: GovernanceFinding
id: FND-single-ui-source-provenance
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- &id001
  resource: repos/initial-local-baselines
  revision: sha256:b050e41e1f6b66e24b34bf5873bcec251d020373c44b4dc4badda42c34b2f3b0
  sha256: b050e41e1f6b66e24b34bf5873bcec251d020373c44b4dc4badda42c34b2f3b0
- &id002
  resource: conversation:current/user-message/initial-repositories
  revision: request-2026-10-14-initial-repositories
  sha256: 3846ed5ac24f11790e3e11c25817faaa872b5ee57b81e84da2e8ce4b8de6bb16
generated:
  by: agent:codex
  at: '2026-10-14T01:06:51.080147+00:00'
verified: []
subject:
  id: ARCH-single-ui-contracts
  version: 2
category: missing_source_revision
severity: warning
evidence:
- *id001
- *id002
proposed_action: Use the new local commits to bind contract sources. Keep original
  repository history explicitly unavailable.
resolution: resolved
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# Initial local source revisions

## Subject

The user selected initial local repositories for the three supplied source copies.
Independent Git commits now identify each initial source baseline.
Original repository history remains unavailable.

## Evidence

The [user clarification](../raw/2026-10-14-initial-repositories/user-clarification.txt) authorizes initial local repositories.
The [baseline inventory](../raw/2026-10-14-initial-repositories/initial-baselines.json) records their full commit IDs.
All thirty retained source excerpts match bytes from those commits.
The contract registry now binds eight candidate declarations to those local revisions.

Consequence: Missing original commits no longer block local contract registration.
The new commits do not authenticate authors, approve business intent, or establish deployed behavior.

Owner: unknown.

## Proposed action

Use the local initial commits for source references.
Keep original history, owner review, and deployed routing limits explicit.
Add new snapshots and revisions when the source changes.

## Resolution

resolved

Local initial source revision binding is complete.
Original repository history remains unavailable by the selected baseline approach.
