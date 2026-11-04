# SDK API compatibility evidence

> **The supplied APIs cannot establish complete SDK migration coverage.**
> Action: capture the SDK assigned-role response and verify each configured legacy entity.
> Consequence: current samples do not execute the candidate's transport contract.
> Owner: unknown. Evidence: [API inventory](api-inventory.json) and [request](user-input.md#exact-user-input).

## Scope and identities

Baseline: `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`.
Candidate: `fd9a157e260850b6d9efa10da3223950ea61133a`.
Repository: `repos/libraries/single-ui-sdk-starter`.
Assessment date: 4 November 2026, Asia/Singapore.

The [inventory](api-inventory.json) binds 20 YAML files by SHA-256.
Eighteen files contain response examples. Two files contain folder metadata.
Four examples describe CES. Fourteen examples describe EMS2 UAT or PROD.
No network requests or SDK executions occurred in this inspection.

The [comparison result](api-parity.json) retains sample counts, differences, and source hashes.
The [inspection script](inspect_api_parity.py) reproduces those comparisons without emitting headers or credentials.

## Function and contract inventory

| Boundary | Baseline | Candidate | Evidence and disposition |
| --- | --- | --- | --- |
| Account role discovery | EMS2 account response supplies numeric role and entity identities. | Assigned CES roles supply application and entitlement names. | Candidate uses `/fmces/v1/entitlement/user/{userId}`. Supplied examples omit this endpoint. Current runtime support remains unknown. |
| Permission transport | EMS2 entitlement-list POST returns role-scoped subject/action grants. | CES assigned-role GET requires `appId`, `appName`, `entitlementName`, and `featureActionDtos`. | All four supplied CES shapes differ. Endpoint substitution alone cannot adapt them. |
| Role attribution | Numeric EMS2 role joins preserve entity and role scope. | Configured application, entity, role aliases, and feature filters preserve supported role scope. | Code supports several mappings. Reviewed project configuration remains necessary. |
| `X_RATANONE` functional permissions | PROD examples use `FMO_RO` and `NON_FMO_RO`. | Same-name CES catalog definitions preserve those sample pairs. | 55/55 sample grants match. Catalog assignments include both sample users. SDK execution remains unverified. |
| Data permission marker | `RATAN_DATA_ENTITLEMENT:Global` grants `RATAN_DATA_ENTITLEMENT/VIEW_ENTITLEMENT`. | CES catalog assigns `Global` and the same feature/action to both sample users. | 2/2 sample grant rows match. The README's single mapping cannot emit the legacy entity key. |
| System functions | `RATAN_FUNC:SYS_RO` grants three `Ratan_Function_*` subjects with `Query`. | CES catalog assigns `SYS_RO` and those pairs to `srv.ratan.001`. | 3/3 sample grants match. A separate legacy entity mapping remains necessary. |
| Data restrictions | Baseline SDK map exposes permission markers, not resolved policy fields. | Candidate DTO exposes feature/action pairs, not effective data restrictions. | No SDK regression is established for resolved restrictions. Broader data-access equivalence remains unverified. |
| Account status | Baseline lookup reads entitlement types without enforcing status fields. | Assigned-role adapter has no account-status predicate. | This does not establish an introduced status defect. Required status policy remains unresolved. |
| FMO administration | UAT sample grants `RATAN_PROD` three administration actions. | RATAN CES catalog has no matching same-name role. | User intent treats FMO as a separate, lower-priority non-production comparison. This does not block production parity. |

Candidate source: `AuthorizationImpl.java`, lines 164–217; `CesRole.java`, lines 10–43; `AuthProperties.java`, lines 34–56.
Read these paths at the candidate revision. The checkout started on the baseline and later moved to the reviewed candidate.
Baseline source: `AuthorizationImpl.java`, lines 30–64, 71–101, and 132–143.

## Bounded positive result

All 60 EMS2 PROD sample grant rows match CES catalog definitions and catalog account assignments.
Those rows represent three accounts and five account/entity/role combinations.
They contain 59 distinct entity/role/subject/action tuples because `Global` repeats across two accounts.
The [result](api-parity.json) keeps these denominators separate.

This comparison uses same-name roles, feature names, and action names.
It compares permission sets. It does not establish output array order or duplicate preservation.
It uses retained PROD EMS2 and UAT CES snapshots.
It does not prove live assignments, SDK output equality, or complete production population coverage.

## Complete supplied function inventory

The inspection includes every supplied EMS2 dictionary row and every supplied account grant row.
The [result](api-parity.json) retains each dictionary's exact names, source path, and SHA-256.

| Environment and entity | Supplied dictionary | Matching CES names | Missing exact names | Action-definition limit |
| --- | --- | ---: | --- | --- |
| PROD `RATAN_FUNC` | Three subjects. | 3/3 | None. | Dictionary supplies no actions. Three observed `Query` pairs match. |
| PROD `RATAN_DATA_ENTITLEMENT` | One subject. | 1/1 | None. | Dictionary supplies no actions. The observed `VIEW_ENTITLEMENT` pair matches. |
| PROD `X_RATANONE` | Twenty-four roles, despite the filename. | 23/24 | `EMS2_ADMIN`. | No complete subject dictionary or role grant definitions. All 32 observed subject/action pairs match. |
| PROD `FMO PORTAL ADMIN` | Zero subjects. | 0/0, empty denominator. | None in this empty response. | This response cannot establish functional coverage. |
| UAT `RATAN_FUNC` | Four subjects. | 3/4 | `srv.fxu.001`. | No action definition or account grant for the missing subject. Three observed `Query` pairs match. |
| UAT `RATAN_DATA_ENTITLEMENT` | One subject. | 1/1 | None. | Dictionary supplies no actions. The observed `VIEW_ENTITLEMENT` pair matches. |
| UAT `X_RATANONE` | Twenty-eight roles, despite the filename. | 24/28 | `EMS2_ADMIN`, `FMO_VPA_TEST`, `FMO_MO_CDS`, `FMO_RATAN_TEST`. | No complete subject dictionary or role grant definitions. All 63 observed subject/action pairs match. |
| UAT `FMO PORTAL ADMIN` | Three subjects. | 0/3 | `category`, `importmap`, `tile`. | Their three `READ-WRITE` pairs are absent from both CES catalogs. FMO remains separate. |

The RATAN CES catalog contains 74 entitlements, 39 distinct features, and 52 distinct action names.
The FLOWZERO catalog contains 40 entitlements, 18 distinct features, and 28 distinct action names.
These are catalog unions. They do not establish that each account holds every listed permission.
The comparison preserves RATAN application scope. FLOWZERO presence cannot replace a RATAN permission.

The PROD account union contains 36 distinct subject/action pairs across three legacy entities.
All 36 pairs occur in the RATAN CES catalog.
The non-FMO UAT account union contains 67 distinct subject/action pairs. All 67 pairs occur there.
These union counts differ from the 59 PROD role-scoped tuples and 60 PROD account grant rows.
Union presence cannot prove correct role attribution or complete account assignments.

The supplied `RATAN_FUNC` and data dictionaries contain no missing PROD subject names.
The supplied material lacks a complete `X_RATANONE` subject dictionary and any complete action dictionary.
Therefore, these files cannot establish all-function coverage beyond their recorded dictionaries and account examples.

The UAT subject `srv.fxu.001` is absent from both CES feature unions.
Its dictionary row supplies no actions. The account samples show no grant for that subject.
Consequence: an untranslated name remains visible, but tangible permission loss is unproved.
Owner: unknown. Next action: classify this subject and inspect its actual role/action assignments.
Confidence: HIGH for name absence; UNKNOWN for migration applicability and user impact.

The `EMS2_ADMIN` description states IAM role and entitlement management responsibility.
This supports a platform-administration interpretation, but no source records its cutover disposition.
Keep its missing name separate from demonstrated business-function loss.
Owner: unknown. Next action: confirm whether CES management roles replace this EMS2 role.

## Configuration needed for the matched sample scope

The configuration below is a sample-derived proposal.
It covers only the three supplied PROD account examples.
It requires assigned-role responses with the same reviewed permissions.
It does not approve a complete migration configuration.

```yaml
fmoportal:
  auth:
    ces:
      base-url: ${CES_BASE_URL}
      entity-mappings:
        - app-id: "51358"
          app-name: RATAN_ENTITLEMENT_RULE
          entity-name: X_RATANONE
          role-mappings:
            FMO_RO: FMO_RO
            NON_FMO_RO: NON_FMO_RO
        - app-id: "51358"
          app-name: RATAN_ENTITLEMENT_RULE
          entity-name: RATAN_DATA_ENTITLEMENT
          role-mappings:
            Global: Global
          feature-names:
            - RATAN_DATA_ENTITLEMENT
        - app-id: "51358"
          app-name: RATAN_ENTITLEMENT_RULE
          entity-name: RATAN_FUNC
          role-mappings:
            SYS_RO: SYS_RO
          feature-names:
            - Ratan_Function_Cashflow
            - Ratan_Function_Ssi_Stamping
            - Ratan_Function_Suppression
```

No subject alias is needed for these inspected sample pairs.
CES action names already match their EMS2 counterparts.
Role allowlists prevent unrelated application roles from appearing under each legacy entity.
Adding mappings without these boundaries can duplicate unrelated grants across legacy entities.

The candidate README shows only `X_RATANONE` with no role or feature allowlist.
Under that example, `Global` and `SYS_RO` use the `X_RATANONE` entity prefix.
Their required legacy data and system entity keys remain absent.
This is a configuration compatibility gap, not proof of the deployed configuration.
Owner: unknown. Next action: retain and execute the full reviewed project mapping.

## Remaining evidence gaps

### API-01: Runtime response contract

The SDK accepts assigned-role responses.
The supplied CES files contain two effective user responses and two application catalogs.
The effective user rows combine grants across entitlements.
The application catalogs retain role definitions and account assignments with a different transport shape.
Neither shape is a direct `CesRole` input.

Canonical case: [SDK-TC-004](../../../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-004).
This source comparison applies its malformed-response predicate. No new case execution occurred.

Setup: use one supplied CES response without changing its JSON shape.

1. Configure the candidate endpoint to return that supplied response.
2. Invoke the explicit-token entitlement lookup.
3. Assert the returned failure classification.

Intended result: preserve supported role-specific permissions without invented attribution.
Old result: EMS2 reads its own account and entitlement-list contracts; this CES input is inapplicable.
New result: source predicts `INVALID_RESPONSE` because application identity fields are absent.
The one-argument method catches this failure and returns an empty map.
No runtime reproduction occurred in this independent inspection.

Consequence: repointing the endpoint property cannot consume the supplied APIs.
Owner: unknown. Next action: capture the actual assigned-role endpoint or implement a separately reviewed catalog adapter.
Confidence: HIGH for shape incompatibility; UNKNOWN for current assigned-role service support.

### API-02: Current data role fixture coverage

The candidate retained assigned-role fixture contains six roles.
The current `1481696` effective sample contains seven roles, including `Global`.
The current application catalog also assigns `Global` and its permission marker to that user.
The [result](api-parity.json) binds the fixture hash and current sample source.

The missing fixture role does not prove that today's assigned-role endpoint omits `Global`.
Different endpoint shapes and capture times prevent that conclusion.
Consequence: the retained fixture cannot establish current data-role compatibility.
Owner: unknown. Next action: refresh the assigned-role fixture and assert `RATAN_DATA_ENTITLEMENT:Global` separately.
Confidence: HIGH for fixture difference; UNKNOWN for current runtime omission.

### API-03: Complete role and account scope

The PROD `X_RATANONE` file contains 24 roles despite its `subjects` filename.
Twenty-three names occur in the RATAN CES catalog. `EMS2_ADMIN` does not occur.
The UAT file contains 28 names. Four names do not occur in that CES catalog.
The absent UAT names are `EMS2_ADMIN`, `FMO_VPA_TEST`, `FMO_MO_CDS`, and `FMO_RATAN_TEST`.

Role-name presence does not establish equal role definitions or assignments.
No authoritative evidence classifies `EMS2_ADMIN` as a required migrated business role or excluded platform role.
Consequence: complete role inventory coverage remains unresolved.
Owner: unknown. Next action: classify these names through the migration scope and compare applicable definitions and accounts.
Confidence: HIGH for presence counts; UNKNOWN for the missing names' migration disposition.

### API-04: UAT differences

Both human UAT EMS2 samples use `FMO_OPS_BOM` with 63 permission pairs.
The same CES catalog role includes all 63 pairs and five additional validation-exception pairs.
Neither sample user appears in that CES role's assignment list.
The [comparison result](api-parity.json) retains all five additional pairs.

These differences do not contradict the matched PROD sample result.
They do prevent treating UAT EMS2 snapshots as equal to the current CES user snapshots.
Consequence: environment-specific parity requires its own reviewed expected scope.
Owner: unknown. Next action: compare synchronized environment snapshots before claiming UAT equality.
Confidence: HIGH for retained snapshot differences; UNKNOWN for current runtime behavior.

## Intent sources

The [SDK clarification](../../../../evidence/knowledge/sources/user-clarifications/single-ui-sdk-ces-migration-20261101/user-clarification-implementation.md#exact-user-input) requires compatibility assessment, caller FMAA tokens, version 3.0.0, and tests.
The [consolidation clarification](../user-input-20261030-api-samples-and-feature-consolidation.txt) places functional and data features under CES RATAN.
The [parity candidate](../../../../knowledge/candidates/security/KT-ces-migration-parity.md#documented-knowledge) preserves mapping scope and the separate FMO exception.
These sources establish intent. They do not establish runtime execution or publication approval.

## Writing checks

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
