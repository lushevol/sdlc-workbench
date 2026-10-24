# Release report implementation questions

Date opened: 2026-10-24 (Asia/Singapore).
Status: Unanswered. Preparation can finish with these questions open.

The [exact user request](evidence/release-report-intake-20261024/user-input.md#exact-input) defines the scope.
The [preparation report](RELEASE_REPORT_REPRODUCTION.md) explains the source behavior and proposed design.
Keep answers here, with their source and date.
No proposed choice below is selected.

## Q1: Target release identity

The [source collector](../core/release-report/ado-api/release.ts#L11-L40) accepts an ADO work item ID.
Other release identifiers need a different collection path.

Question: Which identity should the initial report accept?

Proposed choices: Release work item; classic release pipeline release; YAML pipeline run.
Another answer, unknown, or a named contact is also valid.

- Answer: _Unanswered._
- Organization or collection and project: _Unanswered. Do not enter credentials._
- Reference release and build IDs: _Unanswered._
- Expected report locator, if available: _Unanswered._
- Answer source and date: _Unanswered._

## Q2: Production baseline

The [source selection](../core/release-report/ado-api/pipeline.ts#L80-L174) infers production from named stages and limited history.
That code does not establish the team's authoritative deployment rule.

Question: What evidence identifies the production baseline for each repository?

Proposed choices: Explicit deployed build ID; approved release record with deployment evidence; documented stage-history rule.
Another answer, unknown, or a named contact is also valid.

- Answer: _Unanswered._
- Evidence locator and process owner: _Unanswered._
- Main branch, production stage, and rollback stage mappings: _Unanswered._
- Answer source and date: _Unanswered._

## Q3: Compliance scope

The [compliance import](../core/release-report/ado-api/client.ts#L54-L60) refers to missing source.
The [UI mappings](../core/release-report/release/data/compliance-audit.ts#L118-L152) name checks but do not define backend rules.
Release Clinic has a separate [TDA reporting procedure](RELEASE_CLINIC.md#generate-an-html-release-report).

Question: Which compliance scope should the replacement use?

Proposed choices: Existing Release Clinic TDA rules; recovered original rules; source fields without a new compliance verdict.
Another answer, unknown, or a named contact is also valid.

- Answer: _Unanswered._
- Rule source, version, and responsible owner: _Unanswered._
- Required custom field mappings: _Unanswered._
- Answer source and date: _Unanswered._

## Q4: Delivery and feature scope

The source contains a host-dependent page and an optional graph consumer.
It contains no report upload path.
The [proposed stages](RELEASE_REPORT_REPRODUCTION.md#small-implementation-stages) start with local JSON and HTML.

Question: Which delivery should the initial implementation provide?

Proposed choices: Local JSON and HTML; Workbench interactive page; attachment on the selected ADO work item.
Another answer, unknown, or a named contact is also valid.

- Answer: _Unanswered._
- Required sections, including graph or Sonar issues: _Unanswered._
- Attachment destination and write authorization, if selected: _Unanswered._
- Answer source and date: _Unanswered._

## Review status

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
