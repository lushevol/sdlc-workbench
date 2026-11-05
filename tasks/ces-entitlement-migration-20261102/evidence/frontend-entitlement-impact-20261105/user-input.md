# Frontend entitlement impact: user input

- Source: User message in the current Codex chat.
- Date: 2026-11-05 (Asia/Singapore).
- Priority: High-priority reference for this analysis.
- Scope: Identify frontend changes. This request does not authorize application fixes or deployment.

## Exact user input

> [application_tile_1105.csv](<tasks/ces-entitlement-migration-20261102/ces migration/application_tile_1105.csv>) is dump from db,  [login-response.json](<tasks/ces-entitlement-migration-20261102/ces migration/login-response.json>) is captured from real login api for user 1481696, now base on changes in single-ui-bff for migrating EMS2 to CES (compare to main), identify changes required for mfe-base and mfe-ratan-container to support new entitlement system. What I can see is that there is a hardcode X_RATANONE identification in code.
