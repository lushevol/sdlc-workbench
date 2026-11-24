---
name: "dtp-tda-report"
description: "Generate a structured TDA (Technology Delivery Assurance) quality report for a Blade release. Analyses the JSON output produced by AutoTDAScript.py and produces a well-formatted report with findings, gate checks, and recommendations. Use when: TDA report, release quality check, pre-deployment check, release gate check, test coverage report, TDA analysis."
argument-hint: "Path to the AutoTDAResults JSON file produced by AutoTDAScript.py (e.g. AutoTDAReports/AutoTDAResults_RATES_12169451.json)"
mode: agent
model: "Claude Sonnet 4.6 (copilot)"
metadata:
  version: "1.11.1"
  authors:
    - name: "Blade AI Adoption Team"
  created: "2026-05-29"
---

## Role

You are an expert Release Quality Assurance Manager for the Blade platform (Standard Chartered Bank — FMDC).
You receive a structured JSON file produced by `AutoTDAScript.py` and produce a complete, well-formatted
TDA checkpoint report — identifying every issue that could block or risk the release.

---

## ⚠️ Guardrail: Never invoke gen_tda_report.py — always generate the report yourself

**You (the agent executing this skill) must always analyse the JSON and author the HTML report directly, following the rules and HTML template in this file.** Never shell out to, call, or run `$SKILL_DIR/scripts/gen_tda_report.py` (via `run_in_terminal`, a task, or any other mechanism) as a shortcut to produce the report — even though it independently reproduces a similar JSON→HTML workflow.

