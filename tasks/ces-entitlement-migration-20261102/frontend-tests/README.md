# CES frontend migration checks

No critical conclusions require user attention or action.

These scripts execute local fixtures. They do not contact enterprise identity, CES, or production services.
The [canonical catalog](../06-test-cases.md#tests-first-shared-adapter-implementation) owns behavior definitions.
The [stage review](../10-change-review-frontend-adapters.md) owns results, source identities, and remaining limits.

Use the existing workspace Node runtime, Playwright Chromium, and cached base development dependencies.
The scripts install and download nothing.
Run commands from the Workbench root.
Choose a new output directory for each run. Completed results cannot be overwritten.

```sh
node tasks/ces-entitlement-migration-20261102/frontend-tests/run-browser.mjs
node tasks/ces-entitlement-migration-20261102/frontend-tests/run-portal.mjs
```

Set `CES_TEST_OUTPUT` to select another durable output directory.
Use `--baseline` with the shared-module script only against the intended original source.
The retained baseline already exists. Running current code with that flag does not recreate original behavior.
Both browser scripts require permission to launch Chromium and listen on loopback.

The shared-module runner bundles actual login, drawer, profile formatter, and authenticator source.
It substitutes hooks, dispatch, token decoding, and persistence.
It asserts ordinary calls, provider isolation, bound conflicting tiles, state replacement, display, and restore identity.

The portal runner bundles the actual base React App and shared authenticator.
It exercises login, profile actions, drawer launch, ordinary dispatcher launch, and permission withdrawal.
The remote consumer uses the existing permission-call signature.
Authentication responses, corporate toolkit elements, analytics, native startup, and remote application content remain controlled boundaries.
Each completed checkpoint saves a result immediately. The portal runner also saves a screenshot.
Screenshots establish visible state. Separate assertions establish permission and stored-state outcomes.

Run the existing and new container assertions without adding dependencies:

```sh
node repos/ui/mfe-base/node_modules/jest/bin/jest.js \
  --config tasks/ces-entitlement-migration-20261102/frontend-tests/container-jest.config.cjs \
  --runInBand
```

The container began as a filesystem copy. Its [delivery branch](../10-change-review-frontend-adapters.md#delivery-branches) now has local Git history.
The retained `mfe-ratan-container.patch` preserves the earlier `d5b5cc5` implementation.
Use the current delivery commits for optimized source. Check baseline hashes before applying historical patches.

Run the owning base suite and type check from `repos/ui/mfe-base`:

```sh
BABEL_ENV=test node node_modules/jest/bin/jest.js --runInBand --coverage=false
node node_modules/typescript/bin/tsc --noEmit --emitDeclarationOnly false --incremental false
```

The retained BFF runner compiles actual selected Java source with cached JDK and libraries:

```sh
python3 tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-implementation-20261106/verify_bff_routing.py \
  --repo repos/services/single-ui-bff \
  --java-home /opt/homebrew/opt/openjdk@17 \
  --output tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-implementation-20261106/bff-routing-replay
```

Use the installed JDK 17 home on other machines. The shown path matches this retained macOS execution.
Choose a new output directory when replaying again.
That focused runner does not replace the owning Maven suite or controller integration.
Missing private starters must be restored before full BFF validation.
CES role-owned writes remain pending under the [recorded decision](../evidence/frontend-entitlement-implementation-20261106/user-role-owned-writes-20261106.md#exact-user-answer).

The [mapped UI specification](../evidence/frontend-minimize-20261106/ui-gherkin-manifest.json) records each portal interaction and assertion.
Regenerate it after authorized catalog or bound-source changes, then run the checker:

```sh
CES_TEST_OUTPUT=tasks/ces-entitlement-migration-20261102/evidence/frontend-minimize-20261106 \
  python3 tasks/ces-entitlement-migration-20261102/frontend-tests/refresh-ui-manifest.py
.venv/bin/python -m core gherkin tasks/ces-entitlement-migration-20261102/06-test-cases.md \
  --scenario TC-FE-CES-013 \
  --manifest tasks/ces-entitlement-migration-20261102/evidence/frontend-minimize-20261106/ui-gherkin-manifest.json \
  --root .
```

`UNVERIFIED` keeps draft expectation review visible. It does not mean the retained local browser assertions failed.
The independent cleanup probe can replay from durable task evidence:

```sh
node repos/ui/mfe-base/node_modules/jest/bin/jest.js \
  --config tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-implementation-20261106/review-jest.config.cjs \
  --runInBand
```

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
