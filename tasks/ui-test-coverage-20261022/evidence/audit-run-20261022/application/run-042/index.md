# UI audit evidence

**Use each case scope and assertion mapping before claiming a canonical business result.**

Execution scope: ACTUAL_APPLICATION_LOCAL_SERVICES.

Completed cases: 9 of 9.

- [AUTH-062 access acquisition race](cases/auth-062-access-acquisition-race-a0bf076df3ed-attempt-1/result.json): passed.
- [AUTH-063 access acquisition race](cases/auth-063-access-acquisition-race-5880ba871fde-attempt-1/result.json): passed.
- [AUTH-093 logout blocks renewal paths](cases/auth-093-logout-blocks-renewal-paths-08e2cdfdcafd-attempt-1/result.json): passed.
- [AUTH-097 late recovery cannot restore logout](cases/auth-097-late-recovery-cannot-restore-logout-27a83652d3d7-attempt-1/result.json): failed.
- [AUTH-098 rapid recovery activation](cases/auth-098-rapid-recovery-activation-cba34cc05986-attempt-1/result.json): failed.
- [AUTH-099 malformed refresh timeout mount](cases/auth-099-malformed-refresh-timeout-mount-c8aa44a1d2df-attempt-1/result.json): failed.
- [AUTH-104 feedback popup boundary](cases/auth-104-feedback-popup-boundary-0ea96f2ae13a-attempt-1/result.json): passed.
- [AUTH-105 feedback popup boundary](cases/auth-105-feedback-popup-boundary-495ebd910e23-attempt-1/result.json): passed.
- [AUTH-106 feedback popup boundary](cases/auth-106-feedback-popup-boundary-7d052e0de1cb-attempt-1/result.json): passed.

writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
