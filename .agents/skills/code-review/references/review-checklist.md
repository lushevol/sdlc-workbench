# Semantic review checklist

Read this reference when selecting review risks or investigating a suspected defect.
Use the sections relevant to the changed behavior.
Read [validation guidance](validation.md) before claiming that checks establish behavior.

## Select consequential risks

Start with the change purpose, affected users, data, interfaces, and execution paths.
Identify the invariants that the change must preserve.
Use repository instructions, approved contracts, implementation, callers, and inspected assertions as separate evidence.
Resolve the actual trigger and failure path before reporting a defect.
State unresolved business intent as a question or evidence limit.

Prioritize security failures, incorrect business results, data loss, service disruption, and incompatible contracts.
Review changed lines and enough surrounding code to establish their effects.
Follow affected callers, imported interfaces, serializers, persistence mappings, and configuration paths.
A finding can describe unchanged code when the proposed change creates its failure condition.
Locate the finding on the smallest changed range that explains the cause.

## Correctness and business behavior

- Does the implementation satisfy the documented condition, action, observable result, and required limit?
- Can boundary values, missing values, malformed input, or unexpected ordering produce incorrect results?
- Are comparisons, units, currencies, time zones, rounding, and date boundaries consistent with the contract?
- Does each state transition preserve required preconditions and terminal states?
- Can partial success, retries, cancellation, or duplicated delivery repeat a business effect?
- Do feature flags, defaults, and fallback paths preserve the intended behavior?
- Does a changed dependency or configuration alter behavior outside the requested scope?

Inspect the complete path when a local check depends on upstream normalization or downstream validation.
Do not report a missing guard when an established boundary already guarantees its precondition.
Do not invent policy from variable names or existing implementation alone.

## Security and trust boundaries

- Where does untrusted input enter, and where does the code use it with greater authority?
- Can input reach command execution, queries, templates, file paths, redirects, or deserialization without appropriate controls?
- Can URL handling expose internal services or credentials through redirects, DNS changes, or alternate address forms?
- Are credentials, personal data, and tokens excluded from logs, errors, reports, caches, and client responses?
- Do cryptographic operations preserve the required randomness, integrity, expiration, and key handling?
- Does a new dependency, build step, or deployment permission expand the trusted execution surface?

Trace a plausible source, transformation, boundary, and sensitive operation before claiming exploitability.
Record required attacker access and configuration conditions.
Redact suspected secret values from findings and retained evidence.
Pattern matches identify candidates; they do not establish complete secret detection or a clean security result.

## Authentication, authorization, and tenant isolation

- Does the server authenticate each protected operation through the expected identity mechanism?
- Does authorization cover the requested object and operation, including list, export, batch, and administrative paths?
- Does tenant identity come from a trusted context rather than an unchecked client field?
- Do queries, cache keys, storage paths, background jobs, and events preserve tenant boundaries?
- Can role changes, session expiration, revocation, impersonation, or shared credentials bypass required checks?
- Do failures deny access without revealing sensitive existence or ownership information?

Inspect object ownership checks beyond route middleware.
Check cache and asynchronous paths when they carry an identity outside the original request.

## Data changes and migrations

- Can old and new application versions use the schema during the planned rollout order?
- Do defaults, nullability, constraints, indexes, and backfills preserve existing records?
- Can migration locks or table rewrites exceed established availability limits?
- Does the migration handle interruption, restart, duplicate execution, and partial completion?
- Can mapping changes truncate, reinterpret, omit, or expose stored data?
- Are recovery assumptions supported by the deployment procedure and retained evidence?

Inspect readers and writers before treating a schema change as compatible.
State unknown production volume, engine behavior, or deployment order beside the affected conclusion.
Do not run a migration against shared data as part of review.

## Concurrency and asynchronous execution

