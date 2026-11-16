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

## Historical request profiles and planning counts

The request locates Gold Custody services in India, with daily position updates to CSS. Domestic Disbursement names SG and HK launches and MT566 generation after EBBS credit, with delivery to SeCCuRe.

Requested total/new/concurrent users are 10/10/5 for Cash Projection, Funds Gating, and Gold Custody. Domestic Disbursement gives 25/10/10; SSI gives 11/11/5. Collateral uses existing users without a numerical count. These values describe historical requests, with no current usage or capacity proof.

The requested entities include FSSFM_GATING_TXN_HK, FSSFM_GATING_REF_HK, SSI, CA_DOMESTIC_SG, CA_DOMESTIC_HK, CA_DOMESTIC_CN, CA_DOMESTIC_IN, and GOLD_CUSTODY_IN. General roles include MASTER, MAKER, CHECKER, PSS USER, and BUSINESS USER. Gold Custody lists MAKER, CHECKER, and VIEWER. Collateral names FSSDA_CLM_AE. Requested profiles establish no current grants or role equivalence.

[KT-release-operations — fss-request-scope-and-profiles](../../../records/candidates/operations/KT-release-operations.md#fss-request-scope-and-profiles) [KT-release-operations — cash-projection-request-scope](../../../records/candidates/operations/KT-release-operations.md#cash-projection-request-scope)
