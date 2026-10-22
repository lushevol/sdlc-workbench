# Local audit environment

**Action: Treat these results as controlled local UI observations. Business acceptance remains blocked. Owner: Test owner, identity unknown.**

The prepared BFF differs from the registered BFF revision. This difference limits backend and policy conclusions.
See the [revision comparison](bff-revision-delta.json) and [readiness record](readiness.json).

The user selected the isolated local application environment.
The root agent owns supervisor session `67431` and its shutdown.
Do not stop servers from other tasks.

## Scope and source identity

The running shell uses actual React application source with local build wrappers.
All 223 implementation files match the registered MFE source bytes.
Two test files differ. See the [complete source comparison](mfe-source-comparison.json).

The registered MFE revision is `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
The registered BFF revision is `834b4155232222347220e47139a502ee43a9cbdf`.
The prepared BFF revision is `85d7cc03eb12710d6facf581987fd4ae24fc9844`.
The [build manifest](bff-source-build-manifest.json.snapshot) records selected source and class hashes.
It states `production_runtime_equivalence: NOT_ESTABLISHED`.

The BFF uses synthetic identity, catalog, entitlements, and an H2 database.
Its catalog returns empty drawers. Business admin APIs are unavailable.
The local timeout profile uses shortened token durations.
This environment cannot establish production session policy or complete backend acceptance.

Browser routes may supply controlled login responses and workspace data.
Each case records those fixture limits separately.
Such cases test the actual MFE rendering and interaction under those responses.
They do not test server authorization or persistence.

## Launch evidence

The [first attempt](attempt-01-sandbox-bind-failure/stack-lifecycle.json) failed because the sandbox denied local server sockets.
The [failure log metadata](attempt-01-sandbox-bind-failure/log-metadata.json) retains raw log hashes and the classified error.
No UI case ran in that attempt.

The second attempt used the [retained configuration](attempt-02/stack-config.json.snapshot).
All five readiness URLs returned HTTP `200`.
The [lifecycle record](attempt-02/stack-lifecycle.json) retains ports, process identifiers, timestamps, configuration hashes, and readiness observations.
The root agent owns its supervisor session.
Its graceful shutdown also retains sanitized compile metadata and raw log hashes.

The login URL is `http://localhost:8128/?show_normal_login=Y`.
The UI test prefix is `MicroWebUI_base`.
The stack uses ports `8122`, `8124`, `8125`, `8128`, and `8129`.
The launcher checks exclusive port availability before starting services.
It stops only the process groups that it created.

The launcher installs no dependencies and downloads no browsers.
Raw logs remain in the ignored runtime directory.
Retained service metadata excludes credentials, token values, request headers, and response bodies.
Screenshots establish visible states only. Case assertions establish the specific observed UI results.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
