---
artifact_kind: test-execution-report
id: REPORT-portal-background-session-reproduction-20261019
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-portal-run001-review-6b95269bba2c54ca89
  - SRC-portal-run001-d1f015546cc4cb277d
  - SRC-portal-local-b41c647cf1c7bb26a0
  - SRC-portal-local-e9ea73b748a7c4c086
  - SRC-portal-local-a3c4f7a97404e81afb
related_ids:
  - portal-session-local-2026-10-19
  - mfe-base
  - mfe-root-config
  - single-ui-bff
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Portal background session reproduction

## Run identity and provenance

The local reproduction confirms the reported failure chain in Microsoft Edge.

The tab slept while another tab remained active.

The scheduled refresh then ran after access expiry.

The timeout control started automatic logout before the refresh response arrived.

The frontend then cleared authentication after the backend rejected the expired access token.

The returned page showed `Sign In`.

This result explains why the user had no usable manual extension.

The run does not establish production settings or the reported user's browser state.

## Facts, inferences, and unresolved questions

The test used local services only.

No DEV, UAT, STAGING, or PROD system was available.

The frontend used the source revision listed above.

The backend used the actual controller, JWT, session, and JPA paths.

Synthetic OUD, EMS2, catalog, analytics, H2, and generated process keys replaced external dependencies.

The toolkit package used a disclosed stub for two custom elements.

The stub does not reproduce toolkit appearance or behavior.

The observed chain proves the local client and controller interaction.

It does not prove production token policy, Edge fleet policy, or external identity behavior.

## Setup readiness

| Component | Local endpoint | Result | Evidence |
| --- | --- | --- | --- |
| Microsoft Edge | `155.0.4283.60`, arm64 | Installed and used | `setup/edge-runtime-settings.json` |
| Root shell | `http://localhost:8001/` | Started | `setup/local-root/start.json` |
| Instrumented MFE | `http://127.0.0.1:8002/base.js` | Webpack and TypeScript passed | `setup/instrumented-mfe/instrumentation-manifest.json` |
| Session backend | `http://127.0.0.1:8088/api/auth` | Health and smoke checks passed | `setup/local-bff/smoke-result.json` |
| Edge sleeping tabs | Sleep after 15 minutes | Enabled before the run | `setup/edge-runtime-settings.json` |

The settings were not changed for the reproduction.

The observer added no timer, polling loop, or background request.

All 342 mirrored MFE source files retain their source hashes.

## Reproduction steps

1. Start the local root, MFE, backend, and evidence collector.
2. Open the portal in Edge.
3. Sign in with the disposable local fixture.
4. Add a workspace and switch to another Edge tab.
5. Leave the portal tab inactive for more than 30 minutes.
6. Return to the portal tab without selecting an extension action.

Run 001 used a static local background page in the second tab.

Run 002 used a second portal origin and independently reproduced the same failure.

Neither run used DevTools during the inactive interval.

## Assertions and outcomes

| Event | UTC time | Evidence |
| --- | --- | --- |
| Login response | 07:51:33.352 | Access token issued with 15-minute expiry |
| Refresh target | 08:06:08.000 | Home timer scheduled 25 seconds before expiry |
| Access expiry | 08:06:33.000 | Token reached its expiry while hidden |
| Tab hidden | 07:52:00.367 | Browser lifecycle event |
| Tab frozen | 07:55:25.884 | Browser lifecycle event |
| Tab resumed | 08:23:06.318 | Browser lifecycle event |
| Refresh callback | 08:23:06.349 | 1,018,349 milliseconds after target |
| Refresh request | 08:23:06.352 | Sent with expired access and no refresh state |
| Timeout mount | 08:23:06.398 | `refreshPresent=false` |
| Automatic logout branch | 08:23:06.398 | Missing refresh caused immediate logout |
| Logout state | 08:23:06.420 | `isOnLogout=true` |
| Backend refresh response | 08:23:06.477 | HTTP 401, `TOKEN_INVALID_EXPIRED` |
| Authentication clear | 08:23:06.478 | Access and refresh state became absent |
| Logout request | 08:23:07.401 | Sent after state clear |
| Returned page | After logout | Accessibility tree showed `Sign In` |

The retained browser export contains 28 events and no raw token values.

