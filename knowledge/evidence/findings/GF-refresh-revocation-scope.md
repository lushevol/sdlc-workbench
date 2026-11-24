---
type: GovernanceFinding
id: GF-refresh-revocation-scope
version: 1
owner: unknown
governance_state: candidate
status: draft
sources: &id001
- resource: git://single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: b71df7273263aa8c17b8ea58e9e727008b108ec51ffdc70e266207ed07efad4a
- resource: git://single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: 548150730664b0417dcc115ede889b74536a207938a2912e7da2231d6184b41e
- resource: git://single-ui-bff/src/main/resources/db/migration/V1_0_2__fmo_schema_config.sql
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: f3e2bf950bc7b41709a8c90d1031456f0c69955f0d2e6232cf26dac1532865d2
- resource: git://single-ui-bff/src/main/resources/application.yml#L73-L76
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: 20928e87c49fe09880b3737341e592c320e12ff74cb46165b896acf4fee2086c
- resource: git://single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: c5cb0cb4a7a00663deaaa169837cd607bbaf35f8bf3eda04ffbe951b246d06af
- resource: git://single-ui-auth-sdk/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: dd0c58c0f226a28ca7eab10d8a7955baa30061c192008dc77b1096b6e574ee9d
- resource: git://single-ui-auth-sdk/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 48cfea2643775aa3c936e8391a0f2c1bcdba9a540e4b7761848a35906793ecba
generated:
  by: agent:codex
  at: '2026-10-15T14:18:44.259641+00:00'
verified: []
subject:
  id: ARCH-authentication-runtime-baseline
  version: 1
category: revocation_scope_unknown
severity: warning
evidence: *id001
proposed_action: Confirm the required logout boundary and test refresh-token reuse across cleanup and downstream
  instances.
resolution: open
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# Refresh-token revocation scope

## Subject

The [authentication code baseline](../candidates/architecture/ARCH-authentication-runtime-baseline.md) records the supplied session and SDK paths.
This finding concerns logout revocation while refresh tokens can remain unexpired.
It does not establish an observed deployed defect.

## Evidence

The BFF inserts the access token's session ID during logout.
Relogin validates refresh-token blacklist membership through the same session service.
Evidence: [BFF logout and relogin](<../raw/code/single-ui-bff/091c9d16c13f285a78463ff0235c21b152844b61/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java.snapshot#L358>); [BFF blacklist lookup](<../raw/code/single-ui-bff/091c9d16c13f285a78463ff0235c21b152844b61/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java.snapshot#L18>).

The migration defines an insert-triggered deletion of blacklist rows older than 15 minutes.
Its deletion target uses an unqualified table name.
Effective deployment, schema lookup, and later migrations remain unconfirmed.
Evidence: [Blacklist cleanup migration](<../raw/code/single-ui-bff/091c9d16c13f285a78463ff0235c21b152844b61/src/main/resources/db/migration/V1_0_2__fmo_schema_config.sql.snapshot#L25>).

The recorded JWT defaults specify 225 refresh-token minutes.
Generation adds another 24,000 milliseconds.
Refresh tokens carry the session ID and omit the access token's absolute-time claim.
Evidence: [Recorded JWT defaults](<../raw/code/single-ui-bff/091c9d16c13f285a78463ff0235c21b152844b61/src/main/resources/application.yml.L73-L76.snapshot#L1>); [Refresh-token generation](<../raw/code/single-ui-bff/091c9d16c13f285a78463ff0235c21b152844b61/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java.snapshot#L53>); [BFF logout and relogin](<../raw/code/single-ui-bff/091c9d16c13f285a78463ff0235c21b152844b61/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java.snapshot#L358>).

The SDK constructs a filter-local blacklist and checks it only when the token contains a session ID.
A checked logout URI adds that ID to the filter-local list.
No supplied consumer establishes shared deployment or global logout propagation.
Evidence: [SDK filter configuration](<../raw/code/single-ui-auth-sdk/b0aa82005e7f14202f85f5ef583f25e42da9eeb3/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java.snapshot#L20>); [SDK filter](<../raw/code/single-ui-auth-sdk/b0aa82005e7f14202f85f5ef583f25e42da9eeb3/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java.snapshot#L35>).

Inference: Cleanup could remove a BFF revocation record while its refresh token remains unexpired.
That inference depends on the migration's actual table resolution and the absence of replacement controls.
No environment execution tested that condition.

Consequence: The supplied evidence cannot establish universal logout revocation throughout the refresh-token lifetime.
Owner: unknown.

## Proposed action

Confirm the required boundary across the current browser, other tabs, devices, and downstream services.
Inspect applicable migrations, table lookup, SDK consumers, and replacement revocation controls.
Retain a controlled logout-and-reuse execution with exact revisions and token lifetimes.
Record response codes and new-token counts before and after cleanup.
Do not reuse real credentials or token values in the resulting knowledge.

## Resolution

open

Owner: unknown.
Next action: assign the session owner and verify the required revocation predicate in the supported environment.
The session-renewal pilot does not change this boundary.
