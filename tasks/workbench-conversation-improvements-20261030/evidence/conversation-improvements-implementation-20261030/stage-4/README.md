# Stage 4 verification: test planning and preflight

No critical conclusions require user attention or action.

**Seven real setup cases passed their assertions. No application suite executed during these cases.**
Owner: Workbench maintainer.
Next action: run an authorized business suite after resolving its specific setup and source prerequisites.
Source: [implementation authorization](../user-input.md).

## Results

| Case | Setup and observable result | Evidence |
| --- | --- | --- |
| PF-REAL-001 | Five prepared Session Refresh service URLs refused connections. Each receives a setup failure and action. | [Case receipt](PF-REAL-001.json) |
| PF-REAL-002 | A local HTTP fixture serves the retained frontend asset. Its source-bound SHA-256 matches. | [Case receipt](PF-REAL-002.json) |
| PF-REAL-003 | The same fixture serves altered bytes. Preflight reports a build mismatch. | [Case receipt](PF-REAL-003.json) |
| PF-REAL-004 | A reachable service has no asset fingerprint. Build identity remains unknown. | [Case receipt](PF-REAL-004.json) |
| PF-REAL-005 | The source manifest fingerprint is invalid. Preflight rejects it before any asset request. | [Case receipt](PF-REAL-005.json) |
| PF-REAL-006 | A readiness endpoint returns a redirect. Preflight refuses the redirect and reports setup failure. | [Case receipt](PF-REAL-006.json) |
| PF-REAL-007 | A readiness response exceeds one MiB. Preflight rejects it without retaining the body. | [Case receipt](PF-REAL-007.json) |

Each case saved its result before the next case started.
The [reproduction script](verify_real_cases.py) records assertions and source identities.
The [verification receipt](verification-receipt.json) records its command and request paths.
The [source manifest](retained-root-asset-source-manifest.json) binds the actual retained frontend artifact.
Its source map contains `src/root.ts` bytes identical to the inspected checkout.

## Evidence limits

The asset fixture is a controlled loopback server, not the Session Refresh application runtime.
The retained build result and source map support only the declared artifact and source scope.
They do not establish current application composition or production parity.
The prepared Session Refresh stack uses historical source bindings, H2, and disclosed substitutes.
All 15 inspected stack bindings matched their declared hashes during this check.

No browser, credentials, application login, business suite, or authenticated endpoint was used.
Setup failures do not establish product failures or release blockers.
Unknown build identity prevents an unsupported readiness claim.
The check does not infer business acceptance or deployment authorization.

## Focused validation

The focused suite contains 26 tests for passive planning and consequential setup boundaries.
A previous Robot command assertion used an unresolved macOS temporary path.
The implementation correctly resolved that suite path.
The fixture now compares resolved paths. This change does not alter application behavior.

Further checks cover Robot suite directories, selected Python environments, and changed resource grants.
Independent review also corrected URL query disclosure, missing environment settings, and relative browser-cache resolution.
The [corrected regression run](independent-review/regressions-after-fix.json) retains exact source identities.
The parent stage performs complete runtime, packaging, and installed-workspace validation before its commit.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
