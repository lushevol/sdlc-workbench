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
| Access | Authentication mechanism, permissions, headers, token/session prerequisites, and the environment or approved secret-store binding; no credential values |
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

Use retained real exchanges as published examples when available. Keep synthetic inputs separate for controlled tests or unsupported illustrations.
Label synthetic examples explicitly when no suitable real exchange exists. They establish no observed behavior.
Keep each request attached to its corresponding response, operation, condition, and source exchange.
Use named OpenAPI examples for concise variants. Store detailed pairs in `Contracts/examples/` when context is needed.
Record path/query/header values and request bodies that explain the variation. Redact private values consistently.
Preserve status, relevant response headers, body, and the original evidence binding for that same request.
Represent observed differences in optional parameters, payloads, empty results, pagination, validation errors, and permission failures.
Missing variants are gaps to investigate, not scenarios to fabricate or execute without task authorization.

A paired case records its ID, operationId, applicability, request, response, evidence classification, and exact source binding.
For retained observations, supply the source revision or hash, locator, observation date, and environment when known.
Label a supplied response-body fixture as a fixture. Do not invent its request, status, headers, date, or environment.

Redact credentials, personal or account identities, and other sensitive values. Preserve meaningful application, entitlement, feature, action, and policy names unless sensitive.
Sanitization must preserve field types, nulls, omissions, relationships, and the distinction between input variants.
Keep original sensitive evidence in its approved location. Record sanitized examples as derivatives rather than claiming identical original bytes.
Record redacted fields and transformations. For projections, retain selected source paths or ranges, original lengths, and omitted-content limits.
Do not use projected examples to establish completeness or absence. Compare derivatives against their retained sources before publishing them.

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

### External system dependencies

Record stable contract properties in Contracts or Knowledge. This includes observed base URLs, route templates, API versions, media types, stable authentication schemes, and response properties.
Do not move those properties into project settings or replace them with an unbound local value.
If an adapter requires a local copy, record it as a validated mirror of the domain contract.

Record each external dependency in the workflow's prerequisites and inputs using one of these scopes:

1. **Secret binding** — environment variable or approved secret-store key, authentication type, requiredness, and redaction rule. Never store resolved secrets in skills, examples, catalogs, logs, or task evidence.
2. **Dynamic runtime value** — account, environment selection, selector, request parameter, evidence path, or machine-specific CA path supplied by the selected client or task. Keep its source, owner, safe unset behavior, and confirmed precedence explicit.
3. **Task input** — local variable-file field or task-record field for dynamic values and evidence. Shipped templates remain unset or use safe placeholders.

Use existing client loading conventions for credential and dynamic values. Do not invent a new configuration loader or assume that environment variables override configuration files.
Retained examples supply source evidence for domain properties. They do not supply credentials or independently override the maintained contract.
Validate configuration and access bindings before making an external call. Name missing inputs without printing resolved secrets.
A missing binding blocks that live step and its live verification. Continue offline extraction from retained sources and document the unfinished step.

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
Inspect callers before removing legacy scripts, wrappers, or duplicate files. Keep one maintained implementation and reference shared definitions.
Repair commands, tests, links, and packaging consumers together. Preserve distinct validation responsibilities and protected historical evidence.
Record removed paths, prior hashes or revisions, replacement locations, and reasons in the owning task.
Check the diff for lost detail, duplicates, broken links, secrets, unsupported guarantees, and unreviewed authority claims.
Record actual automated checks separately from writing review under the project's reporting convention.
