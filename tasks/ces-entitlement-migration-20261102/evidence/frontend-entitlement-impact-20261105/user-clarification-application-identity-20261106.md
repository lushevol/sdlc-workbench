# CES application identity clarification

- Source: User message in the current Codex chat.
- Date: 2026-11-06 (Asia/Singapore).
- Priority: High-priority requirement for the BFF and frontend compatibility assessment.

## Exact user input

> No, applicationName is name of team, should be RATAN in this case, but there has no RATAN in CES but its id 51358. X_RATANONE equal to RATAN_ENTITLEMENT_RULE in CES, which is present in name field from login.

## Confirmed correspondence

| Contract meaning | EMS2 / legacy value | CES value |
| --- | --- | --- |
| Entity or application name used by the CES authorization scope | `X_RATANONE` | `RATAN_ENTITLEMENT_RULE` |
| Team or display application name | `RATAN` | Must remain `RATAN` in the normalized BFF entity |
| Application identity | Legacy numeric identity, when present | `user_data.itam_id = "51358"` |

`user_data.app_name` is `RATAN_ENTITLEMENT_RULE`. It is the CES authorization name.
It must not replace the legacy team value in `applicationName`.
The BFF must keep `applicationName` and `applicationId` as separate fields.

## Implementation consequence

The CES mapper must receive an authoritative legacy team label or an explicit reviewed application mapping.
It must not derive `RATAN` from the CES name by string manipulation.
The normalized CES entity is therefore expected to contain `name: RATAN_ENTITLEMENT_RULE`, `applicationName: RATAN`, and `applicationId: "51358"` when the mapping is available.
