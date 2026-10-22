---
artifact_kind: requirement
id: REQ-RELEASE-CLINIC-HTML-20261020
version: 1
status: draft
owner: unknown
source_refs: [SRC-USER, SRC-WORKBENCH, SRC-UPSTREAM]
related_ids: []
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Generate a Release Clinic HTML report

## Description

As a release analyst, I need clear HTML reporting instructions for Release Clinic.
Inspect the upstream reporting flow and enhance the Workbench integration where evidence shows a gap.

## Rationale

The user reports that the origin project can generate an HTML release report.
The user requests investigation and enhancement in the message dated 2026-10-20.

## Scope

| Included behavior | Excluded behavior | Reason |
| --- | --- | --- |
| Inspect upstream HTML reporting and improve the supported Workbench flow. | External release collection, hosting, and publication. | The request concerns reporting capability and guidance. |

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Reporting guidance enhancement | READY | Bundled instructions, CLI forwarding, and report assertions establish both reporting paths. No release data is needed for documentation. | None within local documentation scope. | Coding agent; update guidance and verify commands. |

- Expected behavior authority: the user's enhancement request; business publication review remains pending.
- Existing authorization: local investigation, reversible enhancements, relevant checks, and the required stage commit.
- Evidence index: [evidence/index.md](evidence/index.md).
- Business review: pending. Readiness does not grant approval.

## Actors and business rules

| Actor | Rule ID | Condition | Required behavior | Source |
| --- | --- | --- | --- | --- |
| Release analyst | RC-HTML-001 | Retained collector JSON exists. | Follow the supported upstream procedure to create a local HTML report. | SRC-USER; SRC-UPSTREAM pending inspection. |
| Coding agent | RC-HTML-002 | The user requests a release report. | Select the correct report mode and retain evidence limits. | SRC-WORKBENCH reporting guidance. |

## Dependencies

| Related ID | Relationship | Evidence | Unresolved impact |
| --- | --- | --- | --- |
| release-clinic | Supplies bundled report tools and upstream instructions. | SRC-WORKBENCH; source manifest. | No unresolved impact within documentation scope. Remote parity remains untested. |

## Acceptance criteria

```gherkin
@REQ-RELEASE-CLINIC-HTML-20261020
Feature: Generate a Release Clinic HTML report

  @RC-AC-001
  Scenario: Discover supported HTML reporting
    Given the bundled upstream reporting sources are available
    When the analyst reads the enhanced release-clinic skill
    Then the instructions identify both supported HTML reporting modes

  @RC-AC-002
  Scenario: Follow the upstream report procedure
    Given the analyst has retained collector JSON
    When the analyst follows the agent report instructions
    Then the instructions identify the installed skill, template, and integrity checks

  @RC-AC-003
  Scenario: Check local report generation
    Given a controlled local collector JSON input
    When the analyst runs the documented script report command
    Then one HTML report is written at the selected workspace output path
```

```yaml
acceptance_criteria:
  - id: RC-AC-001
    given: Given the bundled upstream reporting sources are available
    when: When the analyst reads the enhanced release-clinic skill
    then: Then the instructions identify both supported HTML reporting modes
    measure:
      metric: documented report mode count
      operator: equals
      value: 2
      unit: count
  - id: RC-AC-002
    given: Given the analyst has retained collector JSON
    when: When the analyst follows the agent report instructions
    then: Then the instructions identify the installed skill, template, and integrity checks
    measure:
      metric: required procedure element count
      operator: equals
      value: 3
      unit: count
  - id: RC-AC-003
    given: Given a controlled local collector JSON input
    when: When the analyst runs the documented script report command
    then: Then one HTML report is written at the selected workspace output path
    measure:
      metric: generated HTML report count
      operator: equals
      value: 1
      unit: count
```

## Measurement conditions

| Criterion ID | Measurement method | Environment and data | Interval and load | Evidence required |
| --- | --- | --- | --- | --- |
| RC-AC-001 | Inspect documented mode selection and upstream sources. | Local checkout. | One review. | Source locators and change diff. |
| RC-AC-002 | Inspect links, commands, template, and upstream checks. | Installed integration and bundled sources. | One review. | Source hashes and command results. |
| RC-AC-003 | Run the existing report command and inspect its output. | Controlled synthetic JSON; no external collection. | One report. | Input, output, hashes, and command result. |

## Traceability

