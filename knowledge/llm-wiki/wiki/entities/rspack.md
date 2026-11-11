---
sources: ["summaries/KT-architecture-evolution.md"]
type: "Product"
description: "Rust-based JavaScript bundler recommended for incremental migration from Webpack in the portal."
---

# Rspack

## What it is

Rspack is a JavaScript/TypeScript build tool (bundler) named in the portal's React build-tooling research as the recommended option for incremental migration away from [[entities/webpack]]. The source document, [[summaries/KT-architecture-evolution]], records this as a research recommendation rather than an accepted decision.

## Key facts from the source

- The research recommends **Rspack for incremental migration from Webpack** and [[entities/vite]] for new or simpler applications.
- It treats compatibility with [[entities/systemjs]] as an architectural constraint. [[entities/systemjs]] handles module resolution while [[entities/single-spa]] handles lifecycle management, so a bundler change touches the portal loading boundary, not only individual application builds.
- The proposed pilot checks module loading, hot module replacement (HMR), and asset paths before any gradual rollout.
- The same report proposes a longer-term move away from [[entities/systemjs]]. That suggestion changes the platform boundary beyond a bundler substitution and is not part of the Rspack recommendation itself.

## Evidence status

The report gives no publication date and retains no benchmark inputs or execution records. Its performance rankings therefore cannot predict results for the portal repositories. The Rspack recommendation is a research statement, not a verified conclusion or an accepted migration instruction.

Required before adoption: identify the report's provenance and run a bounded project pilot in the actual repositories.

## Related pages

- [[concepts/build-tool-migration]] — the migration path and pilot approach around this tool.
- [[concepts/microfrontend-layering]] — the loading boundaries a bundler change can affect.
- [[concepts/shared-dependency-governance]] — how shared dependencies such as [[entities/react]] and theme packages constrain tooling choices.
- [[entities/webpack]] — the incumbent bundler that Rspack would replace incrementally.
- [[entities/vite]] — the alternative recommended for new or simpler applications.
- [[entities/fmo-post-trade-portal]] — the platform whose applications the research concerns.

## Open questions

- Which Rspack version does the research assume, and which benchmark runs support its rankings?
- Has any pilot been executed, and what were its loading, HMR, and asset-path results?
- Is a migration decision accepted, with scope and effective date?

Owner: unknown.