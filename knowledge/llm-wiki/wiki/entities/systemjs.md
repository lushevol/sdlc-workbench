---
sources: ["summaries/KT-admin-and-onboarding.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md"]
type: "Product"
description: "Module loader in the portal microfrontend design and a constraint on build-tool migration."
---

# SystemJS

SystemJS is the module loader named in the documented microfrontend composition model. It resolves registered module names to deployed JavaScript files and loads those modules into the page. The UI stack explanation separates this module-resolution role from the lifecycle management performed by [[entities/single-spa]].

## Role in the composition model

Within the four-layer design described in [[summaries/KT-frontend-composition]], SystemJS sits between the root configuration and application loading:

| Element | Documented responsibility |
| --- | --- |
| Root configuration and import map | Locate modules and support shared loading configuration. |
| **SystemJS** | Resolve module names to files and load modules into the page. |
| [[entities/single-spa]] | Mount applications and manage application lifecycle. |
| Base container | Provide common routing, global state, and theme context. |
| Application container and tiles | Supply domain modules and user-facing views. |

[[entities/single-spa]] registers only the shell; SystemJS, together with React Router, supports the successive loading of application containers and feature tiles. The [[entities/mfe-root-config]] and its import map supply the name-to-file registrations that SystemJS consumes.

## Import maps and shared modules

The design uses export and import statements to share modules through registered names. Import maps connect those names to deployed files, so a shared module such as [[entities/mfe-base]] can be consumed by multiple tenant applications without each application bundling its own copy.

Because several applications may resolve the same registered name, shared dependencies require coordinated upgrades — see [[concepts/shared-dependency-governance]]. The development guideline records shared [[entities/mui]] themes and a specific [[entities/react]] version as part of this baseline.

## Migration and build-tool research

The build-tool research in [[summaries/KT-architecture-evolution]] treats SystemJS compatibility as an architectural constraint. That research recommends [[entities/rspack]] for incremental migration from [[entities/webpack]] and [[entities/vite]] for new or simpler applications. Its proposed pilot checks loading, hot module replacement, and asset paths before gradual rollout.

The same research proposes a longer-term move away from SystemJS. That suggestion changes the platform loading boundary beyond a bundler substitution and requires separate architectural review. Changed output formats or shared dependencies can affect the portal loading boundary, so a migration must consider more than individual application builds — see [[concepts/build-tool-migration]].

The research report has no publication date and no retained project benchmark provenance. Its recommendations remain research statements, not verified technical conclusions or accepted migration instructions.

## Evidence limits

The sources describe SystemJS as part of the intended loading design. They do not establish the exact SystemJS version, its runtime configuration in active deployments, or reproducibility of the setup procedure, since referenced archives and setup screenshots are absent from the supplied copy. Current loading compatibility therefore requires separate inspection.

The materials do not record an accepted decision on retaining or replacing SystemJS. Applicable implementation versions and any approved migration scope remain unresolved.

## Related pages

- [[concepts/microfrontend-layering]]
- [[concepts/shared-dependency-governance]]
- [[concepts/build-tool-migration]]
- [[entities/single-spa]]
- [[entities/mfe-root-config]]
- [[entities/mfe-base]]
- [[entities/rspack]]
- [[entities/vite]]
- [[entities/webpack]]
- [[summaries/KT-frontend-composition]]
- [[summaries/KT-architecture-evolution]]

See also: [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-admin-and-onboarding]]