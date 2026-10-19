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

# Release Clinic HTML reporting enhancement

The bundled upstream skill already supports a complete HTML release report.
The shared skill now explains both reporting modes and links the complete Workbench procedure.

## Findings and changes

| Finding | Evidence | Consequence | Owner | Action and result |
| --- | --- | --- | --- | --- |
| Agent analysis requires a saved HTML deliverable. | Upstream `SKILL.md:1220`; `SKILL.md:1752`. | A Markdown-only response leaves the report incomplete. | Coding agent | Updated mode selection and added `references/html-reporting.md`. |
| The initial script uses a separate implementation. | Upstream skill v1.11.1; script `SKILL_VERSION` v1.10.2. | Script output cannot establish current agent-rule coverage. | Coding agent | Kept script mode explicit and documented its review placeholders. |
| Annotation controls require the complete HTML shell. | Upstream `SKILL.md:1324`; `SKILL.md:1772`. | Truncation can remove reviewer controls without a visible document error. | Coding agent | Documented required blocks, six checks, and the annotation export rule. |
| Upstream examples use Downloads paths. | Upstream `SKILL.md:1225`; Workbench `core/release_clinic.py:91`. | Copied examples can save reports outside the selected workspace. | Coding agent | Documented installed discovery and workspace output resolution. |

The integration guide now includes an agent prompt and the separate initial-report command.
The existing CLI and renderer remain the implementation for script reports.
This change adds no dependency.
Implementation risk is low because the change updates guidance only.
Incorrect mode selection remains the main procedural risk.

## Validation

| Check | Result | Evidence and limits |
| --- | --- | --- |
| Skill validation | PASSED | `evidence/skill-validation.log`; checks skill metadata and scaffold content. |
| Intake lint | PASSED with warnings | `evidence/intake-lint.json`; ownership and reviews remain unresolved. |
| Release Clinic tests | 36 passed | `evidence/release-clinic-tests.log`; inspected existing command and configuration assertions. |
| Initial script command | PASSED | `evidence/report-verification-002.json`; synthetic input and selected workspace output. |
| Six HTML integrity checks | PASSED | Same run; structural markers only. |
| Documentation links | PASSED | `evidence/documentation-verification.json`; all selected local links resolve. |
| Generated workspace | PASSED | Same record; guide bytes match, installed upstream skill exists, and workspace validation passes. |
| Independent source review | Completed | Two corrections applied: annotation controls wording and mandatory annotation export requirements. |

The first synthetic run used the unsupported `release_title` key.
The generator succeeded, but the synthetic-label assertion failed.
The second run used `release_features[0].System.Title`, as required by the inspected renderer.
Both runs remain retained.

## Evidence limits and next use

No actual release input was supplied.
No external collection or remote origin comparison occurred.
The source manifest identifies the bundled revision and declared upstream repository.
The generated HTML is a synthetic script check, not a release assessment.
Browser layout, annotation interactions, and annotated downloads remain untested.
The documentation change required no wheel build or new runtime test.
Generated workspace checks used the existing editable installation.
Business approval and full ASD review remain pending.

For an actual release, supply retained collector JSON to the enhanced `release-clinic` skill.
The agent can then apply the installed rules and produce the final HTML deliverable.
See [the evidence index](evidence/index.md) for source hashes and retained results.
