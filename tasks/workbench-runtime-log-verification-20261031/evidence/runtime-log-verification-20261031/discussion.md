# Runtime evidence for change verification

Date: 2026-10-31, Asia/Singapore.
Status: Discussion proposal. No release policy or implementation change is approved by this document.

**Proposed direction: collect and analyze essential-path runtime evidence before release, during E2E tests and representative usage.**
The user selected both observation modes. Owners must still define applicable paths, workloads, assertions, and release conditions.

## High-priority references

- [Original user input](user-input.md#exact-user-input).
- [Latest scope clarification](user-clarification.md#exact-user-answer).

## Existing rules and evidence

Sources below were inspected at Git revision `bf7c2a202dbe9eb8352686e19f8d47140fd1f4b8`.
These claims describe documented procedure. They do not establish implemented log analysis or passing application execution.

| Claim | Class | Confidence and rationale | Source | Limit |
| --- | --- | --- | --- | --- |
| Runtime observations can support verification. | Documented intent | High. The guide requires boundaries, responses, and correlations. | [System investigation](../../../tasks/README.md#investigate-the-current-system) | Authorized observations support only their recorded conditions. |
| Logs must accompany explicit behavioral evidence. | Documented intent | High. The rules require predicates, assertions, and retained execution. | [Verification procedure](../../../.agents/skills/verify-implementation/SKILL.md#bind-the-assertion-chain-to-the-result) | A success event alone cannot prove a business outcome. |
| Release conditions require sourced policy and applicable evidence. | Documented intent | High. The model separates mandatory conditions from recommendations. | [Applicable release conditions](../../../.agents/skills/release-confidence/references/decision-model.md#select-applicable-conditions) | This discussion does not create an executable gate. |

## Proposed verification flow

1. Map each changed behavior to essential paths and affected consumers.
2. Inspect existing logs, traces, and metrics before adding instrumentation.
3. Define expected decisions, transitions, side effects, and timing limits from approved intent.
4. Capture correlated events during E2E tests and bounded representative usage.
5. Check expected behavior and investigate unexplained signals.
6. Retain results, contradictions, collection limits, and release-relevant findings.

Select decision points, state changes, external calls, asynchronous boundaries, retries, fallbacks, and failures when relevant.
Record stable event names, run and correlation IDs, build identity, timestamps, reasons, outcomes, and safe state summaries.
Keep credentials and raw tokens outside retained evidence. Record redaction and sampling limits.
Use the adopting project's existing tools. Shared procedure should require no particular logging vendor, language, or hosting platform.

## Two analysis purposes

| Purpose | Example checks | Result |
| --- | --- | --- |
| Confirm expected behavior. | Valid state transitions, allowed retry counts, completion, and independently observed side effects. | A scoped assertion result with matching evidence. |
| Discover overlooked behavior. | New exception patterns, repeated calls, unexpected fallbacks, stalled work, and inconsistent outcomes. | An investigation lead until evidence establishes the cause and consequence. |

For example, a save test could confirm the displayed result and read the stored value independently.
Correlated events could then expose unexpected duplicate writes or a fallback hidden by the successful screen.
This example proposes a method. It records no observed application defect.

AI can group unusual events and propose explanations. Explicit checks and corroborating evidence must support verification claims.
An empty error search cannot prove success. Missing events can indicate unexercised paths, collection loss, sampling, or instrumentation defects.
Check collection completeness before drawing negative conclusions.

## Candidate comparison and release use

Compare baseline and candidate under equivalent workloads before calling an anomaly a regression.
Bind each run to its artifact, configuration, inputs, environment, time window, and correlation identifiers.
Distinguish existing, introduced, worsened, corrected, and unexplained observations.
Use existing sourced limits. This proposal sets no arbitrary error threshold or observation duration.
Representative usage must cover relevant actors, data, concurrency, background work, and lifecycle timing within authorized access.
Pre-release observations cannot establish unobserved production behavior.

Recommend mandatory collection and analysis for the declared essential paths, with observable completeness checks.
Keep missing evidence separate from demonstrated failure. Judge each anomaly by its concrete consequence and applicable release conditions.
Lower priority when disruptive user impact remains unproved. Retain demonstrated blockers and mandatory failed conditions.
The [unit-test release condition](../../../PRINCIPLE.md#10-delivery-requires-passing-unit-tests) remains independently applicable.

Business investigation evidence belongs under its [owning task](../../../tasks/README.md#keep-evidence-with-the-task).
Preserve logs and assertion results separately from analysis. Save each completed case before further execution or waits.

## Remaining design choices

The application, first change, workload, duration, existing telemetry, and owners are unspecified.
Select these from the first candidate's source and operational evidence before defining collection requirements.
No application was executed or instrumented during this discussion.

## Report checks

Checks passed for local links, heading anchors, whitespace, and proposal prose sentence lengths.
These documentation checks do not verify application behavior. The complete ASD writing review remains pending.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
