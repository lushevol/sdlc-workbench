# CES response contracts

The variable template records the supplied UAT origin and route templates for the three CES GET views.
Confirm the route revision, authentication, and capture completeness for the selected environment. [Variable template](../assets/variables.example.json)

| View | Route key under `ces.routes` | Body and identity | JSON Schema |
| --- | --- | --- | --- |
| Application catalog | `catalog` | Array of entitlement definitions. Bind the application to the request metadata. | [Catalog](../schemas/catalog-response.schema.json) |
| Effective user | `effective_user` | Array containing zero or one record. Match `user_data.app_name` and `user_data.user_id` to the request. | [Effective user](../schemas/effective-user-response.schema.json) |
| Assigned role details | `assigned_roles` | User-wide array of role assignments. Bind the user to the request and select the application. | [Assigned roles](../schemas/assigned-role-response.schema.json) |

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

The Draft 2020-12 schemas describe the supported shapes in retained captures. Validate exported JSON bodies with a compatible local validator.
The inspector separately checks capture identity and duplicate grants or assignments. It uses the Python standard library.
Synthetic examples live under `assets/`. Confirm service-wide pagination, errors, and authorization behavior from a source for the selected scope.
