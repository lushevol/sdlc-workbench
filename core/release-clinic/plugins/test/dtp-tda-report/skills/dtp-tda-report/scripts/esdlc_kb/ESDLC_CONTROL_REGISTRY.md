# eSDLC Control Registry — dtp-tda-report Coverage Mapping

> Curated by hand. This file is **never overwritten automatically** by
> `fetch_esdlc_kb.py` re-runs — only the `raw/` cache and
> `esdlc_kb_manifest.json` are refreshed. When a re-run reports a changed
> page (see `esdlc_kb_changes_<date>.md`), review the affected control
> row(s) below and update this table manually.
>
> Source: https://dev.azure.com/sc-ado/ESDM/_wiki/wikis/ESDM.wiki/29/Enterprise-sdlc
> Scaffolded: 2026-10-13 from the live `e-sdlc-controls.md` page.
> **Verified: 2026-10-13** — one-time snapshot review, read every control's real "Control
> Attributes"/Evidence table (`raw/e-sdlc-controls__*.md`) side-by-side with the actual
> SKILL.md rule text (not just the control names) before classifying each row below.
> **Corrected: 2026-10-13** — the initial pass incorrectly flagged "NFR doc not checked" as a
> gap under Approved Requirements. Re-verified against `tda/collectors/release.py` and
> `ado_field_config.yaml`: `Custom.NFRApprovalExpiryDate`/`Custom.NFRDocumentLink` are already
> fetched identically to Architecture/ASRM/Test Strategy/Test Environment (same `_DOC_LINK_FIELDS`
> map), and SKILL.md explicitly names "NFR" in both the Application Approvals expiry rule and the
> Confluence Post-Approval Edit Check rule. This was a false gap, not a real one — row updated below.

