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

# Release Clinic HTML evidence

**No critical conclusions require user attention or action.**

| Evidence ID | Claim or question | Locator and retained path | Exact revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |
| SRC-USER | Inspect origin HTML and enhance release-clinic. | User message in this chat. | 2026-10-20 | Not available for chat. | Local enhancement requested; no release data supplied. |
| SRC-UPSTREAM | HTML rules, canonical shell, and six integrity checks; agent metadata.version 1.11.1. | `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/SKILL.md` | `832b76a750556cdad69f699db9c1176d47c29ee5` | `3c0d4b182dad89c43292aa1e5522184a16b2f5ca441e97777262cae0bb3fcb76` | Local source inspection only. |
| SRC-SCRIPT | Initial script report, SKILL_VERSION 1.10.2; main and build_html inspected. | `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/gen_tda_report.py` | `832b76a750556cdad69f699db9c1176d47c29ee5` | `81434fdf282fbc20cf1e40161457d83bb8cfd7e798bc0b32ae8298f1d03cdd56` | Local source inspection only. |
| SRC-ORIGIN | Declared origin sc-ado/FMQPR/50665-fm-dtp-qa-utilities, branch main; no remote comparison. | `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/tda/version_check.py` | `832b76a750556cdad69f699db9c1176d47c29ee5` | `6a8792fc02d4b26c323bee49175f0e6bdf933db132bd227d7c43d60e5ef5ae65` | Local source inspection only. |
| SRC-CLI | Release Clinic parser and remainder argument forwarding. | `core/cli.py` | `832b76a750556cdad69f699db9c1176d47c29ee5` | `b4f54552cca9604af3ffed95624e2454c0b9ce64abb12adb5152150eb92e362a` | Local source inspection only. |
| SRC-RUNNER | paths, environment, run, and report subprocess forwarding. | `core/release_clinic.py` | `832b76a750556cdad69f699db9c1176d47c29ee5` | `105ee8962f7ec92e6dd8e1a7d74e298cba043a823390e5594bcfb0591c62980f` | Local source inspection only. |
| SRC-ASSERTIONS | Report output, explicit path, review placeholders, missing input, and filename boundary assertions inspected. | `tests/test_release_clinic.py` | `832b76a750556cdad69f699db9c1176d47c29ee5` | `e8f5fca11a603fcede7409e7a16a8f979dab932d04330840ce31c51fc5cde627` | Local source inspection only. |
| SRC-PACKAGING | Recursive source skill and installed upstream asset copy inspected. | `setup.py` | `832b76a750556cdad69f699db9c1176d47c29ee5` | `f4819e5e6298287a4304d759cdb18360f6d9c50e007af5805a3f5d9db860364e` | Local source inspection only. |
| SRC-SCAFFOLD | Canonical .agents/skills and integration guide included. | `scaffold.json` | `832b76a750556cdad69f699db9c1176d47c29ee5` | `7b717c1f74fcb0e7e4a9ab299538fbdd96928f9a152bfa51ec6f8d21c679cc68` | Local source inspection only. |
| SRC-INITIALIZE | initialize_workspace recursively copies shared skills. | `core/workspace.py` | `832b76a750556cdad69f699db9c1176d47c29ee5` | `8e00885bfd37d765c33b73298b253fe26d3f6ad482a4bcdf5e62e06648edb4a5` | Local source inspection only. |
| SRC-KNOWLEDGE | Domain operations candidate; no applicable HTML generator procedure. | `knowledge/candidates/operations/KT-release-operations.md` | `832b76a750556cdad69f699db9c1176d47c29ee5` | `e387777a26becd3ad3fa93d0ce1c09e59c7c62af71093b008e41003182a4cffc` | Local source inspection only. |
| SRC-INTAKE-TEMPLATE | Working template used for task intake; existing unrelated changes retained. | `knowledge/templates/sdlc/requirement.md` | `832b76a750556cdad69f699db9c1176d47c29ee5` | `c033ac7245708129ddae3602112531779884aa76d0cddd9083b886830b399781` | Local source inspection only. |
| SRC-TASK-GUIDE | Working task intake instructions; existing unrelated changes retained. | `tasks/README.md` | `832b76a750556cdad69f699db9c1176d47c29ee5` | `db05fb90128105a63feb99c3686e7fe8ab8dd75d1bfaeb44becbc021871d02d0` | Local source inspection only. |
| RUN-001 | Retained investigation artifact. | [documentation-verification.json](documentation-verification.json) | 2026-10-20 | `0f764a1a74863b87de4baaebec32b2a293170b2b43f87f31002c5c5f319a73d6` | Retained execution or discovery artifact; no actual release verification. |
| RUN-003 | Retained investigation artifact. | [installed-paths.json](installed-paths.json) | 2026-10-20 | `3e8308221789aa8575eeb730acebbe104449c0eeb54e53f7dc9023eed6f28e1c` | Retained execution or discovery artifact; no actual release verification. |
| RUN-004 | Retained investigation artifact. | [intake-lint.json](intake-lint.json) | 2026-10-20 | `3a5e3d75b7db9a1519601eb555bcc53eadc14456065e76dfe02f18d894273bc7` | Retained execution or discovery artifact; no actual release verification. |
| RUN-005 | Retained investigation artifact. | [release-clinic-tests.log](release-clinic-tests.log) | 2026-10-20 | `1f833ba350f7657403fc76d9697a9ebffd1c5215bab5289fa6d44a69b82a73ca` | Retained execution or discovery artifact; no actual release verification. |
| RUN-006 | Retained investigation artifact. | [report-command-002.log](report-command-002.log) | 2026-10-20 | `0cd183684bc5ee51870c28ef7ce1598aa6b862b684c3b19dab150c7f4f6078a3` | Retained execution or discovery artifact; no actual release verification. |
| RUN-007 | Retained investigation artifact. | [report-command.log](report-command.log) | 2026-10-20 | `bfc3161add9a291ca7af30cddcac8d7d429ef84109b141cb6e61a8ae79cab508` | Retained execution or discovery artifact; no actual release verification. |
| RUN-008 | Retained investigation artifact. | [report-verification-002.json](report-verification-002.json) | 2026-10-20 | `250dc1186177db7de69c584c8ef61c1f9c17a25b68f48aa2120dc8e09cb2163a` | Retained execution or discovery artifact; no actual release verification. |
| RUN-009 | Retained investigation artifact. | [report-verification.json](report-verification.json) | 2026-10-20 | `2b78ec0569f8a0514d61a001b2ff70b181b32311bd2d9be6ba548b0ead085547` | Run 001 label assertion failed because the fixture used an unsupported key; generator exited 0. |
| RUN-010 | Retained investigation artifact. | [skill-validation.log](skill-validation.log) | 2026-10-20 | `db349825903d66adffea3ecf1bd8e1803043e8a71cf1a051235dabc5371f5bb0` | Retained execution or discovery artifact; no actual release verification. |
| RUN-012 | Retained investigation artifact. | [smoke-workspace/input.json](smoke-workspace/input.json) | 2026-10-20 | `491d78bfa4e9f3873afb65cd4f7751fbe923e65d6b9cbda51ab61f2d40c58ee1` | Retained execution or discovery artifact; no actual release verification. |
| RUN-014 | Retained investigation artifact. | [smoke-workspace/reports/initial-report.html](smoke-workspace/reports/initial-report.html) | 2026-10-20 | `0438c244dc64ebf43ff1da5eded2b2aabab897b34d10215bcc3f8d96e648720d` | Synthetic script report; not an actual release assessment. Browser controls untested. |
| RUN-016 | Retained investigation artifact. | [smoke-workspace-002/input.json](smoke-workspace-002/input.json) | 2026-10-20 | `bc57912c66d0cc32d66ccbe4b59fff69624a11dd3cee81f6b4b5b56c0a3b538e` | Retained execution or discovery artifact; no actual release verification. |
| RUN-018 | Retained investigation artifact. | [smoke-workspace-002/reports/initial-report.html](smoke-workspace-002/reports/initial-report.html) | 2026-10-20 | `42148b4f43997ce293603d5e920ce526be42fb996c90c38fcc90f7c29cde168f` | Synthetic script report; not an actual release assessment. Browser controls untested. |
| RUN-019 | Retained investigation artifact. | [source-manifest.json](source-manifest.json) | 2026-10-20 | `2dea3c8f3d382ee03e923c064e2caa7cb02f6d7642e636a44d5a7b5040ab5fe9` | Retained execution or discovery artifact; no actual release verification. |
| RUN-020 | Retained investigation artifact. | [workspace-status.json](workspace-status.json) | 2026-10-20 | `03b683ccf3d6b90c674fdc8a515367a7f8d7444e4cf43443a391c706a980f13a` | Retained execution or discovery artifact; no actual release verification. |

