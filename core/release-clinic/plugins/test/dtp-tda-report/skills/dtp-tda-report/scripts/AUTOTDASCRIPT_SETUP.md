h1. AutoTDAScript.py — First-Time Setup Guide

Step-by-step guide for setting up {{AutoTDAScript.py}} for the first time after cloning the repository. For a description of the business checks it feeds, see AUTOTDASCRIPT_CHECKS (companion document).

Paths below are relative to the plugin root: {{plugins/test/dtp-tda-report/}}. The script itself lives at {{skills/dtp-tda-report/scripts/AutoTDAScript.py}}.

h2. 1. Prerequisites

* *Python 3.10 or later* (the codebase uses {{from __future__ import annotations}} plus PEP 604 union syntax throughout the {{tda/*}} package).
* Network access to: Azure DevOps (on-prem), Confluence, SonarQube, Genie reporting API, and (optionally) ServiceNow — directly or via the corporate proxy, depending on the host.

h3. Install Python dependencies

From the plugin root:

{code:language=powershell}
cd plugins/test/dtp-tda-report
pip install -r requirements.txt
{code}

This installs {{requests}}, {{PyYAML}}, {{beautifulsoup4}}, {{lxml}}, {{atlassian-python-api}}, {{python-sonarqube-api}}, {{cryptography}}, {{rapidfuzz}} (with {{fuzzywuzzy}}/{{python-Levenshtein}} as a fallback), plus the legacy-only {{pandas}}/{{tabulate}}/{{python-docx}} (not required by the current {{AutoTDAScript.py}}, only by the deprecated {{AutoTDAScript_Legacy.py}}).

h2. 2. Locate the scripts folder

All commands from here on assume you are in:

{code:language=powershell}
cd plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts
{code}

This folder contains {{AutoTDAScript.py}}, the {{tda/}} package, {{.env.example}}, {{stream_config.yaml}}, and {{ado_field_config.yaml}}.

h2. 3. Configure environment variables ({{.env}})

Copy the template and fill it in:

{code:language=powershell}
Copy-Item .env.example .env
{code}

{{.env}} is {{.gitignore}}d — never commit it. Populate the following (see {{.env.example}} inline comments for full detail on each):

||Variable||Required?||Notes||
|{{ADO_TOKEN}}|Yes|Azure DevOps PAT. Scopes: Work Items (Read), Build (Read), Test Management (Read).|
|{{ADO_ORGANIZATION}} / {{ADO_PROJECT}}|Yes|Defaults provided ({{sc-ado}} / {{FMQPR}}) — change only if your release lives elsewhere.|
|{{USER_EMAIL}}|Yes|Your SC email — used for Confluence basic auth.|
|{{CONFLUENCE_TOKEN}}|Yes|Confluence PAT.|
|{{SONAR_URL}} / {{SONAR_TOKEN}}|Yes|SonarQube token with read access to the relevant projects.|
|{{GENIE_REPORT_LINK}} / {{GENIE_TOKEN}}|Yes (unless every stream you use is Genie-disabled)|Genie regression reporting API.|
|{{HTTPS_PROXY}}|Usually yes|Corporate proxy for outbound calls to non-ADO/Confluence hosts. Leave blank on macOS if using the system proxy.|
|{{TDA_OUTPUT_DIR}}|No|Defaults to {{./AutoTDAReports}}.|
|{{PARALLEL_ENABLED}}|No|Defaults to {{true}}.|
|{{ADO_THROTTLE_DELAY_MS}}|No|Defaults to {{0}} (disabled). Raise to 200–500 only if you see ADO throttling/timeouts.|
|{{GENIE_TIMEOUT_SECONDS}}, {{HTTP_RETRY_ATTEMPTS}}, {{HTTP_RETRY_BACKOFF_SECONDS}}|No|Sensible defaults baked into the code; only needed if you see proxy/timeout warnings.|
|{{SN_INSTANCE}}, {{SNOW_API_PATH}}, {{CLIENT_ID}}, {{FERNET_KEY}}, {{SNOW_BLADE_KEY}}, {{CLIENT_SECRET}}|Only if SNOW is enabled|See section 4 below.|
|{{SCWIKI_URL}}, {{SCWIKI_WIKI_NAME}}, {{SCWIKI_API_KEY}}|No \u2014 not yet used by any collector|SC Wiki integration (future Confluence replacement). See section 6 below.|

{info:title=No Vault fallback}
All required secrets ({{ADO_TOKEN}}, {{CONFLUENCE_TOKEN}}, {{SONAR_TOKEN}}, {{GENIE_TOKEN}}, SNOW credentials) are read *directly from {{.env}}* — there is no HashiCorp Vault or other secret-manager fallback in {{AutoTDAScript.py}}. If a required key is missing, the script fails immediately with a {{KeyError}} naming the missing variable.
{info}

h2. 4. ServiceNow (SNOW) setup — only if you need it

SNOW is *enabled by default* ({{SNOW_ENABLED}} defaults to {{true}} when unset). If your stream doesn't use a CHG/ServiceNow process, either:

* Set {{SNOW_ENABLED=false}} in {{.env}} (global default), or
* Set {{streams.<STREAM>.snow_enabled: false}} in {{stream_config.yaml}} (per-stream override — see section 5).

When SNOW *is* enabled, you must populate {{CLIENT_ID}}, {{FERNET_KEY}}, {{SNOW_BLADE_KEY}}, and {{CLIENT_SECRET}} (encrypted). One-time generation from your {{secret.key}} / {{snow_blade.key}} files:

{code:language=powershell}
[Convert]::ToBase64String([IO.File]::ReadAllBytes('secret.key'))
[Convert]::ToBase64String([IO.File]::ReadAllBytes('snow_blade.key'))
{code}

Paste the two outputs into {{.env}} as {{FERNET_KEY}} and {{SNOW_BLADE_KEY}} respectively. {{CLIENT_SECRET}} is then decrypted automatically at script startup — do not set it manually.

h2. 5. Configure {{stream_config.yaml}}

{{stream_config.yaml}} (in the same {{scripts/}} folder) is the *single, mandatory source of truth* for all per-stream settings — PIT URL, build IDs, Sonar/Genie/regression behaviour. The script will fail fast ({{FileNotFoundError}}/{{ValueError}}) if this file is missing or your stream has no entry under its top-level {{streams:}} key.

# Confirm your stream already has a {{streams.<STREAM>}} block (all 14 supported streams — FXO, RATES, RULES, CREDIT, SCALE, KDB, SCM, OMS, XAP, BCF, PLATFORM, ION, MDA-PXE, S2BX — have one).
# *If your stream supports build auto-discovery* (the default), you usually don't need to touch {{builds:}} — the script discovers component build IDs automatically from the release build's {{promotedImageList}} artifact. Skip to section 7.
# *If your stream has {{sonar_config.auto_discovery: false}}*, or auto-discovery isn't applicable (e.g. RULES/Apollo), you must populate {{streams.<STREAM>.builds}} with {{pipeline_name: build_id}} (optionally {{build_id version}}, e.g. {{13028582 185.0.0}}) before running — find these under *Release Summary → Published Artifacts of Type Application* on your release pipeline build in ADO.
# *SCM, OMS, XAP, BCF, and PLATFORM currently ship with empty {{builds: {}}} placeholders* — populate the block for your stream before your first run against one of these streams, or the run will fail with a {{ValueError}} pointing you at the exact block to fill in.
# *S2BX is an Apollo-based stream (like RULES) and requires a manual {{builds:}} map* — populate {{streams.S2BX.builds}} with {{pipeline_name: build_id}} entries from the release pipeline's *Published Artifacts of Type Application* before running.

h2. 6. SC Wiki (SCWiki) integration — optional, not yet used by any collector

{{tda/integrations/scwiki.py}} is a standalone integration point for SC Wiki (the org's new internal documentation platform, an eventual — not immediate — replacement for Confluence). No collector calls into it yet; this section only applies if you're testing the module directly or building on top of it.

# *Create a personal API key* — log in to your SCWiki instance, open your profile (username/avatar in the top-right) → *Application* tab → *+ Create* → give it a label (e.g. {{migration-script}}) → *Create*. Copy the key immediately; it is shown only once.
# *Populate {{.env}}* — set {{SCWIKI_URL}} (base URL, no {{/rest}} suffix), {{SCWIKI_WIKI_NAME}} (usually {{xwiki}}), and {{SCWIKI_API_KEY}} (the key from step 1). See section 3's table.
# *Rotate keys with zero downtime* — create the new key first, update {{.env}}, verify, then delete the old key from the same Application tab.

h2. 7. Gather the IDs you need to run the script

# *Release Work Item ID* — open your Release WI in ADO; copy the numeric ID from the URL (e.g. {{13596392}}).
# *Build ID* — open the main release pipeline build → *Release Summary* tab → copy the {{buildId}} (e.g. {{12134096}}). Not required if you plan to run with {{--rwi-only}}.
# *Stream name* — one of {{FXO}}, {{RATES}}, {{RULES}}, {{CREDIT}}, {{SCALE}}, {{KDB}}, {{SCM}}, {{OMS}}, {{XAP}}, {{BCF}}, {{PLATFORM}}, {{ION}}, {{MDA-PXE}}, {{S2BX}}.
# *Release version* (optional but recommended) — e.g. {{455.0}}. Supplying this avoids fragile branch-name parsing for Sonar/PIT.

h2. 8. Run the script

{code:language=powershell}
python AutoTDAScript.py <release_id> <build_id> <stream> [release_version]
{code}

*Example:*
{code:language=powershell}
python AutoTDAScript.py 13596392 12134096 RULES 185.0.0
{code}

h3. Optional flags

||Flag||Effect||
|{{--use-yaml}}|Skip auto-discovery; read build IDs straight from {{stream_config.yaml}}.|
|{{--no-batch}}|Fetch linked work items one-by-one instead of via bulk {{workitemsbatch}}.|
|{{--no-parallel}}|Disable all threading (useful when debugging or on a flaky proxy).|
|{{--rwi-only}}|Collect only Release-WI-derived data (stories, bugs, test plan, traceability, SNOW, PIT, PT). Skips unit tests, Sonar, and Genie/regression. {{build_id}} is not required in this mode.|

The script prints progress through 6 numbered steps ({{[1/6]}} … {{[6/6]}}). On the first full run, you'll be asked to confirm the resolved builds:

{code}
==========================================================================
  PLEASE VERIFY ASSOCIATED BUILDS FOR STREAM: RULES
==========================================================================
  Source: auto-discovered

    Pipeline                                           Build ID       Version
    --------------------------------------------------- -------------- ------------
    51527-dtp-services_maven_pipeline                  13092413       185.0.0
    ...

Confirm builds are correct and continue? [y/N]:
{code}

Type {{y}} to proceed, or anything else to abort — the script will tell you which config file to check/update before re-running.

h2. 9. Output

* Full JSON: {{AutoTDAReports/AutoTDAResults_<STREAM>_<release_id>.json}}
* Compact summary: {{AutoTDAReports/AutoTDASummary_<STREAM>_<release_id>.json}}

Both are written under {{scripts/AutoTDAReports/}} (gitignored). Hand the summary (or full JSON) to the {{dtp-tda-report}} Copilot skill to generate the formatted HTML report and PASS/CONDITIONAL/BLOCKED verdict, e.g.:

{code}
/dtp-tda-report ./AutoTDAReports/AutoTDAResults_RULES_13596392.json
{code}

h2. 10. Troubleshooting first-run issues

||Symptom||Likely cause / fix||
|{{KeyError: 'ADO_TOKEN'}} (or similar) at startup|Required variable missing from {{.env}} — check section 3.|
|{{stream_config.yaml not found in project root or script directory}}|Run the script from the {{scripts/}} folder, or copy {{stream_config.yaml}} alongside it.|
|{{Stream '<X>' has no entry under 'streams' in stream_config.yaml}}|Add a {{streams.<X>}} block — see section 5.|
|{{401 Unauthorized}} from SC Wiki|{{SCWIKI_API_KEY}} missing/expired — create a fresh key from your SCWiki profile's Application tab (see section 6) and update {{.env}}.|
|{{'streams.<STREAM>.builds' in stream_config.yaml has no entries}}|Populate the {{builds:}} map for your stream (common for SCM/OMS/XAP/BCF/PLATFORM on first use).|
|{{Could not extract Build ID from Custom.LatestPipelineRuns}}|Supply the build ID explicitly as the second CLI argument instead of relying on auto-extraction.|
|Repeated {{ProxyError}}/502/timeout warnings from Genie or Sonar|Raise {{HTTP_RETRY_ATTEMPTS}} / {{HTTP_RETRY_BACKOFF_SECONDS}} in {{.env}}.|
|ADO calls intermittently time out or get throttled|Set {{ADO_THROTTLE_DELAY_MS=200}} (or higher) in {{.env}}, optionally combined with {{--no-parallel}}.|
|{{[SNOW] No change record data returned}}|Verify the CHG number on the Release WI, and your SNOW credentials/connectivity — this is a warning, not a fatal error.|
