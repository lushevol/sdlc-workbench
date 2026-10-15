---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Samples establish no approved business intent, actual implementation, or business execution.
  - Gherkin checks cover selected structure only. No official parser or business step definitions executed.
---

# SDLC template catalog stage

The [catalog](../../knowledge/templates/sdlc/README.md) contains 37 authoring guides and one connected fictional sample context.
Each guide supplies AI instructions, a copyable template, an illustrative sample, and completion checks.
The [requirement guide](../../knowledge/templates/sdlc/requirement.md) includes description, rationale, measurable Gherkin, and matching structured acceptance fields.
The user's current request supplies the consumer and scope for these reusable authoring resources.

## Scope and risk

The change adds 39 catalog Markdown files and updates two navigation guides.
Affected interfaces are template discovery, packaged workspace resources, and workspace initialization.
Existing packaging and initialization already copy the template directory recursively.
The six runtime knowledge types remain the governed transfer targets.
Authoring forms use `artifact_kind` and do not define additional runtime knowledge types.

Runtime risk is low because this stage changes documentation only.
Semantic risk concerns copied sample rules, missing source authority, and unsupported verification claims.
The shared instructions label samples, separate evidence states, and require actual review and retained execution.
No governed project record changes in this stage.

## Validation observations

| Check | Observed result | Evidence limit |
| --- | --- | --- |
| Runtime suite | All 78 existing tests passed. | The mock HTTP registry required local loopback permission. |
| Source workspace | VALID; nine documents; zero findings. | Structural and provenance validation does not establish business correctness. |
| Catalog coverage | All 37 requested guides exist. | Combined catalog entries remain combined authoring forms. |
| Copyable forms | All 74 template and sample envelopes parsed. | Authoring envelopes require transfer into supported knowledge contracts. |
| Structured snippets | All 104 checked YAML blocks parsed. | Placeholder values require replacement before real use. |
| Template consistency | Template and sample section lists matched for all 37 guides. | Human review must assess meaning. |
| Source and review defaults | Samples retained unknown owners, pending reviews, and unavailable evidence values. | Illustrative sources have no business authority. |
| Gherkin structure | All 14 blocks contained a Feature and scenarios with Given, When, and Then. | Selected structure checks do not replace an official parser or assertions. |
| Local links | All 151 catalog links resolved. | Real authored documents need their own source and relationship checks. |
| Writing checks | Prose sentence, table sentence, and paragraph limits passed. | Full ASD-STE100 review remains pending. |
| Wheel build | The wheel built with installed build dependencies and `--no-build-isolation`. | The default isolated build could not download build dependencies. |
| Installed workspace | The installed wheel initialized and validated a workspace outside the checkout. | PyYAML came from the installed dependency without network access. |
| Shipped catalog | All 39 catalog files matched source bytes in the wheel and initialized workspace. | Samples remain authoring resources. |
| Shared resources | All 21 checked schemas, shared skills, and responsibility guides matched source bytes. | Runtime source, runtime tests, and pyproject.toml remained outside generated workspaces. |
| Starter isolation | The initialized workspace contained zero documents, catalog entries, source records, and audit events. | Empty structure does not imply approved knowledge. |
| Requirement transfer | An illustrative candidate transferred into the supported Requirement contract and validated with zero findings. | The check establishes structure and retained sample provenance only. |
| AI usability | A separate agent drafted denied-access criteria with count 0 and an additional denial-message assertion. | The simulation used fictional context and performed no business execution. |

The wheel SHA256 is `3ff22f3924893b21c42f02e2d67cf9d221cac70bc62071ae22b4d7590c255b6d`.
No new runtime tests were needed for this documentation stage.
Existing tests and temporary checks exercised the affected packaging and contract boundaries.

## Commands

Run commands from the standalone source checkout with its Python environment active.

```sh
python -m unittest discover -s tests -v
ai-sdlc --workspace . validate
python -m pip wheel . --no-deps --wheel-dir dist
python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist
git diff --check
```

The first wheel command failed when restricted network access blocked build dependency retrieval.
The second command used installed build dependencies and succeeded.
The wheel was installed with `--no-deps --no-index` in a separate temporary environment.
The installed `ai-sdlc` command initialized and validated the temporary workspace.

## Measurable acceptance observations

```gherkin
Feature: Author SDLC artifacts from reusable guides

  Scenario: Find every requested authoring form
    Given the requested catalog contains 37 artifact kinds
    When the catalog and its linked guides are inspected
    Then exactly 37 guides provide template and sample blocks
    And all 74 blocks contain the common authoring envelope

  Scenario: Transfer a requirement into the supported contract
    Given the requirement sample and retained illustrative context bytes
    When their content becomes a candidate Requirement with measured acceptance fields
    Then validation reports zero findings for one candidate
    And no human approval or business execution is recorded

  Scenario: Ship templates without project records
    Given the built wheel installed outside the source checkout
    When its installed command initializes a workspace
    Then all 39 catalog files match their source bytes
    And the initial workspace contains zero governed documents
    And every catalog has zero entries
```

## Remaining review

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Complete writing review remains pending. | Automated checks cover selected sentence, paragraph, structure, and link rules only. | Full ASD-STE100 compliance is not established. | unknown | Perform the complete writing review and record its actual reviewer and date. |

No implementation blocker remains for the requested authoring catalog.
