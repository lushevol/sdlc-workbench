---
type: GovernanceFinding
id: FND-sdk-authorization-enforcement
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 48cfea2643775aa3c936e8391a0f2c1bcdba9a540e4b7761848a35906793ecba
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: d41ab828e2295fa4e5d4ccbe87d8a80e54522e0aa9df88f9dd8bfd085d09274f
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: dd0c58c0f226a28ca7eab10d8a7955baa30061c192008dc77b1096b6e574ee9d
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 09d8595302dd702b8f38c298ff9e5a91f6107678ffd61714b540253605bcc161
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/AuthorizationService.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: cc81a872b3565aa58175e6f8630667e776d102e0ebc160d488f4ce0691f5edab
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 74587cf78a69e0c9b7b3920d510248acd5501dbaa7ac27035b3b9c5fc91bc2d1
generated:
  by: agent:codex
  at: '2026-10-14T01:33:53.488111+00:00'
verified: []
subject:
  id: ARCH-sdk-e2e-contracts
  version: 2
category: missing_permission_enforcement_evidence
severity: warning
evidence:
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 48cfea2643775aa3c936e8391a0f2c1bcdba9a540e4b7761848a35906793ecba
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: d41ab828e2295fa4e5d4ccbe87d8a80e54522e0aa9df88f9dd8bfd085d09274f
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: dd0c58c0f226a28ca7eab10d8a7955baa30061c192008dc77b1096b6e574ee9d
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 09d8595302dd702b8f38c298ff9e5a91f6107678ffd61714b540253605bcc161
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/AuthorizationService.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: cc81a872b3565aa58175e6f8630667e776d102e0ebc160d488f4ce0691f5edab
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 74587cf78a69e0c9b7b3920d510248acd5501dbaa7ac27035b3b9c5fc91bc2d1
proposed_action: Identify a downstream owner and inspect permission checks before claiming API authorization
  enforcement.
resolution: open
consequence: Authentication and entitlement lookup do not establish action or role enforcement in a downstream
  service.
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# Downstream authorization evidence remains missing

## Subject

`ARCH-sdk-e2e-contracts`, version 2.
The supplied SDK declares token authentication and a separate entitlement lookup API.
No consuming service was supplied for permission enforcement review.

## Evidence

The retained [filter](../raw/2026-10-14-sdk-e2e-registration/single-ui-auth-sdk/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java.snapshot) validates tokens and maps claims into serialized JSON `userInfo`.
It sets `version` to string `3` in that request attribute.
It copies optional `entitlements` and `oud` claims without checking action or role permissions.
A configured skip header bypasses authentication when its incoming request value is nonempty.
URL exclusions also bypass checks.
Logout rejection uses local filter state.

The retained [configuration](../raw/2026-10-14-sdk-e2e-registration/single-ui-auth-sdk/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java.snapshot) declares an `AuthorizationService` bean.
The retained [implementation](../raw/2026-10-14-sdk-e2e-registration/single-ui-auth-sdk/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java.snapshot) retrieves EMS2 roles and entitlements.
Its return value maps entities, roles, subjects, and action names.
The filter does not call this service.
No retained execution proves downstream authorization or distributed session revocation.

Consequence: Claiming complete API authorization would exceed the inspected evidence.
A downstream caller can require permission checks beyond token validation.
This finding records missing integration evidence. It does not establish a confirmed SDK defect.

Owner: unknown.

## Proposed action

Identify a current downstream service and its accountable owner.
Inspect dependency configuration, filter activation, trusted bypass settings, and action or role permission checks.
Retain allowed and rejected request results against measurable acceptance scenarios.
Record human review before publishing important authorization decisions.

## Resolution

open

Downstream permission enforcement and ownership remain unresolved.
