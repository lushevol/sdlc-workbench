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
| The default overview remains unchanged. | [Overview pair panel 1](svg/01-overview-before.svg) / [Overview pair panel 2](svg/01-overview-after.svg), three links in both snapshots | Default navigation does not expose most new detail. | Skill maintainer; person UNKNOWN | Make repository detail and changed areas easier to find. |
| Business enrichment remains small. | [Business pair panel 1](svg/03-business-before.svg) / [Business pair panel 2](svg/03-business-after.svg), 323 versus 333 relationships | Larger total counts cannot establish richer capability structure. | Skill maintainer; person UNKNOWN | Review missing Business relationships against source evidence. |
| More Runtime records do not establish clearer presentation. | [Configuration pair panel 1](svg/06-configuration-before.svg) / [Configuration pair panel 2](svg/06-configuration-after.svg) | Clipped names and overlapping connections hide identity and direction. | Skill maintainer; person UNKNOWN | Improve label expansion, role placement, edge routing, and grouping. |
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

- [Parent versus latest local: Runtime panel 1](svg/16-parent-vs-local-runtime-parent.svg) / [Parent versus latest local: Runtime panel 2](svg/16-parent-vs-local-runtime-after.svg)
- [Parent versus latest local: Business panel 1](svg/17-parent-vs-local-business-parent.svg) / [Parent versus latest local: Business panel 2](svg/17-parent-vs-local-business-after.svg)
- [System overview panel 1](svg/01-overview-before.svg) / [System overview panel 2](svg/01-overview-after.svg)
- [Runtime dimension panel 1](svg/02-runtime-before.svg) / [Runtime dimension panel 2](svg/02-runtime-after.svg)
- [Business dimension panel 1](svg/03-business-before.svg) / [Business dimension panel 2](svg/03-business-after.svg)
- [Provided APIs panel 1](svg/14-provided-before.svg) / [Provided APIs panel 2](svg/14-provided-after.svg)
- [Outbound API calls panel 1](svg/04-api-before.svg) / [Outbound API calls panel 2](svg/04-api-after.svg)
- [GraphQL calls and documents panel 1](svg/15-graphql-before.svg) / [GraphQL calls and documents panel 2](svg/15-graphql-after.svg)
- [Storage and columns panel 1](svg/05-storage-before.svg) / [Storage and columns panel 2](svg/05-storage-after.svg)
- [Configuration panel 1](svg/06-configuration-before.svg) / [Configuration panel 2](svg/06-configuration-after.svg)
- [Internal Java dependencies panel 1](svg/07-internal-java-before.svg) / [Internal Java dependencies panel 2](svg/07-internal-java-after.svg)
- [Shared web symbols panel 1](svg/08-shared-web-before.svg) / [Shared web symbols panel 2](svg/08-shared-web-after.svg)
- [Messaging panel 1](svg/09-messages-before.svg) / [Messaging panel 2](svg/09-messages-after.svg)
- [Package dependencies panel 1](svg/10-packages-before.svg) / [Package dependencies panel 2](svg/10-packages-after.svg)
- [Testing dependencies panel 1](svg/11-testing-before.svg) / [Testing dependencies panel 2](svg/11-testing-after.svg)
- [Parent source: Runtime panel 1](svg/12-parent-runtime-parent.svg) / [Parent source: Runtime panel 2](svg/12-parent-runtime-parent_after.svg)
- [Parent source: Business panel 1](svg/13-parent-business-parent.svg) / [Parent source: Business panel 2](svg/13-parent-business-parent_after.svg)
