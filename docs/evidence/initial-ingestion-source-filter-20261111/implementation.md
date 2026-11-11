# Source preparation pipeline implementation

Date: 11 November 2026, Asia/Singapore.
Reference: [implementation request](user-implementation.md#exact-user-input).
Follow-up: [source and knowledge folder question](user-layout-question.md#exact-user-input).
Design: [pipeline and storage design](recommendation.md#full-export-pipeline).

**The local source preparation pipeline is implemented. MOM remains held for missing attachment context.**

## Scope and risk

Implement local full-export import, source selection, generated views, and freshness verification.
Keep semantic classification and knowledge synthesis in the existing agent skills.
Keep knowledge review, publication, and wiki compilation separate from source preparation.

The affected interfaces are the installed CLI, source manifest, selection index, generated source links, and workspace instructions.
Source integrity has material risk. A changed export must never overwrite registered snapshots or silently reuse stale exclusions.
Generated outputs must not overwrite user files. Every link must retain the source-page SHA-256.
No new dependency, external service, credential, or startup download is required.

## Processing contract

1. Accept the complete Markdown export in a writable import directory.
2. Reuse retained source bytes, or append a new source revision and snapshot.
3. Record hash-bound decisions in `evidence/knowledge/selections/<source-id>.json`.
4. Generate selected exact excerpts or complete-page links in ignored working storage when requested.
5. Reconcile canonical knowledge through existing ingestion and review procedures.
6. Compile the wiki from canonical knowledge through its existing bridge.

New or changed source pages require review. This includes previously excluded pages.
Changed policy or governing context also invalidates a decision.
Missing pages remain recorded without deleting retained evidence or derived knowledge.

## Required checks

- Source revisions, snapshot reuse, and separate source identities for equal bytes.
- Stale source, policy, and context detection, including excluded and missing pages.
- Hash-bound links and excerpts with exact original-to-output ranges.
- Rejection of unsafe paths, malformed selections, and retained-source tampering.
- Real import and selection of the existing 85-document export.
- Runtime tests, wheel build, and generated workspace validation using the installed wheel.

## Progress

The initial worktree includes unrelated wiki edits and an untracked release-report directory.
Those changes are outside this implementation scope.
Separate agents implemented runtime and guides. Independent review checked paths, freshness, hashes, and output preservation.
The primary agent completed CLI integration, real source selection, packaging checks, and final reconciliation.

### Initial CLI verification

Five CLI integration cases passed with zero failures or skips.
The independent test agent ran `python -m unittest discover -s tests -p test_source_preparation_cli.py -v`.
The run completed in 0.529 seconds.

Cases cover review lifecycle, stale exclusions, changed policy, output preservation, and hash-bound links with exact excerpt mappings.
Assertions reside in [the CLI tests](../../../tests/test_source_preparation_cli.py).
Test file SHA-256: `2c8509941a77b38e23e3f46581a49a35d1a15be8d13f0bc835555c6a9884d5c0`.
Tested CLI SHA-256: `ed623fc9ecbc9a476abe637f704b2e4e73d16772be0bb760d4a900555d74c015`.
Tested runtime SHA-256: `1dc55d2611c25e88a98e130fa5a344b3725b276d86bd71241ec5458a782cc92f`.
This initial run predates the completed runtime. The final complete-suite result below supersedes it.

### Real source preparation

All 85 existing Markdown documents were imported and reviewed through the new CLI.
The import reused every registered revision. It created zero source revisions and zero retained snapshot payloads.
The source manifest and all 85 original files retain their previous bytes and SHA-256 values.

Decisions: 6 KEEP, 55 KEEP_SECTIONS, 11 EVIDENCE_ONLY, 12 EXCLUDE, and 1 HOLD.
The generated view contains 6 complete-page links and 55 exact excerpts. It reports 24 omitted pages.
Every emitted source hash, output hash, exact excerpt, and line mapping passed independent checks.

Collection verification returns NEEDS_REVIEW because MOM remains held for missing attachment context.
This expected result prevents a complete-readiness claim. The 61 reviewed intent inputs remain available.

Durable selections: [portal-document-export.json](../../../evidence/knowledge/selections/portal-document-export.json).
Selection SHA-256: `b316af7cd0e22484ec5f56a70f4623f6fbf0007c16672adf31033dbbf28e267c`.
Source manifest SHA-256: `5d95c78cec4a5ad94ee4609be9f8dfc134f52e2c5cf2a1cde5d5aad348341b4a`.
Generated view: `.workbench/ingestion/filtered/portal-20261111/`.
View manifest SHA-256: `fd1c25d15e3bf70dda0bbb37ace72a418d42fa3338a752845d03e4f14ebf712d`.
The generated view is ignored and rebuildable. Its selection metadata remains tracked.

### Initial complete-suite run

The sandboxed full suite ran 927 cases. It reported 36 errors and two existing skips.
The errors occurred when local HTTP fixtures attempted prohibited loopback socket binding.
This environment failure does not establish a source preparation defect.
At that checkpoint, an unrestricted rerun was required. The completed rerun appears below.
No assertions were weakened and no failing cases were removed.

### Installed wheel and generated workspace

The wheel built successfully without dependency downloads.
Wheel SHA-256: `81e9fa31601d69a74b6cfd15fa7d8fd58593eb4d18c0a0c980144ec44005a438`.
The wheel was installed into a temporary target outside this checkout. Runtime origin matched that target.
The existing virtual environment supplied dependencies. This check did not install a fresh dependency set.

The installed CLI initialized a workspace with empty catalogs and source manifest.
The filter policy, source preparation reference, raw guide, and runtime responsibility guide were present.
Runtime Python source and package build configuration were absent from the generated workspace.
Fixture refresh, selection, hash-bound view, readiness verification, and workspace validation all passed.

### Completed verification

All 18 source preparation cases passed, with zero failures or skips.
Independent review found a missing-input freshness defect. Two regression cases now cover disappearance and reappearance.
A source changed during link creation also fails before a valid view manifest is published.

The unrestricted complete suite ran 934 cases in 81.415 seconds.
It reported zero failures, zero errors, and two disabled optional Node integration cases.
The 932 executed cases passed. Those optional integrations require `WORKBENCH_CONNECTOR_INTEGRATION=1`.
No case was disabled to obtain this result.

The sandboxed result remains historical evidence of loopback restrictions. The unrestricted run resolved all 36 environment errors.
Workspace validation passed with 14 documents and zero findings.
The source manifest still matches its recorded SHA-256. No canonical knowledge or wiki page changed through these commands.

The revised ingestion procedure and source selections have new candidate audit records.
Existing audit events remain unchanged. These records grant no business approval or publication.

## Declared behavior checks

These checks cover the authorized harness change. They define no business-system acceptance criteria.

```gherkin
Scenario: SP-1 Preserve complete imports and source history
  Given a registered collection contains complete Markdown exports
  When refresh imports new, changed, or equal source pages
  Then previous snapshots remain byte-identical
  And equal payloads share retained storage with distinct source identities

Scenario: SP-2 Reassess stale decisions
  Given a reviewed selection includes excluded pages and governing context
  When source bytes, policy, context, or input presence changes
  Then stale decisions cannot produce a current view
  And refresh requires review for changed meaning inputs

Scenario: SP-3 Preserve filtered source provenance
  Given reviewed whole pages and selected physical line ranges
  When a new view is generated
  Then source and output SHA-256 values match their bytes
  And exact excerpts retain original-to-output line mappings

Scenario: SP-4 Retain missing and held material
  Given a page is held or absent after refresh
  When the collection is verified or rendered
  Then readiness remains incomplete
  And the view reports omitted material without deleting retained evidence

Scenario: SP-5 Reject unsafe or inconsistent inputs
  Given malformed declarations, unsafe paths, or changed retained source bytes
  When source preparation runs
  Then the operation fails without accepting invalid source bindings
  And existing output files remain unchanged

Scenario: SP-6 Keep source stages separate
  Given canonical knowledge references a source revision
  When refresh records a changed or missing source
  Then the result identifies affected canonical records
  And the command preserves canonical knowledge and wiki content

Scenario: SP-7 Ship the supported workspace interface
  Given a wheel installed outside the source checkout
  When the installed CLI initializes and processes a fixture collection
  Then source commands and filter guides are available
  And runtime Python files are absent from the generated workspace
  And workspace validation passes
```

### Check-to-assertion coverage

| Check | Direct assertion definition | Execution |
| --- | --- | --- |
| SP-1 | [test_equal_new_payloads_share_storage_but_keep_distinct_provenance](../../../tests/test_source_preparation.py#L63) | Passed in the complete suite. |
| SP-2 | [test_policy_and_context_changes_invalidate_reviewed_exclusions](../../../tests/test_source_preparation.py#L157) | Passed in the complete suite. |
| SP-3 | [test_views_bind_links_and_excerpts_to_original_and_output_hashes](../../../tests/test_source_preparation.py#L120) | Passed in the complete suite. |
| SP-4 | [test_missing_export_page_keeps_evidence_and_flags_affected_knowledge](../../../tests/test_source_preparation.py#L94) | Passed in the complete suite. |
| SP-5 | [test_failed_decision_batch_does_not_commit_an_earlier_valid_decision](../../../tests/test_source_preparation.py#L146) | Passed in the complete suite. |
| SP-6 | [test_missing_export_page_keeps_evidence_and_flags_affected_knowledge](../../../tests/test_source_preparation.py#L94) | Passed in the complete suite. |
| SP-7 | [test_generated_workspace_review_lifecycle_and_idempotent_refresh](../../../tests/test_source_preparation_cli.py#L70) | Passed in the complete suite. |

SP-7 also passed the installed-wheel exercise described above.
All seven declared checks have direct assertion evidence. This denominator excludes business behavior and native Windows integration.

### Check-to-code coverage

| Checks | Changed implementation | Trace limit |
| --- | --- | --- |
| SP-1 | [refresh_sources](../../../core/ingestion/sources.py#L351) | Local Markdown source preparation. |
| SP-2 | [_freshness](../../../core/ingestion/sources.py#L443) | Local Markdown source preparation. |
| SP-3 | [render_sources](../../../core/ingestion/sources.py#L534) | Local Markdown source preparation. |
| SP-4 | [_summary](../../../core/ingestion/sources.py#L307) | Local Markdown source preparation. |
| SP-5 | [apply_selections](../../../core/ingestion/sources.py#L471) | Local Markdown source preparation. |
| SP-6 | [_affected_knowledge](../../../core/ingestion/sources.py#L323) | Local Markdown source preparation. |
| SP-7 | [CLI dispatch](../../../core/cli.py), [scaffold](../../../scaffold.json), and [package inclusion](../../../MANIFEST.in). | Installed wheel and generated workspace. |

All seven checks trace to implemented paths. These links do not establish business conformance or publication approval.

### Code-to-assertion coverage

| Changed unit | Direct checks | Passing evidence |
| --- | --- | --- |
| Source import, snapshot reuse, and source identity | SP-1, SP-2 | Runtime import and stale-exclusion cases. |
| Selection validation and freshness | SP-2, SP-5 | Context, policy, malformed input, atomic selection, and presence regressions. |
| Source view and hash enforcement | SP-3, SP-5 | Exact excerpts, output preservation, and changed-target regression. |
| Readiness and affected-record reporting | SP-4, SP-6 | Empty, held, missing, and canonical-reference cases. |
| CLI dispatch and shipped source guides | SP-7 | Five CLI cases and the installed-wheel exercise. |

All five changed executable responsibility groups have direct assertions. This is a traceability denominator, without measured line coverage.
Guide and policy changes received document checks. They require semantic review when applied to another source collection.

## Limits and next use

The local importer accepts regular UTF-8 Markdown pages up to sixteen MiB per file.
It does not fetch attachments, classify meaning automatically, synthesize knowledge, or refresh wiki content.
Native Windows and external source-system export execution were not tested.
The complete suite includes concurrent, unrelated repository work. That work is excluded from this implementation commit.

Replace the complete export under `raw/incoming/`, then run refresh with the same collection ID.
Review changed pages and apply their hash-bound decisions. Generate a new filtered view before canonical ingestion.
Resolve MOM's missing attachment context before claiming complete source readiness. Owner: unknown.

Final core/ingestion/sources.py SHA-256: `eff135618a2ccc634452b12ba5fb49b37744b4329e510187487b56dc30730985`.

Final core/cli.py SHA-256: `ed623fc9ecbc9a476abe637f704b2e4e73d16772be0bb760d4a900555d74c015`.

Final tests/test_source_preparation.py SHA-256: `9002bf594c7d6058e6a1949e8f1ee40fa4b61148aed9710aa241a9c2f5e91c18`.

Final tests/test_source_preparation_cli.py SHA-256: `2c8509941a77b38e23e3f46581a49a35d1a15be8d13f0bc835555c6a9884d5c0`.

Final .agents/skills/ingest-knowledge/assets/source-filter.yaml SHA-256: `f077139beb2a84be9e7fd72ec3215b29196c0e8d524aeb12e9aeda1be131df92`.

Complete-suite command: `.venv/bin/python -m unittest discover -s tests -v`.
Complete-suite output SHA-256: `63cc3d9b5d3c4683e3c1d75518bd4e9d7533b2be2f53783f780c9e742fc865a7`.
Routine command output stays in ignored runtime storage. The compact results above retain the decision evidence.
Wheel command: `.venv/bin/python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist`.

After the complete-suite run, SP-6 gained explicit canonical-record and wiki-alias preservation assertions.
All 18 focused cases passed again in 1.680 seconds. Runtime code and wheel bytes were unchanged.
Final focused output SHA-256: `9f677223e1da15812c73ded8e4d2b95af9c1a4cd7b670c320ef1cc11b2a78a30`.

## Folder layout clarification

Reference: [the user's folder question](user-layout-question.md#exact-user-input).

Inspection found one README under top-level `raw/`, with no source payloads.
All 85 Confluence Markdown sources remain under `evidence/knowledge/sources/confluence/`.
Both wiki source folders contain 12 symbolic links and no regular source copies.

| Claim | Class and confidence | Supporting source |
| --- | --- | --- |
| The added raw directory describes a replaceable import inbox. | Inspected documentation; high. | [Raw guide](../../../raw/README.md). |
| Evidence and canonical knowledge have different responsibilities. | Documented contract; high. | [Evidence guide](../../../evidence/knowledge/README.md) and [knowledge guide](../../../knowledge/README.md). |
| Core knowledge contains authoring resources. | Documented contract; high. | [Core resource guide](../../../core/knowledge/README.md). |

The separate import lifecycle protects retained snapshot bytes from overwritten exports.
It does not require another top-level directory. The added name makes the existing source layout harder to understand.
This question does not authorize source relocation or deletion. No source or folder location changed during this clarification.
