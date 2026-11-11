---
sources: ["summaries/KT-release-operations.md"]
type: "Product"
description: "Post-trade product whose Fix Link and Trade Monitor tiles were requested for Portal release."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# VPA

VPA is a post-trade application that requested Portal integration for two tiles through the [[entities/markets-operations-one-release]] change-request process on the [[entities/fmo-post-trade-portal]].

## Requested capabilities

The VPA change request describes two intended business functions:

| Capability | Documented purpose |
| --- | --- |
| VPA Fix Link | Correct broken links so subsequent trade processing can continue. |
| VPA Trade Monitor | Monitor trade status and retrieve source and transformed files. |

These descriptions explain why VPA tiles need Portal integration. They do not establish approved detailed rules, release completion, or present availability. See [[summaries/KT-release-operations]].

## Release evidence

The request separates Portal and application go-live dates, consistent with the wider pattern where [[concepts/tenant-production-readiness]] distinguishes technical deployment from business activation. The request template explicitly allows Portal deployment before the application deployment.

Readiness evidence in the VPA request is incomplete: several evidence references are struck through. Missing or withdrawn references cannot establish the corresponding release gate, so the stated dates do not prove completed deployments or business acceptance.

## Relationships

- [[entities/cdups]] and [[entities/ddr]] submitted parallel requests in the same release calendar, with similar evidence gaps.
- Tile registration and authorization depend on [[concepts/portal-entry-and-tile-authorization]] and the [[concepts/portal-tile-workspace-model]].
- Configuration promotion for the tiles follows [[concepts/configuration-promotion]] under the proposed [[concepts/release-window-governance]] rules.

## Evidence limits

All facts above come from the supplied change request copy. Original page revisions, current authority, and human approval remain unconfirmed, and no deployment, connectivity, or sign-off check ran during ingestion.