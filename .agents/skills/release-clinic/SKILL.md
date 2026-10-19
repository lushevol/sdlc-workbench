---
name: release-clinic
description: Set up and use Release Clinic for release collection, TDA quality analysis, HTML reports, audits, and portfolios. Includes dtp-tda-report rules and templates.
---

# Release Clinic setup and usage

Use this procedure to install, configure, diagnose, or use Release Clinic in AI SDLC Workbench.
Use the installed Workbench commands in source checkouts and generated workspaces.
Generated workspaces do not need copied runtime source.
For an existing installation, start with configuration checks and the requested operation.

## Install the tools

Select the target workspace before changing configuration.
Distinguish the Workbench source checkout from a generated workspace.
The source checkout contains `pyproject.toml`; generated workspaces contain records, guides, and skills.
Use Python 3.10 or newer.
Reuse the project's Python environment when it exists.
Create an environment only when needed:

```sh
python -m venv .venv
```

On macOS or Linux, activate it with `source .venv/bin/activate`.
On Windows PowerShell, use `.\.venv\Scripts\Activate.ps1`.
Use `python3` when the selected system exposes that command instead of `python`.

Run the source installation from the standalone Workbench checkout:

```sh
python -m pip install ".[release-clinic]"
```

When the configured package index supplies Workbench, install its optional dependencies:

```sh
python -m pip install "ai-sdlc-workbench[release-clinic]"
```

If that index lacks the package, install the supplied Workbench wheel with its `release-clinic` extra.
Do not run `pip install .` inside a generated workspace.
Its runtime remains in the installed Python package.

## Configure variables at the workspace root

Use the selected workspace's `.env.example` as the template.
Create root `.env` only when it does not exist.
Merge missing settings into an existing file and preserve its values.
Keep credentials out of tracked files, reports, and command arguments.
Existing shell values take precedence, including explicit empty values.

| Root variables | Purpose |
| --- | --- |
| `AZURE_DEVOPS_ORG_URL`, `AZURE_DEVOPS_PAT`, `ADO_PROJECT` | ADO organization or collection URL, token, and project. |
| `CONFLUENCE_BASE_URL`, `CONFLUENCE_PAT`, `USER_EMAIL`, `CONFLUENCE_SPACE_KEY` | Confluence access and document space. |
| `SONAR_BASE_URL`, `SONAR_TOKEN` | Sonar access. |
| `GENIE_REPORT_LINK`, `GENIE_TOKEN` | Genie access. |
| `SNOW_ENABLED`, `SN_INSTANCE`, `SNOW_API_PATH` | ServiceNow activation and endpoint. |
| `CLIENT_ID`, `FERNET_KEY`, `SNOW_BLADE_KEY` | ServiceNow credentials when enabled. |
| `TDA_OUTPUT_DIR`, `TDA_LOG_DIR`, `TDA_REGISTRY_PATH` | Report, log, and service registry paths. |
| `TDA_STREAM_CONFIG`, `TDA_FIELD_CONFIG` | Optional collector YAML overrides. |
| `STREAM_CONFIG_FILE` | Optional service stream YAML override. |

Relative paths resolve from the selected workspace root.
Default outputs use `.workbench/release-clinic/reports` and `.workbench/release-clinic/logs`.
Empty YAML override values select shipped configuration files.
Collector and service stream files use different schemas.
Keep their overrides separate.
Check the selected stream's `snow_enabled` setting; it can override root `SNOW_ENABLED`.

Connector variable names map to the collector's legacy names.
For example, `AZURE_DEVOPS_PAT` supplies `ADO_TOKEN`, and `CONFLUENCE_PAT` supplies `CONFLUENCE_TOKEN`.
Shell settings override file settings across these aliases.
Direct collector names take precedence within the same source.
Read the [integration guide](../../../docs/RELEASE_CLINIC.md) for remaining aliases, proxy settings, and explicit environment file overrides.

## Check setup

Replace `PATH` with the selected workspace directory.
Quote paths that contain spaces.

