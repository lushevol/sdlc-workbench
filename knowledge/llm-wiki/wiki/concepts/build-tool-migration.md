---
type: "Concept"
sources: ["summaries/KT-architecture-evolution.md"]
description: "Proposed migration of portal React builds from Webpack to Rspack or Vite, constrained by SystemJS loading."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Build-Tool Migration

## Definition

Build-tool migration is the proposed replacement of the portal's JavaScript bundler and development tooling. The draft research recommends [[entities/rspack]] for incremental migration from [[entities/webpack]] and [[entities/vite]] for new or simpler applications. It also proposes a longer-term move away from [[entities/systemjs]]. These are research statements, not accepted migration instructions. See [[summaries/KT-architecture-evolution]].

## Why it matters

The portal loads tile applications through a shared composition layer. [[entities/single-spa]] manages application lifecycles, while [[entities/systemjs]] resolves modules at runtime. A bundler change therefore affects more than one application build. It can change output format, shared dependency resolution, and the portal loading boundary. See [[concepts/microfrontend-layering]] and [[concepts/shared-dependency-governance]].

## Documented landscape

The source materials record the following facts.

- The UI stack explanation separates SystemJS module resolution from single-spa lifecycle management.
- The development guideline records shared [[entities/mui]] themes and a specific [[entities/react]] version.
- The research report compares bundler options and treats SystemJS compatibility as an architectural constraint.
- The report recommends Rspack for incremental migration and Vite for new or simpler applications.
- The report proposes a pilot that checks loading, HMR, and asset paths before a gradual rollout.
- The report also proposes a longer-term move away from SystemJS. That change alters the platform boundary beyond a bundler substitution.

## Proposed approach

The documented proposal has two paths.

1. Incremental path. Keep the existing Webpack builds in service and migrate selected applications to Rspack. Validate loading, HMR, and asset paths in a pilot before broad rollout.
2. Greenfield path. Use Vite for new or simpler applications where SystemJS compatibility is not a constraint.

The proposal places the pilot before the rollout. The pilot is a proposed control, not an executed result.

## Migration constraints

- Runtime module resolution. SystemJS compatibility governs whether a new bundler output loads inside the portal shell. See [[entities/mfe-root-config]] and [[entities/mfe-base]].
- Shared dependencies. Shared React and MUI versions must stay consistent across tiles during a mixed-tooling period. See [[concepts/shared-dependency-governance]].
- Mixed tooling. Webpack, Rspack, and Vite builds can coexist only if the loading contract stays stable.
- Long-term boundary change. Removing SystemJS is a composition change, not a tooling change. It requires coordination with tile owners and onboarding steps. See [[concepts/frontend-onboarding]].

## Evidence limits

The research report has no publication date and no retained benchmark provenance. Its benchmark tables lack inputs and execution records. Its performance rankings therefore cannot predict results for these repositories. The recommendations remain research statements. They are not verified conclusions or accepted migration instructions. The applicable implementation versions require inspection before any inference is validated. See [[summaries/KT-frontend-composition]].

## Related topics

- [[concepts/component-library-selection]] records the parallel evaluation of frontend libraries.
- [[concepts/application-ownership]] defines who approves a migration per application.
- [[entities/webpack]], [[entities/rspack]], [[entities/vite]], [[entities/systemjs]], [[entities/single-spa]], [[entities/react]], [[entities/mui]].
- [[summaries/KT-architecture-evolution]] supplies the source context.

## Open questions

- Who authored the build-tool research?
- Which versions and benchmark runs support its recommendations?
- Which applications, if any, have completed or approved a migration?
- Which target tooling replaces SystemJS, and under what composition contract?

Next action: identify the report's provenance and run a bounded project pilot before adopting any recommendation.
