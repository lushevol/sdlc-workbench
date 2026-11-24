# UI audit evidence

**Use each case scope and assertion mapping before claiming a canonical business result.**

Execution scope: ACTUAL_APPLICATION_LOCAL_SERVICES.

Completed cases: 4 of 4.

- [AUTH-066 short access Home mount acquires recovery](cases/auth-066-short-access-home-mount-acquires-recovery-25e507f64b17-attempt-1/result.json): passed.
- [AUTH-112 fresh login acquires distinct recovery](cases/auth-112-fresh-login-acquires-distinct-recovery-0face8036278-attempt-1/result.json): passed.
- [AUTH-138 recovery removes old entity and controls](cases/auth-138-recovery-removes-old-entity-and-controls-be0ad3149058-attempt-1/result.json): failed.
- [AUTH-144 forged entitlement is rejected by current server](cases/auth-144-forged-entitlement-is-rejected-by-current-server-02f9e8faa9f8-attempt-1/result.json): failed.

writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
