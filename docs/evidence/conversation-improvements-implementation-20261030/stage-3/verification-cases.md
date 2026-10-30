# Stage 3 verification cases

**No critical conclusions require user attention or action.**

Owner: Workbench implementation agent.
Action: integrate the verified coverage and ledger operations.
Business acceptance remains outside these harness checks.

## Real retained ledger

```gherkin
Scenario: LEDGER-REAL retains original browser and unit instances
  Given the original Session Refresh browser inventory and Jest result
  When the ledger imports both original formats
  Then it retains 467 browser instances and 471 unit instances in separate namespaces
```
The [first case receipt](session-ledger-case.json) records all explicit assertions.
The [derived ledger](session-ledger.json) retains source hashes and original statuses.
The [manifest](session-ledger-manifest.json) identifies unchanged original inputs.

Browser outcomes remain 182 passed, 15 failed, 199 partial, and 71 blocked.
Twenty-five characterization passes remain distinct.
Twenty-six definition/source mismatches remain recorded.
RN-S002 has no raw runner status. Its aggregate failure remains a separate declaration.
The Jest result retains 471 passing tests across 123 suites.

The real Jest output repeats 126 suite/full-name labels.
Each runner position remains a separate instance.
These positions do not establish canonical identity across different runs.

## Repeated import

```gherkin
Scenario: LEDGER-REPEAT preserves repeated imports
  Given the same real browser inventory twice
  When the ledger imports each copy under a distinct ID
  Then it retains 1405 records and 938 unique attempts
  And it reports 467 duplicate import records
```
The unique outcome counts remain unchanged.
The [repeat receipt](session-repeat-import-case.json) records the result.

## Selected coverage

```gherkin
Scenario: COVERAGE-REAL preserves selected assertion coverage
  Given seven real ACs and twelve selected changed files
  When the coverage tool validates the derived index
  Then it generates all three matrices
  And the complete changed-predicate denominator remains unknown
```

Inputs: [derived index](session-coverage-index.json).
Outputs: [coverage matrices](session-coverage.json).
The [coverage receipt](session-coverage-case.json) records exact metrics and limits.

All seven ACs have selected assertion-map references.
The adapter preserves grouped associations. It does not invent individual assertion-to-case joins.
All twelve selected files have a directly inspected representative assertion and a matching retained unit result.

Six files concern business changes. Six files provide supporting maintenance.
The complete changed-predicate denominator remains unknown.

Complete predicate coverage and behavioral equivalence remain unproved.
The adapter narrows representative assertions to the matching case source ranges.
The [adapter](verify-real-coverage.py) retains exact Git snapshots and checks their declared hashes.

No AC gains matching passing coverage for its declared system level.
Selected unit passes cannot fill a system-level evidence gap.
No selected changed-file metric receives a whole-scope percentage.

## CES unknown scope

```gherkin
Scenario: COVERAGE-CES preserves unknown scope
  Given the real CES draft criterion and unknown inventories
  When the coverage tool calculates metrics
  Then it preserves all unknown denominators
  And it omits whole-scope percentages
```

Output: [coverage view](ces-coverage.json).
Zero declared changes does not establish a complete empty change inventory.
The [CES receipt](ces-coverage-case.json) records these assertions.

## Automated boundary checks

The [focused test receipt](focused-tests.json) binds executed checks to exact runtime and test source hashes.
Checks cover unsafe paths, stale evidence, missing results, retries, interruptions, duplicate names, and direct assertion boundaries.
They also separate absent source identities, named environments, characterization, and simulation from eligible passing evidence.
The [initial failures](initial-test-results.json) preserve interpreter and fixture contract errors.
The [adapter error](coverage-adapter-initial-failure.json) preserves the initial task-relative source reference limit.
The adapter now handles retained source files without Git revision declarations.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
