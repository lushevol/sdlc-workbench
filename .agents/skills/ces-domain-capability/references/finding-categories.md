# Finding categories

Use one primary category per finding. Add a secondary category only when the same behavior crosses boundaries.

| Category | What to scan for | Typical consequence |
| --- | --- | --- |
| `identity-cardinality` | `role`, `roleName`, `roleId`, `roleList`, scalar equality, first-match role selection | Multi-role CES users lose a route, action, owner, or data profile. |
| `legacy-projection` | `X_RATANONE`, direct `user.entitlements`, JWT entitlement maps, `entity.name:roleName` | A raw reader bypasses the compatibility adapter and sees no permission or profile. |
| `action-parity` | `hasPermission`, `subject:action` literals, maker/checker actions, `ACCESS_*` | Controls fail closed because CES actions were not flattened into the old keys. |
| `ownership` | `assignee`, `moduleOwner`, `owner`, saved views, saved filters, creator/role writes | Reads are incomplete or writes use an arbitrary role owner. |
| `tile-routing` | EMS2/EMS3 flags, entitlement routes, tile IDs, application scopes, duplicate routes | A partial rollout drops tiles or resolves the same feature to conflicting providers. |
| `data-scope` | `data_profiles`, `data_policies`, `dataEntitlementRoles`, authorization limits, `PSS_RO` | Data access becomes empty, malformed, or incorrectly restricted. |
| `admin-token` | `FMO PORTAL ADMIN`, category/import-map/tile administration, token role validation | Admin requests lose their legacy role owner or are rejected. |
| `lifecycle-cache` | module-level permission booleans, memoized auth decisions, provider initialization order | A session keeps stale permissions or evaluates before CES data exists. |
| `configuration-alias` | feature-flag entitlement names, EMS2 subject aliases, blank CES feature fields | Features silently disappear or are admitted then denied. |
| `verification` | EMS2-only fixtures, missing roleList cases, missing empty-grant cases, no live evidence | The code may be compatible, but the migration boundary is unverified. |

## Disposition guidance

- Use `lower-layer-preservable` only when the old API has enough capacity for an additive projection and the mapping is deterministic.
- Use `hard-incompatibility` when valid CES data has more cardinality or semantics than the old field can represent, such as multiple owners or profiles.
- Use `conditional` when the old contract works for EMS2-only or one-role users but fails for CES-only, multi-role, mixed-provider, or conflicting-route cases.
- Use `latent` when static inspection found no reachable production caller. Keep the finding because future imports or indirect calls can activate it.
- Use `verification-gap` when the implementation appears compatible but the test or runtime evidence does not cover the relevant CES shape.
