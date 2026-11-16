---
type: Architecture
id: ARC-platform-cashflow-data-exposure
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement System Design/Expose The Cashflow Data Design/Cashflow data provider
    query solution for big volume/PT for big volume query/page.md
  revision: sha256:50b1e100385cc8bc3a040501cf17f6f5f6a1c37447e27f704e10c926bfce1986
  sha256: 50b1e100385cc8bc3a040501cf17f6f5f6a1c37447e27f704e10c926bfce1986
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement System Design/Expose The Cashflow Data Design/Cashflow data provider
    query solution for big volume/page.md
  revision: sha256:f6bb1a73b2400a5db2df24cb8dd354417d38946954ace52a22e16cbbd9eb683f
  sha256: f6bb1a73b2400a5db2df24cb8dd354417d38946954ace52a22e16cbbd9eb683f
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement System Design/Expose The Cashflow Data Design/page.md
  revision: sha256:0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c
  sha256: 0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Dormant
    SSI processing/page.md
  revision: sha256:6e7dbfdbfe1b3443417cd6b6621344e04e4e90434c96708ab4328b0231f4167f
  sha256: 6e7dbfdbfe1b3443417cd6b6621344e04e4e90434c96708ab4328b0231f4167f
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:23:59.449656+08:00'
verified: []
scope: Historical selected-source design for platform cashflow data exposure.
components:
- Data-provider query interface
- Logical field catalog
- Streaming query transport
- Daily SSI usage feed
interfaces:
- SQL-shaped cashflow query request
- Sliced HTTP response proposal
- SSI usage query alternatives
dependencies:
- Cashflow read/history storage
- FMAA and caller entitlement policy
- DQSL/SSDR and SSI+ consumer contracts
decisions:
- Return matching valid business records under authorized query contracts.
- Preferred streaming transport does not establish capacity acceptance.
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Platform cashflow data exposure

## Scope

Historical selected-source design for platform cashflow data exposure.

## Components

- Data-provider query interface
- Logical field catalog
- Streaming query transport
- Daily SSI usage feed

## Interfaces

- SQL-shaped cashflow query request
- Sliced HTTP response proposal
- SSI usage query alternatives

## Dependencies

- Cashflow read/history storage
- FMAA and caller entitlement policy
- DQSL/SSDR and SSI+ consumer contracts

## Decisions

- Return matching valid business records under authorized query contracts.
- Preferred streaming transport does not establish capacity acceptance.

## Documented knowledge

### External data access contract

The design requires cashflow data availability at any time and all valid records matching query criteria.
Its phased interface accepts a queryCondition SQL string at the data-provider endpoint.
It distinguishes invalid or non-query SQL, unsupported fields/operations, entitlement failures, busy/oversized requests, and common HTTP failures.
One phase lists custom 461/462/463 statuses; another lists standard status codes.

The selected sources do not settle the final error contract or a complete safe query grammar.

