---
name: release-clinic
description: Collect release assurance data, analyze TDA reports, and summarize findings or service jobs through installed Release Clinic tools.
---

# Release Clinic

Use this procedure for release assurance collection, TDA reporting, audit extraction, and portfolio analysis.
Use the installed Workbench commands in source checkouts and generated workspaces.
Generated workspaces do not need copied runtime source.

## Check configuration

```sh
ai-sdlc --workspace PATH release-clinic doctor
ai-sdlc --workspace PATH release-clinic path
```

Read the returned JSON paths before opening installed scripts or upstream skills.
Read only the upstream skill for the requested analysis.
Use `dtp-tda-report` for one release, `dtp-tda-trends` for extracted findings, or `dtp-tda-portfolio-report` for service jobs.
Use command help and the installed parser before adding options.

Configure variables in the selected workspace's root `.env`.
Existing shell variables take precedence over `.env` values.
Keep credentials out of tracked files, reports, and command arguments.
Check the selected configuration paths and missing dependencies from `doctor`.
Do not substitute another workspace's configuration when settings are missing.

## Collect one release

```sh
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

For an agent-authored report, read the installed `dtp-tda-report/SKILL.md` returned by `path`.
Read the exact input JSON again for each invocation.
Apply its current gate rules, stream snapshot requirements, HTML template, and integrity checks.
Generate the report directly when that skill requires agent analysis.
Use a workspace output directory instead of its platform-specific Downloads examples.
Preserve the original JSON and record collector version, collection time, source identities, and active configuration.

The separate script produces an initial report when the user requests that mode:

```sh
ai-sdlc --workspace PATH release-clinic report PATH_TO_COLLECTOR_JSON
```

This command forwards the JSON path to `gen_tda_report.py`.
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
Retain the exact registry input and aggregate JSON.
Report filters, record counts, failures, and sample limits.
Job completion does not establish release quality.

## Run the optional service

```sh
ai-sdlc --workspace PATH release-clinic serve --help
```

Start the service only when the user requests hosting or service development.
Check service dependencies, bind settings, stream configuration, and credential mode first.
Vault mode requires configured Vault access and AppRole credentials.
Use `VAULT_DEV_MODE=true` only for local development with the required credential variables.
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
