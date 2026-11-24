# dtp-tda-report

A two-part tool for automating TDA (Technology Delivery Assurance) checkpoint reporting for Blade releases at Standard Chartered Bank (FMDC).

**Part 1 — `AutoTDAScript.py`**: Collects all TDA data from ADO, Confluence, ServiceNow, Sonar, and Genie and writes it to a structured JSON file.

**Part 2 — `dtp-tda-report` Copilot skill**: Reads that JSON and produces a fully formatted, colour-coded HTML report with findings, gate checks, and a PASS / CONDITIONAL / BLOCKED verdict.

---

## Supported Streams

| Stream | Description |
|--------|-------------|
| FXO | Blade FX Options |
| RATES | Blade Rates |
| RULES | Apollo Rules Engine |
| SCM | SC Markets |
| OMS | Order Management System |
| XAP | Cross-Asset Platform |
| CREDIT | Blade Credit |
| BCF | Business Continuity Framework |
| PLATFORM | Blade Platform |

---

## Prerequisites

### Python dependencies

```powershell
pip install requests pandas atlassian-python-api sonarqube-client python-docx fuzzywuzzy tabulate beautifulsoup4 lxml cryptography pyyaml
```

### Environment variables

Copy `.env.example` (at the repo root) to `.env` and fill in your values:

```powershell
Copy-Item .env.example .env
```

Open `.env` and populate:

| Variable | Description |
|---|---|
| `HC_ROLE_ID` | HashiCorp Vault AppRole Role ID |
| `HC_SECRET_ID` | HashiCorp Vault AppRole Secret ID |
| `ADO_TOKEN` | Azure DevOps Personal Access Token (scopes: Work Items Read, Build Read, Test Management Read) |
| `USER_EMAIL` | Your SC email address (used for Confluence auth) |
| `FERNET_KEY` | Base64-encoded contents of `secret.key` |
| `SNOW_BLADE_KEY` | Base64-encoded Fernet token of `snow_blade.key` |

**One-time setup for SNOW keys** (run once in PowerShell, then paste output into `.env`):
```powershell
$env:FERNET_KEY     = [Convert]::ToBase64String([IO.File]::ReadAllBytes('secret.key'))
$env:SNOW_BLADE_KEY = [Convert]::ToBase64String([IO.File]::ReadAllBytes('snow_blade.key'))
```

> **Note:** `CONFLUENCE_TOKEN`, `SONAR_TOKEN`, `CLIENT_ID`, `CLIENT_SECRET`, and `GENIE_TOKEN` are fetched automatically from HashiCorp Vault at startup — you do not need to set these manually.

---

## Step-by-Step Usage

### Step 1 — Get your IDs from ADO

You need three values before running the script:

1. **Release Work Item ID** — open your Release WI in ADO, copy the numeric ID from the URL or title bar (e.g. `13596392`)
2. **Build ID** — open the main release pipeline build in ADO → go to the **Release Summary** tab → copy the `buildId` from the URL (e.g. `12134096`)
3. **Stream name** — one of the values in the Supported Streams table above (e.g. `RULES`)

### Step 2 — Update `associated_builds.yaml`

Open `plugins/test/dtp-tda-report/scripts/associated_builds.yaml` and update the section for your stream with the pipeline names and their build IDs for this release.

Find build IDs from the **Release Summary** tab → **Published Artifacts of Type Application** section in ADO.

```yaml
RULES:
  51527-fmdc-releases: 12134096
  51527-dtp-services_maven_pipeline: 12112449
  50665-dtp-client_maven_pipeline: 11949862
  50665-dtp-client_npm_pipeline: 11948104
```

Only the section matching your stream argument will be read — other sections are ignored.

### Step 3 — Run AutoTDAScript.py

Navigate to the scripts directory and run the script with your three arguments:

```powershell
cd plugins/test/dtp-tda-report/scripts

python AutoTDAScript.py <release_id> <build_id> <stream>
```

**Example:**
```powershell
python AutoTDAScript.py 13596392 12134096 RULES
```

The script will print progress as it runs:

```
[env] Loaded environment from ...\.env
[1/6] Loading associated builds from associated_builds.yaml...
      Loaded 4 build(s): [51527-fmdc-releases, ...]
[2/6] Starting full TDA data collection for release 13596392 (RULES)...
  [3/6] Fetching release WI, SNOW, PT checks, unit tests, Genie regression, Sonar...
        Fetching Genie regression results...
        Genie done. Passed=8 Failed=0
        Fetching Sonar coverage for 4 RULES pipeline(s)...
  [4/6] Processing linked work items...
  [5/6] Building traceability...
  [6/6] Writing JSON output...
TDA data written to: ./AutoTDAReports/AutoTDAResults_RULES_13596392.json
```

The JSON output file is written to `scripts/AutoTDAReports/` (gitignored — not committed).

### Step 4 — Generate the TDA report using the Copilot skill

In VS Code Copilot Chat (Agent mode), run:

```
/dtp-tda-report ./AutoTDAReports/AutoTDAResults_RULES_13596392.json
```

Or use the full path if running from a different working directory:

```
/dtp-tda-report plugins/test/dtp-tda-report/scripts/AutoTDAReports/AutoTDAResults_RULES_13596392.json
```

The skill will analyse the JSON and produce:
- A detailed HTML report saved to `~/Downloads/TDAReport_<STREAM>_<release_id>.html`
- A summary of all critical, moderate, and minor findings directly in chat
- A final verdict: **PASS**, **CONDITIONAL**, or **BLOCKED**

---

## Output

### JSON (intermediate)
`scripts/AutoTDAReports/AutoTDAResults_<STREAM>_<release_id>.json`

Contains all raw TDA data collected: release checks, SNOW, PT, PIT, unit tests, Sonar coverage, Genie results, traceability, and test results.

### HTML Report
`~/Downloads/TDAReport_<STREAM>_<release_id>.html`

A fully formatted, colour-coded report suitable for sharing with the release team. Open in any browser.

---

## Data Sources

| Source | What is collected |
|--------|-------------------|
| **Azure DevOps** | Release WI, stories, bugs, test plans, test cases, test results, build metadata |
| **ServiceNow** | CHG state, risk, priority, type |
| **Confluence** | PT plan/report/PTIA approval status, PIT page accessibility and content |
| **SonarQube** | Overall and new code coverage metrics per pipeline |
| **Genie** | Regression scenario pass/fail counts and story tag traceability |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `KeyError: 'HC_ROLE_ID'` | `.env` file not found or variable missing — check path and contents |
| `associated_builds.yaml not found` | Run script from `scripts/` directory, or ensure the file exists |
| `No entries found for stream 'X'` | Add a `X:` section to `associated_builds.yaml` with pipeline: build_id entries |
| Sonar coverage is empty `[]` | Check that the build IDs in `associated_builds.yaml` are correct for this release |
| `Fetching Sonar coverage for 0 pipelines` | `associated_builds.yaml` section for your stream has no entries |
| Genie returns 0 results | Confirm the release name matches exactly what is registered in the Genie portal |
| HTML report opens blank | Open from `~/Downloads/` directly in a browser — do not preview inside VS Code |
