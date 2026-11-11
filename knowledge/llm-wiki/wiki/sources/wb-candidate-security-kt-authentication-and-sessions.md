---
title: "Authentication and sessions"
type: source
tags: []
sources: []
source_file: raw/workbench/knowledge/candidates/security/KT-authentication-and-sessions.md
source: raw/workbench/knowledge/candidates/security/KT-authentication-and-sessions.md
source_hash: f24b8314e2d2acf1
last_updated: 2026-11-11
candidate_id: KT-authentication-and-sessions
candidate_version: 9
candidate_governance_state: candidate
candidate_status: draft
candidate_classification: security
workbench_origin: knowledge/candidates/security/KT-authentication-and-sessions.md
workbench_sha256: f24b8314e2d2acf1b0656d4324a20071f205c1240c9ebf4623c024e0efd8fdbb
workbench_status: candidate-derived
---

# Authentication and sessions

## Scope

This topic connects user authentication, portal sessions, and the supplied Entra migration materials.
It describes intended behavior, source design statements, and historical proposals.
It does not establish deployed behavior or approved security policy.

## Summary

The target portal authenticates users, obtains entitlements, and issues tokens for application requests.
Its session materials distinguish idle timeout, absolute timeout, refresh tokens, and repeated login.
Entra migration replaces the SSO provider while preserving separate entitlement and portal-session responsibilities.
Several intended timing and activation rules require reconciliation.

For all portal environments, the user selected denial when an authenticated SC user lacks any registered application entity entitlement.
This is user-stated intent, not approved policy or verified enforcement.
The [retained answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/ui-q-002-source.json) and [scope answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/ui-q-002-scope-source.json) preserve the selections.

## Documented knowledge

### Intended session renewal

The active-session requirement ([[wb-candidate-requirements-req-active-session-renewal]]) defines the ideal target behavior.
Eligible mouse, keyboard, and scroll activity must support continued portal-session renewal.
Elapsed time alone must not require fresh authentication while eligible activity and successful renewal continue.
The target includes continued renewal across the initial refresh-token expiry.

During manual recovery, the expiry prompt must remain open while renewal is pending.
Successful renewal must close the prompt exactly once after completion.
A rejected renewal must preserve the prompt and permit another renewal attempt under the canonical criterion conditions.
The requirement holds the canonical measurable scenarios. This topic creates no additional scenario or timeout setting.

The independent [intent-to-reality gap record](../../../../tasks/portal-background-session-20261019/09-intent-reality-gaps.md) holds actual implementation and observation comparisons.
Defects, passing observations, backlog, and deployment state do not redefine this intended behavior.
Human publication review remains pending for this candidate topic and its linked requirement.

### Current user-stated portal-entry rule

An authenticated SC user with no entitlement for any registered application entity must be denied portal entry.
The user selected this rule for local, test, UAT, and production environments.
The [owner answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/ui-q-002-owner-source.json) identifies `portal team` for this policy only.
User identity remains unknown. Portal-team authority and approval remain unconfirmed.
Approval for the intended applicability remains pending.

The answer defines no HTTP status, denial wording, or additional entity-versus-role semantics.

The [draft principles, line 14](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L14>) state the same denial direction.
The [older tile-security proposal, line 7](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L7>) instead permits entry for SC accounts.
Retain that conflicting proposal as historical evidence, not the selected user intent.
Neither historical source establishes approved applicability.

