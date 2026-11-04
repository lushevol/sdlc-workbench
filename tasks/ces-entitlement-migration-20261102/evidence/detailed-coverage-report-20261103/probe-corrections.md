# Sample verification correction

No critical conclusions require user attention or action.

The first sample checker collapsed repeated spaces within HTML table cells.
The supplied role name contains two spaces: `FM Trading -  Rates`.
The report retained those source bytes. The checker incorrectly changed them before comparison.

Original assertion:

```text
AssertionError: ('report', 'HTML missing tuple', ('RATAN_ENTITLEMENT_RULE', 'FM Trading -  Rates'))
```

The corrected checker strips cell boundaries and preserves internal whitespace.
The comparison predicates and report content remain unchanged.

```yaml
standard: ASD-STE100
automated_check: NOT_RUN
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
