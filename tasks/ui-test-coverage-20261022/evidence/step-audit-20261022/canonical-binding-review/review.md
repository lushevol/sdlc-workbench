# Canonical binding review and correction

No critical conclusions require user attention or action.

The focused review found two material test binding defects.
[AUTH-143](../../../test-cases.md#auth-143) is corrected and passed with controlled provider responses.
The root agent corrected the [AUTH-098](../../../test-cases.md#auth-098) observer and retained its resulting failure separately.

## Findings

### CANON-BIND-001: Count application recovery transitions

Priority: P2. Owner: Audit harness owner.

The previous AUTH-098 assertion incremented a local counter once after a response helper completed.
That helper can deliver multiple queued responses. The assertion could pass after multiple effective application transitions.
The canonical assertion requires the application transition count.

Evidence: [Initial source findings](findings.json) and [canonical assertion](../../../test-cases.md#auth-098).
Next action: Use an application transition observer and retain its count after responses settle.
The root agent completed this correction. It reported run-079 failure at step 7.
This review did not independently execute that run.

### CANON-BIND-002: Enact provider cancellation before retry

Priority: P2. Owner: Audit harness owner.

The previous AUTH-143 setup opened a fresh login page and recorded a cancellation label.
It did not start or cancel an earlier provider attempt.
A normal first SSO navigation could therefore satisfy the cancellation retry case.

Evidence: [Initial source findings](findings.json) and [canonical setup](../../../test-cases.md#auth-143).
Next action: Start SSO-A, cancel through the provider boundary, then verify the next provider navigation.
The correction now performs those actions with controlled provider HTML.
It checks the returned anonymous login state and zero callback login requests.
It then requires exactly two provider visits, labelled SSO-A and SSO-B.

## Retained correction evidence

[Correction metadata](auth143-correction.json) records source hashes, canonical hashes, validation, and every screenshot hash.
[Run result](../../audit-run-20261022/application/run-078-retry/run-result.json) records one passed case.
[Case result](../../audit-run-20261022/application/run-078-retry/cases/auth-143-source-configured-sso-navigation-bddb5f7531d4-attempt-1/result.json) records the executed assertions.
[Step ledger](../../audit-run-20261022/application/run-078-retry/cases/auth-143-source-configured-sso-navigation-bddb5f7531d4-attempt-1/frames.json) records five passed canonical steps and eight frames.

- [SSO-A provider frame](../../audit-run-20261022/application/run-078-retry/cases/auth-143-source-configured-sso-navigation-bddb5f7531d4-attempt-1/002-sso-a-provider-before-cancel.png).
- [Cancellation return frame](../../audit-run-20261022/application/run-078-retry/cases/auth-143-source-configured-sso-navigation-bddb5f7531d4-attempt-1/003-sso-a-cancelled-return.png).
- [New navigation frame](../../audit-run-20261022/application/run-078-retry/cases/auth-143-source-configured-sso-navigation-bddb5f7531d4-attempt-1/005-step-03.png).

Type checking and the source diff check passed.
All eight screenshot hashes matched their retained files.
The run reported no source drift. The three essential frames passed visual review.

The first launch selected zero tests because an anchored grep excluded Playwright's file-prefixed title.
[That launch](../../audit-run-20261022/application/run-078/run-result.json) remains retained.
The corrected selection executed AUTH-143 in a fresh directory.

## Scope and limits

The review inspected selected authentication, workspace, catalog, module, notification, administration, and dialog bindings.
BFF and KNOW boundaries were excluded. Previously reviewed raw-store and accessibility nuances were excluded.
The review focused on consequential setup and assertion gaps. It does not establish exhaustive semantic coverage.

The corrected test uses the prepared actual frontend and controlled provider responses.
Real identity-provider cancellation remains unverified.
AUTH-029 retains its previous path. Only AUTH-143 was rerun.
No business repository source or BFF database was changed.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
