---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
---

# Owner decisions

Nine unanswered questions need seven scoped responses. Three recorded answers are reproduced below.
Confidence is high for the recorded text and source limits. Synthetic evidence supplies no business-execution acceptance.

The editable fields below supplement the [original living questions](../tasks/questions.md).
For every field, another answer, “unknown,” or a named contact is acceptable.
Record respondent, authority, date, and applicable scope beside each returned answer.

## Policy decisions

### Portal UAT activity — KQ-02, KQ-05, KQ-07

Owner `owner:portal`. Authority `policy`, actor `operator`, environment `UAT`, version `v1`, decision `renewal-scope`.

These questions share one decision context. KQ-01 already records “Mouse, keyboard, and scroll.”
The draft qualifies renewal while refresh credentials remain usable. Event details affect eligibility. [Activity source](../sources/portal/activity.md)

| ID | Decision needed | Proposed options | Editable answer |
| --- | --- | --- | --- |
| KQ-02 | Do touch events qualify? | Eligible, ineligible, or condition-specific. | ___ |
| KQ-05 | Which keyboard and scroll inputs qualify? | All such inputs, or a specified subset with conditions and exclusions. | ___ |
| KQ-07 | Are synthetic input events eligible? | Eligible, ineligible, or condition-specific. | ___ |

### Portal PROD touch — KQ-03

Owner `owner:portal`. Authority `policy`, actor `operator`, environment `PROD`, version `v1`, decision `renewal-scope`.

Does touch qualify in PROD? Choose eligible, ineligible, or condition-specific, with any conditions.
The supplied source leaves touch unspecified. The recorded UAT answer has its own scope. Production adoption remains unverified. [Activity source](../sources/portal/activity.md)

**Answer** ___

### Late-arrival retention — KQ-12

Owner `owner:settlement`. Authority `policy`, actor `operator`, environment `UAT`, version `v1`, decision `late-arrival`.

What retention duration applies? Supply the duration and unit, including any applicable conditions.
The source leaves duration unresolved and provides no default. This answer completes the missing retention rule. [Recovery source](../sources/settlement/recovery.md)

**Answer** ___

## Engineering evidence requests

Each engineering owner is `unknown`. A named responsible contact can resolve ownership.

| ID and exact scope | Evidence needed and consequence | Editable answer |
| --- | --- | --- |
| KQ-04 · authority `engineering` · actor `operator` · environment `UAT` · version `v1` · decision `renewal-scope` | Does ui-42 implement touch renewal? Supply inspected code and applicable touch assertions or execution evidence. Available observations cover local mouse events, a controlled clock, and a stub issuer. Touch support remains unknown. [Observation](../sources/portal/observation.md) | Implemented, absent, conditional, or unknown, with evidence/contact ___ |
| KQ-06 · authority `engineering` · actor `operator` · environment `UAT` · version `v2` · decision `renewal-timing` | What delay does v2 use? Supply its exact revision and timing configuration or code. The available 5,000 ms delay belongs to ui-42. v2 timing remains unverified. [Observation](../sources/portal/observation.md) | Delay and unit, revision, evidence/contact ___ |
| KQ-09 · authority `engineering` · actor `service` · environment `UAT` · version `v1` · decision `issuer` | Supply effective issuer configuration and clock evidence bound to UAT. YAML specifies 15 minutes. Local JVM override is 480 minutes. One UAT sample lasts 900 seconds. Effective UAT configuration and clock offset remain unknown. [Runtime source](../sources/operations/runtime.md) | Configuration, clock evidence, environment/build binding, or contact ___ |

## Publication decision — KQ-08

Owner `owner:portal`. Authority `publication`, actor `reviewer`, environment `UAT`, version `v1`, decision `publish`.

May the [Portal candidate](../knowledge/records/portal.md) be published?
Proposed responses are approve reviewed bytes, request revisions, or defer with a reason.
Record the authorized reviewer and exact reviewed hash. Current candidate hash is below.

```text
d0f432185cb07637f5cdb6531f386535aac7cd8aa8d04417fc4260859d812d7f
```

The declaration records candidate publication and absent human approval. Historical local execution is the available execution scope. [Declaration](../selection.json)

**Answer** ___

## Recorded answers

These quotations reproduce the three populated answers exactly. Each answer applies to its recorded question and scope. [Living questions](../tasks/questions.md)

| ID | Authority / actor / environment / version / decision | Owner | Exact recorded answer |
| --- | --- | --- | --- |
| KQ-01 | policy / operator / UAT / v1 / renewal-scope | owner:portal | Mouse, keyboard, and scroll. |
| KQ-10 | maintenance / agent / local / v1 / recovery | maintainer | Continue the saved payment recovery draft; retain accepted work. |
| KQ-11 | policy / agent / local / v1 / retention | maintainer | No. Review consumers and provenance first. |

## Resume context

KQ-10 points to the [saved recovery draft](../tasks/recovery-draft.md).
The checkpoint accepts Portal activity and context, identifies recovery as unfinished, and holds Access for denial-clause review. [Checkpoint](../tasks/checkpoint.json)

The recovery source supplies original-reference retry and accepted-reference duplicate prevention.
The saved draft needs these details. Only late-arrival duration requires the remaining settlement answer. [Recovery source](../sources/settlement/recovery.md)

The Access source already supplies denial without a matching action grant. Canonical review remains pending. [Grant source](../sources/access/grants.md)

The saved “all four” completion claim conflicts with this checkpoint and the incomplete candidate content.
Reviewed receipt labels and wiki freshness alone leave that discrepancy unresolved. [Progress](../tasks/progress.md), [Settlement candidate](../knowledge/records/settlement.md), [Access candidate](../knowledge/records/access.md), [Receipts](../selection.json)

KQ-11 is answered. The retention instruction requires consumer and provenance review, meaningful failure retention, and one canonical payload.
The historical consumer inventory remains incomplete. [Retention source](../sources/operations/retention.md)
