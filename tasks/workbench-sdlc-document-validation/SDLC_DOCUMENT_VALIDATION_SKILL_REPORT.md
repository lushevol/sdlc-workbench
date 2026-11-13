---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# SDLC document validation skill

## Purpose and scope

The user requested a skill for document schemas, essential fields, and Gherkin acceptance criteria.
The current consumer is a coding agent that reviews the SDLC authoring catalog's completed documents.
The skill combines existing deterministic validation with separate content review.

The [canonical skill](../../.agents/skills/validate-sdlc-documents/SKILL.md) uses `ai-sdlc lint` for authoring artifacts.
It uses workspace validation for supported governed knowledge records.
Ordinary documents receive an explicit manual comparison against the applicable template.
Catalog guides require inspection of their inner Template or Sample blocks.

Changes cover skill instructions, discovery aliases, packaging declarations, navigation, and packaging regressions.
The qualitative risk is low.
The stage adds no runtime implementation or dependencies.
Canonical instructions remain under `.agents/skills/validate-sdlc-documents/`.
Discovery aliases expose them through `skills/` and `.claude/skills/`.

## Validation evidence

| Check | Observed result | Scope or limit |
| --- | --- | --- |
| Skill creator's `quick_validate.py` | PASSED | Frontmatter, naming, and unfinished scaffolding checks. |
| Artifact lint regression suite | 51 tests passed. | Existing schema, Markdown, acceptance, and read-only behavior. |
| Workspace layout suite | 17 tests passed. | Discovery, canonical bytes, packaging, and denied directory-link fallback. |
| Isolated standalone source suite | 279 tests passed. | Tracked baseline plus this stage; unrelated graph edits excluded. |
| Wheel build | PASSED | Used installed build dependencies with `--no-build-isolation`. |
| Source distribution | PASSED | One canonical skill; discovery copies excluded. |
| Wheel installation outside checkout | PASSED | Installed module path confirmed outside the source checkout. |
| Generated workspace | VALID | Empty catalogs and zero governed documents. |
| Installed skill discovery and reading | PASSED | CLI returns the canonical skill bytes. |
| Shipped templates and knowledge schemas | PASSED | Generated copies match source bytes; 40 catalog files remain available. |
| Runtime ownership boundary | PASSED | Generated workspace has no runtime Python source, runtime tests, or `pyproject.toml`. |
| Source workspace validation | VALID | 12 governed documents; zero findings. |
| Local references and prose sentence length | PASSED | Selected checks only; full ASD review remains pending. |
| Independent workflow evaluation | PASSED | Expected defects reported; all selected input hashes preserved. |

The isolated source baseline is `4da389b39fae889cdd8f7de7a7f24035e93cf744`.
The stage overlays only its own files and discovery links.
The final portability test adjustment passed a separate 17-test layout run.
The tests ran on macOS with Python 3.14.
Directory-link denial was simulated; Windows execution was not performed.

The wheel SHA-256 is `84c15a5c073bbc804511c17eb2f79a916d5965e6a4a216b3925543457be33c5c`.

These commands ran from the isolated standalone source checkout:

```sh
python -m unittest discover -s tests -v
python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist
python -m unittest discover -s tests -p test_workspace_layout.py -v
```

The installed command validated a new workspace outside that checkout:

```sh
ai-sdlc --workspace GENERATED_WORKSPACE validate
ai-sdlc --workspace GENERATED_WORKSPACE skills
ai-sdlc --workspace GENERATED_WORKSPACE skills validate-sdlc-documents
```

## Independent workflow evaluation

An independent agent received the skill, temporary documents, and a validation request.
The request covered authoring artifacts, ordinary prose, a governed requirement, and a catalog sample.
It also requested normal and strict handoff results.
The agent completed ten validator commands and a separate content review.
The selected documents are fictional evaluation fixtures, not approved business records.

| Input | Automated result | Agent content result |
| --- | --- | --- |
| Requirement A | Normal and strict failed: three errors and four warnings. | Missing owner, missing Rationale, and reversed Gherkin steps were reported. |
| Requirement B | Normal passed with five warnings; strict failed. | Gherkin required two invoices; the structured criterion required one. |
| Requirement C | Normal passed with five warnings; strict failed. | Acceptance representations matched; evidence and reviews remained incomplete. |
| Ordinary requirement D | Automated validation did not run. | Missing contract, essential content, and measurable acceptance criteria were reported. |
| Governed requirement | Workspace returned INVALID and reported missing `version`. | Further missing fields, sections, structured criteria, and source provenance were reported. |
| Extracted catalog sample | Normal passed with five warnings; strict failed. | Illustrative status, incomplete reviews, and acceptance agreement were reported. |

The combined authoring run returned three errors and fourteen warnings in both modes.
The agent preserved the catalog guide and five prepared documents without changes.
It preserved the extracted sample's exact bytes.
Root independently confirmed the five prepared document hashes.
No business tests or document corrections occurred.

The content review also reported missing dependency metadata in the illustrative sample.
That finding remains separate from automated schema results and this skill's interface checks.
The final independent skill review found no consequential omissions or interface blockers.

## Evidence limits and next action

The skill preserves automated statuses and reports semantic contradictions separately.
The linter checks selected English Gherkin syntax without executing step definitions.
Workspace requirement validation checks structured clauses, not complete fenced Gherkin syntax.
No passing result establishes business correctness, source authority, publication approval, or verified execution.

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Gherkin syntax and schema checks do not establish semantic agreement. | Conflicting numeric limits can pass automated lint. | Document owner; unknown when unavailable. | Compare descriptions, structured criteria, scenarios, and measurement conditions. |
| The illustrative sample names `SAMPLE-REQ-002` in Dependencies but keeps `related_ids: []`. | Metadata consumers can miss that declared dependency. | Sample owner: unknown. | Confirm the relationship and align metadata before real use. |
| Full ASD review is pending. | Automated prose checks cannot establish complete compliance. | Writing reviewer: unknown. | Perform a complete writing review before claiming compliance. |

Important governed requirements and decisions still require recorded human review before publication.
The skill must preserve source snapshots and append-only audit history during authorized corrections.
