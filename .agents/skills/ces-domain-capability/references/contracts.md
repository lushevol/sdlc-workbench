# CES response contracts

The routes below are templates from retained CES GET captures.
Confirm the service base URL, route revision, authentication, and capture completeness for the selected environment.
The included inspector accepts exported JSON response bodies from these two views.

| View | Observed route template | Body and identity |
| --- | --- | --- |
| Application catalog | `/fmces/v1/entitlement/app/{itam_id}/{application}` | Array of entitlement definitions. Bind the application to request metadata because the sampled rows omit it. |
| Effective user | `/fmces/v1/entitlement/app/{itam_id}/{application}/user/{user_id}` | Array of account results. Match `user_data.app_name` and `user_data.user_id` to the requested scope. |

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
It rejects missing required fields, conflicting identity, and duplicate entries within the supported records.
The files in `assets/` illustrate the supported fields with synthetic data.
The script checks this subset of the captured formats. Service-wide pagination, error, and authorization behavior need their own source.
