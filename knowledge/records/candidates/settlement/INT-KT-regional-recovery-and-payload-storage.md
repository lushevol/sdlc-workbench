---
type: KnowledgeTopic
id: INT-KT-regional-recovery-and-payload-storage
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-dcf899a5a3b9ec9bd959d428
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/2026
    Design/Cash Settlement Platform Architecture - Indonesia/Active-Active to Active-Passive/page.md
  revision: sha256:47935b4641025e501c36fd6f11fbbf9932fe47922d1d32f542daba9f589d6a0b
  sha256: 47935b4641025e501c36fd6f11fbbf9932fe47922d1d32f542daba9f589d6a0b
- id: SRC-9282a74f249e837d118d0334
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/2026
    Design/Cash Settlement Platform Architecture - Indonesia/Message Middleware DR
    Solution/page.md
  revision: sha256:9bc394d848c09b0c4f460939f3284c9781cb5e14677de57fad72dad0a263f3f5
  sha256: 9bc394d848c09b0c4f460939f3284c9781cb5e14677de57fad72dad0a263f3f5
- id: SRC-d64cf80584db5b15b6572fa7
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/2026
    Design/Cash Settlement Platform Architecture - Indonesia/Minio Solutioning/page.md
  revision: sha256:2e0da40d66544427575f650858fc984ca691c0be42634402c6ef19d4dae75123
  sha256: 2e0da40d66544427575f650858fc984ca691c0be42634402c6ef19d4dae75123
- id: SRC-a1187f929470f8e84fc077f7
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/2026
    Design/Cash Settlement Platform Architecture - Indonesia/Mirror Maker 2 Solutioning/page.md
  revision: sha256:02d0a8bde35ac96e3a77b6ffe8d616ba0751aac123cc32657ced4c8cc59b11df
  sha256: 02d0a8bde35ac96e3a77b6ffe8d616ba0751aac123cc32657ced4c8cc59b11df
generated:
  by: agent:codex:sol-integrations-review
  at: '2026-11-16T01:30:46.166743+00:00'
verified: []
classification: settlement
scope: Regional recovery and payload-storage proposals
summary: Selected source descriptions preserve scoped intended responsibilities. Current
  authority and applicability remain unresolved.
related: []
open_questions:
- 'KDQ-b40f37b35f: Which messaging topology and producer/replay controls meet the
  approved Indonesia RTO/RPO?'
- 'KDQ-ab088db087: Which MirrorMaker failover/failback tests and evidence establish
  the accepted recovery scope?'
- 'KDQ-abee8e3109: Which MinIO security, read/failure mode, migration rollback sequence,
  and per-scenario DR targets are approved?'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Regional recovery and payload-storage proposals

## Scope

Regional recovery and payload-storage proposals.
These source descriptions define separate contracts. They establish no deployed or tested behavior.

## Summary

The selected sources describe related responsibilities and conditions.
Their original authority, effective dates, and current applicability remain unresolved.

## Documented knowledge

### DR-01 — Active-passive topology alternatives

The deployment proposal retains two choices: one profile with VIP switching, or isolated dual profiles.
VIP switching requires stopping primary applications, checking shutdown, switching VIPs, and starting standby applications with checks.
Dual profiles require deployment changes and controls against simultaneous message consumption.
Kafka alternatives include a custom synchronizer, MirrorMaker 2, and producer/consumer reconciliation with replay after DR.
No inspected choice establishes an accepted topology or replay equivalence.

