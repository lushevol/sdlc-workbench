# CES coverage automation input

- Source: User message in the Codex chat.
- Date: 3 November 2026, Asia/Singapore.
- Priority: High-priority scope clarification and implementation request.

## Exact user input

```text
FMO Portal Admin entity is an exception: it only exists in the non-production environment, hasn't launched yet, and isn't assigned to any users. Because of that, we can keep its comparison as a lower priority.

For the rest of the comparisons, it comes down to what we discussed regarding entitlements and users:

1. Entitlements: First, when comparing the two, there are no missing entitlements and no gaps. However, you need to understand the mapping relationship. Going from EMS2 to CES, role, entity, subject, and action map over to entitlement, app, feature, action. Once those are mapped, we filter out everything that has been completely migrated.
2. Users: As you can see, I only gave you data for two users, but in reality, there are a huge number of users in a single cell. Because of that, you'll need to write a script to dynamically fetch all the users and then run the comparison to generate the final result.

I want both of these coverage checks to run end-to-end via a script with a single click and output the results.
```
