# EMS2 and CES API sample comparison

> **Critical conclusions: Permission parity remains unproved.**
> Action: obtain equivalent account snapshots and the authoritative mapping before implementation acceptance.
> Consequence: the current samples cannot establish preserved access.
> Owner: unknown. Evidence: [pair comparison](api-sample-manifest-20261030.json).

## Scope and evidence

This review parsed all eight supplied JSON files on 30 October 2026.
Every file parsed successfully. No prefix removal or byte repair was necessary.
Each file contains one JSON line. The tables use JSON pointers for exact locators.
The [manifest](api-sample-manifest-20261030.json) retains source hashes, sizes, counts, and pair differences.
No live API, business test, or runtime authorization check ran.
Capture dates, source environments, response headers, and HTTP methods are unavailable.
Filename paths identify likely endpoints. They do not establish an authoritative API contract.

| Evidence | Source | Exact payload locator |
| --- | --- | --- |
| A1 | [EMS2 user account](../api/:ems2:rest:account:1481696.json) | `/accountStatus`, `/accountName`, `/accountType`, `/entitlementTypes` |
| A2 | [EMS2 service account](../api/:ems2:rest:account:srv.ratan.001.json) | `/accountType`, `/accountOwner`, `/entitlementTypes/0/uniqueName` |
| A3 | [EMS2 entitlement list](../api/:ems2:rest:entitlements:entitlementList%20.json) | `/1481696/entitlements`, `/1481696/count` |
| A4 | [CES user role details](../api/-fmces-v1-entitlement-user-1481696.json) | `/0/entitlementId`, `/0/appId`, `/0/appUID`, `/0/itamId`, `/5/featureActionDtos` |
| A5 | [CES application catalog](../api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE.json) | `/0/entitlement_id`, `/0/role_entitlements`, `/0/user_ids` |
| A6 | [CES aggregate user response](../api/-fmces-v1-entitlement-app-51358-RATAN_ENTITLEMENT_RULE-user-1481696.json) | `/0/user_data`, `/0/entitlements` |
| A7 | [CES response sample](../api/-fmces-v1-entitlement-user-response-1481696.json) | `/0/entitlements` |
| A8 | [CES entitlement 588 detail](../api/-fmces-v1-entitlement-588-app-51358-RATAN_ENTITLEMENT_RULE.json) | `/entitlementId`, `/featureActions`, `/policies`, `/profiles` |

## Confirmed sample differences

Confidence is high for payload facts below. The conclusion applies only to these retained samples.

| Concern | EMS2 sample | CES sample | Migration implication and limit |
| --- | --- | --- | --- |
| Account identity | A1 contains status, type, name, owner, and 69 `entitlementTypes` entries. | A6 contains user ID and application identity. | No CES account-status, owner, or full-name replacement appears in these samples. |
| Service accounts | A2 shows `accountType: Service` and five assigned entries. | No service-account response is supplied. | Service authentication and permissions require separate mapping evidence. |
| Role identity | A1 uses composite `uniqueName`, role names, and application names. | A4 uses `entitlementId`, `entitlementName`, and application fields. | Composite IDs cannot be mechanically retained as CES entitlement IDs. |
| Functional access | A3 uses nested `subject`, `role`, `action`, and EMS2 `entity`. | A4 uses `featureActionDtos`; A6 uses flat `feature` and `action` pairs. | A candidate bridge maps subject names to feature names. Business equivalence needs review. |
| Scope | A3 supplies 63 rows under user `1481696`, all for `X_RATANONE` and `FMO_OPS_BOM`. | A4 supplies six roles under application `RATAN_ENTITLEMENT_RULE`. | These are different role sets. Same user ID does not prove comparable grants. |
| Application identifiers | A1 uses named applications within a cross-application account response. | A4 uses `appId: "51358"`, `appUID: 10`, and `itamId: null`. A6 uses `itam_id: "51358"`. | Keep external ITAM identity, internal application identity, and application name distinct. |
| Naming and types | A1 and A3 use EMS2 DTO fields and numeric object IDs. | A4 uses camelCase and string entitlement IDs. A5 uses snake_case and numeric entitlement IDs. | Different CES responses need explicit models and identifier normalization. |
| Data access | A1 includes role `Global` under `RATAN_DATA_ENTITLEMENT`. A3 carries functional grants. | A6 includes policy rules, profile rules, and 129 string values for `Entity.Booking_Entity_SCI_FMID`. | Preserve string values. Some values contain letters or spaces. No authoritative legacy data mapping is supplied. |
| Catalog and membership | A1 is an account assignment response. | A5 lists 68 application entitlements, their feature/action pairs, and `user_ids`. | Application catalog retrieval differs from effective user permission retrieval. |
| Role details | No equivalent role-detail sample is supplied. | A8 contains `FMO_MO_SUP`, ID 588, and 27 feature/action pairs across 12 features. | `policies` and `profiles` are empty here. Other shapes remain unknown. |
| Errors and freshness | No error or cache metadata is supplied. | No error, pagination, cache, revocation, or freshness metadata is supplied. | Define these behaviors from the service contract and system policy. |

