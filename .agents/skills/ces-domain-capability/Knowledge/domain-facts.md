# CES domain facts

These facts come from retained CES UAT and SDK captures in the Workbench source checkout.
They describe observed response shapes and source-specific examples. They do not define all CES service behavior or current policy.
The [source register](sources.json) supplies exact paths, revisions, hashes, and locators for each evidence class.

## Endpoint scope

| View | Observed UAT route | Evidence binding |
| --- | --- | --- |
| Application catalog | `/fmces/v1/entitlement/app/{itam_id}/{application}` | `http_sources` entries `catalog-a` and `catalog-b`; paired UAT exchanges for different applications |
| Effective user | `/fmces/v1/entitlement/app/{itam_id}/{application}/user/{user_id}` | `effective-user-a` and `effective-user-b`; separate account-scoped exchanges |
| Assigned roles | `/fmces/v1/entitlement/user/{user_id}` | `assigned_role_fixture` and pinned SDK client source; body has no account identity |

The observed UAT origin is `https://fmcesuat.gdc.standardchartered.com`.
The domain contract owns this base URL. The task selects the environment without redefining its endpoint.
The recorded origin grants no authorization to call CES.
The captured HTTP Date headers are from 3 November 2026. They do not establish present deployment or retrieval time.
Bearer headers appear in captured requests and the pinned SDK client. Permission scopes and service-side authorization behavior remain unknown.
Both effective-user captures and catalog B select ITAM `51358`, application `RATAN_ENTITLEMENT_RULE`.
Catalog A selects the same ITAM with application `FLOWZERO`. Its memberships cannot be reconciled with the RATAN effective-user captures.

## Response facts

The application catalog contains entitlement definitions, explicit member IDs, and feature/action pairs.
The catalog does not establish that every member has an effective-user response.
Catalog A contains 40 definitions, including two empty-grant and 11 empty-membership rows.
Catalog B contains 74 definitions, including 35 empty-grant and 17 empty-membership rows.
The packaged paired catalog bodies are sanitized projections. Their subset counts cannot replace original capture counts.
Large nested membership and grant arrays are sampled. Each projection records the original row, field, length, and selected range.

The assigned-role response preserves entitlement-to-feature/action provenance.
An assigned entitlement can have an explicit empty `featureActionDtos` array.
Its app identity includes `appId`, `appName`, and `appUID`. `itamId` was null in the retained SDK fixture.
Nested application metadata must agree with the selected application when present.
The supplied SDK fixture contains six rows, including three explicit empty-grant assignments.
It provides no captured HTTP status, response headers, account identity, environment, or observation time.

The [effective-user contract](../Contracts/README.md#effective-user) defines the observed fields and attribution limits.
Effective-user A contains five assignment names and 47 flattened grants. Effective-user B contains seven names and 31 grants.
These accounts differ. The two captures do not measure an account's before-and-after access.

## Access interpretation

Use the [access concepts](domain-model.md#access-concepts) to distinguish assignments, grants, data scope, and observed enforcement.

`function_entitlement` is a value-level contract under investigation.
The retained user direction requires exactly one functional profile for an assigned account and rejection checks for incompatible assignments.
Generic, System, and Service account cases remain distinct.
The five-second interval is a selected test target after CES confirms a change. It is not an approved CES NFR.
The register's `functional_profile_user_sources` binds these statements to the exact 17 November user answers.
The response field location, empty wire value, and live provisioning outcome remain unresolved.

## Source limits

The catalog and effective-user captures are structural evidence.
The assigned-role fixture is a supplied SDK test resource.
Historical candidate records remain draft and do not establish current authority, deployment, or live parity.
Use the schemas and inspector for structural checks. Use governed records and scoped execution evidence for policy conclusions.
