---
type: "Concept"
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-release-operations.md", "summaries/KT-observability-and-performance.md", "summaries/KT-application-interoperability.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md"]
description: "Rules and practices controlling shared code, library versions, and module interfaces across teams."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Shared dependency and compatibility governance

## Definition

Shared dependency and compatibility governance is the set of rules, roles, and coordination practices that control how common code, library versions, build tooling, and module interfaces are shared across independently owned applications. In a [[concepts/microfrontend-layering]] model, tenant teams release separately but still consume a common base, so every shared interface is a potential cross-team compatibility boundary.

[[summaries/KT-frontend-composition]] records the documented model: shared platform modules supply common context, while application teams supply containers and tiles. The governance question is who controls change at the seams between them.

## Why shared dependencies need governance

The design shares modules through exports, imports, and registered names resolved by [[entities/systemjs]] and mounted by [[entities/single-spa]]. The framework comparison in the source distinguishes shared dependencies from libraries retained inside individual applications. It cautions that shared dependencies require coordinated upgrades.

Inference from the source: a shared interface change can affect several tenant consumers at once, because a single registered module name may be loaded by multiple containers and tiles. This inference requires exact provider and consumer evidence before assessing a particular change. No such provider/consumer inventory is recorded.

Shared dependencies also include the toolchain that produces each application bundle. [[summaries/KT-architecture-evolution]] records build-tool research that treats [[entities/systemjs]] compatibility as an architectural constraint. The research recommends [[entities/rspack]] for incremental migration from [[entities/webpack]] and [[entities/vite]] for new or simpler applications. It proposes a pilot that checks loading, HMR, and asset paths before gradual rollout. Because a bundler change can alter output formats and shared dependency handling, it is a platform-level compatibility decision, not a local application choice. The report has no publication date or retained benchmark provenance, so its recommendations are research statements rather than accepted migration instructions. See [[concepts/build-tool-migration]].

Shared contracts are not limited to code modules. Event and API schemas are also cross-team interfaces. The notification table draft in the same source separates topics, subscriptions, messages, and per-user read state, but leaves retention and the `isRead` field contract unresolved. A shared event schema would need the same governance as a shared module before it could become a supported platform contract.

## Documented governance rules

- **Shared repositories are reviewed by the microfrontend team.** Application teams may choose their own deployment approach and must supply static-file and API URLs routed through [[entities/nginx]], but changes to shared repositories are reserved for review and approval by the platform team. See [[concepts/application-ownership]].
- **Shared backend availability belongs to the microfrontend team**, while application-domain backend availability belongs to each application team.
- **External GUI dependencies require an approved exception.** The supplementary principle prohibits direct external frontend dependencies unless platform governance reviews and approves an exception. Internal packaging and tenant-owned backend encapsulation are named implementation options.
- **Tenant teams retain residual risk responsibilities** for security, licensing, vulnerability, support, resilience, and rollback of any approved dependency.

## Version and standard coordination

The development guideline prescribes TypeScript, functional components, shared [[entities/mui]] themes, and separation of view, logic, styles, and interfaces. It names React 18.2.0 and prefers Context and Reducer over additional state libraries.

That version pin has no effective date or supersession record in the source. Its instructions therefore cannot be treated as the current platform baseline. Reuse for new development requires confirming accepted versions and the applicable guideline revision.

The standalone [[entities/react]] template reuses [[entities/mfe-base]] components through import-map registration. Its no-install statement concerns consuming those components; the template still installs its own dependencies. Current template and shared-component compatibility require separate inspection.

Component-library choice is a related shared standard. The library comparison evaluates [[entities/mui]], [[entities/ant-design]], and [[entities/ag-grid]] using GitHub statistics dated 5 July 2023. The conceptual-design draft retains placeholders and an approval link to an unrelated ClickHouse design, so it does not establish an accepted component standard or purchasing decision. See [[concepts/component-library-selection]].

The build-tool research adds a further boundary question. Its longer-term suggestion to move away from SystemJS would change the platform loading boundary beyond a bundler substitution. That is a shared-interface change requiring explicit governance and an accepted migration path, not only a tooling preference. See [[concepts/build-tool-migration]].

## Interaction with onboarding

The documented [[concepts/frontend-onboarding]] sequence requires an application team to update module names, build configuration, imports, interfaces, container entry points, unit tests, and the local import map. Each of these steps touches a shared contract, which is where compatibility governance applies. The [[entities/mfe-root-config]] layer holds the import map and shared loading configuration that these steps modify.

A change in bundler or shared dependency format would also change these onboarding steps. Onboarding guidance and shared build configuration therefore need to be versioned together, with a clear statement of which template, module format, and shared-component versions are supported.

Optional performance guidance of 500 KB files and six concurrent static-file requests is suggested but does not establish an accepted SLA.

## Evidence limits

The source manifest identifies local bytes without original page revisions or confirmed source authority, so the rules are reproducible readings rather than verified approvals. Current named owners and effective approvals are unknown. The missing template archives prevent verifying which shared-component versions actually work together. The build-tool report lacks publication date and retained benchmark provenance, and the component-library statistics are dated 2023. These gaps prevent treating any recommendation as a current standard.

## Open questions

- Which development guidelines and shared dependency versions are currently accepted?
- Which owner controls compatibility changes across shared modules and tenant applications?
- Which dependency exceptions have platform review, accountable tenant ownership, and effective dates?
- Which standalone template and shared-component versions remain supported?
- Which repository revisions implement the current container, tile, and routing interfaces?
- Which build-tool migration, if any, has an accepted decision and pilot evidence?
- Which component-library and licensing choice is the current standard, and since when?

## Related pages

- [[concepts/microfrontend-layering]]
- [[concepts/application-ownership]]
- [[concepts/frontend-onboarding]]
- [[concepts/build-tool-migration]]
- [[concepts/component-library-selection]]
- [[summaries/KT-frontend-composition]]
- [[summaries/KT-architecture-evolution]]
- [[entities/mfe-base]]
- [[entities/mfe-root-config]]
- [[entities/single-spa]]
- [[entities/systemjs]]

See also: [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-application-interoperability]]

See also: [[summaries/KT-observability-and-performance]]

See also: [[summaries/KT-release-operations]]

See also: [[summaries/KT-ces-migration-parity]]
