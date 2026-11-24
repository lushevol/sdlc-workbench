# CES role-owned writes remain pending

- Source: User answer to the implementation clarification in this Codex chat.
- Date: 2026-11-06 (Asia/Singapore).
- Priority: High-priority clarification for this implementation.

## Exact question

> For CES saved views and filters, the backend still expects one owner role. When a user has several CES roles, how should a new item choose its owner?

## Exact user answer

> Keep CES role-owned writes pending until the ownership rule is agreed

## Scope

Do not select a primary CES role or send comma-joined role names as a scalar owner.
Keep the affected CES write paths unavailable until a sourced ownership rule exists.
Preserve existing EMS2 ownership behavior.
This answer does not define CES role-query rules or approve a multiple-role exclusion policy.
