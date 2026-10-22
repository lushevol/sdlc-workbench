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

# Canonical case bindings

The [canonical catalog](../../tasks/ui-test-coverage-20261022/test-cases.md) owns all 521 case definitions.
The POM does not duplicate those definitions.
The [binding manifest](bindings.json) links canonical components and steps to executable source.
The generated [case inventory](cases.json) retains every case identifier, version, hash, quality state, and execution state.

All 521 canonical cases remain `NOT_RUN`.
The 28 failed canonical UI gates remain `BLOCKED` in this inventory.
Static component support does not establish complete scenario coverage.
The synthetic session fixture checks harness mechanics.
It does not establish React application behavior, BFF authentication, or business acceptance.

| Support state | Meaning |
| --- | --- |
| `UNBOUND` | No implemented component or workflow currently maps to this definition. |
| `PARTIAL` | Named components or a substitute workflow map to part of this definition. |
| `BLOCKED` | The canonical case has a failed UI quality gate. |
| `COMPLETE_BINDING` | Every canonical step maps to real application fixtures and inspected source references. |

`COMPLETE_BINDING` describes an implementation binding.
It does not establish passing execution.
The current manifest contains no complete bindings or verified business scenarios.

Run the static checker from the workspace root:

```sh
node e2e/scripts/check-traceability.mjs
```

After an authorized canonical or binding change, inspect the definitions and regenerate the derived inventory:

```sh
node e2e/scripts/check-traceability.mjs --write
node e2e/scripts/check-traceability.mjs
```

The checker verifies canonical identities, hashes, versions, assertion counts, step references, implementation hashes, and generated-file freshness.
It rejects duplicate, missing, stale, and orphan records.
Implementation references require an existing file and the exact named text.
This text check does not prove call execution or semantic equivalence.
The checker does not launch a browser, inspect deployed controls, or change canonical readiness.

The [AUTH-078 binding](../../tasks/ui-test-coverage-20261022/test-cases.md#auth-078) maps 13 steps to a synthetic session workflow.
Its six assertion steps reference independent flow assertion identifiers.
The fixed access and refresh expiry step remains unbound.
The binding records these limits under `gaps`.
The [session flow](../flows/session-extension.flow.ts) separates dialog closure, installed credentials, request counts, and authentication validation.

Component references use existing canonical component identifiers.
They contain no locator implementation.
The executable page and component objects own locators.
The generated inventory copies support limits from the binding manifest.
These limits include dynamic fixture identifiers and source differences in accessible roles or dialog names.

Live component coverage remains `null` in this inventory.
Runtime discovery must measure identifiable components in the selected page state.
Such measurements must retain their target revision, environment, observation time, and execution evidence separately.
