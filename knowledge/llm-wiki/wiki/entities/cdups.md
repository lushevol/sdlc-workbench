---
sources: ["summaries/KT-release-operations.md"]
type: "Product"
description: "Confirmation-management product whose Portal tile was requested via a Markets Operations One change request."
---

# CDUPS

CDUPS is a post-trade confirmation-management product that was proposed for Portal integration through the [[entities/markets-operations-one-release]] change-request process. Its Portal tile request sits alongside requests from [[entities/fss]], [[entities/vpa]], and [[entities/ddr]].

## Documented capability

The release request describes CDUPS Confirmation as managing outbound confirmation documents and inbound confirmations in separate blotters. This is the intended business function stated in the request; the supplied materials do not establish approved detailed rules, release completion, or present availability.

Source: CDUPS request, lines 9–10.

## Release readiness

The CDUPS change request is part of the [[entities/markets-operations-one-release]] calendar and was assessed in [[summaries/KT-release-operations]] as an example of incomplete readiness evidence. The request leaves the following unprovided:

- UAT sign-off
- User profiles
- User counts
- UVT details

Because these fields are missing, the request's target date cannot establish [[concepts/tenant-production-readiness]] or business acceptance. Missing evidence cannot satisfy a release gate.

Source: CDUPS request, lines 14–21.

## Placement in the Portal model

Like other requested tenant tiles, CDUPS would appear through the Portal's registered tile and drawer configuration, so its onboarding depends on [[concepts/admin-catalog-configuration]], [[concepts/configuration-promotion]], and the [[concepts/portal-tile-workspace-model]]. Scheduling would follow [[concepts/release-window-governance]], which in the supplied proposal remains ambiguous on release duration and urgent-release confirmation.

## Evidence limits

Local hashes identify the supplied bytes only. Original page revisions, current authority, and human approval remain unconfirmed, and no deployment, upload, or UAT check ran during ingestion.

## Related

- [[summaries/KT-release-operations]]
- [[entities/markets-operations-one-release]]
- [[entities/fmo-post-trade-portal]]
- [[concepts/tenant-production-readiness]]
- [[concepts/release-window-governance]]
