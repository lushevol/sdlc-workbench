# Delivery branch instruction

Source: direct user message, 6 November 2026, Asia/Singapore.
Authority: latest explicit branch and PROD baseline instruction.

## Exact user input

> for changes in mfe-base and mfe-ratan-container and single-ui-bff, create new branch to ship your change not on main, main is represent for PROD.

## Authorized scope

Create delivery branches for the three application repositories.
Remove this task's migration commit from mfe-base main after preserving it on the delivery branch.
Preserve existing PROD baseline refs and unrelated work.
Do not push or deploy through this instruction alone.
