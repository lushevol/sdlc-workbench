# Construct a domain capability library

Read the section for each artifact being maintained. These are content requirements, not mandatory files for every domain.

## Contracts

Use valid OpenAPI 3.1 YAML for supported REST operations. Reference the relevant official specification when available.
Keep the observed operation subset focused. Other interfaces can use their native schema and concise Markdown bindings.
Document only supported details. List missing contract information explicitly instead of inventing a complete service specification.

For each operation, capture:

| Concern | Required detail when supported |
| --- | --- |
| Identity | System, service, purpose, method, path, stable operationId, API version, scoped base URL |
| Access | Authentication mechanism, permissions, headers, token/session prerequisites; no credential values |
| Request | Path/query/header parameters, body, media type, types, requiredness, nullability, defaults, constraints, dependencies |
| Response | Status, relevant headers, body schemas, conditional fields, errors, pagination and continuation |
| Dependencies | Interface consumers/providers, ordering, protocols, versions, access and runtime prerequisites |
| Provenance | Exact specification revision or observed exchange, date, environment, locator, hash and evidence classification |

Reuse `components/schemas` and `$ref` for common models. Keep `operationId` and case identities stable across updates.
Use schema references from the existing domain instead of copying definitions into workflows or background pages.
OpenAPI 3.1 nullability uses JSON Schema types or unions, not the older `nullable` keyword.
Distinguish fields required by a specification from fields merely present in all available samples.
An unknown permission, error shape, or default stays unknown; it does not imply no permission, no errors, or a default.
Do not publish captured credentials as security defaults or turn an observed URL into execution authority.

### Paired examples

Keep each request attached to its corresponding response, operation, condition, and source exchange.
Use named OpenAPI examples for concise variants. Store detailed pairs in `Contracts/examples/` when context is needed.
Record path/query/header values and request bodies that explain the variation. Redact private values consistently.
Preserve status, relevant response headers, body, and the original evidence binding for that same request.
Represent observed differences in optional parameters, payloads, empty results, pagination, validation errors, and permission failures.
Missing variants are gaps to investigate, not scenarios to fabricate or execute without task authorization.

A paired case needs these fields; use the project's existing format when equivalent:

```yaml
id: list-items-page-two
operationId: listItems
applicability:
  environment: synthetic
  api_version: "1"
request:
  method: GET
  path: /items
  query: {cursor: example-next}
response:
  status: 200
  body: {items: [], next: null}
evidence:
  classification: synthetic
  source: illustrative-only
```

This example illustrates pairing only. For retained observations, supply the actual source, revision or hash, locator, and date.
Sanitization must preserve field types, nulls, omissions, relationships, and the distinction between input variants.
Keep original sensitive evidence in its approved location. Record sanitized examples as derivatives rather than claiming identical original bytes.

Validate YAML, references, and examples using available project tooling. Check both request and response schemas when present.
Separate syntax checks, schema checks, source comparison, and live verification in the outcome.
An observation-derived schema can model the available captures while recording incomplete service-wide guarantees.

## Workflows

Describe a complete operational scenario in Markdown, including intermediate outputs and decisions needed by another agent.
Use the actual project-specific sequence. A generic vendor API list cannot supply missing selection rules or deployment steps.
Keep a partial workflow usable by naming where evidence ends and which result remains unverified.

Use this content checklist, combining sections when that improves readability:

```markdown
# Workflow: <scenario>

## Purpose and applicability
Outcome, trigger, system, environment, versions, and conditions where the procedure applies.

## Prerequisites and inputs
Access, configuration, dependencies, variable definitions, required inputs, and supported defaults.

## Procedure
For each step: action, exact API/command/script, inputs, expected output, interpretation, and next-step dependency.
Reference the matching operation and paired cases in Contracts.

## Decision rules
Selection rules, branches, continuation, bounded retry, stop conditions, and unresolved decisions.

## Failure points
Attempt, relevant input, actual error, scope, reproduction status, cause status, correction, and evidence.

## Verification and recovery
Assertions that establish completion, observed results and limits, safe retry, rollback or manual intervention.
Distinguish documented verification steps from checks actually executed.

## Related knowledge and evidence
Relative links to conventions, background, source revisions, and retained results.
```

Preserve failed approaches when their conditions or corrections help avoid repeated investigation.
Record confirmed causes separately from hypotheses and unresolved issues. Include a successful correction only when supported.
Keep an unsuccessful attempt scoped to its inputs, version, environment, and permissions.
Do not convert one failure into a universal prohibition or erase useful failures after recording success.
Keep long logs and incident timelines in task evidence and link the relevant ranges.

### Optional executable support

Keep the Markdown procedure useful when no script exists. Link scripts at the steps they implement.
Document each tool's purpose, inputs, outputs, dependencies, side effects, errors, and tested conditions.
Prefer predictable structured output when another step consumes it. Use existing project conventions.
For network acquisition, retain bounded timeouts/retries and sanitized failure guidance.
Run existing meaningful tests for changed tools. Check copied-folder execution only when standalone use is claimed.
Do not label an unexecuted script verified or claim dry-run safety without inspecting its behavior.

## Knowledge

Explain the domain concepts and rationale needed to interpret contracts and workflows.
Keep background, architecture relationships, conventions, scoped rules, decisions, and known limitations where they answer a current question.
Reference contracts for wire details and workflows for execution steps.
Link canonical business intent rather than republishing its rules as a competing authority.

For material facts, identify their source, applicable version/environment/date, confidence basis, and limits.
Keep documented intent, observed implementation, inference, and deployment state distinguishable.
Never resolve contradictory observations by selecting the latest file timestamp alone.
Use exact source scope to explain compatible variations. Flag unresolved contradictions without silently replacing supported facts.
Background extraction does not turn draft decisions into approved rules.

## Index and maintenance checks

Update the domain README with linked operations, scenarios, background topics, applicability, and material gaps.
An index entry must resolve to real content. Do not advertise absent scripts, APIs, or verified outcomes.
Reopen existing files and compare source conditions before merging. Preserve earlier supported examples and significant contrary evidence.
Keep stable file and operation identities. Add a distinct scenario only when its purpose or conditions differ materially.
Check the diff for lost detail, duplicates, broken links, secrets, unsupported guarantees, and unreviewed authority claims.
Record actual automated checks separately from writing review under the project's reporting convention.
