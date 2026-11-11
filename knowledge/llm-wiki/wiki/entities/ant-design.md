---
sources: ["summaries/KT-architecture-evolution.md"]
type: "Product"
description: "A React component library evaluated alongside MUI and AG Grid in the TPT UI library comparison."
---

# Ant Design

Ant Design is a React UI component library. In this knowledge base it appears as a candidate evaluated in the UI library comparison for the [FMO Post Trade Portal]([[entities/fmo-post-trade-portal]]).

## Role in the documented evaluation

- The comparison in [[summaries/KT-architecture-evolution]] places Ant Design alongside [MUI]([[entities/mui]]) and [AG Grid]([[entities/ag-grid]]).
- Criteria include available components, styling approach, and licensing terms.
- The dedicated Ant Design note emphasizes forms, feedback components, and layout differences compared with the alternatives.
- Some comparison statistics are GitHub figures dated 5 July 2023, so the material is explicitly historical.

## Decision status

No accepted selection or licensing decision is documented. The conceptual-design draft associated with the comparison still contains unresolved rationale and placeholder tables, and its approval link points to an unrelated design. The evaluation therefore records concerns at a point in time rather than an adopted standard. See [[concepts/component-library-selection]].

## Caveats

- The dated statistics do not describe current library capabilities.
- Any future adoption would interact with the shared theme approach recorded in the portal development guideline, and with the composition constraints of [single-spa]([[entities/single-spa]]) and [SystemJS]([[entities/systemjs]]) described in [[concepts/microfrontend-layering]].
- Ownership of the comparison material is unknown, and source revisions have not been confirmed.

## Related

- [MUI]([[entities/mui]])
- [AG Grid]([[entities/ag-grid]])
- [React]([[entities/react]])
- [[concepts/component-library-selection]]
- [[concepts/shared-dependency-governance]]
- [[summaries/KT-architecture-evolution]]
