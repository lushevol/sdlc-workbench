# CES migration coverage input

- Source: User message in the Codex chat.
- Date: 3 November 2026, Asia/Singapore.
- Priority: High-priority reference for this coverage investigation.

## Exact user input

```text
I updated [api](tasks/draft-ces-migration/api/) to latest open format including requests and response, and 4 entities matrix. Right now, the CS team is pulling our production entities from EMS2 and syncing them over to CES. We're currently looking at the CES UAT environment, where the endpoints correspond to the production EMS2 API calls and the CES UAT API calls.\
\
In theory, this data should match up completely, meaning there shouldn't be any data loss during the migration from EMS2 to CES. I need to figure out what the coverage rate is. This breaks down into two parts:\
\
1\. Entitlement coverage: For the four entities migrating from EMS2 to CES, are there any missing subjects?\
2\. User profile coverage: Do all user's permission profile in the EMS2 production environment have identical content in CES?\
\
You can pull the users and their profiles under these entities from the four Excel files. Take a look at this, and let's discuss your understanding of it.
```