[Selected original evidence](../../../evidence/sources/sha256/47935b4641025e501c36fd6f11fbbf9932fe47922d1d32f542daba9f589d6a0b.md#L1-L16), [Selected original evidence](../../../evidence/sources/sha256/47935b4641025e501c36fd6f11fbbf9932fe47922d1d32f542daba9f589d6a0b.md#L30-L32), [Selected original evidence](../../../evidence/sources/sha256/47935b4641025e501c36fd6f11fbbf9932fe47922d1d32f542daba9f589d6a0b.md#L43-L49).

### DR-02 — Messaging recovery objectives and options

The middleware proposal targets automated RTO at most two hours and RPO zero.
It compares MirrorMaker 2, Confluent replication, producer dual-write, object-log shipping, and replacing Kafka with Solace.
Asynchronous MirrorMaker replication permits nonzero lag. Its mechanism alone cannot establish the zero-loss objective.
The dual-write recommendation depends on producer changes and unresolved consistency handling.
Ordering, retries, replay, and CQRS differences require scoped design decisions. Recommendations are not approved selections.

[Selected original evidence](../../../evidence/sources/sha256/9bc394d848c09b0c4f460939f3284c9781cb5e14677de57fad72dad0a263f3f5.md#L3-L24), [Selected original evidence](../../../evidence/sources/sha256/9bc394d848c09b0c4f460939f3284c9781cb5e14677de57fad72dad0a263f3f5.md#L31-L87), [Selected original evidence](../../../evidence/sources/sha256/9bc394d848c09b0c4f460939f3284c9781cb5e14677de57fad72dad0a263f3f5.md#L111-L215), [Selected original evidence](../../../evidence/sources/sha256/9bc394d848c09b0c4f460939f3284c9781cb5e14677de57fad72dad0a263f3f5.md#L216-L299).

### DR-03 — MirrorMaker POC scope

The MirrorMaker proposal prefers distributed Kafka Connect for production and covers all Indonesia topics.
Normal replication is one-way from primary to standby. Reverse replication is limited to controlled failback.
The selected test matrix has no completed status or evidence, and DR rehearsal remains TBD.
The proposal establishes neither a passing POC nor zero data loss.

[Selected original evidence](../../../evidence/sources/sha256/02d0a8bde35ac96e3a77b6ffe8d616ba0751aac123cc32657ced4c8cc59b11df.md#L1-L16), [Selected original evidence](../../../evidence/sources/sha256/02d0a8bde35ac96e3a77b6ffe8d616ba0751aac123cc32657ced4c8cc59b11df.md#L31-L63), [Selected original evidence](../../../evidence/sources/sha256/02d0a8bde35ac96e3a77b6ffe8d616ba0751aac123cc32657ced4c8cc59b11df.md#L148-L177).

### DR-04 — Object storage and consistency proposal

The MinIO proposal separates raw trade payloads from PostgreSQL metadata and object references.
References include bucket, key, size, and SHA256 checksum.
The write flow uploads first and then commits the database reference. Database failure triggers asynchronous orphan deletion.
The preferred read mode streams through the service; a presigned URL is an alternative with proposed 15-minute expiry.
Upload failure prevents database writes. Missing objects return 404 with an alert.
Checksum mismatch rejects the response and marks corruption. Unavailable storage triggers a circuit breaker with unresolved read-only or 503 handling.
The proposal includes bounded exponential retries, orphan cleanup, and periodic reference consistency checks. These are design requirements only.

[Selected original evidence](../../../evidence/sources/sha256/2e0da40d66544427575f650858fc984ca691c0be42634402c6ef19d4dae75123.md#L1-L26), [Selected original evidence](../../../evidence/sources/sha256/2e0da40d66544427575f650858fc984ca691c0be42634402c6ef19d4dae75123.md#L28-L85), [Selected original evidence](../../../evidence/sources/sha256/2e0da40d66544427575f650858fc984ca691c0be42634402c6ef19d4dae75123.md#L88-L148), [Selected original evidence](../../../evidence/sources/sha256/2e0da40d66544427575f650858fc984ca691c0be42634402c6ef19d4dae75123.md#L203-L231).

### DR-05 — Storage security and recovery scope

The storage proposal includes TLS, encryption at rest, and managed-key alternatives.
Its sample role and department check do not define accepted production roles or regional authorization.
A single-node failure target of RPO zero and RTO below one minute differs from cross-site targets.
The full-site targets are RPO below 30 seconds and RTO below 15 minutes. They do not satisfy messaging RPO zero.
Replication direction remains selectable. Versioning is recommended for accidental deletion protection.
Migration proposes dual writes, backfill, object-first reads with database fallback, and later legacy-column removal.
The backfill clearing step conflicts with retaining legacy data for rollback; the safe sequence requires a decision.
Sample sizes, throughput, durability, and latency figures are proposed benchmarks, not accepted or measured results.

[Selected original evidence](../../../evidence/sources/sha256/2e0da40d66544427575f650858fc984ca691c0be42634402c6ef19d4dae75123.md#L280-L299), [Selected original evidence](../../../evidence/sources/sha256/2e0da40d66544427575f650858fc984ca691c0be42634402c6ef19d4dae75123.md#L302-L351), [Selected original evidence](../../../evidence/sources/sha256/2e0da40d66544427575f650858fc984ca691c0be42634402c6ef19d4dae75123.md#L355-L380), [Selected original evidence](../../../evidence/sources/sha256/2e0da40d66544427575f650858fc984ca691c0be42634402c6ef19d4dae75123.md#L418-L425), [Selected original evidence](../../../evidence/sources/sha256/2e0da40d66544427575f650858fc984ca691c0be42634402c6ef19d4dae75123.md#L429-L450), [Selected original evidence](../../../evidence/sources/sha256/2e0da40d66544427575f650858fc984ca691c0be42634402c6ef19d4dae75123.md#L454-L476).

## Connections

The owning task retains related source and question evidence.

## Evidence limits

Source descriptions supply documented intent and historical proposals only.
They do not establish current approval, implementation, configuration, deployment, execution, or acceptance.
Unselected content and attachments were not used to fill gaps.

## Open questions

Owner: unknown. Answers remain pending in the single [task question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
