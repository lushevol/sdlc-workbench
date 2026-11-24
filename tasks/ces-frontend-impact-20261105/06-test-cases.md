---
artifact_kind: test-case
id: CES-FRONTEND-PROBES-20261105
version: 1
status: draft
owner: unknown
source_refs: [USER-001, BFF-001, BASE-001, CONTAINER-001]
related_ids: [CES-FRONTEND-IMPACT-20261105]
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Frontend contract investigation cases

> **Critical conclusions: These probes establish helper results within synthetic fixtures.**
> Action: retain browser and live contract verification for implementation.
> Consequence: probe success cannot establish deployed permission equivalence.
> Owner: unknown. Evidence: [probe implementation](evidence/contract-probes.cjs).

## Objective and traceability

The [user request](evidence/user-input.md#exact-user-input) requests frontend migration impact analysis.
These cases test current helper responses to reconstructed BFF payloads.
They do not define approved product acceptance criteria.
The [BFF comparison](evidence/bff-contract-analysis.md) defines the inspected provider contract.
The [analysis](05-impact-analysis.md) records required corrections separately from these diagnostic assertions.

## Preconditions and fixtures

| Item | Required state | Setup evidence |
| --- | --- | --- |
| Runtime | Existing local Node.js and Base TypeScript package | [Probe implementation](evidence/contract-probes.cjs) |
| Frontend source | Actual function bodies extracted through the TypeScript parser | [Source hashes](evidence/contract-probe-summary.json) |
| User | Synthetic user `fixture-user`; no credentials | [Probe fixtures](evidence/contract-probes.cjs) |
| Feature and action | `RATAN_TRADE_BLOTTER` and `F_Custom_View_Builder_Private` | [Probe fixtures](evidence/contract-probes.cjs) |
| Legacy application | `X_RATANONE`, source `EMS2` | [Probe fixtures](evidence/contract-probes.cjs) |
| CES application | `RATAN_ENTITLEMENT_RULE`, source `EMS3` | [Name clarification](../ces-entitlement-migration-20261102/evidence/user-input-20261030-field-equivalence.txt) |
| Saved workspace | `saved-trade`; current drawer includes its same container, module, and tile | [Probe fixtures](evidence/contract-probes.cjs) |

Isolation uses a Node VM and injected Hooks state.
The fallback workspace factory returns the deterministic ID `blank-fixture`.
All permission and validation function bodies come from existing source.
Cleanup requires no application or external-state changes.

## Procedure and assertions

### PROBE-01 — Legacy subject rejects an authorized CES tile

```gherkin
@PROBE-01
Feature: Observe frontend tile validation under migrated payloads
  Scenario: The unchanged validator rejects a different CES feature name
    Given the legacy entity contains subject "Legacy Trade Tile"
    And the CES entity contains feature "RATAN_TRADE_BLOTTER"
    And both corresponding drawers include the same tile
    And the tile subject remains "Legacy Trade Tile"
    When the actual helpers validate and restore workspace "saved-trade"
    Then the legacy tile validation returns true
    And the CES tile validation returns false
    And the legacy result retains workspace "saved-trade"
    And the CES result contains fallback workspace "blank-fixture"
    And the CES deep-link launch callback runs zero times
```

1. Construct equivalent drawer membership with legacy and CES subject representations.
2. Call the actual validation and restoration helpers.
3. Call the actual launch helper with the CES validation result.
4. Assert every diagnostic result stated above.

Intended migration outcome: preserve authorized launch and restoration after reviewed configuration mapping.
Old result: the legacy subject matches.
New result: the legacy subject differs from the CES feature.
Classification: compatibility mismatch under the stated fixture; no deployed failure claim.
Evidence: [retained result](evidence/PROBE-01.json).

### PROBE-02 — CES application bypasses legacy permission lookup

```gherkin
@PROBE-02
Feature: Observe application feature action lookup
  Scenario: The same grant resolves only through the legacy application
    Given the legacy application grants the named feature and action
    And the CES application grants the same feature and action
    When hasPermission evaluates "RATAN_TRADE_BLOTTER:F_Custom_View_Builder_Private" separately for each payload
    Then the legacy result equals true
    And the CES result equals false
```

1. Supply the legacy grant through Hooks.
2. Evaluate the requested action.
3. Replace Hooks with the CES grant.
4. Assert legacy true and CES false.

Intended migration outcome: preserve the mapped application permission.
Classification: compatibility mismatch under the stated fixture.
Evidence: [retained result](evidence/PROBE-02.json).

### PROBE-03 — A legacy entity masks a CES grant

```gherkin
@PROBE-03
Feature: Observe mixed entitlement handling
  Scenario: A legacy denial prevents discovery of a CES grant
    Given X_RATANONE contains only action "DifferentAction"
    And RATAN_ENTITLEMENT_RULE grants the requested feature and action
    When hasPermission evaluates "RATAN_TRADE_BLOTTER:F_Custom_View_Builder_Private"
    Then the result equals false
```

1. Supply both source representations through Hooks.
2. Evaluate the requested action.
3. Assert false from the actual helper.

Intended outcome requires explicit application scope and the effective migration provider.
Arbitrary union across providers is not a proposed policy.
Evidence: [retained result](evidence/PROBE-03.json).

### PROBE-04 — Repeated application names overwrite grants

```gherkin
@PROBE-04
Feature: Observe entitlement normalization
  Scenario: A later entity replaces an earlier application's feature actions
    Given the first RATAN_ENTITLEMENT_RULE entity grants the requested action through EMS3
    And the second RATAN_ENTITLEMENT_RULE entity grants only "DifferentAction" through EMS2
    When getUser normalizes both entities
    Then the normalized feature actions exclude "F_Custom_View_Builder_Private"
```

1. Supply both entities in their declared order.
2. Call the actual normalization helper.
3. Assert that the earlier grant is absent.

Intended outcome requires retaining source and application identity before permission resolution.
This case does not approve unioning grants across sources or application IDs.
Evidence: [retained result](evidence/PROBE-04.json).

## Execution binding

Run `node tasks/ces-frontend-impact-20261105/evidence/contract-probes.cjs` from the workspace root.
Each case saves its result before the next case starts.
The summary records runtime versions, file hashes, and the Base main comparison.

- Execution status: results are recorded in the [summary](evidence/contract-probe-summary.json).
- Base revision: `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`; selected helper bodies also compared with local `main`.
- BFF baseline: `834b4155232222347220e47139a502ee43a9cbdf`.
- BFF candidate: `267081800cc28b6af0f8e080fa67c2d5f14d3a26`.
- Container revision: unavailable; [filesystem hashes](evidence/container-source-hashes.json).
- Assertions: `save` calls in the [probe implementation](evidence/contract-probes.cjs).
- Browser, BFF Java, CES requests, session lifecycle, and production execution: `NOT_RUN`.

## Facts, inferences, and unresolved questions

The probes execute extracted frontend functions with synthetic payloads.
Reconstructed payloads follow inspected BFF mapping; they are not captured service responses.
Missing live mapping and release identities limit product conclusions.
Owner: unknown. Next action: verify approved mappings with actual BFF responses during implementation.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [PROBE-01](#probe-01--legacy-subject-rejects-an-authorized-ces-tile) | Authorized drawer membership can disagree with workspace and deep-link checks. | unknown | Align checks with the effective BFF tile decision. |
| [PROBE-02](#probe-02--ces-application-bypasses-legacy-permission-lookup) | A mapped grant can resolve false. | unknown | Add explicit application-scoped CES resolution. |
| [PROBE-03](#probe-03--a-legacy-entity-masks-a-ces-grant) | Legacy lookup can mask CES permissions. | unknown | Select the effective provider for the application. |
| [PROBE-04](#probe-04--repeated-application-names-overwrite-grants) | Source provenance and earlier actions are lost. | unknown | Preserve distinct source and application identities. |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| USER-001 | [User request](evidence/user-input.md#exact-user-input) | 2026-11-05 | [Manifest](evidence/source-manifest.json) | User; authorizes analysis. |
| BFF-001 | [BFF contract](evidence/bff-contract-analysis.md) | Base and candidate listed above | [Manifest](evidence/source-manifest.json) | Owner unknown; source contract only. |
| BASE-001 | [Base analysis](evidence/mfe-base-analysis.md) | Current Base HEAD listed above | [Base hashes](evidence/mfe-base-source-hashes.json) | Owner unknown; local source only. |
| CONTAINER-001 | [Container analysis](evidence/mfe-ratan-container-analysis.md) | Filesystem copy | [Container hashes](evidence/container-source-hashes.json) | Owner unknown; deployment unavailable. |
