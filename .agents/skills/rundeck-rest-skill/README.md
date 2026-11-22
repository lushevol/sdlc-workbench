# Rundeck REST skill for AI SDLC Workbench

A tokenless Rundeck 5.10 connector with human-governed skill. **No official Rundeck CLI, no MCP, no external Python libraries, no database, no server-side installation.** Works locally on macOS and Windows 11 with Python 3.9+.

## Install into an existing workspace

The archive already contains ready-to-copy mirrored skills under `.claude/skills/rundeck/` and `.github/skills/rundeck/`, plus the canonical `skills/rundeck/`. Copy your selected skill directory and `packages/connectors/rundeck/` into your workbench without overwriting existing root configuration files. Keep a project root `.env` next to `packages/`; merge the supplied `.gitignore` entries and `AGENTS-rundeck-snippet.md` into your existing files. Verify your particular agent version discovers the target skills directory.

```text
workbench/
├── .env                          # NON-SECRET config, gitignored
├── skills/rundeck/SKILL.md
└── packages/connectors/rundeck/
    ├── rdk.py                    # only supported entry point
    ├── client.py                 # cookie-session REST transport
    ├── policy.py                 # immutable-by-agent local policy
    ├── policy.json               # default read-only
    ├── sanitize.py               # output redaction, best effort
    └── tests/                    # offline unit tests
```

## Setup

1. Copy `.env.example` to `.env` in the workbench root and fill out only URL, user, version, timeout. Use real trusted HTTPS; set up internal CA certificates in your OS/Python trust configuration if needed.
2. `python packages/connectors/rundeck/rdk.py projects --limit 30` (or `python3 ...` on macOS). Type your password at the **local prompt**, not in chat.
3. If a coding agent cannot acquire interactive credentials, configure your **approved** enterprise secrets broker to inject `RUNDECK_PASSWORD` directly into the connector's process. Do not place it in files or agent tool arguments.
4. `python -m unittest discover -s packages/connectors/rundeck/tests -v` to run offline tests. No external network is contacted by tests.

If you want a list of projects read only, use `python packages/connectors/rundeck/rdk.py projects --limit 30`.

Examples:

```bash
python packages/connectors/rundeck/rdk.py health
python packages/connectors/rundeck/rdk.py jobs list --project Operations
python packages/connectors/rundeck/rdk.py jobs show --id 11111111-1111-4111-8111-111111111111
python packages/connectors/rundeck/rdk.py executions list --project Operations --status failed --recent 7d
python packages/connectors/rundeck/rdk.py executions logs --id 12345 --lines 100
```

### Enable one approved job (optional)

A repository owner may update `packages/connectors/rundeck/policy.json` after organizational approval:

```json
{
  "allowed_projects": ["DevOps-DEV"],
  "enable_job_definition_read": false,
  "enable_job_execution": true,
  "executable_jobs": {
    "11111111-1111-4111-8111-111111111111": {
      "project": "DevOps-DEV",
      "allowed_options": ["target"]
    }
  },
  "max_list_items": 100,
  "max_log_lines": 200,
  "max_response_bytes": 1048576
}
```

After inspecting the job and gaining explicit approval, run on a local terminal:

```bash
python packages/connectors/rundeck/rdk.py jobs run --id 11111111-1111-4111-8111-111111111111 --option target=dev1
```

An exact `RUN <uuid>` terminal confirmation is mandatory; this is **not unattended execution**. Secret values must never be passed as command arguments. Keep prod operations behind your enterprise change-control processes.

## Common failure modes

- **401/403**: Wrong credentials, expired cookie, insufficient ACL, or cookie API use disabled. Ask the Rundeck admin about `rundeck.security.apiCookieAccess.enabled`.
- **HTML instead of JSON**: Login redirect or reverse-proxy authentication issue; no workaround/bypass.
- **No cookie**: Authentication failed or reverse proxy does not pass `Set-Cookie`.
- **TLS errors**: Install the corporate CA into an approved trust store. Never use `verify=False` or unverified SSL contexts.
- **Session invalidation**: Other concurrent login sessions may cause conflicts if maxSessions is enforced; use your admin to confirm configuration.
- **Logs too large**: Reduce `--lines`; the response body is capped.

## Design limitations

- This skill can **only** use a session established with approved username/password auth; it cannot bypass disabled cookie-based API access.
- Each invocation performs its own login. The session is in memory and is not persisted for reuse between commands. This is intentionally safer but less convenient than a managed persistent credential/session broker.
- Regex redaction cannot guarantee removal of customer data, secrets, or sensitive production information. Review data classification and AI ingress policies.
- No live Rundeck 5.10 server was available during packaging; offline unit tests are not an end-to-end compatibility guarantee.

## Sources

- https://docs.rundeck.com/docs/api/#password-authentication
- https://docs.rundeck.com/docs/upgrading/upgrading-to-4.8.html
- https://docs.rundeck.com/docs/administration/configuration/config-file-reference.html
- https://docs.rundeck.com/docs/api/rundeck-api-versions.html
