---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
- Automated checks do not check the complete approved dictionary or grammar rules.
- This review covers supplied Markdown text. Attachments, external destinations, and current runtime behavior remain unreviewed.
- Source links require the supplied local export, which remains untracked and outside the review commit.
---

# Markdown import review

The review read all 118 supplied Markdown files under `knowledge/raw/confluence/`.
The files contain 502,757 bytes across 7,698 lines.
Original bytes remain unchanged.

The supplied export remains untracked and outside the review commit.
Source links require that local export.
The raw manifest remains empty because this stage reviews the materials before ingestion.
No approved knowledge, candidates, governance findings, audit events, or skill changes were created.

The [detailed review](markdown-import-review.json) contains the source inventory and 42 observations.
The observations distinguish textual inconsistencies, missing evidence, and unresolved historical context.
Their severity concerns knowledge reuse and does not rate confirmed production defects.
All finding owners remain unknown.

## Automated source checks

| Check | Observed result |
| --- | --- |
| Markdown inventory | 118 files; all text read. |
| Whitespace-only files | 11 files. |
| Exact duplicate nonempty files | None detected. Repeated sections and related versions still occur. |
| Detected local attachment references | 567 occurrences. No referenced local attachment exists in this copy. |
| Unmatched fence markers | None detected by the fence scan. |
| Original byte hashes | All 118 files match the initial review inventory. |

Attachment counts use inline Markdown pattern inspection.
They do not establish a complete CommonMark parse.
External links were not fetched or classified as broken.
Original Markdown does not need Workbench frontmatter.

## Consequential observations

### 1. The copied materials omit referenced artifacts

