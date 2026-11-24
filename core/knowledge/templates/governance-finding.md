---
type: GovernanceFinding
id: replace-id
version: 1
owner: replace-owner
governance_state: candidate
status: draft
sources:
- &id001
  resource: illustrative://fixture/one-item
  revision: example-v1
  sha256: 15826082e182d7add64f52f46a81d453de0ccabf0d3732dfd29fdc9bd12ea6e9
generated:
  by: illustrative-template
  at: '2026-10-14T00:00:00Z'
verified: []
subject:
  id: illustrative-requirement
  version: 1
category: review_required
severity: info
evidence:
- *id001
proposed_action: Ask the source owner to review the instantiated document.
resolution: open
---
# Illustrative GovernanceFinding

This example records no business asset or approval. Replace each example value before use.

## Subject

{"id": "illustrative-requirement", "version": 1}

## Evidence

- {"resource": "illustrative://fixture/one-item", "revision": "example-v1", "sha256": "15826082e182d7add64f52f46a81d453de0ccabf0d3732dfd29fdc9bd12ea6e9"}

## Proposed action

Ask the source owner to review the instantiated document.

## Resolution

open
