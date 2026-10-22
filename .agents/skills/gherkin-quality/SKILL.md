---
name: gherkin-quality
description: Generate and review evidence-backed business and UI E2E Gherkin scenarios, component inventories, assertion mappings, and automation readiness.
---

# Generate and review Gherkin test cases

Keep business intent, UI actions, and observed results separate.
Use this skill when creating or reviewing UI E2E specifications and their business behavior links.
Keep business-only acceptance criteria independent of UI implementation details.

Read the [writing rules](references/writing-rules.md) when generating or reviewing cases.
Read the [command and manifest guide](../../../docs/GHERKIN_QUALITY.md) for local validation and CI use.
The [session fixtures](../../../docs/examples/gherkin-session/session.md) demonstrate source-backed wording and unresolved verification.

## Select sources and definitions

Read repository instructions and the existing task before changing business cases.
Apply the [canonical case rules](../../../tasks/README.md#canonical-gherkin-test-cases).
Keep task cases in one `06-test-cases.md` catalog with stable headings and criterion links.
Preserve historical cases and evidence when their bytes support retained results.
Tooling maintenance requires no new business task or knowledge record.

Inspect requirements, acceptance criteria, UI source, existing tests, and retained observations at exact revisions.
Use existing knowledge and investigation results before asking for unavailable information.
Keep approved intent, established observations, draft expectations, and unknown rules distinct.
An implementation observation does not establish an approved requirement.

Discover components through existing source, accessibility inspection, page objects, or browser tools within authorized access.
Use the existing browser framework when runtime discovery is needed.
Do not add a discovery service or browser dependency for this workflow.

## Generate linked specifications

Write or link the business scenario before describing its UI implementation.
Name the actor, permission, entity, initial state, data, and required outcome.
Identify positive, negative, boundary, failure, recovery, and concurrency cases supported by the scope.
State material exclusions and unresolved policy. Do not invent cases solely to increase their count.

Build a component inventory before writing UI interactions.
Record each component's semantic type, verified identity, containing scope, distinguishing attributes, and evidence.
Prefer accessibility role and name, then visible label with scope, stable test ID, or another stable identifier.
Verify uniqueness within the stated scope. Repeated rows require a stable business identifier.
Mark source-derived semantics and runtime uniqueness separately when only one has been inspected.

Write one ordered action per `When` step.
Identify the actor, action, component type, exact identity, and location.
Distinguish a business verb from a control bearing the same text.
State exact labels even when they differ from illustrative proposal wording.

Give every `Then` an observation point, comparison, and expected value or state.
Separate UI observations from functional assertions.
Use timing limits only when a cited source establishes their meaning and measurement conditions.
Dialog closure alone cannot prove session renewal. Request counts alone cannot prove successful authentication.
Link each outcome to its requirement or established behavior evidence.

## Map evidence and automation

Save a versioned manifest beside the canonical catalog or under its owning task evidence.
Use root-relative paths, exact file hashes, and source line ranges.
Link each scenario to its business intent, requirement evidence, and specific criterion locator.
Map every step by its absolute source line to components and evidence.
Hash the completed specification after its wording and line positions are stable.
Refresh hashes and step mappings after authorized edits. Preserve earlier evidence versions when retained results require them.

Inspect the existing framework before assigning automation bindings.
Map each step to an exact keyword or function and its helper assertions.
Inspect setup, fixtures, selectors, response predicates, and omitted boundaries.
Readable Gherkin is not automatically executable because a Robot or JavaScript test exists.
Use existing Robot Browser bindings where applicable. Do not introduce a parallel Cucumber framework.

Record missing labels, scopes, expectation sources, or bindings against the affected scenario and step.
Give each gap a consequence, owner, and next action. Use `unknown` when the owner is unavailable.
Leave affected review states `UNVERIFIED`. Do not invent reviewer identities or approval records.

## Validate and correct

Run the installed checker against explicitly selected UI specifications:

```sh
ai-sdlc gherkin tasks/<task-id>/06-test-cases.md --manifest tasks/<task-id>/evidence/gherkin-manifest.json --root .
```

Use repeatable `--scenario ID` options when the canonical catalog also contains business-only scenarios.
Use [the guide](../../../docs/GHERKIN_QUALITY.md) for schema inspection, supported syntax, exit codes, and strict mode.
The checker reads local evidence. It does not execute browser steps or authenticate review claims.
Keep its findings separate from ordinary artifact lint and agent semantic findings.

For semantic review, compare every identity, scope, assertion, and binding with its cited source bytes.
Check contradictions between business scenarios, UI steps, manifest records, and executable assertions.
Report unsupported assumptions even when deterministic checks pass.
Use the existing [verification procedure](../verify-implementation/SKILL.md) for claims about actual behavior.

Apply authorized wording corrections, then rerun the checker.
Keep unresolved evidence visible. A passing syntax check cannot resolve missing business intent.
Treat automation readiness as scoped to inspected bindings and supported expectations.
Keep execution `NOT_RUN` until matching retained execution establishes the stated assertions.

## Deliver the handoff

Return links to canonical business and UI cases, the component inventory, criterion mappings, and missing information.
Include checker status, actionable findings, semantic review limits, and automation binding status.
Keep passing business execution separate from specification quality and readiness.
When saving a report, use the repository's output-review metadata with the actual automated result.
Keep `asd_review: PENDING` unless a complete writing review occurred.
