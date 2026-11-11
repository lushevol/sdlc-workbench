# Source folder layout correction

Date: 12 November 2026, Asia/Singapore.
References: [folder question](user-layout-question.md#exact-user-input) and [cleanup authorization](user-layout-cleanup.md#exact-user-input).

**Remove the extra top-level raw directory. Preserve original source documents and their hash bindings.**

## Scope and risk

Use `evidence/knowledge/incoming/COLLECTION/` for replaceable complete exports.
Keep retained originals under `evidence/knowledge/sources/`.
Keep selection metadata under `evidence/knowledge/selections/` and generated filtered views under ignored `.workbench/` storage.
Canonical knowledge, the derived wiki, schemas, and templates retain their existing responsibilities and locations.

The affected interfaces are source input validation, workspace generation, package inclusion, documentation, and source preparation tests.
The runtime change has material integrity risk if it permits protected evidence directories or changes existing source identities.
No existing source, manifest entry, selection, or audit event requires relocation or modification.
No new dependency or external access is required.

## Authorized removal

| Removed path | SHA-256 | Prior Git revision | Reason |
| --- | --- | --- | --- |
| `raw/README.md` | `43ca3452c1ca4fca5cc89d71ac1e831303b71bcd426e502e05e1841823c78dac` | `7a4a9d3019a76e9794e49baa6830799429efb903` | Remove the confusing extra root. Put import instructions in the existing evidence guide. |

The removed directory contained one guide and no source documents.
The prior guide remains available in Git at the recorded revision.
Active references and generated-workspace packaging must use the existing evidence guide instead.

## Baseline

The checkout contains 85 retained Confluence Markdown sources and 68 existing audit events.
Source manifest SHA-256: `5d95c78cec4a5ad94ee4609be9f8dfc134f52e2c5cf2a1cde5d5aad348341b4a`.
Selection index SHA-256: `b316af7cd0e22484ec5f56a70f4623f6fbf0007c16672adf31033dbbf28e267c`.
The unrelated untracked `core/release-report/` directory is outside this change.

## Required verification

1. Accept the new evidence inbox without permitting unrelated protected evidence paths.
2. Preserve source identity and manifest bytes when switching an existing collection to a new inbox.
3. Retain old snapshots and require review when a new inbox page changes.
4. Confirm generated workspaces omit the extra raw root and retain source preparation instructions.
5. Check all original source hashes, the source manifest, selection metadata, and prior audit bytes.
6. Run focused cases, the complete runtime suite, wheel installation, generated-workspace checks, and workspace validation.

## Progress

The user input is preserved before investigation and delegation.
Documentation and runtime changes are assigned separately to prevent conflicting edits.
The initial source, manifest, selection, and audit hashes are retained in ignored runtime storage for final comparison.
No source payload was copied into a new inbox during this cleanup.

### Initial focused run

The runtime agent ran 21 source preparation cases in 1.805 seconds.
Twenty cases passed. The generated-workspace assertion failed while the old raw guide remained in the scaffold.
This intermediate result preceded the packaging edits. The final run must include the corrected scaffold.
The new inbox identity, revision retention, generic input, and protected-path cases passed.
No assertion was weakened or removed.

### Completed focused run

All 21 source preparation cases passed in 1.875 seconds, with zero failures, errors, or skips.
The final scaffold resolved the intermediate generated-workspace failure.
Checks cover unchanged identity reuse, changed revision retention, protected evidence, generic inputs, and absence of the extra root.
The documentation agent verified three added links, scaffold paths, ignore rules, and scoped diff formatting.

### Independent review

No actionable defect remained after review. All 21 focused cases also passed independently in 1.979 seconds.
The review confirmed the narrow inbox exception, existing path protections, legacy identities, and consistent package guidance.

## Declared behavior and traceability

### LC-1 Preserve source identity across inbox changes

```gherkin
Scenario: Preserve source identity across inbox changes
  Given a collection has retained source pages and reviewed decisions
  When refresh reads the same relative pages from the evidence inbox
  Then source identities and unchanged manifest bytes remain identical
```

### LC-2 Keep generated workspaces free of the extra raw root

```gherkin
Scenario: Keep generated workspaces free of the extra raw root
  Given the installed package contains the corrected scaffold
  When the CLI initializes a workspace
  Then the workspace has source preparation guidance and no top-level raw directory
```

### LC-3 Preserve input boundaries and compatibility

```gherkin
Scenario: Preserve input boundaries and compatibility
  Given an input path identifies unrelated protected evidence or an existing generic import
  When refresh validates that path
  Then protected evidence fails while the supported generic input succeeds
```

### Criterion-to-test coverage

| Criterion | Direct assertion | Execution |
| --- | --- | --- |
| [LC-1](#lc-1-preserve-source-identity-across-inbox-changes) | [test_new_inbox_preserves_legacy_source_binding_and_changed_page_history](../../../tests/test_source_preparation.py#L77) | Passed. |
| [LC-2](#lc-2-keep-generated-workspaces-free-of-the-extra-raw-root) | [test_generated_workspace_review_lifecycle_and_idempotent_refresh](../../../tests/test_source_preparation_cli.py#L70) | Passed. |
| [LC-3](#lc-3-preserve-input-boundaries-and-compatibility) | [test_other_evidence_folders_remain_protected](../../../tests/test_source_preparation.py#L125) | Passed. |

LC-3 also uses [the generic import case](../../../tests/test_source_preparation.py#L116).
All three declared criteria have direct assertions. They cover local source preparation, without business conformance claims.

### Criterion-to-code coverage

| Criterion | Changed implementation | Boundary |
| --- | --- | --- |
| LC-1, LC-3 | [refresh_sources](../../../core/ingestion/sources.py#L351) | Narrow input-path exception. Existing import and retention code remains active. |
| LC-2 | [scaffold](../../../scaffold.json) and [package inclusion](../../../MANIFEST.in). | Remove the raw guide from new workspaces. |

All three criteria trace to changed interfaces. Existing identity handling supplies required unchanged behavior.

### Code-to-test coverage

| Changed responsibility | Direct checks | Additional validation |
| --- | --- | --- |
| Runtime input validation | LC-1, LC-3 | Existing source, context, policy, and snapshot cases. |
| Workspace and package layout | LC-2 | Installed-wheel workspace exercise. |
| Guides and ignore rules | Manual document checks | Links, commands, package paths, and ignored inbox checks. |

Both changed executable responsibility groups have direct assertion coverage. No measured line coverage is claimed.

## Final retained-source checks

All 85 original source pages retain their exact bytes and SHA-256 values.
The source manifest and selection index retain their baseline hashes.
All 68 prior audit event files retain their exact bytes. One new candidate event records the revised ingestion procedure.
The top-level raw directory is absent. No source payload was copied into the new inbox.

## Installed wheel and generated workspace

The wheel built without dependency downloads and was installed into a temporary target outside the checkout.
Runtime origin matched that installed target. Existing virtual-environment dependencies were reused.
Wheel SHA-256: `d94111f8da190a7330e2804fdf0da21deeadd6ace5b84a27154972685171e53b`.

The wheel and generated workspace contain no top-level raw directory.
The existing evidence guide, inbox ignore rule, source preparation reference, and skill instructions are present.
Generated catalogs and source manifest were empty. Runtime Python source and package build configuration were absent.

A fixture collection passed refresh, selection, view creation, readiness verification, and workspace validation.
Source and output hashes matched. Unchanged reimport created zero revisions or payloads and preserved manifest bytes.

## Final validation and limits

The complete runtime suite ran 937 cases in 81.998 seconds.
All 935 executed cases passed. There were zero failures and errors.
Two existing optional Node integrations remained disabled by their environment flag. No failing case was disabled.
The complete command used the declared suite with loopback HTTP fixture access.
Command: `.venv/bin/python -m unittest discover -s tests -v`.
Runtime output SHA-256: `e8e926cbfb181d0a49195e5aeb8abf2a7486e1353a0355e560524e2bb3326d17`.

Workspace validation passed with 14 documents and zero findings.
All 212 checked local documentation references, headings, and line targets resolved.
Source verification reports the existing MOM hold and no stale or invalid bindings.
The 61 selected source inputs and 24 omissions retain their previous decisions.

Native Windows and external source-system exports were not executed.
Knowledge reconciliation and wiki synthesis remain separate stages. This layout correction changes neither meaning nor publication.
The inbox can overlap retained bytes while an incoming export is present. Repeated imports reuse retained payloads.
No additional source payload exists because of this cleanup.

## Final source identities

| Changed source | SHA-256 |
| --- | --- |
| `core/ingestion/sources.py` | `bdcecc94c6f15adff0d89d611e09e1311d68638351748fad0e4bf6a70f460227` |
| `tests/test_source_preparation.py` | `a32b0e4f37716e696ea56ab9798ecfa18a3515e16e9bdc373d63cad531b865f7` |
| `tests/test_source_preparation_cli.py` | `dc01831180960e20c45a6d85fa8ed9273879ed4379ce939225cee69a39aa3df2` |
| `.agents/skills/ingest-knowledge/SKILL.md` | `6b5b54ea6302dec6601a9bd5d42406630486cfa769bf2fc9a9b9eb24cd046089` |
| `.agents/skills/ingest-knowledge/references/source-preparation.md` | `7dbb3faca18483cee37d568a29ab15c307a97f7fd1874fe85f9f0ab3b1ad8fe2` |
