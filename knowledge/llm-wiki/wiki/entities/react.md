---
sources: ["summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md"]
type: "Product"
description: "JavaScript UI library used across the portal's microfrontend layers and standalone templates."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# React

## What it is

React is the JavaScript UI library used as the rendering foundation for the portal's frontend composition. It appears at every documented layer of the [[concepts/microfrontend-layering]]: the base shell, application containers, and feature tiles are React-based, and React Router drives the successive container and tile loading stages described in [[summaries/KT-frontend-composition]].

## Key facts from the sources

- **Version.** The development guideline names React 18.2.0 as the baseline. The source carries no effective date or supersession record, so this version cannot be treated as the confirmed current platform baseline.
- **Component style.** The guideline prescribes functional components written in TypeScript, with view, logic, styles, and interfaces kept in separate files.
- **State management.** Context and Reducer are preferred over introducing additional state libraries into tenant applications.
- **Styling.** Shared themes are delivered through [[entities/mui]], which tenant and platform modules consume rather than re-implement.
- **Routing.** React Router supports the successive container and tile loading that follows [[entities/single-spa]] registration of the shell, with props selecting distinct route stages.
- **Standalone template.** A React template project reuses [[entities/mfe-base]] components through import-map registration. Its "no install" claim concerns consuming those shared components only; the template still installs its own dependencies and ships with a Jest configuration.
- **Module loading.** Component resolution at runtime depends on [[entities/systemjs]] resolving registered module names, not on bundled React duplication.

## Boundaries and caveats

- The standalone guide depends on an absent `simple-app.zip` archive and screenshots, so its setup cannot be reproduced from the supplied text.
- Shared React and shared component versions must be upgraded in coordination across tenant applications; see [[concepts/shared-dependency-governance]].
- Current template, dependency, and loading compatibility require separate inspection before reuse in new development.

## Related pages

- [[summaries/KT-frontend-composition]]
- [[concepts/frontend-onboarding]]
- [[concepts/shared-dependency-governance]]
- [[entities/mfe-base]]
- [[entities/mui]]
- [[entities/single-spa]]
- [[entities/systemjs]]
- [[entities/fmo-post-trade-portal]]


See also: [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-architecture-evolution]]