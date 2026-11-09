---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Independent tile rollout assessment

> **Each tile can select its provider. Complete operational isolation is absent.**
> Action: resolve shared failure handling before claiming isolated rollout. Owner: unknown.
> Consequence: one CES application failure can remove other CES tiles.
> Evidence: [service aggregation](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L123-L136).

## Scope and conclusion

The [user request](evidence/user-input.md#exact-user-input) asks whether each BFF tile can move independently.
This assessment separates tile admission, shared grants, backend authorization, and operational isolation.
BFF source: `95480c0e2563bc2a5a639bca1f22ecedb61936c2`.
The retained export contains 113 tiles. It does not establish the current deployed database.

| Boundary | Independent? | Evidence and condition |
| --- | --- | --- |
| Select EMS2 or CES for one tile | Yes | Each [tile record](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/entity/ApplicationTile.java#L79-L92) stores its provider and CES binding. |
| Keep other tiles on EMS2 | Yes | Use [EMS3_PRIMARY_DUAL_READ](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L59-L72). EMS2 receives only remaining legacy entity requests. |
| Select a feature within one CES application | Yes | [Feature matching](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileFeatureMatcher.java#L13-L23) grants tile IDs separately. Multiple configured features use ANY matching. |
| Isolate successful CES apps from another failed app | No | [Future aggregation](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L123-L136) discards the assembled CES result on one exception. |
| Keep CES login working during EMS2 failure | No, during mixed mode | The [EMS2 read](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L60-L68) runs before CES error handling. |
| Restrict response grants to the rolled tile | No | The [mapper](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L53-L105) projects all application role permissions. Tile admission remains separate. |
| Move admin operation checks through tile settings | No | [Admin validation](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L45-L65) requires legacy `FMO PORTAL ADMIN:<role>`. |
| Change backend authorization or upper application behavior | Not established | BFF configuration controls its response and drawer. Other services retain their own authorization configuration. |

## Effective modes and configuration

| Mode | Effective behavior | Suitable for partial rollout? |
| --- | --- | --- |
| EMS2_ONLY | All tile rows use legacy entity lists. CES-configured rows produce effective EMS2 routes. | No CES rollout; global legacy rollback. |
| EMS3_PRIMARY_DUAL_READ | EMS2 rows use EMS2. CES rows use their configured application and feature. | Yes, with the shared failure limits above. |
| EMS3_ONLY | CES rows remain controlled. EMS2 grants are not fetched. Ordinary legacy tiles lose admission. | No, while ordinary EMS2 tiles remain. |

The [base YAML](../../repos/services/single-ui-bff/src/main/resources/application.yml#L85-L109) selects `EMS3_PRIMARY_DUAL_READ`.
Runtime overrides and deployed configuration were unavailable.
The legacy application name map currently covers application `51358` as `RATAN`.
Other application mappings require explicit configuration when consumers need the legacy display name.

For each migrated tile, retain its legacy configuration for rollback.
Set `entitlement_source` to `EMS3` and supply its CES application ID and application name.
Supply the intended feature names through `entitlement_app_feature`.
CES application names use comma-separated entries. Each application gets a separate read.
The [validator](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/TileEntitlementConfig.java#L26-L65) normalizes lists and rejects invalid definitions.

A blank feature deliberately bypasses CES feature authorization in the [drawer path](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L178-L200).
It must not be described as tested CES grant enforcement.
An invalid nonblank CES definition remains CES and fails closed. It cannot recover legacy admission automatically.
A recognized user-not-found response denies only that application. Other thrown errors use shared failure handling.

The [CRUD endpoint](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L48-L113) changes one tile and records an audit.
A maker edit makes the tile inactive until checker approval.
Category and import-map activation also control the [drawer query](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/repository/ApplicationCategoryRepo.java#L26-L27).
The [CSV path](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/CsvUtility.java#L93-L140) supports four CES columns together.
Legacy CSV headers preserve stored migration fields during import.
Login and relogin rebuild routing. Token extension alone does not rebuild it.
Existing sessions therefore need login or relogin before they receive changed tile routing.

Data filters remain separate from functional provider selection.
The [filter executor](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/AuthFilterExecutor.java#L25-L43) still applies configured regional rules.
Changing `entitlement_source` alone does not remove a CES regional filter during rollback.
A complete rollback must account for the filter and its intended business policy.

The auth server has separate provider selection by user and migration mode.
Its `scb.ems3.enabled` switch gates the separate data-filter API, not the full JWT projection.
Use its migration mode or user allowlist for full-read rollback.
Evidence: [auth review](evidence/auth-review.json).

## Retained tile inventory

Source: [supplied database export](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv).
SHA-256: `23b23415ebe9def55b854f36e85465b54add2356d5b9fc165cb8c54a15647486`.
The source filename identifies 5 November. Its environment, build, and extraction time remain unknown.
`Active` below describes only the tile flag. Category and import-map flags are absent from this export.

| Configuration | All tiles | Tile flag active | Tile flag inactive |
| --- | ---: | ---: | ---: |
| CES binding | 45 | 43 | 2 |
| EMS2, without a CES binding | 68 | 58 | 10 |
| Total | 113 | 101 | 12 |

All 45 CES rows use application `51358` and name `RATAN_ENTITLEMENT_RULE`.
Forty-four have nonblank features. Tile 192 has a blank feature and is inactive.
Twenty-seven CES rows also contain CES regional filters. No EMS2 row contains a filter in this export.
The 68 EMS2 rows require sourced CES mappings before migration. Their legacy subjects cannot establish CES policy automatically.
Thirteen EMS2 rows are templates. Their legacy admission bypass does not establish the intended CES policy.
Admin tiles 1–4 also require legacy authorization for management operations.

### Per-tile result

`Binding present` means local metadata can select CES for that tile.
It does not establish correct CES assignments, upper application compatibility, runtime acceptance, or independent failure handling.
`Mapping required` means the export has no usable CES application binding.

| Tile ID | Title | Active | Provider | CES feature | Regional CES filter | Per-tile result |
| --- | --- | --- | --- | --- | --- | --- |
| [1](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L2) | Module Map | Yes | EMS2 | — | No | Mapping required; admin operations remain EMS2 |
| [2](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L3) | Drawer Category | Yes | EMS2 | — | No | Mapping required; admin operations remain EMS2 |
| [3](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L4) | Tile Configuration | Yes | EMS2 | — | No | Mapping required; admin operations remain EMS2 |
| [4](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L5) | FDC3 Configuration | Yes | EMS2 | — | No | Mapping required; admin operations remain EMS2 |
| [15](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L6) | Validation Exceptions | Yes | EMS3 | RATAN_VALIDATION_EXCEPTION | No | Binding present |
| [16](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L7) | Settlement Exceptions | Yes | EMS3 | RATAN_SETTLEMENT_EXCEPTION | No | Binding present |
| [17](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L8) | MO Exceptions | Yes | EMS3 | RATAN_MO_EXCEPTION | No | Binding present |
| [18](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L9) | Korea MX Exceptions | Yes | EMS3 | RATAN_KR_EXCEPTION | No | Binding present |
| [19](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L10) | Payment Processing | Yes | EMS2 | — | No | Mapping required |
| [20](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L11) | Payments - Transaction | Yes | EMS2 | — | No | Mapping required |
| [21](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L12) | Payments - Reference | Yes | EMS2 | — | No | Mapping required |
| [22](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L13) | FSS Services – DAC | Yes | EMS2 | — | No | Mapping required |
| [23](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L14) | BAP Digitization | Yes | EMS2 | — | No | Mapping required |
| [24](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L15) | FA - Reference | Yes | EMS2 | — | No | Mapping required |
| [25](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L16) | FA - Transaction | Yes | EMS2 | — | No | Mapping required |
| [26](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L17) | FSS Rules Management | Yes | EMS2 | — | No | Mapping required |
| [28](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L18) | Security Threats | No | EMS3 | RATAN_MO_EXCEPTION | No | Binding present |
| [29](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L19) | Authorization Limits | Yes | EMS3 | RATAN_PROFILE_LIMITS | Yes | Binding present |
| [30](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L20) | Settlement NSTP Rules | Yes | EMS3 | RATAN_SETTLEMENT_STP_RULE | Yes | Binding present |
| [31](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L21) | Settlement NSTP Rules | Yes | EMS3 | RATAN_SETTLEMENT_STP_RULE | No | Binding present |
| [32](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L22) | Suppression Rules | Yes | EMS3 | RATAN_SUPPRESSION_RULE | No | Binding present |
| [33](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L23) | Suppression Rules | Yes | EMS3 | RATAN_SUPPRESSION_RULE | Yes | Binding present |
| [34](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L24) | Suppression Rules | Yes | EMS3 | RATAN_SUPPRESSION_RULE | Yes | Binding present |
| [35](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L25) | MO Rules | Yes | EMS3 | RATAN_MO_RULE | No | Binding present |
| [36](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L26) | Cashflow Blotter | Yes | EMS3 | RATAN_CASHFLOW_BLOTTER | No | Binding present |
| [37](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L27) | Cashflow Blotter | Yes | EMS3 | RATAN_STRATEGIC_CASHFLOW_BLOTTER | Yes | Binding present |
| [38](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L28) | Grouping Blotter | Yes | EMS3 | RATAN_CASHFLOW_GROUP_BLOTTER | Yes | Binding present |
| [39](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L29) | Cashflow Dashboard | Yes | EMS3 | RATAN_STRATEGIC_CASHFLOW_BLOTTER | Yes | Binding present |
| [43](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L30) | SSI | Yes | EMS2 | — | No | Mapping required |
| [44](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L31) | Static | Yes | EMS2 | — | No | Mapping required |
| [45](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L32) | Validation rules and Market filter set | Yes | EMS2 | — | No | Mapping required |
| [46](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L33) | Work Queues | Yes | EMS2 | — | No | Mapping required |
| [47](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L34) | Import/Export | Yes | EMS2 | — | No | Mapping required |
| [48](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L35) | Mapping Query | Yes | EMS2 | — | No | Mapping required |
| [49](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L36) | Audit | Yes | EMS2 | — | No | Mapping required |
| [50](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L37) | Netting Static | Yes | EMS3 | RATAN_NETTING_RULE | Yes | Binding present |
| [51](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L38) | Nostro Static | Yes | EMS3 | RATAN_NOSTRO_BLOTTER | Yes | Binding present |
| [52](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L39) | BIC Netting Static | Yes | EMS3 | RATAN_NETTING_RULE | Yes | Binding present |
| [54](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L40) | Trade Blotter | Yes | EMS3 | RATAN_TRADE_BLOTTER | No | Binding present |
| [65](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L41) | Date Range Picker Example | Yes | EMS2 | — | No | Mapping required |
| [66](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L42) | Modal Example | Yes | EMS2 | — | No | Mapping required |
| [67](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L43) | Search Block | Yes | EMS2 | — | No | Mapping required |
| [68](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L44) | Search Block | Yes | EMS2 | — | No | Mapping required |
| [69](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L45) | Simple Table | Yes | EMS2 | — | No | Mapping required |
| [70](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L46) | Grid Tool Table | Yes | EMS2 | — | No | Mapping required |
| [71](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L47) | Routing Tile | Yes | EMS2 | — | No | Mapping required |
| [72](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L48) | Inbound Blotter | Yes | EMS2 | — | No | Mapping required |
| [73](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L49) | Analytics | Yes | EMS2 | — | No | Mapping required |
| [74](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L50) | LoanIQ UI | Yes | EMS2 | — | No | Mapping required |
| [94](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L51) | Outbound Blotter | Yes | EMS2 | — | No | Mapping required |
| [95](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L52) | Inbound Blotter | Yes | EMS2 | — | No | Mapping required |
| [96](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L53) | FMCES | Yes | EMS2 | — | No | Mapping required |
| [98](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L54) | Billing - EVAT | Yes | EMS2 | — | No | Mapping required |
| [100](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L55) | FSS Mosaic | Yes | EMS2 | — | No | Mapping required |
| [102](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L56) | test | No | EMS2 | — | No | Mapping required |
| [104](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L57) | FM COO Rules | Yes | EMS3 | RATAN_FM_COO_RULE | No | Binding present |
| [105](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L58) | FM COO Exceptions | Yes | EMS3 | RATAN_FM_COO_EXCEPTION | No | Binding present |
| [106](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L59) | Exception Management | Yes | EMS2 | — | No | Mapping required |
| [108](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L60) | Flowzero | Yes | EMS2 | — | No | Mapping required |
| [112](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L61) | Reporting Framework | Yes | EMS2 | — | No | Mapping required |
| [114](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L62) | C&A Rules | Yes | EMS3 | RATAN_MO_RULE | No | Binding present |
| [115](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L63) | C&A Exceptions | Yes | EMS3 | RATAN_MO_EXCEPTION | No | Binding present |
| [119](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L64) | FSS Business Rules | Yes | EMS2 | — | No | Mapping required |
| [122](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L65) | FSS Billing | Yes | EMS2 | — | No | Mapping required |
| [123](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L66) | Nostro Threshold Static | Yes | EMS3 | RATAN_NETTING_RULE | Yes | Binding present |
| [124](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L67) | CA Domestic | Yes | EMS2 | — | No | Mapping required |
| [125](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L68) | FSS DA Billing | Yes | EMS2 | — | No | Mapping required |
| [130](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L69) | Report Download | Yes | EMS2 | — | No | Mapping required |
| [131](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L70) | Report Scheduler | No | EMS2 | — | No | Mapping required |
| [132](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L71) | Query Builder | No | EMS2 | — | No | Mapping required |
| [134](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L72) | FSS Rebalancing | Yes | EMS2 | — | No | Mapping required |
| [137](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L73) | Utilization Static | Yes | EMS3 | RATAN_NETTING_RULE | Yes | Binding present |
| [139](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L74) | FX True Up & RIK | Yes | EMS2 | — | No | Mapping required |
| [140](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L75) | FSS Swing Price Metrics | Yes | EMS2 | — | No | Mapping required |
| [141](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L76) | FSS Funds Reference | Yes | EMS2 | — | No | Mapping required |
| [143](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L77) | SSI | Yes | EMS2 | — | No | Mapping required |
| [147](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L78) | CA Dashboard | Yes | EMS2 | — | No | Mapping required |
| [149](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L79) | FSS Fair Price Metrics | Yes | EMS2 | — | No | Mapping required |
| [150](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L80) | Cash Projection | Yes | EMS2 | — | No | Mapping required |
| [152](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L81) | Cashflow Blotter | Yes | EMS3 | RATAN_STRATEGIC_CASHFLOW_BLOTTER | No | Binding present |
| [154](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L82) | DDR | No | EMS2 | — | No | Mapping required |
| [158](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L83) | Fix Link | Yes | EMS2 | — | No | Mapping required |
| [161](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L84) | Cashflow Blotter | Yes | EMS3 | RATAN_STRATEGIC_CASHFLOW_BLOTTER | Yes | Binding present |
| [164](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L85) | Grouping Blotter | Yes | EMS3 | RATAN_CASHFLOW_GROUP_BLOTTER | Yes | Binding present |
| [165](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L86) | Cashflow Dashboard | Yes | EMS3 | RATAN_STRATEGIC_CASHFLOW_BLOTTER | Yes | Binding present |
| [166](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L87) | Nostro Threshold Static | Yes | EMS3 | RATAN_NETTING_RULE | Yes | Binding present |
| [167](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L88) | BIC Netting Static | Yes | EMS3 | RATAN_NETTING_RULE | Yes | Binding present |
| [168](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L89) | Netting Static | Yes | EMS3 | RATAN_NETTING_RULE | Yes | Binding present |
| [169](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L90) | Utilization Static | Yes | EMS3 | RATAN_NETTING_RULE | Yes | Binding present |
| [170](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L91) | Nostro Static | Yes | EMS3 | RATAN_NOSTRO_BLOTTER | Yes | Binding present |
| [171](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L92) | Authorization Limits | Yes | EMS3 | RATAN_PROFILE_LIMITS | Yes | Binding present |
| [172](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L93) | Settlement NSTP Rules | Yes | EMS3 | RATAN_SETTLEMENT_STP_RULE | Yes | Binding present |
| [173](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L94) | Suppression Rules | Yes | EMS3 | RATAN_SUPPRESSION_RULE | Yes | Binding present |
| [174](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L95) | Suppression Rules | Yes | EMS3 | RATAN_SUPPRESSION_RULE | Yes | Binding present |
| [175](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L96) | Trade Monitor | Yes | EMS2 | — | No | Mapping required |
| [177](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L97) | Gold Custody | Yes | EMS2 | — | No | Mapping required |
| [179](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L98) | Reporting Framework | Yes | EMS2 | — | No | Mapping required |
| [182](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L99) | FSS Funds Gating | Yes | EMS2 | — | No | Mapping required |
| [185](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L100) | Exception Handle | Yes | EMS2 | — | No | Mapping required |
| [186](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L101) | Audit Log | Yes | EMS2 | — | No | Mapping required |
| [187](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L102) | PLACEHOLDER | Yes | EMS2 | — | No | Mapping required |
| [188](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L103) | 1 | No | EMS2 | — | No | Mapping required |
| [189](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L104) | 112 | No | EMS2 | — | No | Mapping required |
| [190](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L105) | 2 | No | EMS2 | — | No | Mapping required |
| [191](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L106) | 3 | No | EMS2 | — | No | Mapping required |
| [192](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L107) | Exception Auto Recover | No | EMS3 | (blank) | No | Blank feature bypass; inactive |
| [194](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L108) | FSS DS Query | No | EMS2 | — | No | Mapping required |
| [195](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L109) | FSS DS Query | No | EMS2 | — | No | Mapping required |
| [196](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L110) | Control Data Blotter | Yes | EMS3 | RATAN_OPTION_CDS_BLOTTER | No | Binding present |
| [202](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L111) | cashflow_cn_ces | Yes | EMS3 | RATAN_STRATEGIC_CASHFLOW_BLOTTER | Yes | Binding present |
| [203](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L112) | cashflow_cn_ces-test | Yes | EMS3 | RATAN_STRATEGIC_CASHFLOW_BLOTTER | Yes | Binding present |
| [204](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L113) | cashflow_cn_ces_test1 | Yes | EMS3 | RATAN_STRATEGIC_CASHFLOW_BLOTTER | Yes | Binding present |
| [205](../ces-entitlement-migration-20261102/ces%20migration/application_tile_1105.csv#L114) | Cashflow Generator | Yes | EMS3 | RATAN_STRATEGIC_CASHFLOW_BLOTTER | No | Binding present |

## Validation and remaining limits

The [code review](10-change-review.md) records findings, controlled execution, source fingerprints, and unavailable checks.
Current database state, live CES responses, and deployed overrides remain unverified.
No tile's full business workflow is certified by this metadata inventory.
Owner: unknown. Next action: validate the selected tile with both migrated and remaining legacy journeys in UAT.
