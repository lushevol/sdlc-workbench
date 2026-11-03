---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Run coverage inside the internal network

> **Run the existing suite with `--mode live` on the internal machine. Reports are generated locally.**
> Action: install the core, check endpoint configuration, supply credentials, and run the commands below.
> Consequence: inaccessible endpoints and missing definitions remain unassessed.
> Owner: internal operator, identity unknown.
> Source: [user question](../evidence/internal-network-run-guide-20261103/user-input.md#exact-user-input).

These instructions cover EMS2 PROD versus CES UAT and EMS2 PROD versus EMS2 UAT.
This guide does not record enterprise execution. The retained sample uses supplied responses.

## 1. Transfer and install

Use a complete copy of this Workbench source checkout on the internal machine.
Preserve the task folder, including `coverage/`, `api/`, `ces migration/`, and the launchers.
The installed Python wheel does not contain those task inputs.
The EMS2 environment comparison reads stored API request keys during account discovery, including live runs.

Install approved Python 3.10 or later, with compatible dependency wheels available for that interpreter.
Select the same interpreter when preparing dependencies and installing them.
Node.js and a report server are unnecessary for these coverage commands.
Create the Python environment on the target computer. Do not copy `.venv` between computers.

If the internal machine can reach an approved Python package index, run core setup from the Workbench root:

| System | Install | Check installation |
| --- | --- | --- |
| Windows PowerShell | `.\setup.cmd --core-only` | `.\setup.cmd --check --core-only` |
| macOS | `./setup.command --core-only` | `./setup.command --check --core-only` |

If package registries are unavailable, prepare a core bundle on a connected staging computer:

| System | Prepare on staging computer | Install on internal computer |
| --- | --- | --- |
| Windows PowerShell | `py -3 core\offline.py prepare --output offline-bundle --core-only` | `.\setup.cmd --core-only --offline-bundle .\offline-bundle` |
| macOS | `python3 core/offline.py prepare --output offline-bundle --core-only` | `./setup.command --core-only --offline-bundle ./offline-bundle` |

The staging and target computers must match operating system, CPU architecture, Python minor version, interpreter implementation, and ABI.
Transfer the unchanged source checkout and `offline-bundle/` together through the approved company process.
Do not transfer `.env`, `.venv`, `node_modules`, or private package-manager settings.
See the [offline setup contract](../../../docs/SETUP.md#install-without-package-registry-access) for target checks and bundle validation.

## 2. Check endpoint configuration

Check the endpoint addresses and entity identifiers against the internal environment.
Keep FMO Portal Admin excluded from production denominators.

| File | Fields to check |
| --- | --- |
| [config.json](config.json) | `ems2.base_url`, `ces.base_url`, request paths, EMS2 entity IDs, CES application routing, matrix paths. |
| [ems2-config.json](ems2-config.json) | `prod.base_url`, `uat.base_url`, request paths, each entity's `prod_id` and `uat_id`. |
| [suite.json](suite.json) | Both child configurations and the output location. |

The current configurations target EMS2 PROD, EMS2 UAT, and CES UAT.
Environment-specific numeric identifiers locate requests. Names define comparison identity.
The default request timeout is 15 seconds, with one retry and four account workers.
Adjust these configuration values to the internal service limits when required.

The internal host needs DNS and HTTPS access to all configured endpoints.
Allow GET for CES and inventory requests. Allow JSON POST for the EMS2 `entitlementList` read operation.

## 3. Create private configuration

Create `.env` at the Workbench root, beside `setup.cmd` and `setup.command`.
Use valid API credentials supplied through your internal access process.

```dotenv
CES_COVERAGE_BEARER_TOKEN=replace-with-CES-UAT-token
CES_COVERAGE_EMS2_TOKEN=replace-with-EMS2-PROD-token-if-required
EMS2_COVERAGE_PROD_TOKEN=replace-with-EMS2-PROD-token-if-required
EMS2_COVERAGE_UAT_TOKEN=replace-with-EMS2-UAT-token-if-required
CES_COVERAGE_CA_FILE=C:/Company/Certificates/enterprise-ca.pem
```

On macOS, use the corresponding local certificate path.
Omit `CES_COVERAGE_CA_FILE` when Python already trusts every endpoint certificate chain.
A relative CA path resolves from the Workbench root. TLS certificate verification remains enabled.
The shared CA bundle must trust all three endpoints when supplied.

Both PROD token variables can contain the same token when they access the same service.
EMS2 tokens can remain unset only when those endpoints permit requests without an authorization header.
CES requires its configured token. Raw tokens receive the `Bearer` prefix automatically.
Explicit `Bearer ...` and `Basic ...` authorization values are also supported.
An existing browser login does not supply credentials to this runner.
Browser SSO cookies, Kerberos, NTLM, client certificate configuration, and redirects are not supported by this client.

If your network requires a proxy, configure `HTTPS_PROXY` and the appropriate `NO_PROXY` host list.
`HTTP_PROXY` and lowercase forms are also supported.
Process environment variables override `.env`, including explicit empty values.
Keep credential values outside JSON configurations and source control.

## 4. Run both comparisons

Run commands from the Workbench root.
Start with a bounded live run to check account collection and report generation.
The bound limits scheduled accounts per comparison. Catalog and inventory requests still run.
Its account selection follows each comparator's discovery order; the two samples can contain different accounts.

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m ai_sdlc_workbench.coverage_suite --config tasks/draft-ces-migration/coverage/suite.json --mode live --user-limit 2 --open
```

macOS or Linux, using an installed environment:

```sh
.venv/bin/python -m ai_sdlc_workbench.coverage_suite --config tasks/draft-ces-migration/coverage/suite.json --mode live --user-limit 2 --open
```

Check each report's evidence source. It must say `LIVE: collected API responses`.
Check source errors and account outcomes. A bounded run can report `INCOMPLETE` because accounts remain unscheduled.
Then remove `--user-limit 2` to compare the complete discovered population:

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m ai_sdlc_workbench.coverage_suite --config tasks/draft-ces-migration/coverage/suite.json --mode live --open
```

macOS or Linux:

```sh
.venv/bin/python -m ai_sdlc_workbench.coverage_suite --config tasks/draft-ces-migration/coverage/suite.json --mode live --open
```

Alternatively, pass `--mode live` to the existing launcher from a terminal:

| System | Run all live comparisons |
| --- | --- |
| Windows PowerShell | `.\tasks\draft-ces-migration\run-all-coverage.cmd --mode live` |
| macOS | `./tasks/draft-ces-migration/run-all-coverage.command --mode live` |

Double-clicking these launchers without arguments still runs supplied-response replay.
On a server without a desktop, use the Python command and omit `--open`.
Keep API calls on the internal host. Open the generated files on an internal desktop when needed.

## 5. Read and retain the reports

Each run creates a timestamped directory under `tasks/draft-ces-migration/evidence/coverage-runs/`.
The terminal prints the actual Markdown and HTML paths.

| Output | Content |
| --- | --- |
| `index.html` and `index.md` | Both complete comparisons, with separate populations and denominators. |
| Child `report.html` and `report.md` | Detailed entitlements, assignments, permissions, role grants, matches, and unassessed accounts. |
| Child `differences.csv` | Exact missing, additional, inconsistent, and unassessed items. |
| `result.json`, `binding.json`, `cases.jsonl`, and `responses/` | Metrics, source identities, durable account checkpoints, and retained response evidence. |

HTML reports contain their styles and scripts. They need no public CDN or web server.
Retain the complete run directory when moving or sharing the report internally, so relative evidence links continue to work.

| Exit code | Meaning |
| --- | --- |
| `0` | Functional comparisons match within the declared scope. |
| `1` | Completed comparisons contain differences. |
| `2` | At least one comparison is incomplete, or setup failed. |

Network, TLS, or authorization failures can stop further account scheduling. The remaining accounts stay unassessed.
Review `MISSING_CREDENTIAL`, HTTP 401/403, `TLS_ERROR`, `TLS_CONFIGURATION`, or `NETWORK_ERROR` before another run.
Check [individual-run recovery](README.md#recover-an-individual-run) when continuing a retained child run.

## Evidence limits

Live mode replaces supplied response bodies with current API collection. It does not add missing endpoint contracts.
Discovery uses matrices, CES memberships where applicable, configured users, and stored EMS2 request keys.
It cannot prove a complete enterprise account directory.
The EMS2 comparison supports an explicit `users` array in [ems2-config.json](ems2-config.json) for additional known accounts.
Complete role definitions, empty assigned roles, and full data-policy equality still require authoritative comparable sources.
The runner does not add pagination beyond the supplied contracts.
Captured requests do not establish an atomic snapshot across environments.
Read inventory presence, definition retention, user equality, and acquisition completeness as separate measurements.

## Verification

The [guide validation](../evidence/internal-network-run-guide-20261103/validation.json) records source inspection and local command checks.
Those checks do not establish internal installation, endpoint connectivity, or live comparison success.
Windows commands were inspected but not executed on a Windows host.
The [reporting validation](../evidence/detailed-coverage-report-20261103/validation.json) retains the earlier tooling test and sample evidence.
