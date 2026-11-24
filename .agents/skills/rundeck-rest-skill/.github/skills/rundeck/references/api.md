# Rundeck 5.10 REST reference

Official API: https://docs.rundeck.com/docs/api/
Authentication: https://docs.rundeck.com/docs/api/#password-authentication
Cookie rotation (Rundeck 4.8+): https://docs.rundeck.com/docs/upgrading/upgrading-to-4.8.html
Cookie API gate: https://docs.rundeck.com/docs/administration/configuration/config-file-reference.html
Version history: https://docs.rundeck.com/docs/api/rundeck-api-versions.html

## Authentication

- POST `<base>/j_security_check`, form-urlencoded `j_username`, `j_password`.
- Redirect to `/user/login` or `/user/error` means authentication failed.
- Follow same-origin redirects and maintain `JSESSIONID` across them (4.8+ rotation).
- Retain session cookies in memory, not on disk. Confirm cookie-based API access is enabled.

## Read-only routes (API v46)

| Operation | Endpoint |
|---|---|
| system info | GET `/api/46/system/info` |
| projects | GET `/api/46/projects` |
| jobs | GET `/api/46/project/{project}/jobs` |
| job info | GET `/api/46/job/{uuid}/info` |
| job definition | GET `/api/46/job/{uuid}?format=json` (opt-in) |
| execution query | GET `/api/46/project/{project}/executions?statusFilter=failed&recentFilter=7d&max=20` |
| execution details | GET `/api/46/execution/{id}` |
| execution log | GET `/api/46/execution/{id}/output?lastlines=100` |

## Mutating route (disabled by default)

- POST `/api/46/job/{uuid}/run`, JSON `{"options":{"name":"value"}}`. Requires server ACL `run`, local job allowlist and in-person confirmation. Do not send secure option values via CLI flags.

## Compatibility notes

- Rundeck 5.10.0 is newer than API v46; v46 is a deliberate baseline, not a claim that v46 is the server's maximum API version.
- API `system/info` may require server authorization. Do not assume failure means Rundeck is unavailable.
- Endpoint results differ by server configuration, license, ACL and job type.
- Routines are implemented and unit-tested locally but cannot be tested live against the user's private Rundeck without access.
