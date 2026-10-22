# Current Workbench diagrams

The editable [drawing](../../../AI%20SDLC%20Workbench.drawio) contains four pages.
It updates the [earliest draft](../../../AI%20SDLC.drawio) from the current Workbench sources.
The draft contains both original views on one draw.io page.

The diagrams distinguish agent procedures, implemented runtime support, human decisions, and planned automation.
They describe the Workbench on 22 October 2026.
They do not establish business approval or passing business execution.

## Pages and exports

| Page | Purpose | Vector preview | Image preview |
| --- | --- | --- | --- |
| 1. Three loops | Intent, implementation, and observation share an evidence foundation. | [SVG](01-concept.svg) | [PNG](01-concept.png) |
| 2. Lifecycle control | Intake, readiness, implementation, review, execution, and feedback retain separate controls. | [SVG](02-lifecycle.svg) | [PNG](02-lifecycle.png) |
| 3. Architecture and skills | Agent interfaces, fourteen shared skills, runtime support, and existing assets have separate responsibilities. | [SVG](03-architecture.svg) | [PNG](03-architecture.png) |
| 4. Knowledge and evidence | Source provenance connects reviewed intent to code, assertions, observations, and scoped conclusions. | [SVG](04-evidence.svg) | [PNG](04-evidence.png) |

Open the drawing in diagrams.net or a compatible draw.io editor.
Each page uses editable native shapes, text, and connectors.
PNG previews use twice the drawing resolution.
SVG previews retain vector text and shapes.
The previews share the drawing's coordinate model.
After editing the drawing, export updated previews from the editor.

## Changes from the draft

The three viewpoints remain **Intent**, **Reality**, and **Observed**.
Each viewpoint now contains a feedback loop.
The shared Workbench hub connects context, knowledge, relationships, evidence, procedures, and granted execution.

The lifecycle includes readiness assessment and separate feedback paths for implementation, intent, and verification gaps.
Completed cases require immediate evidence retention.
Business decisions and knowledge publication retain their own review requirements.

The architecture adds the current skills and implemented support within the six architectural capability areas.
The evidence page adds source identities, exact revisions, inspected assertions, provenance, audit events, and environment identity.

## Controls and limits

Readiness applies to a named next phase.
Only `READY` permits that phase within existing authorization.
`READY_WITH_LIMITS` and `NEEDS_CLARIFICATION` permit further intake evidence collection only.
The runtime does not enforce this procedure or resume interrupted workflows.

Important requirements and decisions require recorded human review before publication.
Knowledge `verified` concerns reviewed knowledge claims.
It does not establish passing business execution.

Catalog declarations do not grant execution or prove deployed connectivity.
The runtime checks explicit operation grants and retains action evidence.
A successful command alone does not establish verified behavior.
Behavior evidence review always reports `NOT_VERIFIED` for business verification.

Automatic source ingestion, AI governance, complete mapping, complete automated behavior verification, and durable workflows remain planned.
Independent platform orchestration also remains planned.
Release Clinic analyzes release evidence and does not approve deployment.

## Source register

The inspected Workbench revision is `9e489fef435bd0a79055c7827b7882e48cd234d8`.
Source labels in diagram footers refer to this register.
The diagrams synthesize these sources; they do not introduce new runtime contracts.

| Label | Sources | Supported content |
| --- | --- | --- |
| S1 | [Principles](../../../PRINCIPLE.md#project-principles), [ownership](../../../PRINCIPLE.md#ownership-boundary) | Shared context, existing assets, evidence, and responsibility boundaries. |
| S2 | [Layers](../../../ARCHITECTURE.md#three-layers), [capabilities](../../../ARCHITECTURE.md#six-core-capabilities), [workflow](../../../ARCHITECTURE.md#core-workflow), [phases](../../../ARCHITECTURE.md#evolution-phases) | Architecture, lifecycle, readiness, and planned capabilities. |
| S3 | [Identities](../../WORKSPACE_DESIGN.md#asset-identities-and-local-locations), [governance](../../WORKSPACE_DESIGN.md#knowledge-format-and-governance), [traceability](../../WORKSPACE_DESIGN.md#traceability) | Separate identities, provenance, review, audit events, and evidence relationships. |
| S4 | [Impact analysis](../../../.agents/skills/impact-analysis/SKILL.md), [gap detection](../../../.agents/skills/detect-gaps/SKILL.md), [verification](../../../.agents/skills/verify-implementation/SKILL.md) | Change analysis, comparison, assertion inspection, and feedback. |
| S5 | [Task scope](../../../tasks/README.md#scope), [canonical cases](../../../tasks/README.md#canonical-gherkin-test-cases), [case checkpoints](../../../tasks/README.md#save-case-evidence-and-resume-checkpoints), [readiness](../../../tasks/README.md#decide-whether-intake-can-finish) | Business intake, maintenance scope, case evidence, and readiness procedure. |
| S6 | [Release Clinic analysis](../../../.agents/skills/release-clinic/SKILL.md#analyze-one-release) | Release evidence analysis and approval limits. |
| S7 | [Shared skills](../../../.agents/skills/), [skill guide](../../../README.md#shared-skills-and-agent-adapters) | Current skill inventory and agent interfaces. |
| S8 | [Runtime dispatch](../../../core/runtime.py), [execution](../../../core/execution/README.md), [ingestion](../../../core/ingestion/README.md), [behavior evidence review](../../BEHAVIOR_REVIEW.md#interpret-the-result), [assurance implementation](../../../core/assurance.py) | Grants, retained results, snapshot limits, source freshness, and `NOT_VERIFIED`. |

The original drawing's SHA-256 is `bff26cffb78900a884e93bd6a1fef2840b4961b5062dc1881f5dc22b9a76a213`.
Its bytes remain unchanged.

## Scope and validation

This documentation change has low implementation risk.
It adds the drawing, previews, and this guide.
It changes no runtime symbol, interface, dependency, package, or business knowledge record.
The current consumer is the owner's request to explain the evolved Workbench concept.

Validation covers XML structure, unique identifiers, connector references, page bounds, text fit, source links, and preview parity.
All four rendered previews received visual inspection.
Independent source reviews checked the lifecycle and architecture claims.
The drawing was not opened in the diagrams.net application during validation.
No runtime tests or wheel build apply to this documentation change.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - XML and preview checks do not replace a diagrams.net application compatibility test.
```
