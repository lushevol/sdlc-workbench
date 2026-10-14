---
type: GovernanceFinding
id: FND-ratan-skipped-result-status
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: repos/testing/ratan-test-engine/GenResults.py#L27-L39
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 80eb3ca34b7e3f462e9fa130d30ad62f49f0a19514fb3d40c11d2694a9e52de6
- resource: repos/testing/ratan-test-engine/GenResults.py#L149-L163
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 54fdbc5daeff83f673742d39aa1a7919c3ddf5ba1ee1d90e9e0ad76c3def6913
- resource: repos/testing/ratan-test-engine/GenResults.py#L188-L205
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 93ee5ed8f1c33b11c8eac26c88aa5e64f65ad1f32395bf53f17dc93e0f980f38
- resource: repos/testing/ratan-test-engine/GenResults.py#L261-L299
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 5c4938bb9ed5dc9d8081ee6350054c7215916f7ff23b32da379987cb038e3907
generated:
  by: agent:codex
  at: '2026-10-14T01:33:53.488111+00:00'
verified: []
subject:
  id: ARCH-sdk-e2e-contracts
  version: 2
category: ambiguous_execution_status
severity: warning
evidence:
- resource: repos/testing/ratan-test-engine/GenResults.py#L27-L39
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 80eb3ca34b7e3f462e9fa130d30ad62f49f0a19514fb3d40c11d2694a9e52de6
- resource: repos/testing/ratan-test-engine/GenResults.py#L149-L163
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 54fdbc5daeff83f673742d39aa1a7919c3ddf5ba1ee1d90e9e0ad76c3def6913
- resource: repos/testing/ratan-test-engine/GenResults.py#L188-L205
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 93ee5ed8f1c33b11c8eac26c88aa5e64f65ad1f32395bf53f17dc93e0f980f38
- resource: repos/testing/ratan-test-engine/GenResults.py#L261-L299
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 5c4938bb9ed5dc9d8081ee6350054c7215916f7ff23b32da379987cb038e3907
proposed_action: Identify the reporting owner and review skipped-result semantics before using exported
  PASSED as behavior evidence.
resolution: open
consequence: Exported PASSED and passed totals can include tests without executed assertions.
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# Exported passed results include skipped tests

## Subject

`ARCH-sdk-e2e-contracts`, version 2.
The supplied Robot result exporter merges passing and skipped test statuses.

## Evidence

The retained [XML input excerpt](../raw/2026-10-14-sdk-e2e-registration/ratan-test-engine/GenResults.py.L27-L39.snapshot) reads Robot results through `ExecutionResult`.
The retained [status mapping](../raw/2026-10-14-sdk-e2e-registration/ratan-test-engine/GenResults.py.L149-L163.snapshot) maps both `PASS` and `SKIP` to `PASSED`.
The same excerpt adds passed and skipped counts in the passrate numerator.
The retained [statistics excerpt](../raw/2026-10-14-sdk-e2e-registration/ratan-test-engine/GenResults.py.L188-L205.snapshot) also combines those counts in `passed`.
The retained [output excerpt](../raw/2026-10-14-sdk-e2e-registration/ratan-test-engine/GenResults.py.L261-L299.snapshot) writes `result.json`.

Consequence: Exported `PASSED` alone cannot distinguish passing assertions from skipped tests.
Consumers can overstate executed test coverage if they treat this field as behavior verification.
No retained execution or expected reporting policy was reviewed.
This finding does not establish a confirmed defect without that policy.

Owner: unknown.

## Proposed action

Identify the reporting owner and current result consumers.
Review whether those consumers require separate skipped and passed states.
Retain original Robot XML and inspect assertions before claiming passing business behavior.
If review confirms a defect, add a regression for the agreed reporting semantics.

## Resolution

open

Expected status semantics and business result consumers remain unresolved.