- Can concurrent requests violate uniqueness, balance, ordering, or ownership invariants?
- Are check-and-write sequences atomic where correctness requires atomicity?
- Do transaction boundaries and isolation levels match the demonstrated failure risk?
- Can locks, callbacks, cancellation, or shared mutable state cause deadlock, races, or resource leaks?
- Do retries preserve idempotency and distinguish transient failures from permanent failures?
- Can events arrive late, out of order, or more than once?
- Are acknowledgments, commits, and external side effects ordered to prevent lost or repeated work?

Describe an interleaving or concrete sequence when reporting a concurrency defect.
Do not assert timing, throughput, or recovery durations without supporting evidence.

## APIs and compatibility

- Do existing callers still receive the documented status, schema, defaults, ordering, and error behavior?
- Are newly required parameters, removed fields, renamed operations, or changed types compatible with supported consumers?
- Do serialization, validation, routing, pagination, and version negotiation preserve existing contracts?
- Are event producers and consumers compatible across mixed deployment versions?
- Can an additive change alter overload resolution, validation, dispatch, or exhaustive matching?
- Do dependency upgrades change supported platforms, runtime behavior, or transitive requirements?

Inspect actual consumers and supported compatibility promises.
Public syntax changes are evidence candidates, not automatic proof of breakage.
Compare the selected baseline and reviewed implementation; never substitute the previous commit automatically.

## Errors, cleanup, and operational behavior

- Are errors propagated or translated without hiding consequential failure?
- Can cleanup run after partial initialization, timeout, cancellation, or exception?
- Are files, connections, locks, subscriptions, and temporary resources released through each exit path?
- Can broad exception handling convert a failed operation into an incorrect success response?
- Do logs and metrics identify actionable failures without disclosing sensitive data?
- Do health checks, readiness, shutdown, and retry behavior preserve established availability requirements?

Check the caller's error contract before proposing exception handling changes.
Logging before every throw is not a universal requirement.

## Performance and resource use

- Does the change add repeated queries, unbounded iteration, large materialization, or costly work inside a repeated path?
- Are pagination, batching, backpressure, queue growth, and memory use bounded where the contract requires limits?
- Does an index support a changed query under the actual filtering and ordering pattern?
- Can caching produce stale, incorrectly shared, or unbounded data?
- Does asynchronous code block its execution thread or create uncontrolled parallel work?

Connect performance findings to an affected input size, path, or established constraint.
Use measurements where practical and authorized.
Treat unknown workload and infrastructure capacity as evidence limits.
Do not use a universal complexity threshold as proof of a defect.

## Infrastructure and delivery

- Do permissions, network exposure, workload identities, and storage policies match the intended trust boundaries?
- Can mutable images, unverified downloads, build secrets, or broad CI tokens expose the delivery process?
- Do deployment ordering, readiness, shutdown, and rollback preserve supported versions and persistent data?
- Are resource limits, probes, and encryption settings required by this workload and its supplied policy?
- Does a workflow run untrusted pull request code with privileged credentials or write permissions?

Inspect rendered configuration, inherited image settings, and platform defaults before reporting a missing setting.
Apply supplied policy rather than universal Docker, Terraform, or Kubernetes rules.
Use existing infrastructure analyzers when available; keep their findings separate from manual review conclusions.

## Tests and review conclusions

- Do inspected assertions observe the changed result or invariant?
- Do tests exercise consequential boundary conditions, failure paths, authorization, and compatibility risks?
- Can mocks, fixtures, swallowed errors, or weak assertions permit the demonstrated defect?
- Does test setup preserve the actual transaction, serialization, or asynchronous behavior under review?
- Are skipped tests or changed assertions removing relevant protection?

Use [validation guidance](validation.md) to select meaningful checks and interpret their results.
Request a test only when it protects consequential behavior or demonstrates a confirmed defect.
Avoid findings about personal style, universal language preferences, or harmless pre-existing conventions.
Consolidate findings with the same root cause.
Do not invent findings to fill a quota.
