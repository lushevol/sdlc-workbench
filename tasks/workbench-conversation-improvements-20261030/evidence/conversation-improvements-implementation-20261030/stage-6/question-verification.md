# Question propagation verification

**The EMS3 answer lacks propagation into the declared candidate architecture record.**
Owner: unknown knowledge reviewer. Action: update the consumer through its existing governance procedure.
Evidence: [real case receipt](questions-case.json) and [reference report](questions-result.json).
Consequence: consumers can still read the superseded Auth Server limitation.

## QUESTIONS-EMS3

```gherkin
Scenario: QUESTIONS-EMS3 detects a resolved answer without its consuming update
  Given KQ-ARCH-16 is ANSWERED_FROM_EVIDENCE with three source references
  And candidate architecture version 1 retains the older Auth EMS3 limitation
  When the reconciliation checker inspects both retained records
  Then it reports ANSWER_PROPAGATION_MISSING
  And it retains the observed consumer version 1
  And it leaves both original records unchanged
  And it grants no publication or business verification
```

The [manifest](questions-manifest.json) records exact original hashes.
The result concerns declared reference drift.
Source inspection separately confirmed the conflicting EMS3 statements.

## Independent review

Independent review found that deeper answer headings escaped the original section hash.
The corrected boundary includes deeper headings and stops at equal or higher headings.
A regression changes a nested answer and asserts that the prior propagation hash becomes stale.
Numeric IDs and malformed consumer metadata now produce structured validation errors.
The [review evidence](independent-review/nested-answer-result.json) preserves the original reproduction.
Ten [focused tests](question-tests.log) passed after correction.

No knowledge content, reviewer identity, approval, or audit history changed.
The existing knowledge review and publication requirements remain applicable.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
