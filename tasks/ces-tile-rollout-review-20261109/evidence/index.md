# Evidence index

> **Four implementation findings and one exposed-contract gap remain open.**
> Action: review the [findings](../10-change-review.md#findings) and select corrections. Owner: unknown.
> Consequence: dependency initialization and complete tile isolation remain unresolved.

- [Latest compatibility clarification](user-followup-20261110.md#exact-user-input).
- [BFF consumer contract trace](bff-contract-followup.json) and [auth wire-contract comparison](auth-contract-followup.json).
- [Exact user input](user-input.md#exact-user-input) and [bounded intake](../01-intake.md).
- [Current code review](../10-change-review.md) and [all 113 tile results](../09-tile-rollout.md#per-tile-result).
- [Canonical probe cases](../06-test-cases.md).
- [BFF comparison](single-ui-bff-context.json), [BFF dispositions](bff-review.json), and [BFF scan](single-ui-bff-scan.json).
- [Auth comparison](ratan-auth-server-context.json), [auth dispositions](auth-review.json), and [auth scan](ratan-auth-server-scan.json).
- [CES candidate inventory](entitlement-scan.json). Matches require source review. They are not confirmed findings.
- [Dependency assertions](probe_bff_dependencies.py) and [paired results](bff-dependencies.json).
- [Rollout assertions](probe_bff_rollout.py) and [four case results](bff-rollout-probe.json).
- [28 routing/drawer results](bff-routing-tests/result.json) and [34 mapper results with blocked service compilation](bff-mapper-service-tests/result.json).
- [Auth mapper assertions](AuthMappingProbe.java) and [revision mismatch result](auth-mapping-probe.json).
- [Final document and source validation](review-validation.json).

Result files retain source hashes, dependency identities, case outcomes, timestamps, and substitutions.
The tile inventory references the canonical supplied CSV. It does not copy the payload.
Passing observation probes can reproduce product defects. They do not establish product conformance.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
