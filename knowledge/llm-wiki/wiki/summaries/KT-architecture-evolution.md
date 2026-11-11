---
type: "Summary"
description: "Maps historical UI evaluations, experiments, and platform proposals with unresolved decisions."
doc_type: short
full_text: "sources/KT-architecture-evolution.md"
---

# Architecture Evolution and Proposal Boundaries — Summary

Source: KT-architecture-evolution (this document)

The document is a knowledge topic that organizes several independent UI and platform investigations. It separates documented recommendations, experiments, and future proposals from evidence of adoption. Its central claim is that the materials do not form one continuous, approved architecture roadmap.

## Key concepts and findings

### Component-library evaluation
- Compares [[entities/mui]], [[entities/ant-design]], and [[entities/ag-grid]] using GitHub statistics dated 5 July 2023, plus components, styling, and licensing criteria.
- The Ant Design note focuses on forms, feedback components, and layout differences.
- The conceptual-design draft still contains placeholders and unresolved rationale. Its review and decision tables do not prove approval, and its approval link points to an unrelated ClickHouse design.
- Implication: historical comparison cannot establish current library capability or an accepted purchasing decision. See [[concepts/component-library-selection]].

### Composition as a migration constraint
- The UI stack distinguishes [[entities/systemjs]] module resolution from [[entities/single-spa]] lifecycle management.
- The development guideline records shared [[entities/mui]] themes and a specific [[entities/react]] version.
- Implication: build-tool or dependency changes can affect the portal loading boundary, not just individual application builds. See [[concepts/microfrontend-layering]] and [[concepts/shared-dependency-governance]].

### Build-tool research
- Recommends [[entities/rspack]] for incremental migration from [[entities/webpack]] and [[entities/vite]] for new or simpler applications.
- Treats [[entities/systemjs]] compatibility as an architectural constraint.
- Proposes a pilot that checks loading, HMR, and asset paths before gradual rollout.
- Also suggests a longer-term move away from SystemJS, which changes the platform boundary beyond a bundler swap.
- The report has no publication date or retained benchmark provenance. Its recommendations are research statements, not verified conclusions. See [[concepts/build-tool-migration]].

### Notification experiments
- The draft identifies many tiles opening separate subscription connections and proposes one SSE connection per user to reduce browser resource use.
- Three experiments are described: [[entities/graphql]] over SSE with Node.js, GraphQL over WebSocket with [[entities/spring-boot]], and SSE with a Spring Boot backend.
- The store draft declares `isRead` as a string but assigns boolean `false` in its event handler, leaving the field contract unresolved.
- The table schema separates notification topics, user subscriptions, notification messages, and per-user read or display state. Retention is proposed as one hour, six hours, or 24 hours, but no rule is accepted.
- Implication: protocol, schema, cleanup behavior, and production adoption remain unproved. See [[concepts/realtime-notification-delivery]] and the notification data model.

### Platform proposals for 2026 and early 2027
- The deployment proposal covers tenant changes, workflow AI, telemetry, and infrastructure migration.
- It lists notification, persona dashboards, and [[entities/openfin]] as refining requirements.
- Target services separate authentication, tile management, telemetry, and AI.
- The current-architecture and target logical-architecture sections have no explanatory content, so service interfaces and migration paths are undefined.
- Implication: target service names cannot support implementation planning without accepted requirements and design. See [[entities/fmo-post-trade-portal]] for platform modernization context.

### Unchecked future-work list
- Proposes central-monitoring foundation work, [[entities/spring-boot]] 4.0.6 upgrade, moving properties into services, and removing account-and-password login.
- Provides no completion records, migration order, or accepted scope.
- Implication: the list cannot establish current platform versions or enabled login methods. See technical roadmap governance.

## Overall findings

- The materials mix historical evaluation, technical experiments, and future proposals. They should not be read as an approved architecture baseline.
- Recommendations require decision records, effective dates, and implementation evidence before adoption.
- Historical statistics and benchmark tables are context, not current performance predictions.
- Draft schemas and unchecked work lists are inputs to review, not generated requirements.

## Open questions

- Which component-library and licensing choices were accepted, and when?
- Who authored the build-tool research, and which versions and benchmark runs support it?
- Which notification experiment became a supported portal service?
- Which 2026 and 2027 target services have approved requirements and deployed implementations?
- Which notification retention and unread-message rules are accepted?
- Which unchecked work items have accepted scope, owners, and completion evidence?

## Evidence limits

The source manifest identifies local bytes but not original page revisions or confirmed source authority. Ownership is unknown. Citations support a reproducible reading, but they do not establish approved or current project intent. Source ownership, applicability, and original revisions should be confirmed before publication. See technical evidence assessment.

## Related topics

[[summaries/KT-portal-purpose]], [[summaries/KT-frontend-composition]], application interoperability, observability and performance, release operations.

## Related Concepts
- [[concepts/application-ownership]]
- [[concepts/frontend-onboarding]]
- [[concepts/portal-tile-workspace-model]]

## Entities
- [[entities/mfe-base]]
- [[entities/mfe-root-config]]
- [[entities/single-ui-bff]]
- [[entities/ems2]]
- [[entities/ces]]
- [[entities/fdc3]]
