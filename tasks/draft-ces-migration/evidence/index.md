# CES migration evidence index

> **Migration decisions remain open.**
> Action: complete the [five-question batch](../01-intake.md#answer-and-question-log), or identify the responsible contacts.
> Consequence: complete implementation planning remains blocked.
> Owner: unknown. Evidence: [living intake](../01-intake.md#intake-readiness-and-authority).

## Current task

- [EMS2 to CES output mapping](../03-output-mapping.md), current source-query stage.
- [High-priority mapping request](user-input-20261030-output-mapping.txt), 30 October 2026.

- [Living intake and migration account](../01-intake.md).
- [High-priority current user request](user-input-20261030-migration-plan.txt), 30 October 2026.
- [High-priority historical user inputs](historical-user-inputs-20261028-29.json), 28–29 October 2026.
- [Raw conversation capture](chatgpt-conversation-20261030.json) from [Migration Runbook Template](https://chatgpt.com/c/6ae1608f-7898-83ea-aa42-90a40dfc75cd).

The app returned five exchanges and reported no further page.
Historical user wording establishes intent within its scope.
Assistant drafts do not establish user approval or deployment.

## Completed source investigations

| Investigation | Source identities | Checks and limits |
| --- | --- | --- |
| [API comparison](api-analysis-20261030.md) | [Eight sample hashes and full permission comparison](api-sample-manifest-20261030.json) | [JSON, link, and consistency checks](api-analysis-checks-20261030.json); no live API execution. |
| [Backend migration](backend-analysis-20261030.md) | [Auth, BFF, SDK source manifest](backend-source-manifest-20261030.json) | Exact source and selected assertions; business execution NOT_RUN. |
| [Frontend and consumers](frontend-analysis-20261030.md) | [Source hashes and repository states](frontend-sources-20261030.json) | Local consumers and prior answers; business execution NOT_RUN. |

## Output mapping evidence

- [Mapping source facts and exact JSON pointers](output-mapping-sample-facts-20261030.json).
- [Mapper and consumer facts at exact revisions](output-mapping-code-facts-20261030.json).
- [Source-backed example projections](output-mapping-examples-20261030.json).
- [Mapping lint, reference, fingerprint, and independent review checks](output-mapping-checks-20261030.json).

## Provenance and validation

- [Workspace resource discovery](workspace-status-20261030.json).
- [Source register](source-register-20261030.json), including historical review identity.
- [Task document and source checks](document-checks-20261030.json).
- [Intake artifact lint](intake-lint-20261030.json).

No application code changed. Existing source samples and unrelated worktree changes remain preserved.
The historical review retains its [original location](../../ems3-entitlement-review-20261027/07-code-review.md).
Its older findings need current revision reconciliation; its prior dependency failure does not establish a product failure.

## Writing checks

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
