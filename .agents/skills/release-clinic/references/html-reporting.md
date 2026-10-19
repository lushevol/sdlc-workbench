# Generate a release HTML report

Read this reference when the user requests a release report or asks how HTML reporting works.
The [included dtp-tda-report skill](dtp-tda-report.md) contains the complete analysis rules and HTML template.
Check it against the installed upstream source for each report. This reference adapts its procedure to Workbench paths.

## Included upstream source

`dtp-tda-report.md` is a byte-identical distribution copy of the bundled upstream `SKILL.md`.
The authoring source remains `core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/SKILL.md` in the Workbench source checkout.
Refresh the included copy from that source when adopting upstream skill changes.
Do not maintain separate rule or template edits in the included copy.
Wheel builds and workspace initialization include this reference through the existing shared-skill copy.

The included frontmatter records the upstream identity, version, and model provenance.
Workbench agents retain their current model.

## Check the report instructions

Run `release-clinic path` for the selected workspace and read its `report_skill` path.
From that workspace, compare the complete included instructions with the returned source:

```sh
python .agents/skills/release-clinic/scripts/check_report_parity.py --upstream REPORT_SKILL_PATH
```

Replace `REPORT_SKILL_PATH` with the returned path. Quote paths that contain spaces.
The helper reads both files without changing them. It makes no network requests.

| Status | Exit code | Required action |
| --- | --- | --- |
| `MATCH` | 0 | Read and follow the complete included reference. Its bytes match the installed upstream skill. |
| `MISMATCH` | 1 | Read and follow the complete installed upstream skill. Record the mismatch and selected source hash. |
| `ERROR` | 2 | Resolve the missing or invalid source before claiming parity. An included-only report must state that parity remains unconfirmed. |

Compare content hashes even when version numbers match.
Use one selected edition for rules, templates, and report version metadata.
Do not silently use a stale included edition or mix content from different editions.
Refresh the included copy during skill maintenance after reviewing the upstream changes.

## Select inputs and installed sources

Use the selected workspace and the user's collector JSON.
Obtain missing release inputs before collection or analysis.
Do not substitute a demonstration report for the user's release.

```sh
ai-sdlc --workspace PATH release-clinic path
```

Read `report_skill` from the returned JSON.
Its parent directory is the upstream skill directory.
Use that directory for every `$SKILL_DIR` reference in the selected instructions.
The returned `scripts` directory contains collector configuration and the standalone generator.
Generated workspaces use these installed paths; they do not contain the upstream runtime source.
Record the content parity result with report provenance.

Read the exact input JSON again for every invocation.
Both `AutoTDAResults_<STREAM>_<release_id>.json` and `AutoTDASummary_<STREAM>_<release_id>.json` are supported.
Use the upstream format detection rules to interpret full or compact data.
Apply upstream suppression rules before treating missing data as a finding.
Record material evidence limits without creating findings that explicit upstream rules prohibit.

The bundled version mentions `analyze_genie_scenario_tags.py`, but that helper is absent from the installed scripts.
For legacy Genie input, retain the upstream per-story ST/IT evidence limit.
When recollection is authorized, use the collector to obtain the missing breakdown.
Do not invent per-story counts or invoke the absent helper.

Read the effective collector stream configuration once.
Use the root-resolved `TDA_STREAM_CONFIG` override when configured; otherwise use `scripts/stream_config.yaml`.
`doctor` reports the selected configuration paths, even when collection configuration is incomplete.
Validate the stream against the actual `streams` keys and retain its configuration block.
Apply the upstream missing-file procedure if the configuration cannot be read.
The service's `STREAM_CONFIG_FILE` has a different schema.

## Analyze and author the report

Follow the selected upstream edition's sections in this order:

1. Read `Step 1 — Read JSON Output`, version checks, and `Analysis Rules`.
2. Apply `Report Format`, all applicable `Summary Tables`, and `Gate Verdict`.
3. Complete `Step 3 — Generate HTML Report` using its canonical CSS and HTML shell.
4. Write the file and run `Mandatory post-write integrity check — remediation system` against that same path.

Author the Markdown analysis and HTML directly for this mode.
The upstream guardrail prohibits using `gen_tda_report.py` as an agent-report shortcut.
Its separate implementation can lag behind the current skill's rules.
Do not invoke the script through `release-clinic report` during this skill's report flow.

Keep the canonical severity colors, finding format, section organization, and verdict mapping.
Retain the expanded Summary Tables `<details>` element.
Include the Stream Configuration Snapshot appendix and its configuration-time caveat.
That snapshot describes report-generation settings; it does not prove collection-time settings.

### Apply upstream rule precedence

