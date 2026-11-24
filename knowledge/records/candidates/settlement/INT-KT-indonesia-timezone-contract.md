---
type: KnowledgeTopic
id: INT-KT-indonesia-timezone-contract
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-064442d94934445511e7ea15
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/2026
    Design/Cash Settlement Platform Architecture - Indonesia/UTC Time zone impact
    - Indonesia/page.md
  revision: sha256:e80d6bead69cfc90483e3bd16186bbcc3d56f062c51ee363bc4c11db15eebce3
  sha256: e80d6bead69cfc90483e3bd16186bbcc3d56f062c51ee363bc4c11db15eebce3
- id: SRC-5803371f7102bd81d727c4a1
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/2026
    Design/Cash Settlement Platform Architecture - Indonesia/UTC Time zone impact
    - Indonesia/Time Fields Summary/page.md
  revision: sha256:1b4cda0f7dd2183149240560b98d42feb74bdc69ffa8b0e09f72f6de1b035ac8
  sha256: 1b4cda0f7dd2183149240560b98d42feb74bdc69ffa8b0e09f72f6de1b035ac8
generated:
  by: agent:codex:sol-integrations-review
  at: '2026-11-16T01:30:46.199689+00:00'
verified: []
classification: settlement
scope: Indonesia timezone scope and unresolved conversions
summary: Selected source descriptions preserve scoped intended responsibilities. Current
  authority and applicability remain unresolved.
related: []
open_questions:
- 'KDQ-a38deeae40: Which valid JVM, OS, database, and cron UTC configuration applies
  to each service?'
- 'KDQ-d21b459a46: What conversion and precision rules apply to each field, especially
  Z-suffixed inputs treated as local UTC+7?'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Indonesia timezone scope and unresolved conversions

## Scope

Indonesia timezone scope and unresolved conversions.
These source descriptions define separate contracts. They establish no deployed or tested behavior.

## Summary

The selected sources describe related responsibilities and conditions.
Their original authority, effective dates, and current applicability remain unresolved.

## Documented knowledge

### TIME-01 — UTC runtime target

The timezone note targets UTC for JVM/OS and PostgreSQL time behavior.
It identifies effects on LocalDateTime, scheduled cron, and database now/date functions.
The source spells the JVM option `-Duser,timezone=UTC`. This malformed example is not a verified executable instruction.
The accepted configuration and cron scope require confirmation.

[Selected original evidence](../../../evidence/sources/sha256/e80d6bead69cfc90483e3bd16186bbcc3d56f062c51ee363bc4c11db15eebce3.md#L1-L7).

### TIME-02 — Field-level timezone distinctions

The inventory distinguishes local audit, exception, net-trigger, and cutoff fields from upstream UTC timestamps.
History effective/execution times and data-publication timestamps are listed as UTC. Cutoff/release fields are listed as local.
The proposed transformation examples convert local UTC+7 inputs into UTC.
Some examples also treat Z-suffixed inputs as local UTC+7 and reduce displayed precision.
Those examples conflict with ordinary Z semantics and do not establish an accepted conversion or precision-loss rule.
Blank service rows and linked images cannot fill missing field contracts.

[Selected original evidence](../../../evidence/sources/sha256/1b4cda0f7dd2183149240560b98d42feb74bdc69ffa8b0e09f72f6de1b035ac8.md#L1-L20), [Selected original evidence](../../../evidence/sources/sha256/1b4cda0f7dd2183149240560b98d42feb74bdc69ffa8b0e09f72f6de1b035ac8.md#L23-L30), [Selected original evidence](../../../evidence/sources/sha256/1b4cda0f7dd2183149240560b98d42feb74bdc69ffa8b0e09f72f6de1b035ac8.md#L54-L61).

## Connections

The owning task retains related source and question evidence.

## Evidence limits

Source descriptions supply documented intent and historical proposals only.
They do not establish current approval, implementation, configuration, deployment, execution, or acceptance.
Unselected content and attachments were not used to fill gaps.

## Open questions

Owner: unknown. Answers remain pending in the single [task question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
