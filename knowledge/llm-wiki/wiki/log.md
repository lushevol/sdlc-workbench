# Operations Log

## [2026-11-11 14:26:03] ingest | KT-sdk-and-entitlements.md

## [2026-11-11 14:27:46] ingest | ARC-portal-service-relationships.md

## [2026-11-11 14:28:36] ingest | KT-frontend-composition.md

## [2026-11-11 14:30:19] ingest | KT-portal-purpose.md

## [2026-11-11 14:31:41] ingest | KT-architecture-evolution.md

## [2026-11-11 14:32:54] ingest | KT-application-interoperability.md

## [2026-11-11 14:33:59] ingest | KT-observability-and-performance.md

## [2026-11-11 14:35:40] ingest | KT-admin-and-onboarding.md

## [2026-11-11 14:37:30] ingest | KT-release-operations.md

## [2026-11-11 14:38:23] ingest | REQ-active-session-renewal.md

## [2026-11-11 14:40:06] ingest | KT-authentication-and-sessions.md

## [2026-11-11 14:41:25] ingest | KT-ces-migration-parity.md

## [2026-11-11 14:42:53] query | What is the candidate target behavior for active session renewal after refresh-token expiry, including manual recovery?

## [2026-11-11 14:44:23] query | How should the candidate CES migration preserve EMS2 permission meaning, and what equivalence limits remain?

## [2026-11-11 14:44:43] query | What are the candidate Portal frontend layers and their ownership boundaries?

## [2026-11-11 14:45:14] query | What responsibilities do Portal and tenant teams have during routing, validation, onboarding, and release?

## [2026-11-11 14:45:38] query | What candidate contract is required for application interoperability and OpenFin context readiness?

## [2026-11-11 14:46:04] query | What do the candidate records say about portal interaction analytics, cache behavior, and performance evidence?

## [2026-11-11 14:48:34] lint | report → lint_20261111_144834.md

## [2026-11-11 14:57:10] query | How should the Portal preserve an active session across refresh-token expiry, and what manual recovery is required after a rejected renewal?

## [2026-11-11 14:57:54] query | What candidate mapping rules map EMS2 roles and entitlements to CES permissions, and what parity limits remain unresolved?

## [2026-11-11 14:58:20] query | What are the Portal frontend composition layers and ownership boundaries among root config, base, container, feature, module, and tile?

## [2026-11-11 14:58:38] query | Which responsibilities belong to Portal and tenant teams for routing, release, validation, and rollback?

## [2026-11-11 14:58:56] query | What candidate interoperability contract and OpenFin/FDC3 context readiness are required between caller and provider applications?

## [2026-11-11 14:59:16] query | What telemetry and performance or capacity evidence exists for portal interactions, cache behavior, and response time, and what remains proposed or missing?

## [2026-11-11 17:06:07] repair | Restore release-window concept

Added `concepts/release-window-governance.md` from canonical candidate/draft `KT-release-operations` version 2 and added its catalog entry. Preserved the unresolved 10-versus-24-hour duration and explicit-confirmation-versus-silence alternatives. The repair supplies the missing target for 14 existing references and does not approve a release rule.

## [2026-11-11 17:06:07] repair | Clarify CES field additions

Clarified active summaries, concepts, and entities against canonical `KT-ces-migration-parity`: `roleList` and `applicationId` are the two new fields; `name` and `applicationName` remain existing fields with the source's clarified meanings. Preserved application scope, scalar-role limits, candidate status, and unchanged EMS2 behavior requirements.

## [2026-11-11 17:06:07] repair | Catalog and navigation boundaries

Removed six obvious self-wikilinks from five concept pages. Added the candidate/draft authority preamble and source-manifest binding link to the catalog. Verified that all six retained exploration pages already have catalog entries with descriptions. Original benchmark material and canonical source content remain unchanged.

Native OpenKB structural functions after these repairs found zero broken wikilinks, index synchronization issues, orphan pages, invalid frontmatter, or missing required OKF fields. These structural checks used the local installation without model-provider calls and do not establish semantic correctness or publication approval.

## [2026-11-11 15:50:35] lint | ADE source-fidelity corrections (F2)

Corrected BFF/SDK responsibility statements in the portal entity and SDK concept, and removed an unsupported HTTP-interceptor dependency from the MFE Base entity. Read the cited canonical responsibility and permission-criterion sections. This was current-agent maintenance, with no external model call or new compilation. All 12 canonical input hashes and source bindings remain unchanged.

## [2026-11-11 16:00:56] lint | ADE source navigation and status notes (F5)

Added source-status notes to all 91 derived pages, direct canonical record/version links to all 12 summaries, and exact canonical sections for seven key concepts. Repaired the empty-subject criterion locator. Native metadata, canonical bytes, source bindings and original compilation identity remain unchanged. This was current-agent maintenance without a provider call.
