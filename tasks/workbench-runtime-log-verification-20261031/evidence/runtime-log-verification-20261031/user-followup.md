# Runtime evidence metric and local pilot request

Source: User message in Codex chat.
Date: 2026-10-31, Asia/Singapore.
Priority: High-priority reference for the metric and pilot scope.

## Exact user input

> It must be one key metric in release confidence checking, to collect logs from remote log systems (local logs only feasible for local development) when UAT processing. Let’s use session renewal issue fixing as example to check if your plan is right. run in local first.

## Scope

The user requires runtime log evidence as a key release-confidence metric during UAT.
UAT evidence must come from remote log systems. Local logs support local development only.
The user requests a local pilot using the existing session-renewal fix.
The pilot does not establish remote UAT collection or production suitability.

## Report checks

```yaml
standard: ASD-STE100
automated_check: NOT_RUN
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
