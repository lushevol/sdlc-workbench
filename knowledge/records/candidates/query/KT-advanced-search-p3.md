---
type: KnowledgeTopic
id: KT-advanced-search-p3
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Settlement
    Advanced Search Design/Ratan Advanced Search Guide/page.md
  revision: sha256:35dddbc053e967ef7fdf94ae3bdb35cb97c397a21ccecf954436a8d4c0227359
  sha256: 35dddbc053e967ef7fdf94ae3bdb35cb97c397a21ccecf954436a8d4c0227359
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Settlement
    Advanced Search Design/page.md
  revision: sha256:098042589beedfc1d4898db3c7b7a35f2db0e0e8c3ba5e68ea796f1b8b99f04f
  sha256: 098042589beedfc1d4898db3c7b7a35f2db0e0e8c3ba5e68ea796f1b8b99f04f
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:23:59.479662+08:00'
verified: []
scope: Historical selected-source design for advanced search p3.
classification: query
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which DSL rules and examples are authoritative, including nesting counts, single-key
  objects, NOTIN, and sort/pagination scope?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Advanced search p3

## Scope

Historical selected-source design for advanced search p3.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Search behavior and compatibility

The advanced-search proposal adds nested AND/OR groups for commodity and precious-metal use cases.
All existing query scenarios must remain supported.
Field operators, pagination, and logical result selection are required.
Sorting and OpenSearch compatibility are listed as nonmandatory new scope in the feature table, despite stronger benefits language.

The guide allows the same field in different groups and limits nesting depth to three.

Sources: [original lines 3–105](../../../evidence/sources/sha256/098042589beedfc1d4898db3c7b7a35f2db0e0e8c3ba5e68ea796f1b8b99f04f.md#L3-L105), [original lines 10–13](../../../evidence/sources/sha256/35dddbc053e967ef7fdf94ae3bdb35cb97c397a21ccecf954436a8d4c0227359.md#L10-L13).

### LogicFilter structural rules

Each LogicFilter object contains exactly one of and, or, or filters.
Top-level filters contains at most one item.
Groups without child groups require more than one filter item, otherwise the filter moves to the parent.
The examples conflict with these rules: a valid-labeled top-level filter has multiple items.

Another sample maps NOTIN to SQL IN and has incomplete SQL.
The count example also mixes and and or at one level.
The rule text and examples require reconciliation before treating the DSL as executable.

Sources: [original lines 3–105](../../../evidence/sources/sha256/098042589beedfc1d4898db3c7b7a35f2db0e0e8c3ba5e68ea796f1b8b99f04f.md#L3-L105).

### Pagination and endpoint proposals

Page-index pagination is the defined mode.
Cursor and full-dataset modes remain placeholders.
Sorting defaults to creation time, while configurable sorting remains a placeholder.
The proposal defines cashflowUltraQuery and cashflowUltraQueryCount with LogicFilter inputs and result metadata.

The benefits statement does not establish OpenSearch parity or OOM safety.

Sources: [original lines 3–105](../../../evidence/sources/sha256/098042589beedfc1d4898db3c7b7a35f2db0e0e8c3ba5e68ea796f1b8b99f04f.md#L3-L105), [original lines 136–143](../../../evidence/sources/sha256/098042589beedfc1d4898db3c7b7a35f2db0e0e8c3ba5e68ea796f1b8b99f04f.md#L136-L143).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which DSL rules and examples are authoritative, including nesting counts, single-key objects, NOTIN, and sort/pagination scope?
