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

# Current BFF audit runtime

> **Apply these results only to the declared isolated local runtime.**
> Action: Retain the substitutions with each claim. Consequence: This build cannot establish production configuration equivalence. Owner: Codex evidence maintainer.
> Evidence: [readiness](readiness.json), [source manifest](attempt-06/source-build-manifest.json), and [runtime identity](attempt-06/runtime-start.json).

The selected business revision is `834b4155232222347220e47139a502ee43a9cbdf`.
The source manifest lists 122 exact Java source files with hashes.
The successful build compiled 112 business source files and one isolated bootstrap source.
All 11 current migration files ran unchanged against disposable PostgreSQL 18.4.
Evidence: [migration hashes](attempt-06/migration-manifest.json) and [migration execution](attempt-06/migration-execution.json).

The build uses current authentication controllers, RSA signing, RSA verification, session repositories, and administration services.
It also uses current catalog filtering, JPA persistence, and audit repositories.
Synthetic local identities replace external OUD, MFA, and Entra services.
Controlled EMS2 responses replace the external entitlement provider.
Analytics uses a local callback with optional declared failures.
The external EMS3 adapter remains disabled.

An isolated Spring Boot 3 bootstrap replaces the production Boot 4 configuration and private starter wiring.
Jackson creator mixins adapt current Drawer and FilterRule constructors for this isolated runtime.
The business DTO source bytes remain unchanged.
Evidence: [bootstrap source](attempt-06/LocalSessionApplication.java) and [build manifest](attempt-06/source-build-manifest.json).

Earlier attempts remain available, including failed builds and the earlier H2 runtime.
The historical administration smoke result contains stale H2 limit text.
The [readiness correction](readiness.json) identifies that historical limit and selects attempt 06.
The correction preserves the historical result bytes.

The [final runtime snapshot](final-runtime/manifest.json) retains bootstrap files, build files, migration records, and compressed runtime logs.
It also retains 162 compiled class hashes and 120 dependency library hashes.
The [final source check](final-source-validation.json) matches all 122 Java files and 11 migration files to the selected revision.
The snapshot records healthy owned BFF and PostgreSQL processes before shutdown.
These records support provenance for the retained local cases.
The [shutdown record](shutdown.json) verifies process identities before stopping only the owned BFF and disposable PostgreSQL processes.
The [shutdown health check](shutdown-health.json) retains the expected unavailable health endpoint and final compressed logs.

Build success and runtime readiness establish tool availability.
Individual case assertions and retained executions establish only their stated predicates.
ASD review remains pending.
