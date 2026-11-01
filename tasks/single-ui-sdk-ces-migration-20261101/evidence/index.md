# SDK CES migration evidence

> **Resolve the SDK contract and artifact line before product implementation.**
> Action: complete the [living questions](../01-intake.md#answer-and-question-log).
> Consequence: permission mapping and consumer compatibility remain unresolved.
> Owner: unknown. Evidence: [current assessment](../01-intake.md).

The [current assessment](../01-intake.md) contains the update sequence and three coverage matrices.
No application code, Java build, live CES call, or business case execution forms part of this assessment.
The [confidence follow-up](user-followup-confidence.md) requests the assessment below.

## Implementation confidence

Confidence assessment: Codex, 1 November 2026. SDK source remains clean at `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`.
Confidence levels follow the [evidence rubric](../../../tasks/README.md#investigate-before-asking). They are not measured probabilities.

| Claim | Evidence class | Confidence and rationale | Supporting source | Material limit |
| --- | --- | --- | --- | --- |
| C1: The CES client, DTOs, configuration, and token-provider interface can be implemented. | Inference from inspected implementation. | HIGH; endpoint, response shape, authentication, and affected symbols are known. | [SDK scope](sdk-scope.md#concrete-edit-map) and [CES transport](ces-reference.md#transport-and-authentication). | No candidate build or execution exists. |
| C2: Complete compatibility is achievable after contract decisions resolve. | Inference from inspected implementation. | MEDIUM; merged grants cannot establish each legacy role's permissions. | [Mapping limits](ces-reference.md#mapping-references-and-their-limits). | Role-specific output remains unresolved in [SDK-Q1](../01-intake.md#sdk-q1). |
| C3: Consumer upgrade scope is incomplete. | Inspected implementation and unknown deployment scope. | HIGH for the source mismatch; deployed versions remain UNKNOWN. | [Consumer findings](consumer-scope.md#confirmed-consumers-and-compatibility). | Auth declares SDK `1.1.1`; supplied SDK declares `2.0.0-SNAPSHOT`. |
| C4: Local Java and Maven tools are available through explicit paths. | Observed tooling execution. | HIGH; both version commands returned exit code 0. | [Tooling check](tooling-check.json). | JDK 26.0.1 and Maven 3.9.16 do not prove target-runtime compatibility. |

### Decisions needed for completed behavior

1. Resolve [SDK-Q1](../01-intake.md#sdk-q1): preserve role-specific output or introduce a versioned effective-permission API.
2. Resolve [SDK-Q2](../01-intake.md#sdk-q2): identify the released artifacts and consumers that must upgrade.
3. Resolve [SDK-Q3](../01-intake.md#sdk-q3): define token provision and caller behavior for no grants and upstream failures.

The named checkout already defines a source target for a bounded patch.
Its POM declares Java 17 and Boot 4.0.6. Auth declares Java 21 and Boot 4.0.6.
Those declarations do not establish deployed runtime versions.
Evidence: [SDK POM](../../../repos/libraries/single-ui-sdk-starter/pom.xml#L10) and [Auth POM](../../../repos/services/ratan-auth-server/pom.xml#L5).
All unresolved decision owners remain unknown. Their next action is recorded beside each linked question.

### Evidence needed for validation

I can add tests for the CES client, scope isolation, JWT compatibility, and zero EMS2 requests during implementation.
The supplied SDK has no tests. Complete SDK and consumer builds, unit suites, and Spring startup remain unexecuted.
Live integration needs CES/FMAA connectivity, authorized service credentials, trust configuration, and representative allowed/denied accounts.
Permission equivalence needs reviewed mappings and comparable EMS2/CES assignments.
These are validation prerequisites. They do not prevent development against controlled mocks.

Recommendation: use effective feature/action results when actual consumers need only effective permissions.
Retain role-specific compatibility only with supported role attribution or an explicitly reviewed mapping.
Do not assign every merged permission to every returned role.
A host-provided token interface avoids copying Auth Service's Redis token lifecycle into this SDK.
No evidence requires adding a new SDK cache or retry system.

The [rename and feature consolidation](ces-reference.md#resolved-migration-meaning) are already answered.
The SDK does not require full account metadata for its current entitlement lookup.
Overall confidence in a completed compatibility migration is MEDIUM until the contract decisions resolve.
Readiness remains separate from passing execution, business review, and deployment approval.

| Evidence ID | Claim or question | Locator and retained path | Exact revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |
| SRC-USER-001 | Current investigation scope | [user-input.md](user-input.md) | 2026-11-01 message | `99c868591d697f0d499215583436abd16f0b87c95526da38b8f66dfcbe9a8fb9` | Assessment request; no detailed contract approval. |
| SRC-SDK-001 | Exact EMS2 paths and SDK edit map | [sdk-scope.md](sdk-scope.md) | SDK b0aa82005e7f14202f85f5ef583f25e42da9eeb3 | `3ce1de118a541e74a269897c82f510e6c33426c177453fa3f3ac22843fe6828a` | Source analysis; Java and business checks NOT_RUN. |
| SRC-CES-001 | CES client, authentication, and mapping limits | [ces-reference.md](ces-reference.md) | Auth dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2; BFF 134a340472f29d2a4136e07e516690de6a18e323 | `934014f5e1897af4fc393aef53ce5900c19b61e24ebf8044311a393c8861b9a5` | Source and sample evidence; no approved SDK mapping. |
| SRC-CONSUMERS-001 | Known consumers, versions, and assertions | [consumer-scope.md](consumer-scope.md) | Exact heads in consumer-sources.json | `e2257efb321f35a235bd7125ee84950a43245d3cf4067db476ea0ce33c7d01fa` | Search includes ignored checkouts. Deployment inventory remains incomplete. |
| SRC-API-001 | Static response structure and JSON pointers | [api-shape.json](api-shape.json) | 2026-11-01 inspection; original capture unknown | `d5e2579ca29af538fcd75047f55e82022e7f367b829c8d85edbb3c3890efc145` | One retained sample; no live execution. |
| SRC-FILES-001 | Exact inspected source hashes | [source-manifest.json](source-manifest.json) | 2026-11-01 inspection | `43d1980e2c9cc5ad67ed9ac14d02b1a59b1c800dedc149c9c30a72330759691f` | 66 source files; local identities only. |
| CHECK-LINT-001 | Requirement document validation | [intake-lint.json](intake-lint.json) | 2026-11-01 | `f279c0d3ed541950f084815694f0aba23f3013577412b3119b05e5099f610d92` | PASSED with four warnings; owner, review, unresolved content, and writing review remain open. |
| SRC-USER-002 | Confidence question | [user-followup-confidence.md](user-followup-confidence.md) | 2026-11-01 | `0129aa2ada4e729d73d0fb46e0b46ed5e9a957a052da9ba2a42113591bd6a727` | Question only; no missing contract answer supplied. |
| CHECK-TOOLS-001 | Local Java and Maven inventory | [tooling-check.json](tooling-check.json) | 2026-11-01 | `bde5cafe2e8555ec18d577ef3345308d287ac396ca2151948eab602ec8a5d604` | Version commands passed; no application compilation or execution. |

Additional evidence: [workspace discovery](workspace-status.json) and [consumer source manifest](consumer-sources.json).
The [original document checks](document-checks.json) record links, locators, source hashes, and final lint status.
The [follow-up checks](document-checks-confidence.json) cover this confidence assessment and current source hashes.

## Validation

Command: `.venv/bin/ai-sdlc lint tasks/single-ui-sdk-ces-migration-20261101/01-intake.md`.
Result: PASSED, exit code 0, with four warnings.
Unknown ownership, pending business review, unresolved values, and pending ASD review are retained truthfully.
No runtime source changed. Runtime unit tests and wheel builds are not applicable to this documentation stage.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Document checks do not establish business verification or publication approval.
```
