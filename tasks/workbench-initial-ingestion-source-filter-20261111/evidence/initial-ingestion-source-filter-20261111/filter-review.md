# Existing raw document selection review

Date: 11 November 2026, Asia/Singapore.
Mode: source selection review. Original documents remain unchanged.
Reference: [user follow-up](user-followup.md#exact-user-input).

Criteria: [source selection recommendation](recommendation.md#selection-method).

## Current conclusion

**Filter 24 complete documents from the first intent batch. Retain content from 61 documents.**
Exclusion means omission from this initial intent batch. It does not mean deletion.
Candidate intent still requires reconciliation, authority review, and applicable publication review.

| Decision | Documents | Action |
| --- | ---: | --- |
| Exclude from batch | 12 | Omit unrelated, generic, procedural, or template content. |
| Evidence only | 11 | Keep as supporting evidence outside the intent seed. |
| Hold | 1 | Recover necessary content before deriving intent. |
| Keep selected sections | 55 | Select the listed intent passages and preserve their context. |
| Keep | 6 | Retain substantive intent content with its stated lifecycle limits. |

## Scope and source binding

The registered `portal-document-export` collection points to `evidence/knowledge/sources/confluence/`.
The current collection contains 85 Markdown documents: 437,962 bytes and 6,364 lines.
The 12 `knowledge/llm-wiki/raw/` entries link to curated records. They are not original raw documents.

The source manifest contains 102 historical export records. Seventeen records lack active snapshot paths.
Those 17 records are outside this existing-file denominator. They were not filtered or deleted during this review.
Separate user clarifications remain high-priority references. They are outside the 85-document export denominator.

For authorization conflicts, follow the canonical [entry](../../../knowledge/candidates/security/KT-sdk-and-entitlements.md#current-user-stated-portal-entry-rule), [empty-entity](../../../knowledge/candidates/security/KT-sdk-and-entitlements.md#current-user-stated-empty-entity-rule), and [empty-subject](../../../knowledge/candidates/security/KT-sdk-and-entitlements.md#current-user-stated-empty-subject-rule) rules.
These candidate records link the user clarifications and preserve approval limits.
Original attachments and external destinations were not fetched. Their missing contents cannot supply inferred rules.

Content selection does not establish current deployment, approved policy, execution success, or complete domain coverage.

All reviewed source bytes match their registered hashes in the [source manifest](../../../evidence/knowledge/manifest.yaml).
Manifest SHA-256: `5d95c78cec4a5ad94ee4609be9f8dfc134f52e2c5cf2a1cde5d5aad348341b4a`.
Baseline Git revision: `06cdff7dc`.

The document IDs below refer to this review inventory, sorted by source path.
Each source link opens the complete inspected document. Selection ranges refer to physical lines in that document.
Existing manifest entries retain each original source identity and hash.

## Review method and limits

Each assigned reviewer read each complete source before selecting passages.
Three parallel reviewers classified disjoint source groups. The primary reviewer reconciled decisions and checked source bindings.
The review records relevance separately from intent status and confidence.

Confidence rates the classification evidence. It does not rate policy approval or current applicability.
Every kept passage retains its proposed, historical, or unresolved intent status.
An independent reader located tooling exclusions, tile-authorization sources, the held source, and candidate limits.

That check identified a missing route to controlling clarifications. The canonical links above address it.
Unlisted headings and blank separators do not supply additional claims.
Preserve cited definitions and conditions when deriving knowledge. Do not treat a line selection as an approved standalone rule.

For retained contract examples, derive interface meaning. Avoid copying unrelated implementation code or concrete environment values.
Owner for unresolved source authority and missing attachments: unknown.
Next action: use these selections for a later requested ingestion. Investigate flagged context before asserting settled intent.

## Whole documents to exclude

### D014 — Analytics

Source: [Analytics](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/page.md#L1-L10>).
Source ID: `SRC-confluence-dadced48405f20e9`.
Decision: **EXCLUDE**. Classification confidence: high.

Reason: The page contains generic analytics background and navigation links, without a unique system rule.
Intent status: generic context only.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–10`: Generic rationale and child links can remain navigation outside the initial source seed. |

Limits: Use the linked Design and dashboard documents for actual system semantics.

### D020 — Drafts / Nginx Automated Deployment Solution

Source: [Drafts / Nginx Automated Deployment Solution](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Drafts/Nginx Automated Deployment Solution/page.md#L1-L34>).
Source ID: `SRC-confluence-fb2d031445f0ce89`.
Decision: **EXCLUDE**. Classification confidence: high.

Reason: The proposal concerns source control and deployment automation for proxy configuration, outside the initial business behavior seed.
Intent status: draft engineering process.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–34`: Repository creation, Git workflow, syntax checks, restart, and rollback pipeline design. |

Limits: Preserve this engineering source outside intended business-domain knowledge; it is not deleted.

### D039 — Markets Operations One Release / Markets Operations One Release Calendar / [Template] Markets Operations One Change Request

Source: [Markets Operations One Release / Markets Operations One Release Calendar / [Template] Markets Operations One Change Request](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/[Template] Markets Operations One Change Request/page.md#L1-L26>).
Source ID: `SRC-confluence-e778abfc54b9ad86`.
Decision: **EXCLUDE**. Classification confidence: high.

Reason: This is an unfilled release-request form. Its examples and completion instructions do not specify a concrete system rule.
Intent status: template only.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–26`: Blank request fields, example values, sign-off instructions, and release coordination. |

Limits: The form may remain useful for release work outside the initial behavior knowledge seed.

### D040 — Markets Operations One Release / Markets Operations One Release Calendar

Source: [Markets Operations One Release / Markets Operations One Release Calendar](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/page.md#L1-L54>).
Source ID: `SRC-confluence-52e28e4f07d0d2d3`.
Decision: **EXCLUDE**. Classification confidence: high.

Reason: This page is a release schedule and contact/status tracker. Feature names alone do not define system behavior.
Intent status: planned and historical schedule.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–54`: Release windows, feature-name lists, dates, contacts, status fields, and release-record links. |

Limits: Retain the original for deployment chronology; the schedule does not establish actual deployment.

### D043 — Notification (DRAFT) / POC GraphQL over SSE

Source: [Notification (DRAFT) / POC GraphQL over SSE](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/POC GraphQL over SSE/page.md#L1-L31>).
Source ID: `SRC-confluence-67d4fc246fa5d882`.
Decision: **EXCLUDE**. Classification confidence: high.

Reason: The page is POC clone instructions and demo operation links. It supplies no independent supported product behavior rule.
Intent status: implementation experiment.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–31`: Clone commands, demo video link, and localhost GraphQL operation examples. |

Limits: Keep the original as experiment/reproduction material. The parent notification proposal supplies the behavior intent.

### D044 — Notification (DRAFT) / POC GraphQL over WebSocket

Source: [Notification (DRAFT) / POC GraphQL over WebSocket](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/POC GraphQL over WebSocket/page.md#L1-L35>).
Source ID: `SRC-confluence-56c7f21fccc3b0bc`.
Decision: **EXCLUDE**. Classification confidence: high.

Reason: The page is POC clone instructions and demo operation links. It supplies no independent supported product behavior rule.
Intent status: implementation experiment.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–35`: Clone commands, demo video, Swagger and localhost GraphQL operation links. |

Limits: Keep the original as experiment/reproduction material. The parent notification proposal supplies the behavior intent.

### D045 — Notification (DRAFT) / POC SSE using Spring Boot

Source: [Notification (DRAFT) / POC SSE using Spring Boot](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/POC SSE using Spring Boot/page.md#L1-L25>).
Source ID: `SRC-confluence-4bcf2a04323189a3`.
Decision: **EXCLUDE**. Classification confidence: high.

Reason: The page contains clone instructions, a Swagger link, and unavailable screenshots rather than a behavioral specification.
Intent status: implementation experiment.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–25`: Repository setup, demo entry point, and screenshots. |

Limits: Keep the original as experiment/reproduction material.

### D068 — UI Tech Stack / React Build Tooling Research Report

Source: [UI Tech Stack / React Build Tooling Research Report](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/React Build Tooling Research Report/page.md#L1-L374>).
Source ID: `SRC-confluence-9add083ee29ec24e`.
Decision: **EXCLUDE**. Classification confidence: high.

Reason: The source evaluates developer build tools and recommends tooling migration. It does not define runtime behavior or domain responsibilities for this seed.
Intent status: tooling evaluation.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–374`: Generic bundler comparisons, benchmarks, popularity, and proposed developer-tool migration. |

Limits: Compatibility observations can support a separately scoped build-tool decision. This exclusion does not reject a sourced business-system migration requirement.

### D074 — Microfrontend / Single SPA vs Module Federation vs iFrame

Source: [Microfrontend / Single SPA vs Module Federation vs iFrame](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Single SPA vs Module Federation vs iFrame/page.md#L1-L18>).
Source ID: `SRC-confluence-07b0d31be8c1067a`.
Decision: **EXCLUDE**. Classification confidence: high.

Reason: The table scores generic framework capabilities without selecting a project behavior or documenting an applicable system decision.
Intent status: technical evaluation.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–18`: Generic feature comparison, community assessment, implementation approaches, and scores. |

Limits: Can remain supporting material for a separately scoped architecture decision.

### D082 — UI Library Comparations / Draft / Conceptual Design DRAFT

Source: [UI Library Comparations / Draft / Conceptual Design DRAFT](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/UI Library Comparations/Draft/Conceptual Design DRAFT/page.md#L1-L202>).
Source ID: `SRC-confluence-056ed0bbcd5a9d99`.
Decision: **EXCLUDE**. Classification confidence: high.

Reason: The conceptual design is an unfinished vendor-selection template with placeholders, empty decisions, and unrelated approval links.
Intent status: incomplete template.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–202`: Vendor comparison, unfilled requirements and decision fields, review scaffolding, and unrelated approval references. |

Limits: Recover an applicable completed architecture decision if this selection becomes relevant. The exclusion concerns missing settled system content, not the word draft.

### D083 — UI Library Comparations / Usage of Ant Design

Source: [UI Library Comparations / Usage of Ant Design](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/UI Library Comparations/Usage of Ant Design/page.md#L1-L38>).
Source ID: `SRC-confluence-a33cfbab1c166f45`.
Decision: **EXCLUDE**. Classification confidence: high.

Reason: The page compares generic library components and styling conveniences without specifying application behavior or an adopted contract.
Intent status: technical evaluation.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–38`: Generic form, feedback, and layout component comparisons and absent screenshots. |

Limits: Vendor component capabilities do not establish portal requirements.

### D084 — UI Library Comparations

Source: [UI Library Comparations](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/UI Library Comparations/page.md#L1-L84>).
Source ID: `SRC-confluence-fbd92eb4eb061672`.
Decision: **EXCLUDE**. Classification confidence: high.

Reason: The catalog compares vendor popularity, components, licensing, and bundle sizes. It defines no application rule or settled architecture decision.
Intent status: technical evaluation.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–84`: Vendor comparison catalog, feature tables, licensing, pricing, and benchmark illustrations. |

Limits: Useful only as supporting material if an applicable design decision requires it.

## Whole documents to route to evidence

### D005 — Admin Module / EMS2

Source: [Admin Module / EMS2](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/EMS2/page.md#L1-L43>).
Source ID: `SRC-confluence-d62ea00736506481`.
Decision: **EVIDENCE ONLY**. Classification confidence: high.

Reason: The page records entitlement provisioning artifacts, change tickets, and named admin accounts.
Intent status: deployment and provisioning record.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–43`: Release links, missing entitlement artifacts, and user/account rosters do not define a reusable intended access rule. |

Limits: Recover the referenced security matrix if its actual intended role permissions are needed. The separate User Manual states admin access behavior.

### D006 — Admin Module / Firewall Configurations

Source: [Admin Module / Firewall Configurations](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Firewall Configurations/page.md#L1-L8>).
Source ID: `SRC-confluence-a2f118c6e2e51f3f`.
Decision: **EVIDENCE ONLY**. Classification confidence: high.

Reason: The document lists environment hosts, network addresses, contacts, and connectivity confirmations.
Intent status: operational configuration evidence.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–8`: Machine addresses and contact rosters establish configuration context rather than target behavior. |

Limits: Do not reproduce addresses or personal details in synthesized knowledge.

### D007 — Admin Module / Flywaydb

Source: [Admin Module / Flywaydb](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Flywaydb/page.md#L1-L354>).
Source ID: `SRC-confluence-240f5de7543bd39b`.
Decision: **EVIDENCE ONLY**. Classification confidence: high.

Reason: The document is a configuration, schema migration, privilege, and seeded data dump without explanatory policy.
Intent status: implementation snapshot.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–25`: Runtime and database migration configuration.<br>`lines 27–251`: SQL sequences, tables, indexes, and database grants.<br>`lines 253–354`: Seed data and sequence resets. |

Limits: Do not infer intended rules from SQL constraints or seed values. Table Schema and Screen Draft separately explains intended entities, relationships, and visibility semantics.

### D009 — Admin Module / Throughput Testing in UAT

Source: [Admin Module / Throughput Testing in UAT](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Throughput Testing in UAT/page.md#L1-L44>).
Source ID: `SRC-confluence-2c206b29499e9860`.
Decision: **EVIDENCE ONLY**. Classification confidence: high.

Reason: The page reports usage, test workload, response times, and endpoint observations.
Intent status: reported UAT observation.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–44`: Historical measurements and test setup cannot define intended performance limits. |

Limits: JMeter and result attachments are not available in the retained text.

### D030 — MFE Performance Monitoring

Source: [MFE Performance Monitoring](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/page.md#L1-L41>).
Source ID: `SRC-confluence-bc82047451359851`.
Decision: **EVIDENCE ONLY**. Classification confidence: high.

Reason: The page reports development monitoring snapshots and explains generic HTTP caching.
Intent status: historical development observation.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–41`: Monitoring cadence, development URLs, screenshots, generic status-code explanation, and navigation to the separate cache design. |

Limits: Use the cache strategy document for intended cache semantics. Missing screenshots prevent interpreting the reported monitoring results.

### D053 — Security Testing / Penetration Testing report for SPT001414 – SSI+ BA

Source: [Security Testing / Penetration Testing report for SPT001414 – SSI+ BA](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/Penetration Testing report for SPT001414 – SSI+ BA/page.md#L1-L67>).
Source ID: `SRC-confluence-b94df359373d5ce3`.
Decision: **EVIDENCE ONLY**. Classification confidence: high.

Reason: The report records vulnerability findings and reported fixes. These are conformance observations rather than an authoritative target policy.
Intent status: reported findings and remediation.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–67`: Historical finding table, claimed fixes, screenshots, and a token example belong in protected evidence. |

Limits: Attachments and executions were not inspected. Do not copy the embedded token or personal claims into derived knowledge. A reported correction does not establish current deployment or independent intended policy.

### D054 — Security Testing / WAS Scan Report

Source: [Security Testing / WAS Scan Report](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/WAS Scan Report/page.md#L1-L21>).
Source ID: `SRC-confluence-242a14f0e7b2bb23`.
Decision: **EVIDENCE ONLY**. Classification confidence: high.

Reason: The page contains notifications, claimed fixes, planned deployment dates, and screenshots. It does not define intended behavior.
Intent status: historical remediation status.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–21`: Issue notifications, remediation claims, dates, and screenshot evidence. |

Limits: Finding details are primarily in unavailable images.

### D056 — Security Testing / Web Application Vulnerability Scan - SIA-API-ETASK1837309-01122023

Source: [Security Testing / Web Application Vulnerability Scan - SIA-API-ETASK1837309-01122023](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/Web Application Vulnerability Scan - SIA-API-ETASK1837309-01122023/page.md#L1-L18>).
Source ID: `SRC-confluence-b14fb2488c6576e6`.
Decision: **EVIDENCE ONLY**. Classification confidence: high.

Reason: The page reports vulnerability fixes and a planned UAT deployment date. It supplies no independent target behavior specification.
Intent status: historical remediation status.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–18`: Vulnerability status table, fix/deployment claims, and screenshots. |

Limits: No execution or actual deployment evidence was inspected.

### D057 — Security Testing

Source: [Security Testing](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/page.md#L1-L7>).
Source ID: `SRC-confluence-3fcada5a9e0b0c13`.
Decision: **EVIDENCE ONLY**. Classification confidence: high.

Reason: This is an index of historical security reports and their attachments rather than intended behavior.
Intent status: historical report index.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–7`: Report dates, attachment links, and status-page references. |

Limits: Keep the original for evidence navigation; linked reports are not approved policy.

### D061 — Single UI SDK / Single UI SDK V1.1.4 / Java 17 / Migration to Boot 4.0.6

Source: [Single UI SDK / Single UI SDK V1.1.4 / Java 17 / Migration to Boot 4.0.6](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/Migration to Boot 4.0.6/page.md#L1-L28>).
Source ID: `SRC-confluence-42d3b5d3262172da`.
Decision: **EVIDENCE ONLY**. Classification confidence: high.

Reason: Build branch, package versions, and code-change notes describe SDK maintenance rather than intended system behavior.
Intent status: implementation and release status.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–28`: Snapshot package, dependency versions, and implementation change log. |

Limits: Linked changes were not inspected. No behavioral contract is defined here.

### D079 — OpenFin / 5. Technical Issue

Source: [OpenFin / 5. Technical Issue](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/5. Technical Issue/page.md#L1-L29>).
Source ID: `SRC-confluence-8760cec11a48cf7a`.
Decision: **EVIDENCE ONLY**. Classification confidence: high.

Reason: The page reports POC library failures and the implementation workaround. Those observations cannot define intended interoperability policy.
Intent status: reported POC behavior.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–29`: Library versions, reported broadcast and intent results, and POC workaround. |

Limits: Screenshots and execution evidence are absent. The limitations can inform an independent conformance or compatibility investigation.

## Documents on hold

### D001 — MOM

Source: [MOM](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/MOM/page.md#L1-L21>).
Source ID: `SRC-confluence-3c832f99b39e4459`.
Decision: **HOLD**. Classification confidence: high.

Reason: The page indexes meeting attachments but contains no meeting decisions or behavior rules.
Intent status: unavailable.

| Selection | Exact source passages |
| --- | --- |
| Keep | None selected. |
| Filter from intent seed | `lines 1–21`: No substantive meeting payload is available in the page. |

Limits: Recover relevant meeting attachments before classifying their actual content.

## Documents to keep in selected sections

### D002 — Admin Module / Admin Module Release Flow / Admin Module Release Checklist Template / Reference of FMAA API

Source: [Admin Module / Admin Module Release Flow / Admin Module Release Checklist Template / Reference of FMAA API](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/Reference of FMAA API/page.md#L1-L54>).
Source ID: `SRC-confluence-18a7c3158f515b93`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Authentication contracts and token validity rules are mixed with environment addresses, contacts, and account setup.
Intent status: documented historical contract; applicability unresolved.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 11–14`: Client credentials, validation inputs, optional owner validation, success and failure contracts.<br>`lines 24–30`: Separate documented validity for service-account and person tokens.<br>`line 50`: Directory manages accounts; authentication service authenticates those accounts. |
| Filter from intent seed | `lines 3–9`: Environment endpoint and certificate address inventory.<br>`lines 16–22`: Contact directory.<br>`lines 34–49`: Account provisioning tickets, templates, and operational instructions.<br>`lines 52–54`: Password-reset location and empty formatting. |

Limits: Line 13 mixes contract semantics with token samples and command examples. Synthesize only semantics; do not copy samples. Original contract authority and present applicability remain unresolved.

### D003 — Admin Module / Admin Module Release Flow / Admin Module Release Checklist Template

Source: [Admin Module / Admin Module Release Flow / Admin Module Release Checklist Template](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/Admin Module Release Checklist Template/page.md#L1-L29>).
Source ID: `SRC-confluence-b66d4b9435fe7aee`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: A release checklist contains explicit admin workflow, authentication, entitlement, and availability responsibilities.
Intent status: unfinished checklist; candidate intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 9–10`: Module/category/tile configuration and separate maker-checker accounts; deactivation replaces deletion.<br>`lines 12–13`: Shared UI request client, backend JWT validation, and expected tile usability.<br>`lines 16–18`: Account identity constraint and entitled versus unentitled tile visibility.<br>`lines 19–20`: Shared theme requirement and upstream responsibility for disaster recovery. |
| Filter from intent seed | `lines 1–8`: Construction notice, prioritization, and project setup.<br>`line 11`: Proxy configuration code sample.<br>`lines 14–15`: Configuration handoff and performance-test input collection.<br>`lines 21–29`: Release coordination, signoffs, contact procedures, connectivity probes, and completion tracking. |

Limits: Several retained rows mix behavioral requirements with process details and personal examples. Retain only their stated behavioral clauses. Checklist status does not establish completed checks or accepted policy.

### D004 — Admin Module / Admin Module Release Flow

Source: [Admin Module / Admin Module Release Flow](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Admin Module Release Flow/page.md#L1-L57>).
Source ID: `SRC-confluence-ee35de9e44fb891d`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Configuration promotion defines exports, upload authentication, and service processing alongside repository and pipeline operations.
Intent status: documented procedure; applicability unresolved.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 5–10`: Tenant configuration responsibilities and CSV export of module maps, categories, and tiles.<br>`line 15`: Configuration upload contract requires an authentication token.<br>`lines 17–24`: Upload connectivity prerequisite, service account token flow, and validation before CSV processing. |
| Filter from intent seed | `lines 11–14`: Screenshot references and repository preparation.<br>`line 16`: Environment address inventory.<br>`lines 26–57`: Service-account roster, example repository downloads, and one-time release execution details. |

Limits: Preserve upload semantics without copying account identifiers, credential examples, or environment addresses.

### D011 — Admin Module

Source: [Admin Module](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md#L1-L67>).
Source ID: `SRC-confluence-b00dbf78a7ccc381`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The page records self-service administration and role-isolation design, then includes runtime configuration.
Intent status: proposed design with unresolved historical applicability.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 7–37`: Problem, self-service target, team-specific role choices, single-role constraint, and owning service decision. |
| Filter from intent seed | `lines 1–5`: Historical implementation observation and screenshots.<br>`lines 39–67`: Database and framework configuration example. |

Limits: Retain rejected alternatives and draft labels; do not merge historical role proposals into accepted policy.

### D012 — Analytics / Analytic Dashboard in Kibana

Source: [Analytics / Analytic Dashboard in Kibana](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Analytic Dashboard in Kibana/page.md#L1-L105>).
Source ID: `SRC-confluence-9999ec8f5ad884f4`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The dashboard guide describes meaningful event measures alongside environment addresses and screenshots.
Intent status: documented dashboard behavior; applicability unresolved.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 15–25`: Analytics purpose and authentication lifecycle measures.<br>`lines 29–33`: Authentication errors and trace correlation.<br>`lines 37–41`: Tile opening counts and downloadable event data.<br>`lines 47–51`: Workspace interaction counts.<br>`lines 57–61`: Workspace addition and removal measures.<br>`lines 67–71`: Find/new tile action measures.<br>`lines 77–81`: Session extension/logout action measures.<br>`lines 87–91`: Authentication entry action measures.<br>`lines 97–101`: Theme switching measures. |
| Filter from intent seed | `lines 1–13`: Environment endpoint list.<br>`line 27`: Unavailable screenshot.<br>`line 35`: Unavailable screenshot.<br>`lines 43–45`: Unavailable screenshots.<br>`lines 53–55`: Unavailable screenshots.<br>`lines 63–65`: Unavailable screenshots.<br>`lines 73–75`: Unavailable screenshots.<br>`lines 83–85`: Unavailable screenshots.<br>`lines 93–95`: Unavailable screenshots.<br>`lines 103–105`: Unavailable screenshots. |

Limits: The guide describes expected dashboard functions but does not establish measured adoption or current deployment.

### D013 — Analytics / Design

Source: [Analytics / Design](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L1-L241>).
Source ID: `SRC-confluence-81159a8ca38f6bb6`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Analytics design defines events, identity, payload fields, and capture intent, mixed with implementation examples.
Intent status: documented design; conflicting attribute limits.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–115`: Event scope, component identity, custom attributes, and payload design.<br>`line 222`: Event submission integration contract.<br>`lines 226–228`: User network address capture intent. |
| Filter from intent seed | `lines 117–220`: React hook implementation and usage screenshot.<br>`line 224`: Unavailable request screenshot.<br>`lines 230–241`: Implementation algorithm for extracting the network address. |

Limits: Attribute count differs between the first model, later model, and prose. Preserve the conflict; do not choose a final limit. Code examples support design context but cannot establish deployed behavior.

### D015 — Development Principle - Development Guideline - Onboarding Process / Backend Onboarding Process

Source: [Development Principle - Development Guideline - Onboarding Process / Backend Onboarding Process](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Backend Onboarding Process/page.md#L1-L7>).
Source ID: `SRC-confluence-c18459fa7da0c2d0`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Onboarding guidance contains routing responsibilities, domain capability mappings, and backend authentication obligations.
Intent status: documented integration intent; historical mappings.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–3`: Proxy responsibility, required entitlement metadata, application purposes, and integration mapping meanings.<br>`lines 5–6`: Every API call carries a JWT; backend services validate it and obtain entitlement data. |
| Filter from intent seed | `line 7`: Progress notice about unfinished features. |

Limits: Lines 1-3 mix relevant clauses with personal contacts, environment locations, and sample payloads. Retain only semantics. Application mappings are historical declarations rather than current deployment proof.

### D016 — Development Principle - Development Guideline - Onboarding Process / Creating EMS2 Entity Role Subject Action

Source: [Development Principle - Development Guideline - Onboarding Process / Creating EMS2 Entity Role Subject Action](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Creating EMS2 Entity Role Subject Action/page.md#L1-L12>).
Source ID: `SRC-confluence-28cdb4d019a0804d`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The administrative walkthrough supplies entitlement provisioning concepts and role-subject action assignment.
Intent status: documented workflow; external system procedure.

| Selection | Exact source passages |
| --- | --- |
| Keep | `line 1`: Entity, role, subject, action, and user provisioning scope.<br>`lines 6–12`: Creation and assignment relationships for entitlement entities, roles, subjects, and actions. |
| Filter from intent seed | `lines 3–5`: Environment login and basic tool navigation. |

Limits: Missing screenshots limit detailed field and matrix interpretation. Do not treat these tool steps as the portal access policy.

### D017 — Development Principle - Development Guideline - Onboarding Process / Development Guideline

Source: [Development Principle - Development Guideline - Onboarding Process / Development Guideline](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Guideline/page.md#L1-L15>).
Source ID: `SRC-confluence-983d97409a60059d`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Most content prescribes coding style, but some clauses define resilience and shared UI responsibilities.
Intent status: development guidance; candidate architecture intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `line 5`: Component fault containment requirement.<br>`line 7`: Lazy loading design preference for tiles.<br>`line 9`: Base container supplies shared theme configuration and consistent user experience. |
| Filter from intent seed | `lines 1–4`: Language, library version, component style, and folder organization.<br>`line 6`: State library selection.<br>`line 8`: Memoization implementation preference.<br>`lines 10–15`: Styling implementation, file separation, formatting, unit-test workflow, and local development setup. |

Limits: Fault containment and lazy loading need more precise observable outcomes before acceptance criteria can be derived.

### D018 — Development Principle - Development Guideline - Onboarding Process / Development Principle

Source: [Development Principle - Development Guideline - Onboarding Process / Development Principle](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Principle/page.md#L1-L10>).
Source ID: `SRC-confluence-9ef406b86b8aef57`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: System authentication and availability responsibilities are mixed with repository permissions and template instructions.
Intent status: documented architecture intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 2–6`: JWT request contract, validation responsibility, deployment interface inputs, and shared versus tenant availability ownership. |
| Filter from intent seed | `line 1`: Unavailable design image without textual meaning.<br>`lines 7–10`: Template cloning and development repository access controls. |

Limits: Diagrams are unavailable. Role declarations do not prove current named owners or runtime topology.

### D019 — Development Principle - Development Guideline - Onboarding Process / Frontend Onboarding Process

Source: [Development Principle - Development Guideline - Onboarding Process / Frontend Onboarding Process](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Frontend Onboarding Process/page.md#L1-L15>).
Source ID: `SRC-confluence-679e2511e5add4e0`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: A setup sequence also states tile-to-workspace behavior, integration inputs, and optional performance targets.
Intent status: onboarding guidance; optional targets.

| Selection | Exact source passages |
| --- | --- |
| Keep | `line 12`: Configured tiles appear in the drawer and open in workspaces.<br>`lines 14–15`: Static/API integration inputs and optional static file size/concurrency constraints. |
| Filter from intent seed | `lines 1–11`: Repository access, template editing, build setup, unit-test updates, and local import map procedures.<br>`line 13`: Build pipeline creation. |

Limits: Optional loading targets are proposals, not mandatory approved limits. The detailed setup images are unavailable.

### D021 — Drafts / The Proxy Config of Nginx Operation Standard Step

Source: [Drafts / The Proxy Config of Nginx Operation Standard Step](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Drafts/The Proxy Config of Nginx Operation Standard Step/page.md#L1-L61>).
Source ID: `SRC-confluence-ddf874559c9dd5d6`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The template defines routing, request rewriting, timeout, and body-limit semantics alongside operations workflow.
Intent status: draft configuration design.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 3–20`: Upstream/proxy configuration meanings, supported protocols, rewrite semantics, timeout behavior, and body limit.<br>`lines 33–46`: Tenant-supplied routing and connection contract fields. |
| Filter from intent seed | `lines 22–32`: Configuration form download, email handoff, contact and environment fields.<br>`lines 48–61`: Repository and deployment procedure proposals. |

Limits: Retain configuration field meanings rather than copying executable proxy examples or tenant addresses. Template example values do not establish effective production settings.

### D022 — Entra Migration / Post Trade Portal & RATAN Entra Migration - Phase 2 - service account

Source: [Entra Migration / Post Trade Portal & RATAN Entra Migration - Phase 2 - service account](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal & RATAN Entra Migration - Phase 2 - service account/page.md#L1-L32>).
Source ID: `SRC-confluence-0eff33df483d623a`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The migration note separates token requestor/provider roles, but the rest is account inventory and incomplete rollout tracking.
Intent status: unfinalized migration intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–10`: Proposed service-account migration scope, token request/validation roles, and unresolved replacement decision. |
| Filter from intent seed | `lines 12–32`: Account roster, individual integration observations, unresolved usage entries, and rollout status. |

Limits: The source explicitly states the central replacement was not finalized. It cannot establish a completed migration design.

### D023 — Entra Migration / Post Trade Portal Entra Migration - Phase 1 - UI SSO / Entra SSO Non Prod Verification

Source: [Entra Migration / Post Trade Portal Entra Migration - Phase 1 - UI SSO / Entra SSO Non Prod Verification](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Non Prod Verification/page.md#L1-L126>).
Source ID: `SRC-confluence-e1df32b125d53b00`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The verification guide contains authentication prerequisites, expected profile data, login flow, and access-denial rules.
Intent status: documented guide; candidate expected behavior.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 22–31`: Authenticator registration and non-production group prerequisite.<br>`lines 39–42`: Expected login, profile attributes, and tile visibility.<br>`lines 58–103`: SSO redirect, supported non-production account flow, MFA, and return checks.<br>`lines 107–126`: No-entitlement denial and authentication prerequisite/error handling. |
| Filter from intent seed | `lines 1–20`: Account setup links and environment access instructions.<br>`lines 35–37`: Signoff request procedure.<br>`lines 44–56`: Named test users and reported signoff results. |

Limits: Remove personal examples and account identifiers when deriving the workflow. Signoff rows do not prove current behavior; missing screenshots cannot supply additional assertions.

### D024 — Entra Migration / Post Trade Portal Entra Migration - Phase 1 - UI SSO / Entra SSO Prod Guide

Source: [Entra Migration / Post Trade Portal Entra Migration - Phase 1 - UI SSO / Entra SSO Prod Guide](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md#L1-L134>).
Source ID: `SRC-confluence-96093bfd320dfc80`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The guide defines login/fallback behavior and profile contract changes alongside rollout calendars, token samples, and user rosters.
Intent status: pilot guide; historical migration intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–34`: Pilot applicability, MFA, SSO reuse, return flow, and documented authentication session expectation.<br>`lines 40–46`: Phase-specific default and fallback entry behavior; retain phase conditions, not schedule claims.<br>`lines 48–70`: Profile field meaning changes, missing values, and authorization caution.<br>`lines 95–101`: Documented pilot feature-switch persistence expectation. |
| Filter from intent seed | `line 38`: Calendar heading.<br>`lines 72–93`: Consumer code probe and production response examples with personal data.<br>`lines 103–134`: Pilot user rosters, contact data, and signoff tracking. |

Limits: Line 44 says the pilot entry must be revisited after restart; line 101 says no further flag is required. Hold the persistence rule pending reconciliation. Retain profile contract semantics without personal sample values.

### D025 — Entra Migration / Post Trade Portal Entra Migration - Phase 1 - UI SSO / UI SSO Entra Design

Source: [Entra Migration / Post Trade Portal Entra Migration - Phase 1 - UI SSO / UI SSO Entra Design](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/UI SSO Entra Design/page.md#L1-L68>).
Source ID: `SRC-confluence-e33c72473f01c65d`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The design states target login routing, compatibility, service responsibilities, token exchange, and security assumptions.
Intent status: documented target design.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 9–68`: Dual authentication paths, phase behavior, login contracts, component responsibilities, exchange flow, compatibility, and assumptions. |
| Filter from intent seed | `lines 1–7`: Background link and historical implementation summary. |

Limits: Retain pilot phase semantics without copying environment addresses. Stated assumptions and target design do not establish actual token claims or deployment.

### D026 — Entra Migration / Post Trade Portal Entra Migration - Phase 1 - UI SSO

Source: [Entra Migration / Post Trade Portal Entra Migration - Phase 1 - UI SSO](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/page.md#L1-L59>).
Source ID: `SRC-confluence-da70843b431b10aa`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The migration brief defines scope and target SSO behavior, mixed with historical flows and delivery schedules.
Intent status: migration target and historical proposal.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 11–21`: Phase scope, intended migration targets, preserved session behavior, and excluded systems.<br>`lines 35–46`: Target Entra authentication user journey.<br>`lines 48–57`: Phased default/fallback behavior and transition conditions. |
| Filter from intent seed | `lines 1–9`: External announcement, decommission schedule, and onboarding reference.<br>`lines 25–33`: Old authentication journey and screenshot.<br>`line 59`: Empty FAQ heading. |

Limits: Keep old journey as supporting comparison evidence when needed. It is excluded only from the target behavior seed. Schedule estimates and transition criteria do not prove completed rollout.

### D027 — Interoperability Guide

Source: [Interoperability Guide](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Interoperability Guide/page.md#L1-L64>).
Source ID: `SRC-confluence-1ac32c4f6f361a1f`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The guide defines intent navigation, portal mediation, context transfer, authorization, and provider responsibilities.
Intent status: documented intended contract.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–9`: Intent navigation opens a target tile with supplied initial context and transitions the screen.<br>`lines 27–38`: Caller, portal, and provider responsibilities; routing, access control, context handling, and optional results.<br>`lines 44–49`: Registration, handler, agreed context contract, and authorization prerequisites. |
| Filter from intent seed | `lines 11–25`: Unavailable image and empty developer code blocks.<br>`lines 40–42`: Team delivery timing dependency.<br>`lines 50–64`: Testing/release coordination, leadership messaging, and unavailable live-case image. |

Limits: Diagrams and examples are unavailable. No completed implementation follows from this design.

### D028 — MFE Performance Monitoring / FMO Post Trade Portal Frontend Performance Testing May 2023

Source: [MFE Performance Monitoring / FMO Post Trade Portal Frontend Performance Testing May 2023](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L1-L306>).
Source ID: `SRC-confluence-1d352a14219127a5`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The test document contains draft NFR targets and intended journeys, mixed with environment inventory and historical results.
Intent status: historical draft NFR and test intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 48–58`: Single portal purpose, architecture goal, and named user capabilities.<br>`lines 68–89`: Draft availability, latency, capacity, security, compatibility, resource targets, and workload assumptions.<br>`lines 188–201`: Expected portal entry and blotter opening journeys. |
| Filter from intent seed | `lines 1–47`: Document history, uncompleted signoff metadata, and test-plan boilerplate.<br>`lines 62–66`: Template authoring instructions.<br>`lines 91–186`: Test environment inventory, test risks, assumptions, scope boilerplate, and process details.<br>`lines 203–306`: Tooling, execution checklist, screenshots, and reported historical test results. |

Limits: Status is Draft, last edited in May 2023. No attached signoff date establishes approved current NFRs. Keep the current source status and measurement units with each candidate target. Missing result captures cannot verify present performance.

### D031 — MFE Session Control and Implement Refresh Token / MFE Session Control and Implement Refresh Token Version 0

Source: [MFE Session Control and Implement Refresh Token / MFE Session Control and Implement Refresh Token Version 0](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 0/page.md#L1-L73>).
Source ID: `SRC-confluence-9d7082836f5b7097`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain historical session requirements and proposed token lifecycle. Omit generic token-safety assertion and reference-only attachments.
Intent status: historical requirements and proposed design.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–9`: Session duration, expiry notification, renewal, token reuse denial, and one-device requirements.<br>`lines 15–24`: Proposed token purposes and lifetimes.<br>`lines 30–65`: Idle warning, expiry recovery, active renewal, token replacement, and forced logout flow. |
| Filter from intent seed | `lines 26–28`: Generic absolute HTTPS safety claim does not establish the intended system guarantee.<br>`lines 67–73`: External reference and missing image do not supply additional inspected rule text. |

Limits: Absolute-timeout and force-logout durations differ within this source. Later designs and user clarifications must determine applicable policy. Referenced diagrams and screenshots are unavailable.

### D032 — MFE Session Control and Implement Refresh Token / MFE Session Control and Implement Refresh Token Version 1

Source: [MFE Session Control and Implement Refresh Token / MFE Session Control and Implement Refresh Token Version 1](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md#L1-L193>).
Source ID: `SRC-confluence-aa082f0221001faa`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain session problem statements and proposed recovery behavior. Exclude generic JWT teaching and historical execution results.
Intent status: historical proposal with internal conflicts.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–14`: Security classification and user-session-only scope.<br>`lines 102–171`: Idle and absolute timeout logic, recovery proposal, and explicitly deferred single-device and blacklist requirements. |
| Filter from intent seed | `lines 16–100`: Generic JWT and OpenID tutorial material is outside the initial domain seed.<br>`lines 173–193`: Historical timing and screenshot results are observed execution evidence. |

Limits: Refresh-token lifespan arithmetic conflicts within line 136. The absolute-timeout proposal needs reconciliation with predecessor and later user intent. Referenced figures are unavailable.

### D033 — Markets Operations One Release / Markets Operation One TODO List

Source: [Markets Operations One Release / Markets Operation One TODO List](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operation One TODO List/page.md#L1-L4>).
Source ID: `SRC-confluence-f774511fb331e805`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain the proposed removal of account/password login. Defer platform maintenance items.
Intent status: unapproved backlog proposal.

| Selection | Exact source passages |
| --- | --- |
| Keep | `line 4`: Proposed removal of account/password login. |
| Filter from intent seed | `lines 1–3`: Monitoring, runtime upgrade, and properties migration are maintenance backlog items. |

Limits: The remaining login methods, environment, effective date, and owner are not specified.

### D034 — Markets Operations One Release / Markets Operations One Release Calendar / FSS DS Cash Projection Change Request

Source: [Markets Operations One Release / Markets Operations One Release Calendar / FSS DS Cash Projection Change Request](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSS DS Cash Projection Change Request/page.md#L1-L22>).
Source ID: `SRC-confluence-2b6a7579eb0aa485`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain the requested tile purpose and aggregate target workload. Exclude release administration and named user assignments.
Intent status: requested capability, not accepted availability.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 9–10`: Cash Projection is requested as a rule-engine tile for an existing interface.<br>`line 17`: Requested aggregate user and concurrency counts. |
| Filter from intent seed | `lines 1–8`: Form instructions and team metadata.<br>`lines 11–16`: Story, sign-off, connectivity and change-file links, and individually assigned entitlement examples.<br>`lines 18–22`: Release dates, named UVT users, owners, and support contacts. |

Limits: The page gives a capability label without detailed calculation or rule-engine semantics. Requested user counts do not prove performance or actual usage. Entitlement semantics need a separate authoritative source; individual assignments are excluded.

### D035 — Markets Operations One Release / Markets Operations One Release Calendar / FSS Gating, SSI, CA Domestic and Gold Custody Change Request

Source: [Markets Operations One Release / Markets Operations One Release Calendar / FSS Gating, SSI, CA Domestic and Gold Custody Change Request](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSS Gating, SSI, CA Domestic and Gold Custody Change Request/page.md#L1-L23>).
Source ID: `SRC-confluence-3a003ae27635efe6`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain tenant business functions, requested role profiles, and aggregate workload. Exclude release logistics and personal examples.
Intent status: requested capability and access profiles.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 9–10`: Requested gating, settlement instruction, domestic disbursement, gold custody, and collateral functions.<br>`lines 17–18`: Requested application role profiles and aggregate user/concurrency scope. |
| Filter from intent seed | `lines 1–8`: Form instructions and administrative metadata.<br>`lines 11–16`: Work item, sign-off, change-file, and connectivity references.<br>`lines 19–23`: Go-live date, named test users, personal identifiers, and support contacts. |

Limits: Role labels do not define operation-level permissions. Business thresholds and acceptance criteria remain incomplete. Requested dates and capacity are not deployed or executed outcomes.

### D036 — Markets Operations One Release / Markets Operations One Release Calendar / FSSDS Data Distribution and Reporting (DDR)

Source: [Markets Operations One Release / Markets Operations One Release Calendar / FSSDS Data Distribution and Reporting (DDR)](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/FSSDS Data Distribution and Reporting (DDR)/page.md#L1-L23>).
Source ID: `SRC-confluence-6d8fbe96063de05e`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain reporting purpose, container placement, requested access profiles, and workload. Exclude sign-off and release coordination.
Intent status: requested capability and access profiles.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 3–5`: Reporting tile placement and visibility of upstream-to-downstream reports.<br>`lines 14–15`: Requested country/entity role profiles and aggregate concurrency scope. |
| Filter from intent seed | `lines 6–13`: Approval, release work, sign-off, change-file, and firewall coordination.<br>`lines 16–23`: Go-live dates, named UVT users, personal contacts, and release staffing. |

Limits: Role lists do not establish granular permission meanings. Detailed report behavior and current availability remain unconfirmed.

### D037 — Markets Operations One Release / Markets Operations One Release Calendar / Markets Operation One Change Request - CDUPS

Source: [Markets Operations One Release / Markets Operations One Release Calendar / Markets Operation One Change Request - CDUPS](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/Markets Operation One Change Request - CDUPS/page.md#L1-L24>).
Source ID: `SRC-confluence-f80b3b056fa6e915`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain the requested inbound and outbound confirmation management purpose. Exclude incomplete release administration.
Intent status: requested capability.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 9–10`: New confirmation interface with outbound and inbound document-management blotters. |
| Filter from intent seed | `lines 1–8`: Form instructions and team metadata.<br>`lines 11–24`: Approval and implementation references, sign-off placeholders, release dates, staffing, and missing user profiles. |

Limits: The page supplies no detailed confirmation lifecycle or finalized permission rules.

### D038 — Markets Operations One Release / Markets Operations One Release Calendar / VPA Fix-link and Monitor Change Request

Source: [Markets Operations One Release / Markets Operations One Release Calendar / VPA Fix-link and Monitor Change Request](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/Markets Operations One Release Calendar/VPA Fix-link and Monitor Change Request/page.md#L1-L25>).
Source ID: `SRC-confluence-6398bcca1924ede9`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain link-repair and trade-monitor purposes. Exclude deployment evidence and release coordination.
Intent status: requested capability.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 9–10`: Link repair allows trade processing to continue; monitoring exposes trade status and source/transformed files. |
| Filter from intent seed | `lines 1–8`: Form instructions and team metadata.<br>`lines 11–25`: Approval links, changes, connectivity, struck-out profiles, release dates, staffing and personal contacts. |

Limits: Screenshots and linked detailed designs were not retrieved. The source gives purpose without operation-level acceptance criteria.

### D041 — Markets Operations One Release

Source: [Markets Operations One Release](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L1-L199>).
Source ID: `SRC-confluence-67c7f661478adbd1`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain the Portal/tenant responsibility boundary. Defer calendar, staffing, approval, and release-window policy.
Intent status: proposed operating policy with responsibility statements.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 25–40`: Portal change scope and tenant ownership boundary.<br>`line 171`: Portal owns route enabling and routing configuration; tenant teams own their application stack. |
| Filter from intent seed | `lines 1–24`: Release-window frequency, timing, and publication schedule.<br>`lines 44–169`: Cut-offs, readiness administration, staffing, approval, freeze, and failed-release scheduling.<br>`lines 175–199`: Calendar layout and stakeholder contact roster. |

Limits: The responsibility statements do not prove the deployed architecture. Conflicting release durations remain in the preserved original and are excluded from this behavior seed.

### D042 — Notification (DRAFT) / Notification Store and React.useEffect

Source: [Notification (DRAFT) / Notification Store and React.useEffect](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Notification Store and React.useEffect/page.md#L1-L84>).
Source ID: `SRC-confluence-2b82ddd7756a87b7`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain proposed notification fields and user/application interaction semantics. Defer implementation scaffolding and example handlers.
Intent status: draft proposal with type conflict.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–13`: Proposed notification identity, payload, read/shown/muted flags, and destination fields.<br>`lines 36–44`: Open a related record in a tile and react to a notification payload.<br>`line 61`: Applications may register callbacks for new notifications. |
| Filter from intent seed | `lines 15–34`: General root-model implementation structure is not a notification behavior rule.<br>`lines 46–59`: Example React integration code.<br>`lines 63–84`: Example event parsing and callback implementation. |

Limits: The declared read-flag type conflicts with the handler example. UI screenshots are missing. Contract details remain proposed and must not be represented as a supported API.

### D046 — Notification (DRAFT) / Table Schema

Source: [Notification (DRAFT) / Table Schema](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Table Schema/page.md#L1-L36>).
Source ID: `SRC-confluence-fbc13c95a6b135b8`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain proposed notification entities, relationships, flags, and retention alternatives. Exclude populated example records.
Intent status: draft data model with undecided retention.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–4`: Topic metadata field names and routing/subscription responsibilities.<br>`lines 9–12`: User-to-topic preferences and mute/enabled flags.<br>`lines 18–23`: Notification field names and alternative retention durations.<br>`lines 28–33`: User-notification read/shown state and per-user retention alternatives. |
| Filter from intent seed | `lines 5–7`: Populated demonstration endpoints and topic fixtures.<br>`lines 13–16`: Example user assignments.<br>`lines 24–26`: Example transaction identifiers and payloads.<br>`lines 34–36`: Example user notification state rows. |

Limits: The page lists several retention durations without selecting a rule. Field names alone do not establish types, validation, or ownership.

### D047 — Notification (DRAFT)

Source: [Notification (DRAFT)](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/page.md#L1-L102>).
Source ID: `SRC-confluence-92622c071dea109b`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain the notification problem, intended one-connection constraint, and component relationships. Defer generic transport research and POC logistics.
Intent status: draft objective and design.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 58–74`: Many tile subscriptions motivate a single notification SSE connection per user and lower browser resource use.<br>`lines 76–90`: Proposed transport options and notification component relationships. |
| Filter from intent seed | `lines 1–56`: General GraphQL, WebSocket, SSE, and third-party scaling material is not a Portal guarantee.<br>`lines 92–102`: POC links and an action-item email attachment. |

Limits: The one-connection rule is proposed, not executed or approved. Transport alternatives have empty design sections. The source does not determine multi-tab or multi-device scope.

### D048 — On Boarding Records / SSDR On Board Discussion

Source: [On Boarding Records / SSDR On Board Discussion](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md#L1-L79>).
Source ID: `SRC-confluence-da6235912b334d58`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain recorded entitlement principles, proposed exceptions, and rejected alternatives with their original status. Defer discussion identifiers.
Intent status: historical discussion with accepted/proposed/rejected distinctions unresolved.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 8–20`: Registered-entity/subject principles and proposed multiple-entity plus empty-subject handling.<br>`lines 27–69`: Entitlement provisioning option, struck-out guest alternative, existing entitlement-system boundary, and delegated-authorization option. |
| Filter from intent seed | `lines 1–6`: Reported user-profile concerns describe observed onboarding context.<br>`lines 75–79`: Discussion work-item reference is provenance rather than a behavioral rule. |

Limits: Later explicit user clarifications take priority within their scope. Struck-out guest behavior must remain rejected historical context. The source does not clearly record final selection of every alternative.

### D049 — Portal Design

Source: [Portal Design](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Portal Design/page.md#L1-L13>).
Source ID: `SRC-confluence-8021a1ea944159dc`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain the Portal purpose and named post-trade capability scope. Omit edit placeholder and missing screenshots.
Intent status: draft overview.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 5–7`: Integrated post-trade tools for operations users and the intended activity scope. |
| Filter from intent seed | `lines 1–3`: Editing notice and separator.<br>`lines 9–13`: Snapshot heading and missing screenshot references. |

Limits: Listed capabilities are documented scope, not proof of current availability.

### D050 — Post Trade Portal Capabilities

Source: [Post Trade Portal Capabilities](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Capabilities/page.md#L1-L88>).
Source ID: `SRC-confluence-df490605644100fb`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain user-facing capabilities, control responsibilities, and target integration behavior. Defer developer starter promotion.
Intent status: capability overview with in-progress feature labels.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 3–37`: Unified entry, authentication, themes, and interoperability capability statements with the FDC3 progress qualifier.<br>`lines 47–88`: Admin, analytics, tile/workspace lifecycle, access control, tenant routing, and session capability scope. |
| Filter from intent seed | `lines 41–45`: Boilerplate and developer startup promotion is outside the initial behavior seed. |

Limits: Screenshots are missing. FDC3 is explicitly in progress and must remain proposed. Present-tense capability statements are documented intent/context, not verified runtime behavior.

### D052 — Production Release and Tenant on-boarding Checklist

Source: [Production Release and Tenant on-boarding Checklist](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Production Release and Tenant on-boarding Checklist/page.md#L1-L73>).
Source ID: `SRC-confluence-dbe7d2c41e23d282`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain intended connectivity and tenant routing responsibilities. Defer release procedure, host inventory, and communication details.
Intent status: operational guide with architecture recommendation.

| Selection | Exact source passages |
| --- | --- |
| Keep | `line 1`: Onboarding scope includes new user locations and tenant servers.<br>`lines 30–32`: Business users must reach the Portal login page.<br>`lines 40–42`: Portal servers require connectivity to tenant services.<br>`lines 61–63`: Tenant ingress should use tenant Nginx or a load balancer so tenant teams control backend server changes. |
| Filter from intent seed | `lines 5–28`: Release coordination, contacts, agreements, and security-test execution procedure.<br>`lines 34–38`: Issue-handling email attachments.<br>`lines 44–59`: Machine-specific host/address inventory and diagram.<br>`lines 65–73`: Connectivity request emails and release-flow pointer. |

Limits: Connectivity is a stated requirement, not retained proof of live reachability. The original host inventory remains available for operations outside this initial seed.

### D055 — Security Testing / WAS Scan Report SIA-ETASK1854215- 11282023

Source: [Security Testing / WAS Scan Report SIA-ETASK1854215- 11282023](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Security Testing/WAS Scan Report SIA-ETASK1854215- 11282023/page.md#L1-L125>).
Source ID: `SRC-confluence-d37970a011fbb04f`.
Decision: **KEEP SECTIONS**. Classification confidence: medium.

Reason: Retain the explicit proposed public-static-file accessibility rationale. Keep scan observations and remediation claims in evidence only.
Intent status: uncertain security rationale within a scan response.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 9–12`: The author states that nonsensitive static files should remain accessible without authentication. |
| Filter from intent seed | `lines 1–7`: Vulnerability finding and screenshot fix claim.<br>`lines 13–125`: Finding details, historical remediation, endpoint response observations, headers, scripts, and report attachment. |

Limits: This isolated rationale has unconfirmed authority and must remain candidate intent. The source cannot establish that every static file lacks sensitive data. Reported scan responses must not become target error contracts.

### D058 — Single UI SDK / Single UI SDK V1.0.0

Source: [Single UI SDK / Single UI SDK V1.0.0](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.0.0/page.md#L1-L85>).
Source ID: `SRC-confluence-8149095ebbc4b59c`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain version-specific authentication defaults, request matching, and caller context contract. Defer installation and sample application scaffolding.
Intent status: historical version-specific guidance.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–3`: JWT validation responsibility of the SDK.<br>`lines 34–51`: Include/exclude defaults, timeout configuration meaning, matching precedence, and user context fields.<br>`lines 83–84`: Header-based validation bypass behavior stated in configuration comments. |
| Filter from intent seed | `lines 5–30`: Runtime prerequisites and Maven installation sample.<br>`lines 52–82`: Example controller and sample configuration values. |

Limits: Version 1.0.0 must remain distinct from later contracts. The bypass comment describes a configurable behavior; it does not authorize its use.

### D059 — Single UI SDK / Single UI SDK V1.1.1

Source: [Single UI SDK / Single UI SDK V1.1.1](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.1/page.md#L1-L89>).
Source ID: `SRC-confluence-03b28c3944f9d007`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain version-specific caller contract changes, validation defaults, and context fields. Defer dependency setup and controller examples.
Intent status: historical version-specific guidance.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–12`: SDK role and version-specific removal/rename contract changes.<br>`lines 39–57`: Request matching defaults, precedence, and userInfo/entitlement field meaning.<br>`lines 87–88`: Header-based validation bypass behavior stated in configuration comments. |
| Filter from intent seed | `lines 14–35`: Runtime prerequisites and Maven dependency setup.<br>`lines 59–86`: Example controller and sample configuration values. |

Limits: Version 1.1.1 must remain distinct from predecessor and successor contracts. The bypass example is not a policy approval.

### D060 — Single UI SDK / Single UI SDK V1.1.2

Source: [Single UI SDK / Single UI SDK V1.1.2](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.2/page.md#L1-L53>).
Source ID: `SRC-confluence-a544f218d4ae936f`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Retain version-specific authentication changes, validation defaults, and user context contract. Defer installation snippets and controller code.
Intent status: historical version-specific guidance.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–10`: SDK responsibility, max-age validation addition, and OUD context addition.<br>`lines 27–45`: Include/exclude defaults, matching precedence, and three-part caller userInfo contract.<br>`lines 50–53`: Configuration comment states header-based validation bypass; preserve its meaning without adopting sample values. |
| Filter from intent seed | `lines 12–23`: Runtime prerequisites and dependency installation snippet.<br>`lines 47–48`: Example controller implementation. |

Limits: Version 1.1.2 must remain distinct from later SDK versions. The final table embeds a behavior comment among example configuration; synthesize only the stated semantics.

### D062 — Single UI SDK / Single UI SDK V1.1.4 / Java 17

Source: [Single UI SDK / Single UI SDK V1.1.4 / Java 17](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 17/page.md#L1-L169>).
Source ID: `SRC-confluence-70a0e38be607a8f5`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The SDK guide defines authentication, entitlement, default interception, and request-context contracts alongside installation and code examples.
Intent status: version-specific documented contract.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–16`: SDK validation purpose, entitlement retrieval, logout blacklist, and token extraction responsibilities.<br>`lines 49–59`: Configuration meanings, include/exclude matching, defaults, certificate requirement, and entity scope.<br>`lines 81–86`: Request context fields and entitlement contract reference. |
| Filter from intent seed | `lines 18–45`: Java prerequisites and Maven installation.<br>`lines 61–79`: Environment-specific sample configuration.<br>`lines 88–169`: Example integration implementation. |

Limits: Current version applicability and source authority remain unconfirmed. Linked entitlement contract and absent configuration values need separate review.

### D063 — Single UI SDK / Single UI SDK V1.1.4 / Java 8

Source: [Single UI SDK / Single UI SDK V1.1.4 / Java 8](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/Java 8/page.md#L1-L158>).
Source ID: `SRC-confluence-8a6e20dfee8803c6`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The Java 8 guide repeats useful SDK semantics but mixes them with installation, certificate data, and example code.
Intent status: version-specific documented contract.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–16`: SDK validation purpose, entitlement retrieval, logout blacklist, and token extraction responsibilities.<br>`lines 49–59`: Configuration meanings, include/exclude matching, defaults, certificate requirement, and entity scope.<br>`lines 87–92`: Request context fields and entitlement contract reference. |
| Filter from intent seed | `lines 18–45`: Java prerequisites and Maven installation.<br>`lines 61–85`: Environment-specific configuration and embedded certificate data.<br>`lines 94–158`: Example integration implementation. |

Limits: Current version applicability and source authority remain unconfirmed. Preserve its separate version identity even where Java 17 narrative is similar.

### D064 — Single UI SDK / Single UI SDK V1.1.4

Source: [Single UI SDK / Single UI SDK V1.1.4](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/Single UI SDK V1.1.4/page.md#L1-L58>).
Source ID: `SRC-confluence-efbb5749066ee2a3`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The page distinguishes authentication and entitlement tokens and describes two entitlement retrieval contracts.
Intent status: version-specific documented contract.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 7–14`: Two entitlement retrieval methods and prohibition on using entitlement tokens for login.<br>`lines 16–28`: Direct retrieval uses the request-context user identity derived from the authorization header.<br>`lines 42–54`: Entitlement-token validation and request-body token input. |
| Filter from intent seed | `lines 1–5`: Version navigation.<br>`lines 30–40`: Certificate maintenance instructions and absent setup images.<br>`lines 56–58`: Example result image without retained bytes. |

Limits: Method signatures and examples depend on absent images. Retain only supported prose. Current applicability remains unconfirmed.

### D065 — Single UI SDK

Source: [Single UI SDK](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/page.md#L1-L22>).
Source ID: `SRC-confluence-2a322655d17bc02d`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The parent SDK page combines entitlement compatibility and caching intent with delivery progress.
Intent status: historical migration intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–3`: Direct retrieval obligations, existing entitlement-format compatibility, caching, and session-affinity context.<br>`line 15`: Environment-specific intent to remove entitlement detail from the authentication token. |
| Filter from intent seed | `lines 5–13`: Team confirmations and reported delivery progress.<br>`lines 17–22`: Version navigation. |

Limits: The historical migration date does not prove completed rollout or current applicability.

### D067 — Technical Design and Document / Tile Security Control - EMS2

Source: [Technical Design and Document / Tile Security Control - EMS2](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Technical Design and Document/Tile Security Control - EMS2/page.md#L1-L23>).
Source ID: `SRC-confluence-50f47e97fb28ed59`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The proposed tile authorization model is relevant intent. Its current-workflow description is separate implementation evidence.
Intent status: historical proposed intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 5–23`: Proposed portal-entry eligibility, tile visibility, role configuration, and application-owned data authorization. |
| Filter from intent seed | `lines 1–3`: Reported old workflow rather than intended target behavior. |

Limits: The historical entry and empty-role proposal conflicts with later user clarifications in canonical knowledge. Do not promote the proposal to the current accepted rule.

### D069 — UI Tech Stack

Source: [UI Tech Stack](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/UI Tech Stack/page.md#L1-L73>).
Source ID: `SRC-confluence-a9356812ddc54035`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: Runtime module loading responsibilities are useful architecture context. Most content teaches generic frontend tools.
Intent status: documented architecture context.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 35–51`: Runtime loading model and separation between module resolution and application lifecycle management. |
| Filter from intent seed | `lines 1–33`: Generic React and Redux tutorials.<br>`lines 53–73`: Framework and library catalog with logos rather than behavioral rules. |

Limits: The source does not prove current runtime deployment.

### D070 — Microfrontend / Getting Started with Single-Spa Micro-Frontend

Source: [Microfrontend / Getting Started with Single-Spa Micro-Frontend](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Getting Started with Single-Spa Micro-Frontend/page.md#L1-L69>).
Source ID: `SRC-confluence-09344af4ee937ae7`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The local setup guide contains a small explicit portal user journey worth retaining separately.
Intent status: example behavior intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 65–69`: Login, choose a tile, and add the tile to the workspace in the example journey. |
| Filter from intent seed | `lines 1–63`: Local source archives, package modifications, installation, and startup instructions. |

Limits: Example behavior is not proof of current deployment or policy approval. The screenshots and source archives are absent.

### D071 — Microfrontend / Micro-Frontend Deployment

Source: [Microfrontend / Micro-Frontend Deployment](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Micro-Frontend Deployment/page.md#L1-L77>).
Source ID: `SRC-confluence-41de4cec4b95b17d`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The deployment guide states target artifact delivery and pilot/production dependency boundaries alongside CI and branch procedures.
Intent status: historical proposed architecture.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 3–9`: Frontend artifact responsibility is to serve static resources to clients.<br>`lines 41–51`: Supported clients, blue/green proposal, and shared backend boundary between pilot and production. |
| Filter from intent seed | `lines 11–39`: Build artifacts, repository branches, and developer workflow.<br>`lines 55–77`: Jenkins pipeline stages, approvals, and deployment procedures. |

Limits: Claims about scalability are source assertions, not verified guarantees. Proposed pilot and production architecture needs applicable review.

### D072 — Microfrontend / Micro-frontend

Source: [Microfrontend / Micro-frontend](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Micro-frontend/page.md#L1-L200>).
Source ID: `SRC-confluence-e4e8612b58604bc3`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The essay contains intended module ownership and shared platform responsibilities within substantial generic comparison material.
Intent status: historical architecture intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 111–117`: Documented framework choice and source rationale.<br>`lines 130–157`: Common versus application-owned modules, shared routing and theme responsibilities, and integration boundaries.<br>`lines 177–182`: Domain application ownership and unified workspace with shared sign-on and session management. |
| Filter from intent seed | `lines 1–109`: Generic microservice and frontend comparison, tutorials, and code-sharing examples.<br>`lines 119–128`: Repeated problem list.<br>`lines 159–175`: Development, test, staffing, framework, and branch-model benefit assertions.<br>`lines 184–200`: Implementation diagrams absent from this export. |

Limits: The missing diagrams cannot establish service topology, SSO details, or load balancing. Architecture applicability and approval remain unconfirmed.

### D073 — Microfrontend / Portal New Deployment

Source: [Microfrontend / Portal New Deployment](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/Portal New Deployment/page.md#L1-L75>).
Source ID: `SRC-confluence-f2fa7eec2374e232`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The page contains explicit future capabilities and target service roles alongside unverified measurements and infrastructure sizing.
Intent status: proposed future intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 3–18`: Proposed application scope, cross-tile workflows, telemetry, notification center, and persona dashboard capabilities.<br>`lines 58–70`: Proposed authentication, tile management, telemetry, AI, web delivery, load balancing, and database component roles; use role names only. |
| Filter from intent seed | `line 1`: Empty current-architecture heading.<br>`lines 20–47`: Reported and predicted usage, performance, and user-count changes.<br>`lines 49–56`: Empty target logical architecture section.<br>`lines 71–75`: Infrastructure totals and reported current deployment sizing. |

Limits: The sizing cells in lines 62–70 are excluded from semantic knowledge; only proposed component roles qualify. Capabilities are being refined. No detailed rules or completed approval is supplied.

### D076 — OpenFin / 2. Getting Started

Source: [OpenFin / 2. Getting Started](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/2. Getting Started/page.md#L1-L89>).
Source ID: `SRC-confluence-fa449ec25a5c0b52`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The setup tutorial defines provider, window, and view responsibilities useful for interpreting portal interoperability.
Intent status: technical context for intended integration.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–28`: Desktop-agent context and platform provider, window, and view meanings and responsibilities. |
| Filter from intent seed | `lines 30–89`: Example archives, local setup commands, startup checks, and screenshots. |

Limits: The content partly describes vendor capabilities rather than a project-specific commitment. Retain only context needed by the portal interoperability topic.

### D077 — OpenFin / 3. Application Interoperability

Source: [OpenFin / 3. Application Interoperability](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/3. Application Interoperability/page.md#L1-L73>).
Source ID: `SRC-confluence-10f43dbfd1dc608c`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The POC describes candidate authentication handoff, hidden-provider intent, and cross-application user journeys.
Intent status: POC and proposed production distinction.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–31`: Provider responsibilities, hidden-window production intent, POC exception, authentication handoff, and use-case scope.<br>`lines 41–54`: Open portal in a new view or a tile as a workspace in an existing view.<br>`lines 57–69`: Theme-change and context-broadcast actions in the POC. |
| Filter from intent seed | `lines 33–39`: Demo preparation and absent screenshot.<br>`line 55`: Absent demonstration screenshot.<br>`lines 71–73`: Absent screenshot and next-page navigation. |

Limits: The POC is not current approved behavior or verification evidence. Preserve the distinction between POC application lists and the intended hidden provider.

### D078 — OpenFin / 4. FMO Portal FDC3 Contract

Source: [OpenFin / 4. FMO Portal FDC3 Contract](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/4. FMO Portal FDC3 Contract/page.md#L1-L56>).
Source ID: `SRC-confluence-02d4337e38f91397`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The table defines candidate channels, intents, payloads, and tile-opening semantics. Sample handlers are implementation detail.
Intent status: POC contract intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–11`: Channel and intent contracts, theme and tile payload meanings, and listener separation option. |
| Filter from intent seed | `lines 13–56`: Example handler and view-launch implementation code. |

Limits: The table mixes concrete endpoint examples with contract semantics; omit endpoint values from synthesized knowledge. Current interface version and production adoption remain unconfirmed.

### D080 — OpenFin / Ratan OpenFin Briefing

Source: [OpenFin / Ratan OpenFin Briefing](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/Ratan OpenFin Briefing/page.md#L1-L173>).
Source ID: `SRC-confluence-0ab144bd08f5c7bf`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The briefing mixes intended portal interoperability scope and business cases with vendor information, licensing, contacts, and rollout status.
Intent status: mixed target intent and reported state.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 32–34`: Portal use is limited to rendering and interoperability; other integration capabilities are out of scope.<br>`lines 111–125`: Hidden provider and routing responsibility, and use of standardized intents for interoperability.<br>`lines 147–155`: Business use cases for opening trade details and remaining amounts across applications.<br>`line 161`: Candidate rollout constraint that browser-launched applications must remain unaffected.<br>`lines 165–169`: Documented answer about Entra sign-on support as integration context. |
| Filter from intent seed | `lines 1–30`: Generic vendor description and absent architecture illustrations.<br>`lines 36–109`: Runtime version operations, installation, manifest example, licensing, and cost ownership.<br>`lines 127–145`: Contact directory and reported approval and prioritization status.<br>`lines 157–160`: Release phase table structure.<br>`lines 162–163`: Rollout dates and onboarding schedule.<br>`lines 171–173`: Unresolved desktop-owner implementation status. |

Limits: Business cases link to unavailable details; their titles do not establish acceptance criteria. Licensing and approval statements are historical claims, not independently inspected approvals.

### D081 — ReactJS Standalone Project

Source: [ReactJS Standalone Project](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/ReactJS Standalone Project/page.md#L1-L17>).
Source ID: `SRC-confluence-3300bb0a01b52927`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The template page defines a narrow shared-component loading contract amid local setup instructions.
Intent status: documented example integration intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–5`: Standalone applications can consume shared components through an import map without package installation. |
| Filter from intent seed | `lines 7–17`: Template archive, local install commands, Jest setup, and screenshot. |

Limits: Template archive is absent; the supported module surface is not defined here.

### D085 — page.md

Source: [page.md](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/page.md#L1-L47>).
Source ID: `SRC-confluence-860eba663a146c1c`.
Decision: **KEEP SECTIONS**. Classification confidence: high.

Reason: The guild page explains the shared UI mission and portal relationship, mixed with environment links and onboarding navigation.
Intent status: documented purpose and target responsibilities.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–14`: Purpose, consistent design language, shared component and utility responsibilities.<br>`lines 20–23`: Shared frontend component exposure and base-container responsibility.<br>`lines 31–33`: Relationship between the common UI platform and the post-trade portal. |
| Filter from intent seed | `lines 16–18`: Internal design-system access link.<br>`lines 25–29`: Onboarding navigation.<br>`lines 35–43`: Environment endpoint directory and deployment descriptions.<br>`lines 45–47`: Standalone-project navigation. |

Limits: Organizational mission statements are context, not measurable application acceptance criteria.

## Documents to keep

### D008 — Admin Module / Table Schema and Screen Draft

Source: [Admin Module / Table Schema and Screen Draft](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Table Schema and Screen Draft/page.md#L1-L101>).
Source ID: `SRC-confluence-723fa7583c628c20`.
Decision: **KEEP**. Classification confidence: high.

Reason: The draft defines administration entities, field meanings, relationships, visibility controls, and screen structure.
Intent status: draft design intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–60`: Category, tile, and authorization entities with parent relationships and access-control meanings.<br>`lines 64–101`: Proposed admin screens and access prerequisite. |
| Filter from intent seed | None selected. |

Limits: Referenced diagrams and screenshots are unavailable. Blank form headings supply no missing validation rules. Draft field types and applicability require review before use as an accepted contract.

### D010 — Admin Module / User Manual

Source: [Admin Module / User Manual](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md#L1-L233>).
Source ID: `SRC-confluence-6fb800d3b54f06f7`.
Decision: **KEEP**. Classification confidence: high.

Reason: The user manual defines admin user journeys, maker-checker separation, audit history, validation, and state changes.
Intent status: documented user-facing contract; applicability unresolved.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 3–47`: Admin capabilities, required entitlements, separate maker-checker users, and audit recording.<br>`lines 49–127`: Module creation, naming constraints, verification, deactivation, and history workflow.<br>`lines 131–167`: Category creation and shared lifecycle behavior.<br>`lines 169–233`: Tile fields, path and entity transformations, routing consistency, and shared lifecycle behavior. |
| Filter from intent seed | None selected. |

Limits: Screenshots are unavailable. Use explicit text for behavior, not unseen screen details. Documentation does not establish current execution or publication approval.

### D029 — MFE Performance Monitoring / MFE Cache Strategy

Source: [MFE Performance Monitoring / MFE Cache Strategy](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/MFE Cache Strategy/page.md#L1-L45>).
Source ID: `SRC-confluence-f7f29be1f97cb8b1`.
Decision: **KEEP**. Classification confidence: high.

Reason: The source is a cache design with refresh behavior, explicit limitations, expiry policy, and rationale.
Intent status: proposed design intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–43`: Entry revalidation, cached subsequent assets, update detection, first-load limits, refresh requirement, and cache expiry table. |
| Filter from intent seed | None selected. |

Limits: The quantified benefit is a documented design claim without measurement evidence in this source. The empty Implementation heading supplies no implementation or deployment evidence.

### D051 — Post Trade Portal Principles (Draft)

Source: [Post Trade Portal Principles (Draft)](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Principles (Draft)/page.md#L1-L25>).
Source ID: `SRC-confluence-f5f0ae3ea47acb2b`.
Decision: **KEEP**. Classification confidence: high.

Reason: This draft directly states the platform scope, login eligibility, and tile entitlement rules.
Intent status: draft intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–25`: Platform responsibility scope and required entity/subject conditions for entry and tile access. |
| Filter from intent seed | None selected. |

Limits: Draft authority and scope require review. Later explicit user clarifications take priority; this page cannot override them.

### D066 — Supplementary Principle_ External Frontend Dependency Control

Source: [Supplementary Principle_ External Frontend Dependency Control](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Supplementary Principle_ External Frontend Dependency Control/page.md#L1-L54>).
Source ID: `SRC-confluence-85d7dd2fa8978701`.
Decision: **KEEP**. Classification confidence: high.

Reason: The document defines a concrete runtime security boundary and tenant responsibility for external dependencies.
Intent status: documented policy intent.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 3–54`: Permitted internal packaging and backend encapsulation, exception process, ownership, failure responsibility, and default denial rule. |
| Filter from intent seed | None selected. |

Limits: Formal policy approval and current applicability require review. The leading attachment is not available for inspection.

### D075 — OpenFin / 1. Overview

Source: [OpenFin / 1. Overview](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/OpenFin/1. Overview/page.md#L1-L40>).
Source ID: `SRC-confluence-26c93a0d5679958c`.
Decision: **KEEP**. Classification confidence: high.

Reason: The overview states the portal interoperability objective and the domain meanings of intents and shared context.
Intent status: documented target capability.

| Selection | Exact source passages |
| --- | --- |
| Keep | `lines 1–40`: Application-to-application actions, shared context, desktop agent concepts, and intended interoperability use cases. |
| Filter from intent seed | None selected. |

Limits: Linked specifications were not retrieved. Current adopted versions and approval remain unconfirmed.

## Validation

Classification coverage: 85/85 existing raw documents.
Inspected source hashes and range bounds: PASSED for 85 completed classifications.
Source preservation: PASSED. All 462 baseline raw hashes, 67 audit hashes, and the source manifest remain unchanged.

Manual link checks: PASSED for 91 local links, heading anchors, and source ranges.
Initial harness preparation: PREPARED with no findings. Workspace validation passed.
The harness checked 90 links and 84 line fragments. Manual checks covered the nested template label and heading anchors.

Independent retrieval: PASSED for tooling exclusions, tile-authorization context, missing content, and candidate limits.

ASD-STE100 review: PENDING. No complete dictionary or grammar certification was performed.
Business execution: NOT_RUN. This review makes no passing behavior claim.
