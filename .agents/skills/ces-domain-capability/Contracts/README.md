# CES response contracts

Use the [OpenAPI 3.1 subset](openapi.yaml) for the three inspected CES views.
The [source register](../Knowledge/sources.json) binds exact revisions, hashes, request/response locators, and evidence limits.
Select the active origin and route from the task's [variable copy](../Workflows/variables.example.json).
Bearer authentication appears in retained client requests and SDK source. Required scopes and unauthenticated behavior remain unknown.

| View | Route key under `ces.routes` | Body and identity | JSON Schema |
| --- | --- | --- | --- |
| Application catalog | `catalog` | Array of entitlement definitions. Bind the application to the request metadata. | [Catalog inspection schema](schemas/catalog-response.schema.json) |
| Effective user | `effective_user` | Match `user_data.app_name` and `user_data.user_id` to the request. | [Effective-user inspection schema](schemas/effective-user-response.schema.json) |
| Assigned role details | `assigned_roles` | User-wide role array. Bind the account to the request and select the application. | [Assigned-role inspection schema](schemas/assigned-role-response.schema.json) |

## Paired cases and supplied bodies

| Case | Request variation and observed result | Limit |
| --- | --- | --- |
| [Effective user A](examples/effective-user-a-uat-pair.json) | One account: HTTP 200, five assignments, 47 flattened grants | Sanitized observation; account differs from case B |
| [Effective user B](examples/effective-user-b-uat-pair.json) | Another account: HTTP 200, seven assignments, 31 flattened grants | A separate account, not an after-change capture |
| [Catalog A](examples/catalog-a-uat-pair.json) | FLOWZERO: HTTP 200; selected normal, empty-grant, and empty-membership rows | Projected subset of 40 source definitions |
| [Catalog B](examples/catalog-b-uat-pair.json) | RATAN_ENTITLEMENT_RULE: HTTP 200; selected structural variants | Projected subset of 74 source definitions |
| [Assigned-role body](examples/assigned-role-body-fixture.json) | Sanitized SDK fixture with role-level grouping and empty grant arrays | Request, HTTP status, headers, account, and capture time were not retained |

The four HTTP cases preserve request/response pairing and the original source hash.
Account aliases replace user IDs and policy/profile owner identities consistently. Authorization values are redacted.
Application, entitlement, feature/action, policy/profile names, group keys, and data-scope values retain their source values.
Catalog projections state their selected source indexes.
Large membership and grant arrays retain their first two entries, with original lengths and exact ranges recorded.
These projections cannot establish absent memberships or complete catalog counts from their example bodies.
HTTP Date headers describe retained server responses. They are not independent retrieval timestamps.
No captured HTTP failures, request payload variations, query parameters, or continuation exchanges accompany these four cases.

The assigned-role body retains its original field values. It is a supplied fixture, with no accompanying HTTP exchange.
Controlled synthetic inputs remain in Workbench tests, outside this portable library.

## Application catalog

- Read `entitlement_name` as an application-scoped name.
- Read `role_entitlements[]` as pairs with `feature` and `action`.
- Read `user_ids` as an explicit array of account ID strings.
- Keep `entitlement_id` as source metadata when present.
- Check request and collection completeness before concluding an entitlement or membership is absent.

## Effective user

- Read `user_data.app_name` and `user_data.user_id` before interpreting the grants.
- Keep `user_data.itam_id`, when present, as an external application reference.
- Read `entitlements.entitlement_name[]` as assigned names.
- Read `entitlements.role_entitlements[]` as effective feature and action pairs.
- Inspect `entitlements.data_policies`, `data_profiles`, and `data_entitlements` as separate optional sections.
- Distinguish an empty response array from a matching result with explicit empty assignment and permission arrays.

`data_policies` and `data_profiles` contain named groups of policy or profile rules.
`data_entitlements[]` carries a string `key` and a `values` array of strings.

## Assigned role details

- `appName` names the application and `appId` is a string selector on assigned-role rows.
- `appUID` is its internal numeric UID. `itamId` can be null in captured role rows.
- Each selected row binds its `entitlementName` to its `featureActionDtos[]`.
- Feature/action objects use `features.featureName` and `actions.actionName`. Their nested `applicationDto` supplies application identity.
- An explicit empty `featureActionDtos` list retains the assignment with zero recorded grants.
- The supplied role view omits a user identifier. Check the captured request before attributing the rows to an account.

The inspector checks nested application identity when present. It rejects conflicting selected identities and omitted grant arrays.
An observed role grant supplies entitlement-level attribution. The effective-user view supplies resolved, account-level access.

## Schema and transport limits

OpenAPI observation schemas retain supported field types while leaving service-wide requiredness and bounds unconfirmed.
The separate Draft 2020-12 inspection schemas define the complete local inputs accepted by the offline inspector.
Their `required` fields and single-record constraint are inspector requirements, not inferred CES-wide guarantees.
Full schema validation requires a Draft 2020-12 validator, separate from the standard-library inspector.
Workbench's Python environment already includes `jsonschema`. From the skill folder, validate an exported effective-user body:

```sh
python3 - "$CES_BODY_JSON" Contracts/schemas/effective-user-response.schema.json <<'PY'
import json
import sys
from jsonschema import Draft202012Validator

with open(sys.argv[1], encoding="utf-8") as stream:
    body = json.load(stream)
with open(sys.argv[2], encoding="utf-8") as stream:
    schema = json.load(stream)
Draft202012Validator(schema).validate(body)
print("Schema validation passed.")
PY
```

Use the corresponding schema for catalog or assigned-role bodies. Select a Python environment with `jsonschema` available.
Standalone inspector checks cover operational inputs. They do not validate every nested data-policy or profile field.
The inspector separately checks capture identity and duplicate grants or assignments. It uses the Python standard library.
Confirm pagination, errors, authorization, defaults, and nullability outside the captured values from sources for the selected scope.
The assigned-role OpenAPI response uses `default` with a local body-schema reference because no HTTP status accompanied its fixture.
