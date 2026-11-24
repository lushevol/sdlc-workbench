---
type: KnowledgeTopic
id: KT-lock-concurrency-p3
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement Lock Process/page.md
  revision: sha256:37aba76d2ac09f6b8eb8559b0eaff0977a5d9d151ced692ec297320ab6259722
  sha256: 37aba76d2ac09f6b8eb8559b0eaff0977a5d9d151ced692ec297320ab6259722
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Distribution
    lock test cases  && Uber orchestration/page.md
  revision: sha256:d62877540ee41f1a79889fb319ae00ced0c75d9e04a3490166dde1c31a637f87
  sha256: d62877540ee41f1a79889fb319ae00ced0c75d9e04a3490166dde1c31a637f87
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Design Principle/RATANONE Distributed Lock ReDesign/page.md
  revision: sha256:a28ccd6544778f0d3f39dc6f7000f49169f01ff95cd608fa15dcb1718f280a5b
  sha256: a28ccd6544778f0d3f39dc6f7000f49169f01ff95cd608fa15dcb1718f280a5b
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Ratanone-Foundation
    release note/page.md
  revision: sha256:f7825ba44cd92205c90fcfa0e02049219a16d87908747add0c9829fc7a19c24d
  sha256: f7825ba44cd92205c90fcfa0e02049219a16d87908747add0c9829fc7a19c24d
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Redisson
    timeout analysis/page.md
  revision: sha256:f3b2931c92146e713460f2ea7ed4a59ec91e13a0c464ee3263a5e5d6fca8683f
  sha256: f3b2931c92146e713460f2ea7ed4a59ec91e13a0c464ee3263a5e5d6fca8683f
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:20:32.827186+08:00'
verified: []
scope: Historical selected-source design for lock concurrency p3.
classification: architecture
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which lock implementation, owner-validation contract, list atomicity, and idempotent
  result-recovery protocol are approved?
- Which caller migration and timeout configuration preserve behavior across old/new
  lock versions?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Lock concurrency p3

## Scope

Historical selected-source design for lock concurrency p3.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Business locking and recovery responsibilities

The lock-process design keys locks by cashflow ID.
UI operations show a lock alert and require manual retry.
Workflow events, SWIFT status updates, and Accounting status updates automatically retry under their stated processing responsibilities.
The source says until succeeded, without defining delay, maximum duration, or terminal failure handling.

Sources: [original lines 3–6](../../../evidence/sources/sha256/37aba76d2ac09f6b8eb8559b0eaff0977a5d9d151ced692ec297320ab6259722.md#L3-L6).

### Lock ownership and atomicity design

The redesign requires atomic lock and unlock and automatic release on exceptional paths.
The owner creates, extends, releases, and retries after rejected validation.
A reentrant client only validates and rejects expired or invalid locks.
Parallel work is excluded unless stateless.

The design retains enhanced Redis and Redisson alternatives with different validation and renewal behavior.
Batch locking must cover all netting components and release partial acquisitions on failure.
MultiLock/FasterMultiLock alternatives require validation of single-key mutual exclusion; source performance estimates are not acceptance guarantees.

Sources: [original lines 1–34](../../../evidence/sources/sha256/a28ccd6544778f0d3f39dc6f7000f49169f01ff95cd608fa15dcb1718f280a5b.md#L1-L34), [original lines 40–117](../../../evidence/sources/sha256/a28ccd6544778f0d3f39dc6f7000f49169f01ff95cd608fa15dcb1718f280a5b.md#L40-L117).

### Timeout and interservice consistency limits

The redesign identifies a gap when a parent fails or times out while a child continues.
Batch netting can leave service data inconsistent despite resource locking.
It proposes idempotent APIs with retrieval of the last call result and aligned request/rebalance timeouts.
Those are design remedies, not proof of transactional consistency or retry safety.

Sources: [original lines 40–117](../../../evidence/sources/sha256/a28ccd6544778f0d3f39dc6f7000f49169f01ff95cd608fa15dcb1718f280a5b.md#L40-L117).

### Migration API semantics

The new lock guidance changes the second argument from lock expiry to retry/wait duration.
The release note makes the unit change explicit: old milliseconds become waitTimeSeconds.
Redisson watchdog manages duration in the proposed new contract.
Single-key and list overloads retain their call shapes, so unchanged syntax does not preserve meaning.

Direct ResourceLock usage must release in finally.
The guidance requires the foundation feature and Spring Boot 3.4.4 and says Failsafe is unnecessary for lock retries.
These statements do not establish consumer migration or mixed-version compatibility.

Sources: [original lines 14–31](../../../evidence/sources/sha256/d62877540ee41f1a79889fb319ae00ced0c75d9e04a3490166dde1c31a637f87.md#L14-L31), [original lines 33–46](../../../evidence/sources/sha256/d62877540ee41f1a79889fb319ae00ced0c75d9e04a3490166dde1c31a637f87.md#L33-L46), [original lines 174–202](../../../evidence/sources/sha256/a28ccd6544778f0d3f39dc6f7000f49169f01ff95cd608fa15dcb1718f280a5b.md#L174-L202), [original lines 19–45](../../../evidence/sources/sha256/f7825ba44cd92205c90fcfa0e02049219a16d87908747add0c9829fc7a19c24d.md#L19-L45).

### Shared event and Redis configuration proposals

The foundation note agrees a shared cash_settlement_cashflow_domain_events topic.
The Redis-timeout proposal replaces default autoconfiguration with retryAttempts=4, three-second retry/reconnect delays, keepAlive=true, and connectTimeout=3600000 milliseconds.
The one-hour connection timeout is a proposal without a retained domain availability or latency acceptance contract.

Sources: [original lines 86–86](../../../evidence/sources/sha256/f7825ba44cd92205c90fcfa0e02049219a16d87908747add0c9829fc7a19c24d.md#L86-L86), [original lines 19–30](../../../evidence/sources/sha256/f3b2931c92146e713460f2ea7ed4a59ec91e13a0c464ee3263a5e5d6fca8683f.md#L19-L30).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which lock implementation, owner-validation contract, list atomicity, and idempotent result-recovery protocol are approved?
- Which caller migration and timeout configuration preserve behavior across old/new lock versions?