| Criterion ID | Design ID | Repository and exact revision | Test assertion and revision | Retained execution |
| --- | --- | --- | --- | --- |
| RC-AC-001 | Local reporting guidance | SRC-WORKBENCH at 64cc4d58e766fb227f3b495117c0a4c43d1e92f7; final guidance in this change. | Source review and skill validator; no runtime test added for prose. | `evidence/skill-validation.log`; `evidence/documentation-verification.json`. |
| RC-AC-002 | Upstream reporting procedure | SRC-UPSTREAM at the SRC-WORKBENCH revision; SHA-256 in source manifest. | Upstream shell and six markers inspected; installed source available. | `evidence/documentation-verification.json`. |
| RC-AC-003 | Existing CLI forwarding | SRC-WORKBENCH at 64cc4d58e766fb227f3b495117c0a4c43d1e92f7 | `tests/test_release_clinic.py:37`; `:51`; `:59`, at the same revision. | 36 tests passed; `evidence/release-clinic-tests.log`; `evidence/report-verification-002.json`. |

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| SRC-USER | User message in this chat, 2026-10-20. | Not applicable; chat request. | null | User; requested scope. | No release input or release approval supplied. |
| SRC-WORKBENCH | `.agents/skills/release-clinic/SKILL.md`; `core/release_clinic.py`; `docs/RELEASE_CLINIC.md`. | 64cc4d58e766fb227f3b495117c0a4c43d1e92f7 | See evidence index and source manifest. | Workbench source; implementation evidence. | Other unrelated worktree changes exist. |
| SRC-UPSTREAM | `core/release-clinic/plugins/test/dtp-tda-report/`. | Imported at 28244ce962568b10821312ae3c972f2d36a94e6f; inspected at the SRC-WORKBENCH revision. | See evidence index. | Upstream implementation; no business approval inferred. | Current remote parity remains untested. |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Fact | The current skill mentions an agent report and a script report. | SRC-WORKBENCH | Existing capability can be reused. | unknown | Inspect exact procedures. |
| Fact | The upstream skill requires Markdown analysis and a saved HTML report. | SRC-UPSTREAM, sections Report Format and Step 3. | Guidance must cover both deliverables and the integrity checks. | Coding agent | Add the reporting reference. |
| Fact | The standalone script produces an initial report with review placeholders. | `gen_tda_report.py:1949`; `tests/test_release_clinic.py:37`. | Mode selection must explain the review limits. | Coding agent | Verify the existing command with synthetic input. |
| Inference | Documentation changes have low implementation risk. | CLI forwarding and generator remain unchanged. | Incorrect guidance could still select the wrong report mode. | Coding agent | Review mode selection, output paths, links, and upstream invariants. |
| Fact | The worktree contains unrelated changes. | Initial Git status. | Staging must name only task files. | Coding agent | Preserve unrelated changes. |

### Existing knowledge and evidence review

| Search scope and source | Revision or hash | Applicable rule or criterion | Authority and limits | Remaining material gap |
| --- | --- | --- | --- | --- |
| Release Clinic skill and integration guide. | SRC-WORKBENCH revision above. | RC-AC-001; RC-AC-002 | Existing guidance describes two modes briefly. | Resolved through the bundled upstream skill. |
| `knowledge/candidates/operations/KT-release-operations.md`. | Content hash in evidence index. | No applicable HTML generation rule. | Domain release operations candidate; not tool instructions. | No domain knowledge change is needed. |
| `core/release_clinic.py`; `core/cli.py`; `tests/test_release_clinic.py`. | SRC-WORKBENCH revision above. | RC-AC-003 | Inspected subprocess forwarding, output resolution, review markers, and path assertions. | Local command and 36 tests passed; browser controls remain untested. |
| `setup.py`; `core/workspace.py`; `scaffold.json`. | SRC-WORKBENCH revision above. | RC-AC-002 | Shared skill resources are copied recursively into packages and generated workspaces. | Generated workspace retained identical reference bytes and passed validation. Wheel packaging was not changed. |

### Answer and question log

| Round and ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| 1; RC-Q-001 | Can the origin project generate HTML? | Yes. The bundled upstream skill specifies direct HTML authoring and mandatory integrity checks. | SRC-UPSTREAM, Step 3 and post-write integrity check. | answered | Coding agent | Add complete reporting guidance. |
| 1; RC-Q-002 | Is a specific release report requested? | No release identity or input was supplied. | SRC-USER | answered | Coding agent | Improve reusable reporting guidance with local controlled verification. |

### Knowledge-update log

| Gap or question ID | Affected record and prior version | Clarified rule, source, and applicability | Updated record, version, and criteria | Finding and audit references | Publication state, owner, and next action |
| --- | --- | --- | --- | --- | --- |
| RC-Q-001 | Release Clinic implementation guidance. | Bundled upstream v1.11.1 requires a complete saved HTML report. | Shared skill, reporting reference, and integration guide; RC-AC-001 and RC-AC-002. | Not applicable: technical procedure clarification changes no governed domain record. | Technical guidance only; Coding agent; retain sources and validate changes. |

### Intake investigation plan

- Current state: the upstream skill authors HTML directly; the CLI forwards to a separate initial-report script.
- Evidence retained: source hashes, both controlled report executions, document lint, and link checks.
- Method and controls: inspect local sources and run local reporting with synthetic input.
- Retention: keep new results under this task's `evidence/` directory.
- Next decision: the local guidance stage passed its checks and is ready for its required commit.

The [completion report](report.md) records results and evidence limits.
The first synthetic-label assertion failed because its input used an unsupported key.
The corrected run passed. Both runs remain available.
