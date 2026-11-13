---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Artifact structure does not establish source authority, human approval, or business execution.
  - Selected Gherkin checks do not run an official parser or business step definitions.
---

# SDLC artifact lint stage

The user's request adds executable checks for the [SDLC authoring catalog](../../knowledge/templates/sdlc/README.md).
The catalog supplies 37 reusable forms with illustrative samples.
The lint command checks completed Markdown artifacts copied from those forms.
It preserves the separate governed Workbench knowledge validation contract.

## Scope and risk

The installed CLI adds `ai-sdlc lint PATH [PATH...]` and `ai-sdlc lint --print-schema`.
The `--strict` option makes warnings fail the lint gate.
The `ai_sdlc_workbench.artifact_lint` API exposes `lint_artifacts(paths, strict=False)` and `artifact_schema()`.
The [authoring schema](../../knowledge/templates/sdlc/sdlc-artifact.schema.json) describes metadata and required sections for all 37 forms.
The canonical schema ships within the installed runtime.

Affected interfaces include CLI dispatch, runtime API exports, packaged schemas, authoring instructions, and workspace resource copying.
Qualitative risk is moderate because new file parsing and CLI behavior cross the installed package boundary.
Checks must preserve existing commands and reject malformed or ambiguous artifact inputs.
The implementation reads artifact inputs and produces findings without changing their contents.

The lint integration found duplicate sample IDs in two forms.
The delivery sample now uses `SAMPLE-DELIVERY-001`.
The epic sample now uses `SAMPLE-EPIC-001`.
All 37 samples now pass together as one artifact collection.

Directory inputs recurse through Markdown files.
Authors must select directories containing completed artifacts.
Guide containers and ordinary documents require explicit artifact extraction or different input selection.
The linter must not silently omit malformed authoring records.

## Check contract

| Class | Required behavior | Evidence limit |
| --- | --- | --- |
| Schema | Check metadata types, supported artifact kinds, review structures, and required sections. | Schema structure does not establish factual correctness. |
| Identity | Reject duplicate YAML keys and duplicate artifact IDs within selected inputs. | External catalogs and repositories require separate identity checks. |
| Completion | Reject unresolved placeholders and missing required content. | Supported content still requires evidence and review. |
| Inputs | Reject malformed YAML, invalid UTF-8, symlink escapes, and oversized inputs. | The command operates within its declared local input scope. |
| Gherkin | Check selected Feature, Scenario, Given, When, and Then structure. | No step definitions or business assertions execute. |
| Acceptance | Check structured requirement criteria and numeric measure values. | Humans must assess equivalent meaning across Gherkin and structured fields. |
| Warnings | Report unknown owners, missing source references, pending reviews, and illustrative identifiers. | Warning removal requires real evidence and decisions. |
| Exit status | Errors fail normal mode; warnings also fail strict mode. | A passing gate does not grant publication approval. |

## Validation observations

The isolated stage snapshot contains commit `4bf7146a7d376db423f6c30f0799760fb6abd6d4` and this stage's owned files.
It excludes unrelated concurrent graph and ingestion changes.
The installed-wheel checks use that isolated source snapshot.

| Check | Observed result | Evidence limit |
| --- | --- | --- |
| Isolated runtime suite | All 271 tests passed, including 44 artifact lint tests. | Tests ran against the committed baseline plus this stage. |
| Shared working-tree suite | One graph renderer test failed during the 267-test run. | The failure occurred in unrelated concurrent graph changes. |
| Artifact samples | All 37 samples passed together with 185 warnings and zero errors. | Fictional samples retain unresolved ownership, review, and evidence. |
| Invalid artifacts | Regression checks rejected malformed metadata, placeholders, duplicate identities, invalid measures, and malformed inputs. | Structural checks do not establish factual truth. |
| Parser defects | Regressions cover hidden headings, empty tables, whitespace IDs, Feature ordering, and unnamed Background. | Gherkin coverage remains a selected English subset. |
| Strict mode | The installed command returned 0 normally and 1 with strict mode for the same samples. | Warnings limit handoff readiness without granting approval. |
| Read-only behavior | All sample bytes and modification times remained unchanged after both installed lint runs. | The command does not update review or check metadata. |
| Schema export | The installed export matched the canonical and shipped schemas for 37 artifact kinds. | A local reference edit does not change the installed contract. |
| Source workspace | VALID; nine documents; zero findings at the recorded check. | Concurrent ingestion can change the shared workspace afterward. |
| Wheel and installation | The wheel built and initialized a valid external workspace with zero documents. | Build dependencies came from installed packages without network access. |
| Resource availability | All 40 catalog files and 21 checked shared resources matched isolated source bytes. | Runtime source and runtime tests remained outside generated workspaces. |
| Installed failure case | A quoted numeric measure produced exit code 1 and an acceptance error. | No business test executed. |
| Documentation | Local links, selected prose limits, and diff checks passed. | Full ASD review remains pending. |

The wheel SHA256 is `2d7e52b369ceb5f36bc05d114a9e00e870081ef503c3a572c70b4997e38770cc`.
The default isolated build could not retrieve build dependencies through the restricted network.
The successful build used `--no-build-isolation` and the existing installed dependencies.
The wheel installation used `--no-deps --no-index` outside the source checkout.

## Commands

Run runtime checks from the standalone source checkout with its Python environment active.

```sh
python -m unittest discover -s tests -v
python -m pip wheel . --no-deps --wheel-dir dist
python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist
ai-sdlc --workspace . validate
ai-sdlc lint docs/sdlc
ai-sdlc lint docs/sdlc --strict
ai-sdlc lint --print-schema > sdlc-artifact.schema.json
git diff --check
```

The `docs/sdlc` path represents a directory of completed artifacts created by the consuming project.
The authoring catalog is not that directory.
The schema export writes the selected output file through shell redirection; artifact linting remains read-only.

## Measurable acceptance criteria

```gherkin
Feature: Check SDLC authoring artifacts

  Scenario: Check a structurally valid draft with unresolved review
    Given one completed artifact satisfies its selected schema
    And its owner is unknown and business review remains pending
    When normal artifact linting checks that file
    Then the command returns exit code 0
    And the JSON result contains at least one warning
    And the input bytes remain unchanged

  Scenario: Apply the strict handoff gate
    Given one artifact produces warnings and zero errors in normal mode
    When strict artifact linting checks that file
    Then the command returns exit code 1
    And the JSON result contains the reported warnings

  Scenario: Reject an invalid requirement measure
    Given one requirement contains a quoted numeric measure value
    When artifact linting checks that file
    Then the command returns exit code 1
    And the result identifies at least one acceptance error

  Scenario: Reject copied guide containers
    Given one catalog guide contains nested Template and Sample blocks
    When artifact linting checks that guide directly
    Then the command returns exit code 1
    And the result instructs the author to extract an artifact block

  Scenario: Export the authoring schema without workspace configuration
    Given the installed command runs outside a configured workspace
    When schema export runs without artifact paths
    Then the command returns exit code 0
    And the output describes exactly 37 artifact kinds
```

## Remaining review

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Shared graph renderer test failed. | The working-tree run expected 21 trace edges and observed 19. | The shared full suite has a failure outside this stage. | unknown | Resolve the concurrent graph viewer change and rerun its test. |
| Complete writing review remains pending. | Automated checks cover selected structure and writing rules only. | Full ASD-STE100 compliance is not established. | unknown | Complete the writing review and record its actual reviewer and date. |
