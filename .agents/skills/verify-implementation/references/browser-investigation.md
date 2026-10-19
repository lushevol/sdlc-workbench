# Investigate browser lifecycle failures

Use this procedure for defects involving inactive tabs, session expiry, browser sleep, and resume.
The portal session investigation establishes its current use.
Its source-checkout evidence is [the portal verification review](../../../../tasks/portal-background-session-20261019/verification.md).
The archived source used `docs/reviews/PORTAL_BACKGROUND_SESSION_REPRODUCTION.md` at Workbench revision `621096a`.
Generated workspaces omit that project-specific report and its raw evidence.

## Establish the experiment

Start from the issue intake created with the [defect template](../../../../knowledge/templates/sdlc/defect-report.md).
Separate reported conditions, observed conditions, suspected causes, and approved session policy.
Unknown production settings can remain open while authorized local investigation continues.

Record the following inputs before execution:

| Input | Required detail |
| --- | --- |
| Implementation | Repository IDs, exact revisions, relevant source hashes, and local changes. |
| Services | Actual components, endpoints, substituted dependencies, synthetic data, and missing external boundaries. |
| Browser | Product, version, engine, operating system, architecture, profile, launch arguments, extensions, and relevant policies. |
| Lifecycle | Active tab, tab visibility, sleep settings, machine sleep, power state, and available memory-pressure evidence. |
| Session | Known token lifetimes, refresh path, idle policy, absolute policy, and sources for each value. |
| Experiment | Actions, interval, clock source, observation method, assertions, comparison conditions, and completion evidence. |

Mark unavailable inputs unknown.
Use an isolated profile when the experiment needs controlled settings.
Keep the user's personal profile separate from test provisioning.
Inspect existing test-engine capabilities before adding another browser dependency.
Check browser launch arguments for changes to background throttling or renderer behavior.

## Preserve the behavior under investigation

Use actual elapsed time when the claim concerns real browser inactivity.
Label shortened clocks, injected expiry, and forced lifecycle transitions as controlled experiments.
Those experiments can test a branch without establishing natural browser sleep behavior.

Record whether DevTools, tracing, polling, or browser automation was attached during inactivity.
These observation methods can affect the experiment.
Do not assume an automated browser has the same lifecycle behavior as a normal user session.
Observe visibility, freeze, resume, and reload separately where the browser exposes them.
An inactive tab alone does not prove that the browser froze it.

Review instrumentation before relying on its observations.
Compare instrumented files with exact baseline bytes.
Retain every transformation and its purpose.
Check added timers, global wrappers, network calls, synchronous writes, and other work that can affect timing.
State remaining observer effects even when the source checks pass.

## Correlate the failure

Retain event sequence numbers and timestamps with their clock sources.
Record clock differences before ordering events across machines.
Calculate timer delay against the scheduled target and token expiry separately.
Record the refresh request, refresh response, state change, logout action, and returned page where applicable.
Check derived timelines against actual event order and timestamps.
Correlate browser events with service requests using available request or session identifiers.
Retain only the identifiers needed for the investigation.
Exclude credentials and raw tokens from browser evidence.

A logout screen establishes the final display state.
It does not establish the preceding request order or the server's session policy.
No recorded Extend action does not prove that clicking was impossible.
Inspect the rendering and disabled-state paths before describing the available interaction window.

## Validate comparisons and conclusions

Specify each comparison condition before execution.
Check its actual visibility, elapsed interval, lifecycle events, and service configuration afterward.
A second sleeping tab is a repeated background run.
It cannot establish the behavior of a continuously visible tab.
Keep a failed comparison and mark its intended condition unmet.

Separate the following conclusions:

| Evidence | Supported conclusion |
| --- | --- |
| Branch experiment with forced expiry | The inspected branch executed under the disclosed conditions. |
| Actual background browser and local services | The retained local failure chain occurred in that environment. |
| Matching comparison with one changed condition | The observed difference supports that comparison within its stated limits. |
| Local services with substituted external dependencies | The omitted identity, network, and production boundaries remain unverified. |
| Approved intent plus matching corrected execution | Only the asserted corrected predicates can receive a verification claim. |

Do not use a local reproduction to establish production configuration or the original user's browser state.
Keep policy decisions separate from the mechanism observed in code and execution.

## Retain the handoff

Retain source identities, setup records, transformations, launch settings, assertions, logs, and the visible outcome.
Bind each screenshot or accessibility capture to its run, capture time, origin, navigation, and scenario phase.
Mark missing capture bindings unresolved; an image's content alone cannot establish when it was captured.
Preserve original bytes and register retained sources through the existing evidence procedure.
Use relative retained paths so the handoff survives removal of temporary setup directories.
Keep failed controls and contradictory results when they affect causal confidence.
Remove superseded setup attempts under the [task retention rules](../../../../tasks/README.md#evidence-priorities-and-cleanup).

Record the exact validation command, interpreter, exit code, selected tests, and original result output.
Report total, successful, failed, errored, and skipped tests separately.
Preserve expected-failure statuses when the runner reports them.
Do not count skipped cases as successful execution.
State a missing result log beside any count taken from a conversation handoff.

Use the [shared evidence handoff](behavior-review.md#keep-one-evidence-handoff) for later fixes and regressions.
An investigation can finish with a demonstrated local mechanism and unresolved production or policy questions.
Closure still requires the applicable owner decision and corrected-behavior evidence.
