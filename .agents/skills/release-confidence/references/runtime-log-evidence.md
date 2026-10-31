# Runtime log evidence for release confidence

Treat runtime log evidence as a key release-confidence metric alongside assertions, execution results, and deployment evidence.
Use this procedure for essential logic paths during E2E tests and representative usage.
The metric measures evidence collection and analysis. Report behavioral success and failures separately.

## Environment and source boundary

During UAT, collect logs from the application's remote log systems for the actual UAT deployment.
Local application files and developer console captures support local development only. They cannot satisfy remote UAT evidence.
A local export can retain remote evidence when its original remote query and deployment bindings remain inspectable.
Record its remote source identity, query, original time window, collection time, and export hash.
Record `source_kind: remote_log_system` for UAT evidence and `source_kind: local_development` for local runs.
Use null when the source is unavailable. A remote export retains its remote source classification.
Browser traces and screenshots can corroborate remote logs. They cannot replace required remote collection.

Use existing registered connectors and granted operations under the [connector guide](../../../../docs/CONNECTORS.md).
Inspect tool schemas before calls. Keep credentials outside catalogs, arguments, and evidence.
Unknown access or unavailable remote logs create an evidence gap. They do not establish an application defect.
Record the owner, blocked conclusion, and collection action. Mark an unavailable owner `unknown`.

## Declare essential observations

Select essential paths from approved behavior, changed logic, affected consumers, and consequential unchanged boundaries.
Inspect existing instrumentation before adding events. Changes to application logging follow the owning repository's instructions and authorization.
Declare the inventory before execution or counting. Record inclusions, exclusions, criticality sources, and unresolved scope.

Use one stable row for each required observation.
Identify its behavior, path, case or workload, predicate, and observation mode.
The observation mode distinguishes E2E tests from representative usage. Count each required combination once.
Define the workload, actors, data, concurrency, background work, and lifecycle timing from the actual change.
Use sourced timing limits and observation windows. Do not invent universal durations, workload thresholds, or retry limits.

Each row needs these links and values:

- Approved behavior version, path identity, expected decisions or state transitions, and independent outcome assertions.
- Candidate artifact, configuration, environment, run, case or workload, and original observation window.
- Relevant services, expected event boundaries, correlation identifiers, and existing log source.
- Expected failures, allowed side effects, completion criteria, and applicable collection limits.

Event presence alone cannot establish correct persistence, successful renewal, or absence of additional side effects.
Link independent response, state, or downstream outcome assertions where those claims require them.

## Collect and bind

Retain source queries, filters, time zones, pagination, truncation, sampling, clock differences, and known dropped-event indicators.
Wait for required asynchronous outcomes and collector delivery within the sourced observation boundary.
If delivery completeness remains unknown, preserve that limit. Do not treat absent events as proof of absent behavior.
Identify unexercised paths separately from missing instrumentation or collection loss.
Check that emitted fields identify the intended operation and support the required request or trace correlation.
An event name shared across operations cannot qualify a specific path without that binding.
Record missing correlation separately from canceled or unexercised delivery. A later run needs both adequate instrumentation and actual path execution.

Bind retained log bytes to the actual artifact, effective configuration, environment, run, observation row, and correlation chain.
A source commit alone cannot identify deployed bytes. Record unknown provenance instead of reconstructing it later.
Retain safe state summaries and reason codes. Exclude credentials and raw tokens; disclose redaction limits.
Save each completed case under its [task evidence checkpoints](../../../../tasks/README.md#save-case-evidence-and-resume-checkpoints).

## Analyze expectations and unexplained signals

Check each expected predicate against inspected assertions, correlated events, and independent outcomes.
Inspect unexpected exceptions, retries, repeated calls, fallbacks, stalled work, state conflicts, and extra side effects when relevant.
Record the search scope and its limits. An empty error search cannot establish passing behavior.

Compare equivalent baseline and candidate observations before claiming a regression.
Classify observed anomalies as introduced, worsened, unchanged, corrected, or unexplained, using matching evidence.
Keep inference separate when baseline execution or comparable instrumentation is unavailable.
AI grouping can identify investigation leads. Corroborating evidence must support defect and consequence claims.

For each anomaly, retain evidence, concrete consequence, owner, next action, and verification status.
Apply the project's user-impact priority. Keep minimal or unproved disruptive impact separate from demonstrated blockers.
Do not hide failed predicates, contradictions, or unresolved anomalies behind a successful collection metric.

## Report explicit denominators

Let `R` be the declared required observation rows for the named environment and candidate.
For UAT, qualifying acquisition requires remote-origin evidence. Report local pilot counts separately.
An unknown inventory or zero denominator produces `N/A`, with its reason. It cannot produce `100%`.

| Metric | Numerator | Denominator |
| --- | --- | --- |
| Definition support | Required rows with sourced expected predicates, path definitions, and inspected outcome assertions. | `R` |
| Log acquisition | Required rows exercised with retained logs and adequate collection evidence for their stated claims. | `R` |
| Candidate and run binding | Required rows with logs bound to artifact, configuration, environment, window, run, and relevant correlation chain. | `R` |
| Analysis completion | Required rows with expected-predicate checks and anomaly review recorded. | `R` |
| Runtime log evidence assessed | Required rows meeting definition, acquisition, binding, and analysis conditions together. | `R` |
| Matching passing runtime behavior | Required rows with all expected predicates passing and corroborating outcome evidence. | `R` |

Show `Runtime log evidence assessed: N/R` as the key metric in the decision view.
Retain the other fractions, observation inventory, partial predicates, and anomaly register in supporting detail.
Also report unique essential paths and their observation modes. Row counts are not source branch or line coverage.
Do not calculate the intersection numerator from separate totals. Inspect which individual rows satisfy all conditions.
An assessed row can contain a demonstrated failure. Full evidence assessment does not imply fully passing behavior.
Analysis completion requires recorded review, not closure of every detected defect. Keep unresolved dispositions explicit.

## Score and release disposition

Use one independent `Runtime log evidence` row in the [release scorecard](decision-model.md#confidence-score-and-release-status).
Score evidence strength using the existing `0–5` definitions. Keep coverage fractions and behavior outcomes beside that score.
A fully evidenced failure can score `5` while its condition status remains `FAILED`.
Do not average this dimension with passing test counts or convert it into a production success probability.

Required remote UAT collection and analysis must be supported before this dimension can support UAT release confidence.
Local evidence leaves that UAT requirement unresolved, even when the local behavior assertions pass.
Use `UNKNOWN` or `LIMITED` for missing or incomplete evidence, with its material consequence and next action.
Keep `can_go: false` while required UAT evidence remains unsupported. Apply the existing release-status precedence.
A log anomaly becomes a release failure only when evidence establishes an unmet condition or material consequence.
Retain independent mandatory conditions, including the [unit-test condition](decision-model.md#mandatory-unit-test-condition).

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
