# UI audit evidence

**Use each case scope and assertion mapping before claiming a canonical business result.**

Execution scope: ACTUAL_APPLICATION_LOCAL_SERVICES.

Completed cases: 10 of 10.

- [AUTH-043 acquire recovery at T+875 without moving access expiry](cases/auth-043-acquire-recovery-at-t-875-without-moving-access-expiry-3a0261508518-attempt-1/result.json): passed.
- [AUTH-007 actual React PROD credential visibility Y](cases/auth-007-actual-react-prod-credential-visibility-y-b9b8b72d28ff-attempt-1/result.json): passed.
- [AUTH-044 do not acquire recovery at T+874.999](cases/auth-044-do-not-acquire-recovery-at-t-874-999-eed832c71c04-attempt-1/result.json): passed.
- [AUTH-077 access expiry boundary at T+899999ms](cases/auth-077-access-expiry-boundary-at-t-899999ms-d77a7aa88b13-attempt-1/result.json): passed.
- [AUTH-076 access expiry boundary at T+900000ms](cases/auth-076-access-expiry-boundary-at-t-900000ms-86faf42e0a62-attempt-1/result.json): passed.
- [AUTH-081 missing refresh logs out at access expiry](cases/auth-081-missing-refresh-logs-out-at-access-expiry-89b090f09694-attempt-1/result.json): failed.
- [AUTH-080 Logout clears local access after the 1000ms delay](cases/auth-080-logout-clears-local-access-after-the-1000ms-delay-109596f2f5a8-attempt-1/result.json): passed.
- [AUTH-083 open-dialog refresh cutoff at T+598000ms](cases/auth-083-open-dialog-refresh-cutoff-at-t-598000ms-e97b3c1e7ac5-attempt-1/result.json): timedOut.
- [AUTH-084 open-dialog refresh cutoff at T+597999ms](cases/auth-084-open-dialog-refresh-cutoff-at-t-597999ms-208660cd6b09-attempt-1/result.json): timedOut.
- [AUTH-078 manual Extend installs response B and sends controlled validation with B](cases/auth-078-manual-extend-installs-response-b-and-sends-controlled-validation--38fe438c5232-attempt-1/result.json): passed.

writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
