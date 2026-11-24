# Portal source-reported technical context

The retained sources contain historical technical descriptions and implementation reports.
These statements retain their source classification.
Current implementation, deployment, applicability and conformance remain unverified.

## SDK release-note implementation reports

The Java 8 and Java 17 SDK 1.1.4 release notes report using JWT entitlements when present.
They report adding the session identifier to a blacklist at logout and checking that blacklist.
These are release-note implementation reports.
The source review executed no SDK or logout case.
The historical property tables independently define the retained configuration contracts.
[Java 17 release notes, lines 1–16](<../../../knowledge/evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md#L1-L16>)
[Java 8 release notes, lines 1–16](<../../../knowledge/evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 8/page.md#L1-L16>)

## Briefing license and SSO claims

The briefing reports restricted Here Core UI component access, with an exception for part of Notification.
It describes the Ratan solution as OpenFin Container based.
It also states that OpenFin natively supports Entra SSO.
These source-reported license and capability statements remain independently unverified.
The separate technical-phase proposal retains its user-identification and browser-impact conditions in canonical draft intent.
[Briefing license and scope, lines 32–34](<../../../knowledge/evidence/sources/confluence/FM TPT UI Guild/OpenFin/Ratan OpenFin Briefing/page.md#L32-L34>)
[Briefing SSO claim, lines 165–169](<../../../knowledge/evidence/sources/confluence/FM TPT UI Guild/OpenFin/Ratan OpenFin Briefing/page.md#L165-L169>)

## Historical static-delivery scaling assumption

The frontend deployment guide assumes that serving static frontend files requires no scalable server.
That historical source assumption lacks inspected capacity or sizing verification.
The proposed latest-version and blue-green delivery behavior remains historical draft intent.
[Frontend deployment description, lines 3–11](<../../../knowledge/evidence/sources/confluence/FM TPT UI Guild/Microfrontend/Micro-Frontend Deployment/page.md#L3-L11>)

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Source reports establish their stated documentary scope only.
```
