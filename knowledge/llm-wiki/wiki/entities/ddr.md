---
sources: ["summaries/KT-release-operations.md"]
type: "Product"
description: "FSSDS Data Distribution and Reporting product requested for Portal integration to show downstream report distribution."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# FSSDS Data Distribution and Reporting (DDR)

## What it is

DDR is a reporting product in the [[entities/fss]] family. Its documented purpose is to show reports received from upstream systems and forwarded downstream ([DDR request, lines 4–5](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSSDS Data Distribution and Reporting (DDR)/page.md#L4>)).

It appears in the supplied materials as one of the tenant applications proposed for integration into the [[entities/fmo-post-trade-portal]] under [[entities/markets-operations-one-release]]. The purpose statement explains why the tenant tile needs Portal integration; it does not establish approved detailed rules, release completion, or present availability.

## Key facts from the supplied documents

### Separate technical and business milestones

The DDR request lists distinct technical and business target dates. It states that business UAT sign-off follows technical go-live ([DDR request, lines 9–17](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSSDS Data Distribution and Reporting (DDR)/page.md#L9>)).

This matches the wider pattern of [[concepts/tenant-production-readiness]], where technical deployment and business activation need separate evidence. A listed date is planning context; it does not prove deployment, approval, or successful adoption.

### Pending connectivity

The request records connectivity as pending and keeps technical sign-off separate from business validation ([DDR request, lines 9–13](<../../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSSDS Data Distribution and Reporting (DDR)/page.md#L9>)). Under the flow described in [[concepts/configuration-promotion]], Portal-side configuration upload and routing preparation can proceed independently, but neither establishes tenant-side connectivity or business acceptance.

### Scheduling context

The request sits inside the release calendar governed by the proposed [[concepts/release-window-governance]] rules: first, third, and available fifth Saturdays, scope freeze after Monday EOD in the first week, and approved exceptions for late additions. These rules remain proposed and partly ambiguous.

## Evidence limits

No connectivity check, configuration upload, deployment, or UAT validation ran during ingestion of these materials. The DDR request is one record among several tenant requests; it does not by itself establish accepted capability scope or completed release readiness.

## Relationships

- [[entities/fss]] — parent product family for the requested capability.
- [[entities/fmo-post-trade-portal]] — host Portal for the tenant tile entry.
- [[entities/markets-operations-one-release]] — release vehicle carrying the DDR request.
- [[concepts/tenant-production-readiness]] — split between technical go-live and business sign-off.
- [[concepts/configuration-promotion]] — Portal-side configuration and routing steps.
- [[summaries/KT-release-operations]] — source summary for release and tenant context.

## Open questions

- Which record proves DDR technical deployment, and which proves business UAT sign-off?
- Which configuration, connectivity, or sign-off evidence closes the pending connectivity item?
- Which Portal tile or route entry represents DDR, and where is it retained?