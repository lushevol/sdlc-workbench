---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Writing checks, source review, and business execution have separate results.
---

# Authentication investigation and session pilot

The investigation produced a code-backed authentication baseline and an isolated frontend session-renewal pilot.
The ingestion skill now requires implementation traces, assertion inspection, and final source-hash matching.
Knowledge publication, human review, and business environment execution remain pending.

## Scope and evidence

The [classified index](../../knowledge/candidates/index.md) connects historical documents, implementation evidence, requirements, and unresolved findings.
The [architecture baseline](../../knowledge/candidates/architecture/ARCH-authentication-runtime-baseline.md) describes features, branches, interfaces, failures, and external limits.
The [renewal requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md) records seven measurable Gherkin scenarios.
The [revocation finding](../../knowledge/findings/GF-refresh-revocation-scope.md) retains an unresolved security boundary.

| Repository | Inspected initial revision |
| --- | --- |
| `single-ui-bff` | `091c9d16c13f285a78463ff0235c21b152844b61` |
| `mfe-base` | `99b4eda666bedf06574bc48766e4efdb339f4cc7` |
| `mfe-root-config` | `83091d85beff5306ca0cd643955d8ea6ed0a2d93` |
| `single-ui-auth-sdk` | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3` |
| `ratan-test-engine` | `432f898f59fb06414bc14152d6e463a6a1f4eac2` |

Later BFF and frontend commits added onboarding documents during inspection.
Inspected implementation bytes still match the initial revisions.
The pilot starts from frontend revision `dddb76c8e8ba8ea66bb941feaad562740fdb8346`, which includes those documents.
Exact source captures remain in the [raw manifest](../../knowledge/raw/manifest.yaml).
The 102 original Markdown files retain their original bytes.

The Workbench change has low execution risk because it changes knowledge and procedure files.
The frontend pilot has moderate risk because activity can increase renewal requests.
The pilot also propagates relogin request failures to callers.
Known callers and affected interfaces were inspected before implementation.
Unknown external consumers require separate review.

## Feature findings

The following facts apply to inspected source revisions.
They do not establish effective deployment configuration or observed production behavior.
The architecture baseline contains their exact source citations.

| Feature | Implemented behavior | Consequence and limit |
| --- | --- | --- |
| Provider selection | The frontend parses `true`, `1`, `yes`, and `y` as enabled values. | Parsing resolves the documentary conflict; deployed flag policy remains unknown. |
| Authentication routing | Callback inputs select OneMFA or Entra exchange paths. Blank code can select OUD. | Provider trust and deployed gateway controls need separate evidence. |
| Token lifetimes | Retained defaults specify 15-minute access, 225-minute refresh, and 60-minute absolute markers. | Refresh generation adds 24 seconds. Defaults do not prove deployed values. |
| Absolute marker | Validation, selected extension branches, and relogin can reset time claims. | Source does not establish a fixed maximum measured from initial login. |
| Activity renewal | Original Home code debounces mouse movement for five seconds after activity stops. | Continuous movement can postpone renewal. Keyboard and scroll lack equivalent bindings. |
| Idle renewal | The timeout prompt uses the existing refresh token. | The original helper returns before its request completes. |
| Logout | The BFF stores excluded session IDs. The SDK uses a filter-local exclusion list. | Global revocation and persistence lifetime remain unconfirmed. |
| SDK permissions | The filter validates identity and exposes claims. | Downstream code must establish action-level permission enforcement. |
| Existing tests | Assertions use mocked collaborators or limited UI outcomes. | They do not establish full renewal, revocation, or downstream authorization behavior. |

The user selected indefinite renewal during eligible mouse, keyboard, and scroll activity.
The user also retained refresh-token renewal after inactivity.
These replies establish requested intent, without approving the complete drafted requirement or deployment.

## Isolated frontend pilot

Repository: `mfe-base`.
Branch: `codex/session-renewal-pilot`.
Commit: `4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8`.

The pilot changes four runtime/UI files and five regression files.
Document capture listeners observe `mousemove`, `mousedown`, `keydown`, and `scroll`.
All activity types share one five-second leading throttle.
The handler reads current session state and creates no idle renewal loop.
Existing near-expiry and logout guards remain active.

The relogin helper now returns its request promise.
The timeout prompt closes after successful completion.
A rejected request keeps the prompt open and permits retry.
The refresh-expiry logout deadline remains active after failure.
The branch remains separate from the main checkout and deployment.

| Criteria | Local evidence | Remaining limit |
| --- | --- | --- |
| AC-1 to AC-3 | Each activity type and continuous movement reach the renewal call path. | Exact service/browser fixtures and successful backend renewal remain unverified. |
| AC-4 | Source review identifies resettable timing claims. | Four-hour service/browser execution remains unverified. No finite test proves infinity. |
| AC-5 to AC-7 | Controlled checks cover pending, success, rejection, retry, and retained logout timing. | React, browser, and backend behavior remain unverified. |

Cross-origin frame activity does not reach portal document listeners.
That integration requires separate evidence and scope.
No backend timeout or configuration changed.

## Checks and retained results

| Check | Actual result | Evidence limit |
| --- | --- | --- |
| Workbench workspace validation | `VALID`: 12 governed documents; zero findings. | Checks structure, source declarations, and recorded gates. |
| Raw evidence and local links | `PASSED`: 322 snapshots, 195 code captures, and 235 local links. | Hashes and pointers do not establish semantic truth. |
| Workbench scoped suite | `PASSED`: 81 tests. | Covers runtime, catalogs, interfaces, providers, knowledge governance, and workspace layout. |
| Workbench full suite | `FAILED`: 281 passed; one graph viewer test failed. | The failure occurs in concurrent graph changes outside this stage. |
| Wheel build and isolated initialization | `PASSED`. | Uses installed build dependencies and copied PyYAML without network access. |
| Generated workspace | `VALID`; five required resources present; skill bytes match. | Contains no live authentication records or runtime source. |
| Feature parser characterization | `PASSED`: 19 cases. | Actual parser uses controlled environment and browser inputs. |
| Original movement characterization | 1,000 events produced zero calls until a five-second pause. | Controlled clock and source function; no browser execution. |
| Committed pilot characterization | `PASSED`: 12 checks; all five executed hashes match the commit. | Transformed TypeScript uses controlled hooks, events, clocks, and network promises. |
| Continuous pilot movement | 1,000 events produced 200 renewal calls over 1,000 seconds. | Request counts do not establish successful backend renewal. |
| TypeScript transformation | `PASSED`: eight files. | Does not type-check dependencies or execute Jest. |
| Pilot whitespace | `PASSED` with CRLF-aware Git settings. | Two existing fixtures preserve their original CRLF endings. |
| Ingestion skill validator | `PASSED`. | Checks skill structure. |
| Independent ingestion exercise | `PASS_WITH_EVIDENCE_LIMITS`. | Uses seven supplied files, five retrieval questions, and one requirement probe. |
| Independent baseline source review | `PASSED`: 82 sources and 114 links. | Reviews initial source behavior; excludes policy approval and deployment. |
| Jest regressions | `NOT_RUN`: runner absent. | Saved assertions require execution in a provisioned checkout. |
| BFF execution | `NOT_RUN`: Java and the private starter artifact unavailable. | No Maven lifecycle or external system was invoked. |
| Browser/backend and four-hour scenario | `NOT_RUN` / `NOT_VERIFIED`. | Requires the supported business environment. |

The full-suite failure is `GraphViewerRendererTests.test_repository_inventory_full_labels_semantic_routes_and_api_trace`.
Its fixture expects `edge:fixture:inject` and `edge:fixture:type`, which the generated edge set omits.
Owner: unknown; concurrent graph work owns the affected files.
Consequence: the complete Workbench suite is not green.
Next action: resolve that fixture or graph behavior within its owning stage, then rerun the full suite.

An earlier retained pilot result used a pre-final Timeout source hash.
That result remains preserved as investigation history.
A new execution against committed bytes passed all 12 checks.
The requirement now cites the matching result.
An initial rerun without the required VM flag failed during harness setup.
The command below supplies that flag.

```sh
node --experimental-vm-modules /private/tmp/run-mfe-session-pilot-characterization.cjs PILOT_WORKTREE OUTPUT_JSON
PYTHONPATH=tests .venv/bin/python -m unittest test_catalogs test_core test_interfaces test_knowledge_governance test_providers test_workspace_layout test_workspace_v2 -v
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist
ai-sdlc --workspace PATH validate
```

The Node command uses the [retained harness](../../knowledge/raw/execution/session-renewal-pilot-2026-10-15/run-mfe-session-pilot-characterization.cjs).
Replace placeholders with the isolated worktree and a new result path.
The Python commands run from the standalone source checkout.

Retained evidence:

- [Committed pilot execution](../../knowledge/raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json).
- [Scoped suite log](../../knowledge/raw/execution/authentication-stage-2026-10-16/auth-scoped-tests.log).
- [Full suite log](../../knowledge/raw/execution/authentication-stage-2026-10-16/auth-full-tests.log).
- [Installed wheel check](../../knowledge/raw/execution/authentication-stage-2026-10-16/auth-wheel-check-final.json).
- [Independent ingestion exercise](../../knowledge/raw/execution/authentication-stage-2026-10-16/code-ingest-forward-result.json).
- [Initial review findings](../../knowledge/raw/execution/authentication-stage-2026-10-16/auth-baseline-peer-review.json).
- [Resolved source review](../../knowledge/raw/execution/authentication-stage-2026-10-16/auth-baseline-peer-review-complete.json).

## Procedure changes and next actions

The [ingestion skill](../../.agents/skills/ingest-knowledge/SKILL.md) requires caller-to-provider traces and explicit configuration limits.
It requires test assertion inspection and final source-hash matching before result reuse.
It separates documentary intent, implemented behavior, inference, and unresolved questions.
Unavailable environments limit execution but allow code-backed baselines and requirement drafts.

The architecture and two updated topics remain investigated drafts.
The renewal requirement and revocation finding remain candidate drafts.
All records keep empty verification lists and unknown business owners.
New audit events record this stage without changing previous event files.

| Open item | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Requirement review | The draft cannot establish publication approval. | unknown | Review all seven scenarios and record the authorized reviewer. |
| Runtime coverage | Controlled checks cannot establish end-to-end renewal. | unknown | Execute Jest and the browser/backend scenarios on the supported PC. |
| Logout revocation | Refresh credentials may outlive an exclusion entry under the retained cleanup definition. | unknown | Confirm deployed cleanup and revocation requirements; test controlled token reuse. |
| Renewal load | Active input can request renewal every five seconds per mounted portal. | unknown | Measure accepted request load before deployment. |
| Embedded activity | Cross-origin input cannot renew through these document listeners. | unknown | Identify required embedded contexts and their integration owner. |

The revocation consequence is conditional on deployment and additional controls.
It is not an observed production defect.
Human review, ASD writing review, and business execution remain separate gates.
