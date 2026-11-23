# CES response contracts

The routes below are templates from retained CES GET captures.
Confirm the service origin, route revision, authentication, and capture completeness for the selected environment.
Find the route templates in the [variable template](../assets/variables.example.json). The inspector accepts local JSON bodies for these views.

| View | Route key under `ces.routes` | Body and identity |
| --- | --- | --- |
| Application catalog | `catalog` | Array of entitlement definitions. Bind the application to request metadata because the sampled rows omit it. |
| Effective user | `effective_user` | Array of account results. Match `user_data.app_name` and `user_data.user_id` to the requested scope. |
| Assigned role details | `assigned_roles` | User-wide array of role assignments. Bind the user to request metadata and select the application from its rows. |

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

The inspector expects objects for `data_policies` and `data_profiles` and an array for `data_entitlements` when present.

## Assigned role details

- `appName` names the application and `appId` is a string selector on assigned-role rows.
- `appUID` is its internal numeric UID. `itamId` can be null in captured role rows.
- Each selected row binds its `entitlementName` to its `featureActionDtos[]`.
- Feature/action objects use `features.featureName` and `actions.actionName`. Their nested `applicationDto` supplies application identity.
- An explicit empty `featureActionDtos` list retains the assignment with zero recorded grants.
- The supplied role view omits a user identifier. Check the captured request before attributing the rows to an account.

The inspector checks nested application identity when present. It rejects conflicting selected identities and omitted grant arrays.
An observed role grant supplies entitlement-level attribution. The effective-user view supplies resolved, account-level access.

It rejects missing required fields, conflicting identity, and duplicate entries within the supported records.
The files in `assets/` illustrate the supported fields with synthetic data.
The script checks this subset of the captured formats. Service-wide pagination, error, and authorization behavior need their own source.
