---
writing_review:
  standard: ASD-STE100
  automated_check: FAILED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Release Clinic parity review

The user requested no reporting gap between `release-clinic` and the bundled `dtp-tda-report` skill.
The review compares complete instructions, wrapper decisions, distributed resources, and canonical report controls.
The baseline is Workbench revision `844198cea36d6c5d966cd0075dd30a6fe9fc0321`.
The upstream skill version is `1.11.1`.
Its SHA-256 is `3c0d4b182dad89c43292aa1e5522184a16b2f5ca441e97777262cae0bb3fcb76`.

No integration gap remains identified within the reviewed instructions, distributed assets, and tested controls.
One shared upstream browser defect remains. The automated status includes that failed control.

## Findings and affected scope

| Finding | Evidence | Consequence | Owner | Action |
| --- | --- | --- | --- | --- |
| The wrapper permitted script generation inside its report flow. | Prior shared skill, Analyze one release; upstream guardrail at line 22. | Report rules could differ from the upstream agent procedure. | Coding agent | Remove that branch and preserve the independent operator CLI boundary. |
| The wrapper selected the included edition after installed drift. | Prior HTML reporting reference, lines 33–34. | New upstream rules could be bypassed, including unversioned edits. | Coding agent | Add complete-byte comparison and select the installed edition on mismatch. |
| Generic shell instructions conflict with explicit upstream rules. | Upstream lines 228, 304, 366, 545, 962, 1083, and 1454. | Stale tables can create prohibited findings or omit required content. | Coding agent | Give explicit guardrails and required report tables precedence. |
| Existing tests covered the script generator and skill entrypoints. | `tests/test_release_clinic.py`; `tests/test_workspace_layout.py`. | Exact reference distribution and interactive canonical controls lacked retained regression evidence. | Coding agent | Check source parity, generated resources, drift detection, and local browser controls. |
| The upstream instructions recommend an absent Genie helper. | Upstream line 1130; installed scripts directory. | Legacy input cannot use that backfill command. | Coding agent | Preserve the evidence limit and use authorized collector recollection. |

The changes affect skill instructions, one local comparison helper, and focused regression coverage.
The completed changes resolve these integration findings.
The runtime report generator and upstream authoring source retain their existing bytes.
Risk is moderate because incorrect rule selection can change release findings.
Direct full-source reuse and complete-byte checks reduce source drift risk.
The content check does not execute the analysis or prove release quality.

## Coverage and rule decisions

| Area | Exact upstream locator | Integration decision and result |
| --- | --- | --- |
| Direct agent authoring | Lines 22–31 | Prohibit generator execution through either the script or Workbench wrapper. |
| Stream validation, configuration, and inputs | Lines 35–216 | Use fresh full or compact JSON and effective workspace configuration. Preserve the stream snapshot caveat. |
| Release analysis rules | Lines 218–922 | Include every source byte. Read the selected edition in full without reimplementing thresholds. |
| Findings and summary tables | Lines 924–1212 | Preserve applicable tables and required columns. Explicit suppression rules precede stale generic examples. |
| Verdicts and report provenance | Lines 1214–1240 | Preserve verdict mapping and selected edition metadata. Keep report assessment separate from human approval. |
| CSS, HTML, annotations, links, and file checks | Lines 1242–1808 | Preserve complete canonical assets. Verify saved output and retain earlier reports. |
| Installed and initialized resources | `setup.py`; `core/workspace.py` | Wheel and generated workspace retain the full reference and comparison helper. Runtime source remains installed. |
| Source drift | New comparison helper and eight regressions | Detect complete-byte changes, including same-version edits. Select one complete edition after comparison. |

The reviewed wrapper now applies path and configuration adaptations to either selected edition.
Version-specific conflict examples are tied to the source hash above.
Future editions require inspection of their explicit rules before applying those examples.
The agent report flow supersedes the earlier script-mode instructions retained in this task's historical reports.
Earlier script smoke outputs establish the independent operator utility only.

## Validation results

| Check | Retained evidence | Observed result and limit |
| --- | --- | --- |
| Complete source comparison | Browser results; installed parity log | Both files contain 160397 identical bytes and 1808 lines. |
| Runtime regression suite | [runtime-tests-002.log](evidence/parity-checks/runtime-tests-002.log) | 492 tests completed successfully; two skipped. Eight new parity regressions passed. |
| First runtime attempt | [runtime-tests.log](evidence/parity-checks/runtime-tests.log) | The sandbox blocked one mock HTTP server. The authorized loopback retry passed. |
| Skill schema | [skill-validation.log](evidence/parity-checks/skill-validation.log) | Passed. |
| Wheel and external workspace | [distribution.json](evidence/parity-checks/distribution-20261019T170842481043Z/distribution.json) | Offline wheel build, isolated installation, initialization, validation, and installed source comparison passed. |
| First distribution check | [distribution.json](evidence/parity-checks/distribution.json) | The harness named a nonexistent schema. The corrected check used `requirement.schema.json` and passed. |
| Local browser controls | [browser assessment](evidence/parity-browser/assessment.md) | Behavior matched across both sources. Each passed 15 of 16 cases. |
| Evidence identity and documentation | [manifest.json](evidence/parity-checks/manifest.json); [documentation.json](evidence/parity-checks/documentation.json) | Hashes, local links, prose sentence limits, and scoped diff checked. Full ASD review remains pending. |

The new regressions cover read-only comparison, same-version JavaScript drift, missing sources, and invalid path resolution.
They also cover invalid skill content, self-comparison, source aliases, and initialized workspace resources.
The packaging regression checks complete report bytes and helper distribution.
The browser fixtures contain synthetic findings and explicit `TEST ONLY` identities.

## Shared upstream control defect

Evidence: both `reopened_remediate_button_opens_panel` cases returned `open: false` and `display: none`.
Consequence: Remediate buttons cannot open annotation panels after reopening an exported report.
Owner: upstream `dtp-tda-report` maintainer; the individual owner is unknown.
Next action: restore serialized button handlers upstream, validate exports, and synchronize the included source.

Upstream line 1606 assigns `btn.onclick` programmatically.
Line 1691 serializes the document through `outerHTML` without those handlers.
Line 1595 skips existing buttons during reopened initialization.
These statements explain the shared observed failure.
The integration now discloses this limit and retains original reports for further annotation.

## Evidence limits

The browser run used macOS Chromium with sandboxing enabled and blocked external page requests.
No external page request or page error occurred.
Other browsers and native Windows execution remain untested.
The review does not establish remote upstream freshness, human approval, or identical answers from different agents.
No production release was analyzed or collected for this maintenance request.
