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

## [2026-11-11 16:06:47] lint | ADE focused reading routes (F7)

Added focused reading routes to the broad portal entity and ownership concept, merged duplicate related-concept navigation and added the missing release-summary title. All existing content lines and wiki target sets were retained in the four edited pages; all 91 pages and useful single-source topics remain. This improves entry navigation without claiming a smaller semantic corpus. Native structure and source bindings verify.
## [2026-11-12 13:45:11] ingest | OpenKB semantic compilation: KT-settlement-auto-netting.md

## [2026-11-12 22:00:07] ingest | Reviewed portal candidate refresh

Updated 37 derived pages through the current-agent llm-wiki-agent fallback. Reviewed 96 dependent outputs and retained 59 after checking the affected claims and output hashes. Qualified the historical session and telemetry explorations and preserved their original answers.

Verified all 13 linked canonical sources and all six native structural checks. The seven refreshed sources replan as unchanged. Rebuilt the native wiki graph with 89 nodes and 1,468 edges.

Reviewed canonical source SHA-256 values:

- `KT-admin-and-onboarding` `ccdbb0e15f134a8d97981d1fc8b88955b9bd826a7dcef4c3e423ae17b48fa8f9`
- `KT-authentication-and-sessions` `4c21dede2d9031b4994617670806713b1357c35d78f217f41b8d3ed7ba1eaf06`
- `KT-frontend-composition` `700d44d622d5c2cdb8655f1bd096574fee6dd95f5b6909d383efee22ab304668`
- `KT-observability-and-performance` `edd20330c29cfddf534f0836ad529c115cb61e39d9f1d53435f106eb2fc3510d`
- `KT-release-operations` `6abb62a2b36ae98527801d1d81b22b89a353b883de7a52706311573defd33600`
- `KT-sdk-and-entitlements` `dda5236db1f4c742a30af8d04a191aa7ef62352cb722b7f9c1f53323fa403fbe`
- `REQ-active-session-renewal` `7d90d20b35c205940107951497b2b3a48e01d2a8f41bbf573e2ad18250f15779`

The [source manifest](../source-manifest.json) records the reviewed outputs, hashes, and candidate status. RATAN review and canonical publication remain pending.


## [2026-11-12 23:31:20] review | Complete five legacy portal inputs

Reviewed all 96 dependent pages through the current-session llm-wiki-agent workflow. Corrected 33 source-fidelity findings across 31 pages and retained 65 supported unchanged pages. Four newly qualified saved explorations preserve their complete historical body bytes. Two independent correction checks report no unresolved findings.

The bridge recorded reviewed completion for the five unchanged canonical sources below. The exact 12 portal records now replan as unchanged, with no queued portal work. All 13 linked source bindings and six native structural categories verify. Rebuilt the native graph with 89 nodes and 1,467 edges.

Reviewed canonical source SHA-256 values:

- `ARC-portal-service-relationships` `08e3b5a80b6eef6d5c420b0b2be787753d2200b3587c617b83a206bc1e9d3db5`
- `KT-portal-purpose` `29b0432d30bd7ae28dc636bfce8834e7297c9af6cd59e0632bbc9eb57e3ab620`
- `KT-architecture-evolution` `e89f82a3803eb61b562c419e82df1ed29f44c1510d6499aa731821ae08114552`
- `KT-application-interoperability` `6f342b010f7d9a4fa59ccc43456aba67d5ef33aed20f971d9836b4fbc4150d72`
- `KT-ces-migration-parity` `9176c6da48ffd2f9fa7b131f54a982564fd853034cd117b6a68421373c2fc6e0`

[Review evidence](../../../tasks/ui-test-coverage-20261022/evidence/portal-wiki-legacy-review-20261112/completion.json) records the cases and coordinated provenance checks. All 243 protected canonical and evidence files remain unchanged. Source processing has zero queued items; the MOM attachment source remains held. RATAN policy review and publication remain pending. Separate Settlement recipe freshness is outside this portal scope.