```sh
ai-sdlc --workspace PATH release-clinic doctor
ai-sdlc --workspace PATH release-clinic path
ai-sdlc --workspace PATH skills release-clinic
```

`doctor` returns `READY` with exit code 0 or `INCOMPLETE` with exit code 1.
It checks local dependencies, variable presence, and selected configuration file existence.
It does not check credentials, endpoint access, YAML content, Vault settings, or release behavior.
Map `missing_configuration` names to their root aliases before adding duplicate variables.
An incomplete collector setup does not prevent local reporting from retained JSON.

Read the returned JSON paths before opening installed scripts or upstream skills.
The `scripts` path contains collector YAML defaults and executable scripts.
The `service` path contains the hosted service and its separate stream configuration.
Read only the analysis instructions needed for the requested operation.
Use the included `dtp-tda-report` reference for one release.
Use the installed `dtp-tda-trends` skill for extracted findings or `dtp-tda-portfolio-report` for service jobs.
Use command help and the installed parser before adding options.

For an offline setup check, run the requested operation's `--help` without release inputs.
Help still needs valid environment file selection; collector help also needs its Python dependencies.
For a local report check, use retained collector JSON and select an explicit output file.
External connector diagnostics use Workbench `status`, resource `list`, and granted `call` operations.
Read the [connector guide](../../../docs/CONNECTORS.md) when diagnosing those registered tools.

| Observed result | Next action |
| --- | --- |
| `ai-sdlc` is unavailable. | Activate the selected environment or use its command path. |
| `missing_dependencies` contains packages. | Install the `release-clinic` extra in the environment that runs `ai-sdlc`. |
| `missing_configuration` contains names. | Set the corresponding root variables or their supported aliases. |
| `missing_files` contains names. | Correct the selected YAML paths or clear unused overrides. |
| Explicit environment file cannot load. | Correct its root-relative path; the loader does not select a fallback. |
| Required variables remain empty. | Inspect shell overrides without printing credential values. |
| Collection prompts for build confirmation. | Continue in an interactive terminal and review the discovered builds. |

## Collect one release

```sh
ai-sdlc --workspace PATH release-clinic collect --help
ai-sdlc --workspace PATH release-clinic collect RELEASE_ID BUILD_ID STREAM
ai-sdlc --workspace PATH release-clinic collect RELEASE_ID BUILD_ID STREAM RELEASE_VERSION --use-yaml
```

Read the selected stream configuration before collection.
Validate the stream against its `streams` keys.
Use supplied release and build identities.
The collector can prompt for build confirmation and stale-build decisions.
Run it in an interactive terminal and preserve the operator's choices.
Do not supply automatic affirmative input.

Use `--rwi-only` only when the requested scope excludes build-dependent checks.
Record skipped checks with the resulting report.

## Analyze one release

Release Clinic supports two HTML reporting modes:

| Request | Procedure | Deliverable |
| --- | --- | --- |
| Generate or analyze a release report. | Follow the included `dtp-tda-report` reference. | Markdown analysis and a complete HTML report with reviewer annotation controls. |
| Generate an initial report through the script. | Run the `report` command below. | HTML with `[Requires Review]` placeholders. |

Use agent analysis for an ordinary release report request.
Read the full [included dtp-tda-report skill](references/dtp-tda-report.md) before release analysis.
It contains the upstream analysis rules, gate checks, summary tables, canonical CSS, HTML shell, and remediation JavaScript.
Read [HTML reporting](references/html-reporting.md) for input selection, installed source discovery, output preparation, and verification.
Apply these Workbench adaptations when following the included skill:

- Resolve `$SKILL_DIR` to the parent of `report_skill` returned by `release-clinic path`.
- Use the effective root stream configuration and workspace output paths described in the HTML reporting reference.
- Treat upstream model metadata as provenance; keep the current agent and model.
- Use actual ADO identity and deployment URLs when available. Record missing identity instead of assuming upstream organization defaults.
- Keep report verdicts separate from human approval and verified business behavior, including upstream staleness messages.

