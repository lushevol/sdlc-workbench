# Architecture context source refresh

**The context now matches all 46 cited source files. All 23 relationship assessments retain their previous status.**

No critical conclusions require user attention or action.

## Scope and authority

The [implementation continuation](../user-input.md#exact-continuation-input) authorizes the knowledge graph delivery.
This supporting refresh resolves stale architecture evidence before graph generation.
Date: 4 November 2026, Asia/Singapore.
Owner: Workbench maintainer.
Risk: Low. This change updates derived context and evidence references.

The [initial instructions](architecture-instructions-before.md) and [prior context](architecture-context-before.json) preserve their exact original bytes.
The prior context SHA-256 is `30ec7944006481918bd2208c8904ab6f07a9e0d17cd4b219df00758adf48c381`.
The instructions SHA-256 is `fda7590fde683601592b665752a8341171ba06b78142b71758428ae354cae668`.
The [updated context](../../../../relationships/service-dependencies/architecture-context.json) contains the current source hashes, revisions, and citation ranges.
The update changes no domain intent, application source, publication approval, or release authorization.

## Source comparison

Eight cited source files differed from the previous context.
The relevant independent checkouts were clean during inspection.
Unchanged cited files retain their previous exact source revisions.
All affected relationship assessments remain `SUPPORTED`, `INFERRED`, or `OUT_OF_SCOPE`, as previously recorded.

| Independent repository | Previous cited revision | Current inspected revision |
| --- | --- | --- |
| Single UI BFF | `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a` | `134a340472f29d2a4136e07e516690de6a18e323` |
| RATAN Auth Server | `3b32ad5a76c1f7c1cdf7bd7b72b3f3c27360b5ce` | `dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2` |
| Single UI SDK | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3` | `fd9a157e260850b6d9efa10da3223950ea61133a` |

| Context source ID | Inspected support and update |
| --- | --- |
| `bff-auth-controller` | [Current mappings](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L167) retain the seven cited authentication routes. Refresh their shifted ranges. |
| `bff-catalog-props` | [Drawer construction](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L181) still creates container, module, and tile properties. Move the citation to lines 181–191. |
| `bff-ems3-client` | [CES request construction](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/ems3/Ems3EntitlementService.java#L106) retains its endpoint and FMAA bearer header. Error logging changed elsewhere. |
| `bff-token-issuer` | The [issuer constant](../../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/Constant.java#L14) remains unchanged. Tile export headers changed elsewhere. |
| `sdk-auto-configuration` | [Conditional filter configuration](../../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java#L21) remains present. Move its citation to lines 21–34. New token-provider wiring does not establish downstream adoption. |
| `auth-ems2-client` | [Role retrieval](../../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/Ems2LegacyEntitlementReader.java#L158) and [entity retrieval](../../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/Ems2LegacyEntitlementReader.java#L196) retain EMS2 HTTP calls. Logging changes moved both ranges. |
| `auth-ems3-client` | [Configured CES request](../../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/repo/Ems3Repository.java#L38) retains its GET request and bearer header. Narrow the citation to lines 38–51. |
| `auth-entitlement-routing` | [Full reads](../../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java#L40) select configured EMS2, EMS3, or dual modes. [Data-role reads](../../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java#L58) still call EMS2 directly. |

The refreshed routing description distinguishes full entitlement selection from the separate EMS2 data-role path.
This is an implementation observation. It supplies no new intended business rule.
Live configuration, deployed mode, endpoints, successful requests, and downstream SDK adoption remain unverified.

## Checks and limits

The architecture-context loader passed source hashes, contract references, and citation range checks.
The refresh preserved each relationship ID and assessment status.
The source inventory contains 46 records and 23 relationship investigations.
The graph generation stage must still validate and capture these refreshed bytes.
No runtime or business execution was performed for this source comparison.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
