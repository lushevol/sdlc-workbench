---
sources: ["summaries/KT-release-operations.md"]
type: "Organization"
description: "Tenant organization requesting multiple Portal tiles, including gating, SSI, custody, and collateral capabilities."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# FSS

FSS is a tenant organization whose release requests drive several tiles on the [[entities/fmo-post-trade-portal]]. Its requests describe intended business functions that require Portal integration. Those descriptions explain planned capability, not approved rules, completed releases, or present availability.

## Requested capabilities

The supplied change requests describe the following intended functions:

| Capability | Documented purpose |
| --- | --- |
| FSS Cash Projection | Supplies a cash-projection rule-engine tile. |
| FSS Funds Gating | Limits investor redemptions to a percentage of daily net asset value. |
| FSS SSI | Generates settlement instructions from stored agent accounts, with email and download options. |
| FSS Domestic Disbursement | Reconciles depository files and creates MT566 messages after credit for downstream processing. |
| FSS Gold Custody | Captures purchases and sales, settles services, and produces daily position updates. |
| FSS Digital Asset Collateral | Supports collateral use of custodied digital assets and counterparty-risk reduction. |

## Position in release operations

FSS capabilities enter the Portal through the [[entities/markets-operations-one-release]] process. That process separates Portal routing and route enabling, which Portal teams own, from tenant application validation and UVT, which tenant teams own. See [[concepts/application-ownership]].

As a tenant, FSS depends on [[concepts/configuration-promotion]] of Module Map, Drawer Category, and Tile Configuration records, and on [[concepts/tenant-production-readiness]] checks such as connectivity, sign-off, and user profile details. The related tile visibility rules sit in [[concepts/portal-entry-and-tile-authorization]].

## Evidence limits

The supplied materials describe requested scope only. They do not contain retained evidence that any FSS capability passed technical sign-off, business UAT, or business activation. See [[summaries/KT-release-operations]] for the wider release context and its open questions about readiness evidence.

Related entities: [[entities/cdups]], [[entities/ddr]], [[entities/vpa]].