| Control Name | Trigger | ADO Implementation | Automated in dtp-tda-report? | Mapped SKILL.md Section | Notes |
|---|---|---|---|---|---|
| Approved Requirements (Functional & Non-Functional) | Release | Automated | ✅ Yes | Stories in Scope (implicit) + Application Approvals/Confluence Post-Approval Edit Check (NFR doc) | Functional reqs covered via Stories/Epics tagged to the Release WI. NFR document (the control's own required artifact) IS covered — `Custom.NFRApprovalExpiryDate`/`Custom.NFRDocumentLink` are fetched and gate-checked identically to Architecture/ASRM/Test Strategy (expiry CRITICAL/MINOR-Info + post-approval-edit detection). No real gap remains here. |
| Architecture and Design Sign-off | Application | Partially Automated | ✅ Yes | Application Approvals (Architecture expiry) + Confluence Post-Approval Edit Check | Direct match — expiry + post-approval-edit-detection both implemented for the Application Architecture doc. |
| Software Configuration Management | Platform | Automated | ❌ Not covered | — | Enforced by branch policy/repo standards at the pipeline level itself — genuinely out of this report's scope, not a gap. |
| Test Environment Management | Platform | Automated | ✅ Yes | Application Approvals (Test Environment Management expiry) + Confluence Post-Approval Edit Check | Direct match — explicitly named in both rules. |
| Code Review | Release | Automated | ✅ Yes | Sonar Coverage / Quality Gate / New Code Period / Exclusions | Matches the control's "Automated: Report from SonarQube" evidence row directly. PR-based peer review enforcement (branch policy) stays upstream, not re-checked here. |
| Unit Testing | Release | Automated | ✅ Yes | Testing Coverage (Unit tests Failed/Others CRITICAL gate) + Sonar coverage thresholds | Direct match. |
| Test Strategy | Application | Partially Automated | ✅ Yes | Application Approvals (Test Strategy expiry) + Confluence Post-Approval Edit Check | Direct match — doc approval/expiry + post-approval-edit covered; strategy *content* quality itself is not separately scored (not required by the control either). |
| Secure by Design | Release | Partially Automated | ❌ **Not covered — real gap** | — | No SIA/sTK sign-off check anywhere in SKILL.md, and no vulnerability-scan (SAST/Gitleaks/Checkov/Cosign) pass/fail result check. Candidate for new implementation if this data is exposed anywhere in ADO for these pipelines. |
| Functional Testing | Release | Automated | ✅ Yes | Manual Test Execution gate, Traceability — Test Coverage Analysis, Regression Failure Re-Test | Most heavily automated control — strong, direct match across 3 separate SKILL.md sections. |
| Non-Functional Testing | Application | Partially Automated | ✅ Yes | PT / PIT Document Checks (PT Plan+Report / PTIA mutual exclusivity + approvals) | Direct match. |
| Pre-Deployment Verification | Release | Automated | ✅ Yes | Application Approvals (ASRM/Operations Manual expiry); Implementation & Rollback Documentation — Equivalence Check (`aig_rollback_check` + `Custom.ImplementationPlan`/`Custom.BackoutPlan`) | ASRM/Operations Manual approval IS tracked via the generic Application Approvals mechanism. **Deployment/rollback documentation is gate-checked via a two-gate equivalence model (merged 2026-10-13, supersedes the 2026-08-20 dual-source check)**: Gate A (Implementation/Deployment) is satisfied by an AIG document (Release WI link or build artifact) OR the Release WI's `Custom.ImplementationPlan` field; Gate B (Rollback/Backout) is satisfied by an AIG RWI-linked document, a rollback section within an AIG build artifact, OR the Release WI's `Custom.BackoutPlan` field. Treats the AIG document and the Change Manifest fields as alternate/equivalent evidence sources (not independent requirements) so a team using only one mechanism isn't falsely flagged for not using the other — MODERATE only when a gate has zero sources at all. |
| Post Deployment Verification | Release | Automated | ✅ Yes | PIT gate (triple-source: Confluence/SC Wiki page, `Custom.ReviewComments`, `Custom.PITPlan`) | Direct match — this is the dedicated PIT automation for this control. |
| E-SDLC Integrated Training | Squad | Automated | ➖ N/A | — | Org-level training/certification tracking — no per-release ADO data source exists for this at all; not realistically automatable by a release-level report. |
| Data | Release | Partially Automated | ❌ **Not covered — low priority** | — | No CDE impact-assessment check. Note: unlike all 13 other controls, this page defines **no ADO evidencing mechanism/Evidence table at all** — eSDLC itself hasn't defined how this should be evidenced in ADO yet, so this isn't really actionable until that exists upstream. |

## Verified Candidates for New Implementation (2026-10-13 snapshot, corrected same day)

One genuine, actionable gap identified (data likely obtainable via existing collector patterns):

1. **Secure by Design check** — verify SIA/sTK sign-off status and/or surface a vulnerability-scan
   (SAST/Gitleaks/Checkov/Cosign) pass/fail result, if this data is exposed anywhere in ADO for the
   release's component pipelines (needs confirmation this data is actually reachable before committing
   to implement).

(The NFR-documentation idea originally listed here was found to be a false gap on closer inspection —
NFR is already extracted and gate-checked identically to Architecture/ASRM/Test Strategy/Test
Environment. See the corrected row above.)

Everything else classified **❌ Not covered** above is a deliberate/reasonable exclusion (enforced
elsewhere in the pipeline, or no ADO data source exists yet) rather than a real gap — see the
Pre-Flight Checklist cross-reference below for why several of these are already enforced as pipeline
Hard Stops, not omissions.

## Release Compliance Pre-Flight Checklist Cross-Reference

The `/Enterprise-sdlc/checklist/compliance-checks-preflight-checklist.md` page documents the
pipeline's own automated gates (CI Build -> PRE_TEST -> PRE_RELEASE -> Release Approval ->
PRE_PRODUCTION). Several of its Hard Stop items are enforced by the ADO pipeline itself
(secrets scanning, commit-to-work-item linkage, branch naming, SAST, Nexus IQ, Aqua DTA) —
these deliberately do NOT need a dtp-tda-report rule, since they already block the release
pipeline before a release WI is even relevant to this skill. Re-check this cross-reference
whenever the checklist page changes (see `esdlc_kb_changes_*.md`).
