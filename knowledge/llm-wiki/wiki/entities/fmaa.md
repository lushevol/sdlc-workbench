---
sources: ["summaries/KT-authentication-and-sessions.md", "summaries/KT-release-operations.md"]
type: "Product"
description: "Authentication component issuing client-credential tokens for portal admin uploads and machine-to-machine callers."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# FMAA

## What it is

FMAA is an authentication component referenced by the Portal Admin configuration promotion workflow and by a historical Admin Module API reference. In the supplied materials it appears in two roles: as the issuer or validator of the JWT that the Portal Admin service checks before it processes uploaded CSV configuration files, and as the provider that authenticates OUD-managed machine-to-machine accounts through client credentials. The documents do not expand the acronym, describe the service architecture, or confirm who owns it.

## Key facts from the supplied material

### Role in configuration promotion

The documented [[concepts/configuration-promotion]] flow begins with Module Map, Drawer Category, and Tile Configuration changes in Development. Teams export those records as CSV files, retain them in a tenant-owned repository, and an ADO pipeline uploads them to the Portal Admin service at `/api/auth/v1/fmo/admin/config/upload`. The flow states that the service validates an FMAA JWT before processing the CSV files. This describes the documented procedure; the ingestion ran no upload and observed no token validation.

### First release exception

The documented flow states that the first bulk insert into UAT and Production uses a separate BFF release rather than the tenant pipeline. FMAA is described only in connection with the recurring upload path, not that first release exception.

### Historical machine-to-machine authentication

The historical FMAA API reference describes client-credential authentication for machine-to-machine callers, connecting FMAA to [[concepts/machine-to-machine-authentication]]. It separates service-account onboarding from bank-ID onboarding, and it describes OUD-managed accounts authenticated through FMAA. The reference states 17-year validity for service accounts and seven-day validity for bank IDs. These are historical values in one reference; the authentication topic states that they do not establish approved portal-session limits or current token policy, and treats the flows and validity settings as unresolved requirements.

### Planned decommissioning

The Admin Module release checklist, which is still under construction, flags planned FMAA decommissioning. That warning creates an unresolved dependency for both the documented promotion workflow and any machine-to-machine flow that relies on FMAA: the checklist does not name a replacement authentication mechanism, confirm a timeline, or state whether the decommissioning applies to all environments. The authentication topic records the same gap and assigns no confirmed owner. Until that is resolved, teams cannot confirm that the upload path or the service-account flows will keep working.

## Relationships

- [[entities/admin-module]] — the module whose release flow documents the FMAA token check and the decommissioning warning.
- [[entities/fmo-post-trade-portal]] — the Portal whose Admin service performs the validation.
- [[entities/single-ui-bff]] — the BFF release that performs the first bulk insert into UAT and Production.
- [[entities/portal-team]] — Portal-side responsibility for Portal releases and routing rollback.
- [[concepts/single-ui-sdk-authentication]] — broader authentication context in the supplied materials.
- [[concepts/cross-application-authentication-handoff]] — related authentication handover context.
- [[concepts/identity-provider-delegation]] — related delegation context; [[entities/entra]] is the identity provider named elsewhere in the sources.
- [[concepts/machine-to-machine-authentication]] — the client-credential, service-account, and bank-ID flows that the historical FMAA reference describes.
- [[concepts/token-lifecycle-and-timeout-policy]] — the token validity rules that the historical FMAA durations do not settle.
- [[concepts/tenant-production-readiness]] — readiness checks that remain distinct from a successful configuration upload.

## Evidence limits

The name FMAA is not expanded in the supplied copy, and no architecture, sequence diagram, or token specification for it was available. The machine-to-machine details come from one historical Admin Module reference whose original page revisions and approval authority are unconfirmed. Its current operational status, replacement plan, environment coverage, and approval state are unconfirmed. The authentication topic names the intended provider contract and validity limits for each supported flow as an unresolved question with an unknown authentication owner. Related context appears in [[summaries/KT-release-operations]], [[summaries/KT-admin-and-onboarding]], [[summaries/KT-sdk-and-entitlements]], and [[summaries/KT-authentication-and-sessions]].

## Open questions

- What does FMAA stand for, and which team owns it today?
- Which replacement mechanism will validate configuration uploads after decommissioning?
- Does the decommissioning affect Development, UAT, and Production on the same schedule?
- Is the FMAA token check required for every upload, or only for the initial bulk insert path?
- Do the client-credential, service-account, and bank-ID flows remain intended requirements, and which validity limits apply to each?
- Does any target provider contract replace the historical FMAA machine-to-machine flows?