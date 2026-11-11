---
type: "Concept"
sources: ["summaries/KT-release-operations.md", "summaries/KT-observability-and-performance.md"]
description: "Revalidate layer entry files and long-cache hashed assets to speed loads, but updates still need a refresh."
---

# Microfrontend cache strategy and update detection

## Definition

A microfrontend cache strategy splits assets into two classes: small layer entry files that must be revalidated on every request, and content-hashed static assets that can be cached for a long time. Update detection is the mechanism that makes a new entry file point at new hashed assets, so a user picks up new UI code after a refresh or logout.

## Key details from the source

The cache guide proposes revalidation of layer entry files and longer caching of subsequent static files. Its expiry table assigns 120 days to chunks, images, CSS, fonts, JSON, and icons. A changed entry file should reference new subsequent files under the described approach.

- Entry files: revalidated so the browser sees a new asset manifest after a deployment.
- Hashed static assets: cached for 120 days because a content change produces a new file name.
- Update detection: a user still needs a logout or a page refresh to obtain updated UI code.
- Explicit limitation: the guide excludes a first-load improvement. The strategy targets repeat visits, not initial download size.

## Evidence status

These are documented design rules, not verified deployment facts. The cache implementation section contains no configuration. Current response headers, entry revalidation behaviour, and asset naming rules remain unverified. No server-header check ran during ingestion.

## Why the split matters

Layer entry files are the update signal. If an entry file is cached too long, the browser keeps an old asset manifest and users stay on old code. If chunks are not cached, every navigation re-downloads the same bytes. The 120-day value is safe only when asset names change on every content change, which depends on the build and bundler naming rules. See [[concepts/build-tool-migration]] for how bundler changes can affect hashing and emitted file names.

The strategy assumes a layered composition where each layer has its own entry point. See [[concepts/microfrontend-layering]] and [[entities/mfe-root-config]] for the composition context that supplies those layer entry points.

## Limits and open questions

- Which deployed cache settings and asset naming rules implement the documented strategy?
- Does the entry file revalidate correctly through every proxy and server in the path?
- Users need a refresh or logout, so the strategy does not give silent background updates.
- The guide gives no measured effect on load time.

## Related pages

- [[summaries/KT-observability-and-performance]] — the source topic that records the cache guide and its evidence limits.
- [[concepts/frontend-performance]] — performance measurement intent and reported browser metrics.
- [[concepts/build-tool-migration]] — bundler choice and asset naming that the cache rules depend on.
- [[concepts/microfrontend-layering]] — the layer structure that creates separate entry files.
- [[entities/mfe-root-config]] — the root layer entry that bootstraps the other layers.


See also: [[summaries/KT-release-operations]]