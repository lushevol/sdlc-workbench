# SDK migration intent update

> **Candidate intent is updated; full compatibility and failure policy remain separate decisions.**
> Action: compare supported role-specific grants and review the proposed failure contract.
> Consequence: this knowledge update establishes no passing implementation or publication approval.
> Owner: unknown. Evidence: [exact user clarification](user-clarification-implementation.md).

## Updated intent

The [SDK topic](../../../knowledge/candidates/security/KT-sdk-and-entitlements.md#sdk-300-ces-migration-intent) advances from version 7 to version 8.
It remains `governance_state: candidate`, `status: draft`, and `verified: []`.
The target version is `3.0.0`. The old contract must be preserved where possible, with complete compatibility assessed.
The SDK caller supplies the FMAA token. Tests are required.
Failure-handling suggestions remain unselected recommendations. No complete compatibility result is implied.

| Clarification | Intended rule | Knowledge locator | Remaining limit |
| --- | --- | --- | --- |
| SDK-Q1 | Preserve the old contract where possible and assess full compatibility. | [Compatibility criterion](../../../knowledge/candidates/security/KT-sdk-and-entitlements.md#sdk-ces-intent-ac-001). | Full role-specific equivalence needs supporting CES scope and mappings. |
| SDK-Q2 | Target SDK version `3.0.0`. | [Migration intent](../../../knowledge/candidates/security/KT-sdk-and-entitlements.md#sdk-300-ces-migration-intent). | Deployed consumer versions are not supplied. |
| SDK-Q3 token owner | SDK caller supplies FMAA token. | [Token criterion](../../../knowledge/candidates/security/KT-sdk-and-entitlements.md#sdk-ces-intent-ac-002). | Production token lifecycle and trust remain caller integration concerns. |
| SDK-Q3 failures | User invites failure-handling suggestions. | Same intent section. | User has not selected a proposed failure contract. |
| Test request | Add tests for the migration. | Same intent section. | Actual assertions and results belong in task verification evidence. |

## Provenance and audit

- Source resource: `conversation:single-ui-sdk-ces-migration-20261101:implementation-clarification`.
- Source revision: `user-clarification-20261101-1`.
- Source SHA-256: `19aaaecc90ad229dfafacd8313a332f50981c0f01526e7b83f3aa55ba20b3820`.
- Exact-byte snapshot: [retained clarification](../../../evidence/knowledge/sources/user-clarifications/single-ui-sdk-ces-migration-20261101/user-clarification-implementation.md).
- Snapshot bytes equal the [task input](user-clarification-implementation.md).
- Manifest source ID: `SRC-sdk-ces-implementation-clarification-20261101`.
- Manifest: [source registry](../../../evidence/knowledge/manifest.yaml). Only this source entry was appended; earlier bytes remain intact.
- Current candidate SHA-256: `9e10e4df77db6422b048efbf06a95794a2a6badfb7941a62ec7ad7274e00dfbd`.
- Prior version 7 SHA-256: `6a5fa447bcd88333972c576a91599fcf24721f45edff3c1165dc4ed08fe33007`.
- New event: [AUD-20261101-KT-sdk-and-entitlements-v8](../../../evidence/knowledge/audit/AUD-20261101-KT-sdk-and-entitlements-v8.yaml).
- Previous event and all historical snapshots remain unchanged.

## Checks and limits

The ingestion baseline was captured before source, candidate, manifest, or audit changes.
The prepare checkpoint returned `PREPARED` with no findings.
The final [harness result](knowledge-intent-validation.json) returned `PASSED` with no findings.
Workspace validation returned `VALID` for 13 documents.
The selected scope checked 51 local links, four line fragments, one changed governed document, and one new audit event.
It retained 494 manifest records and 59 audit files.

The first final check [failed before the event existed](knowledge-intent-final-before-audit.json).
System `python3` lacked PyYAML, so event creation did not run.
Using `.venv/bin/python` created the required new event. Final validation then passed.
This was a tooling failure. It establishes no product defect.

Command:

```sh
.venv/bin/python -m ai_sdlc_workbench.ingestion.harness check --workspace . --baseline .workbench/ingestion/sdk-ces-intent-20261101-1535/baseline.json --plan .workbench/ingestion/sdk-ces-intent-20261101-1535/plan.yaml --seal .workbench/ingestion/sdk-ces-intent-20261101-1535/prepared.json --output .workbench/ingestion/sdk-ces-intent-20261101-1535/final-with-audit.json
```

The retained final report has unchanged bytes from that output.
Its SHA-256 is `575409219adea4024a5edfe26da3ba4ee73aa17a7f4cebd176288185d9692a4e`.
Source, structural, and audit checks do not establish complete ASD review, passing business execution, or human approval.
Implementation comparisons and execution outcomes remain outside `knowledge/`.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Candidate intent and deterministic validation do not establish implementation or publication approval.
```