The SDK topic criterion ([[wb-candidate-security-kt-sdk-and-entitlements]]) defines the measurable business result.
The [clarification stage](../../../../tasks/ui-test-coverage-20261022/05-entry-clarification.md#ui-q-002) records resolution limits and the unchanged canonical case.


The user also selected denial for tiles without a configured EMS2 entity.
The SDK topic ([[wb-candidate-security-kt-sdk-and-entitlements]]) defines that separate rule across local, test, UAT, and production.

The empty-subject rule ([[wb-candidate-security-kt-sdk-and-entitlements]]) permits tile visibility and launch through one configured EMS2 entity.
The explicit user answer is the first-priority reference for this intended behavior.
The portal team owns this rule across local, test, UAT, and production.

### Authentication responsibilities

The Entra design describes a browser redirect followed by an authorization-code exchange through the BFF.
The BFF builds user information, retrieves EMS2 entitlements, and issues authentication and entitlement tokens.
Its design retains OneMFA fallback and a separate username/password path.
[Entra design, lines 7–31, 40–68](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/UI SSO Entra Design/page.md>)

The phase 1 scope separates authentication from authorization.
It includes UI SSO migration.
It excludes EMS2 replacement, portal session management, and tenant-onboarding authentication.
Machine-to-machine authentication has a separate migration document with unresolved central dependencies.
[Entra phase 1, lines 15–21, 48–57](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/page.md>)
[Service-account migration, lines 1–10](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal & RATAN Entra Migration - Phase 2 - service account/page.md>)

### Session concepts and intended lifecycle

The documents use an access token to authenticate application requests.
An idle timeout limits inactivity.
An absolute timeout limits the interval since authentication.
A refresh token supports another authentication interval without repeating the initial SSO journey.
These are documented concepts, rather than a confirmed runtime contract.
[Session version 0, lines 1–9, 19–24, 38–65](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 0/page.md>)
[Session version 1, lines 102–193](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md>)

Version 0 states limits below 60 minutes for absolute timeout and below 15 minutes for idle timeout.
Its examples use a 15-minute access token and a 24-hour refresh token.
It proposes an inactivity warning, session extension, single-device login, and reused-token rejection.
Those examples do not resolve the strict-limit wording or current implementation.
[Session version 0, lines 1–9, 19–24, 38–65](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 0/page.md>)

Version 1 proposes `exp = iat + 15 minutes` for idle timeout.
It relates absolute timeout to `auth_time` and a 60-minute `max_age` interval.
Its proposed flow obtains a refresh token before access-token expiry.
A later relogin exchanges the refresh token for another access token.
It places single-device login and token-blacklist work on a backlog.
[Session version 1, lines 102–193](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md>)

Version 1 contains both 105-minute and 225-minute refresh-token durations in the same calculation.
Its absolute-timeout discussion also proposes changing `auth_time` during continued activity.
These statements cannot define a single reliable timing rule without review.
[Session version 1, lines 102–193](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md>)

Version 1 also states that refresh tokens have no absolute timeout because they lack `auth_time` and `max_age`.
This is a proposed source statement alongside competing duration and `auth_time` rules, rather than accepted policy.
[Session version 1, lines 133–164](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md>)

### Entra onboarding and user profile

The non-production guide requires a development AD account, Authenticator registration, and RATAN AD-group membership.
It asks teams to check successful login, user information, and expected tile visibility.
Its FAQ associates missing entitlements with tile access and EMS2 configuration.
[Non-production verification guide, lines 5–56, 58–126](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Non Prod Verification/page.md>)

The production guide specifies the intended pilot-user authentication journey.
It describes Windows Hello or Authenticator authentication and an Entra session of one hour.
That provider-session statement does not settle the portal refresh-token lifetime.
[Production pilot guide, lines 1–2, 12–46, 48–86, 95–101](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md>)

The production guide warns that AD profile values differ from OUD values.
It identifies changed surname formatting, country codes, and missing locale values.
Downstream audit or application logic can therefore require profile-field review during migration.
[Production pilot guide, lines 1–2, 12–46, 48–86, 95–101](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md>)

### Historical machine-to-machine authentication

The historical FMAA reference describes client-credential authentication for machine-to-machine callers.
It separates service-account onboarding from bank-ID onboarding.
It describes OUD-managed accounts authenticated through FMAA.
It states 17-year validity for service accounts and seven-day validity for bank IDs.
Those historical values do not establish approved portal-session limits or current token policy.
[Historical FMAA reference, lines 11–13, 24–30, 36–50](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/Reference of FMAA API/page.md>)

## Connections

SDK and entitlements ([[wb-candidate-security-kt-sdk-and-entitlements]]) explains downstream token validation and entitlement responsibilities.
Admin and onboarding ([[wb-candidate-operations-kt-admin-and-onboarding]]) connects tenant setup with role and tile configuration.
Frontend composition ([[wb-candidate-architecture-kt-frontend-composition]]) explains the UI context for login and user state.

Registry capability `single-ui-authentication` connects declared repository and service identities.
Contract `single-ui-sso-token-family` supplies existing interface context for `single-ui-bff` and `mfe-base`.
These declarations do not prove that a migration design runs in any environment.

## Evidence limits

The supplied documents have local byte revisions, but no confirmed original page revisions or approval authority.
This limits their use as current security policy.
Owner: unknown.
Next action: establish the applicable versions with the responsible security and application owners.

Historical session designs contain unresolved timing proposals.
They cannot establish one intended timing policy without an authoritative decision.
Owner: unknown session owner. Next action: reconcile the intended timing rules before policy publication.
Implementation and execution comparisons remain in the independent task gap record.

The design uses `ENABLE_ENTRA_SSO=true/false`; the production guide uses `yes/no`.
The production guide describes both temporary activation and persistent activation after first use.
These differences can produce incorrect pilot or fallback instructions.
Owner: unknown.
Next action: resolve the intended activation grammar and persistence rule with the responsible owner.
[Entra design, lines 7–31, 40–68](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/UI SSO Entra Design/page.md>)
[Production pilot guide, lines 1–2, 12–46, 48–86, 95–101](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md>)

## Open questions

What evidence confirms portal-team authority and approval across the user-stated environments?
The [retained answers](../../../../tasks/ui-test-coverage-20261022/05-entry-clarification.md#ui-q-002) establish user-stated intent and owner identity only.
Consequence: policy publication requires applicable review and authority evidence.
Owner: `portal team`, user-reported for entry policy only.
Next action: obtain applicable authority and approval evidence.

Which intended timeout and refresh-duration rules apply to each supported environment?
The two session designs contain incompatible timing proposals.
Consequence: those proposals cannot define one authoritative target timing policy.
Owner: unknown session owner. Next action: review the intended timing table and token-reuse rule.
[Session version 0](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 0/page.md>)
[Session version 1](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md>)

Which intended migration scope and authentication responsibilities have authoritative approval?
The supplied plans and guides require an applicable design decision.
Consequence: historical schedules cannot select the target provider and fallback policy.
Owner: unknown migration owner. Next action: confirm the intended provider contract and supported fallback boundaries.

Which documented FMAA flows and validity settings remain intended requirements?
The historical reference supplies exceptional validity examples.
Consequence: copying those values into a target rule requires authoritative policy evidence.
Owner: unknown authentication owner. Next action: confirm the intended provider contract and validity limits for each supported flow.
[Historical FMAA reference](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/Reference of FMAA API/page.md>)

The renewal requirement ([[wb-candidate-requirements-req-active-session-renewal]]) holds the canonical target criteria.
The independent [gap record](../../../../tasks/portal-background-session-20261019/09-intent-reality-gaps.md) holds actual behavior and evidence limitations.
