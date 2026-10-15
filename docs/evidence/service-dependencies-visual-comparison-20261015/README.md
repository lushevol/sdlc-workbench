---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Diagram exports are not browser screenshots.
  - Selected examples do not represent every canonical relationship.
  - Static source facts do not establish runtime execution or complete dependency coverage.
---

# Graph comparison pictures

Comparison date: 15 October 2026.
The previous results established more extracted records.
They did not establish better visual usability.
The default overview and Business dimension show little visible change.

Open the [picture gallery](index.html) or the [summary image](00-summary.png).
The [comparison evidence](comparison.json) records counts, filters, selected identities, source hashes, and image hashes.

## Compared source sets

| Comparison | Left | Right | Interpretation |
| --- | --- | --- | --- |
| Direct parent comparison | Published parent, 13 graph repositories | Latest local, nine graph repositories | Source scope differs. Nine parent backend repositories are absent locally. |
| Local before and after | Previous local, eight graph repositories | Latest local, nine graph repositories | Testing creates the additional graph repository. Production counts exclude testing. |
| Identical parent source | Parent generator | Enhanced skill | The source set remains fixed. Both pictures use the latest drawing function. |

The original parent viewer uses a canvas renderer.
These exports show its graph data through the latest SVG drawing function.
They do not reproduce the original parent interface.
Old and latest local exports use their respective saved drawing functions.

Filters select dimension, repository, scope, relationship, and search terms before drawing.
Each example selects at most eight relationships.
The overview retains its three matching links.
The captions distinguish full category counts from selected examples.
A blank example does not establish an empty Runtime dimension.
Retained SVG files preserve the selected diagram renderings.

## Production comparison

| Area | Previous local | Latest local | Result |
| --- | ---: | ---: | --- |
| Highest aggregate links | 3 | 3 | Unchanged |
| Business relationships | 323 | 333 | Little change |
| Runtime relationships | 1,090 | 12,336 | Additional structure and dependency declarations |
| Provided API and handler relationships | 82 | 82 | Unchanged |
| Outbound API and document relationships | 290 | 344 | Selected additions and GraphQL corrections |
| Storage relationships | 13 | 83 | Entity and column mappings added |
| Configuration relationships | 0 | 2,566 | Keys, declarations, reads, and bindings added |
| Shared and internal code relationships | 14 | 5,481 | Source imports, symbol imports, injection, and typed calls added |
| Kafka messaging relationships | 0 | 0 | Unchanged |
| Package relationships | 374 | 374 | Unchanged |

The latest graph separately contains 420 testing nodes and 4,328 testing relationships.
Production scope hides these records initially.
The 41 provided APIs and eight database read relationships remain unchanged.
Added mapping declarations do not establish additional executed database access.

The parent source comparison leaves Business relationships unchanged at 1,419.
Its Runtime relationships increase from 2,840 to 24,738.
The direct parent-versus-local comparison cannot attribute count differences to extraction alone.

## Findings

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| The default overview remains unchanged. | [Overview pair](01-overview.png), three links in both snapshots | Default navigation does not expose most new detail. | Skill maintainer; person UNKNOWN | Make repository detail and changed areas easier to find. |
| Business enrichment remains small. | [Business pair](03-business.png), 323 versus 333 relationships | Larger total counts cannot establish richer capability structure. | Skill maintainer; person UNKNOWN | Review missing Business relationships against source evidence. |
| More Runtime records do not establish clearer presentation. | [Configuration pair](06-configuration.png) | Clipped names and overlapping connections hide identity and direction. | Skill maintainer; person UNKNOWN | Improve label expansion, role placement, edge routing, and grouping. |
| Several categories remain unchanged. | Provided API, messaging, and package pairs | Users cannot expect new detail in these categories. | Skill maintainer; person UNKNOWN | State unchanged categories beside new extraction results. |
| Testing inflated the previous combined totals. | Scope counts in comparison evidence | Combined totals can overstate changes visible in Production scope. | Skill maintainer; person UNKNOWN | Show production and testing totals separately. |
| Parent providers remain absent locally. | Direct parent comparison and repository census | Local source cannot supply those backend service internals. | Workspace maintainer; person UNKNOWN | Map available provider checkouts when the requested scope requires them. |

## Inspection and checks

The picture review checked summary, Runtime, Business, configuration, and parent Runtime exports.
Main captions and overlays fit.
The retained label truncation and overlapping links remain visible defects.
The snapshot bytes remain unchanged.
This stage adds comparison artifacts; it changes no extractor or viewer behavior.

Artifact checks validate image decoding, selected identities, source hashes, local links, and authored prose.
These checks do not establish browser layout quality or complete ASD-STE100 compliance.
Browser policy blocked direct screenshots and prohibited alternate browser surfaces.
The exports use local graph data and SVG drawing code.

## Picture index

- [Parent versus latest local: Runtime](16-parent-vs-local-runtime.png)
- [Parent versus latest local: Business](17-parent-vs-local-business.png)
- [System overview](01-overview.png)
- [Runtime dimension](02-runtime.png)
- [Business dimension](03-business.png)
- [Provided APIs](14-provided.png)
- [Outbound API calls](04-api.png)
- [GraphQL calls and documents](15-graphql.png)
- [Storage and columns](05-storage.png)
- [Configuration](06-configuration.png)
- [Internal Java dependencies](07-internal-java.png)
- [Shared web symbols](08-shared-web.png)
- [Messaging](09-messages.png)
- [Package dependencies](10-packages.png)
- [Testing dependencies](11-testing.png)
- [Parent source: Runtime](12-parent-runtime.png)
- [Parent source: Business](13-parent-business.png)
