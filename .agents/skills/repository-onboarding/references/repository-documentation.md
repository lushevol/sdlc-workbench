# Repository topic documentation

Read this guide when the user requests documents inside the inspected repository.
Keep the normal assessment workflow and external staging directory.
The scanner still requires an output path outside the entire target Git checkout.

## Authorization and directory boundary

The default `assess` mode does not write inside the target repository.
An explicit request for repository documents authorizes that documentation output.
Apply that authorization without requesting it again.
It does not authorize implementation changes, application execution, knowledge publication, or unrelated edits.

Use `documentation_dir` for a repository-relative directory.
Prefer `docs/onboarding/<run-id>/` when repository instructions permit that location.
Check the actual Git root, applicable instructions, existing files, and checkout changes before writing.
Resolve the directory under the target Git root and reject escapes, symlink traversal, or independent nested checkouts.
Do not write into Git metadata, implementation roots, generated runtime output, or dependency directories.
Use a new run directory and preserve previous assessments.
Update existing documents only when the user's request covers that update.
Keep unrelated documents and source changes intact.

## Topic bundle

Use the following topics as the default split.
Adapt names to an existing repository documentation convention when that improves navigation.
Record the actual file list in the index and provenance.

| File | Content |
| --- | --- |
| `README.md` | Purpose, exact assessed revision, critical dependency consequences, topic links, and evidence limits. |
| `architecture-and-responsibilities.md` | Deployables, components, owned functions, entrypoints, and non-goals. |
| `provided-apis-and-permissions.md` | Provided operations, exposure, authentication, authorization, and inspected enforcement points. |
| `outbound-apis-and-call-conditions.md` | External calls, callers, triggers, timing, guards, endpoint bindings, and failure behavior. |
| `messaging-and-events.md` | Kafka, MQ, Solace, managed events, bindings, activation, delivery, and permission limits. |
| `data-and-storage.md` | Databases, caches, search, files, object stores, reads, writes, transactions, and access limits. |
| `configuration-and-secrets.md` | Configuration files, safe key names, consumers, profiles, defaults, precedence, and unresolved substitutions. |
| `identity-and-network.md` | Identity providers, LDAP, token and trust flows, gateways, proxies, transport, and network restrictions. |
| `build-delivery-and-operations.md` | Toolchains, packages, deployment, platform services, schedules, observability, and permitted verification commands. |
| `readiness-and-findings.md` | Readiness, evidence-backed findings, owners, next actions, Gherkin criteria, and required decisions. |
| `evidence-index.md` | Claim navigation, dependency coverage, exact source locators, actual checks, and verification limits. |
| `evidence/claims.json` | Portable derivative of claims, dependency records, and all dependency-family coverage records. |
| `provenance.json` | Repository identity, assessed revision, generation metadata, original artifact hashes, file list, and check results. |

Keep relevant unknowns in their topics rather than omitting an unsupported family.
For an empty topic, give its inspected scope, coverage disposition, and evidence limit.
Do not copy unrelated source excerpts to make a topic appear complete.
Assign each dependency one primary topic and link from other topics when needed.
Cross-links must retain the same dependency ID and evidence status.
Preserve separate statements for source observations, inferred consequences, conflicts, and unresolved production behavior.
Cross-repository claims need evidence from both boundaries and an explicit review location.

## Portable evidence and provenance

Keep `inventory.json`, `repo-onboarding.json`, and helper output in external staging.
The original report retains its machine-local checkout path for the existing evidence helper.
Do not copy that absolute path or staging directory into repository documents.

Derive `evidence/claims.json` from the validated original report.
Preserve claims, citations, dependency attributes, review actions, and coverage records without changing their meaning.
Keep repository-relative citation paths and exact source line ranges.
Replace a checkout locator with `.` when a portable locator is included.
Label this replacement explicitly as a portable rebase.
Identify the file as derived documentation data, not a validator-compatible `repo-onboarding.json` report.
No new runtime schema or validator is required.
Check the derivative against the original arrays and record any intentional omission or safe redaction.
Do not silently remove conflicting claims, unknown fields, or coverage limits.

Record these fields in `provenance.json`:

- Repository ID and full assessed Git commit ID.
- Generation timestamp and `repository-onboarding` skill identity.
- Candidate documentation status and portable checkout locator `.`.
- SHA-256 hashes for the original structured report and inventory.
- Relative paths for all generated topic and evidence files.
- Actual check names, results, scopes, and limits.
- Source checkout changes and inventory omissions that limit the assessment.
- Separate automated-check and ASD review metadata.

Use artifact hashes to identify staging inputs without embedding workstation paths.
Link sources relative to each topic file and show the assessed revision beside citation guidance.
Current checkout links can change later; the recorded revision defines the assessed source baseline.
Use claim IDs and line ranges when the renderer cannot navigate source lines directly.
Do not use another repository's relative paths as evidence for this checkout.

Exclude credentials, secret values, customer data, trading data, and unnecessary source excerpts from every output.
Record safe configuration key names and unresolved binding descriptions instead.
Do not open secret stores to fill documentation gaps.

## Checks and commit timing

Run the existing evidence helper against the original staging report before committing repository documents.
Its HEAD rule and committed-byte checks remain unchanged.
New documentation can remain untracked during this check when cited source files match the assessed commit.
Record the actual helper result and its limits.

Check topic links, source paths, cited line ranges, derivative equality, and the generated file list.
Check that documentation contains no machine paths, staging-only links, secret values, or unsupported certainty.
Review the diff and confirm that implementation source and unrelated changes remain intact.
Run writing checks appropriate to the repository's report standard.
Do not execute the target application or its tests merely to generate documents.

A documentation commit changes HEAD while preserving the assessed implementation baseline.
The original report then fails the helper's HEAD rule until a new assessment uses the new revision.
Do not relabel the original revision or weaken that rule to obtain a passing result.
For later review, compare each cited file's committed bytes at the assessed revision with the current file.
Check cited line ranges against that baseline and record mismatches or unavailable objects.
This separate baseline check does not replace the original helper or establish current deployment behavior.
Reassess changed source rather than silently carrying its earlier conclusions forward.

Keep automated checks separate from ASD review in each saved report.
Use the following review fields and set results only from checks actually performed:

```yaml
standard: ASD-STE100
automated_check: PENDING
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```

Use frontmatter in Markdown reports and equivalent review fields in JSON artifacts.
Keep ASD review pending until a complete writing review occurs.
Every finding needs evidence, a consequence, an owner, and a next action.
Mark unknown owners explicitly.

## Knowledge boundary and handoff

Generated repository documents are candidate engineering documentation.
They do not become governed Workbench knowledge through file placement, validation, or a Git commit.
Keep important requirements and decisions pending the required human review.
Use the normal ingestion and governance procedures when publication is later authorized.

Follow applicable repository commit instructions for the completed documentation stage.
Do not stage unrelated files or modify catalogs to make documentation visible.
Report the index path, source baseline, actual checks, commit result when applicable, and unresolved review needs.
