---
sources: ["summaries/KT-architecture-evolution.md"]
type: "Product"
description: "Frontend build tool recommended in the portal's build-tool research for new or simpler applications."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Vite

Vite is a frontend build and development tool. In the portal's build-tool research, it is one of the two recommended options for React application builds.

## Role in the build-tool research

The research report recommends Vite **for new or simpler applications**. This is a narrower scope than its recommendation for [[entities/rspack]], which is proposed for incremental migration away from [[entities/webpack]] in existing applications.

Both recommendations sit within the portal's microfrontend architecture, where [[entities/systemjs]] module resolution and [[entities/single-spa]] lifecycle management are handled separately. The report treats SystemJS compatibility as an architectural constraint on any bundler choice, and it proposes a pilot that checks loading, HMR, and asset paths before gradual rollout. See [[concepts/build-tool-migration]] and [[concepts/microfrontend-layering]].

## Evidence status

The recommendation is a research statement, not an accepted migration instruction. The report carries no publication date and no retained benchmark provenance, and its performance tables lack the inputs and execution records needed to reproduce them. The proposed ranking therefore cannot predict results for these repositories. Vite's applicability to any specific tile requires a bounded project pilot and a recorded decision before adoption.

The research also proposes a longer-term move away from SystemJS. That change alters the platform loading boundary rather than substituting one bundler for another, and it affects shared dependency handling across tiles. See [[concepts/shared-dependency-governance]].

## Related pages

- [[summaries/KT-architecture-evolution]] — the topic that records this recommendation and its evidence limits.
- [[entities/rspack]] — the companion recommendation for incremental migration.
- [[entities/webpack]] — the incumbent bundler in the migration path.
- [[entities/react]] — the framework whose builds the tooling serves.
- [[concepts/component-library-selection]] — a separate, similarly unresolved evaluation thread.

## Open questions

Who authored the build-tool research, and which versions and benchmark runs support its Vite recommendation?

Owner: unknown. Next action: identify the report's provenance and evaluate a bounded project pilot before adopting the recommendation.