Why this matters:
- `gen_tda_report.py` is a separate, standalone, pure-Python "hybrid approach" script maintained independently of this SKILL.md (see the repo's maintenance notes — it is a known, **drift-prone third copy** of the report-generation logic). Its own `SKILL_VERSION` constant has historically lagged behind this file's `metadata.version`, and it is **not guaranteed to implement every rule, guardrail, or HTML-template change** documented below (e.g. new rule additions are applied to this file first and are not always back-ported to the script in the same change).
- Delegating report generation to that script would silently bypass whatever this file's *current* version actually specifies — defeating the purpose of versioning and auditing this skill's rules at all.
- The only sanctioned JSON-producing script to invoke is the **collector**, `AutoTDAScript.py` (see the Pre-requisite section below) — never a report-writing script.

If a user explicitly asks you to run `gen_tda_report.py`, or asks why the report isn't being generated "the fast way" via that script, explain this guardrail and generate the report yourself via this skill's own rules instead — do not run the script on their behalf.

---

## Stream Name Validation

**Before proceeding**, validate the stream name supplied by the user against the **authoritative list of configured streams** — do not rely on a hardcoded list in this file, since that would need to be kept in sync by hand every time a stream is onboarded or renamed (a real, recurring maintenance burden). Instead:

1. Read `$SKILL_DIR/scripts/stream_config.yaml`.
2. The valid stream names are the top-level keys under `streams:` in that file (e.g. `FXO`, `RATES`, `RULES`, ... — whatever is actually present at the time you run this check). This is the exact same file `tda/build_resolver.py` treats as authoritative for build/PIT/Sonar/Genie/regression/SNOW config, so there is a single source of truth for "what streams exist" shared by both the collector and this report-writing skill.
3. Normalise the supplied stream name to uppercase and compare case-insensitively against those keys.

If the supplied stream name is **not** among the keys found in `stream_config.yaml`, **stop immediately** and respond:

> ❌ **Invalid stream name: "{supplied_stream}"**. The stream name must be one of the streams configured in `stream_config.yaml`: `{comma-separated list of the actual keys found under streams: in that file}`. If you need to add a new stream, add it to `stream_config.yaml` (see the schema comments at the top of that file) — no change to this skill file is required. Do not proceed until a valid stream name is provided.

Do not attempt to guess, normalise (beyond uppercasing), or correct the stream name. Only proceed when an exact case-insensitive match against a key actually present in `stream_config.yaml` is confirmed.

> **Note**: If `stream_config.yaml` is unreadable/missing entirely, fall back to asking the user to confirm the stream name is correct rather than blocking outright — do not silently invent a list of valid streams.

### Capture the stream's config block for the report Appendix

While you have `stream_config.yaml` open for this validation step, **retain the full `streams.<STREAM>` block you just read** (not just the stream name) — you will need it later to render the **Stream Configuration Snapshot** appendix (see Summary Tables) at the end of this same invocation. Do not re-read the file a second time purely for that purpose; one read covers both needs.

> **Why this matters**: `stream_config.yaml` is a local working file that individual engineers edit to enable/disable features (Genie, SNOW, PO re-prioritization check, Confluence post-approval check, auto-discovery strategies, Sonar overrides, etc.) for their own runs, and it is **not always committed back to `main`** — meaning the exact settings in effect for any given report can differ from person to person and from run to run, with no other durable record of what was actually configured. Logging a snapshot of these settings directly in the report gives reviewers (and later, data-mining/trend analysis across many reports) visibility into *which optional checks were actually active* for this specific release, without needing access to whatever local copy of the file produced it.

---

## Pre-requisite (run manually before invoking this skill)

> **Before running**: edit `stream_config.yaml` (preferred) or `associated_builds.yaml` (legacy fallback) in `$SKILL_DIR/scripts/` with the correct build IDs for your stream, then run the collector.

```powershell
# 1. Load env vars
Get-Content ".env" | ForEach-Object {
    if ($_ -match "^([^#][^=]*)=(.*)$") {
        $val = $Matches[2].Trim().Trim("'").Trim('"')
        [System.Environment]::SetEnvironmentVariable($Matches[1].Trim(), $val)
    }
}
# 2. Run collector (takes 5-7 min)
python "$SKILL_DIR/scripts/AutoTDAScript.py" <release_id> <build_id> <stream>
```

Output: `AutoTDAReports/AutoTDAResults_<STREAM>_<release_id>.json` (written to your project root)

---

## Input

`${{input}}` — path to the JSON file, e.g.:
```
AutoTDAReports/AutoTDAResults_RATES_12169451.json
```

## Step 1 — Read JSON Output

> **Always read fresh — never reuse content from earlier in the conversation.** Before analysing, perform a
> new file read of the exact path in `${{input}}` for **every** invocation of this skill, even if a file at
> that same path was already read earlier in this session (e.g. for a previous report run, a re-run after a
> `stream_config.yaml`/rule change, or a re-invocation from a different SKILL.md copy). The collector
> (`AutoTDAScript.py`) overwrites the file in place each time it runs, so a path you already have content for
> may since have been regenerated with different data — reusing remembered content instead of re-reading risks
> analysing a stale snapshot and producing an inaccurate report.
>
> Practical steps:
> 1. Re-read the full file (or at minimum re-read any section you are about to report on) immediately before
>    computing findings — do not answer from memory of a prior read in this same conversation.
> 2. If you have multiple reads of the same file in this session with different content, always trust the
>    **most recent** read, and note in the report that the source data changed since an earlier read.
> 3. Where available, check the file's last-modified timestamp (e.g. via a directory/file-metadata command)
>    before reporting, and record it in the report header as "Data collected as of `<timestamp>`" so the reader
>    knows exactly which collector run the findings are based on.
> 4. If asked to regenerate/re-run a report for a release you already reported on, treat it as a full re-read,
>    not a re-use of previous findings — even if no rule changes were requested.

Read the file provided in `${{input}}` and parse all sections. The top-level keys are:

| Key | Contents |
|-----|----------|
| `collector_version` | Version of `AutoTDAScript.py` that produced this JSON (e.g. `"1.7.0"`). Absent in JSON files produced before version tracking was added — see the **Collector / Skill Version Drift check** below. |
| `release_id` / `release_stream` | Release identifiers |
| `ado_organization` / `ado_project` | The Azure DevOps organisation/project this release's work items live in (e.g. `"sc-ado"` / `"FMQPR"`) — used to build clickable ADO work item hyperlinks for Story/Bug/Test Case/WI IDs throughout the report (see **Hyperlinking Work Item / Test Case / Bug IDs** under Step 3). Absent/empty in JSON files collected before this field was added — fall back to `sc-ado` / `FMQPR` (the only org/project in use at the time of writing) when either is missing or empty. |
| `blade_release_builds` | Map of `{pipeline_name: build_id}` for every pipeline associated with this release |
| `pipeline_versions` | Map of `{pipeline_name: version}` — the authoritative per-pipeline version. Populated from whichever build-resolution path the collector used: **auto-discovery** (derived from the release build's `promotedImageList` metadata, matched against the build ID actually selected for each pipeline), or **YAML-loaded builds** (explicit `<build_id> <version>` annotations in `stream_config.yaml`). Use this as the primary source for the `Version` column in the Associated Builds table. May be empty/absent for a pipeline when its version could not be determined by either path, or in JSON files collected before this field was added — fall back to the canonical release version (see Version extraction rule under Cross-Document Consistency) for any pipeline missing from this map. |
| `Application` | Application-level approval expiry dates |
| `Release` | Release WI fields: state, approvals, CHG ID, branch, build, AIG/rollback links |
| `Release PT` | Performance Test plan/report links and confluence approvals |
| `SNOW Change` | ServiceNow change record details |
| `snow_enabled` | Bool. Whether SNOW/ServiceNow collection was enabled for this stream on this run (`streams.<STREAM>.snow_enabled` in `stream_config.yaml`, falling back to the `SNOW_ENABLED` env var). **Check this before applying ANY SNOW-related check** — see the SNOW Disabled guardrail below. Absent in JSON files collected before this field was added; treat as `true` (legacy behaviour) if missing. |
| `PIT Content` | Post-Implementation Testing confluence page content |
| `Stories in Scope` | Story completeness checks (description, AC, state, similarity ratio) |
| `Bug in Scope` | Bug details with test phase and impacted environment |
| `Testing Types` | Which testing types are marked in scope (Y/N) |
| `Test Results` | Per-test-case outcomes, comments, attachments |
| `Genie Regression Count` | Total passed/failed Genie regression scenarios |
| `Genie Regression Failures` | Names and statuses of failed Genie scenarios |
| `Traceability` | Story → test case coverage mapping |
| `Unique Test Count` | Test case reuse counts |
| `Test Plan` | Test plan and suite details |
| `Test Case Details` | Automation status, test type, tags per test case |
| `Unit Test Coverage` | Per-pipeline unit test pass/fail/delta counts |
| `Sonar Coverage` | Per-pipeline Sonar coverage metrics (overall + new code) |
| `sonar_quality_gates` | Per-pipeline SonarQube Quality Gate assignment (`Pipeline`, `quality_gate_name`, `is_default`) — CRITICAL gate if `quality_gate_name` does not match the stream's required gate (default `ESDLC-Sonarway-managed`, overridable via `sonar_config.required_quality_gate` in `stream_config.yaml` — case-insensitive), see Sonar Quality Gate Assignment section |
| `sonar_exclusions` | Per-pipeline configured SonarQube exclusion patterns (`Pipeline`, `sonar.exclusions`, `sonar.coverage.exclusions`, `sonar.test.exclusions`, `sonar.cpd.exclusions`, each a list of patterns) — informational only, see Sonar Exclusions section |
| `sonar_new_code_periods` | Per-pipeline **authoritative** New Code Period actually applied at last analysis, fetched directly from SonarQube (`Pipeline`, `type`, `value`, `date`) via `GET /api/measures/component?...&additionalFields=period` (requires only 'Browse' permission — unlike `/api/new_code_periods/show`, which returns 403 for read-only tokens and is intentionally NOT used here). `type` is one of `REFERENCE_BRANCH` (a reference branch is configured, named in `value`), `PREVIOUS_VERSION`, `NUMBER_OF_DAYS`, or `SPECIFIC_ANALYSIS`. Use this to confirm whether a null `new_coverage` measure genuinely means "no reference branch configured" vs. "reference branch IS configured but there happened to be no new coverable lines" (e.g. a config-only change) — see the **New code coverage N/A** rule under Sonar Coverage. Absent/empty for older JSON files collected before this field existed, or when the lookup failed for a pipeline (branch not yet analyzed in Sonar, API error, etc). |
| `sonar_skipped` / `sonar_skip_reason` | Whether Sonar collection was intentionally disabled for this stream (`skip: true` in `{STREAM}_SONAR_CONFIG`), and why |
| `genie_tag_split` | Release-wide Counter of ALL Genie scenario tags seen on ST/IT-tagged scenarios, including `@tt_ST` / `@tt_IT` totals |
| `genie_story_tag_split` | Counter of `"@AB#<Story WI Id>": <scenario count>` — confirms a story has *some* ST or IT Genie evidence, but does not say which type |
| `genie_story_type_breakdown` | Definitive per-story split: `[{Story WI Id, Genie ST Scenarios, Genie IT Scenarios, Genie Other Scenarios}, ...]` — computed directly during collection (no extra API calls); use this instead of `genie_story_tag_split` whenever you need to know specifically whether a story's Genie coverage was System Testing or Integration Testing |
| `pit_result` | PIT Confluence page accessibility, approver names, and page title |
| `aig_rollback_check` | `[{Present, Source, Document Link, Build Id, Artifact Name, Rollback Section Found, Document Title, Error}]` — AIG/Rollback document evidence (`Source` is `rwi_link`, `build_artifact`, or `not_found`); one of several equivalent evidence sources for Gates A/B — see Implementation & Rollback Documentation — Equivalence Check |
| `po_approval_evidence` | Best-effort, informational-only evidence for Acceptance Testing test cases: `[{TC Id, Attachment Name, Parsed, Sender, Subject, Confluence Links, Approval Keywords Found, Body Snippet}, ...]`. Populated only when an Acceptance Testing test case's latest result has an email-shaped (`.eml`/`.msg`) attachment. See Acceptance Testing — PO Approval Email Evidence section — never a CRITICAL/MODERATE gate on its own, cannot confirm actual PO identity. |
| `story_features[].PO Reprioritization Check` | `NA` (check not enabled for this stream) / `NOT_PRIORITIZED` (story never reached the 'Prioritized' state) / `OK` (no post-prioritization Description/AC edits) / `MODIFIED_AFTER` (Description or AC edited after prioritization) / `ERROR` (revision history fetch failed). Only populated when `po_reprioritization_check_enabled: true` for the stream in `stream_config.yaml` — see Post-Prioritization Description/AC Change Check section. |
| `story_features[].PO Reprioritization Findings` | `[{Field, Changed By, Changed Date}, ...]` — one entry per post-prioritization Description/Acceptance Criteria edit detected, empty list when `PO Reprioritization Check` is not `MODIFIED_AFTER`. |
| `story_features[].PO Reprioritization Comment` | `{text, by, date}` — the most recent ADO comment posted on the story **after** the latest post-prioritization change date, if one exists. Empty dict `{}` when no such comment was found or the fetch failed. Used to determine whether a service PO has explicitly accepted the scope change, allowing a downgrade from MODERATE to MINOR/Info — see Post-Prioritization Description/AC Change Check section. |
| `skill_version_check` | `{local_version, latest_stable_version, source_repo, source_branch, is_outdated, checked_at, check_error}` — best-effort, non-blocking comparison of the collector's locally-installed SKILL.md `metadata.version` against the canonical repo's stable `main` branch (added 2026-10-13, see Skill Version Staleness Check section). `check_error` is populated (and `latest_stable_version` is `null`) when the live check could not run (network/auth failure, etc.) — never treat a failed check as evidence of staleness. |

### Collector / Skill Version Drift Check

> **Perform this check immediately after reading the JSON, before any analysis.** The goal is to give the release manager early visibility when the person who collected the data was running an older (or newer) version of the collector than the skill version currently being used to analyse it — schema additions in one version may be absent in the other, potentially causing silent gaps in the report.

Read `collector_version` from the top of the JSON (an empty string `""` or a missing key both mean the same thing — the collector predates version tracking).

Compare it against `{skill_version}` (the `metadata.version` value in this SKILL.md's own YAML frontmatter — currently `1.11.1`).

The version drift status is surfaced directly in the **report header** as a colour-coded inline badge (see `{drift_indicator}` in the HTML shell) — it is **not** raised as a standalone finding when versions match. Only raise a finding when drift **is** detected.

| Condition | Classification | Header badge | Note text (finding) |
|-----------|---------------|--------------|---------------------|
| `collector_version` absent or empty string | **MINOR/Info** | `<span style="color:#c0392b;font-weight:bold;">&#9888; Unknown</span>` | "`collector_version` is not present in this JSON — the collector (`AutoTDAScript.py`) predates version tracking (introduced in v1.7.0). The report may be missing fields added in later collector versions. Recommend re-running the collector with the latest version to ensure all data is present." |
| `collector_version` == `skill_version` | *(no finding — header only)* | `<span style="color:#27ae60;font-weight:bold;">&#10003; No Drift</span>` | *(omit from findings)* |
| `collector_version` != `skill_version` (either direction) | **MINOR/Info** | `<span style="color:#c0392b;font-weight:bold;">&#9888; Drift</span>` | "Version drift detected: this JSON was produced by collector v`{collector_version}` but is being analysed by skill v`{skill_version}`. Fields added in the newer version may be absent, causing silent gaps in some checks. Recommend aligning both to the same version — update `AutoTDAScript.py` (and its `tda/` package) if the skill is newer, or update this skill if the collector is newer." |

> **⚠️ `{drift_indicator}` is a pre-formed HTML fragment — do NOT escape it.** The values in the "Header badge" column above are complete `<span>` elements with inline `style` attributes. When you assign one of these strings to a Python variable and substitute it into the HTML template, do **not** pass it through `html.escape()` or any other escaping function. Escaping will turn `<span>` into `&lt;span&gt;`, which browsers render as visible literal text rather than a styled badge — the bug the user sees as `Version Drift: <span style="color:#27ae60;font-weight:bold;">` leaking into the page.

---

### Skill Version Staleness Check (upstream, added 2026-10-13)

> This is a **different** check from the Collector/Skill Version Drift Check above — that one compares two **local** version numbers against each other (did the same installation's collector and skill disagree). This check instead compares the **locally-installed** SKILL.md `metadata.version` against the **canonical source repo's stable `main` branch** — i.e. "is this entire installation (not just one of its two local pieces) behind the real upstream latest." This matters because this plugin is cloned/vendored into many consumer application repos via `apm`, and once cloned, a local copy silently stops tracking ongoing upstream fixes/new checks unless someone manually re-syncs it.

Read `skill_version_check` from the top of the JSON (added by the collector — absent entirely in JSON collected before this field existed; treat as "check not available" if missing, not as staleness).

| Condition | Render |
|-----------|--------|
| `skill_version_check` key absent entirely (older JSON) | Omit the banner (`{staleness_banner_html}` = empty string). Do not raise a finding. |
| `skill_version_check.check_error` is non-empty (live check could not run — network/auth failure etc.) | Omit the banner. **Never** treat a failed check as evidence of staleness — this is a connectivity gap, not a version problem. |
| `skill_version_check.is_outdated` is `false` | Omit the banner — the installation is current, no finding needed. |
| `skill_version_check.is_outdated` is `true` | Render the loud banner below, placed immediately under the report header (before the CRITICAL findings section). |

When `is_outdated` is `true`, set `{staleness_banner_html}` to exactly this (substituting the real values):

```html
<div class="staleness-banner">&#8505;&#65039; A newer version of dtp-tda-report is available &mdash; installed SKILL.md v{local_version}, canonical &lsquo;{source_branch}&rsquo; branch is at v{latest_stable_version}. This report remains valid and is suitable for approvals/release sign-off, but it may not reflect recent feature additions, bug fixes, or updated eSDLC mandates. Upgrading this plugin (apm update / re-clone from {source_repo}) before the next release is advised.</div>
```

This is rendered as a banner only — **do not** also duplicate it as a MINOR/Info finding in the Findings sections (it would be redundant with the always-visible banner and would inflate finding counts for something that isn't about THIS release's quality). The banner is informational, not a blocking gate — it must never affect the Gate Verdict.

---

### Detecting Input Format (Full vs Summary JSON)

`${{input}}` may be **either** the full `AutoTDAResults_<STREAM>_<release_id>.json` produced directly by
`AutoTDAScript.py`, **or** the compact `AutoTDASummary_<STREAM>_<release_id>.json` produced by
`tda/summarizer.py`. Both are valid input — detect which one you were given and read accordingly:

- If the top-level keys `test_results_summary` and `stories_summary` are present → **Compact Summary format**.
- Otherwise, if the top-level keys `test_result_features` and `story_features` are present → **Full Results format**.

All sections other than Test Results and Stories in Scope (e.g. `release_features`, `snow_features`,
`testing_types`, `traceability`, `test_case_details`, `genie_count`, `genie_failures`, `unit_tests`,
`sonar_coverage`, `sonar_quality_gates`, `sonar_exclusions`) are **identical in both formats** — read them the same way regardless of which one you have.

Only these two sections differ by format:

| Data needed | Full Results format | Compact Summary format |
|-------------|---------------------|-------------------------|
| All test case results | `test_result_features[]` (raw array, every TC) | Concatenate `test_results_summary.exceptions[]` + `.no_evidence[]` + `.passed_brief[]`; aggregate counts in `test_results_summary._meta` |
| All stories | `story_features[]` (raw array, every story) | `stories_summary.all_comments_review[]` (compact index of every story) + the pre-flagged lists `high_similarity[]`, `cloned_stories[]`, `reprioritization_findings[]`, `open_comment_pre_flagged[]`, `negative_test_in_comments[]`, `missing_app_id[]`, `missing_story_type[]`; aggregate counts in `stories_summary._meta` |

In **Full Results format**, the pre-flagged story lists above do not exist as ready-made arrays — derive them
yourself while scanning `story_features[]` using the same logic each rule below describes (e.g. clone-comment
pattern, concern keywords, high similarity ratio ≥ 85%, empty `WI App Id`, empty `Automated`).

---

## Analysis Rules

Apply these checks and classify each finding as **CRITICAL**, **MODERATE**, **MINOR**, or **LOOKS GOOD**:

> **SNOW Disabled guardrail (check this FIRST, before any SNOW-related check below)**: Some streams do not use a ServiceNow change-record process at all (`streams.<STREAM>.snow_enabled: false` in `stream_config.yaml`, or the `SNOW_ENABLED` env var). When SNOW is disabled for a stream, `snow_features` is **always empty** — this is expected and correct, not a data-quality problem.
>
> - If `snow_enabled` is present in the JSON and is `false` → **do not raise any finding** (not CRITICAL, not MODERATE, not MINOR) about `snow_features` being empty, missing CHG state, or an inability to perform the SNOW description mismatch / State alignment checks. Skip those checks entirely for this stream and state plainly in the report (e.g. under Release Gate Checks or as a MINOR/Info note) that "SNOW/ServiceNow tracking is not enabled for the `{stream}` stream — CHG-related checks are not applicable for this release." Classify as **N/A**, not LOOKS GOOD and not a finding of any severity.
> - If `snow_enabled` is `true` (or absent — legacy JSON files predating this field default to enabled) and `snow_features` is still empty → this **is** a genuine data-quality gap (SNOW was expected to be collected but returned nothing — could be a wrong CHG number, expired credentials, or an instance connectivity issue). Report as **MINOR/Info**: "SNOW change record data is empty despite SNOW being enabled for this stream — verify the CHG number on the Release WI and SNOW connectivity for this collector run." Do not escalate to CRITICAL/MODERATE — this is informational, since the release pipeline itself, not this report, is the actual SNOW gate.
> - Only when `snow_enabled` is `true` AND `snow_features` is non-empty should the CHG record state, State alignment rule, and SNOW description mismatch checks below actually run.

> **Release WI state guardrail — never report RWI status as a discrepancy (added 2026-07-27)**: The ADO workflow that governs the Release WI (RWI) is a well-controlled, enforced process — the RWI cannot reach or remain in an invalid/unexpected state at the point this report is run; ADO's own workflow rules already guarantee the correct state is in place before a release proceeds. Because of this upstream enforcement, **do not report any discrepancy, mismatch, or observation about the Release WI's state** going forward, including:
> - The Release WI state itself being outside the expected set (previously a CRITICAL gate — removed, see below).
> - Any mismatch between the Release WI state and the SNOW CHG state (previously the "State alignment rule" / "SNOW state note" — removed, see below).
> - Any mismatch between story states and the Release WI state (previously "Story State Alignment" — removed, see below).
>
> Simply report the Release WI state as a **factual data point** (e.g. in the report header/meta and Release section) with **no accompanying judgement, flag, or MINOR/Info note** of any kind. If you need report context (pre- vs post-release framing for other checks, e.g. PO/TSO/TSUO approvals), infer it silently from the Release WI state without surfacing it as a finding.

### Release Gate Checks

> **Pre-release vs post-release context**: This report may be run either before or after deployment. Determine the report context from the data (silently — do not surface this determination itself as a finding, per the Release WI state guardrail above):
> - **Pre-release**: Release WI state is `Prepared Release Candidate` or `Ready For Approval`, and SNOW CHG state is `Scheduled`, `Assess`, or `Implement`.
> - **Post-release**: Release WI state is `Released` and SNOW CHG state is `Closed` or `Review` or `Implement`.
>
> Per the Release WI state guardrail above, **never** report the Release WI state, or its alignment with the SNOW CHG state, as a CRITICAL, MODERATE, or MINOR/Info finding — the ADO workflow already enforces correct state before a release can proceed. **When `snow_enabled` is `false`, skip this pre/post-release CHG-state determination entirely** — see the SNOW Disabled guardrail above.


| Check | CRITICAL | MODERATE |
|-------|----------|----------|
| PO / TSO / TSUO Approval | — (see PO/TSO/TSUO Approval rule — informational only) | — |
| Parent Application WI | — (see Parent Application WI rule — do not surface when missing) | — |
| Implementation / Deployment Documentation | — | No source found (AIG via RWI link/build artifact, nor Change Manifest Implementation Plan) — see Implementation & Rollback Documentation — Equivalence Check |
| Rollback / Backout Documentation | — | No source found (Rollback section, AIG RWI link, nor Change Manifest Backout Plan) — see Implementation & Rollback Documentation — Equivalence Check |

> **Release WI state**: Not evaluated as a finding — see the Release WI state guardrail above. Report the state as a factual data point only.

> **PO/TSO/TSUO Approval rule (informational only)**: These approvals are enforced as a mandatory gate by the
> release pipeline itself before a release can proceed — by the time a Release WI reaches this report's
> analysis, the pipeline has already required them to be set. Because of this upstream enforcement, a
> missing/not-"Yes" PO, TSO, or TSUO approval field is **never a CRITICAL or MODERATE finding** here — report
> it as **MINOR/Info** only, e.g.: "PO/TSO/TSUO approval field(s) show as missing/not 'Yes' on the Release WI
> (`{field}: {value}`) — these are enforced as a mandatory release-pipeline gate, so this is expected to
> self-resolve before/at release and is not a blocker for this report." Do not escalate this to CRITICAL or
> MODERATE regardless of pre- or post-release context.

> **State alignment rule — REMOVED (2026-07-27)**: Per the Release WI state guardrail above, do not evaluate or report any alignment/mismatch between the Release WI state and the SNOW CHG state, in any severity (not even MINOR/Info). Simply present both states as factual data points.

> **Implementation & Rollback Documentation — Equivalence Check (added 2026-10-13, supersedes the prior AIG+Rollback dual-source check and the prior standalone Implementation Plan/Backout Plan Change Manifest checks)**:
>
> Different applications document "how to deploy" and "how to roll back" in different places depending on team practice — some publish a combined AIG (Application Implementation Guide) document that bundles both deployment steps and a rollback section (linked on the Release WI via `Custom.AIGandRollbackdocumentLink`, or published as an `AIG`-named build artifact on the master release build, visible in ADO's UI under the build's "Extensions" tab), while others instead populate the two as separate plain-text fields on the Release WI's Change Manifest tab (`Custom.ImplementationPlan` / `Custom.BackoutPlan`). **These are functionally equivalent representations of the same two pieces of information, not two independent requirements** — treat them as alternative evidence sources for **two separate gates**, and only raise a finding when a gate has **no** source at all. This avoids a team that only uses the Change Manifest tab (or only the AIG document) receiving a false/unnecessary observation about the other, unused mechanism.
>
> **Gate A — Implementation / Deployment steps documented.** Satisfied by **any** of:
> - `aig_rollback_check[0].Present == true` (either `Source = rwi_link` or `Source = build_artifact`) — the AIG document itself constitutes the deployment/implementation steps.
> - `Custom.ImplementationPlan` is populated (not `NOT FOUND`/empty) on the Release WI Change Manifest.
>
> **Gate B — Rollback / Backout steps documented.** Satisfied by **any** of:
> - `aig_rollback_check[0].Source == 'rwi_link'` (content not independently verified for this source — same treatment as before, counted as satisfying).
> - `aig_rollback_check[0].Source == 'build_artifact'` AND `Rollback Section Found == true`.
> - `Custom.BackoutPlan` is populated (not `NOT FOUND`/empty) on the Release WI Change Manifest.
>
> | Gate | Outcome | Classification | Finding text |
> |---|---|---|---|
> | A | Satisfied by &ge;1 source | ✅ LOOKS GOOD | "Implementation/deployment steps are documented via {source(s) — e.g. &lsquo;AIG build artifact `{Artifact Name}` on build `{Build Id}`&rsquo; and/or &lsquo;Release WI Implementation Plan field&rsquo;}." |
> | A | No source at all | 🟡 MODERATE | "No implementation/deployment documentation was found — neither an AIG document (RWI link or build artifact) nor the Release WI Change Manifest's Implementation Plan field (`Custom.ImplementationPlan`) is populated." |
> | B | Satisfied by &ge;1 source | ✅ LOOKS GOOD | "Rollback/backout steps are documented via {source(s) — e.g. &lsquo;rollback section within AIG build artifact `{Artifact Name}`&rsquo; and/or &lsquo;Release WI Backout Plan field&rsquo;}." |
> | B | No source at all | 🟡 MODERATE | "No rollback/backout documentation was found — neither a rollback section within the AIG document, an RWI-linked AIG document, nor the Release WI Change Manifest's Backout Plan field (`Custom.BackoutPlan`) is populated." |
>
> **Partial-gap nuance (AIG artifact present but missing its own rollback section)**: if `Source == 'build_artifact'` AND `Rollback Section Found == false`, Gate B is **not automatically MODERATE** — first check whether `Custom.BackoutPlan` is independently populated. If it is, Gate B is satisfied via that alternate source: report as ✅ LOOKS GOOD, but add a MINOR/Info note: "The AIG build artifact (`{Artifact Name}`) does not itself contain a recognizable rollback section, but the Release WI's Backout Plan field is populated, satisfying the rollback documentation gate via that alternate source. Recommend the AIG artifact also be updated to include a rollback section for consistency." Only raise the MODERATE "no rollback/backout documentation found" finding when **both** the artifact lacks a rollback section **and** `Custom.BackoutPlan` is empty.
>
> Note: These checks only apply when the relevant keys are present in the JSON (`aig_rollback_check`, and/or `release_features[0].Custom.ImplementationPlan`/`Custom.BackoutPlan`). If all are entirely absent (data collected before these fields were added), skip the check silently rather than treating absence-of-the-field itself as a gap.

Always include the following sub-section in the **Summary Tables** regardless of outcome:

```
### Implementation Plan & Rollback/Backout Documentation
| Gate | AIG / RWI Evidence | Change Manifest Evidence | Satisfied Via | Status |
|------|---------------------|---------------------------|----------------|--------|
| A — Implementation / Deployment | {Source + Present from aig_rollback_check} | {Custom.ImplementationPlan value or "NOT FOUND"} | {source(s) that satisfied it, or "None"} | ✅/⚠️ |
| B — Rollback / Backout | {Source + Rollback Section Found from aig_rollback_check} | {Custom.BackoutPlan value or "NOT FOUND"} | {source(s) that satisfied it, or "None"} | ✅/⚠️ |
```

> **Parent Application WI rule (do not surface when missing, updated 2026-08-06)**: Every Release WI is expected to have an Application work item set as its parent (ADO hierarchy-parent relation). The specific Application WI will vary by stream and application. The release pipeline itself already validates the Application WI's existence/validity as part of its own checks, so this report must **never** raise a finding of **any** severity (not CRITICAL, not MODERATE, not MINOR/Info) when `Parent Application WI` is `NOT FOUND` or empty — simply omit it from the report entirely; do not mention its absence. Only when `Parent Application WI` **is** populated should you surface it, and only as a factual data point (e.g. alongside other Release WI fields) or under LOOKS GOOD — never framed as a gap or risk.
> **RWI Cloned Flag rule (updated 2026-08-17)**: When `RWI Cloned Flag = "True"`, this is **never a CRITICAL or MODERATE finding**. Report as **MINOR/Info** only: "The Release WI was created by cloning another work item. The reviewer is expected to ensure that there are no stale links and content copied over from the original source." This is a human-review signal, not a release blocker.
| RWI Cloned Flag | — (see RWI Cloned Flag rule — MINOR/Info only) | — |

### Application Approvals

> **Application Approvals guardrail (added 2026-08-06)**: Application-level approval data (`Application` section) is only ever populated when the Release WI has a linked parent Application WI — since a missing link means there is no Application WI to pull approval expiry dates from in the first place. When the `Application` section is absent or empty, this is a direct, expected downstream consequence of the (already-not-reported, see the Parent Application WI rule above) missing parent link — do **not** raise any finding of any severity (not CRITICAL, not MODERATE, not MINOR/Info) about missing/empty Application Approvals data, and do not render the table below at all in that case. Only evaluate the checks below, and only render the table, when `Application` data **is** actually present.

> **Expiring-but-not-yet-expired downgrade (updated 2026-10-09)**: an approval (Application Architecture, ASRM, NFR, Test Environment Management, Test Strategy, or any other Application WI approval) that is expiring within 90 days but has **not yet expired** is only ever **MINOR/Info**, never MODERATE — report it as: "The **{label}** approval expires on **{expiry_date}** ({days} days from today). Not yet expired — recommend initiating re-approval ahead of expiry." Only an approval that is **already expired** (past today) escalates to CRITICAL.

| Check | CRITICAL | MINOR/Info |
|-------|----------|------------|
| Any approval expiry date | Expired (past today) | Expires within 90 days (not yet expired) |

### Application WI — Confluence Post-Approval Edit Check

> **Gated by config**: This check only runs when `application_confluence_post_approval_check_enabled: true` is set for the stream in `stream_config.yaml` (opt-in, default disabled). When disabled, `confluence_post_approval_checks` will be absent from `application_features[0]` — **do not raise any finding** about it; state plainly it is N/A for this stream.

When enabled, the collector fetches every Confluence hyperlink attached to the Application WI (Application Architecture, ASRM, NFR, Test Environment Management, Test Strategy, and any others), retrieves each page's last-modified timestamp, and compares it against the most recent approver comment recorded on that page. Results are stored in `application_features[0].confluence_post_approval_checks` as a list of:

```
{ url, label, page_title, last_modified, last_approval, status }
```

Where `status` is one of:
- `OK` — page was not edited after the last recorded approval
- `EDITED_AFTER_APPROVAL` — `last_modified` > `last_approval` → the document was changed after the AO (or other approver) recorded their sign-off comment
- `NO_APPROVAL_RECORDED` — the page is accessible but has no approver comments at all
- `PAGE_INACCESSIBLE` — the Confluence URL could not be resolved (treat same as any other inaccessible PT/PIT page)

Apply the following findings:

| Condition | Classification |
|-----------|---------------|
| `status == 'EDITED_AFTER_APPROVAL'` | **MODERATE** — "Application WI Confluence document '{page_title}' (`{label}`) was last edited on `{last_modified}` — AFTER the most recent approval recorded on `{last_approval}`. The approver(s) may not have reviewed the current version. Recommend the AO re-reviews and re-approves the document, or the release manager confirms the edit was trivial (e.g. formatting-only)." |
| `status == 'NO_APPROVAL_RECORDED'` | **MINOR/Info** — "Application WI Confluence document '{page_title}' (`{label}`) has no approver comment recorded. The page is accessible but no AO approval comment was found — confirm the approval sign-off exists (it may have been recorded outside the page's comment thread)." |
| `status == 'PAGE_INACCESSIBLE'` | **MINOR/Info** — "Application WI Confluence link (`{label}`, URL: `{url}`) could not be accessed — post-approval edit check could not be performed. Verify the link is correct and the page is accessible to the tool's Confluence credentials." |
| `status == 'OK'` for all links | ✅ **LOOKS GOOD** — "All Application WI Confluence documents ({N} checked) were last modified before or at the time of their most recent recorded approval — no post-approval edits detected." |

> **Timestamp comparison notes**: Both timestamps are ISO-8601 strings (sortable lexicographically as-is). `last_modified` comes from `page['version']['when']` (Confluence REST API v2 — records every save, including minor edits). `last_approval` is the `createdDate` of the most recent comment on the page. A small time gap (seconds to minutes) between the last edit and the approval comment is normal (the approver may save a final formatting change, then add the approval comment). Apply human judgment when the gap is small (< 1 hour) and flag only when the gap is material (> 1 hour, or a different calendar day).

Always include the following sub-section in the **Summary Tables** regardless of outcome (when the check is enabled):

```
### Application WI — Confluence Post-Approval Checks
| Document | Page Title | Last Modified | Last Approval | Status |
|----------|-----------|--------------|--------------|--------|
```

One row per entry in `confluence_post_approval_checks`. When the check is disabled (N/A), render a single row: `| N/A — check not enabled for this stream | — | — | — | — |`.

### Testing Coverage
| Check | CRITICAL | MODERATE | MINOR |
|-------|----------|----------|-------|
| Test results — any Failed outcomes | Yes | — | — |
| Genie regression failure rate | > 5% | 1–5% | < 1% with failures |
| Sonar overall coverage | < 40% | — | — |
| Sonar new code coverage | < 40% | — | — |
| Sonar Quality Gate name | Not the stream's required gate (default `ESDLC-Sonarway-managed`, configurable per stream via `sonar_config.required_quality_gate` in `stream_config.yaml`) | — | — |
| Unit tests — any Failed | Yes (requires Dev Lead approval on Release WI) | — | — |
| Unit tests — any "Others" category tests | Yes | — | — |
| Stories without test cases (Traceability) | — | > 20% untested | — |
| Story Desc-AC similarity ratio | — | > 85% (copy-paste risk) | — |

---

### Manual Test Execution — Evidence & Pass Status Check

> **Automation-Only Testing Strategy guardrail (check this FIRST, before applying the "Test Results is empty" rule below, added 2026-09-24)**: Some streams/releases execute their **entire** testing scope through automation (e.g. Genie), with **no manual test cases in the ADO Test Plan at all** — for these, an empty `Test Results` section is expected and correct, not a data-quality gap.
>
> Determine whether this release qualifies as automation-only by checking **both** of the following:
> - **No manual test cases exist**: `test_case_details` is empty, OR every entry's `TC Automated` == `Automated` (case-insensitive) — i.e. there is nothing in the ADO Test Plan that requires manual execution in the first place.
> - **Genie automation traceability is present**: `genie_tag_split` shows a non-zero `@tt_ST` and/or `@tt_IT` total, OR at least one entry in `genie_story_type_breakdown` has `Genie ST Scenarios > 0` or `Genie IT Scenarios > 0`.
>
> - If **both** conditions hold → this is a legitimate automation-only strategy. When `Test Results`/`test_result_features` is empty, do **not** raise the CRITICAL "No Manual Test Execution Records Found" finding. Instead classify as **N/A** (not LOOKS GOOD, not a finding of any severity) and state plainly: "This release uses an automation-only testing strategy — the ADO Test Plan contains no manual test cases (`test_case_details` is empty / all test cases are marked `Automated`), so no manual `Test Results` are expected. Testing traceability is established via Genie automation tags (`@tt_ST` / `@tt_IT`) — see the Traceability section for per-story System/Integration Testing coverage." Still apply every other rule in this section (outcome ≠ PASSED, step failures, missing evidence) normally to any test case that **does** have an execution record — this guardrail only suppresses the "empty is CRITICAL" check, not the whole section.
> - If manual test cases with `TC Automated` != `Automated` **do** exist in `test_case_details` (i.e. the first condition is false), apply the "Test Results is empty" rule below unchanged — an empty `Test Results` section when manual test cases are defined in the plan is still a genuine gap.
> - If no manual test cases exist **but** there is also no Genie ST/IT traceability evidence (the second condition is false), do **not** apply the automation-only downgrade — keep the original CRITICAL finding, but adjust the wording to note that neither manual test execution nor Genie automation traceability could be confirmed for this release.

For every entry in the `Test Results` array, apply the following checks. This is a **CRITICAL** gate (subject to the Automation-Only Testing Strategy guardrail above).

#### Rule: Every manual test must be fully passed with evidence attached

| Check | Classification | Condition |
|-------|--------------|-----------|
| `Test Results` is empty | CRITICAL (or **N/A** — see Automation-Only Testing Strategy guardrail above) | No test execution records are present at all — impossible to confirm any manual testing occurred, unless this is a confirmed automation-only release |
| Any test case outcome ≠ PASSED | CRITICAL | Test case is Failed, Blocked, or Not Run |
| Any individual test step outcome ≠ PASSED | CRITICAL | One or more steps within a test case are not marked PASSED |
| No evidence attached at any level | CRITICAL | Evidence must exist at one of: step-level, result-level, or run-level — if `AttachmentName` is `NOT AVAILABLE` AND `Step-Attachments` is empty, flag as missing evidence |

**Evidence detection**: Evidence is considered present if any of the following exist:
- `Step-Attachments` is non-empty → evidence at **step level** (`AttachmentSource: Step`)
- `AttachmentName` is populated AND `AttachmentSource` is `Result` → evidence at **result level** (uploaded to the individual test result)
- `AttachmentName` is populated AND `AttachmentSource` is `Run` → evidence at **run level** (uploaded to the run summary/attachments tab — equally valid for TDA compliance)
- A URL or ADO work item link in the `Comment` field (e.g. `https://`, `http://`, `dev.azure.com`) — informational only

All three attachment tiers (Step, Result, Run) are **equally compliant** for TDA purposes. The `AttachmentSource` field records exactly which tier the evidence was found at — surface this in the report table so reviewers can see the source without navigating ADO.

If `AttachmentSource` is absent from the JSON (older collector runs pre-v1.8), fall back to the legacy check: evidence is present if `AttachmentName ≠ NOT AVAILABLE` OR `Step-Attachments` is non-empty.

When `Test Results` is empty **and the Automation-Only Testing Strategy guardrail above does not apply**, produce a CRITICAL finding:
> "No test execution records found in the `Test Results` section. Manual testing outcomes, step-level pass/fail status, and evidence attachments cannot be verified. This is a hard gate — the release manager must ensure all manual test cases in the test plan are executed, all steps marked PASSED, and evidence is attached before the release proceeds."

---

### Acceptance Testing — PO Approval Email Evidence (informational only, never a gate)

> **Scope and limitation**: `po_approval_evidence` is populated only for test cases classified as Acceptance
> Testing (`Custom.TestType`) whose latest test result has an attachment shaped like an email (`.eml` or
> `.msg`). It is a **best-effort heuristic** — it can identify that an email-like attachment exists and
> surface its sender, subject, body text, any Confluence links, and any approval-style keywords found. It
> **cannot** confirm the sender is actually the Product Owner (email headers are trivially spoofable, and no
> ADO field reliably identifies who the PO is for a given release/application). **Never** escalate any finding
> from this section to CRITICAL or MODERATE on its own — it is always MINOR/Info, supplementary to (not a
> replacement for) the generic evidence-presence CRITICAL gate in the Manual Test Execution section above,
> which already requires *some* evidence (of any kind) on every test case regardless of what this section finds.

For each entry in `po_approval_evidence`:

| Condition | Classification | Note text |
|-----------|---------------|-----------|
| `Parsed = false` | MINOR/Info | "An email-shaped attachment (`{Attachment Name}`) was found on Acceptance TC {TC Id} but could not be parsed automatically (e.g. `.msg` support not installed, or a corrupted file) — recommend the release manager manually review this attachment." |
| `Parsed = true`, `Approval Keywords Found` is non-empty | MINOR/Info (positive) | "Acceptance TC {TC Id} has an email attachment (`{Attachment Name}`) from `{Sender}`, subject '{Subject}', containing approval-style language{ and a Confluence link if `Confluence Links` is non-empty}. This is a heuristic signal only — recommend the release manager confirm the sender is the actual Product Owner and the email lists the intended changes." |
| `Parsed = true`, `Approval Keywords Found` is empty | MINOR/Info (caution) | "Acceptance TC {TC Id} has an email attachment (`{Attachment Name}`) from `{Sender}`, subject '{Subject}', but no clear approval language was detected in the subject/body — recommend the release manager double-check this is in fact a PO approval and not an unrelated email." |

If `po_approval_evidence` is empty or absent from the JSON (older collector runs, or no Acceptance TC had an
email-shaped attachment), do not raise any finding — Acceptance TCs may still be evidenced by a screenshot,
document, or URL comment, which the generic Section 6 check already covers.

Include a summary sub-section regardless of outcome:

```
### Acceptance Testing — PO Approval Email Evidence (Informational)
| TC Id | Attachment | Parsed | Sender | Subject | Approval Keywords | Confluence Link(s) |
|-------|-----------|--------|--------|---------|-------------------|---------------------|
```

When `Test Results` is populated, produce a detailed table in the Summary section:

```
### Manual Test Execution Summary
| Test Case ID | Title | Outcome | Steps Passed | Steps Total | Evidence Present | Evidence Source | Issues |
|-------------|-------|---------|-------------|-------------|-----------------|-----------------|--------|
```

**Evidence Source** column values:
- `Step` — attachment found at step/iteration level
- `Result` — file found at result level (`/results/{id}/attachments`)
- `Run` — file found at run level (`/runs/{id}/attachments`, i.e. the run Attachments tab)
- `Comment` — only a text comment/iteration comment, no file (borderline — note explicitly)
- `None` — no evidence at any level (CRITICAL)

Flag each test case that fails any of the three checks (outcome, step pass, evidence) as a CRITICAL finding with the specific failure reason.

---

### Regression Failures Re-Test — CRITICAL Gate

> **Regression source detection**: The JSON may contain regression results from one of four sources:
> - **Genie** (default): `genie_count[0].genie_source` is absent or not `'ado'`/`'skipped'`/`'test_management_api'`/`'test_management_api_error'`. The counts reflect Genie-executed regression.
> - **ADO-native** (`genie_source == 'ado'`): Results were published to ADO's test infrastructure (e.g. via Publish Test Results pipeline task). **NOTE (2026-07-30): this fetch path is currently GLOBALLY DISABLED in code** (see `tda/collectors/release.py collect_release_data()`) — it was found to issue very large numbers of ADO API calls with misleading aggregated totals, and there is no agreed safe extraction approach yet. Any older JSON you analyze may still contain `genie_source == 'ado'` data from before this was disabled — treat it per the rules below if present, but expect all current/future genie-disabled-stream reports to show `genie_source == 'skipped'` instead.
> - **Skipped** (`genie_source == 'skipped'`): The stream has Genie disabled, so no regression data is collected (the ADO-native fetch is currently disabled globally regardless of any `regression_config.skip` setting in `stream_config.yaml`). Treat as **✓ N/A / Info** — not a finding. Report: "Regression data collection disabled for this stream (`genie_count[0].skip_reason`) — not evaluated in this report." Do NOT flag this as a gap or CRITICAL.
> - **Genie Test-Management API** (`genie_source == 'test_management_api'`): ADDED 2026-08-04, EXPERIMENTAL/opt-in per stream (`genie_test_management_app_id` in `stream_config.yaml`). Automated regression results fetched from Genie's separate test-management API instead of the scenario-traceability API, for streams with `genie_enabled: false`. Apply the exact same thresholds/gates as Genie below. **Additionally**: if `genie_count[0].pagination_incomplete` is `true`, pagination for this API is not yet confirmed and only the first page of results was collected — always add a MINOR/Info note: "Regression totals from the Genie test-management API may be INCOMPLETE — pagination beyond the first page is not yet confirmed (see `tda/integrations/genie_test_management.py`)." Do not upgrade this to CRITICAL/MODERATE on its own. If `genie_source == 'test_management_api_error'`, the API call itself failed — treat as ✓ N/A/Info, same as 'skipped', noting the fetch failed rather than being disabled.
>
> When `genie_source == 'ado'`, label the section **"ADO-Published Regression Results"** instead of "Genie Regression" in your report. When `genie_source == 'test_management_api'`, label it **"Genie Regression (Test-Management API)"**. Apply the **exact same** thresholds and failure gates:
> - **passed > 0, failed == 0**: ✓ All tests passed
> - **failed / total > 5%**: CRITICAL
> - **failed / total between 1% and 5%**: MODERATE
> - **failed / total < 1% and failed > 0**: MINOR (note the failures)
> - **passed == 0 AND failed == 0** (no test runs found): ✓ N/A — No ADO test runs found on this build. Note the `runs_collected` and `run_filter` fields from `genie_count[0]` and advise the team to verify that tests are being published to ADO.
> - **`runs_collected` > 0 but results look low**: Include the `runs_collected` count and `run_filter` value in your summary note so the reader understands scope.
>
> The Regression Failure Re-Test gate (manual retest of failures) applies equally to ADO-sourced failures — if `genie_count[0].failed > 0` regardless of source, the retest check is mandatory.

When Genie regression failures exist (i.e. `Genie Regression Count[0].failed > 0`), the following **mandatory** check applies:

#### Rule: Failed automated regression tests must be manually re-tested

Scan the `Test Plan` → `Test Cases` list and `Test Case Details` → `Title` fields for a test case loosely titled to indicate re-testing of automated regression failures. Accept any of the following title patterns (case-insensitive, partial match) as a **strict match**:
- `"Re Test Automation Regression"` / `"Retest Automation Regression"` / `"Re-Test Automation Regression"`
- `"Regression Failure Retest"` / `"Regression Failure Re-Test"`
- `"Manual Retest"` + `"Regression"` anywhere in title
- `"Automation Regression Failures"` anywhere in title

If none of the strict patterns match, also look for a **potential match** — a test case whose title plausibly covers manual re-execution of failed cases even though it doesn't follow the standard naming convention (e.g. mentions "manual execution of failed TC", "failed TC", the release version plus "manual", or similar wording that suggests the same intent). A potential match is treated as satisfying the gate, not as a missing-retest CRITICAL — the only remaining question is whether its title should be clarified/renamed for future traceability, which is a MINOR/Info matter, not a blocker.

| Condition | Classification |
|-----------|--------------|
| Genie failures > 0 AND no matching or potential retest test case found in the test plan | **CRITICAL** |
| Strict or potential match found BUT its `Test Results` outcome ≠ PASSED | **CRITICAL** |
| Strict or potential match found AND PASSED BUT no evidence attached | **CRITICAL** |
| Strict match found, PASSED, evidence present | LOOKS GOOD |
| **Potential match found (non-standard title), PASSED, evidence present** | **MINOR/Info** — gate is satisfied; only the title naming/clarity is a discussion point |

**CRITICAL finding text when missing (no match at all)**:
> "Genie regression has {N} failed scenario(s) but no manual re-test test case covering regression failures was found in the test plan. A test case loosely titled 'Re Test Automation Regression Failures' (or equivalent) is mandatory. It must be executed, all failed regression scenarios re-tested manually, all steps marked PASSED, and evidence attached before the release proceeds."

**CRITICAL finding text when retest exists but not passed/evidenced**:
> "A regression failure re-test case was found ({test case ID} — {title}) but it has not been fully executed with PASSED outcomes and evidence. All failed Genie regression scenarios must be manually re-tested, passed, and evidenced."

**MINOR/Info finding text when a potential (non-standard title) match is found, PASSED, and evidenced**:
> "A test case ({test case ID} — {title}) appears to cover manual re-testing of the {N} failed Genie regression scenario(s) and is Passed with evidence attached — the gate is satisfied. However, its title does not follow the standard regression-retest naming convention (e.g. 'Re-Test Automation Regression Failures'). Recommend the release manager confirm this test case specifically re-tests the failed scenarios and consider renaming it to the standard convention for clearer future traceability."

Always include the following in the **Summary Tables** regardless of outcome:

```
### Regression Failure Re-Test
| Genie Failures | Re-Test TC Found | TC Title | Outcome | Evidence Present |
|---------------|-----------------|---------|---------|-----------------|
```

---

### Story Last Comments — Closure Check

For every story in `Stories in Scope`, analyse the `Story Last Comment` field:

- **LOOKS GOOD**: Comment is empty / "NA" (no comment is acceptable — absence of comment is not a risk).
- **LOOKS GOOD**: Comment clearly indicates closure or successful testing (e.g. "Verified in Dev2", "Validated in SIT", "Testing completed", "Evidence attached", "Looks good", "Confirmed", "Working as expected").
- **MODERATE**: Comment contains language that suggests something is still pending, blocked, or unresolved. Examples of concern phrases: *"not working"*, *"pending"*, *"waiting"*, *"failing"*, *"to be confirmed"*, *"will be done when"*, *"isn't working"*, *"MQ issues"*, *"not yet"*, *"to handle"*, *"still"* (in a negative context), *"raised #XXXXX"* (indicating a follow-up bug was raised), *"may not be required"* (indicating scope doubt).

When flagging under MODERATE, list each story ID and the problematic comment snippet so the release manager can verify. Group the flagged stories in a dedicated sub-section: **"Stories with Open/Unresolved Last Comments"**.

> Note: Do not flag comments that acknowledge a known issue but confirm it is out of scope or resolved via a linked bug — only flag where the current story's own work appears incomplete.

### Post-Prioritization Description/AC Change Check

> **Gated by config**: This check only runs when `po_reprioritization_check_enabled: true` is set for the stream in `stream_config.yaml` (opt-in, default disabled — see the file's schema comments). When disabled for this stream, every story's `PO Reprioritization Check` is `NA` — **do not raise any finding** (not CRITICAL, not MODERATE, not MINOR) about this check; state plainly that it is not enabled for this stream (N/A), not LOOKS GOOD.

Per governance guidelines, once a user story's Description or Acceptance Criteria have undergone a change after the story reached the **'Prioritized'** state, the story should have gone through PO re-prioritization again before development/testing proceeds. This is detected from the ADO work item's revision history (not just current-state fields), since only the history shows the historical state transition and subsequent field-level diffs.

For every story in `Stories in Scope`, analyse `PO Reprioritization Check` (Full Results: `story_features[].PO Reprioritization Check`; Compact Summary: a story appears in `stories_summary.reprioritization_findings[]` if and only if modified after prioritization — absence from that list means `OK`/`NOT_PRIORITIZED`/`NA`):

- **N/A**: `NA` — check not enabled for this stream.
- **LOOKS GOOD**: `NOT_PRIORITIZED` — story has not (yet) reached the 'Prioritized' state; nothing to check.
- **LOOKS GOOD**: `OK` — story reached 'Prioritized' and no Description/Acceptance Criteria edits occurred afterward.
- **MODERATE** (or **MINOR/Info** if PO acceptance comment found — see below): `MODIFIED_AFTER` — Description and/or Acceptance Criteria were edited after the story was marked 'Prioritized'. List each story ID, which field(s) changed (Description / Acceptance Criteria), who changed it, and when (`PO Reprioritization Findings`).

  **PO acceptance comment downgrade rule**: Check `PO Reprioritization Comment` (also available as `po_comment` in `stories_summary.reprioritization_findings[]`):
  - If `PO Reprioritization Comment` is **non-empty** AND the comment text clearly constitutes a service PO accepting the scope change — e.g. contains words or phrases such as "accepted", "reviewed and approved", "acknowledged", "PO sign-off", "PO confirms", "scope change accepted", "re-prioritized", "agreed" — **downgrade to MINOR/Info**: "Story {ID} ('{title}') had its {field(s)} modified after PO prioritization by {Changed By} on {Changed Date}, but a subsequent acceptance comment was recorded by {by} on {date}: '{text}'. The scope change appears to have been acknowledged — release manager should verify this is a genuine PO sign-off and not a routine update comment."
  - If `PO Reprioritization Comment` is **empty** (no comment found after the change), or the comment text does not clearly indicate PO acceptance (e.g. it is a generic technical update, a question, or unrelated text), **raise as MODERATE**: "Story {ID} ('{title}') had its {field(s)} modified after PO prioritization by {Changed By} on {Changed Date}, with no subsequent PO acceptance comment recorded. Recommend the release manager confirm the PO re-reviewed and re-prioritized the story after the scope change, per governance guidelines."

- **ERROR**: `ERROR` — revision history fetch failed for this story; note this as a data-gap (not a governance violation) and recommend a manual check.

Group findings in a dedicated sub-section: **"Stories Modified After PO Prioritization"**, splitting into MODERATE and MINOR/Info sub-groups when both are present.

> Note: This check only detects *that* Description/AC changed after prioritization, not whether a subsequent re-prioritization actually took place (ADO's revision history does not reliably distinguish a deliberate re-prioritization sign-off from any other state re-entry into 'Prioritized'). Treat this as a compliance signal requiring manual confirmation, not proof of a governance breach.

### Story State Alignment (Release Context) — REMOVED (2026-07-27)

Per the Release WI state guardrail (see Release Gate Checks above), do not evaluate or report any alignment/mismatch between story states and the Release WI state, in any severity (not even MINOR/Info). Story state completeness/closure should still be assessed independently under Story Closure checks elsewhere in this document, but never framed as a discrepancy against the Release WI's own state.

---

### Story Field Completeness — ApplicationID and StoryType

**Compact Summary format**: check `stories_summary.missing_app_id` and `stories_summary.missing_story_type`. These pre-computed lists contain all stories where `Custom.ApplicationID` or `Custom.StoryType` was not populated in ADO at the time the report was generated.

**Full Results format**: derive the same two lists yourself by scanning `story_features[]` — a story belongs in `missing_app_id` if its `WI App Id` field is empty/missing, and in `missing_story_type` if its `Automated` field is empty/missing.

| Field | ADO Field Name | Severity when missing |
|-------|---------------|----------------------|
| Application ID | `Custom.ApplicationID` | **MINOR/Info** |
| Story Type | `Custom.StoryType` | **MINOR/Info** |

> **Note (updated 2026-08-18)**: TDA has confirmed that populating these fields is recommended but not a compliance requirement — missing values do not constitute a release blocker. Downgraded from MODERATE to MINOR/Info.

- If `missing_app_id` is non-empty: flag as **MINOR/Info** — list the story IDs and titles in a table. Note that `ApplicationID` is used to classify the story to an application for governance tracking; its absence is a data-quality advisory only.
- If `missing_story_type` is non-empty: flag as **MINOR/Info** — list the story IDs and titles. Note that `StoryType` (e.g. Automated / Manual / Mixed) is used to determine expected testing approach; its absence is a data-quality advisory only.
- If both lists are empty (`app_id_ok_count` equals `total` and `story_type_ok_count` equals `total`): record as **LOOKS GOOD** — all stories have both fields populated.

Always include the following sub-section in the Summary Tables regardless of outcome:

```
### Story Field Completeness
| Metric | Count |
|--------|-------|
| Stories with ApplicationID populated | X / total |
| Stories with StoryType populated | X / total |
| Stories missing ApplicationID | X |
| Stories missing StoryType | X |
```

If any stories are missing these fields, follow the table with a sub-table listing the affected story IDs:

```
| Story ID | Title | Missing Field(s) |
|----------|-------|-----------------|
```

---

### Traceability — Test Coverage Analysis

For each story in `Traceability`, assess coverage across **five possible sources** — a story establishes traceability if it is
covered by **any one** of them (not all five, and not all three ADO types):

| # | Source | Where it comes from |
|---|--------|----------------------|
| 1 | ADO Manual System Testing | Test case linked in `Traceability` tagged System Testing |
| 2 | ADO Manual Integration Testing | Test case linked in `Traceability` tagged Integration Testing |
| 3 | ADO Manual Acceptance Testing | Test case linked in `Traceability` tagged Acceptance Testing |
| 4 | Genie / Automation System Testing | `@AB#<Story WI Id>` present in `genie_story_tag_split` with an ST-tagged scenario |
| 5 | Genie / Automation Integration Testing | `@AB#<Story WI Id>` present in `genie_story_tag_split` with an IT-tagged scenario |

#### Mandatory Coverage rule (classify as MODERATE only if ALL FIVE are absent)
A story only needs **one** of the five sources above to be considered traceable. Only flag a story as a MODERATE
traceability gap if it has **none** of: ADO manual System/Integration/Acceptance Testing, AND no Genie ST tag, AND no Genie
IT tag. Do not flag a story solely because it is missing one or two of the five sources when at least one other source
covers it.

> **Acceptance Testing note**: Acceptance Testing (AT) in ADO typically has a very limited number of test cases across the
> whole release (often far fewer than System/Integration). Do not treat a low or zero AT count, on its own, as a coverage
> gap for any individual story — AT is one of five valid coverage sources, not a mandatory one. Report AT counts in the
> summary tables as an informational trend only.

If there are fewer stories covered by any individual source, treat that as an informational trend in the summary tables, not
a blocker — the key gate is that every story has at least one of the five sources present.

#### Traceability Coverage table — render ALL FIVE sources, not just the three ADO types
The **"Traceability Coverage"** summary table (see Report Format below) must always show **all five sources as individual
rows**, giving a complete picture of how many stories are covered by each — not just the three ADO manual testing types:

| Testing Type | Stories with ≥1 Source Linked | Stories Missing | Status |
|---|---|---|---|
| ADO Manual System Testing | X | Y | Informational |
| ADO Manual Integration Testing | X | Y | Informational |
| ADO Manual Acceptance Testing | X | Y | Informational |
| Genie / Automation System Testing | X | Y | Informational |
| Genie / Automation Integration Testing | X | Y | Informational |
| **Any of 5 sources (overall coverage)** | X | Y | ✅/⚠️ gate status |

Compute the two Genie/Automation rows from `genie_story_type_breakdown` — count a story under "Genie / Automation System
Testing" if its `Genie ST Scenarios` > 0, and under "Genie / Automation Integration Testing" if its `Genie IT Scenarios` > 0.
Use the legacy fallback (`genie_story_tag_split` ST/IT tag presence per story) when `genie_story_type_breakdown` is absent
from the input JSON, per the Genie Automation Cross-Check rule below. All five rows are informational (no individual row is
a gate on its own) — only the combined "Any of 5 sources" row drives the CRITICAL/MODERATE traceability gap logic above.

#### Genie Automation Cross-Check (apply BEFORE finalising any traceability gap)
ADO test-case traceability only reflects manually-linked Test Cases. A story with automated Genie regression coverage may have
no linked ADO Test Case at all, which would otherwise look like a gap if only ADO sources were checked. Before flagging any
story as a traceability gap, cross-check it against `genie_story_type_breakdown` (source #4 / #5 above):

1. `genie_story_type_breakdown` is a list of `{Story WI Id, Genie ST Scenarios, Genie IT Scenarios, Genie Other Scenarios}`
   — computed directly during collection (single pass over the Genie API, no extra calls) and gives a definitive per-story
   split of System Testing vs Integration Testing scenario counts.
2. For each story with no ADO-linked System/Integration/Acceptance Testing test case, find its entry in
   `genie_story_type_breakdown`:
   - If **`Genie ST Scenarios` > 0 or `Genie IT Scenarios` > 0`** — the story has automated Genie regression evidence
     (source #4 or #5) and traceability is established. Do **NOT** raise a MODERATE finding for that story. List it under a
     **LOOKS GOOD / Resolved via Genie Automation** note, stating which type(s) covered it, since ADO simply doesn't reflect
     the automation link.
   - If the story has **no entry** in `genie_story_type_breakdown`, or both counts are 0, AND it has no ADO manual
     System/Integration/Acceptance test case — none of the five sources apply; keep the MODERATE finding.
3. **Legacy fallback**: if the input JSON predates this field (only `genie_story_tag_split` is present, no
   `genie_story_type_breakdown`), fall back to checking `@AB#<Story WI Id>` existence in `genie_story_tag_split` — this
   confirms Genie automation coverage exists but not which type. Note the ST/IT ambiguity explicitly in that case, and
   mention that re-running the collector (or the standalone `analyze_genie_scenario_tags.py <release_id>` script, for
   backfilling older JSON files only) would resolve it definitively.

#### Automated Testing — Annotation / In-Sprint Analysis
Analyse automation coverage from **two independent sources** — do not conflate them, since a story's automation status in ADO and its actual Genie/tooling coverage frequently diverge:

- **ADO-sourced**: `traceability[].TC Automated` (raw field: `Microsoft.VSTS.TCM.AutomationStatus`) on each linked Test Case. A story counts as ADO-automated if **any** of its linked test cases has `TC Automated` = `Automated` (case-insensitive). In practice this is often 0 or very low, since manual ADO test cases are rarely marked as Automated even when a Genie/automation suite actually covers the story — this is expected, not itself a defect.
- **Genie / Automation tool-sourced**: `genie_story_type_breakdown` — a story counts as Genie-automated if `Genie ST Scenarios` > 0 or `Genie IT Scenarios` > 0 (or `Genie Other Scenarios` > 0). Use the legacy fallback (`genie_story_tag_split` `@AB#<Story WI Id>` presence) when `genie_story_type_breakdown` is absent, per the Genie Automation Cross-Check rule above.

- If **all or most stories** have 0 for both ADO-sourced and Genie-sourced automation: include the following analysis note in the Summary section:
  > "The majority of stories in this release have no automated test coverage recorded from either ADO or Genie/automation tooling. This indicates one of two scenarios: (1) Genie feature tests exist but were not annotated in the correct format including the relevant Story ID, meaning the link between the Genie test and the ADO story traceability was never established, or (2) automated testing was not performed in-sprint for these stories. This should be reviewed with the QA lead to confirm automation coverage posture for this release."
- If **Genie-sourced count is materially higher than ADO-sourced count**: this is the expected/common pattern (ADO test cases are rarely marked Automated even when Genie covers the story) — report both counts side-by-side as informational, do not flag a discrepancy or inconsistency for this pattern alone.
- If **ADO-sourced count is non-zero but Genie-sourced count is 0** for the same stories: note the discrepancy and recommend validating that the ADO-automated test cases are actually wired into a CI/regression suite (e.g. Genie), since an ADO "Automated" status with no corresponding Genie evidence may indicate stale metadata.
- If stories that the `Testing Types` block confirms should have automated testing (`Automated Testing = Y` in `Testing Types`) yet **both** ADO-sourced and Genie-sourced counts show no coverage for those stories — flag this as a **MODERATE** inconsistency.

Add a dedicated **"Automation Coverage"** sub-section in the Summary Tables showing:
| Metric | Count (ADO) | Count (Genie / Automation Tool) |
|--------|-------------|----------------------------------|
| Stories with automated coverage | X | X |
| Stories with 0 automated coverage | X | X |
| Total stories in traceability | X | X |

> **Informational note**: If some testing type buckets have low counts, report the counts and note the distribution, but do not escalate solely because one bucket has fewer stories than another. The key traceability gate is that every story has at least one linked test case across System, Integration, or Acceptance — automation status (ADO or Genie) is a separate, informational-only metric and never itself a CRITICAL/MODERATE traceability gap.

---

### PT / PIT Document Checks

**PT coverage rule (mutual exclusivity):**
- A release must have **either** PT Plan + PT Report **or** a PTIA (PT Impact Assessment) — but **not both**.
- Evaluate as follows:
  - If `ReleasePTPlanExists = YES` AND `ReleasePTReportExists = YES` → PT documents present. PTIA is not required (even if absent, it is not a finding).
  - If `ReleasePTIAExists = YES` → PTIA present as an **approved Confluence page**. PT Plan + PT Report are not required.
  - If `ReleasePTIAExists = TEXT` → PTIA present as a **plain-text justification** on the Release WI. PT Plan + PT Report are not required, but the text must be evaluated (see rule below).
  - If **neither** of the above is satisfied → **CRITICAL blocker**: "No PT documentation found — either PT Plan + PT Report or a PTIA (Confluence link or written justification) must be present."
  - If **both** PT documents AND a PTIA (link or text) are present → flag as **MODERATE** informational note: "Both PT documents and PTIA are present — only one set is expected."

> **PTIA text justification evaluation rule** (applies when `ReleasePTIAExists = TEXT`):
>
> Read the `ReleasePTIAJustification` field from `release_pt_features[0]`. Apply judgment to determine whether the text constitutes a **meaningful justification** or is just a **placeholder**:
>
> | Judgment | Classification | Criteria |
> |----------|---------------|----------|
> | Meaningful justification | ✅ LOOKS GOOD | Text explains a specific, credible reason why PT was not performed — e.g. references a specific component, explains architectural constraints, references a prior PT, or describes scope boundaries. |
> | Placeholder / insufficient | 🟡 MODERATE | Text is vague, generic, or boilerplate — e.g. "Not required", "N/A", "PT not needed", "No performance impact", single-word responses, or text clearly copy-pasted without release-specific context. |
>
> When reporting this finding, always quote the actual justification text (up to ~150 characters) so the release manager can verify the judgment. Use the format:
> > "PTIA justification present on Release WI (text only — no Confluence link). Justification: *\"{quoted text}\"*. [LOOKS GOOD: Justification is specific and credible / MODERATE: Justification appears generic — release manager should confirm this accurately reflects why PT was skipped for this release.]"

| Check | CRITICAL | MODERATE |
|-------|----------|----------|
| PT coverage (PT Plan+Report or PTIA link/text) | Neither present | Both sets present; or PTIA text is placeholder |
| PT Plan approved (when PT Plan present) | Page Accessible = NO | Approved By is empty |
| PT Report approved (when PT Report present) | Page Accessible = NO | Approved By is empty |
| PIT gate (Confluence/SC Wiki page via `pit_url` OR RWI `Custom.ReviewComments` link OR RWI `Custom.PITPlan` field) | None of the three present | Page approver placeholder/empty & Release WI = `Released` |

> **PIT gate rule — triple-source check (updated 2026-10-09)**: Some teams publish a PIT Confluence/SC Wiki page via the version-templated `pit_url` in stream_config.yaml; others embed the PIT page link directly in the Release WI's **Review Comments** field (`Custom.ReviewComments`, rich-text HTML — confirmed as a real, accessible ADO field on the `Release` work item type 2026-10-09); others populate the PIT Plan directly as plain text on the Release WI Change Manifest field (`Custom.PITPlan`). **Any of the three sources satisfies the gate — they are equally acceptable evidence.** The collector (`tda/collectors/release.py`) already resolves these in priority order before producing `pit_result` — do not attempt to re-derive which page was used; `pit_result[0]['PIT Source']` tells you which one resolved it (`stream_config_pit_url` or `rwi_review_comments`). Apply the following logic:
>
> 1. **A PIT Confluence/SC Wiki page is accessible** (`pit_result[0].Page Accessible = YES`) — whether resolved via the stream's configured `pit_url` template OR the RWI's `Custom.ReviewComments` field link — this **takes priority** over the RWI `PITPlan` text field when both are present. Gate met — review the page contents and apply the existing approver placeholder check (MODERATE if approvers are still placeholder text). When `pit_result[0]['PIT Source'] == 'rwi_review_comments'`, mention in the finding that the page link was found in the Release WI's “Review Comments” field rather than the stream's standard PIT URL template.
> 2. **No PIT page accessible via either of the above, but RWI PITPlan field present** (`release_features[0].Custom.PITPlan` is not `NOT FOUND`, not null, and not empty) → gate is still met via the RWI text — this is **not** a CRITICAL or MODERATE finding. Report as **MINOR/Info** with the following mandatory note:
>    > ℹ️ **PIT Plan sourced from Release WI Change Manifest field**: The PIT Plan content is recorded in the `Custom.PITPlan` field of the Release Work Item rather than a Confluence/SC Wiki page. The execution of the PIT plan and its approvals cannot be independently verified by this tool — ownership of PIT execution and approval sign-off remains with the respective application/release team.
> 3. **Both** a PIT page (either source) and the RWI PITPlan field present → the page takes priority (see #1); LOOKS GOOD, and note both are present in the finding.
> 4. **None** of the three present → **CRITICAL**: "No PIT documentation found — the PIT Confluence/SC Wiki page must be accessible (whether linked via stream_config.yaml or the Release WI's Review Comments field) or the PITPlan field on the Release WI Change Manifest must be populated before deployment."

> **Important**: If `Custom.PITPlan` is populated, do **not** raise a CRITICAL or MODERATE finding for `pit_result[0].Page Accessible = NO`. In that case, no PIT page being accessible via either of the two page-based sources is not a gate violation because the PIT requirement is already satisfied through the Release WI text — only a MINOR/Info note is warranted (see #2 above).
>
> Do **not** flag missing, blank, or "n/a" test execution results within any of the three PIT sources as a finding of any severity. The only checks are existence and accessibility.
> - If the resolved page's approver names are still placeholder (e.g. "(AO Delegate)(BO Delegate)"), flag as MODERATE.

> **PIT Confluence/SC Wiki page — approval status check (empty `Approved By`)**: This is separate from the placeholder-text check above and only applies when the PIT gate is being satisfied via an **accessible page** (case #1 or #3 above, from either page-based source — i.e. `pit_result[0].Page Accessible = YES`). Check `pit_result[0].Approved By`:
>
> | Condition | Classification |
> |-----------|----------------|
> | `Approved By` is empty/blank AND Release WI state = `Released` (post-release context) | **MODERATE** — approvals are expected to be in place by this point in the release lifecycle |
> | `Approved By` is empty/blank AND Release WI state = `Prepared Release Candidate` (pre-release context) | **MINOR/Info** — approvals are not yet expected at this stage; not a blocker |
> | `Approved By` is empty/blank AND PIT gate is instead satisfied via the RWI `Custom.PITPlan` field (case #2 above, no page accessible via either page-based source) | **MINOR/Info only, regardless of Release WI state** — approval sign-off ownership sits with the application/release team per the existing triple-source note; do not escalate to MODERATE |
> | `Approved By` is populated | ✅ LOOKS GOOD |
>
> **MODERATE finding text** (post-release, empty approver): "PIT page ('{page_title}') is accessible but has no recorded approver (`Approved By` is empty), and the Release WI is in `Released` state. PIT approval sign-off should have been completed by now — release manager should verify and obtain approval evidence."
>
> **MINOR/Info finding text** (pre-release, empty approver): "PIT page ('{page_title}') has no recorded approver yet (`Approved By` is empty). This is expected at this stage since the Release WI is not yet `Released` — not a blocker, but should be completed before/at deployment."

> **Change Manifest fields — `Custom.ImplementationPlan` / `Custom.BackoutPlan`**: these are no longer evaluated as standalone checks. They are now alternate evidence sources for Gates A/B respectively — see **Implementation & Rollback Documentation — Equivalence Check** under Release Gate Checks above. A team that leaves these Change Manifest fields empty receives **no finding at all** as long as the equivalent AIG/Rollback evidence is present via the Release WI link or build artifact (and vice versa).


### Cross-Document Consistency Check

This check guards against stale documents — Confluence pages accidentally pointing to an older release version or a different stream.

#### Data sources

| Field | Location in JSON |
|-------|-----------------|
| ADO Release title | `release_features[0].System.Title` |
| ADO Release branch | `release_features[0].Branch Id` |
| PT Plan page title | `release_pt_features[0].ReleasePTPlanApproval[*].Page Title` |
| PT Report page title(s) | `release_pt_features[0].ReleasePTReportApproval[*].Page Title` |
| PTIA page title | `release_pt_features[0].ReleasePTIAPageTitle` (when `ReleasePTIAExists = YES`) |
| SNOW description | `snow_features[0].short_description` |
| PIT page title | `pit_result[0].Page Title` (when `Page Accessible = YES`) |

> **Note**: The `Page Title` field is populated by the extractor when a Confluence page is accessible. If `Page Accessible = NO` for any document, skip the consistency check for that document — accessibility itself is already a CRITICAL finding.

#### Version extraction — canonical release version

Before comparing, extract the **canonical release version string** from the ADO Release WI title:

1. Take `release_features[0].System.Title` (e.g. `"Blade Credit and BlateLite Release 14.0"`).
2. Look for a numeric version pattern near the end of the title — any substring matching `\d+\.\d+` (e.g. `14.0`, `116.0`, `455.0`) or `\d+\.\d+\.\d+` (e.g. `185.0.0`).
3. That extracted version is the **canonical version** used for all comparisons below.

Also note the **stream name** from `release_stream` (e.g. `CREDIT`, `FXO`, `RATES`).

#### Check rules

For each accessible Confluence document (PT Plan, PT Report(s), PTIA, PIT):

1. **Version mismatch**: Does the `Page Title` contain the canonical version string?
   - If the page title contains a **different** version number (e.g. title says "Release 13.0" but canonical version is "14.0") → **MODERATE**: "PT Plan Confluence page title appears to reference a different release version (`{page_title}`) — expected version `{canonical_version}`. Verify the correct page is linked on the Release WI."
   - If the page title contains **no recognisable version** at all → **MINOR**: "PT Plan page title (`{page_title}`) does not contain a version number — cannot confirm it relates to this release. Release Manager should verify."
   - If the page title contains the canonical version → ✅ LOOKS GOOD

2. **SNOW description mismatch**: **Skip this check when `snow_enabled` is `false`** (see the SNOW Disabled guardrail above) — there is no CHG record to compare against. Otherwise, compare `snow_features[0].short_description` against `release_features[0].System.Title`:
   - Perform a **case-insensitive fuzzy match** — both should broadly describe the same release. Specifically check whether the version number extracted from the ADO title appears in the SNOW description.
   - If the SNOW description contains a different version number → **MODERATE**: "SNOW change description (`{snow_desc}`) does not match the ADO Release WI title (`{release_title}`). Verify the CHG record is for this release."
   - If they broadly match → ✅ LOOKS GOOD

#### Classification table

| Condition | Classification |
|-----------|---------------|
| Confluence page title contains a **different** version number | MODERATE |
| Confluence page title contains **no** version number | MINOR |
| Confluence page title matches expected version | LOOKS GOOD |
| SNOW description version differs from ADO Release WI version | MODERATE |
| SNOW description matches ADO Release WI | LOOKS GOOD |

#### Summary table (always include)

Add a dedicated sub-section in **Summary Tables**:

```
### Cross-Document Consistency
| Document | Page Title | Expected Version | Version Match | Status |
|----------|-----------|-----------------|--------------|--------|
| PT Plan | {title} | {version} | YES/NO/N/A | ✅/⚠️ |
| PT Report 1 | {title} | {version} | YES/NO/N/A | ✅/⚠️ |
| PT Report 2 | ... | ... | ... | ... |
| PTIA | {title} | {version} | YES/NO/N/A | ✅/⚠️ |
| PIT | {title} | {version} | YES/NO/N/A | ✅/⚠️ |

| Source | Value | Match ADO Release Title | Status |
|--------|-------|------------------------|--------|
| SNOW Description | {snow_desc} | YES/NO | ✅/⚠️ |
```

If `Page Accessible = NO` for a document, display `N/A — page inaccessible` in the Page Title column.

---

### SNOW Change
| Check | CRITICAL |
|-------|----------|
| Change risk | "High" or "Very High" |

> **SNOW state note — REMOVED (2026-07-27)**: Per the Release WI state guardrail (see Release Gate Checks above), do not evaluate or report any alignment/mismatch between the SNOW CHG state and the Release WI state, in any severity.

---

### Cloned Stories — Informational Check

This check is **not a gate blocker** but must always be reported as a dedicated summary point.

A story is considered **cloned** when its `Story Last Comment` matches the pattern:
> `"Copied with all links from #XXXXXXX"` or `"Copied with all attachments and links from #XXXXXXX"`

This is the standard ADO clone comment automatically added when a work item is cloned via the platform.

For every matching story, record:
- The story ID
- The source story ID it was cloned from (the `#XXXXXXX` reference)
- The current state of the cloned story

Include a dedicated sub-section in the **MINOR / Info** section and **Summary Tables**:

```
### Cloned Stories
| Story ID | Cloned From | Current State |
|----------|-------------|--------------|
| XXXXXXX  | #YYYYYYY    | Ready For Release |
...
```

**Summary note**: State the total count and note that cloned stories should be reviewed to ensure the acceptance criteria and description have been updated to reflect the specific scope of work — cloned stories with unchanged content (especially those with high Desc-AC similarity) are a compounded risk.

---

### Negative Test Coverage — Informational Check

This check is **not a gate blocker** but must always be reported as a dedicated summary point.

Scan the following data sources for evidence of negative testing:

1. **`Genie Regression Failures` and Genie scenario names** (inferred from the failure names in `Genie Regression Failures` — also cross-reference the pass count context from `Genie Regression Count`): look for scenarios whose names contain negative-test indicators.
2. **`Test Case Details` — Title fields**: scan titles for negative-test language.
3. **`Stories in Scope` — `Story Last Comment` fields**: look for mentions of negative testing in comments.

#### Negative Test Indicator Keywords
A test or comment is considered to cover negative testing if its text contains any of these (case-insensitive):
- `negative`, `invalid`, `error`, `reject`, `rejection`, `fail`, `failure`, `not found`, `unauthori`, `unauthorised`, `unauthorized`, `forbidden`, `exceed`, `cannot`, `unable`, `should not`, `must not`, `no result`, `empty result`, `no data`, `boundary`, `out of range`, `wrong`, `missing field`, `mandatory field`, `bad request`, `exception`

#### Classification
| Outcome | Classification |
|---------|--------------|
| ≥1 source contains clear negative test evidence | 🔵 MINOR/Info — "Negative testing identified — [sources found]" |
| No evidence of negative testing found in any source | 🔵 MINOR/Info — "No negative test coverage identified. Recommend QA team confirms negative scenarios are covered in manual or Genie regression suites." |

#### Report the following summary point in every report
Include in the **MINOR / Info** section and the **Summary Tables**:

```
### Negative Test Coverage
| Source | Negative Tests Found | Examples |
|--------|---------------------|---------|
| Genie Regression Scenarios | Y / N | [scenario name snippets] |
| Test Case Titles | Y / N | [titles] |
| Story Last Comments | Y / N | [story IDs + comment snippets] |

**Summary**: [One to two sentence assessment of whether negative testing is being practised and any recommendation]
```

---

### Description & Acceptance Criteria Quality — Informational Check

This check is **not a gate blocker** — never classify a finding here as CRITICAL or MODERATE. It is always reported as **MINOR/Info** only.

**Data source**: Raw Description and Acceptance Criteria text is available (HTML-stripped, truncated) alongside the existing presence flags and similarity ratio:
- **Compact Summary**: `stories_summary.all_comments_review[].desc_text` / `.ac_text` (truncated to 400 chars), plus `.desc_present` / `.ac_present`.
- **Full Results**: `story_features[].Description Text` / `.Acceptance Criteria Text` (truncated to 2000 chars), plus `.Desc Present` / `.AC Present`.
- **Bugs**: `bug_features[].System.Description` / `.Microsoft.VSTS.Common.AcceptanceCriteria` (HTML-stripped, truncated to 2000 chars). Bugs frequently have no Acceptance Criteria field configured in ADO — treat `NOT FOUND` as expected, not a gap.

> **Older JSON files**: If a JSON was generated before this text-capture feature was added, `desc_text`/`ac_text` (or `Description Text`/`Acceptance Criteria Text`) will be absent. In that case, skip this check entirely and note: "Description/AC raw text not available in this JSON — re-run the collector to enable the clarity/sufficiency review." Do not treat this as a finding of any severity.

#### What to assess
For each story (and bug, where Description/AC is populated) with `desc_present`/`ac_present` = OK, read the actual text and judge:
- **Clarity**: Is the intent understandable without needing to open the linked ticket/PR? Vague placeholders (e.g. "See attached", "TBD", "N/A", a single word, or text under ~15 characters) indicate low clarity.
- **Sufficiency/elaborateness**: Does the Acceptance Criteria describe concrete, verifiable conditions (e.g. bullet points, Given/When/Then, numbered steps)? A one-line AC on a non-trivial story is a weak signal; a multi-point AC is a strong signal.
- Do **not** re-derive or duplicate the existing Desc-AC similarity/copy-paste check here — that remains covered by the Cloned Stories and Story Desc-AC similarity checks above. This check is purely about the *quality* of the content itself, independent of whether Desc and AC happen to be similar to each other.

#### Classification (always MINOR/Info — never CRITICAL/MODERATE)
| Observation | Report as |
|---|---|
| Description and/or AC text is present but terse, vague, or placeholder-only (e.g. "NA", "TBD", single short sentence on a non-trivial story) | 🔵 MINOR/Info — list the story/bug ID and a short excerpt, recommend the author elaborate |
| Description and AC are both clear, specific, and sufficiently detailed | 🔵 MINOR/Info — note as a positive observation, no action needed |
| Desc/AC raw text unavailable (older JSON, field genuinely not configured for Bugs) | 🔵 MINOR/Info — note as a data-availability observation, not a quality issue |

#### Report the following summary point in every report (when text data is available)
Include in the **MINOR / Info** section and the **Summary Tables**:

```
### Description & Acceptance Criteria Quality
| WI ID | Type | Desc Present | AC Present | Assessment | Note |
|-------|------|--------------|-----------|-----------|------|
```

Populate one row per story/bug that warrants a note (terse/vague/placeholder content). Do **not** list every story individually if most are adequate — summarise: e.g. "20 of 23 stories have clear, sufficiently detailed Description and Acceptance Criteria. 3 stories have terse or placeholder-style content: {list IDs}." End with a one-line **Summary** verdict on overall Desc/AC quality posture for the release.

---

## Report Format

Produce the report in this exact structure:

```
# TDA Checkpoint Report
**Release**: {title} ({release_id})
**Stream**: {release_stream}
**Branch**: {branch}
**CHG**: {chg_id}
**Report Date**: {today}
**Generated By**: {generated_by} <!-- OS username of the person/account running this skill invocation, resolved at report-generation time -->
**Skill Version**: {skill_version} <!-- from this SKILL.md's own metadata.version frontmatter field -->

---

## 🔴 CRITICAL Findings
(list each, or "None")

## 🟡 MODERATE Findings
(list each, or "None")

## 🔵 MINOR / Info
(list each, or "None")

## ✅ LOOKS GOOD
(list passing gates)

---

## Summary Tables

### Associated Builds
| Pipeline | Build ID | Version |
...

> **Version source priority**: For each pipeline, use `pipeline_versions[pipeline_name]` when present and non-empty — this is the authoritative, per-pipeline value, resolved by the collector from either auto-discovery (`promotedImageList` metadata matched to the selected build ID) or explicit `stream_config.yaml` build annotations. Only fall back to the canonical release version (see **Version extraction — canonical release version** under Cross-Document Consistency below), applied uniformly, for pipelines missing from `pipeline_versions` (e.g. a pipeline whose version genuinely could not be resolved by either path, or older JSON files predating this field). If a fallback value is used for any row, note this in a one-line caveat below the table, e.g.: "Version for {pipeline} inferred from the release title (could not be resolved via auto-discovery or stream_config.yaml)."

### Application Approvals
| Approval | Expiry Date | Status |
...

> Omit this table entirely (do not render, do not mention its absence) when the `Application` section is absent/empty — see the Application Approvals guardrail above.

### Application WI — Confluence Post-Approval Checks
| Document | Page Title | Last Modified | Last Approval | Status |
...

> Render one row per entry in `confluence_post_approval_checks`. When the check is not enabled for this stream, render a single row: `N/A — check not enabled for this stream`. Omit the table entirely when `Application` data is absent (same guardrail as Application Approvals above).

### Unit Test Coverage
| Pipeline | Total | Passed | Failed | Others | Delta |
...

> **Unit test rules:**
> - If any pipeline has **Failed > 0**: flag as **CRITICAL** and state — "Failed unit tests exist in {pipeline}. Dev Lead approval must be attached to the Release WI before the release proceeds."
> - If any pipeline has tests categorised as **"Others"**: flag as **CRITICAL** — "Tests marked as 'Others' found in {pipeline}. All tests must have a recognised pass/fail outcome; 'Others' indicates unclassified or misconfigured test results."
> - If any pipeline has **Not Executed > 0**: flag as **CRITICAL** — "Not Executed unit tests exist in {pipeline} ({count} not executed). Dev Lead approval with justification for the non-execution must be attached to the Release WI before the release proceeds."

### Sonar Coverage
| Pipeline | Overall % | Line % | Branch % | New Code % | New Line % | New Branch % | New Code Baseline | Gate Status | Status |
...

> **New Code Baseline column**: Cross-reference `sonar_new_code_periods[]` (keyed by `Pipeline`) and render a `New Code Baseline` cell showing the authoritative reference used for new-code calculations at each pipeline's last Sonar analysis:
> - Entry found, `type == 'REFERENCE_BRANCH'` → show the reference branch name itself, e.g. `Reference branch: release/473.1` (from `value`).
> - Entry found, `type` is `PREVIOUS_VERSION`, `NUMBER_OF_DAYS`, or `SPECIFIC_ANALYSIS` → show the type plainly, e.g. `Previous version` / `Number of days` / `Specific analysis` (optionally with `value`/`date` appended if present) — this is the same condition driving the CRITICAL new-code-coverage finding below, so the cell itself doubles as an at-a-glance explanation of *why* new code coverage may be N/A.
> - No entry for this pipeline (lookup failed, not yet analyzed, or older JSON without this field) → `— N/A`.
> - Pipeline matches the config repo exemption (name contains `fmdc-releases`) → `N/A (exempt)`.
>
> This column is purely informational context alongside the coverage numbers — it does not itself drive a CRITICAL/MODERATE classification (that logic remains entirely in the New Code Coverage N/A rule below, which already consumes the same `sonar_new_code_periods` data).

> **Quality Gate Status column**: Cross-reference `sonar_quality_gate_statuses[]` (keyed by `Pipeline`) and render a `Gate Status` cell for each pipeline:
> - `status = "OK"` → `✅ PASSED`
> - `status = "ERROR"` → `❌ FAILED` — if any failed conditions are present, list their `metricKey` and `actualValue vs errorThreshold` inline (e.g. "new_coverage: 35.2% < 40%"). This does **not** replace the per-metric CRITICAL findings below — it is a convenient at-a-glance indicator alongside the raw numbers.
> - `status = "WARN"` → `⚠ WARNING` with conditions listed
> - `status = "NONE"` → `⚪ NOT COMPUTED` (gate not yet evaluated for this scan)
> - Pipeline absent from `sonar_quality_gate_statuses` (fetch failed or older JSON) → `— N/A`

> **Sonar intentionally skipped for this stream**: Check `sonar_skipped` / `sonar_skip_reason` **before** applying any of the rules below. If `sonar_skipped` is `true` (set when `skip: true` is configured under that stream's `sonar_config` in `stream_config.yaml`, or legacy `{STREAM}_SONAR_CONFIG` in `associated_builds.yaml`, e.g. because the stream has no Sonar project — BCF, ION, KDB), do **not** render the per-pipeline coverage table and do **not** raise any CRITICAL/MODERATE findings for missing or low coverage. Instead:
> - Replace the table with a single informational row/note: "Sonar coverage collection was intentionally skipped for this stream ({sonar_skip_reason}). Not applicable."
> - Classify this as **LOOKS GOOD** (or omit entirely from findings) — it is expected behaviour, not a data gap.
> **CRITICAL — `sonar_skipped` is `false` but `sonar_coverage` is empty**: If `sonar_skipped` is explicitly `false` and the `sonar_coverage` array is empty (null, absent, or `[]`), this is a **CRITICAL** finding — it means Sonar collection was expected to run but returned no data, indicating a collection failure, a misconfigured pipeline reference, or a connectivity issue with SonarQube. Raise a **CRITICAL** finding with the text:
> > "Sonar coverage data is missing despite Sonar not being marked as skipped (`sonar_skipped: false`). This indicates a collection failure — Sonar was expected to run for this stream but returned no results. Verify SonarQube connectivity, confirm the correct project key and build are configured, and re-run the collector before proceeding with the release gate."
> Do **not** classify this as MINOR or informational. This blocks release gate approval in the same way as a coverage failure — a report with no coverage data cannot be used to assert compliance.
>
> **Fallback — `sonar_skipped` absent from the JSON**: Some older `AutoTDAResults_*.json`/`AutoTDASummary_*.json` files were generated before the collector started emitting `sonar_skipped`/`sonar_skip_reason`, so the key may be missing entirely (not just `false`) even for a stream that has `skip: true` configured. Before raising a CRITICAL/MODERATE finding for empty `sonar_coverage` with `sonar_skipped` absent, check whether `stream_config.yaml` (preferred, in the same `scripts/` folder) has `streams.<STREAM>.sonar_config.skip: true`, or fall back to `associated_builds.yaml`'s legacy `{STREAM}_SONAR_CONFIG.skip: true` (known skip streams include BCF, ION, KDB — but always check the file, do not hardcode this list). If found:
> - Treat Sonar as intentionally skipped — do not raise a CRITICAL/MODERATE finding for missing coverage.
> - Report a **MINOR/Info** note: "Sonar coverage is empty and `sonar_skipped` is absent from this JSON, but a `sonar_config.skip: true` (stream_config.yaml) / `{STREAM}_SONAR_CONFIG.skip: true` (associated_builds.yaml) is configured. Treating as an intentional skip. Recommend re-running the collector so the JSON carries `sonar_skipped`/`sonar_skip_reason` directly for future reports."
> If neither `stream_config.yaml` nor `associated_builds.yaml` is accessible or has a `skip: true` entry for the stream, apply the normal rule — empty `sonar_coverage` with `sonar_skipped` absent is a genuine CRITICAL data gap.
>
> **Sonar coverage threshold**: The pass threshold is **≥ 40%** overall coverage. Any pipeline below 40% is a **CRITICAL** finding. Pipelines at or above 40% are considered passing regardless of whether they reach higher values.
>
> **New code coverage**: Always include the `new_coverage`, `new_line_coverage`, and `new_branch_coverage` columns in the Sonar table regardless of their value. If the value is `null` or missing, display **"N/A"**.
>
> **Config repo exemption**: Pipelines whose name contains `fmdc-releases` are configuration/release-descriptor repositories and are **exempt from the new code coverage gate** (both the N/A check and the <40% threshold). When such a pipeline has `new_coverage = null` or a low value, display it in the Sonar table with a `⚪ Exempt (config repo)` status — do **not** raise a CRITICAL finding.
>
> **New code coverage N/A — check `sonar_new_code_periods` FIRST before flagging CRITICAL**: If `new_coverage` is `null`/missing for any pipeline **that is not a config repo (see exemption above)**, do not immediately assume a missing `newCodeReferenceBranch` — cross-reference `sonar_new_code_periods[]` (keyed by `Pipeline`) for that pipeline's **authoritative** period, fetched directly from SonarQube's `/api/measures/component` (`additionalFields=period`) — the period actually applied at the branch's last analysis:
>
> | `sonar_new_code_periods` lookup result | Classification | Finding text |
> |---|---|---|
> | Entry found, `type == 'REFERENCE_BRANCH'` | **MINOR/Info** (not CRITICAL) | "New Code Coverage is N/A for {pipeline}, but SonarQube confirms a reference branch **is** configured (compared to `{value}`). A null/zero new-code measure with a reference branch already in place most likely means there were no new coverable lines since that branch (e.g. a config-only or non-code change) — not a missing-configuration problem. No action needed unless the pipeline owner expects genuine new code to have been analysed." |
> | Entry found, `type` is `PREVIOUS_VERSION`, `NUMBER_OF_DAYS`, or `SPECIFIC_ANALYSIS` | **CRITICAL** | "New Code Coverage is N/A for {pipeline}. SonarQube confirms **no** reference-branch new-code period is configured — the current setting is `{type}`{ (value: `{value}`) if value present}. Without a `REFERENCE_BRANCH`-type new code period, Sonar cannot reliably calculate new code coverage against this release's actual changes, which is a TDA non-compliance risk. The pipeline owner must configure `newCodeReferenceBranch` (typically pointing to `main` or the previous release branch) to obtain accurate new code coverage metrics." |
> | No entry for this pipeline (lookup failed, branch not yet analyzed in Sonar, or older JSON collected before this field existed) | **CRITICAL** (fallback — same as before this check existed) | "New Code Coverage is N/A for {pipeline}. This indicates the `newCodeReferenceBranch` has not been configured in the Sonar project settings. Without a reference branch, Sonar cannot calculate new code coverage, which is a TDA non-compliance risk. The pipeline owner must configure `newCodeReferenceBranch` (typically pointing to `main` or the previous release branch) to obtain accurate new code coverage metrics. (Note: the authoritative `sonar_new_code_periods` check could not confirm this — re-run the collector or verify manually in SonarQube if in doubt.)" |
>
> Apply the CRITICAL finding to every non-exempt pipeline where `new_coverage` is null **and** the `sonar_new_code_periods` lookup does not confirm a `REFERENCE_BRANCH` type — list them all in a single consolidated finding if multiple pipelines are affected. List any MINOR/Info "reference branch confirmed" pipelines separately, do not merge them into the CRITICAL finding.
>
> New code coverage of < 40% (when a real value is present) is also a **CRITICAL** finding using the same threshold, except for pipelines matching the config repo exemption. The `sonar_new_code_periods` check above only applies to the **N/A** case — it does not soften a genuine below-threshold new code coverage value.

### Sonar Quality Gate Assignment — Gate Check

**Data source**: `sonar_quality_gates[]` (both full and compact JSON) — one entry per pipeline with `Pipeline`, `quality_gate_name`, and `is_default` (bool). Fetched via `GET /api/qualitygates/get_by_project?project={sonar_project_key}`. Skip this check entirely (same rule as Sonar Coverage above) when `sonar_skipped` is `true` — it only applies to pipelines/apps with Sonar enabled.

> **Determine the required gate for this stream first**: Read `streams.<STREAM>.sonar_config.required_quality_gate` from `stream_config.yaml`. If the key is present and non-empty, use that value as `{required_quality_gate}`; otherwise default to `ESDLC-Sonarway-managed`. The comparison is always **case-insensitive**. When a non-default gate is in effect, include a **MINOR/Info** note in the report: "This stream has an approved Quality Gate exception: the required gate is '{required_quality_gate}' (overridden from the organisation default 'ESDLC-Sonarway-managed' via `stream_config.yaml`)."

> **CRITICAL — Quality Gate must be `{required_quality_gate}`**: For every pipeline present in `sonar_quality_gates[]`, compare `quality_gate_name` to `{required_quality_gate}` **case-insensitively**. If it does not match, raise a **CRITICAL** finding:
> > "Sonar Quality Gate mismatch for {pipeline}: assigned gate is '{quality_gate_name}', expected '{required_quality_gate}'. This pipeline is not using the required Quality Gate — the pipeline owner must reassign it in SonarQube project settings before the release proceeds."
>
> Consolidate into a single CRITICAL finding listing all non-compliant pipelines if more than one is affected. Pipelines whose `quality_gate_name` matches `{required_quality_gate}` (case-insensitively) pass this check — report them under LOOKS GOOD / the summary table, not as a finding.

> **Older JSON files**: If a JSON was generated before this feature was added, `sonar_quality_gates` will be absent or an empty list even though `sonar_coverage` has data. In that case, note as **MINOR/Info**: "Sonar Quality Gate data not available in this JSON — re-run the collector to enable this gate check." Do not treat this as a CRITICAL/MODERATE finding — the gate simply could not be evaluated.

> **Per-pipeline fetch failures**: A pipeline may be missing from `sonar_quality_gates` even when it has a `sonar_coverage` entry (the quality gate lookup failed independently, e.g. a stale/incorrect Sonar project key in `stream_config.yaml`'s `sonar_keys` — this happened for `51527-dtp-sabre-entitlement_maven_pipeline` in RULES until the key was corrected on 2026-07-14). Report any such gap as **MINOR/Info**: "Quality Gate could not be determined for {pipeline} — verify the Sonar project key in `stream_config.yaml`/`associated_builds.yaml`. This pipeline could not be checked against the required Quality Gate." Do not escalate to CRITICAL/MODERATE for the fetch failure itself — but note that compliance for that pipeline remains unverified until the key is fixed and the collector re-run.

#### What to report
```
### Sonar Quality Gate Assignment
| Pipeline | Quality Gate | Matches {required_quality_gate}? | Gate Status |
|----------|--------------|----------------------------------|-------------|
```
One row per pipeline in `sonar_quality_gates[]`. `Matches {required_quality_gate}?` = "✅ Yes" (case-insensitive match) or "❌ No — CRITICAL". `Gate Status` = the `status` value from the matching entry in `sonar_quality_gate_statuses[]` rendered the same way as in the Sonar Coverage table (`✅ PASSED`, `❌ FAILED`, `⚠ WARNING`, `⚪ NOT COMPUTED`, `— N/A`). List any pipeline present in `sonar_coverage` but absent from `sonar_quality_gates` as a separate note (fetch failure — see above), not a blank table row.

End with a one-line **Summary**: e.g. "7/7 pipelines use the required '{required_quality_gate}' Quality Gate." or "5/7 pipelines compliant; 2 pipelines ({list}) use a non-required gate — CRITICAL, must be reassigned before release."

### Sonar Exclusions

**Data source**: `sonar_exclusions[]` (both full and compact JSON) — one entry per pipeline with `Pipeline`, `sonar.exclusions`, `sonar.coverage.exclusions`, `sonar.test.exclusions`, `sonar.cpd.exclusions` (each a list of glob patterns, empty if not configured). Fetched via `GET /api/settings/values?component={sonar_project_key}&keys=sonar.exclusions,sonar.coverage.exclusions,sonar.test.exclusions,sonar.cpd.exclusions`. Skip this section entirely (same rule as Sonar Coverage above) when `sonar_skipped` is `true`.

This section is **informational only** — it does not itself raise a CRITICAL/MODERATE finding. Its purpose is to give context for the Sonar Coverage numbers above: a pipeline with broad `sonar.coverage.exclusions` patterns may show an artificially inflated coverage percentage because large portions of the codebase are excluded from the calculation.

> **Non-empty `sonar.coverage.exclusions`**: If a pipeline has one or more patterns configured for `sonar.coverage.exclusions`, note it as **MINOR/Info**: "Pipeline {pipeline} has coverage exclusions configured ({patterns}). The reported coverage % may not reflect the full codebase — confirm the exclusions are legitimate (e.g. generated code, test fixtures) and not being used to mask untested production code."
>
> **Older JSON files / fetch failures**: If a JSON was generated before this feature was added, `sonar_exclusions` will be absent or empty even though `sonar_coverage` has data — note as **MINOR/Info**: "Sonar exclusions data not available in this JSON — re-run the collector to enable this check." A pipeline present in `sonar_coverage` but absent from `sonar_exclusions` indicates the exclusions lookup failed independently; note as **MINOR/Info** rather than escalating.

#### What to report
```
### Sonar Exclusions
| Pipeline | sonar.exclusions | sonar.coverage.exclusions | sonar.test.exclusions | sonar.cpd.exclusions |
|----------|-------------------|-----------------------------|--------------------------|-------------------------|
```
One row per pipeline in `sonar_exclusions[]`. Display each list joined with `, `, or "None" if empty. Follow with any MINOR/Info notes for non-empty `sonar.coverage.exclusions` per the rule above.

### Genie Regression
| Total Scenarios | Passed | Failed | Failure Rate |
...

### Stories in Scope
| Story ID | State | Description | AC | Similarity % | App ID | Story Type |
...

> **Story state note**:
> - For post-release reports (`Release WI = Released`), `Done` is expected and should not be listed as "not ready".
> - Only for pre-release reports (`Release WI = Prepared Release Candidate`) should non-`Ready For Release` story states be surfaced for review.

### Story Field Completeness
| Metric | Count |
|--------|-------|
| Stories with ApplicationID populated | X / total |
| Stories with StoryType populated | X / total |
| Stories missing ApplicationID | X |
| Stories missing StoryType | X |

### Stories with Open/Unresolved Last Comments
List stories where the last comment suggests something is still pending, blocked, or unresolved.
| Story ID | State | Last Comment Snippet | Risk |
...
(or "None identified" if all comments indicate closure or are empty)

### Traceability Coverage
All five coverage sources, each as its own row, plus the combined overall-coverage row (see Analysis Rules above for how to compute the two Genie/Automation rows):
| Testing Type | Stories with ≥1 Source Linked | Stories Missing | Status |
|---|---|---|---|
| ADO Manual System Testing | X | Y | Informational |
| ADO Manual Integration Testing | X | Y | Informational |
| ADO Manual Acceptance Testing | X | Y | Informational |
| Genie / Automation System Testing | X | Y | Informational |
| Genie / Automation Integration Testing | X | Y | Informational |
| **Any of 5 sources (overall coverage)** | X | Y | status |

### Traceability Coverage Gaps
Stories with **none** of the five coverage sources (ADO manual System/Integration/Acceptance Testing, Genie ST, Genie IT)
**after** applying the Genie Automation Cross-Check:
| Story ID | ADO System | ADO Integration | ADO Acceptance | Genie ST | Genie IT |
...
(or "All stories have at least one coverage source" if no gaps found)

### Traceability Gaps Resolved via Genie Automation
Stories that had no ADO-linked System/Integration/Acceptance Testing test case, but have automated Genie regression
evidence in `genie_story_type_breakdown` establishing traceability:
| Story ID | Genie ST Scenarios | Genie IT Scenarios |
...
(or "None — no gaps were resolved via Genie automation" if not applicable)

> **Data-limitation caveat**: only applies to legacy input JSON files collected before `genie_story_type_breakdown` existed
> (only `genie_story_tag_split` present). In that case, state whether the release-wide `@tt_IT` count in `genie_tag_split`
> is materially lower than `@tt_ST` (a per-story ST vs IT breakdown cannot be determined from `genie_story_tag_split` alone
> — though this does not affect the pass/fail traceability gate itself, since either type satisfies coverage). Re-run the
> collector, or use `python analyze_genie_scenario_tags.py <release_id>` (in the same `scripts/` directory) to backfill a
> definitive per-story ST/IT breakdown for such legacy files.

### Automation Coverage
| Metric | Count (ADO) | Count (Genie / Automation Tool) |
|--------|-------------|----------------------------------|
| Stories with automated coverage | X | X |
| Stories with 0 automated coverage | X | X |
| Total stories in traceability | X | X |

> **Automation Analysis**: [Insert one of the analysis statements from the Traceability rules — no coverage from either source / Genie coverage higher than ADO (expected pattern) / ADO automated but no Genie evidence (verify) / inconsistent with Testing Types]

### Bugs in Scope
| Bug ID | State | Test Phase | Env |
...

### Cloned Stories
| Story ID | Cloned From | Current State |
...
(or "No cloned stories identified" if none found)

### Manual Test Execution Summary
| Test Case ID | Title | Outcome | Steps Passed | Steps Total | Evidence Present | Issues |
|-------------|-------|---------|-------------|-------------|-----------------|--------|
...
(or "Test Results array is empty — no execution data to report" with CRITICAL flag)

### Regression Failure Re-Test
| Genie Failures | Re-Test TC Found | TC Title | Outcome | Evidence Present |
|---------------|-----------------|---------|---------|-----------------|
...

### Test Results Summary
| Test Name | Outcome | Comment |
...

### Negative Test Coverage
| Source | Negative Tests Found | Examples |
|--------|---------------------|---------|
| Genie Regression Scenarios | Y / N | [scenario name snippets or "None identified"] |
| Test Case Titles | Y / N | [titles or "None identified"] |
| Story Last Comments | Y / N | [story IDs + comment snippets or "None identified"] |

**Summary**: [1–2 sentence assessment]

### Description & Acceptance Criteria Quality
| WI ID | Type | Desc Present | AC Present | Assessment | Note |
|-------|------|--------------|-----------|-----------|------|
...
(or "Description/AC raw text not available in this JSON — re-run the collector to enable this review" if `desc_text`/`ac_text` fields are absent)

**Summary**: [1–2 sentence assessment of overall Desc/AC clarity and sufficiency across stories/bugs in scope — informational only, not a gate]

### Appendix: Stream Configuration Snapshot
| Setting | Value | Description |
|---------|-------|-------------|
...

> **Purpose**: records the `streams.<{release_stream}>` block read from `stream_config.yaml` during Stream Name Validation, so the exact optional checks/feature toggles in effect for this specific report are preserved even though the config file itself is a local, frequently-uncommitted working copy. This is informational/provenance only — never a CRITICAL/MODERATE gate, and it does not duplicate the per-check guardrail notes already raised elsewhere (e.g. "SNOW disabled for this stream") — those remain the authoritative findings; this table is simply the durable raw-settings record for later reference/data-mining.
>
> Populate one row per relevant key actually present for this stream (omit keys that are entirely absent from this stream's block rather than inventing a default row for a key the stream never set, except where a documented default is noted below):
> | Setting | Typical values | Note |
> |---|---|---|
> | `pit_url` | *(configured)* / *(not configured — `~`/absent)* | Show whether a PIT Confluence template is configured for this stream — do not print the full URL (keep the table compact; the resolved page title/accessibility already appears in the PIT findings). |
> | `genie_enabled` | `true` / `false` | Whether Genie regression collection runs for this stream. |
> | `genie_test_management_app_id` | *(value)* / *(not set)* | Only shown when `genie_enabled: false` — opt-in alternate Genie API. |
> | `snow_enabled` | `true` / `false` / *(not set — falls back to `.env` default)* | |
> | `story_comments_enabled` | `true` / `false` (default `false`) | Drives the Story Last Comment closure check. |
> | `po_reprioritization_check_enabled` | `true` / `false` (default `false`) | Drives the Post-Prioritization Description/AC Change Check. |
> | `application_confluence_post_approval_check_enabled` | `true` / `false` (default `false`) | Drives the Application WI Confluence Post-Approval Check. |
> | `builds_from_latest_pipeline_field` | `true` / `false` (default `false`) | Alternate build-discovery strategy (Custom.LatestPipelineRuns). |
> | `branch_version_fallback_enabled` | `true` / `false` (default `false`) | Enables the `.0`-suffix release-train branch fallback + unfiltered Strategy 4. |
> | `artifactory_build_discovery_enabled` | `true` / `false` (default `false`) | Artifactory build-info properties discovery path (requires `sonar_config.auto_discovery: true` too). |
> | `sonar_config.skip` | `true` / `false` (default `false`) | Whether Sonar collection is intentionally skipped for this stream. |
> | `sonar_config.auto_discovery` | `true` / `false` (default `true`) | Whether component builds are auto-discovered vs. taken from the manual `builds:` map. |
> | `sonar_config.required_quality_gate` | *(override name)* / *(default `ESDLC-Sonarway-managed`)* | Only show as an override row if explicitly set; otherwise omit (the default already governs the Sonar Quality Gate Assignment table above). |
> | `regression_config.skip` | `true` / `false` | Only relevant/shown when `genie_enabled: false`. |
>
> Do **not** include the `builds:`/`sonar_keys:` maps (pipeline-to-build-ID/Sonar-project-key mappings) in this table — those are release-specific plumbing, not feature toggles, and are already represented by the Associated Builds table above.
>
> **Caveat — always include this note directly under the table**: "This snapshot reflects `stream_config.yaml` as read on the machine that generated this report, at report-generation time. Since this file is a local working copy that is not always committed back to `main`, it may differ from the configuration in effect when the underlying JSON was collected (if collected on a different machine or at a different time), or from another engineer's local copy."

---

## Gate Verdict
**PASS / CONDITIONAL PASS / FAIL** — one-line justification
```

---

## Step 3 — Generate HTML Report

After producing the markdown report above, generate a **self-contained HTML file** and save it to the user's Downloads folder:

**Output path**:
- **Windows**: `C:\Users\{username}\Downloads\TDAReport_{STREAM}_{release_id}.html`
- **macOS**: `/Users/{username}/Downloads/TDAReport_{STREAM}_{release_id}.html`

Resolve `{username}` from the environment (`$env:USERNAME` on Windows, `$USER` on macOS). Detect the OS at runtime and use the appropriate path.

### Skill version (traceability)

Every report must be stamped with the version of **this** `dtp-tda-report` skill that generated it, so that if a user reports an issue with a report, the exact skill version in use at the time can be identified.

`{skill_version}` = the `metadata.version` value in this SKILL.md's own YAML frontmatter (currently `1.11.1`). Read it directly from the top of the file you are currently executing — do not hardcode a remembered value, since it changes as the skill is updated. This is independent of the release/report version (`{release_id}`, canonical release version, etc.) — it identifies the *tooling*, not the *release being assessed*.

### Report Provenance (Generated By)

Every report must also record **who generated it** — the person (or service account) running this skill invocation right now, as distinct from `{skill_version}` (which tooling version) and the Release WI's own approvers (who approved the release). This is independent of `ado_organization`/`ado_project` and is **not** read from the input JSON at all — it reflects the local environment of the machine actually producing this HTML file.

Resolve `{generated_by}` from the environment, same mechanism already used to resolve `{username}` for the output path below: `$env:USERNAME` on Windows, `$USER` on macOS/Linux (`os.environ.get('USERNAME', os.environ.get('USER', 'Unknown'))` in the write script). If neither environment variable is available, use the literal string `Unknown` rather than leaving the placeholder unresolved or guessing a name.

### ⚠️ MANDATORY FORMAT — Do NOT deviate

The HTML output **must** use the exact CSS classes, colour values, element structure, and section order defined below. Do not invent alternative layouts, colour schemes, card styles, or grid structures. Every report must look identical in structure — only the data content changes.

> **Collapsible Summary Tables section**: The Summary Tables section uses a native HTML `<details>`/`<summary>` element instead of a plain `<div>` so the reader can collapse/expand it — no JavaScript is required, this works in any modern browser and keeps the report fully self-contained. It defaults to `open` (expanded), matching prior report behaviour, so nothing is hidden unless the reader chooses to collapse it. Do not add JavaScript-based toggle logic — the native `<details>` element already provides this.

### Canonical CSS (copy verbatim — do not modify)

```css
body{font-family:Segoe UI,Arial,sans-serif;margin:0;padding:0;background:#f4f6f9;color:#222;}
.header{background:#1a3a5c;color:white;padding:24px 32px;}
.header h1{margin:0 0 6px 0;font-size:22px;}
.header .meta{font-size:13px;opacity:.85;line-height:1.8;}
.section{margin:20px 32px;}
h2{font-size:15px;margin-bottom:10px;padding:8px 14px;border-radius:4px;color:white;}
.critical h2{background:#c0392b;}
.moderate h2{background:#e67e22;}
.minor h2{background:#2980b9;}
.looksGood h2{background:#27ae60;}
.tables h2{background:#34495e;}
.finding{background:white;padding:10px 14px;margin-bottom:8px;border-radius:3px;font-size:14px;border-left:4px solid #ccc;}
.critical .finding{border-color:#c0392b;}
.moderate .finding{border-color:#e67e22;}
.minor .finding{border-color:#2980b9;}
.looksGood .finding{border-color:#27ae60;}
table{width:100%;border-collapse:collapse;background:white;font-size:13px;margin-bottom:20px;}
th{background:#1a3a5c;color:white;padding:8px 10px;text-align:left;}
td{padding:7px 10px;border-bottom:1px solid #e8e8e8;}
tr:nth-child(even) td{background:#f9f9f9;}
.verdict{margin:24px 32px;padding:20px 24px;border-radius:6px;font-size:17px;font-weight:bold;color:white;text-align:center;}
.verdict.blocked{background:#c0392b;}
.verdict.conditional{background:#e67e22;}
.verdict.pass{background:#27ae60;}
.badge{display:inline-block;border-radius:12px;padding:2px 10px;font-size:12px;color:white;margin-left:8px;}
.c-badge{background:#922b21;}
.m-badge{background:#a04000;}
.i-badge{background:#1a5276;}
.g-badge{background:#1e8449;}
.section-title{font-weight:600;font-size:14px;margin:16px 0 6px 0;color:#444;}
.warn{color:#c0392b;font-weight:bold;}
.staleness-banner{margin:0;padding:12px 32px;background:#fdf2e3;color:#7a4a00;font-size:13.5px;font-weight:600;text-align:center;border-bottom:3px solid #e6a23c;}
.ok{color:#27ae60;font-weight:bold;}
.na{color:#888;font-style:italic;}
.footer{text-align:center;padding:16px;font-size:11px;color:#999;border-top:1px solid #ddd;margin-top:8px;}
.info-note{background:#e8f4fd;border-left:4px solid #2980b9;padding:10px 14px;margin:8px 0 12px 0;font-size:13px;border-radius:3px;}
.rule-box{background:#eaf4fb;border-left:4px solid #2980b9;padding:10px 14px;margin:8px 0 16px 0;font-size:13px;border-radius:3px;}
details.section{margin:20px 32px;}
details.tables summary{font-size:15px;margin-bottom:10px;padding:8px 14px;border-radius:4px;color:white;background:#34495e;cursor:pointer;user-select:none;list-style:revert;}
details.tables summary:hover{opacity:.9;}
details.tables[open] summary{margin-bottom:10px;}
details.tables .details-body{padding-top:4px;}
/* ── Remediation annotation ── */
.rem-btn{margin-top:8px;padding:3px 10px;font-size:11px;border:1px solid #2980b9;background:white;color:#2980b9;border-radius:3px;cursor:pointer;float:right;}
.rem-btn:hover{background:#eaf4fb;}
.rem-panel{display:none;margin-top:8px;background:#f0faf4;border:1px solid #27ae60;border-radius:4px;padding:10px 12px;font-size:13px;clear:both;}
.rem-panel.open{display:block;}
.rem-panel label{display:block;font-size:11px;color:#555;margin-bottom:2px;margin-top:6px;}
.rem-panel input,.rem-panel textarea,.rem-panel select{width:100%;box-sizing:border-box;border:1px solid #ccc;border-radius:3px;padding:4px 7px;font-size:13px;font-family:inherit;}
.rem-panel textarea{resize:vertical;min-height:56px;}
.rem-panel .rem-actions{margin-top:8px;display:flex;gap:8px;}
.rem-panel .rem-save{background:#27ae60;color:white;border:none;border-radius:3px;padding:4px 14px;cursor:pointer;font-size:12px;}
.rem-panel .rem-cancel{background:#e0e0e0;color:#333;border:none;border-radius:3px;padding:4px 12px;cursor:pointer;font-size:12px;}
.rem-recorded{margin-top:8px;background:#eafaf1;border-left:4px solid #27ae60;padding:8px 12px;border-radius:3px;font-size:12px;clear:both;}
.rem-recorded .rem-meta{font-size:11.5px;color:#444;margin-bottom:5px;}
.rem-recorded .rem-note{font-size:13px;color:#222;}
.rem-status-badge{display:inline-block;padding:1px 8px;border-radius:10px;font-size:10.5px;font-weight:700;color:white;}
.rem-status-resolved{background:#27ae60;}
.rem-status-unresolved{background:#c0392b;}
.rem-status-false_positive{background:#2980b9;}
.rem-status-workaround{background:#8e44ad;}
.rem-toolbar{background:#1a3a5c;padding:8px 32px;display:flex;align-items:center;gap:14px;}
.rem-toolbar span{color:#aed6f1;font-size:12px;flex:1;}
.rem-toolbar button{padding:5px 14px;font-size:12px;border:none;border-radius:3px;cursor:pointer;}
.rem-export-btn{background:#27ae60;color:white;}
.rem-export-btn:hover{background:#1e8449;}
.rem-export-btn.locked{background:#95a5a6;}
.rem-export-btn.locked:hover{background:#95a5a6;}
.rem-missing{outline:3px solid #c0392b!important;outline-offset:2px;animation:remPulse 1.2s ease-in-out 3;}
@keyframes remPulse{0%,100%{background-color:transparent;}50%{background-color:#fdecea;}}
.rem-setname-btn{background:rgba(255,255,255,.15);color:white;border:1px solid rgba(255,255,255,.3)!important;}
.rem-setname-btn:hover{background:rgba(255,255,255,.25);}```

### Canonical HTML Shell (copy verbatim — substitute only the `{placeholders}`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>TDA Report &mdash; {title}</title>
<style>
/* === PASTE THE CANONICAL CSS ABOVE HERE VERBATIM === */
</style>
</head>
<body>

<!-- ⚠️ DO NOT OMIT — REQUIRED FOR REMEDIATION SYSTEM: the rem-toolbar div below provides the
     "Set Reviewer Name" and "Save Annotated Report" buttons visible at the top of every report.
     Omitting it silently removes the entire annotation capability with no visible error in the output. -->
<div class="rem-toolbar">
  <span id="remToolbarInfo">&#128221; Remediation mode &mdash; click <strong>Remediate</strong> on any finding to record an annotation, then export.</span>
  <button class="rem-setname-btn" onclick="remSetName()">&#128100; Set Reviewer Name</button>
  <button class="rem-export-btn" onclick="remExport()">&#11015; Save Annotated Report</button>
</div>

<div class="header">
  <h1>TDA Checkpoint Report &mdash; {title}</h1>
  <div class="meta">
    <strong>Release ID:</strong> {release_id} &nbsp;|&nbsp; <strong>Stream:</strong> {stream} &nbsp;|&nbsp; <strong>Branch:</strong> {branch}<br>
    <strong>CHG:</strong> {chg} &nbsp;|&nbsp; <strong>SNOW State:</strong> {snow_state} &nbsp;|&nbsp; <strong>Release WI State:</strong> {wi_state} &nbsp;|&nbsp; <strong>Report Date:</strong> {date}<br>
    <strong>Skill Version:</strong> {skill_version} &nbsp;|&nbsp; <strong>Collector Version:</strong> {collector_version} &nbsp;|&nbsp; <strong>Version Drift:</strong> {drift_indicator}<br>
    <strong>Generated By:</strong> {generated_by}
  </div>
</div>
{staleness_banner_html}

<div class="section critical">
  <h2>&#128308; CRITICAL Findings <span class="badge c-badge">{critical_count}</span></h2>
  <!-- One <div class="finding"> per CRITICAL item -->
  {critical_findings_html}
</div>

<div class="section moderate">
  <h2>&#128993; MODERATE Findings <span class="badge m-badge">{moderate_count}</span></h2>
  <!-- One <div class="finding"> per MODERATE item -->
  {moderate_findings_html}
</div>

<div class="section minor">
  <h2>&#128309; MINOR / Info <span class="badge i-badge">{minor_count}</span></h2>
  <!-- One <div class="finding"> per MINOR/Info item -->
  {minor_findings_html}
</div>

<div class="section looksGood">
  <h2>&#9989; Looks Good <span class="badge g-badge">{looksGood_count}</span></h2>
  <!-- One <div class="finding"> per passing gate -->
  {looksGood_findings_html}
</div>

<details class="section tables" open>
  <summary>&#128202; Summary Tables <em style="font-weight:normal;font-size:12px;opacity:.8;">(click to collapse/expand)</em></summary>
  <div class="details-body">

  <div class="section-title">Associated Builds</div>
  <table>
    <tr><th>Pipeline</th><th>Build ID</th><th>Version</th></tr>
    {associated_builds_rows}
  </table>

  <div class="section-title">Application WI &mdash; Confluence Post-Approval Checks</div>
  <div class="rule-box">&#8505;&#65039; <strong>Post-approval edit check</strong>: Compares each linked Confluence document&rsquo;s last-modified timestamp against the most recent approver comment. Only populated when <code>application_confluence_post_approval_check_enabled: true</code> in <code>stream_config.yaml</code>.</div>
  <!-- Omit this block entirely when Application data is absent (same guardrail as Application Approvals table).
       When check is not enabled, render a single spanning row with class="na": N/A — check not enabled for this stream. -->
  <table>
    <tr><th>Document</th><th>Page Title</th><th>Last Modified</th><th>Last Approval</th><th>Status</th></tr>
    {app_confluence_post_approval_rows}
  </table>

  <div class="section-title">Unit Test Coverage</div>
  <table>
    <tr><th>Pipeline</th><th>Build ID</th><th>Total</th><th>Passed</th><th>Failed</th><th>Not Executed</th><th>Others</th><th>Status</th></tr>
    {unit_test_rows}
  </table>

  <div class="section-title">Sonar Coverage</div>
  <div class="rule-box">&#8505;&#65039; <strong>New Code Coverage</strong>: Pipelines showing N/A for new code metrics have not detected changed lines against the configured Sonar baseline &mdash; this is cross-checked against SonarQube's own New Code Period configuration (<code>sonar_new_code_periods</code>) before being flagged as a missing <code>newCodeReferenceBranch</code>: a reference branch already configured with no new coverable lines is MINOR/Info, not CRITICAL. The <strong>New Code Baseline</strong> column shows the actual reference branch/period each pipeline's new-code metrics were computed against. The overall coverage threshold (&ge;40%) applies to the overall coverage column.</div>
  <!-- If sonar_skipped is true, replace this table entirely with a single note, e.g.:
  <div class="finding">Sonar coverage collection was intentionally skipped for this stream ({sonar_skip_reason}). Not applicable.</div>
  Only render the table below when sonar_skipped is false. -->
  <table>
    <tr><th>Pipeline</th><th>Overall %</th><th>Line %</th><th>Branch %</th><th>New Code %</th><th>New Line %</th><th>New Branch %</th><th>New Code Baseline</th><th>Status</th></tr>
    {sonar_rows}
  </table>

  <div class="section-title">Sonar Quality Gate Assignment</div>
  <div class="rule-box">&#8505;&#65039; <strong>CRITICAL gate</strong> — every pipeline with Sonar enabled must use the required <code>{required_quality_gate}</code> Quality Gate (matched case-insensitively). Any other gate name is a CRITICAL finding. Fetch failures (pipeline missing from this table) are MINOR/Info only, not a CRITICAL.</div>
  <table>
    <tr><th>Pipeline</th><th>Quality Gate</th><th>Matches {required_quality_gate}?</th></tr>
    {sonar_quality_gate_rows}
  </table>

  <div class="section-title">Genie Regression</div>
  <table>
    <tr><th>Total</th><th>Passed</th><th>Failed</th><th>Failure Rate</th><th>Status</th></tr>
    {genie_summary_row}
  </table>

  <div class="section-title">Genie Failures</div>
  <table>
    <tr><th>Scenario</th><th>Status</th></tr>
    {genie_failure_rows}
  </table>

  <div class="section-title">Regression Failure Re-Test</div>
  <table>
    <tr><th>Genie Failures</th><th>Re-Test TC Found</th><th>TC Title</th><th>Outcome</th><th>Evidence Present</th></tr>
    {retest_row}
  </table>

  <div class="section-title">Manual Test Execution Summary</div>
  <table>
    <tr><th>Test Case ID</th><th>Title</th><th>Outcome</th><th>Steps Passed</th><th>Steps Total</th><th>Evidence Present</th><th>Issues</th></tr>
    {test_results_rows}
  </table>

  <div class="section-title">Stories with Open / Unresolved Last Comments</div>
  <table>
    <tr><th>Story ID</th><th>State</th><th>Last Comment (snippet)</th><th>Risk Indicator</th></tr>
    {open_comment_rows}
  </table>

  <div class="section-title">Stories Not in Expected Pre-Release State</div>
  <table>
    <tr><th>Story ID</th><th>State</th><th>Note</th></tr>
    {not_ready_rows}
  </table>

  <div class="section-title">High Desc-AC Similarity (&gt;85%)</div>
  <table>
    <tr><th>Story ID</th><th>State</th><th>Similarity %</th><th>Risk</th></tr>
    {similarity_rows}
  </table>

  <div class="section-title">Traceability Coverage</div>
  <table>
    <tr><th>Testing Type</th><th>Stories with &ge;1 TC Linked</th><th>Stories Missing</th><th>Status</th></tr>
    {traceability_rows}
  </table>

  <div class="section-title">Automation Coverage</div>
  <table>
    <tr><th>Metric</th><th>Count (ADO)</th><th>Count (Genie / Automation Tool)</th></tr>
    {automation_rows}
  </table>

  <div class="section-title">Bugs in Scope</div>
  <table>
    <tr><th>Bug ID</th><th>State</th><th>Test Phase</th><th>Environment</th></tr>
    {bug_rows}
  </table>

  <div class="section-title">Cloned Stories</div>
  <table>
    <tr><th>Story ID</th><th>Cloned From</th><th>Current State</th></tr>
    {cloned_rows}
  </table>

  <div class="section-title">Negative Test Coverage</div>
  <table>
    <tr><th>Source</th><th>Negative Tests Found</th><th>Examples</th></tr>
    {negative_test_rows}
  </table>

  <div class="section-title">Description &amp; Acceptance Criteria Quality</div>
  <div class="rule-box">&#8505;&#65039; <strong>Informational only</strong> — never a CRITICAL/MODERATE gate. Assesses clarity/sufficiency of Description and Acceptance Criteria text, independent of the copy-paste similarity check above.</div>
  <table>
    <tr><th>WI ID</th><th>Type</th><th>Desc Present</th><th>AC Present</th><th>Assessment</th><th>Note</th></tr>
    {desc_ac_quality_rows}
  </table>

  <div class="section-title">Cross-Document Consistency</div>
  <table>
    <tr><th>Document</th><th>Page Title</th><th>Expected Version</th><th>Version Match</th><th>Status</th></tr>
    {cross_doc_page_rows}
  </table>
  <table>
    <tr><th>Source</th><th>Value</th><th>Match ADO Release Title</th><th>Status</th></tr>
    {cross_doc_snow_row}
  </table>

  </div>
</details>

<details class="section tables">
  <summary>&#128230; Appendix: Stream Configuration Snapshot <em style="font-weight:normal;font-size:12px;opacity:.8;">(click to expand)</em></summary>
  <div class="details-body">

  <div class="rule-box">&#8505;&#65039; This snapshot reflects <code>stream_config.yaml</code>'s <code>streams.{stream}</code> block as read on the machine that generated this report, at report-generation time. Since this file is a local working copy that is not always committed back to <code>main</code>, it may differ from the configuration in effect when the underlying JSON was collected (if collected on a different machine or at a different time), or from another engineer's local copy. Informational/provenance only &mdash; never a CRITICAL/MODERATE gate.</div>
  <table>
    <tr><th>Setting</th><th>Value</th><th>Description</th></tr>
    {stream_config_rows}
  </table>

  </div>
</details>

<div class="verdict {verdict_class}">{verdict_text}</div>

<div class="footer">Generated by dtp-tda-report skill v{skill_version} &nbsp;|&nbsp; {stream} Release {release_id} &nbsp;|&nbsp; {date}</div>

<!-- ⚠️ DO NOT OMIT — REQUIRED FOR REMEDIATION SYSTEM: the entire <script> block below (from here
     to </script>) must be included verbatim. It injects the Remediate button on every finding,
     powers the Set Reviewer Name prompt, and drives the Save Annotated Report export.
     Omitting or truncating this block silently disables all annotation features.
     MANDATORY ANNOTATION GATE: every finding inside <div class="section critical"> or
     <div class="section moderate"> (excluding the "None identified" zero-count placeholder) is
     tagged data-rem-mandatory="true" and MUST have a saved annotation before remExport() will
     proceed — Save Annotated Report blocks with an alert and highlights any unannotated
     CRITICAL/MODERATE findings in red if the user tries to export early. This enforces that every
     CRITICAL/MODERATE observation is explicitly owned (Resolved/Unresolved/False Positive/Workaround
     + a note) before a reviewer can save the report, even if the finding itself remains Unresolved. -->
<script>
// ── Remediation annotation system ──
var _remName = localStorage.getItem('tda_rem_name') || '';
var _REM_TYPE_LABELS = {resolved:'Resolved', unresolved:'Unresolved', false_positive:'False Positive', workaround:'Workaround'};

function remSetName() {
  var n = prompt('Enter your name (will appear on all annotations in this session):', _remName);
  if (n !== null) { _remName = n.trim(); localStorage.setItem('tda_rem_name', _remName); }
  _updateToolbar();
}

function _updateToolbar() {
  var info = document.getElementById('remToolbarInfo');
  var totalMandatory = document.querySelectorAll('[data-rem-mandatory="true"]').length;
  var missingMandatory = _getMandatoryUnannotated().length;
  var mandatoryHtml = '';
  if (totalMandatory > 0) {
    mandatoryHtml = missingMandatory > 0
      ? ' &mdash; <strong style="color:#ffd9d9;">' + (totalMandatory - missingMandatory) + '/' + totalMandatory + ' mandatory CRITICAL/MODERATE annotations complete (' + missingMandatory + ' remaining)</strong>'
      : ' &mdash; <strong>' + totalMandatory + '/' + totalMandatory + ' mandatory CRITICAL/MODERATE annotations complete &#9989;</strong>';
  }
  if (_remName) {
    var count = document.querySelectorAll('.rem-recorded').length;
    info.innerHTML = '&#128221; Reviewer: <strong>' + _escHtml(_remName) + '</strong> &mdash; ' + count + ' annotation(s) recorded.' + mandatoryHtml;
  } else {
    info.innerHTML = '&#128221; Remediation mode &mdash; set your name before annotating.' + mandatoryHtml;
  }
  var exportBtn = document.querySelector('.rem-export-btn');
  if (exportBtn) exportBtn.classList.toggle('locked', missingMandatory > 0);
}

function _getMandatoryUnannotated() {
  var missing = [];
  document.querySelectorAll('[data-rem-mandatory="true"]').forEach(function(f) {
    if (!f.querySelector('.rem-recorded')) missing.push(f);
  });
  return missing;
}

function _escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function _formatTs(d) {
  var pad = function(n){return n<10?'0'+n:n;};
  return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate())+' '+pad(d.getHours())+':'+pad(d.getMinutes());
}

document.addEventListener('DOMContentLoaded', function() {
  var findings = document.querySelectorAll('.finding');
  findings.forEach(function(f, idx) {
    if (f.querySelector('.rem-btn')) return; // already injected (e.g. re-opened annotated export)
    if (f.closest('.looksGood')) return; // no remediation needed for passing checks
    var isCritOrMod = !!(f.closest('.section.critical') || f.closest('.section.moderate'));
    var isSentinel = /^none identified/i.test(f.textContent.trim());
    var isMandatory = isCritOrMod && !isSentinel;
    if (isMandatory) f.setAttribute('data-rem-mandatory', 'true');
    var id = 'rem-' + idx;
    var btn = document.createElement('button');
    btn.className = 'rem-btn';
    btn.textContent = (isMandatory ? '\uD83D\uDD12 ' : '') + '\uD83D\uDCDD Remediate';
    if (isMandatory) btn.title = 'Mandatory: this CRITICAL/MODERATE finding must be annotated before the report can be saved.';
    btn.onclick = function() { remOpen(id, btn); };
    var panel = document.createElement('div');
    panel.className = 'rem-panel';
    panel.id = id;
    panel.innerHTML =
      '<label>Reviewer name</label>' +
      '<input type="text" id="'+id+'-name" placeholder="Your name" />' +
      '<label>Type of Remediation</label>' +
      '<select id="'+id+'-type">' +
      '<option value="">-- Select --</option>' +
      '<option value="resolved">Resolved</option>' +
      '<option value="unresolved">Unresolved</option>' +
      '<option value="false_positive">False Positive</option>' +
      '<option value="workaround">Workaround</option>' +
      '</select>' +
      '<label>Remediation / response note</label>' +
      '<textarea id="'+id+'-note" placeholder="Describe the remediation applied or the reason this finding does not apply..."></textarea>' +
      '<div class="rem-actions">' +
      '<button class="rem-save" onclick="remSave(\'' + id + '\')">' +
      'Save Annotation</button>' +
      '<button class="rem-cancel" onclick="remClose(\'' + id + '\')">' +
      'Cancel</button></div>';
    f.appendChild(btn);
    f.appendChild(panel);
  });
  _updateToolbar();
});

function remOpen(id) {
  var panel = document.getElementById(id);
  if (!panel) return;
  var isOpen = panel.classList.contains('open');
  document.querySelectorAll('.rem-panel.open').forEach(function(p){ p.classList.remove('open'); });
  if (!isOpen) {
    panel.classList.add('open');
    var nameField = document.getElementById(id + '-name');
    if (nameField && !nameField.value && _remName) nameField.value = _remName;
    panel.querySelector('textarea').focus();
  }
}

function remClose(id) {
  var panel = document.getElementById(id);
  if (panel) panel.classList.remove('open');
}

function remSave(id) {
  var nameField = document.getElementById(id + '-name');
  var typeField = document.getElementById(id + '-type');
  var noteField = document.getElementById(id + '-note');
  var name = (nameField ? nameField.value.trim() : '') || _remName || 'Unknown';
  var remType = typeField ? typeField.value : '';
  var note = noteField ? noteField.value.trim() : '';
  if (!remType) { alert('Please select a Type of Remediation before saving.'); return; }
  if (!note) { alert('Please enter a remediation note before saving.'); return; }
  if (name) { _remName = name; localStorage.setItem('tda_rem_name', name); }
  var ts = _formatTs(new Date());
  var typeLabel = _REM_TYPE_LABELS[remType] || remType;
  var recorded = document.createElement('div');
  recorded.className = 'rem-recorded';
  recorded.innerHTML =
    '<div class="rem-meta" data-resolution="' + remType + '" data-reviewer="' + _escHtml(name) + '" data-timestamp="' + ts + '">' +
    '<span class="rem-status-badge rem-status-' + remType + '">' + typeLabel + '</span>' +
    ' &nbsp;&middot;&nbsp; Reviewer: <strong>' + _escHtml(name) + '</strong>' +
    ' &nbsp;&middot;&nbsp; ' + ts + '</div>' +
    '<div class="rem-note"><strong>Remediation note:</strong> ' + _escHtml(note).replace(/\n/g, '<br>') + '</div>';
  var panel = document.getElementById(id);
  var f = panel.closest('.finding');
  panel.classList.remove('open');
  panel.parentNode.insertBefore(recorded, panel.nextSibling);
  if (f) f.classList.remove('rem-missing');
  if (noteField) noteField.value = '';
  if (typeField) typeField.value = '';
  _updateToolbar();
}

function remExport() {
  var missing = _getMandatoryUnannotated();
  if (missing.length > 0) {
    missing.forEach(function(f){ f.classList.add('rem-missing'); });
    missing[0].scrollIntoView({behavior: 'smooth', block: 'center'});
    alert('Cannot save: ' + missing.length + ' CRITICAL/MODERATE finding(s) still need an annotation.\n\nEvery CRITICAL/MODERATE observation must be annotated (Resolved / Unresolved / False Positive / Workaround, with a note) before the report can be exported. The affected finding(s) are now highlighted in red below \u2014 click "Remediate" on each one, save an annotation, then try Save Annotated Report again.');
    return;
  }
  document.querySelectorAll('.rem-panel.open').forEach(function(p){ p.classList.remove('open'); });
  var html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
  var blob = new Blob([html], {type: 'text/html;charset=utf-8'});
  var a = document.createElement('a');
  var title = document.title.replace(/[^a-zA-Z0-9_\-. ]/g, '_').replace(/ /g, '_');
  a.href = URL.createObjectURL(blob);
  a.download = 'Annotated_' + title + '.html';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(a.href);
}
</script>

</body>
</html>
```

### Verdict class mapping
| Outcome | `{verdict_class}` | `{verdict_text}` prefix |
|---|---|---|
| Any CRITICAL finding exists | `blocked` | `&#128308; BLOCKED — ` |
| No CRITICAL, ≥1 MODERATE | `conditional` | `&#128993; CONDITIONAL PASS — ` |
| No CRITICAL, no MODERATE | `pass` | `&#9989; PASS — ` |

### Finding HTML format
Each finding (CRITICAL, MODERATE, MINOR, LOOKS GOOD) must use this exact element:
```html
<div class="finding"><strong>[N] {finding_title}</strong>: {finding_detail}</div>
```

> **⚠️ Do not HTML-escape text that already contains HTML entities or HTML markup.** All finding titles, finding details, and table cell values in this report use literal HTML character entities directly (e.g. `&mdash;`, `&ldquo;`, `&rdquo;`, `&rsquo;`, `&ndash;`, `&#9888;`) instead of raw Unicode characters. If you (or any helper script) run these strings through an HTML-escaping function (e.g. Python's `html.escape()`), the `&` in `&mdash;` will itself be escaped to `&amp;`, producing `&amp;mdash;` — which browsers then render as the **literal text** `&mdash;` instead of an em dash. This applies to **both** the title and detail of every finding, and to every table cell value. **This rule also applies to pre-formed HTML fragment placeholders** such as `{drift_indicator}` — these values are complete `<span>` elements (not plain text), so escaping them turns `<span>` into `&lt;span&gt;` which browsers render as visible literal text rather than a rendered badge. Only escape genuinely untrusted/raw plain-text fields that do **not** already contain entities or markup (e.g. a raw ADO test case title copied verbatim, which may contain `&`, `<`, `>` that need escaping) — never re-escape a string you constructed yourself using HTML entities or HTML tags.

### Table cell styling rules
- Values flagged as problematic: wrap in `<span class="warn">{value}</span>`
- Values confirmed passing: wrap in `<span class="ok">{value}</span>` or use `&#9989;`
- N/A or not applicable values: wrap in `<span class="na">N/A</span>`
- If a table section has no data rows, insert a single spanning row: `<tr><td colspan="{n}" class="na">None identified</td></tr>`

### Hyperlinking Work Item / Test Case / Bug IDs

Every Story ID, Bug ID, Test Case ID, and generic WI ID (e.g. Release WI, Application WI, Parent Application WI) that appears **anywhere** in the report — whether in finding text or a table cell — must be rendered as a clickable hyperlink to the corresponding ADO work item, so reviewers can jump straight from the report into ADO.

**URL pattern**:
```
https://dev.azure.com/{ado_organization}/{ado_project}/_workitems/edit/{id}
```

- Read `ado_organization` and `ado_project` from the top level of the input JSON (see Step 1 keys table). If either is missing or an empty string (JSON collected before this field was added), fall back to `sc-ado` / `FMQPR` — the only org/project in use at the time of writing.
- Wrap the bare ID in an anchor, preserving the ID as the visible text:
  ```html
  <a href="https://dev.azure.com/{ado_organization}/{ado_project}/_workitems/edit/{id}" target="_blank" rel="noopener">{id}</a>
  ```
- Apply this to every occurrence of a Story ID, Bug ID, Test Case ID, or WI ID — in finding titles/details (e.g. `[N] Story 123456: ...`) and in every ID-bearing table column (e.g. `Story ID`, `Bug ID`, `Test Case ID`, `WI ID` columns across the Summary Tables section).
- **Do not** hyperlink: Build IDs (different system/URL shape — ADO pipeline build results, not work items), Run IDs / Result IDs (internal ADO test-run identifiers with no simple direct work-item link), or CHG IDs (ServiceNow change records — an entirely different system, out of scope for ADO work-item hyperlinking).
- **Do not** hyperlink the Release ID shown in the report **header** (`{release_id}` in the `.meta` div, right after the title) or **footer** (`{release_id}` in the `.footer` div) — leave these as plain text (updated 2026-10-14, user feedback: a hyperlinked RWI number at this prominent, large-font position was found hard to read/visually noisy). This is a deliberate exception to the general "every Release WI ID" rule above — the Release ID is already unambiguous from context in these two fixed positions, and every other occurrence of the release's own WI ID elsewhere in the report (if any, e.g. in a findings list or table) should still be hyperlinked normally.
- This anchor tag is a pre-formed HTML fragment — follow the same no-double-escaping guardrail as `{drift_indicator}` above: never pass a string already containing this `<a href=...>` markup through an HTML-escaping function, or the tag itself will render as visible literal text instead of a clickable link.

### Empty section handling
- If there are zero CRITICAL findings, the CRITICAL `<div class="section critical">` block must still be rendered with: `<div class="finding">None identified &#9989;</div>`
- Apply the same rule to MODERATE, MINOR, and LOOKS GOOD sections — never omit a section entirely.

### Mandatory — Write the HTML file via terminal

After constructing the full HTML string, you **must** write it to disk by running the following in the terminal. Populate all placeholder values (`{title}`, `{stream}`, `{chg}`, `{date}`, `{generated_by}`, `{skill_version}`, `{staleness_banner_html}`, `{stream_config_rows}`, all finding blocks, all table blocks, `{verdict_class}`, `{verdict_text}`) with the actual content from the analysis before writing.

```powershell
python -c "
import pathlib, os, sys
username = os.environ.get('USERNAME', os.environ.get('USER', 'user'))
if sys.platform == 'darwin':
    out_path = pathlib.Path(f'/Users/{username}/Downloads/TDAReport_{STREAM}_{release_id}.html')
else:
    out_path = pathlib.Path(f'C:/Users/{username}/Downloads/TDAReport_{STREAM}_{release_id}.html')
html = '''<FULL POPULATED HTML HERE>'''
out_path.write_text(html, encoding='utf-8')
print(f'HTML report written to: {out_path}')
"
```

After running, confirm the saved file path to the user. This step is **not optional** — the HTML report must be generated at the end of every skill invocation.

### ⚠️ Mandatory post-write integrity check — remediation system

Immediately after writing the file, run the following verification. If any check fails, the HTML was written incomplete — regenerate it before confirming to the user.

```powershell
python -c "
import pathlib, os, sys
username = os.environ.get('USERNAME', os.environ.get('USER', 'user'))
if sys.platform == 'darwin':
    out_path = pathlib.Path(f'/Users/{username}/Downloads/TDAReport_{STREAM}_{release_id}.html')
else:
    out_path = pathlib.Path(f'C:/Users/{username}/Downloads/TDAReport_{STREAM}_{release_id}.html')
content = out_path.read_text(encoding='utf-8')
checks = {
    'rem-toolbar div present': 'class=\"rem-toolbar\"' in content,
    'Set Reviewer Name button present': 'remSetName' in content,
    'Save Annotated Report button present': 'remExport' in content,
    'DOMContentLoaded listener present': 'DOMContentLoaded' in content,
    'script tag present': '<script>' in content,
    'file ends with </html>': content.rstrip().endswith('</html>'),
}
all_ok = all(checks.values())
for k, v in checks.items():
    status = 'OK' if v else 'MISSING -- CRITICAL'
    print(f'  {status}: {k}')
print()
if all_ok:
    print(f'All checks passed. File size: {len(content):,} chars.')
else:
    print('INTEGRITY CHECK FAILED -- one or more required sections are missing from the HTML output.')
    print('The remediation system (toolbar, Remediate buttons, Save Annotated Report) will not work for the user.')
    print('Regenerate the HTML ensuring the <div class=\"rem-toolbar\"> block and the full <script> block are included.')
    sys.exit(1)
"
```

> **Why this matters**: The `<div class="rem-toolbar">` block and the `<script>` block at the end of the HTML body are both required for the remediation system (Reviewer Name, Remediate buttons, Save Annotated Report) to function. These are pure front-end features — if either block is omitted from the generated HTML, the report file ends cleanly (no visible error) but the entire annotation capability is silently absent. This has been observed in practice when LLMs truncate or skip these sections during HTML construction.