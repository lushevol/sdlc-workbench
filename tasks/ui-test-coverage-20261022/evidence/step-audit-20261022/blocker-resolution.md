---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Resolve blocked UI cases

> **Critical conclusion: Build missing automation and fixtures.**
> Action: Execute the batches below. Consequence: Missing bindings currently prevent execution. Owner: Codex for harness work.
> Evidence: [455 case plans](blocker-resolution.json) and [prior results](../audit-run-20261022/report-001/case-results.json).
> **Business acceptance still requires current service and policy evidence.**
> Action: Resolve service, tenant, and historical POC dependencies. Consequence: Fixture passes cannot establish those boundaries. Owner: unknown.

The prior report blocked 455 cases. Missing automation does not prove an unavailable environment.
Controlled responses and containers are permitted by the [canonical fixture rules](../../test-cases.md#ui-fixture-extension).
Each JSON record retains its definition hash, source locators, actions, dependencies, and screenshot step lines.
This plan records no execution. It preserves canonical definitions and prior results.

## Execution batches

| Batch | Cases | Action | Owner |
| --- | --- | --- | --- |
| A: Controlled authentication and session probes | 93 | Bind actual MFE login, response handlers, session services, clock, visibility, and storage observations. | Codex harness maintainer |
| B: Shell, catalog, modules, and profile | 53 | Build the declared SystemJS test container. Bind real shell controls and exact drawer response shapes. | Codex harness maintainer |
| C: Frontend administration and source-risk probes | 84 | Extend Category, Import Map, and Tile POMs. Provide stateful complete response fixtures and independent reload observations. | Codex harness maintainer |
| D: UI quality and compatibility probes | 72 | Bind real controls, browser keyboard and viewport operations, fixture data, and measured DOM observations. | Codex harness maintainer |
| E: Domain policy and tenant integration | 34 | Define a versioned synthetic tenant contract. Bind actual shell integration separately from simulated tenant behavior. | unknown |
| F: Versioned cache fixture | 12 | Build V1/V2 fixture entries, chunks, CSS, images, headers, and lazy-panel control. Retain requested assets and hashes. | Codex harness maintainer |
| G: Current BFF and persistence boundary | 101 | Build current BFF revision with disposable database, signed test credentials, fault injection, and independent readback. | unknown |
| H: Conditional OpenFin POC | 6 | Select the historical POC build and supported native runtime. Bind its publisher controls and exact channel contract. | unknown |

## Boundaries requiring attention

The prepared BFF differs from the selected current revision.
Build the current BFF before claiming server validation, authorization, storage, or audit outcomes.
Evidence: [readiness](../audit-run-20261022/environment/readiness.json). Owner: unknown.

Suspension cases declare controlled clocks. A timer suspension adapter can run those probes.
Keep real device sleep and natural browser suspension unverified. Owner: Codex.

Current MFE listens to `scb.ViewLaunch`. The historical POC requires `fmchannel` contracts.
Select a matching POC before executing its six cases. Owner: unknown.
Evidence: [current listener](../../../../repos/ui/mfe-base/src/pages/Home/common/useOpenfin.ts#L15).

Policy conflicts affect acceptance. They do not prevent measuring the current UI as a proposed probe.
Keep each observed result separate from approved intent. Owner: unknown.
Evidence: [open decisions](../knowledge-inspection.md#open-rule-decisions).

## Quality binding overlays

There are 66 failing rules across 28 cases. The JSON records candidate targets for each case.
Source A already names the fixture action `Send trade context`.
Other tenant controls require an explicit fixture contract. No product tenant control is inferred.
Inspect rendered uniqueness before using any candidate target.

| Case | Candidate target | Required work |
| --- | --- | --- |
| [AUTH-144](../../test-cases.md#auth-144) | button `Create` in Category dialog titled new ID: 101 | `PROPOSED_BINDING_REQUIRES_CURRENT_BFF` |
| [KNOW-015](../../test-cases.md#know-015) | portal navigation `T-REPORT controlled deep link` in Actual portal browser page | `PROPOSED_NAVIGATION_OVERLAY; original When requires formal binding review` |
| [KNOW-017](../../test-cases.md#know-017) | portal navigation `T-REPORT controlled deep link` in Actual portal browser page | `PROPOSED_NAVIGATION_OVERLAY; original When requires formal binding review` |
| [KNOW-011](../../test-cases.md#know-011) | button `Load trade` in Controlled T-TRADE or T-REPORT fixture region | `NEW_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-012](../../test-cases.md#know-012) | button `Edit trade` in Controlled T-TRADE fixture region | `NEW_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-016](../../test-cases.md#know-016) | button `Load report` in Controlled T-TRADE or T-REPORT fixture region | `NEW_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-018](../../test-cases.md#know-018) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-019](../../test-cases.md#know-019) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-020](../../test-cases.md#know-020) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-021](../../test-cases.md#know-021) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-022](../../test-cases.md#know-022) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-023](../../test-cases.md#know-023) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-024](../../test-cases.md#know-024) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-025](../../test-cases.md#know-025) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-026](../../test-cases.md#know-026) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-027](../../test-cases.md#know-027) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-028](../../test-cases.md#know-028) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-029](../../test-cases.md#know-029) | button `Run provider action` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-031](../../test-cases.md#know-031) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-032](../../test-cases.md#know-032) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-040](../../test-cases.md#know-040) | button `Send trade context` in Controlled Source A tenant region | `NEW_VERSIONED_FIXTURE_CONTRACT_REQUIRED` |
| [KNOW-033](../../test-cases.md#know-033) | button `Publish POC request` in Selected historical POC publisher region | `SELECT_REAL_POC_FIRST` |
| [KNOW-034](../../test-cases.md#know-034) | button `Publish POC request` in Selected historical POC publisher region | `SELECT_REAL_POC_FIRST` |
| [KNOW-035](../../test-cases.md#know-035) | button `Publish POC request` in Selected historical POC publisher region | `SELECT_REAL_POC_FIRST` |
| [KNOW-036](../../test-cases.md#know-036) | button `Publish POC request` in Selected historical POC publisher region | `SELECT_REAL_POC_FIRST` |
| [KNOW-037](../../test-cases.md#know-037) | button `Publish POC request` in Selected historical POC publisher region | `SELECT_REAL_POC_FIRST` |
| [KNOW-038](../../test-cases.md#know-038) | button `Publish POC request` in Selected historical POC publisher region | `SELECT_REAL_POC_FIRST` |
| [KNOW-049](../../test-cases.md#know-049) | button `Open lazy search` in Controlled T-CACHE fixture region | `NEW_FIXTURE_CONTRACT_REQUIRED` |

## Screenshot evidence

Capture a fresh screenshot after each executed Given, When, Then, And, and But step.
Keep the canonical step number, source line, timestamp, hash, outcome, and frame path together.
Record request, storage, clock, and persistence predicates separately. Screenshots cannot prove those predicates.
If a step fails, save its frame immediately. Mark later steps as not executed.
Preserve failed attempts. Show the latest attempt separately from historical attempts.

## Validation

The plan includes exactly 455 distinct blocked IDs. Every ID exists in the canonical catalog.
All 28 quality failures have candidate overlays. The overlays preserve the canonical definition hash.
ASD review remains pending.
