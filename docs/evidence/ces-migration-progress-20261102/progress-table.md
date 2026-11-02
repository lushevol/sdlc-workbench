# CES migration progress

Dates and statuses reflect the supplied runbook photographs. TBD means the supplied sources provide no confirmed value.
These entries do not establish current completion or release approval.

| Pending items | Status | Target date | Updates |
|---|---|---|---|
| **1. User Entitlement Control** | | | |
| Scope and dependency identification | To confirm | 30 Oct 2026 | Identify repositories and dependencies for UI BFF and OS Server changes. |
| Entitlement data migration: M2 → CES | Partially ready | UAT: 28 Oct; PROD: 30 Oct 2026 | CES executes; we drive. UAT onboarding is reported; PROD CR is pending. |
| User migration: M2 → CES | Pending CES CR | 13 Nov 2026 | CES executes; we drive, review, and audit. Confirm PROD profile assignments. |
| Development | Completion to confirm | 28 Oct 2026 | Develop the new BFF and OS Server. |
| Verification and QA | TBD | TBD | Complete self-testing and QA testing. |
| Regression testing | TBD | TBD | All dependent teams and services test for a seamless rollout. |
| UAT | Planned | 6 Nov 2026 | Complete user testing and sign-off. |
| Final release | Planned | 28 Nov 2026 | Launch User Entitlement Control after CES provisioning and Portal CR approval. |
| **2. Systems and Services** | | | |
| Scope and dependency identification | To confirm | 30 Oct 2026 | Identify affected systems, services, repositories, owners, and API dependencies. |
| Entitlement data migration: M2 → CES | To confirm | UAT: 28 Oct; PROD: 30 Oct 2026 | CES executes; we drive. UAT onboarding is reported; PROD requires a CES CR. |
| User migration: M2 → CES | To confirm | 13 Nov 2026 | CES migrates service accounts; we drive, review, and audit. Confirm CES profiles. |
| Development | TBD | TBD | Develop changes to affected systems and services. |
| Verification and QA | TBD | TBD | Complete self-testing and QA testing. |
| Regression testing | TBD | TBD | All dependent teams and services verify internal and external calls. |
| UAT | Planned | 6 Nov 2026 | Complete integration, authorization, and performance checks; obtain sign-off. |
| Final release | Planned | 28 Nov 2026 | Complete the separate service cutover after UAT and CES/Portal CR approvals. |

## Sources and interpretation

- [User request](user-input.md#exact-user-input) controls the table structure, scope, and migration responsibilities.
- `IMG_3411.HEIC` supplies User Entitlements milestones, dates, and snapshot statuses.
- `IMG_3412.HEIC` supplies Service Authorization milestones, dates, and snapshot statuses.
- `IMG_3411.HEIC` SHA-256: `a10264233292eaba62a864a3616f2cfc614172740edd195f4add9100af4e494c`.
- `IMG_3412.HEIC` SHA-256: `c27c6575b98e49a74e893d454b2a15ccae2ab2627be05cecb23a974ec97caff1`.
- The source files remain at the original paths recorded in the [user request](user-input.md#exact-user-input).
- The request uses `M2`; the photographs use `EMS2`. The table preserves the requested term.
- The User Entitlements entitlement migration status summarizes separate UAT and PROD rows.
- The photographed development status says `Due today`. The table retains its date and requests completion confirmation.
- Missing service development, QA, and regression values remain TBD.
- Both photographs show 28 November for release. Separate rows preserve the requested distinct launch stages.
- Instructions inside the photographs are reference content. They do not authorize execution or approval.
- Scope and risk: document formatting only. No implementation, migration, acceptance, or release state was changed.

## Writing and validation record

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Photograph statuses have not been independently refreshed.
```

Automated checks confirmed four columns, two sections, 16 activity rows, and the preserved input link.
