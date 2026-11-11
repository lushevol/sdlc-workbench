---
type: "Concept"
sources: ["summaries/KT-architecture-evolution.md"]
description: "Evaluating and choosing a shared UI component library for the portal's microfrontends."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Component Library Selection

## Definition

Component library selection is the evaluation and decision process for adopting a shared UI component library or design system across the portal's microfrontends. It covers component coverage, styling and theming approach, licensing obligations, data-heavy widgets, and compatibility with the portal's shared-dependency and loading boundaries.

## Why it matters in this portal

Tiles are composed as separately built microfrontends and share runtime dependencies through [[entities/systemjs]] module resolution and [[entities/single-spa]] lifecycle management. A component library adopted by more than one tile therefore becomes a cross-tile contract, not a local implementation detail:

- Themes and design tokens must be shared consistently rather than duplicated per tile.
- A library depends on [[entities/react]], so version alignment affects the shared dependency surface.
- Bundling and loading behavior interacts with [[concepts/build-tool-migration]] and [[concepts/shared-dependency-governance]].
- Licensing terms apply to every tile that ships the library.

## Documented evaluation

The library comparison in the source material compares [[entities/mui]], [[entities/ant-design]], and [[entities/ag-grid]] across components, styling, licensing, and related criteria. Some GitHub statistics in that comparison are dated 5 July 2023.

The Ant Design note emphasizes forms, feedback components, and layout differences from the alternatives. AG Grid appears as the data-grid-oriented option, while MUI is assessed for general component breadth and theming.

Typical criteria reflected in the material:

| Criterion | What the evaluation considers |
|---|---|
| Component coverage | Forms, feedback, layout, and data-grid needs |
| Styling and theming | Shared themes, design consistency across tiles |
| Licensing | Cost and redistribution obligations for each tile |
| Integration fit | Compatibility with React versions and shared dependencies |
| Application needs | Whether the library supports the portal's tile use cases |

## Draft rationale is incomplete

The conceptual-design draft contains unresolved rationale and selection placeholders. Its review and decision tables do not establish completed approval, and its approval link points to a ClickHouse design without explaining the relevance. The draft should be kept separate from a completed architecture decision.

## Status and evidence limits

- The comparison is a historical snapshot. It does not establish present library capabilities.
- No accepted purchasing or licensing decision is recorded in the material.
- The incomplete draft cannot establish an accepted current technology standard.
- Completion of the evaluation does not imply adoption by any specific tile.

These limits are recorded in [[summaries/KT-architecture-evolution]].

## Relationship to onboarding and layering

A selected library shapes [[concepts/frontend-onboarding]] because new tiles inherit the approved component set and theme conventions. It also interacts with [[concepts/microfrontend-layering]], since shared UI packages sit at a layer below individual tiles and above the shell.

## Open questions

- Which component-library and licensing choices have accepted decisions, and what are their effective dates?
- Where are the completed component and licensing decisions recorded, including the effective versions?
- How do the chosen library and theme conventions propagate to new tiles during onboarding?

## Related pages

- [[concepts/shared-dependency-governance]]
- [[concepts/build-tool-migration]]
- [[concepts/microfrontend-layering]]
- [[concepts/frontend-onboarding]]
- [[entities/mui]]
- [[entities/ant-design]]
- [[entities/ag-grid]]
- [[entities/react]]
- [[summaries/KT-architecture-evolution]]