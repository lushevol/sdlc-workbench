---
type: Summary
description: "Preserves candidate advanced-search nesting, LogicFilter rule conflicts, pagination limits, and endpoint proposals."
doc_type: short
full_text: sources/KT-advanced-search-p3.md
---

> **Candidate/draft only:** The DSL rules, examples, and query targets are unresolved proposals. Owner is unknown; `verified` is empty.

# Advanced search p3

The proposal adds nested AND/OR groups for commodity and precious-metal searches while requiring existing query scenarios to remain supported. The guide permits the same field in different groups and limits nesting depth to three. Each LogicFilter object should contain exactly one of `and`, `or`, or `filters`; top-level filters allow at most one item. Some labeled-valid examples violate these rules, and another maps NOTIN to SQL IN. The text and examples need reconciliation before treating the DSL as executable.

The design defines page-index pagination and proposes cashflowUltraQuery and cashflowUltraQueryCount. Cursor and full-dataset modes remain placeholders; configurable sorting is also unfinished. Benefits language does not establish OpenSearch compatibility or memory safety.

The related [[summaries/ARC-uber-open-search-routing-20261115]] describes a separate OpenSearch routing proposal. [[summaries/ARC-platform-cashflow-data-query]] addresses query-model mapping; neither resolves this DSL's rules or proves runtime behavior.

## Canonical sections

- [Search behavior and compatibility](../../../records/candidates/query/KT-advanced-search-p3.md#search-behavior-and-compatibility)
- [LogicFilter structural rules](../../../records/candidates/query/KT-advanced-search-p3.md#logicfilter-structural-rules)
- [Pagination and endpoint proposals](../../../records/candidates/query/KT-advanced-search-p3.md#pagination-and-endpoint-proposals)

## Typed input and result boundaries

Operator and value selectors remain unchanged. RatanUltraQuery requires filters, pagingOption, pageIndex, itemsPerPage, and orderArgs; cursor remains optional. Required orderArgs coexists with unfinished configurable sorting, and an example supplies an empty array. [Canonical detail](../../../records/candidates/query/KT-advanced-search-p3.md#typed-advanced-query-input-and-result-catalog)

UltraQueryResult requires totalResult, itemsPerPage, lastPage, and results. The results list and ResultNew items are non-null; pageIndex and pagingCursors are nullable. Cursor previous/next values are nullable strings. Count input requires filters; count result requires integer count. Both query payload arguments are nullable. These proposed contracts establish no executed compatibility. [Canonical detail](../../../records/candidates/query/KT-advanced-search-p3.md#typed-advanced-query-input-and-result-catalog)