The retained backend record matches the browser 401 and logout request.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Edge froze the hidden tab until 16 minutes after access expiry. | A normal expiry timer could not refresh before expiry. | unknown | Review browser sleeping policy and lifecycle handling. |
| Home schedules refresh at access expiry minus 25 seconds. | The scheduled callback ran 1,018,349 milliseconds late. | unknown | Refresh on resume before using the expired access token. |
| Login returned only `Single-UI-Authorization`. | `refreshToken` remained absent before the first refresh response. | unknown | Define whether login must issue a refresh token. |
| Timeout checks refresh state once on mount. | The missing-refresh branch called logout immediately. | unknown | Wait for an in-flight refresh result before selecting logout. |
| BFF validates access expiry before issuing a refresh token. | The late refresh returned HTTP 401 `TOKEN_INVALID_EXPIRED`. | unknown | Permit a valid refresh path when policy allows it. |
| Error handling clears state on `TOKEN_INVALID_EXPIRED`. | The next visible page showed `Sign In`. | unknown | Preserve a recoverable session state or present a usable recovery action. |

The automatic branch sets loading before the buttons render as disabled.

The event stream contains no Extend action.

The evidence cannot exclude a very brief click before the disabled state rendered.

## Sources

| Source | Revision and location | Inspected behavior |
| --- | --- | --- |
| MFE Home controller | `src/pages/Home/common/useController.ts:87-100` | Schedules refresh 25 seconds before access expiry. |
| MFE Timeout controller | `src/components/Timeout/common/useController.ts:25-41` | Missing refresh calls logout during the mount effect. |
| MFE service | `src/hooks/service/index.ts:27-43` | Refresh request sends the current access token. |
| MFE success handler | `src/hooks/service/util/succes.response.handler.ts:25-41` | Refresh state is stored only after a refresh response header. |
| MFE error handler | `src/hooks/service/util/error.response.handler.ts:29-31` | `TOKEN_INVALID_EXPIRED` clears authentication. |
| MFE reducer | `src/hooks/reducer/root0.reducers.ts:6-10,36-45` | Access replacement clears refresh state; clear removes all auth state. |
| BFF controller | `src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java:303-324` | Refresh validates the access token before issuing refresh state. |
| BFF JWT utility | `src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java:48-69,89-105` | Access validation checks signature, expiry, and maximum age. |

The source snapshots and hashes are retained with the run evidence.

## Recommended correction

The owning teams should make refresh lifecycle handling resume-aware.

The implementation should re-check token claims after a hidden-tab resume.

The implementation should avoid immediate logout while a refresh request is pending.

The implementation should keep a usable recovery action after a failed refresh.

The owning teams should confirm whether login must issue a refresh token.

The fix requires tests for sleeping tabs, resume timing, pending refresh, and rejected refresh.

Production validation requires approved access to the affected environment.

## Retained evidence inventory

- `knowledge/raw/execution/portal-session-local-2026-10-19/run-001/retention-map-v2.json`
- `knowledge/raw/execution/portal-session-local-2026-10-19/run-001/browser/browser-events-001.json`
- `knowledge/raw/execution/portal-session-local-2026-10-19/run-001/reviews/causal-review.json`
- `knowledge/raw/execution/portal-session-local-2026-10-19/run-001/reviews/observer-review.json`
- `knowledge/raw/execution/portal-session-local-2026-10-19/run-001/reviews/sign-in.ax.full.txt`
- `knowledge/raw/execution/portal-session-local-2026-10-19/run-001/bff/local-bff-runtime.stdout.log`
- `knowledge/raw/execution/portal-session-local-2026-10-19/run-002/browser/browser-events-001.json`
- `knowledge/raw/execution/portal-session-local-2026-10-19/run-002/browser/return.ax.full.txt`
- `knowledge/raw/execution/portal-session-local-2026-10-19/setup/edge-runtime-settings.json`
- `knowledge/raw/code/mfe-base/f025513f696476a9cc8162681410cbd21e029bcb/`
- `knowledge/raw/code/single-ui-bff/85d7cc03eb12710d6facf581987fd4ae24fc9844/`

## Verification conclusion

The browser observer review passed its automated evidence checks.

The source hash checks passed for the instrumented MFE.

The local backend smoke assertions passed.

The Workbench workspace validation passed with 13 documents.

The report lint passed with four review warnings.

The virtual environment test run passed 478 tests and hit one sandbox socket error.

The virtual environment wheel build passed without build isolation.

The prescribed system test run cannot import PyYAML in this environment.

The prescribed isolated wheel build cannot download build dependencies through the restricted proxy.

The report writing review remains pending.

The report does not claim production behavior verification.
