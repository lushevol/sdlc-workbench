---
sources: ["summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md"]
type: "Product"
description: "React component library evaluated for shared theming in the portal."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

## What it is

MUI is a React component library. It appears in two roles in the documented material: the development guideline prescribes shared MUI themes for applications in the FMO Post Trade Portal, and a separate component-library comparison evaluated MUI alongside [[entities/ant-design]] and [[entities/ag-grid]]. The comparison is an evaluation record, not proof that MUI was adopted as the standard.

The document set does not record an accepted MUI version, licence arrangement, or the exact set of components exposed through shared packaging. Those details remain unresolved.

## Key facts from the source

- The development guideline prescribes **shared MUI themes** as part of the common styling baseline for applications built on the documented microfrontend model.
- The guideline requires separation of view, logic, styles, and interfaces — implying that styling concerns, including MUI theme usage, are kept distinct from component logic.
- The guideline pairs this styling guidance with [[entities/react]] 18.2.0 and a preference for Context and Reducer over additional state libraries. Both instructions carry the same versioning caveat: the document has no effective date or supersession record, so the guidance cannot be treated as the confirmed current baseline.
- The standalone React template consumed components from [[entities/mfe-base]] through import-map registration; the sources do not state explicitly whether those shared components are MUI-based wrappers, though the shared-theme rule suggests a common styling foundation.
- The component-library comparison recorded in [[summaries/KT-architecture-evolution]] compares MUI, Ant Design, and AG Grid across components, styling, licensing, and related criteria. It records GitHub statistics dated 5 July 2023.
- The comparison's historical date means its figures describe evaluation context in 2023. They do not establish MUI's present capabilities, current licensing terms, or an accepted purchasing decision.
- The associated conceptual-design draft contains unresolved rationale and selection placeholders. Its review and decision tables do not establish completed approval, and its approval link points to a ClickHouse design without explaining relevance. The draft therefore does not confirm MUI selection.
- No source records whether MUI was chosen, rejected, or retained as one option among the three compared libraries.

## Why it matters for composition

Shared theming is one of the mechanisms that make independently owned applications look and behave consistently inside [[entities/fmo-post-trade-portal]]. It is a cross-tenant concern and therefore falls under [[concepts/shared-dependency-governance]]: an MUI upgrade or theme contract change can affect every consumer at once, and coordinated upgrades are required.

Because MUI sits in the shared layer, its handling also bears on [[concepts/microfrontend-layering]] (which layer owns the theme context) and on [[concepts/application-ownership]] (which team approves changes to a shared styling contract used by tenant teams).

The comparison context adds a decision-record dimension. [[concepts/component-library-selection]] covers the evaluation criteria, but the available material does not show an accepted selection outcome. Teams should not treat MUI as the confirmed standard without locating the decision record and its effective date.

## Open questions

- Which MUI version and theme package are currently accepted?
- Was MUI formally selected from the 2023 comparison, and if so, when and by whom?
- Which licensing terms were evaluated, and did they affect the selection?
- Who owns and approves changes to the shared theme contract?
- Are tenant teams permitted to override shared themes locally, and under what review?
- How is MUI supplied — bundled per application, or registered as a shared dependency alongside other common libraries?

## Related

- [[summaries/KT-frontend-composition]]
- [[summaries/KT-architecture-evolution]]
- [[entities/react]]
- [[entities/ant-design]]
- [[entities/ag-grid]]
- [[entities/mfe-base]]
- [[concepts/component-library-selection]]
- [[concepts/shared-dependency-governance]]
- [[concepts/microfrontend-layering]]
- [[concepts/application-ownership]]
- [[concepts/frontend-onboarding]]

See also: [[summaries/KT-portal-purpose]]