# Architecture source binding review

Review date: 18 November 2026.
Scope: Two changed BFF sources referenced by the saved architecture context.

> [!IMPORTANT]
> Both graph relationship assessments retain source support.
> The context now binds their current hashes, revisions, and exact source ranges.
> This review establishes no deployment, active routing, or runtime execution.

The saved source revision was `95480c0e2563bc2a5a639bca1f22ecedb61936c2`.
The current source revision is `d93455b6533bc017ab6bc42b0b585b804e1e96a1`.
Both prior snapshots match their saved Git revision.
Both current files match the current Git revision and have no local changes.

The controller removed `entitlementRouting` construction from authentication responses.
The utility now reads `entitlementSource` from catalog rows.
Neither reviewed graph claim asserts these field semantics.
Response compatibility was outside this graph review.

| Claim | Assessment | Reviewed support |
| --- | --- | --- |
| `shell-bff-api` | `SUPPORTED` | Seven HTTP method and path declarations retain exact text at new lines. |
| `shell-loads-container` | `INFERRED` | Container, module, and tile metadata retain exact text at existing lines. |

| Source | Previous range | Current range |
| --- | --- | --- |
| `bff-auth-controller` | 171–173 | 167–169 |
| `bff-auth-controller` | 327–329 | 317–319 |
| `bff-auth-controller` | 215–217 | 209–211 |
| `bff-auth-controller` | 267–269 | 259–261 |
| `bff-auth-controller` | 299–301 | 289–291 |
| `bff-auth-controller` | 352–354 | 342–344 |
| `bff-auth-controller` | 384–386 | 372–374 |
| `bff-catalog-props` | 203–217 | 203–217 |

The [review record](source-review.json) retains source identities, hashes, and range mappings.
The [source diff](source-review.diff) records every source change against the captured snapshots.
The [prior context](source-review-context-before.json) and referenced prior source bytes remain retained here.
The [current context](../../../../relationships/service-dependencies/architecture-context.json) changes only two source bindings and seven range pairs.

The [automated check](source-review-check.json) verified all 43 sources and 19 investigations.
It compared all eight reviewed ranges and found no remaining source drift.
No business source file changed during this work.

Owner: UNKNOWN.
Outcome: The dependency graph was rebuilt with the refreshed context.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Source inspection does not establish response compatibility or runtime execution.
```
