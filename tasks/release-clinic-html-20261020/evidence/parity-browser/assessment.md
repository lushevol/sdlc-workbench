---
standard: ASD-STE100
automated_check: FAILED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Canonical report browser comparison

Both canonical sources produced identical fixture bytes and browser results.
Each source passed 15 of 16 control checks.
Reopened annotation buttons failed in both sources.
This finding limits the browser control result, while the parity comparison passed.

## Evidence

The executed sources were upstream `SKILL.md` and the shared `references/dtp-tda-report.md` copy.
Both files contained version `1.11.1`.
Both files had SHA-256 `3c0d4b182dad89c43292aa1e5522184a16b2f5ca441e97777262cae0bb3fcb76`.
The retained result records source, CSS, JavaScript, shell, fixture, and exported-file hashes.

The successful execution result is [results-2026-10-19T17-01-39-778Z.json](results-2026-10-19T17-01-39-778Z.json).
Its `writing_review.automated_check: PASSED` describes the completed comparison.
This assessment records `automated_check: FAILED` because one browser control failed.
The earlier result preserves the sandbox's loopback `EPERM` failure.

## Observed controls

| Control | Upstream | Included |
| --- | --- | --- |
| Initial buttons and mandatory annotation tags | Passed | Passed |
| Summary Tables initial expansion | Passed | Passed |
| Summary Tables collapse and expansion | Passed | Passed |
| Explicit `TEST ONLY` reviewer naming | Passed | Passed |
| Export blocked before mandatory annotations | Passed | Passed |
| Annotation requires status and note | Passed | Passed |
| Critical and moderate annotations save | Passed | Passed |
| Export blocked with one annotation missing | Passed | Passed |
| Export succeeds with both annotations | Passed | Passed |
| Reopened export preserves annotations | Passed | Passed |
| Reopened Remediate button opens its panel | Failed | Failed |
| Reopened reviewer naming and export | Passed | Passed |

## Shared upstream finding

Evidence: `reopened_remediate_button_opens_panel` returned `open: false` and `display: none` for each source.
Consequence: reviewers cannot open annotation panels through Remediate buttons after reopening exported reports.
Owner: upstream `dtp-tda-report` maintainer; the individual owner is unknown.
Next action: restore annotation button handlers after reopening exports and synchronize both canonical sources after validation.

The source assigns each button handler through `btn.onclick` at upstream line 1606.
The export serializes `document.documentElement.outerHTML` at upstream line 1691.
That serialization omits programmatic event handlers.
Reopening initialization skips existing buttons at upstream line 1595.
These source statements explain the observed result.

## Execution limits

The fixtures contain synthetic `TEST ONLY` content and explicit test reviewer names.
The run used Playwright `1.64.1` and macOS Chromium `156.0.8078.4`.
The browser retained `chromiumSandbox: true`.
The fixture server listened on loopback.
The browser blocked external page requests and disabled background networking at launch.
No external page request or page error occurred.

The run preserved complete canonical CSS and JavaScript.
It used no standalone report generator.
Screenshots, traces, exports, and accessibility snapshots remain beside the fixtures.
This comparison does not validate release analysis or business behavior.
Windows and other browsers remain untested.
