# CES investigation variables

Copy the [variable template](variables.example.json) into local task storage. Fill only fields relevant to the investigation.
Use the inputs from that copy when running the documented commands. The inspector takes explicit flags and paths.

| Input | How to bind it |
| --- | --- |
| `topic`, `environment` | Name the investigation and the environment where the response originated. Record replay or live separately in the evidence. |
| `account.id`, `account.type` | Use the exact account in the authorized capture. Keep human and general account types explicit. |
| `ces.origins.uat`, `ces.base_url`, `ces.routes` | Select the named UAT origin when UAT is in scope. Set the active base URL in the local copy and confirm the route against the applicable contract. |
| `ces.application_name`, `itam_id`, `assigned_role_app_id`, `application_uid` | Keep app name, external ITAM reference, assigned-role `appId`, and internal UID distinct. Supply sourced identifiers. |
| `query` | Use the exact entitlement, feature, action, or policy reference needed for the question. Preserve case and meaningful spaces. |
| `evidence` | Supply local catalog, assigned-role, effective-user, and comparison body paths. Retain each request identity, observation time, and hash or revision. |
| `functional_profile` | Supply the sourced JSON Pointer and independent expected-value JSON file. Bind the empty representation and timing target separately. |

Keep live tenant values in the task's local copy and credentials in the approved secret store.
The example records the supplied CES UAT origin under `ces.origins.uat`.
Select the environment and active base URL in the local copy.
`functional_profile.value_locator` is relative to the effective-user record, without the outer response array index.
`expected_value_path` names a local file containing one JSON string or `null`, justified by its independent source.
The example leaves the profile locator, empty representation, and timing target unset.
Reconciliation requires all three captures to describe the same account, application, environment, and compatible observation boundary.
The tool checks response identities where available. The operator must bind identities omitted from catalog and assigned-role bodies.