Evidence: [Meeting records](<../../knowledge/raw/confluence/FM TPT UI Guild/MOM/page.md#L3>) refer to email attachments.
The [getting-started guide](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/Getting Started with Single-Spa Micro-Frontend/page.md#L15>) depends on source archives and screenshots.
The architecture-diagram and non-functional requirements pages contain no substantive text.
Consequence: The export cannot supply the meaning or evidence held in those missing artifacts.
Owner: unknown.
Next action: Recover relevant attachments and determine whether empty pages are containers or export omissions.

### 2. Session rules require reconciliation

Evidence: [Version 1, line 136](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md#L136>) specifies 105 minutes, then calculates with 225 minutes.
Consequence: An AI-generated expiry scenario could select the wrong limit.
Owner: unknown.
Next action: Resolve the intended duration against the governing session design.

The [earlier requirement](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 0/page.md#L4>) limits absolute session duration.
The [later proposal](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Session Control and Implement Refresh Token/MFE Session Control and Implement Refresh Token Version 1/page.md#L159>) resets `auth_time` during renewal.
Consequence: Their relationship does not establish one accepted session boundary.
Owner: unknown.
Next action: Identify the accepted reauthentication rule before deriving measurable acceptance scenarios.

### 3. Entra entry instructions differ

Evidence: The [design](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/UI SSO Entra Design/page.md#L15>) uses `true` and `false` for `ENABLE_ENTRA_SSO`.
The [production guide](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md#L40>) uses `yes` and `no`.
Consequence: These texts alone cannot establish accepted flag values.
Owner: unknown.
Next action: Confirm supported values against the applicable client revision.

The same guide's rollout table requires revisiting the pilot link after browser restart.
Its [pilot section](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Entra Migration/Post Trade Portal Entra Migration - Phase 1 - UI SSO/Entra SSO Prod Guide/page.md#L101>) says further flags are unnecessary.
Consequence: Pilot preference persistence remains unclear.
Owner: unknown.
Next action: Confirm storage and restart behavior before producing one instruction set.

### 4. The release proposal contains inconsistent and ambiguous rules

Evidence: The [summary](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L19>) specifies 24 hours.
The [rule table](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L52>) specifies 10 hours.
Consequence: Release planners could derive different outage and standby periods.
Owner: unknown.
Next action: Record the accepted duration, policy status, and effective date.

The [urgent-release table](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Markets Operations One Release/page.md#L149>) requires all confirmations and permits proceeding when no concerns arise.
Consequence: The relationship between explicit confirmation and absence of objections remains unclear.
Owner: unknown.
Next action: Define the required decision evidence and accountable approval roles.

### 5. Drafts and historical versions need explicit applicability

Evidence: [SDK guidance](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Single UI SDK/page.md#L15>) dates an entitlement change to DEV in 2024.
The [capabilities page](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Post Trade Portal Capabilities/page.md#L37>) marks FDC3 as in progress.
Other records describe POCs, later guides, rollout targets, and reported fixes.
Consequence: Combining them without version boundaries could present proposals or historical observations as current behavior.
Owner: unknown.
Next action: Establish source dates, environments, applicability, and supersession relationships before synthesis.

### 6. Examples and templates do not establish completed implementation

Evidence: The [Jenkins sample](<../../knowledge/raw/confluence/FM TPT UI Guild/Bin/Jenkins Pipeline/page.md#L76>) uses placeholder `echo` statements for scan stages.
The [conceptual draft](<../../knowledge/raw/confluence/FM TPT UI Guild/UI Library Comparations/Draft/Conceptual Design DRAFT/page.md#L9>) contains unresolved placeholders.
Its approval links target a ClickHouse conceptual-design page without explaining their relevance.
Consequence: AI could reuse scaffolding as completed implementation or accepted rationale.
Owner: unknown.
Next action: Label examples and templates, then locate their applicable implementation or completed decision records.

### 7. Export formatting obscures relationships

Evidence: [Library comparisons](<../../knowledge/raw/confluence/FM TPT UI Guild/UI Library Comparations/page.md#L13>) place nested table text inside one row.
The [getting-started guide](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/Getting Started with Single-Spa Micro-Frontend/page.md#L9>) uses bracket-only page labels.
Consequence: Extraction can assign values to incorrect columns or infer incorrect page relationships.
Owner: unknown.
Next action: Resolve source page identities and normalize tables in derived documents.

### 8. Example data contracts have inconsistent fields

Evidence: [AnalyticsData](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Analytics/Design/page.md#L80>) defines attributes through 20.
The same document's other type and explanatory text stop at 10.
Consequence: The accepted receiving contract remains unclear.
Owner: unknown.
Next action: Identify the applicable analytics contract and each field's meaning.

The [notification interface](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Notification Store and React.useEffect/page.md#L5>) declares `isRead` as a string.
Its [handler](<../../knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Notification (DRAFT)/Notification Store and React.useEffect/page.md#L69>) assigns boolean `false`.
Consequence: Generated types and example consumers could disagree.
Owner: unknown.
Next action: Resolve the intended field type before using this draft for implementation.

## Proposed knowledge topics

These topics are proposed outputs, not approved project knowledge.

| Topic | Materials to connect |
| --- | --- |
| Portal purpose and capability map | Guild vision, capabilities, portal principles, and deployment proposals. |
| Frontend composition | Single-spa design, module boundaries, component guidance, and onboarding instructions. |
| Authentication and session rules | Login eligibility, token contracts, session versions, and Entra migration material. |
| SDK and downstream authorization | SDK versions, entitlement payloads, EMS2 roles, and integration responsibilities. |
| Tile administration and onboarding | Maker-checker procedures, provisioning, tenant onboarding, and configuration promotion. |
| Release and operating procedures | Release proposals, calendars, phase-specific approvals, rollback, and historical records. |
| Interoperability | Browser and OpenFin contexts, FDC3 contracts, compatibility, and POC limits. |
| Analytics and performance | Event fields, handling boundaries, test scopes, cache rules, and retained observations. |
| Architecture evolution | Historical options, research, decisions, effective dates, and superseded proposals. |

This collection mainly describes the portal and UI platform.
Its document count does not establish coverage of the complete brownfield business domain.
Coverage should answer agreed project questions and expose unsupported answers.

## Proposed skill changes

The existing ingestion skill remains unchanged during this review.
The review supports these focused changes:

- Select review mode for verification requests and keep original bytes unchanged.
- Inventory the full batch and check attachment completeness before interpreting source claims.
- Distinguish current instructions, historical observations, proposals, POCs, templates, and placeholders.
- Separate confirmed textual conflicts from unresolved version or approval relationships.
- Return one consolidated review with citations, consequences, unknown owners, and proposed actions.
- Use ingestion mode to preserve sources and synthesize connected topics when that work is requested.

The next useful pilot would reconcile one topic across its related sources.
Authentication and session behavior provide concrete examples for that pilot.
Important rules need owner review before adoption.

## Review validation and limits

```gherkin
Scenario: Review originals without changing them
  Given 118 supplied Markdown files
  When the batch review completes
  Then all 118 files retain their initial SHA256 hashes
  And every reported evidence quotation matches its cited source line
  And the raw manifest retains zero source records
```

Report checks cover source hashes, evidence quotations, report links, and prose length.
The Workbench validator reports `VALID` with zero governed documents.
That result does not establish raw export completeness or business correctness.
Attachments and external sources remain unreviewed.
No business repository code, source-document command, or deployment was executed.
ASD writing review remains pending.
