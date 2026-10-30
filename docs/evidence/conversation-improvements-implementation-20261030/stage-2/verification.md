# Reusable summary verification

**The real Session Refresh summary preserves the recorded hold and all 467 outcomes.**
Owner: Workbench maintainer. Action: reuse this renderer for retained task assessments.
Evidence: [Session result](session-refresh-result.json) and [CES result](ces-result.json).

## SUMMARY-SESSION

```gherkin
Scenario: SUMMARY-SESSION preserves the recorded release decision
  Given the real Session Refresh inventory contains 467 execution records
  And the priority audit contains 285 observations
  When the offline renderer reads the shared index
  Then it displays NO_GO and the RN-S002 replay consequence
  And it displays the owner and next action
  And it preserves 182 passes, 15 failures, 199 partial results, and 71 blocked results
  And it keeps 25 characterization passes separate from intended business verification
  And it collapses the 284 other observations
  And it leaves original evidence bytes unchanged
```

[Desktop inspection](summary-desktop.png) and [mobile inspection](summary-mobile.png) found no horizontal overflow.
The report is readable on both retained viewports.
The initial fixture checks needed resolved macOS paths and an execution artifact role.
Those fixture corrections did not change business evidence.

## SUMMARY-CES

```gherkin
Scenario: SUMMARY-CES preserves unknown release scope
  Given the CES migration has draft criteria and unknown approved inventories
  When the offline renderer reads its shared index
  Then it displays INSUFFICIENT_EVIDENCE
  And it displays zero retained executions
  And it leaves deployment authorization UNKNOWN
```

## Verification limits

Seven summary boundary tests passed.
The related review suites passed 104 tests with zero failures, errors, or skips.
The renderer reports retained assessments. It does not approve releases or inspect deployed behavior.

The full inventory exposed composite case IDs and line references.
The contract now accepts existing slash-separated IDs as identifiers.
The adapter preserves numbered line locators instead of treating them as heading anchors.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
