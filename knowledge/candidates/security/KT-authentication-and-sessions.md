---
type: KnowledgeTopic
id: KT-authentication-and-sessions
version: 2
owner: unknown
governance_state: investigated
status: draft
sources:
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control
    and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 0/page.md
  revision: sha256:ea697bdb2fc3ee5adf8bcfe67a38ac4df756efc189a729e664c194dff4ce91ed
  sha256: ea697bdb2fc3ee5adf8bcfe67a38ac4df756efc189a729e664c194dff4ce91ed
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control
    and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md
  revision: sha256:66fa08bf2807a8ae864f8cdda0856b531fceffe11dd655b2bde45ce322ee2ac7
  sha256: 66fa08bf2807a8ae864f8cdda0856b531fceffe11dd655b2bde45ce322ee2ac7
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post
    Trade Portal Entra Migration - Phase 1 - UI SSO/page.md
  revision: sha256:d035c6cb7803bb6b1011befc428e125bf4e1c466dcf845e0a359a5a7e947dd5d
  sha256: d035c6cb7803bb6b1011befc428e125bf4e1c466dcf845e0a359a5a7e947dd5d
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post
    Trade Portal Entra Migration - Phase 1 - UI SSO/UI SSO Entra Design/page.md
  revision: sha256:e52e079787b9cf1b30a5b16535b9b455e302a647b33ec6715424d0be9c52daee
  sha256: e52e079787b9cf1b30a5b16535b9b455e302a647b33ec6715424d0be9c52daee
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post
    Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md
  revision: sha256:0979a0498132d53449ad1c74a2323f2f2396fefcf6af1afc0f92215237e48957
  sha256: 0979a0498132d53449ad1c74a2323f2f2396fefcf6af1afc0f92215237e48957
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post
    Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Non Prod Verification/page.md
  revision: sha256:37b2b6ced13197b54ee429535d8716cc63bb3fff87212f5d3418781c6d9687b0
  sha256: 37b2b6ced13197b54ee429535d8716cc63bb3fff87212f5d3418781c6d9687b0
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post
    Trade Portal & RATAN Entra Migration - Phase 2 - service account/page.md
  revision: sha256:1fec370791ec875c7ae61a2084fec02e192378e055957c0647eedca9822048dd
  sha256: 1fec370791ec875c7ae61a2084fec02e192378e055957c0647eedca9822048dd
- resource: "knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/Penetration\
    \ Testing report for SPT001414 \u2013 SSI+ BA/page.md"
  revision: sha256:86953471062331bc2092737467b10269c101513fdc6cf52617882359a080ef84
  sha256: 86953471062331bc2092737467b10269c101513fdc6cf52617882359a080ef84
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/WAS
    Scan Report SIA-ETASK1854215- 11282023/page.md
  revision: sha256:b2677f993b154c2705c4fe103d5e2bbff1a45b618f0129ae0234fa69c381b692
  sha256: b2677f993b154c2705c4fe103d5e2bbff1a45b618f0129ae0234fa69c381b692
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/Web
    Application Vulnerability Scan - SIA-API-ETASK1837309-01122023/page.md
  revision: sha256:3f1d4d92134c3eee85f2955b685cd68d7bf32a4ee8005cfdf68e82e9c0131267
  sha256: 3f1d4d92134c3eee85f2955b685cd68d7bf32a4ee8005cfdf68e82e9c0131267
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin
    Module Release Flow/Admin Module Release Checklist Template/Reference of FMAA API/page.md
  revision: sha256:2f0fdbf083a56fc293ef6be8cdb531d6e290c74a7a7fa1c645639c57229609c9
  sha256: 2f0fdbf083a56fc293ef6be8cdb531d6e290c74a7a7fa1c645639c57229609c9