Explicit suppression and skip rules take precedence over generic empty-data rules and stale shell examples.
Use the same resulting findings, counts, tables, and verdict in Markdown and HTML.
The following conflicts were confirmed in version `1.11.1` at SHA-256 `3c0d4b182dad89c43292aa1e5522184a16b2f5ca441e97777262cae0bb3fcb76`.
For a different selected edition, inspect its explicit rules before applying these examples.

- Suppress Release WI and story state-alignment findings, including the stale pre-release story-state shell block.
- Omit absent parent Application details and Application approvals as the upstream guardrails require.
- Apply disabled SNOW, Sonar, regression, and optional-check rules before testing empty results.
- Apply the automation-only exception before classifying empty manual test results as CRITICAL.
- Preserve alternate PIT evidence, Genie traceability, and informational-only classifications from the full rules.

The current upstream shell omits some tables and columns required by its analysis and Report Format sections.
Include each applicable required table and column inside Summary Tables, using the canonical table and section-title styling.
Preserve the complete canonical CSS and remediation JavaScript.

Check implementation/backout evidence, Application approvals, acceptance email evidence, and stories.
Also check field completeness, traceability, test results, and Sonar exclusions.
Keep the required manual Evidence Source and Sonar gate Status columns.
Do not add a suppressed table because it appears in a generic shell example.

Copy the complete remediation toolbar and JavaScript from the current HTML shell.
They provide reviewer naming, finding annotations, and Save Annotated Report.
Annotated export requires a saved status and note for every CRITICAL or MODERATE finding.
Do not truncate those blocks during HTML construction.

Escape raw source text once. Preserve trusted template markup and entities without double escaping.
Check work-item links against the actual ADO organization, project, and deployment type.
Some upstream link examples assume cloud ADO URLs.

Read `metadata.version` from the selected skill edition for the report's tooling version.
Retain collector version, collection time, release identity, and source identities from the input when available.
Use the upstream environment lookup for Generated By, with `Unknown` when unavailable.
An environment username does not authenticate the generator or identify a release approver.
Apply version drift and staleness rules to collected evidence; a failed version check does not establish staleness.
Upstream staleness text does not establish approval or release sign-off.

## Save and verify

Select a workspace output path instead of the upstream platform-specific Downloads examples.
Honor an explicit user output path.
Otherwise use `TDA_OUTPUT_DIR` or `.workbench/release-clinic/reports`, relative to the workspace when needed.
Use a separate run directory when an earlier report exists.

Use `TDAReport_<STREAM>_<release_id>.html` with filename-safe identifiers.
Create the output directory and write the populated report as UTF-8 through a local file command.
Keep retained input bytes and earlier outputs available.

Adapt the upstream integrity check's output path to the actual saved file.
Its six checks require these elements:

| Check | Required content |
| --- | --- |
| Remediation toolbar | `class="rem-toolbar"` |
| Reviewer naming | `remSetName` |
| Annotated export | `remExport` |
| Initialization listener | `DOMContentLoaded` |
| Remediation script | `<script>` |
| Complete document | File ends with `</html>` after trailing whitespace removal. |

Correct incomplete HTML and repeat the checks before claiming completion.
Those six markers do not prove complete script bodies or working controls.
Compare the full CSS and remediation script against the selected source when checking generated report integrity.
Check populated placeholders, release identity, finding counts, table contents, and verdict consistency against the analysis.
Retain commands, versions, input hashes, output hashes, selected configuration identity, and check results.

Include the writing-review block from the parent skill, with status based on actual checks.
Keep `asd_review: PENDING` unless a complete writing review occurred.

Open the HTML in an available browser when validating layout or annotation behavior.
Check Summary Tables, Set Reviewer Name, Remediate, and Save Annotated Report when those controls need verification.
Use an explicit reviewer identity only when supplied for that review.
Preserve the original report and any annotated export separately.
Structural checks alone do not verify browser behavior.

Version `1.11.1` has a confirmed shared control defect in the canonical shell identified above.
After reopening an annotated export, Remediate buttons do not open their panels.
Saved annotations, reviewer naming, and export still work in the tested Chromium browser.
Retain the original report for further annotation and disclose this limit when delivering affected reports.
Do not claim that reopening verification passed or silently change canonical JavaScript.

Return the saved HTML link, the analysis, observed checks, and remaining review needs.
A gate verdict describes the report's assessment. It does not establish release approval or verified business behavior.

## Standalone script boundary

The integration guide documents an independent initial-report CLI utility for operators.
That utility does not execute this agent skill and does not establish parity with its current rules.
Keep it outside the `dtp-tda-report` report flow.