The installed path capture identifies local assets. It does not establish current remote origin parity.
The source manifest retains exact source identities and hashes.
All human review identities remain unknown or null.

Final intake lint: [intake-lint-final.json](intake-lint-final.json).
SHA-256: `3a5e3d75b7db9a1519601eb555bcc53eadc14456065e76dfe02f18d894273bc7`.
Lint passed with explicit ownership, review, and unresolved-value warnings.
Those warnings do not block this technical guidance change. No business publication is requested.
Selected new prose passed the automated 20-word sentence check. Full ASD review remains pending.

## Task document order

Read documents by lifecycle stage. Use the existing current-stage links to assess the latest scope.
Filename numbers do not establish readiness or approval.

| Stage | Document |
| --- | --- |
| 01 Receive | [01-intake.md](../01-intake.md) |
| 06 Implement | [06-skill-inclusion.md](../06-skill-inclusion.md) |
| 09 Compare evidence | [09-parity-review.md](../09-parity-review.md) |
| 10 Scoped handoff | [10-report.md](../10-report.md) |

The [filename map](document-order.json) retains original paths, compatibility links, source revisions, and unchanged hashes.

## Complete skill inclusion

The follow-up request includes the complete upstream skill inside the shared release-clinic reference directory.

| Evidence ID | Claim or question | Locator and retained path | Exact revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |
| INCLUDE-001 | Skill inclusion and distribution checks. | [skill-inclusion/skill-validation.log](skill-inclusion/skill-validation.log) | 2026-10-20 | `db349825903d66adffea3ecf1bd8e1803043e8a71cf1a051235dabc5371f5bb0` | Local validation; no actual release assessment. |
| INCLUDE-002 | Skill inclusion and distribution checks. | [skill-inclusion/source-verification.json](skill-inclusion/source-verification.json) | 2026-10-20 | `0c465498bae2bbb7db71a4579bb163a0f44135a9e93941fe3fdc492fb265225a` | Local validation; no actual release assessment. |
| INCLUDE-003 | Skill inclusion and distribution checks. | [skill-inclusion/verification.json](skill-inclusion/verification.json) | 2026-10-20 | `321735c68ffb66fbdaaecbc09dc4f9ef83b7d123bfb996223dc8c22fdf82eccb` | Local validation; no actual release assessment. |
| INCLUDE-004 | Skill inclusion and distribution checks. | [skill-inclusion/wheel-build.log](skill-inclusion/wheel-build.log) | 2026-10-20 | `4c6c8482e6a379a74aa0cfcf7faabe0b36baec6372415e5a5d20f79361e3bad0` | Local validation; no actual release assessment. |
| INCLUDE-005 | Skill inclusion and distribution checks. | [skill-inclusion/wheel-command-1.log](skill-inclusion/wheel-command-1.log) | 2026-10-20 | `074e94ba0e256c078585a6937f807c6286bb205870566e7e3519e1d5a97763be` | Local validation; no actual release assessment. |
| INCLUDE-006 | Skill inclusion and distribution checks. | [skill-inclusion/wheel-command-2.log](skill-inclusion/wheel-command-2.log) | 2026-10-20 | `02e245a7930455e0c4b03009d8df6ef240c022903379053c695923881f04981c` | Local validation; no actual release assessment. |
| INCLUDE-007 | Skill inclusion and distribution checks. | [skill-inclusion/wheel-command-3.log](skill-inclusion/wheel-command-3.log) | 2026-10-20 | `32f402963b72c84b9669b573ca7b2f60a482aef68ec7905836acd2b043cf755b` | Local validation; no actual release assessment. |
| INCLUDE-008 | Skill inclusion and distribution checks. | [skill-inclusion/wheel-command-4.log](skill-inclusion/wheel-command-4.log) | 2026-10-20 | `e539d1d2daf030581ce676cbdf2910d28859ac5eb232f47f1585e53ebefaeba3` | Local validation; no actual release assessment. |
| INCLUDE-009 | Skill inclusion and distribution checks. | [skill-inclusion/wheel-verification.json](skill-inclusion/wheel-verification.json) | 2026-10-20 | `207cfdc8a4900e0bd5992287634e39ef76615d74e2bc0d76cc57895b4a046c2f` | Local validation; no actual release assessment. |
| INCLUDE-010 | Skill inclusion and distribution checks. | [skill-inclusion/workspace-tests.log](skill-inclusion/workspace-tests.log) | 2026-10-20 | `ef2f1d7d7c10008cd2fc9ddd8d26140db556f55d7b68e5b672ca0ef79c2e9b7d` | Local validation; no actual release assessment. |

