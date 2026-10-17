# Release Clinic

Release Clinic supplies TDA data collection, initial HTML reports, audit extraction, portfolio summaries, and an optional service.
The Workbench installs these tools under `ai_sdlc_workbench`.
Generated workspaces receive the shared skill and this guide.
They do not receive runtime source.

## Install and inspect

Run installation from the standalone source checkout.

```sh
python -m pip install ".[release-clinic]"
ai-sdlc --workspace . release-clinic doctor
ai-sdlc --workspace . release-clinic path
ai-sdlc --workspace . skills release-clinic
```

For an installed distribution, use `python -m pip install "ai-sdlc-workbench[release-clinic]"`.
`doctor` checks local dependencies and required variable names without making network requests.
It returns `INCOMPLETE` with exit code 1 when configuration or dependencies are missing.
It never prints credential values.
`path` identifies installed scripts and upstream reporting instructions.

## Root configuration

Copy the root [.env.example](../.env.example) to `.env` when that file does not exist.
Keep existing settings when adding Release Clinic variables.
The project ignores `.env` and tracks its example.
Shell values take precedence, including explicit empty values.
Direct script execution finds the enclosing project root.
Installed commands select the directory supplied through `--workspace`.

| Root variable | Consumer |
| --- | --- |
| `AZURE_DEVOPS_ORG_URL`, `AZURE_DEVOPS_PAT`, `ADO_PROJECT` | ADO collection APIs. |
| `CONFLUENCE_BASE_URL`, `CONFLUENCE_PAT`, `USER_EMAIL`, `CONFLUENCE_SPACE_KEY` | Confluence collection. |
| `SONAR_BASE_URL`, `SONAR_TOKEN` | Sonar collection. |
| `GENIE_REPORT_LINK`, `GENIE_TOKEN` | Genie collection. |
| `SCWIKI_URL`, `SCWIKI_TOKEN`, `SCWIKI_WIKI` | Optional SCWiki adapter. |
| `SNOW_ENABLED`, `SN_INSTANCE`, `SNOW_API_PATH` | Optional ServiceNow collection. |
| `CLIENT_ID`, `FERNET_KEY`, `SNOW_BLADE_KEY` | ServiceNow credential decryption when enabled. |
| `TDA_OUTPUT_DIR`, `TDA_LOG_DIR`, `TDA_REGISTRY_PATH` | Reports, service logs, and service job registry. |
| `TDA_STREAM_CONFIG`, `TDA_FIELD_CONFIG` | Optional collector stream and field YAML files. |
| `STREAM_CONFIG_FILE` | Optional service stream YAML file. |
| `PARALLEL_ENABLED`, `ADO_THROTTLE_DELAY_MS` | Collector concurrency and ADO request spacing. |
| `HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY` | Network routing. |

Legacy collector names remain supported: `ADO_TOKEN`, `ADO_ORGANIZATION`, `ADO_ORG_URL`, `CONFLUENCE_URL`, `CONFLUENCE_TOKEN`, and `SONAR_URL`.
Within one configuration source, direct collector names take precedence over connector aliases.
Relative paths resolve against the selected workspace root.
Default report and log directories are `.workbench/release-clinic/reports` and `.workbench/release-clinic/logs`.
Empty YAML path settings use the shipped files.
Collector and service stream files have different contracts.
Keep their overrides separate.

`AI_SDLC_WORKSPACE` selects an absolute workspace for direct script execution.
`AI_SDLC_ENV_FILE` explicitly selects another environment file relative to that root.
The service also supports the explicit legacy `SERVICE_ENV_FILE` setting.
A missing explicit environment file fails without a fallback.

## Collect and report

Replace the uppercase inputs with actual release identities and paths.

```sh
ai-sdlc --workspace PATH release-clinic collect --help
ai-sdlc --workspace PATH release-clinic collect RELEASE_ID BUILD_ID STREAM
ai-sdlc --workspace PATH release-clinic report COLLECTOR_JSON --output .workbench/release-clinic/report.html
ai-sdlc --workspace PATH release-clinic portfolio --help
ai-sdlc --workspace PATH release-clinic audit --help
```

The collector retains its interactive build confirmation.
Use an interactive terminal for collection.
The report command produces an initial HTML report with review placeholders.
The shared skill describes agent analysis and final report preparation.
Collection requires valid endpoint access and release inputs.
A local setup check does not establish either condition.
Some imported report links still assume cloud ADO URLs.
Review hyperlinks when using ADO Server collections.

Direct commands preserve native script output and exit codes.
They do not create Workbench action records.
Keep original input bytes, command details, configuration identity, and output hashes when retaining evidence.
The audit command can clear matching files in selected output directories.
Use a separate directory for each audit run.

## Optional service

```sh
ai-sdlc --workspace PATH release-clinic serve --help
ai-sdlc --workspace PATH release-clinic serve
```

The command binds to `127.0.0.1:8080` by default.
Native Uvicorn options can override those settings.
Vault mode uses root Vault settings and AppRole credentials.
`VAULT_DEV_MODE=true` uses environment credentials and skips Vault authentication.
Stream settings can override `SNOW_ENABLED`.
Check the selected stream before removing its ServiceNow credentials.

The service retains its existing job model and collection behavior.
This integration does not establish release approval or verified business behavior.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
