# Test execution planning and preflight

Planning resolves an existing runner command without executing its suite.
Preflight checks declared setup before a long run.
Both operations keep setup status separate from business verification.

## Select an existing runner

Use a registered `testing.command` or `testing.robot` resource.
Use `playwright` for existing `e2e:test`, `e2e:remote`, or `e2e:ai` npm scripts.
Named environments apply only to `e2e:remote`.
Source checkouts include profile selection and authentication setup in `e2e/README.md`.
Generated workspaces require a separately configured test runner.

```sh
ai-sdlc --workspace PATH test plan --runner registered --resource RESOURCE_ID --suite SUITE
ai-sdlc --workspace PATH test preflight --runner playwright --suite e2e:test
ai-sdlc --workspace PATH test preflight --runner playwright --suite e2e:remote \
  --environment nonprod --environments-file .workbench/e2e-environments.json \
  --checks .workbench/preflight-checks.json --probe-services
```

The plan records the exact command, working directory, output directory, and selected source hashes.
It also records environment overrides required by that command.
A `null` override means remove that variable before invocation.
Planning creates no runner output directory and contacts no target service.

These commands inspect setup. Run the existing runner separately after reviewing the result.
A registered run grant remains required for registered suites.
Preflight rejects changed resource declarations and changed configuration bindings.

## Declare additional prerequisites

Use a local JSON checks file for package versions, browser paths, services, and served assets.
Authentication checks inspect file presence and size only.
They do not read credential values or establish session validity.
URLs must use HTTP(S) without embedded credentials.
Reports omit URL query values.

Preflight reloads private request URLs only after it validates the checks file's recorded hash.
Automatic package checks remain active when that file omits package declarations.

```json
{
  "schema_version": 1,
  "packages": [{"path": "node_modules/@playwright/test/package.json", "version": "1.64.1"}],
  "browser_executable": "adapters/browser/.browsers/selected-browser",
  "authentication_state": ".workbench/auth/nonprod.json",
  "services": [{"id": "portal", "url": "http://127.0.0.1:8128/"}],
  "served_assets": [{
    "id": "root-config",
    "url": "http://127.0.0.1:8128/config.js",
    "artifact_path": "build/config.js",
    "source_manifest": "build/source-manifest.json",
    "source_manifest_sha256": "REPLACE_WITH_64_LOWERCASE_HEX_CHARACTERS"
  }]
}
```

Each prerequisite list supports at most 32 entries.
Package versions must match declared exact versions when supplied.
Robot checks inspect installation metadata in the selected Python environment.
Browser checks inspect prepared assets without downloading or launching a browser.

Service checks require explicit `--probe-services`.
They use GET requests with a three-second timeout and refuse redirects.
Service responses have a one-MiB limit. Served assets have a 16-MiB limit.
Response bodies are not retained.
Select readiness URLs whose GET behavior fits the authorized environment.

## Bind actual served bytes

A source manifest binds local source files and built artifacts through SHA-256 values.
The checks file binds that manifest through its own SHA-256 value.
Relative manifest paths resolve from the selected workspace root.

```json
{
  "schema_version": 1,
  "sources": [{"path": "src/root.ts", "sha256": "SOURCE_SHA256", "revision": null}],
  "artifacts": [{"path": "build/config.js", "sha256": "ARTIFACT_SHA256"}]
}
```

Replace placeholders with lowercase SHA-256 values.
Revision labels can contain complete Git object IDs or `null`.
Preflight checks current source and artifact bytes before requesting the served asset.
It does not authenticate the build process or attest Git history.

| Result | Meaning |
| --- | --- |
| `MATCHED` | Every declared served asset matches its bound local artifact. |
| `MISMATCH` | At least one served asset contains different bytes. |
| `UNKNOWN` | A target lacks supported fingerprints, a binding fails, or an asset remains unavailable. |
| `NOT_APPLICABLE` | No target, service, or served artifact requires identity inspection. |

`INVALID_BINDING` identifies failed local evidence bindings.
`UNAVAILABLE` identifies failed asset requests.
Neither status proves a business defect.
A reachable service without a fingerprint retains unknown build identity.

## Interpret setup status

`READY` means all declared prerequisite checks passed within their stated limits.
`INCOMPLETE` retains failed, unknown, and unprobed checks with specific next actions.
Both results retain `suite_executed: false` and `product_behavior: NOT_EXECUTED`.
Prerequisite checks do not prove authenticated access, business behavior, or production parity.

Python callers use `plan_test_execution()` and `preflight_test_execution()` from `ai_sdlc_workbench.test_preflight`.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
