---
type: KnowledgeTopic
id: KT-static-data-cache-p3
version: 3
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
  by: agent:sol_complete_sources
  at: '2026-11-16T07:47:55.070193+00:00'
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
previous_version: 2
previous_content_sha256: a99de74d3a6bc9466abdf81bec993c9d192ced1c67949eb69c463e75bfa81ec9
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

### Historical FileIT request and acknowledgement fields

The historical request envelope is ImftFileRequest, with header fields messageVersion, flowIdentifier, uuid, country and sourceName.
Its payload identifies source.srcFilePath, target.dstName and target.dstFilePath. Each request requires a new UUID.
The acknowledgement envelope is IMFTFileNotification. Header fields include Version, Identifier, UUID, SrcJMSID, Source, Target, Country and Timestamp.

Payload fields include Component, SubComponent, TrackingID and SrcFilePath. Status carries Code, Reason and Causes.Details.
These are documented interface examples. Runtime schema compatibility remains unverified.

| Code | Source reason |
| --- | --- |
| 1000 | ACCEPTED |
| 1001 | NOT_AUTHORIZED |
| 1002 | BAD_REQUEST |
| 1003 | INVALID_ROUTING_RULE |
| 1004 | CFT_AUTHORIZATION_FAILURE |
| 1005 | CFT_UNAVAILABLE |
| 1006 | COPILOT_UNAVAILABLE |
| 1100 | INITIATED |
| 2000 | CFT_SUCCESSFUL |
| 2001 | CFT_SOURCE_PATH_INVALID |
| 2002 | CFT_SOURCE_PRE_PROCESSING_FAILED |
| 2003 | CFT_SOURCE_POST_PROCESSING_FAILED |
| 2004 | CFT_PARTNER_INVALID |
| 2005 | CFT_TARGET_PATH_INVALID |
| 2006 | CFT_TARGET_POST_PROCESSING_FAILED |
| 2007 | CFT_SOURCE_FILE_INSUFFICIENT_PERMISSION |
| 2008 | CFT_TARGET_PATH_INSUFFICIENT_PERMISSION |
| 2010 | CFT_SOURCE_IDF_INVALID |
| 2020 | CFT_TRANSFER_FAILED |
| 5000 | CFT_NOTIFICATION |
| 5001 | CFT_NOTIFICATION |

The source distinguishes accepted, initiated and successful transfer notifications.
Its 5000 notification describes receiver-processing success. Its 5001 notification describes failure from error processing.
Operational topic names, queue names, paths and populated identifiers remain retained source context.

Removal timing, retry and reconciliation policy remain unresolved beyond the source's after-delivery choice.
[Selected original lines 1–5](../../../evidence/sources/sha256/480cf95c126930918e648e6ff196add793a474185de68c8cd98d72d0dfaa27d5.md#L1-L5) [Selected original lines 34–40](../../../evidence/sources/sha256/480cf95c126930918e648e6ff196add793a474185de68c8cd98d72d0dfaa27d5.md#L34-L40) [Selected original lines 54–135](../../../evidence/sources/sha256/480cf95c126930918e648e6ff196add793a474185de68c8cd98d72d0dfaa27d5.md#L54-L135)

### Stage-one cache population and key contracts

A cache hit returns its stored value. A miss loads the database, stores a value with TTL, and returns that value.
The owning application handles population and freshness. The cache itself performs no automatic database fetch.
A database write invalidates its corresponding cached entry. The next read repopulates that entry.

The settlement-method design names group-management and SSI-stamping consumers of static-data-service configuration.
SSI stamping depends on the data ambassador for SSI+ data. The CES example connects query-service to auth-server and EMS3.
These are source-declared design dependencies. Current interface implementation remains unverified.

The generic prefix list names SETTLEMENT_METHOD, SSI_STAMP and CES. Its settlement-key example instead begins SettlementMethod.
The settlement key combines BookingEntityFmId, CounterpartyFmId, Taxonomy and Currency in that order.
The SSI proposal hashes query conditions, stores List<VostroStampingResponse>, and maintains a reverse index of SSI identifiers.

Its example string key is SSI:a1b2c3. Key encoding, collisions, reverse-index updates and CES lifecycle remain unresolved.
The illustrated query fields include branch, payment currency, CFI, counterparty, debit/credit, settlement type, method and SSI status.
Populated query values remain examples. The prefix differences retain their original source-specific spelling.
[Selected original lines 1–109](../../../evidence/sources/sha256/08d6bac2c24254da5a7b173a846268d3eba0159b12f1df77996d330cabb41358.md#L1-L109)

### Historical cache storage decision branches

The design first stores and updates data in the database. Database sufficiency for business NFRs selects database storage.
The following branches apply when database storage misses those NFRs.

| Usage and data | Proposed storage |
| --- | --- |
| Frequently used, small dataset | Cache all data in memory and retain all data in the database. |
| Frequently used, large dataset | Cache part of the data and retain all data in the database. |
| Infrequent external reference data, changes more than one hour apart | Database. |
| Infrequent external reference data, changes less than one hour apart | Query the golden source. |
| Infrequent Ratan-owned data | Database. |

The frequent-use branches apply to both source types and both listed change-frequency categories.
The source leaves the exact one-hour boundary unspecified.
It proposes daily SCI synchronization and consideration of third-party scheduling for SCI or Ratan crash recovery.

For user queries, it permits local or Redis caching under the same static-data rules.
Its middleware use cases name Redis for distributed locks, duplicate checking, X-Token sessions, gateway URL whitelists and data caching.

The HA proposal names six production nodes and both ARK and Watford, with active-active availability.
Its wording leaves the exact per-site node allocation unconfirmed. Traffic targets live service nodes, and DR follows HA.
The existing Day1 Redis and later-Hazelcast alternatives retain their qualifications.
[Selected original lines 3–54](../../../evidence/sources/sha256/4e4d48829f04608d8c375c697d280421ed37ca0973ad3f99cdbcee6109a9f496.md#L3-L54) [Selected original lines 73–149](../../../evidence/sources/sha256/4e4d48829f04608d8c375c697d280421ed37ca0973ad3f99cdbcee6109a9f496.md#L73-L149) [Selected original lines 174–199](../../../evidence/sources/sha256/4e4d48829f04608d8c375c697d280421ed37ca0973ad3f99cdbcee6109a9f496.md#L174-L199) [Selected original lines 205–209](../../../evidence/sources/sha256/4e4d48829f04608d8c375c697d280421ed37ca0973ad3f99cdbcee6109a9f496.md#L205-L209)

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