- resource: git://mfe-base/src/utils/featureFlagController.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: 981abe52bb786188dab592e435ce7dfcb957ee5be9949c020ef7206396f4e56c
- resource: git://single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: c5cb0cb4a7a00663deaaa169837cd607bbaf35f8bf3eda04ffbe951b246d06af
- resource: git://single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: b71df7273263aa8c17b8ea58e9e727008b108ec51ffdc70e266207ed07efad4a
- resource: git://mfe-base/src/pages/Home/common/useController.ts#L1-L31
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: c27cc263a0cb6b6c1a81d0ad236d3348378c1de7c65c8a881c1b94b7c592a739
generated:
  by: agent:codex
  at: '2026-10-15T14:22:43.471011+00:00'
verified: []
classification: security
scope: Portal user authentication, session design, and the documented Entra migration boundaries.
summary: The materials describe portal authentication and session responsibilities, with unresolved timing
  and migration rules.
related:
- KT-sdk-and-entitlements
- KT-admin-and-onboarding
- KT-frontend-composition
- single-ui-authentication
- single-ui-sso-token-family
- single-ui-bff
- mfe-base
- ARCH-authentication-runtime-baseline
- REQ-active-session-renewal
open_questions:
- Which effective token settings and refresh-token expiry behavior apply to each supported environment?
- Which client artifact and runtime overrides govern deployed login and restart behavior?
- Which current identity-provider profile fields can downstream services depend on?
- Which release and test evidence establishes the current migration state?
- Which historical security findings have current remediation and assertion-bearing retest evidence?
- Which historical FMAA flows and validity settings remain applicable?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# Authentication and sessions

## Scope

This topic connects user authentication, portal sessions, and the supplied Entra migration materials.
It describes document statements and proposals.
It does not establish deployed behavior or approved security policy.

## Summary

The [code baseline](../architecture/ARCH-authentication-runtime-baseline.md) records implemented behavior at exact repository revisions.
This topic retains document statements separately from that source-backed investigation.

The portal authenticates users, obtains entitlements, and issues tokens for application requests.
Its session materials distinguish idle timeout, absolute timeout, refresh tokens, and repeated login.
Entra migration replaces the SSO provider while preserving separate entitlement and portal-session responsibilities.
Several timing, rollout, and browser-state statements require reconciliation.

## Documented knowledge

### Authentication responsibilities

The Entra design describes a browser redirect followed by an authorization-code exchange through the BFF.
The BFF builds user information, retrieves EMS2 entitlements, and issues authentication and entitlement tokens.
Its design retains OneMFA fallback and a separate username/password path.
[Entra design, lines 7–31, 40–68](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/UI SSO Entra Design/page.md>)

The phase 1 scope separates authentication from authorization.
It includes UI SSO migration.
It excludes EMS2 replacement, portal session management, and tenant-onboarding authentication.
Machine-to-machine authentication has a separate migration document with unresolved central dependencies.
[Entra phase 1, lines 15–21, 48–57](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/page.md>)
[Service-account migration, lines 1–10](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal & RATAN Entra Migration - Phase 2 - service account/page.md>)

### Session concepts and intended lifecycle

The documents use an access token to authenticate application requests.
An idle timeout limits inactivity.
An absolute timeout limits the interval since authentication.
A refresh token supports another authentication interval without repeating the initial SSO journey.
These are documented concepts, rather than a confirmed runtime contract.
[Session version 0, lines 1–9, 19–24, 38–65](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 0/page.md>)
[Session version 1, lines 102–193](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md>)

Version 0 states limits below 60 minutes for absolute timeout and below 15 minutes for idle timeout.
Its examples use a 15-minute access token and a 24-hour refresh token.
It proposes an inactivity warning, session extension, single-device login, and reused-token rejection.
Those examples do not resolve the strict-limit wording or current implementation.
[Session version 0, lines 1–9, 19–24, 38–65](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 0/page.md>)

Version 1 proposes `exp = iat + 15 minutes` for idle timeout.
It relates absolute timeout to `auth_time` and a 60-minute `max_age` interval.
Its proposed flow obtains a refresh token before access-token expiry.
A later relogin exchanges the refresh token for another access token.
It places single-device login and token-blacklist work on a backlog.
[Session version 1, lines 102–193](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md>)

