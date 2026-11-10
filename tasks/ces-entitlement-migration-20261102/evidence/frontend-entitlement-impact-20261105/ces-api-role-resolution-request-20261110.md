# CES API role-resolution request

**Subject:** CES API request: identify the EMS2-compatible role after migration

Hi CES team,

During the EMS2-to-CES migration, one EMS2 entity represented one role. After migration, the same entity can contain several CES roles with equal priority. Because there is no priority or identifying marker, we cannot determine which CES role corresponds to the role that existed in EMS2.

For example, the CES response for user `1481696`, application `RATAN_ENTITLEMENT_RULE` (`itam_id: 51358`), returns multiple entitlement names under the same application. The consuming applications need to find the role that matches a particular function and scope.

Please support one of these two simple schema options. Existing fields such as `entitlement_name` should remain available.

## Option 1: identify one primary role

Add one field under the application entitlement data:

```json
{
  "entitlement_name": [
    "NON_FMO_RO",
    "RATAN_ENTITLEMENT_COMMON",
    "Global"
  ],
  "primary_role": "NON_FMO_RO"
}
```

`primary_role` must be exactly one value from `entitlement_name`. It should be the CES role that represents the role previously returned by EMS2 for this application/entity.

## Option 2: tag each role for lookup

Add function and scope tags for each role:

```json
{
  "entitlement_name": [
    "NON_FMO_RO",
    "RATAN_ENTITLEMENT_COMMON",
    "Global"
  ],
  "role_tags": [
    {
      "role_name": "NON_FMO_RO",
      "function": "business_role",
      "scope": "X_RATANONE"
    },
    {
      "role_name": "Global",
      "function": "data_access",
      "scope": "X_RATANONE"
    }
  ]
}
```

The consumer can then search for the role matching a specific `function` and `scope`. A function/scope combination must identify at most one role. If it identifies none or more than one role, the response should make that explicit rather than relying on response order.

Please confirm which option CES can support. The required behavior is:

1. Keep the current entitlement names and permission grants.
2. Make the EMS2-compatible role identifiable for each application/entity.
3. Keep business roles separate from data-access roles such as `Global`.
4. Do not require consumers to select the first role or join multiple roles into one comma-separated value.
5. Keep the role selection scoped to the application/entity that returned it.

This information will allow the BFF and shared UI adapter to continue exposing the existing scalar role contract to upper applications while preserving the complete CES role list.

Thanks,

## Internal notes

- This is a request draft only; it has not been emailed.
- `primary_role` is the smallest change and is suitable when one legacy-compatible role is sufficient.
- `role_tags` is more flexible when consumers must select different roles by function and scope.
- The field must identify the functional/business role. It must not be filled from a data profile or data policy without an agreed mapping.
- This request does not define saved-item ownership, Cashflow authorization-limit profiles, or PSS exclusion behavior; those remain separate policy decisions.
