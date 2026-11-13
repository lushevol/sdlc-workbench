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

# Gherkin quality and automation readiness

[Documentation map](README.md)

Use the shared Gherkin procedure to generate and review source-backed business and UI E2E cases.
Keep business intent, UI identity, observable assertions, semantic review, and automation bindings distinct.
The checker validates declared wording and evidence. It does not establish business approval or passing execution.
Use existing test frameworks through inspected native or mapped bindings; no parallel Cucumber framework is required.
Business-only acceptance criteria retain their ordinary artifact validation route.

## Use the workflow

Invoke the `gherkin-quality` skill when generating or reviewing UI E2E cases.
Read its [writing rules](../.agents/skills/gherkin-quality/references/writing-rules.md) for mandatory requirements and vocabulary.
Keep business intent linked to the canonical UI case and its specific criterion.
Build the component inventory from inspected evidence before writing UI steps.
Record missing details instead of filling them from illustrative examples.

Run the installed command from the workspace root:

```sh
ai-sdlc gherkin tasks/<task-id>/06-test-cases.md --scenario UI-001 --manifest tasks/<task-id>/evidence/gherkin-manifest.json --root .
ai-sdlc gherkin --print-schema
```

Use explicit `.md` or `.feature` files. Directories are not accepted.
Use repeatable `--scenario ID` options when a canonical catalog contains both business and UI scenarios.
Without that option, every scenario in each selected file receives UI quality checks.
Structural syntax checks cover each selected file, including unselected scenarios.
The command does not load workspace configuration or call external connectors.

Use `--strict` to reject maintainability warnings.
Use `--require-ready` when CI requires automation readiness.
Keep ordinary `ai-sdlc lint` and workspace validation separate from this gate.

| State | Meaning | Normal exit |
| --- | --- | --- |
| `FAIL` | A mandatory structural, wording, or mapping rule is violated. | 1 |
| `UNVERIFIED` | Evidence, expectation authority, semantic review, or automation binding remains unresolved. | 2 |
| `WARNING` | Mandatory checks pass with a maintainability concern. | 0; strict mode returns 1 |
| `PASS` | Required checks pass within recorded evidence and review limits. | 0 |

State precedence is FAIL, UNVERIFIED, WARNING, then PASS.
The readiness option returns 1 when any selected case is unready.
Argument errors also return 2. A checker result contains structured findings that distinguish missing evidence from argument errors.

## Evidence manifest

The installed schema is the canonical machine contract. Inspect it with `--print-schema`.
The [example manifest](examples/gherkin-session/manifest.json) shows actual UI and behavioral evidence.
Do not copy its labels or source claims into unrelated applications.

| Field | Required meaning |
| --- | --- |
| `version` | Contract version, currently `1`. |
| `evidence` | Source IDs mapped to root-relative paths, SHA-256, bounded lines, kind, authority, and optional revision. |
| `scenarios` | Entries keyed by the stable case identifier. The last tag before `Scenario` supplies this identifier. |
| `file`, `sha256` | Exact canonical specification path and complete file fingerprint. |
| `behavior` | Business intent, behavioral evidence ID, and a specific requirement or criterion locator. |
| `components` | Actual type, exact identity, identity method, distinguishing scope, and UI evidence IDs. |
| `steps` | Absolute file-line mappings for conditions, interactions, events, and assertions. |
| `review` | Recorded semantic review state, actual reviewer, timezone-aware completion time, and scope notes. |
| `automation` | Optional framework, `native` or `mapped` mode, exact per-step symbols, evidence, and binding review. |

Each source `kind` is `ui`, `behavior`, or `automation`.
Each source `authority` is `approved`, `established`, `draft`, or `unknown`.
These fields record claims. The checker does not authenticate them.
Draft and unknown expectation sources keep their consuming cases unverified.
An established implementation observation does not become an approved requirement.

Each interaction maps its target components through `components`.
Conditions and assertions also map their referenced UI components.
Inventory type, identity, and scope must appear explicitly in the mapped step.
Assertions declare `observation: ui` or `observation: functional`.
An event classification supports non-UI events; it cannot hide a recognized UI action.

Use a timezone-aware ISO timestamp when a review actually completes.
Leave review state `UNVERIFIED` and reviewer fields null when evidence cannot support completion.
Never invent an identity or approval to obtain PASS.
Semantic review must inspect identity, uniqueness, scope, expectation meaning, fixtures, and every executable assertion.

