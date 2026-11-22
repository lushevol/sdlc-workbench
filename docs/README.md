# Workbench documentation

This series gives the integrated current view of Workbench across its lifecycle and capability areas.
Maintain these pages as the system changes. Extend an existing subject before adding a new document.
Use [principles](../PRINCIPLE.md), [architecture](../ARCHITECTURE.md), and [workspace design](WORKSPACE_DESIGN.md) for the governing boundaries.
Open the [Workbench concept diagram](../ARCHITECTURE.md#workbench-concept) for the three layers and feedback loops, or the [full SDLC lifecycle diagram](../ARCHITECTURE.md#full-sdlc-lifecycle) for entry routes, phase controls, delivery, and learning.

## Read by lifecycle

| Stage | Current documentation and procedure | Result and handoff |
| --- | --- | --- |
| Adopt an existing system | [Workspace design](WORKSPACE_DESIGN.md#brownfield-adoption-boundary), [repository onboarding](../.agents/skills/repository-onboarding/SKILL.md), [setup](SETUP.md), [dependencies](DEPENDENCIES.md) | Select supported assets and tools, register their identities, and state unsupported scope. |
| Configure access and agent context | [Connectors](CONNECTORS.md), [hooks](HOOKS.md), [registry guide](../registry/README.md) | Configure local settings, exact operation grants, and the active work record. Configuration does not establish service access. |
| Capture and refine work | [Task guide](../tasks/README.md), [requirement analysis](../.agents/skills/analyze-requirement/SKILL.md), [question reconciliation](QUESTION_RECONCILIATION.md), [Gherkin quality](GHERKIN_QUALITY.md) | Preserve input, investigate existing evidence, define the next phase, and resolve material intent questions. Maintenance uses its lighter work record. |
| Maintain and retrieve intent | [Knowledge lifecycle](KNOWLEDGE_LIFECYCLE.md), [knowledge contract](../knowledge/README.md), [lifecycle coordinator](../.agents/skills/manage-knowledge-lifecycle/SKILL.md) | Prepare sources, review canonical claims, apply governance, and maintain one derived wiki. Keep each lifecycle's state separate. |
| Analyze, design, and implement | [Architecture](../ARCHITECTURE.md), [workspace design](WORKSPACE_DESIGN.md), [impact analysis](../.agents/skills/impact-analysis/SKILL.md), [Ponytail](../.agents/skills/ponytail/SKILL.md) | Trace affected consumers and contracts, compare old and intended behavior, and follow the owning repository's implementation rules. |
| Review and verify | [Code review](../.agents/skills/code-review/SKILL.md), [implementation verification](../.agents/skills/verify-implementation/SKILL.md), [behavior review](BEHAVIOR_REVIEW.md), [review index](REVIEW_INDEX.md) | Inspect code and assertions, retain exact evidence, and report AC-to-test, AC-to-change, and change-to-test coverage separately. |
| Prepare and execute tests | [Preflight](TEST_PREFLIGHT.md), [browser investigations](BROWSER_INVESTIGATIONS.md), [Robot testing](ROBOT_TESTING.md), [Gherkin quality](GHERKIN_QUALITY.md) | Check the selected environment, run the existing authorized runner, and save each completed case with its assertions and limits. |
| Assess release and delivery | [Release confidence](../.agents/skills/release-confidence/SKILL.md), [release reports](RELEASE_REPORT.md), [Release Clinic](RELEASE_CLINIC.md) | Combine business and system impact, conformance, tests, and operational evidence. Keep recommendations and human deployment authorization distinct. |
| Learn and maintain | [Capability learning](CAPABILITY_LEARNING.md), [task handoff](../tasks/README.md), [reusable domain experience](EXPERIENCE_ASSETS.md), [release knowledge synchronization](../.agents/skills/sync-release-knowledge/SKILL.md), [knowledge lifecycle](KNOWLEDGE_LIFECYCLE.md) | Update current documentation, source-backed intent, and reusable experience while retaining change history, unresolved gaps, and supporting evidence in the owning task. |

## Read by capability

These areas follow the [six core capabilities](../ARCHITECTURE.md#six-core-capabilities).
They describe Workbench responsibilities. Project business domains keep their intended rules and target architecture in `knowledge/records/`.

| Capability area | Maintained reference owners | Important boundary |
| --- | --- | --- |
| Context Registry | [Workspace design](WORKSPACE_DESIGN.md#asset-identities-and-local-locations), [registry guide](../registry/README.md), [setup](SETUP.md), [dependencies](DEPENDENCIES.md) | Repository, service, capability, contract, source, and tool identities remain separate. |
| Knowledge Governance | [Knowledge lifecycle](KNOWLEDGE_LIFECYCLE.md), [knowledge contract](../knowledge/README.md), [question reconciliation](QUESTION_RECONCILIATION.md) | Source evidence, canonical intent, and derived wiki have separate responsibilities and review states. |
| Relationship Engine | [Traceability](WORKSPACE_DESIGN.md#traceability), [graph procedure](../.agents/skills/service-dependencies-graph/SKILL.md), [review index](REVIEW_INDEX.md) | Declared links and static discovery need supporting evidence and explicit extraction limits. |
| Verification Engine | [Behavior review](BEHAVIOR_REVIEW.md), [review index](REVIEW_INDEX.md), [Gherkin quality](GHERKIN_QUALITY.md), [preflight](TEST_PREFLIGHT.md), [browser investigations](BROWSER_INVESTIGATIONS.md), [Robot testing](ROBOT_TESTING.md) | Structure, freshness, readiness, assertions, and passing business execution are different claims. |
| Workflow Engine | [Task guide](../tasks/README.md), [hooks](HOOKS.md), [shared skills](../.agents/skills/), [knowledge lifecycle](KNOWLEDGE_LIFECYCLE.md) | Skills coordinate agent procedures. Hooks provide advisory context and checks. No durable workflow runner is implied. |
| Tool Registry | [Registry guide](../registry/README.md), [connectors](CONNECTORS.md), [Release Clinic](RELEASE_CLINIC.md), [release reports](RELEASE_REPORT.md) | Registration does not grant execution. Installed providers and exact configured grants govern available operations. |

## Keep current documentation and history connected

`docs/` owns the overall current explanation: responsibilities, interfaces, supported procedures, configuration, and material limits.
`tasks/<task-id>/` owns the timeline of individual changes: user input, decisions, investigations, evidence, and outcomes.
Use the [task guide](../tasks/README.md) for business intake or the lighter maintenance route.
Task history does not create another current specification.

Before a consequential task is handed off, update each affected existing guide to the resulting current state.
Record the changed sections and links in the task, or explain why the work has no documentation impact.
Do not create a new guide for each feature, task, review, or release.
Add a page only when a stable subject has no suitable owner in this series; update both maps in the same change.
Keep one canonical explanation of each contract and link it from other views.

Keep business intent in canonical knowledge, implementation and conformance evidence in tasks and repositories, and runtime authoring resources under `core/`.
Apply the [retention rules](../tasks/README.md#critical-evidence-and-reusable-payloads) before removing or relocating historical material.
Preserve source revisions, meaningful failed evidence, and immutable audit history.

## Read states and evidence

Label implemented behavior, proposed design, source-inspected conclusions, actual execution, and deployment observations separately.
A source review can explain implementation without proving that it ran in a target environment.
A passing command, valid contract, fresh hash, or compiled wiki does not establish business conformance, acceptance, or deployment approval.
Keep unknown scope and unsupported environments visible beside the relevant instructions.
The documentation maintenance procedure adds no runtime gate, automatic synchronization, or approval engine.