## Complete report parity review

The follow-up request requires complete report parity with the bundled `dtp-tda-report` skill.
The [parity review](../09-parity-review.md) records fixes, coverage, results, and the shared upstream defect.
Earlier reports and script smoke outputs retain their original evidence scope.

| Evidence ID | Claim or question | Locator and retained path | Capture date | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |
| PARITY-001 | Full source and execution identities. | [parity-checks/manifest.json](parity-checks/manifest.json) | 2026-10-20 | `522e03aa6f91d9f58c43a9b71ce212a53c23bf3d493e88704a68268f04756353` | Local bytes and hashes; no remote freshness claim. |
| PARITY-002 | Runtime suite with mock loopback access. | [parity-checks/runtime-tests-002.log](parity-checks/runtime-tests-002.log) | 2026-10-20 | `18175155f5d2fa11e45712d4a4d17a59db27c88e220120cbd44268f3aece9b31` | 492 tests completed; two skipped. No release behavior claim. |
| PARITY-003 | Wheel and initialized workspace distribution. | [parity-checks/distribution-20261019T170842481043Z/distribution.json](parity-checks/distribution-20261019T170842481043Z/distribution.json) | 2026-10-20 | `40b04f287ab7892fc3e5f48d09dd24a3cb6a8a8ecd34748117aaf28b021f333b` | Complete reference, helper, and wrapper resources matched. |
| PARITY-004 | Canonical browser behavior comparison. | [parity-browser/results-2026-10-19T17-01-39-778Z.json](parity-browser/results-2026-10-19T17-01-39-778Z.json) | 2026-10-20 | `dd5c5182bf1b7d45e25b6681fc86daaff8d1ccd2c89520c7fe631dea38aec577` | Matched behavior; each source passed 15 of 16 controls. |
| PARITY-005 | Shared browser defect and scope. | [parity-browser/assessment.md](parity-browser/assessment.md) | 2026-10-20 | `9bbac1cf13990495b809a7b083e313944e33bc11935c1f92758db2c50dbce7c6` | Reopened Remediate panels fail in both sources. |
| PARITY-006 | Local links, sentence limits, and scoped diff. | [parity-checks/documentation.json](parity-checks/documentation.json) | 2026-10-20 | `1f32edf8b41bc331120b5fa65c9c502129c2cf15f63a883190d0456764462c12` | Checks passed. Full ASD review remains pending. |
