---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
- Automated checks do not check the complete approved dictionary or grammar rules.
- Source authority, current applicability, and business execution require separate review.
---

# Knowledge ingestion stage

The [ingestion skill](../../.agents/skills/ingest-knowledge/SKILL.md) now supports review and ingestion modes.
It preserves original bytes and produces classified, connected knowledge with reproducible source citations.
The [classified index](../../knowledge/candidates/index.md) provides the project entry point.
All nine topics remain candidates with unknown owners and no recorded verifiers.
Human review must establish which claims can support project sources of truth.

## Scope and risk

The change adds the `KnowledgeTopic` contract, one template, and one consequential-boundary regression test.
The existing validator uses the new schema without another execution engine.
The skill and responsibility guides describe agent-assisted synthesis separately from deterministic validation.
Affected interfaces are document validation, shipped knowledge resources, workspace initialization, and shared skill retrieval.
Runtime risk is low because the contract extends existing validation paths.
Semantic risk remains unresolved because the export lacks confirmed original authority and current applicability.

The batch contains 102 Markdown files and 445,711 original bytes.
The manifest registers those originals and the exact user ingestion request.
Topics directly cite 83 distinct documents.
The remaining 19 files contain empty pages, attachment-dependent material, navigation, historical personal registers, or repeated context.
The index records those retrieval limits.

All current originals match the earlier review's byte hashes.
That review covered 118 files.
Its 16 `Bin` files are absent from this batch and supply no new topic evidence.
The collection primarily describes the portal and UI platform.
It does not establish complete brownfield business-domain coverage.

## Validation evidence

| Check | Observed result |
| --- | --- |
| Skill structure | The skill-creator validator passed. |
| Runtime suite | All 78 tests passed, including the new topic contract boundary. |
| Workspace validation | Nine documents passed; no structural or provenance findings occurred. |
| Source preservation | All 103 retained snapshots matched their manifest hashes. All 102 originals matched prior hashes. |
| Topic integrity | Source bindings, classification folders, related IDs, local links, and citation locators passed. |
| Writing checks | Prose sentence and paragraph limits passed. Full ASD review remains pending. |
| Wheel build | Build passed with installed dependencies and `--no-build-isolation`. |
| Installed workspace | The wheel initialized and validated a workspace outside the checkout. |
| Shipped resources | The new schema, template, skill, and responsibility guides matched source bytes. |
| Starter isolation | The generated workspace contained zero project documents, source records, catalog records, and audit events. |

The default isolated wheel build could not obtain build dependencies through the restricted network.
The successful build used the installed build dependencies.
The isolated runtime received the installed PyYAML package without network access.
The test suite required local loopback permission for its mock HTTP registry.
No business repository test, deployment, external destination, or source-document command ran.

## Workflow and retrieval tests

An isolated workspace received three real documents without project-specific hints in the skill.
Review mode read them and proposed topics without registering sources, creating candidates, or recording governance events.
Ingestion created three source records, two connected candidate topics, and three audit events.
The CLI validator passed before and after repeated ingestion.
The repeated request produced zero writes and preserved every artifact hash.
The test checked raw hashes, source bindings, local links, candidate states, and audit hashes.

A separate consumer answered three questions from the isolated index and its citations.
All 25 candidate links resolved; six source declarations matched three retained sources.
The consumer retrieved timing conflicts and distinguished design claims from deployed authorization behavior.
It identified an implicit refresh-token absolute-cap issue.
The project topic now states that source claim explicitly and preserves its unresolved status.
The consumer recorded no invented approval.

The project retrieval test answered four questions and assessed one tenant-onboarding request.
It reached composition, administration, security, interoperability, analytics, and release context without a navigation blocker.
That evaluator previously authored three project topics, which limits its independence.
The isolated consumer evaluation used a separate agent.
Neither test establishes business correctness, approved intent, or execution verification.

Changed-source predecessor recovery and publication were not exercised by the isolated workflow test.
Stable ID allocation and saved review locations remain agent choices within the shipped contracts.
The tested unchanged ingestion reused its records successfully.

## Measurable acceptance observations

```gherkin
Scenario: Preserve supplied originals during ingestion
  Given 102 supplied Markdown files with retained review hashes
  When ingestion registers the batch and writes classified topics
  Then all 102 files retain their prior SHA256 hashes
  And the manifest contains 103 retained source records

Scenario: Retrieve connected project context
  Given the classified index and nine candidate topics
  When an agent answers four project questions and assesses one onboarding request
  Then all four answers reach supporting context through the index
  And zero navigation blockers prevent the assessment
  And unresolved authority and behavior limits remain explicit

Scenario: Reuse unchanged ingestion records
  Given an isolated workspace with three registered documents and two candidate topics
  When the same ingestion request repeats without source changes
  Then zero artifacts change
  And source, topic, and audit counts remain unchanged

Scenario: Ship reusable workspace resources
  Given the built wheel installed outside the source checkout
  When the installed command initializes and validates a workspace
  Then validation reports zero findings
  And the workspace contains the new topic schema, template, and ingestion skill
  And it contains zero live project records
```

Owner: unknown for unresolved source authority, current rules, and business evidence.
Next action: resolve each topic's questions with responsible owners, applicable decisions, exact implementations, and retained assertions.
