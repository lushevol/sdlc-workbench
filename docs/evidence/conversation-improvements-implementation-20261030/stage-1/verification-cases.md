# Stage 1 verification cases

**Scope: validate real retained references while preserving unknown and adverse outcomes.**
Owner: Codex. Action: execute the two reference cases and the package installation case.
Evidence: [implementation authorization](../user-input.md).

These cases verify harness behavior. They do not establish business acceptance or deployment readiness.

## IDX-SESSION: Preserve real Session Refresh outcomes

```gherkin
Scenario: IDX-SESSION preserves selected retained dispositions
  Given the real Session Refresh aggregate contains 467 instances
  And the pilot selects RN-A001, RN-A007, RN-A009, RN-A011, RN-W001, and RN-S002
  When the installed assurance index command validates the pilot
  Then the reference contract is valid
  And all six normalized outcomes equal the recorded aggregate dispositions
  And each original status and characterization flag remains unchanged
  And RN-S002 retains its recorded release hold
  And RN-A001 retains its recorded P4 disposition without a release hold
  And business verification remains NOT_VERIFIED
```

Input: [selected reference index](session-refresh-index.json).
Sources remain referenced from that index with their exact SHA-256 values.
Unknown levels, environments, and assertion completeness remain unknown.

## IDX-CES: Preserve unknown approved scope

```gherkin
Scenario: IDX-CES preserves draft scope and missing execution
  Given the real CES intake contains draft criterion MIG-AC-001
  And approved criterion, complete change, and case inventories remain unknown
  When the installed assurance index command validates the CES pilot
  Then the reference contract is valid
  And all three inventory completeness values remain UNKNOWN
  And the execution inventory remains empty
  And no release recommendation is invented
  And business verification remains NOT_VERIFIED
```

Input: [CES reference index](ces-migration-index.json).
The source intake retains its own readiness and review state.

## IDX-WHEEL: Preserve standalone distribution

```gherkin
Scenario: IDX-WHEEL exposes the installed reference contract
  Given a wheel built from the completed stage
  And that wheel is installed outside the source checkout
  When its installed command initializes a fresh workspace
  Then the fresh workspace contains the shared review guide
  And the installed index schema has version 1
  And the fresh workspace has no runtime source or project evidence
  And workspace validation succeeds
```

The installation uses prepared local dependencies. It does not require a package-registry download.
The check covers the executing platform only.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