Version 1 contains both 105-minute and 225-minute refresh-token durations in the same calculation.
Its absolute-timeout discussion also proposes changing `auth_time` during continued activity.
These statements cannot define a single reliable timing rule without review.
[Session version 1, lines 102–193](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md>)

Version 1 also states that refresh tokens have no absolute timeout because they lack `auth_time` and `max_age`.
This is a proposed source statement alongside competing duration and `auth_time` rules, rather than accepted policy.
[Session version 1, lines 133–164](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md>)

### Entra onboarding and user profile

The non-production guide requires a development AD account, Authenticator registration, and RATAN AD-group membership.
It asks teams to check successful login, user information, and expected tile visibility.
Its FAQ associates missing entitlements with tile access and EMS2 configuration.
The included completion table reports verification; retained execution evidence was not inspected.
[Non-production verification guide, lines 5–56, 58–126](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Non Prod Verification/page.md>)

The production guide targets pilot users after technical go-live in May 2026.
It describes Windows Hello or Authenticator authentication and an Entra session of one hour.
That provider-session statement does not settle the portal refresh-token lifetime.
[Production pilot guide, lines 1–2, 12–46, 48–86, 95–101](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md>)

The production guide warns that AD profile values differ from OUD values.
It identifies changed surname formatting, country codes, and missing locale values.
Downstream audit or application logic can therefore require profile-field review during migration.
[Production pilot guide, lines 1–2, 12–46, 48–86, 95–101](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md>)

### Historical machine-to-machine authentication

The historical FMAA reference describes client-credential authentication for machine-to-machine callers.
It separates service-account onboarding from bank-ID onboarding.
It describes OUD-managed accounts authenticated through FMAA.
It states 17-year validity for service accounts and seven-day validity for bank IDs.
Those historical values do not establish approved portal-session limits or current token policy.
[Historical FMAA reference, lines 11–13, 24–30, 36–50](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/Reference of FMAA API/page.md>)

### Historical security observations

The penetration-test notes report logout-session blacklisting and removal of normal production login during 2023 remediation.
They also list access-control, error-disclosure, headers, TLS, storage, and CORS findings.
Those statements describe historical findings and reported changes, without establishing a current security baseline.
[Penetration-test notes, lines 5–15, 23–29, 47–67](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/Penetration Testing report for SPT001414 – SSI+ BA/page.md>)

Other scan notes report UAT header changes and Dev fixes planned for UAT deployment during December 2023.
Their screenshots and referenced scan reports are absent.
A reported fix or deployment plan does not establish a passing security retest.
[WAS notes, lines 31–53, 123–125](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/WAS Scan Report SIA-ETASK1854215- 11282023/page.md>)
[API scan notes, lines 6–18](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/Web Application Vulnerability Scan - SIA-API-ETASK1837309-01122023/page.md>)

### Code investigation at the initial revisions

