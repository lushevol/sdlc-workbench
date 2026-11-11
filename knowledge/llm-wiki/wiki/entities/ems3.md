---
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-release-operations.md", "summaries/ARC-portal-service-relationships.md"]
type: "Product"
description: "Entitlement provider reported in the portal and used as the CES wire value in the migration contract."
---

# EMS3

EMS3 is an entitlement and authorization provider named in the reported portal architecture. It appears as a delegated authorization target — not as a component inspected in its own right — and, in the CES migration contract, it is also the wire value that denotes the CES authorization path.

## Reported role

The user clarification for [[summaries/ARC-portal-service-relationships]] states that portal authorization is delegated to two external systems: [[entities/ems2]] and EMS3. In that model, the portal does not evaluate entitlements itself; it asks a provider which functions a caller may use. This is the same delegation pattern described under [[concepts/identity-provider-delegation]], applied to authorization rather than authentication.

## EMS3 as the CES wire value

The provider-union clarification recorded in [[summaries/KT-ces-migration-parity]] states that the migration contract uses `EMS3` as its CES wire value. The frontend clarification writes the CES path as `EMS2 (CES)`; that phrase denotes the CES path, and the exact user quotation remains unchanged in its source. This interpretation does not merge the legacy EMS2 and CES tile admission choices — each tile selects its provider independently under [[concepts/per-tile-provider-selection]].

### Additive entity metadata

The BFF field decision in [[summaries/KT-ces-migration-parity]] requires two new fields on EMS3 entities: `roleList` and `applicationId`. The table also records the clarified values of the existing `name` and `applicationName` fields, which remain in the contract.

| Field | Required value | Meaning |
| --- | --- | --- |
| `roleList` | CES `entitlements.entitlement_name` values | Application-scoped assignment names |
| `applicationId` | CES application `itam_id` (e.g. `"51358"`) | Corresponding CES application identity |
| `name` | `RATAN_ENTITLEMENT_RULE` | CES application/entity name corresponding to EMS2 `X_RATANONE` |
| `applicationName` | `RATAN` | Legacy team/display application name |

CES `user_data.app_name` supplies the CES authorization name; it does not supply the legacy team label. The clarified values apply to the [[entities/ratan]] mapping and do not establish labels for other CES applications. The fields must be bound to their own application — another application's entitlement names must not populate the entity — and the additions must remove no existing entity field and change no legacy EMS2 authorization decision.

The fields expose assignment names and application identity only. They do not resolve scalar role semantics: multiple CES roles must not be collapsed into one proven assigned role (see [[concepts/ces-role-multiplicity]]).

### Position in the shared permission check

An existing `hasPermission(code)` call may accept a mapped grant from either EMS2 or CES, with a log identifying the provider that supplied an accepted grant and no new caller scope argument. That shared functional check is separate from tile admission, as described under [[concepts/permission-check-provider-union]] and [[concepts/ems2-to-ces-permission-mapping]].

## What the local sources show

- The RATAN authentication service copy available for review contains **no identified EMS3 implementation**. It also contains no identified Entra SPN integration.
- EMS3 calls do exist, but in a different place: the [[entities/single-ui-bff]] holds an entitlement service under the `service/v2/filter/ems3` path (`Ems3EntitlementService.java`), which issues EMS3 calls.
- The source review records local support for OUD, FMAA, and EMS2 paths, but not for EMS3 or Entra SPN.

The CES migration sources add no implementation evidence. The BFF field decision defines target metadata for EMS3 entities; it does not establish implemented, tested, or deployed response behavior, or that deployed provider-source logs are collected.

## Interpretation and limits

Because the only code evidence for EMS3 sits in the BFF, the clarification should not be read as inserting an [[entities/ratan-auth-server]] hop into the EMS3 call path. The source paths remain the relevant evidence, and the reported scope of the Auth Server does not prove that every portal request passes through it.

Four further qualifications apply:

1. The reported topology carries no deployment identifier, so neither the active call path nor the deployed upstreams are established.
2. No live requests or business tests were executed for this review.
3. The migration sources treat EMS3 metadata and permission checks as intended behavior; they record no completed migration, deployed permission equality, or acceptance.
4. How multiple CES roles map to caller contracts that require one role remains an open question in [[summaries/KT-ces-migration-parity]].

## Related pages

- [[concepts/entitlement-retrieval]] — how entitlements are obtained and applied
- [[concepts/portal-entry-and-tile-authorization]] — how entitlements gate tiles and entries
- [[concepts/per-tile-provider-selection]] — independent provider selection per tile
- [[concepts/permission-check-provider-union]] — accepting mapped grants from either provider
- [[concepts/ems2-to-ces-permission-mapping]] — the concept mapping between the two providers
- [[concepts/ces-role-multiplicity]] — why CES roles do not collapse to one assigned role
- [[entities/ces]] — the CES system that EMS3 denotes on the wire
- [[entities/ems2]] — the companion authorization provider reported alongside EMS3
- [[entities/single-ui-bff]] — the component that issues the observed EMS3 calls
- [[summaries/ARC-portal-service-relationships]] — the architecture clarification this page draws on
- [[summaries/KT-ces-migration-parity]] — the migration parity intent that fixes the EMS3 wire value and entity fields
- [[concepts/single-ui-sdk-authentication]] — the token validation layer that precedes entitlement checks


See also: [[summaries/KT-release-operations]]
