# dtp-tda-service

Hosted REST service for TDA (Technology Delivery Assurance) data collection.

This plugin is the **service companion** to `dtp-tda-report`.  It exposes
Part 1 of the TDA workflow (data collection via `AutoTDAScript.py`) as a
central REST API so that teams across the division can trigger TDA runs
without any local setup.  The `dtp-tda-report` Copilot skill (Part 2)
remains in the marketplace and is consumed locally as before — it reads the
same `AutoTDASummary JSON` whether it came from this service or the local script.

---

## Architecture

```
Caller (any team)
  POST /tda/run  { release_id, build_id, stream, ... }
       ↓  202 Accepted + job_id
  GET  /tda/jobs/{job_id}          ← poll (5-7 min)
       ↓  status: complete
  GET  /tda/jobs/{job_id}/result   ← download AutoTDASummary JSON
       ↓
  dtp-tda-report Copilot skill     ← unchanged, local, same JSON input
```

**Nothing changes for the skill consumer.**  The only difference is where
the JSON comes from: this service instead of a local script run.

---

## What This Service Replaces

| Previously (dtp-tda-report local) | Now (dtp-tda-service) |
|---|---|
| Clone the repo | No setup — just POST |
| Configure `.env` | Hosting team manages Vault |
| Maintain `associated_builds.yaml` | Pass `build_overrides` in request (optional) |
| Run `AutoTDAScript.py` locally | POST `/tda/run` |
| Wait 5-7 min at terminal | Poll `/tda/jobs/{id}` |
| Hand JSON to skill | Download from `/tda/jobs/{id}/result`, hand to skill |

---

## Request Body

```json
{
  "release_id": "12347453",
  "build_id": "9086679",
  "stream": "RATES",
  "release_version": "455.0",
  "build_overrides": {
    "blade-rates-api": "9086679",
    "blade-rates-ui": "9086700"
  },
  "flags": {
    "rwi_only": false,
    "no_batch": false,
    "no_parallel": false,
    "auto_confirm_builds": true,
    "use_yaml": false
  }
}
```

`build_overrides` is optional — when omitted, builds are auto-discovered from
the ADO pipeline artifact (same as the local script).  `build_id` is not
required when `flags.rwi_only` is `true`.

---

## Supported Streams

`FXO` · `RATES` · `RULES` · `SCM` · `OMS` · `XAP` · `CREDIT` · `BCF` · `PLATFORM` · `ION`

---

## Deployment (hosting team)

### 1. Install dependencies

```powershell
pip install -r plugins/test/dtp-tda-service/requirements.txt
```

### 2. Make the `tda` package importable

The `tda/` package lives in `dtp-tda-report`.  Either:

**Option A** — set `TDA_PKG_PATH` (recommended for same-repo deployments):
```
TDA_PKG_PATH=plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts
```

**Option B** — install it as an editable package:
```powershell
pip install -e plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts
```

### 3. Configure environment variables

| Variable | Description |
|---|---|
| `VAULT_ADDR` | HashiCorp Vault URL |
| `VAULT_ROLE_ID` | AppRole role_id |
| `VAULT_SECRET_ID` | AppRole secret_id |
| `VAULT_MOUNT_POINT` | KV v2 mount point (default: `secret`) |
| `VAULT_PATH_GLOBAL` | Path for ADO/Sonar/Genie/Confluence credentials (default: `tda-service/global`) |
| `VAULT_PATH_SNOW` | Path for SNOW credentials (default: `tda-service/snow`) |
| `ADO_ORGANIZATION` | ADO organisation name (e.g. `sc-ado`) |
| `ADO_PROJECT` | ADO project name (e.g. `FMQPR`) |
| `CONFLUENCE_URL` | Confluence base URL |
| `CONFLUENCE_SPACE_KEY` | Confluence space key (e.g. `DTP`) |
| `SN_INSTANCE` | ServiceNow instance hostname (e.g. `scbnow01.service-now.com`) |
| `SNOW_API_PATH` | ServiceNow REST API path |
| `SNOW_ENABLED` | `true` or `false` |
| `SONAR_URL` | SonarQube base URL |
| `GENIE_REPORT_LINK` | Genie API base URL |
| `HTTPS_PROXY` | Corporate proxy (e.g. `http://10.239.9.188:443`) |
| `PARALLEL_ENABLED` | `true` or `false` (default: `true`) |
| `ADO_THROTTLE_DELAY_MS` | Min delay (ms) between outbound ADO calls, shared across all concurrent job threads (default: `0`, disabled) |
| `TDA_OUTPUT_DIR` | Where JSON files are written (default: `/tmp/tda-output`) |
| `SERVICE_BASE_URL` | Canonical public URL of this service (used in response URLs) |
| `WORKER_POOL_SIZE` | Concurrent job threads (default: `4`) |
| `STREAM_CONFIG_PATH` | Path to `stream_config.yaml` (default: `service/stream_config.yaml`) |

### 4. Populate Vault secrets

```
secret/data/tda-service/global:
  ADO_TOKEN, SONAR_TOKEN, GENIE_TOKEN, CONFLUENCE_TOKEN, CONFLUENCE_USER

secret/data/tda-service/snow:
  CLIENT_ID, FERNET_KEY, SNOW_BLADE_KEY
```

### 5. Configure `stream_config.yaml`

Edit `service/stream_config.yaml` to set the PIT URL template for each
stream.  Sonar key overrides go here too (replaces `associated_builds.yaml`).
Two additional opt-in per-stream flags are supported, matching `dtp-tda-report`'s
stream_config.yaml conventions:

| Field | Default | Description |
|---|---|---|
| `story_comments_enabled` | `false` | Fetch each story WI's last comment (one extra ADO call per story). |
| `ado_regression_skip` | `false` | Temporarily bypass the ADO-native regression fetch for this stream. |

### 6. Start the service

```powershell
uvicorn service.main:app --host 0.0.0.0 --port 8080
```

---

## API Reference

Interactive docs available at `http://<host>:8080/docs` (Swagger UI) and
`http://<host>:8080/redoc` when the service is running.

| Method | Path | Description |
|---|---|---|
| `POST` | `/tda/run` | Submit a collection job (returns 202 + job_id) |
| `GET` | `/tda/jobs/{id}` | Poll job status |
| `GET` | `/tda/jobs/{id}/result` | Download `AutoTDASummary_*.json` |
| `GET` | `/tda/jobs/{id}/logs` | Get accumulated log lines |
| `GET` | `/health` | Liveness + readiness check |

---

## File Structure

```
service/
├── main.py            FastAPI app (routes, lifespan)
├── models.py          Pydantic request / response models
├── job_store.py       In-memory job state (swap for Redis in production)
├── job_runner.py      Thread pool executor
├── vault_client.py    HashiCorp Vault credential loader
├── stream_config.py   Per-stream server-side config loader
├── stream_config.yaml Stream config (PIT URLs, Sonar overrides)
├── server_config.py   Builds tda.config.Config from Vault credentials
└── runner.py          Headless orchestration (adapted from AutoTDAScript.py)
```

---

## Relationship to dtp-tda-report

`dtp-tda-service` does **not** replace `dtp-tda-report`.  The existing plugin
remains unchanged and continues to work for teams that prefer the local workflow.
Both tools produce the same `AutoTDASummary JSON` consumed by the same `SKILL.md`.