Write the HTML file and run its integrity checks before reporting completion.
Return a link to the saved HTML alongside the analysis.

The separate script produces an initial report when the user requests that mode:

```sh
ai-sdlc --workspace PATH release-clinic report PATH_TO_COLLECTOR_JSON --output .workbench/release-clinic/initial-report.html
```

This command forwards the JSON path to `gen_tda_report.py`.
Input and output paths resolve from the selected workspace.
Its report requires review and can differ from the current agent skill.
Do not use it as a shortcut for an agent-authored final report.
Do not present its gate verdict as human approval or verified business behavior.

## Extract audit findings

```sh
ai-sdlc --workspace PATH release-clinic audit --start-date YYYY-MM-DD --end-date YYYY-MM-DD --attachments ATTACHMENTS_DIR --findings FINDINGS_DIR
ai-sdlc --workspace PATH release-clinic audit --skip-download --attachments ATTACHMENTS_DIR --findings FINDINGS_DIR
```

Use explicit dates and separate directories for each audit run.
The audit script clears matching files in its selected output directories.
Preserve earlier HTML attachments and findings before reuse.
Use `--application-id` only when the requested scope names that application.
Without `--skip-download`, the audit reads ADO and downloads attached reports.

For trends, read the installed `dtp-tda-trends` skill and the extracted `TDAFindings_*.json` files.
Use `audit` for extraction; do not invoke the absent `extract_tda_findings.py` mentioned by upstream instructions.
Keep reviewed annotations separate from unreviewed findings.

## Summarize service jobs

Use the portfolio operation for an authorized service administrator's requested scope.
Read the installed `dtp-tda-portfolio-report` skill before interpretation.

```sh
ai-sdlc --workspace PATH release-clinic portfolio --registry REGISTRY_JSONL --stream STREAM --since YYYY-MM-DD --until YYYY-MM-DD --output PORTFOLIO_JSON
```

Omit filters only when the request includes their full scope.
Date filters use UTC days and include both boundary dates.
Create the selected output directory before writing an aggregate file.
Retain the exact registry input and aggregate JSON.
Report filters, record counts, failures, and sample limits.
Job completion does not establish release quality.

## Run the optional service

```sh
ai-sdlc --workspace PATH release-clinic serve --help
ai-sdlc --workspace PATH release-clinic serve
```

Start the service only when the user requests hosting or service development.
Check service dependencies, bind settings, stream configuration, and credential mode first.
Vault mode requires configured Vault access and AppRole credentials.
Set `VAULT_ADDR`, `VAULT_NAMESPACE`, `HC_ROLE_ID`, `HC_SECRET_ID`, `HC_VAULT_AUTH_PATH`, and `HC_VAULT_SECRET_PATH` for that mode.

Use `VAULT_DEV_MODE=true` only for local development with the required credential variables.
That mode requires `ADO_TOKEN`, `SONAR_TOKEN`, `GENIE_TOKEN`, `CONFLUENCE_TOKEN`, and `USER_EMAIL`, including supported aliases.
The service binds to `127.0.0.1:8080` by default.
Use native Uvicorn options only when the requested hosting scope needs them.
Keep service credentials, logs, and job data within the selected workspace's configured paths.
This skill does not authorize deployment or external messages.

## Retain evidence

Preserve original collected bytes, downloaded attachments, annotations, failed outputs, and separate run directories.
Record command, tool version, input paths and hashes, output paths and hashes, environment identity, and observed result.
Direct commands do not by themselves create governed knowledge or prove passing business behavior.
Use the ingestion procedure when the task requires raw snapshots or candidate knowledge.

Keep facts, inferences, missing evidence, and human review separate.
Give each finding evidence, a consequence, an owner, and a next action.
Mark unknown owners explicitly.
Keep automated checks separate from the writing review in every saved report.
Use this review block and set its check status from actual results:

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```

Report setup status, missing variable names, output locations, and remaining review needs.
Include the operation result when execution occurred.
