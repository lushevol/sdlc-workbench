---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Spring example: verify EMS2 to CES SDK outputs

> **Run this project inside the company network to measure actual SDK permission parity.**
> Action: supply the complete account inventory, reviewed mappings, endpoints, and authorized credentials.
> Consequence: a local replay cannot establish complete migration or seamless application behavior.
> Owner: company execution owner, unknown.
> Evidence: [user request](../evidence/spring-verifier-20261104/user-input.md#exact-user-input).

This executable Spring Boot application invokes `AuthorizationService.getEntitlements(String userId)` through both actual SDK artifacts.
Separate class loaders prevent their identical package names from shadowing each other.
The project does not change either SDK or any company permissions.

| SDK | Exact source revision | Artifact |
| --- | --- | --- |
| EMS2 baseline | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3` | `lib/ems2-sdk.jar` |
| CES candidate, version `3.0.0` | `fd9a157e260850b6d9efa10da3223950ea61133a` | `lib/ces-sdk.jar` |

## 1. Prepare both SDKs

Install approved JDK 17+, Maven 3.8+, Git, and Python 3.10+.
Use the [dependency guide](docs/DEPENDENCIES.md) for approved downloads, offline preparation, deadlines, and recovery.
The root Workbench installer does not install this task-specific Java environment.

Run from this directory:

```sh
python3 prepare-sdks.py --sdk-repo ../../../repos/libraries/single-ui-sdk-starter --check
python3 prepare-sdks.py --sdk-repo ../../../repos/libraries/single-ui-sdk-starter
```

Use `py -3` on Windows.
Use `--java-home PATH` when the default JDK differs.
Both exact revisions must already exist in the independent SDK checkout.
Preparation exports source into temporary directories and runs the original tests.
It retains artifact hashes, exact commands, source hashes, test counts, and build logs under `lib/`.
Existing artifacts require a new `--output` directory.

Preparation bounds each SDK build to 600 seconds, including package acquisition.
Use company Maven settings and mirrors for restricted package access.
For transferred dependencies, use `--offline --maven-repository PATH`.
Restore missing packages before retrying. Do not skip failed tests.

## 2. Build and run the local example

```sh
mvn -B clean verify
./run.command
```

On Windows, run `run.cmd` after the same Maven build.
The launcher uses the packaged application without downloading dependencies.
The default replay serves synthetic EMS2 and CES responses over loopback HTTP.
The actual SDK jars execute their original one-argument lookup methods.
The fixture includes human and service accounts, three legacy entities, duplicate actions, and an empty role.

Run these deliberate negative examples:

```sh
./run.command --verification.replay.variant=missing
./run.command --verification.replay.variant=extra
./run.command --verification.replay.variant=failure
./run.command --verification.replay.variant=malformed
./run.command --verification.replay.variant=empty
./run.command --verification.population-complete=false
```

Use the same arguments with `run.cmd` on Windows.
Missing or additional grants return exit `1`. Failed acquisition or incomplete population returns exit `2`.
The valid empty fixture matches, but its permission denominators remain empty.
Its account parity percentage does not represent permission coverage.

## Local verification result

The retained [complete build](../evidence/spring-verifier-20261104/full-build-05/result.json) passed 32 tests without failures, errors, or skips.
The [actual-SDK replay suite](../evidence/spring-verifier-20261104/actual-sdk-replays-05/result.json) passed all eight declared checks.
The [credential guard](../evidence/spring-verifier-20261104/missing-live-token-final/result.json) stopped live startup before lookup when its CES token was absent.
The SDK candidate also passed all 44 existing tests through qualified offline module goals.
Ordinary offline SDK packaging remained blocked by unavailable formatter dependencies.
The [artifact provenance](../evidence/spring-verifier-20261104/qualified-sdk-preparation/preparation.json) keeps that limitation separate from runtime JAR qualification.

## 3. Configure company-network execution

Copy these files before changing them:

```sh
cp config/live.properties.example config/live.local.properties
cp config/company-mappings.json.example config/company-mappings.local.json
cp config/users.csv.example config/users.local.csv
```

On Windows Command Prompt, use `copy` instead of `cp`.
All `*.local.*` configuration files are ignored by Git.
The shipped account IDs and mappings are sample-derived proposals. They are not a complete reviewed inventory.

1. Replace `users.local.csv` with the authoritative complete account list for the declared scope.
2. Include human accounts, service accounts, and valid accounts with no assignments.
3. Review every entity, application, role alias, subject alias, and feature selector in the mapping file.
4. Set `verification.population-source` to the retained inventory record and its revision.
5. Set `verification.population-complete=true` only after that inventory is confirmed complete.
6. Set both base URLs through `SDK_VERIFY_EMS2_BASE_URL` and `SDK_VERIFY_CES_BASE_URL`.
7. Provision `SDK_VERIFY_CES_TOKEN` through the company's approved secret mechanism.
8. Set `SDK_VERIFY_EMS2_TOKEN` when the legacy gateway requires an authorization header.

The CES token must omit the `Bearer ` prefix.
The optional EMS2 token accepts a raw bearer token or a complete `Bearer ` or `Basic ` value.
Credentials must not appear in command arguments, committed configuration, or shared reports.

The CES endpoint must return assigned roles with role provenance:

```json
[
  {
    "appId": "APP_ID",
    "appName": "APP_NAME",
    "entitlementName": "ROLE_NAME",
    "featureActionDtos": [
      {"features": {"featureName": "SUBJECT"}, "actions": {"actionName": "view"}}
    ]
  }
]
```

An aggregate effective-user payload cannot establish this role-specific contract.
Confirm the actual assigned-role endpoint and path with its owner.
The CES path uses `{userId}`. The EMS2 account path uses `%s`.
Review the exact API contracts in the [SDK review](../10-change-review-sdk-function-coverage.md#current-task-state).

## 4. Run against company endpoints

```sh
./run.command --spring.config.additional-location=file:config/live.local.properties
```

Windows:

```bat
run.cmd --spring.config.additional-location=file:config/live.local.properties
```

Run against compatible populations and a controlled observation window.
An EMS2 PROD versus CES UAT difference can reflect provisioning drift.
It does not alone establish an adapter defect.
Record the actual deployment builds, environments, configuration, inventory revision, and observation window with the report.
The verifier cannot independently authenticate those deployment identities.

Requests use normal JVM certificate validation and bounded connect/read timeouts.
Redirects are disabled. Responses are limited to 8 MiB each.
Configure approved JVM trust stores and proxy settings when company routing requires them.
Each account can issue two EMS2 requests and one CES request. Accounts run sequentially.
No request retry or background polling runs.
Coordinate the population size and observation window with the endpoint owners.

## 5. Read the result

Each execution creates a unique directory under `reports/`:

| File | Evidence |
| --- | --- |
| `report.html` | Local summary, per-account differences, and complete expandable evidence. |
| `report.json` | Exact outputs, metrics, errors, hashes, and scope declarations. |
| `report.md` | Portable complete report. |
| `accounts/00001.json` | Account evidence saved immediately after that lookup pair completes. |
| `progress.json` | Latest completed account checkpoint when execution is interrupted. |

The report compares role keys, subjects, action values, occurrence counts, and action order.
It also compares effective permissions without allowing that union to hide role-specific differences.
Missing empty roles and duplicate loss remain differences.
HTTP errors, malformed payloads, missing artifacts, and uncertain acquisition remain unassessed.
Request evidence retains status codes, redacted paths, byte counts, and response hashes.
Raw HTTP response bodies and authorization headers are not retained.
Reports contain account IDs and permission maps. Store them through the company's approved evidence process.

| Result | Exit | Meaning |
| --- | --- | --- |
| `SCOPED_SDK_PARITY_PASS` | `0` | Every declared account completed with exactly equal SDK maps and a complete population declaration. |
| `DIFFERENCES` | `1` | Acquisition completed, but at least one declared account has missing or additional content or order changes. |
| `INCOMPLETE` | `2` | Configuration, acquisition, artifacts, or population completeness prevented a full scoped comparison. |

Check additional counts even when a baseline coverage metric shows `100%`.
The pass condition requires zero differences and zero unassessed accounts.
`migrationVerified` remains `false` because this project measures SDK-map parity only.

## 6. Establish complete migration acceptance

Use the [existing API coverage tool](../coverage/README.md#run-all-coverage) for inventory and supplied API contract comparisons.
This Spring project adds actual SDK invocation to those checks.
Complete migration acceptance also requires evidence for these boundaries:

| Boundary | Required evidence outside this command |
| --- | --- |
| Entire population and scope | Authoritative complete accounts, roles, entities, features, and exclusion decisions. |
| Unassigned role definitions | Full role-to-subject-to-action catalog equality. |
| Data restrictions | Authoritative definitions and resolved values beyond SDK marker permissions. |
| Actual application adoption | Compile, start, and exercise each consuming application with SDK `3.0.0`. |
| Seamless user behavior | Assert allowed and denied business actions, token renewal, expired tokens, logout, and replay handling. |
| Company execution | Matching deployment identities, authorized requests, correlations, and remote runtime log evidence. |

A `100%` scoped result supports its declared SDK predicate.
It cannot prove the unexecuted boundaries above.
The [stage review](../10-change-review-spring-verifier.md#stage-evidence-and-completion) records local results and traceability.