## Internal consistency checks

The checks below concern static payload consistency. They do not verify business access.

- A6 and A7 are byte-identical. They provide one independent payload example.
- A4 has six roles. Their feature/action union equals A6's 30 unique pairs.
- A8's 27 pairs equal entitlement 588's pairs in A5.
- A4 assigns entitlement 149, `RATAN_ENTITLEMENT_GLOBAL`, to the supplied user.
- A5 entry `/6` lists entitlement 149 with empty `user_ids`.
- Five other assigned roles include the supplied user in A5 membership lists.

The membership difference is unresolved. Capture times and direct-versus-effective membership semantics are unknown.
Owner: unknown. Next action: identify authoritative membership semantics and compare synchronized responses.
This difference does not establish a service defect or release blocker.

## Permission comparison and its limits

A3 has 63 unique subject/action pairs. A6 has 30 unique feature/action pairs.
Exact name matching finds 23 shared pairs, 40 EMS2-only pairs, and seven CES-only pairs.
The [machine comparison](api-sample-manifest-20261030.json) retains every pair.

EMS2-only examples include cashflow ad hoc initiation, verification, and public-view permissions.
CES-only examples include option-expiry access, option-expiry read, `Entitlement/View`, and `Reports/View`.
These differences show why a payload translation alone cannot establish migration parity.
They do not prove accidental permission loss or additional unauthorized access.
The samples have different assigned roles and no synchronized capture evidence.

Intended result: unknown until the mapping and permitted changes are reviewed.
Old result: A3 contains the 63 recorded EMS2 pairs.
New result: A6 contains the 30 recorded CES pairs.

Comparison steps:

1. Read A3 at `/1481696/entitlements`.
2. Extract each `subject.name` and `action.name` pair.
3. Read A6 at `/0/entitlements/role_entitlements`.
4. Extract each `feature` and `action` pair.
5. Compare the two sets using exact, case-sensitive names.
6. Retain shared, old-only, and new-only sets in the manifest.

## Material remaining questions

These questions require contract evidence or an accountable owner.
They do not request answers already present in the samples.

| ID | Question | Consequence | Owner | Next evidence or action |
| --- | --- | --- | --- | --- |
| API-Q1 | Which CES response is the supported effective-permission contract? | Consumers could select incompatible DTOs or incomplete grants. | unknown | Obtain versioned OpenAPI or CES owner guidance. |
| API-Q2 | Which mappings replace EMS2 entities, composite roles, and legacy data-entitlement roles? | Portal entry, tile access, actions, and data scope remain unbound. | unknown | Obtain the mapping table and permitted grant changes. |
| API-Q3 | How does CES supply account status, user profile data, and service-account permissions? | Login and backend account flows may retain unmigrated dependencies. | unknown | Obtain account and service-account contracts and samples. |
| API-Q4 | Do catalog `user_ids` represent direct membership while user responses include inherited membership? | A5 and A4 disagree for entitlement 149. | unknown | Compare synchronized responses and membership semantics. |
| API-Q5 | Which environments, capture dates, and role assignments apply to these samples? | Static pair differences cannot establish permission preservation. | unknown | Obtain synchronized EMS2/CES snapshots for representative accounts. |
| API-Q6 | What are CES authentication, error, empty-result, timeout, cache, and revocation rules? | Safe cutover and recovery behavior cannot be finalized. | unknown | Inspect the authoritative operational and API contracts. |

## Writing checks

[Automated checks](api-analysis-checks-20261030.json) checked local links, JSON parsing, and sample set consistency.
These checks do not establish business verification.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