An automation binding covers each setup, action, and assertion step, including inherited Background steps.
Its exact `symbol` must occur within cited automation source lines.
Symbol presence alone does not establish matching parameters, executable compatibility, or assertion coverage.
Record those conclusions in the binding review after inspecting the existing framework.
Native mode identifies direct step consumption; mapped mode identifies implementation through existing keywords or functions.

Keep paths within the selected evidence root. Symbolic links cannot escape that root.
The default root is the manifest's parent directory. Use `--root .` for workspace-relative manifests.
Hashes use exact file bytes. Line ranges use one-based, inclusive text lines.
Refresh mappings and reviews after definition or evidence changes.
Preserve older definitions and fingerprints when retained execution depends on them.

## Deterministic coverage and limits

Checks reuse the existing English Gherkin subset for clauses, Background, outlines, and Examples.
Scenarios start with Given conditions and end with Then assertions.
Ordered When/Then groups can repeat to preserve intermediate observations.
Given conditions cannot follow an action.
Markdown fences preserve absolute source line numbers.
Unsupported step syntax fails within the selected subset.
The checker supports comments, step tables, and Doc Strings; it does not replace a complete Gherkin parser.
Selected inputs and evidence files have an eight MiB limit.

The checker detects missing component types, identities, scopes, inventory references, and recognized compound actions.
Recognized actions include filling fields, replacing values, and moving the mouse, pointer, or cursor.
Clock movement remains a fixture event. Movement and replacement nouns do not establish UI actions.
It detects selected vague assertions, missing source mappings, stale hashes, invalid ranges, and incomplete reviews.
It also checks criterion fields, assertion classification, automation coverage, and cited binding symbol presence.
Unrecognized interaction or observation wording remains unverified.
Arbitrary semantic equivalence and every possible ambiguous sentence are outside deterministic coverage.

Review exact labels, accessible roles, repeated rows, and target uniqueness against actual sources or DOM evidence.
Review fixture values, timing boundaries, requirement meaning, and outline parameter handling separately.
Inspect actual assertions before recording framework compatibility.
The checker does not inspect a live DOM, run browser tests, authenticate reviewers, or establish full ASD compliance.

## Actionable findings

Each finding contains `status`, `rule`, `path`, `scenario_id`, `line`, `explanation`, `correction`, and `evidence`.
Missing evidence uses explicit missing-information text or the absent reference ID.
File-level findings can have no scenario ID or step line.
Human reports add the consequence, owner, and next action.
Use `unknown` when the responsible owner is unavailable.

```json
{
  "status": "FAIL",
  "rule": "ui_type",
  "path": "cases.feature",
  "scenario_id": "UI-001",
  "line": 5,
  "explanation": "The UI action does not identify a component type.",
  "correction": "Name the actual button, textbox, option, or other component.",
  "evidence": []
}
```

Correct supported wording, retain unresolved gaps, and run the checker again.
Do not substitute a numerical score for findings.

## Session demonstration

```sh
ai-sdlc gherkin docs/examples/gherkin-session/ambiguous.md --manifest docs/examples/gherkin-session/manifest.json --root .
ai-sdlc gherkin docs/examples/gherkin-session/session.md --manifest docs/examples/gherkin-session/manifest.json --root .
```

The ambiguous fixture must FAIL for missing UI target details and a vague result.
The source-backed fixture must remain UNVERIFIED while expectation review and automation mapping remain unresolved.
The actual dialog says `Your session has been expired`. Its action label is `Extend`.
The example separates dialog visibility from authenticated request validation.
Its request predicate covers portal authentication validation, not downstream authorization or extended session lifetime.

These maintained fixtures support tooling demonstration. They do not replace historical canonical business cases.
Generated workspaces receive the guides and fixtures, but not business checkouts, knowledge, or task evidence.
Their source references remain unavailable until the corresponding assets exist.
Missing assets produce UNVERIFIED findings. No startup download occurs.

## Maintenance checks

The source checkout owns the [quality regressions](../tests/test_gherkin_quality.py) and [CLI regressions](../tests/test_gherkin_cli.py).
Run their supported unittest checks after changing the checker, schema, or maintained fixtures.
Check both demonstration states after changing the example definitions or their manifest.
Tooling checks do not run the business browser scenario or establish target-environment behavior.
Generated workspaces receive the guide and fixtures without runtime test source or project validation history.
