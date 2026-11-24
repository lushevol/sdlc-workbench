---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Ambiguous session example

**FAIL: Correct the control reference and expected result before review. Owner: fixture consumer. The steps below deliberately violate mandatory rules.**

This negative tooling fixture preserves the ambiguity described in the proposal.
It is not a business case or executable automation.
The [corrected fixture](session.md) uses the inspected label, component type, dialog scope, and independent authentication assertions.

```gherkin
Feature: Detect ambiguous session instructions
  @SESSION-AMBIGUOUS-EXAMPLE
  Scenario: Reject an ambiguous interaction and outcome
    Given User A has a portal session
    When User A clicks Extend
    Then the operation succeeds
```

The action omits the component type and scope.
The result has no observable predicate.
Missing source support and missing bindings also prevent automation readiness.

```sh
ai-sdlc gherkin docs/examples/gherkin-session/ambiguous.md --manifest docs/examples/gherkin-session/manifest.json --root .
```

The expected quality state is `FAIL`.
The command must return a nonzero exit status.
