# CES investigation variables

Copy the [variable template](../assets/variables.example.json) into local task storage. Fill only fields relevant to the investigation.
Use the inputs from that copy when running the documented commands. The inspector takes explicit flags and paths.

| Input | How to bind it |
| --- | --- |
| `topic`, `environment` | Name the investigation and the environment where the response originated. Record replay or live separately in the evidence. |
| `account.id`, `account.type` | Use the exact account in the authorized capture. Keep human and general account types explicit. |
| `ces.base_url`, `ces.routes` | Fill the service origin from approved environment configuration. Confirm each route template against the applicable contract. |
| `ces.application_name`, `itam_id`, `assigned_role_app_id`, `application_uid` | Keep app name, external ITAM reference, assigned-role `appId`, and internal UID distinct. Supply sourced identifiers. |
| `query` | Use the exact entitlement, feature, action, or policy reference needed for the question. Preserve case and meaningful spaces. |
| `evidence` | Supply the local capture paths, observation time, and capture hash or source revision. |
| `functional_profile` | Supply the verified response locator and independent expected-value source. Bind the empty representation and test target separately when known. |

Keep live tenant values in the task's local copy and credentials in the approved secret store.
Keep packaged deployment fields unset. Update route templates in the example only when the source and scope support the change.
