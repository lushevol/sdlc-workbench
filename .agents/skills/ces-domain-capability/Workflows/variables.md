# CES investigation variables

Copy the [variable template](variables.example.json) into local task storage. Fill only fields relevant to the investigation.
Use the inputs from that copy when running the documented commands. The inspector takes explicit flags and paths.
This template records task bindings. It does not load environment variables or acquire credentials automatically.
The domain library owns the observed base URL, route templates, API version, media types, and authentication scheme in its Contracts and Knowledge files.

| Input | How to bind it |
| --- | --- |
| `topic`, `environment` | Name the investigation and the environment where the response originated. Record replay or live separately in the evidence. |
| `account.id`, `account.type` | Use the exact account in the authorized capture. Keep human and general account types explicit. |
| `ces.token_env` | Record the environment-variable name consumed by the selected client. Required only for an authorized live step using that credential. Never put the token here. |
| `ces.ca_env` | Record the selected client's environment-variable name for a trusted CA file, when needed. Keep the machine-specific path outside the skill. |
| `ces.application_name`, `itam_id`, `assigned_role_app_id`, `application_uid` | Keep app name, external ITAM reference, assigned-role `appId`, and internal UID distinct. Supply sourced identifiers. |
| `query` | Use the exact entitlement, feature, action, or policy reference needed for the question. Preserve case and meaningful spaces. |
| `evidence` | Supply local catalog, assigned-role, effective-user, and comparison body paths. Retain each request identity, observation time, and hash or revision. |
| `functional_profile` | Supply the sourced JSON Pointer and independent expected-value JSON file. Bind the empty representation and timing target separately. |

Keep stable contract properties in the domain library. Keep dynamic selectors and resolved investigation values in the task's local copy.
Credentials come from the selected runtime environment or approved secret-store injection, never this JSON file.
Read the observed CES origin and route templates from [the contract](../Contracts/openapi.yaml) and [source-bound facts](../Knowledge/domain-facts.md).
If an adapter needs a local copy of a contract property, validate it against the domain contract. Do not create a second domain definition.
`functional_profile.value_locator` is relative to the effective-user record, without the outer response array index.
`expected_value_path` names a local file containing one JSON string or `null`, justified by its independent source.
The example leaves the profile locator, empty representation, and timing target unset.
Reconciliation requires all three captures to describe the same account, application, environment, and compatible observation boundary.
The tool checks response identities where available. The operator must bind identities omitted from catalog and assigned-role bodies.

## External dependencies and resolution

Offline inspection needs local response bodies and explicit selectors. It needs no live credentials or network access.
Missing live credentials do not block extraction of supported contracts or offline inspection.
For a separately authorized live collection, use the existing client and its credential and dynamic-input bindings.
Record environment-variable names, dynamic inputs, required values, and confirmed precedence before executing that step.
Do not assume every CES client uses the same variable names or dotenv behavior.

The existing Workbench coverage helper mirrors these domain properties and uses these external bindings:

| Binding | Existing consumer behavior |
| --- | --- |
| CES base URL and route paths | The domain contract records the observed origin and routes. The helper's local config mirrors them for its adapter and must remain aligned with the contract. |
| `ces.token_env` | Names the credential environment variable. The retained migration configuration selects `CES_COVERAGE_BEARER_TOKEN`. |
| `ces.ca_env` | Names the CA-file environment variable. The retained configuration selects `CES_COVERAGE_CA_FILE`. |
| Selected workspace `.env` | Loaded by the existing helper only for live mode. Process variables override file values, including empty values. |
| CA-file resolution | A configured relative CA path resolves from the selected workspace root. The HTTP client otherwise uses `SSL_CERT_FILE` or system trust. |

These credential and CA bindings are scoped to that helper. They are not universal CES API requirements or defaults for standalone copies.
Source checkout, revision `d684799f3`: `core/entitlement_coverage.py` (`Collector.get`, `run`), `core/entitlement_sources.py` (`load_root_env`, `JsonHttpClient.request`), `core/doctor.py` (`_environment`), and `tasks/ces-entitlement-migration-20261102/coverage/config.json` (`/ces`).
Those files can be unavailable in a standalone copy. Inspect the selected project's client before reusing these bindings.

Before a live step, confirm required credential bindings and dynamic inputs without printing values.
Report missing key names and the affected step. Keep that step unexecuted until its dependencies are supplied.
Use the configured secret provider for acquisition or renewal. Do not extract a token from retained examples or another project.
Keep environment dumps, resolved credentials, and Authorization values out of commands, reports, and captures.
Credential presence alone does not prove validity, permission, network availability, or successful authentication.
