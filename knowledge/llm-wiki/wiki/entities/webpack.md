---
sources: ["summaries/KT-architecture-evolution.md"]
type: "Product"
description: "JavaScript module bundler named as the incumbent tool in the portal's build-tool migration research."
---

# Webpack

Webpack is a JavaScript module bundler. In the source materials it appears as the incumbent build tool that the portal's microfrontend applications use, and as the baseline that migration research measures alternatives against.

## Key facts from the source

- The build-tool research recommends [[entities/rspack]] for **incremental migration from Webpack**, and [[entities/vite]] for new or simpler applications. Webpack is therefore treated as the tool to move away from, not the target.
- The research treats [[entities/systemjs]] compatibility as an architectural constraint on any bundler change. Webpack configuration and output shape sit inside that loading boundary managed by [[entities/single-spa]].
- The proposed migration path is a pilot that checks loading, HMR, and asset paths before a gradual rollout — implying a period in which Webpack-built and non-Webpack-built applications coexist.
- The report also proposes a longer-term move away from [[entities/systemjs]], which would change the platform boundary beyond a bundler substitution.

## Status and evidence limits

The research report has no publication date and no retained benchmark provenance. Its performance rankings and migration recommendations are research statements, not verified conclusions or accepted migration instructions. Nothing in the materials establishes an approved decision to replace Webpack, a migration schedule, or ownership of that work.

## Related

- [[concepts/build-tool-migration]] — the migration options and pilot approach.
- [[concepts/shared-dependency-governance]] — shared libraries such as [[entities/react]] and [[entities/mui]] themes that bundler changes can affect.
- [[concepts/microfrontend-layering]] — how applications and the root configuration relate.
- [[entities/mfe-root-config]], [[entities/mfe-base]] — portal composition points affected by build output.
- [[summaries/KT-architecture-evolution]] — the topic that records this research.
- [[summaries/KT-frontend-composition]] — loading and ownership boundaries.
