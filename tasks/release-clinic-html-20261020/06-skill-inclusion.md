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

# Include the complete dtp-tda-report skill

The user requested direct inclusion of the bundled `dtp-tda-report` skill into `release-clinic`.
The previous change provided workflow guidance and installed source discovery.
This change includes the complete upstream instructions as `release-clinic/references/dtp-tda-report.md`.
Release analysis must read that local reference.

## Source and scope

The authoring source remains `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/SKILL.md`.
The included reference preserves all 160397 source bytes.
Both files have SHA-256 `3c0d4b182dad89c43292aa1e5522184a16b2f5ca441e97777262cae0bb3fcb76`.
The inspected source revision is `23ed299`, with the full revision recorded in the verification evidence.
The source metadata version is `1.11.1`.

| Finding | Evidence | Consequence | Owner | Action |
| --- | --- | --- | --- | --- |
| The full instructions were outside the shared skill. | Prior `SKILL.md` and HTML reference. | Copying the shared skill did not include the complete analysis rules. | Coding agent | Included the full source and made reading it mandatory. |
| Upstream paths assume an upstream skill directory. | Included `$SKILL_DIR` references. | A local reference directory contains no collector scripts. | Coding agent | Bound `$SKILL_DIR` to the installed `report_skill` parent. |
| Upstream metadata and examples contain deployment assumptions. | Upstream model, Downloads paths, ADO defaults, and staleness language. | Blind adoption can misstate identity, approval, or execution context. | Coding agent | Retained explicit Workbench adaptations and the included version baseline. |

The shared skill and integration guide explain the included reference.
The included copy must remain synchronized with its upstream authoring source.
Existing recursive copy operations distribute the reference into wheels and generated workspaces.
This change adds no runtime source, package dependency, or packaging algorithm.
Risk is low because executable behavior remains unchanged.
Future source drift remains a maintenance risk; refresh the included bytes when adopting upstream changes.

## Checks and limits

- Skill validation passed.
- All nine selected local documentation links resolve.
- The source and included reference match exactly.
- All 18 existing workspace layout tests passed.
- The wheel built successfully without dependency installation.
- The wheel contains matching reference and upstream source bytes.
- A workspace initialized from the wheel contains the complete reference as a regular file.
- That workspace passed validation and resolved the installed report tools.
- Independent review found no actionable conflicts.

The checks used macOS and existing Python environment dependencies.
Windows execution and external services remain untested.
No release report or human approval was generated during this inclusion check.
See [the verification evidence](evidence/skill-inclusion/verification.json) for commands, hashes, and observed results.