Sources: [original lines 1–9](../../../evidence/sources/sha256/0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c.md#L1-L9), [original lines 17–39](../../../evidence/sources/sha256/0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c.md#L17-L39), [original lines 50–72](../../../evidence/sources/sha256/0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c.md#L50-L72), [original lines 273–289](../../../evidence/sources/sha256/0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c.md#L273-L289), [original lines 296–318](../../../evidence/sources/sha256/0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c.md#L296-L318).

### Caller and entitlement boundary

The interface requires FMAA token, user, and application header consistency.
Bank-Id plus Country selects the documented SSDR path; otherwise it selects the EOD path.
The staged design treats these caller contexts separately.
This documentation grants no remote access and supplies no current authentication or entitlement verification.

Sources: [original lines 50–72](../../../evidence/sources/sha256/0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c.md#L50-L72).

### Phased capacity and storage alternatives

Phase one describes CN day-one storage below 100000 records.
Phase two addresses larger storage and slow queries through column/type/index changes.
Phase three targets million-record scale, more consumers, and second-level responses.
It considers alternative or independent storage.

These are scenario scopes and objectives, not measured capacity guarantees.

Sources: [original lines 17–39](../../../evidence/sources/sha256/0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c.md#L17-L39), [original lines 273–289](../../../evidence/sources/sha256/0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c.md#L273-L289), [original lines 296–318](../../../evidence/sources/sha256/0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c.md#L296-L318), [original lines 355–367](../../../evidence/sources/sha256/0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c.md#L355-L367).

### Large-volume transport design

The alternatives include precomputed report tables/files, gRPC in either client/server direction, and HTTP StreamingResponseBody.
Solution D is preferred to preserve the DQSL client while streaming repeated query slices.
A companion fragment uses 5000-record slices serialized to bytes.
The design leaves concurrency, splitting basis, refresh frequency, report reuse, and file retention open.


Sources: [original lines 36–46](../../../evidence/sources/sha256/f6bb1a73b2400a5db2df24cb8dd354417d38946954ace52a22e16cbbd9eb683f.md#L36-L46), [original lines 48–60](../../../evidence/sources/sha256/f6bb1a73b2400a5db2df24cb8dd354417d38946954ace52a22e16cbbd9eb683f.md#L48-L60), [original lines 62–75](../../../evidence/sources/sha256/f6bb1a73b2400a5db2df24cb8dd354417d38946954ace52a22e16cbbd9eb683f.md#L62-L75), [original lines 77–83](../../../evidence/sources/sha256/f6bb1a73b2400a5db2df24cb8dd354417d38946954ace52a22e16cbbd9eb683f.md#L77-L83), [original lines 85–92](../../../evidence/sources/sha256/f6bb1a73b2400a5db2df24cb8dd354417d38946954ace52a22e16cbbd9eb683f.md#L85-L92), [original lines 94–101](../../../evidence/sources/sha256/f6bb1a73b2400a5db2df24cb8dd354417d38946954ace52a22e16cbbd9eb683f.md#L94-L101), [original lines 44–46](../../../evidence/sources/sha256/50b1e100385cc8bc3a040501cf17f6f5f6a1c37447e27f704e10c926bfce1986.md#L44-L46).

### Exposed business field semantics

The field catalog distinguishes cashflow, business, major, minor, and audit versions.
It preserves origin message identifiers and links previous/next cashflow IDs for withdrawal/new chains.
Pay/receive is from SCB perspective; manual unnet is distinct from trade amendment.
The DVP delivery description requires both cash and security transfers.

Position_Id carries a do-not-use restriction pending modeling-team contact.
The V2 audit-query note requires Cashflow.Cashflow_Id.
The catalog labels many semantic flags and amounts String, so it cannot establish one runtime typing contract.

Sources: [original lines 369–534](../../../evidence/sources/sha256/0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c.md#L369-L534), [original lines 535–540](../../../evidence/sources/sha256/0ce6304c04ae783d634a12fa19fb558acf503d3ad328e755fcd0cd34b368057c.md#L535-L540).

### Dormant SSI usage feed

The dormant-SSI design records last use and supplies daily incremental used-SSI data for BCS and FMPR.
SSI+ uses the data to mark SSIs unused for 24 months inactive.
The table retains POST data-provider and GET payment-date SSI alternatives with different authorization descriptions.
Both return cashflow IDs and SSI unique IDs.

The GET example specifies a date-format error, without establishing an accepted general validation status.
The design does not define the last-used calculation, day boundary, or reconciliation of both interfaces.

Sources: [original lines 1–7](../../../evidence/sources/sha256/6e7dbfdbfe1b3443417cd6b6621344e04e4e90434c96708ab4328b0231f4167f.md#L1-L7), [original lines 12–16](../../../evidence/sources/sha256/6e7dbfdbfe1b3443417cd6b6621344e04e4e90434c96708ab4328b0231f4167f.md#L12-L16).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which versioned data-provider grammar, error codes, caller headers, and entitlement contract are approved?
- Which large-volume transport, stable slicing/order, capacity acceptance, and report retention are selected?
- Which typed field catalog and SSI last-used/inactivity boundaries govern consumers?
