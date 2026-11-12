# Portal knowledge ingestion answers

Source: Codex user message, 12 November 2026, Asia/Singapore.
Priority: Latest user clarification for the nine entries in the portal knowledge questionnaire.

## Exact user input

> 1. RATAN team own and review policy, but the policy follow ICS bank security policy 2. ICS bank security policy defined idle session timeout no greater than 15mins, absolute session timeout no greater than 60 mins. 3. OneMFA is decommission now, not allow fallback. 4. for UI it take effect on next login, for api call it take effect when redis expire (in auth server, 1 hour for entitlement cache, 2 hours for jwt token parsing) 5. Ideally logout should revoke all sessions; It not include identity provider like Entra, revocation should take effect immediately. 6. For UI tile validation, it happens on login, refresh page and extend the session when idle. 7. Portal admin can read all tenant audit history and configs; a tile can never refer to metadata from another tile. 8. NFR is 5s for API loading, no restrict metrics for UI. 9. Analytics mainly used to collect user activities, CPO will use the data to review usage of business products. Data will save on PROD for 3 months.
