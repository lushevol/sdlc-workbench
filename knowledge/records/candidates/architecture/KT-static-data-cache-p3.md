---
type: KnowledgeTopic
id: KT-static-data-cache-p3
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Ratan
    FileIT infra setup introduction/page.md
  revision: sha256:480cf95c126930918e648e6ff196add793a474185de68c8cd98d72d0dfaa27d5
  sha256: 480cf95c126930918e648e6ff196add793a474185de68c8cd98d72d0dfaa27d5
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Ratan
    Generic Cache Kit Stag1/page.md
  revision: sha256:08d6bac2c24254da5a7b173a846268d3eba0159b12f1df77996d330cabb41358
  sha256: 08d6bac2c24254da5a7b173a846268d3eba0159b12f1df77996d330cabb41358
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/The
    Cache Data Layer Design/page.md
  revision: sha256:4e4d48829f04608d8c375c697d280421ed37ca0973ad3f99cdbcee6109a9f496
  sha256: 4e4d48829f04608d8c375c697d280421ed37ca0973ad3f99cdbcee6109a9f496
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:29:53.347423+08:00'
verified: []
scope: Historical selected-source design for static data cache p3.
classification: architecture
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which source synchronization, reconciliation schedule, and freshness requirements
  govern each settlement dataset?
- What are the approved TTL, invalidation, key-collision handling, reverse-index update,
  and CES cache policies?
- Which Redis or Hazelcast architecture is approved for the applicable stage and environment?
- When may FileIT remove source files, and what acknowledgement, retry, retention,
  and reconciliation conditions govern removal?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Static data cache p3

## Scope

Historical selected-source design for static data cache p3.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Reference-data ownership and reconciliation

The historical cache-layer design distinguishes external reference data from Ratan-owned static data.
It proposes golden-source dumps for initialization and EDMI notifications for updates.
Daily source changes arrive by file, with end-of-day reconciliation and refresh when files differ.
It prefers database storage when that storage meets business NFRs.

Sources: [original lines 3–54](../../../evidence/sources/sha256/4e4d48829f04608d8c375c697d280421ed37ca0973ad3f99cdbcee6109a9f496.md#L3-L54).

### Data-specific stamping responsibilities

The design initializes Vostro data from SSI+ dumps and updates it through SSI+ notifications.
It requires end-of-day reconciliation.
Nostro data uses manual initialization and later data dumps.
Counterparty data uses SCI API initialization, notifications, and scheduled synchronization.

The key examples use SSI-ID, Nostro entity/currency/means/account, and counterparty FMID.

Sources: [original lines 73–149](../../../evidence/sources/sha256/4e4d48829f04608d8c375c697d280421ed37ca0973ad3f99cdbcee6109a9f496.md#L73-L149).

### Cache-aside service responsibility

The stage-one cache proposal covers settlement methods, SSI Vostro, and CES.
The application populates cache entries on misses and controls TTL freshness.
After database writes, it invalidates corresponding cache entries.
Settlement-method keys combine booking entity, counterparty, taxonomy, and currency.

SSI keys derive from query conditions and reference an SSI reverse index.
The CES key and dataset lifecycle sections remain incomplete.

Sources: [original lines 11–41](../../../evidence/sources/sha256/08d6bac2c24254da5a7b173a846268d3eba0159b12f1df77996d330cabb41358.md#L11-L41), [original lines 43–109](../../../evidence/sources/sha256/08d6bac2c24254da5a7b173a846268d3eba0159b12f1df77996d330cabb41358.md#L43-L109).

### Settlement file-transfer contract

The FileIT design chooses removal of source files after delivery.
Its request identifies the flow, country, source, a new request UUID, and source and destination paths.
The acknowledgement includes UUID, tracking identity, source path, and status.
Accepted and initiated statuses are distinct from transfer-success status 2000.

The failure taxonomy distinguishes authorization, routing, availability, path, permission, processing, and transfer failures.

Sources: [original lines 1–5](../../../evidence/sources/sha256/480cf95c126930918e648e6ff196add793a474185de68c8cd98d72d0dfaa27d5.md#L1-L5), [original lines 34–40](../../../evidence/sources/sha256/480cf95c126930918e648e6ff196add793a474185de68c8cd98d72d0dfaa27d5.md#L34-L40), [original lines 54–135](../../../evidence/sources/sha256/480cf95c126930918e648e6ff196add793a474185de68c8cd98d72d0dfaa27d5.md#L54-L135).

### Historical middleware alternatives

The cache-layer document proposes clustered Hazelcast with HA and DR deployment.
Its final upgrade strategy instead specifies Redis v6+ for Day1 and Hazelcast as a later NFR improvement.
These source-specific proposals do not establish a current middleware selection.

Sources: [original lines 174–199](../../../evidence/sources/sha256/4e4d48829f04608d8c375c697d280421ed37ca0973ad3f99cdbcee6109a9f496.md#L174-L199), [original lines 205–209](../../../evidence/sources/sha256/4e4d48829f04608d8c375c697d280421ed37ca0973ad3f99cdbcee6109a9f496.md#L205-L209).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which source synchronization, reconciliation schedule, and freshness requirements govern each settlement dataset?
- What are the approved TTL, invalidation, key-collision handling, reverse-index update, and CES cache policies?
- Which Redis or Hazelcast architecture is approved for the applicable stage and environment?
- When may FileIT remove source files, and what acknowledgement, retry, retention, and reconciliation conditions govern removal?
