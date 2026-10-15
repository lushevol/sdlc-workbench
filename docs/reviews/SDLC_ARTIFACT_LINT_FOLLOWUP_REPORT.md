---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Markdown and Gherkin checks cover selected structures only.
  - Lint does not establish source authority, human approval, or business execution.
---

# Artifact lint follow-up

Review date: 16 October 2026.
The user's continuation request prompted a focused review of the existing authoring tools.
The review found five defects in current guidance and lint behavior.
This stage corrects those defects and retains seven regression tests.

## Scope and risk

The change affects the artifact linter, its tests, and two authoring guides.
The CLI and Python API signatures remain unchanged.
The 37 artifact kinds and their schema sections remain unchanged.
Parsing helpers supply the existing `lint_artifacts` entry point.
Its current consumers are the CLI, Python callers, and AI-assisted document authors.

Qualitative risk is moderate because comment parsing can affect required-section discovery.
Existing tests still reject hidden headings, duplicate sections, invalid measures, and ambiguous identities.
The change adds no dependency, execution grant, or knowledge lifecycle transition.
Concurrent graph and knowledge changes remain outside this stage.

## Corrected findings

| Finding and evidence | Consequence | Owner | Resolution and next action |
| --- | --- | --- | --- |
| Inline code containing `<!--` opened a false comment in `_sections`. | Later required headings disappeared and valid artifacts failed. | unknown | Preserve matched code spans and escapes. Retain the regression. |
| `_meaningful` removed comment text inside fenced code. | A valid code example appeared empty. | unknown | Preserve code content after section parsing. Retain the regression. |
| `_HEADING` required column-zero headings. | Required headings with one through three leading spaces failed. | unknown | Accept the supported ATX indentation. Keep four-space rejection coverage. |
| Sample detection inspected artifact IDs and source references only. | Copied identifiers in related references or bodies escaped the warning. | unknown | Inspect parsed references and document identifiers. Retain positive and negative cases. |
| The requirement guide instructed authors to repeat both representations. | Distinct YAML blocks triggered `criteria_conflict`. | unknown | Require one complete criterion list and matching scenarios. Retain list and conflict checks. |

The [CommonMark heading rules](https://spec.commonmark.org/0.31.2/#atx-headings) permit up to three leading spaces.
Its [code span rules](https://spec.commonmark.org/0.31.2/#code-spans) define matched backtick delimiters for literal code.
These references support the corrected cases. They do not establish complete parser conformance.

## Validation observations

The isolated source contains commit `618d42ced7fc38fe911574745000fc18e13a7b79` and this stage's four changed source files.
It excludes unrelated concurrent work.

| Check | Observed result | Evidence limit |
| --- | --- | --- |
| Targeted lint suite | All 51 tests passed. Seven tests cover the follow-up cases. | Assertions check authoring behavior, not business execution. |
| Isolated runtime suite | All 278 tests passed. | The suite used the committed baseline plus this stage. |
| Isolated source validation | VALID; nine documents; zero findings. | Structural validation does not establish business correctness. |
| Shared working-tree suite | One graph renderer test failed during the 282-test run. | The failure remains in concurrent graph changes. |
| Shared workspace validation | INVALID; three `audit_state_missing` findings among 12 documents. | Concurrent knowledge changes need their own matching audit events. |
| Wheel build | The wheel built with installed dependencies and `--no-build-isolation`. | The default isolated build could not download build dependencies. |
| Installed workspace | The wheel initialized a VALID workspace with zero documents and zero catalog entries. | An empty workspace supplies no approved knowledge. |
| Installed sample collection | All 37 samples passed normally with 185 warnings; strict mode returned exit code 1. | Samples retain unresolved evidence and reviews. |
| Installed regression cases | Inline code, fenced HTML, and indented heading cases passed. Body sample references produced warnings. | These checks cover the confirmed cases only. |
| Input preservation | Sample bytes and modification times remained unchanged after normal and strict checks. | Lint does not update check or review metadata. |
| Shipped resources | All 40 catalog files and 21 checked shared resources matched isolated source bytes. | Generated workspaces contain no runtime source or runtime tests. |
| Schema export | The installed export matched the catalog schema. | The schema remains separate from governed knowledge contracts. |
| Documentation | Local links, prose limits, and staged whitespace checks passed. | Complete ASD-STE100 review remains pending. |

The wheel SHA256 is `fbb2da0562831f2659ae3a12f7a6bceb4ecfa86bf8ca40a2d52396c138d14d1a`.
The installed runtime used existing dependency packages without network access.
The installation used `--no-deps --no-index` outside the source checkout.

## Commands

Run commands from the standalone source checkout with its Python environment active.

```sh
python -m unittest discover -s tests -p test_artifact_lint.py -v
python -m unittest discover -s tests -v
python -m pip wheel . --no-deps --wheel-dir dist
python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist
ai-sdlc --workspace PATH validate
ai-sdlc lint ARTIFACT_PATH
ai-sdlc lint ARTIFACT_PATH --strict
git diff --cached --check
```

## Remaining limits

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Shared graph renderer failure remains. | The working-tree assertion expected 21 trace edges and observed 19. | The shared full suite does not pass. | unknown | Resolve the concurrent graph change and rerun its test. |
| Shared knowledge audit bindings are incomplete. | Three changed documents lack matching current-content transition events. | Shared workspace validation fails. | unknown | Record the actual governance changes through new audit events. |
| Complete writing review remains pending. | Automated checks cover selected writing rules only. | Full ASD-STE100 compliance is not established. | unknown | Perform the complete writing review and record its reviewer and date. |