The supplied frontend accepts `true`, `1`, `yes`, and `y` after lowercasing a declared feature value.
Other supplied values disable the feature.
Thus, `true` versus `yes` does not create a parser incompatibility at this revision.
The parser does not persist the query override.
[Retained code](<../../raw/code/mfe-base/99b4eda666bedf06574bc48766e4efdb339f4cc7/src/utils/featureFlagController.ts.snapshot#L1>)

The repository JWT settings specify 15 access minutes, 225 refresh minutes, and 60 absolute minutes.
Refresh generation adds 24,000 milliseconds.
Validate, near-boundary extend, and refresh relogin can reset the absolute-time reference.
Refresh relogin performs no fresh external SSO challenge.
These source behaviors resolve implementation questions without establishing effective deployment settings or approved policy.
[Retained code](<../../raw/code/single-ui-bff/091c9d16c13f285a78463ff0235c21b152844b61/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java.snapshot#L1>); [Retained code](<../../raw/code/single-ui-bff/091c9d16c13f285a78463ff0235c21b152844b61/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java.snapshot#L1>)

The initial Home handler renews only through a mouse-movement debounce.
Continuous events postpone that callback until movement stops for five seconds.
The separate pilot adds the requested mouse, keyboard, and scroll handling.
Its own revision and retained checks are recorded in the stage report.
[Retained code](<../../raw/code/mfe-base/99b4eda666bedf06574bc48766e4efdb339f4cc7/src/pages/Home/common/useController.ts.L1-L31.snapshot#L1>)

Owner: unknown for effective deployment settings and source-authority review.
Next action: use the code baseline for implementation context and review the requested requirement separately.

## Connections

[SDK and entitlements](KT-sdk-and-entitlements.md) explains downstream token validation and entitlement responsibilities.
[Admin and onboarding](../operations/KT-admin-and-onboarding.md) connects tenant setup with role and tile configuration.
[Frontend composition](../architecture/KT-frontend-composition.md) explains the UI context for login and user state.

Registry capability `single-ui-authentication` connects declared repository and service identities.
Contract `single-ui-sso-token-family` supplies existing interface context for `single-ui-bff` and `mfe-base`.
These declarations do not prove that a migration design runs in any environment.

## Evidence limits

The supplied documents have local byte revisions, but no confirmed original page revisions or approval authority.
This limits their use as current security policy.
Owner: unknown.
Next action: establish the applicable versions with the responsible security and application owners.

Version 1 reports an August 2023 idle-timeout example, but its screenshot evidence is absent from this copy.
No session or login execution was performed.
Current timing and behavior remain unverified.
Owner: unknown.
Next action: retain assertion-bearing execution for the approved session rules.
[Session version 1, lines 102–193](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md>)

The design uses `ENABLE_ENTRA_SSO=true/false`; the production guide uses `yes/no`.
The production guide describes both temporary activation and persistent activation after first use.
These differences can produce incorrect pilot or fallback instructions.
Owner: unknown.
Next action: compare the deployed parser and browser-state behavior with both guides.
[Entra design, lines 7–31, 40–68](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/UI SSO Entra Design/page.md>)
[Production pilot guide, lines 1–2, 12–46, 48–86, 95–101](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md>)

Evidence: Historical security notes report remediation without the referenced scan attachments or inspected retest execution.
Consequence: Neither current finding status nor the effectiveness of those controls is established.
Owner: unknown.
Next action: obtain applicable scan reports, deployed revisions, and retained retest assertions.

## Open questions

Which timeout definitions and refresh duration govern each supported environment?
The two session versions contain incompatible limits and proposals.
This prevents precise session acceptance criteria.
Owner: unknown.
Next action: record a reviewed timing table with boundaries and token-reuse behavior.
[Session version 0, lines 1–9, 19–24, 38–65](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 0/page.md>)
[Session version 1, lines 102–193](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md>)

Which Entra migration state is current?
The phase plan and pilot guide provide different rollout dates and no inspected deployment evidence.
A schedule cannot establish completed migration or removed fallback.
Owner: unknown.
Next action: connect the applicable release record and environment-specific verification.
[Entra phase 1, lines 15–21, 48–57](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/page.md>)
[Production pilot guide, lines 1–2, 12–46, 48–86, 95–101](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md>)

Which historical security findings have current remediation and assertion-bearing retest evidence?
Owner: unknown.
Next action: connect each relevant historical finding to its applicable current control and retest evidence.

Which historical FMAA flows and validity settings remain applicable?
The reference supplies exceptional validity values, while the service-account migration describes unresolved replacement dependencies.
Adopting those values could misstate current machine-to-machine authentication policy.
Owner: unknown.
Next action: establish the applicable provider contract and reviewed validity limits for each supported service flow.
[Historical FMAA reference, lines 24–30, 36–50](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/Reference of FMAA API/page.md>)

The [renewal requirement](../requirements/REQ-active-session-renewal.md) records the user's requested pilot behavior.
Its scenarios and deployment verification remain separate from these historical documents.
