# BFF entity field request and compatibility question

- Source: User message in the current Codex chat.
- Date: 2026-11-06 (Asia/Singapore).
- Priority: High-priority requirement for the scoped BFF change.

## Exact user input

> use minor code change to let single-ui-bff api returns EMS3 entities with new field roleList which contains entitlement_name from CES api [EMS3-user entitlements by app and user (1481696).yml](<tasks/ces-entitlement-migration-20261102/api/EMS3-user entitlements by app and user (1481696).yml>) use itam_id (in this case 51358) to new field applicationId.
> One more question, for the principle that we need to try best not to break previous contract, what still break ?

## Authorized scope

Add `roleList` and `applicationId` to EMS3 BFF entities with minimal source changes.
Inspect the supplied CES contract and preserve existing EMS2 behavior.
Assess remaining compatibility limits separately from the additive BFF fields.
Application deployment and frontend implementation remain outside this request.
