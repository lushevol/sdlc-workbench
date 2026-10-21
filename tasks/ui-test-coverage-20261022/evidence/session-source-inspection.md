---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Authentication and session source inspection

> **Proposed expectations need review before business acceptance.**
> Action: Review the proposed cases before acceptance. Consequence: Their acceptance assertions remain unapproved.
> Owner: unknown. Evidence: [Canonical session cases](../test-cases.md#group-login). No business execution occurred.

## Scope and revisions

The contribution contains 144 UI case designs. It contains 119 implementation characterizations and 25 proposed expectations.
Each design has a stable ID, concrete setup, Gherkin step arrays, and visible UI assertions.
No case ran during this source inspection. No passing behavior or deployed configuration is established.

| Repository | Exact HEAD | Worktree state |
| --- | --- | --- |
| mfe-base | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `tsconfig.tsbuildinfo` modified before this inspection. Source files inspected here are unchanged. |
| single-ui-bff | `834b4155232222347220e47139a502ee43a9cbdf` | Clean. |

The affected scope includes login, token interception, session timers, and profile logout callers.
Risk is high for authentication state. A stale response can restore permissions after a user changes sessions.
This task changes no application source.

## Coverage

| Category | Cases |
| --- | --- |
| Login | 28 |
| SSO | 8 |
| Identity | 6 |
| Refresh | 26 |
| Activity | 7 |
| Expiry | 18 |
| Suspension | 8 |
| Logout | 13 |
| Multi-tab | 3 |
| BFF boundary | 22 |
| SSO security | 5 |

## Source-backed observations

- The visible acquisition schedule uses access expiry minus 25 seconds. Hidden transitions can request recovery credentials.
- Mouse movement uses a five-second debounce. Activity extension stops below 25 seconds of remaining access.
- Recovery reuse requires more than three hours of remaining refresh lifetime. Exactly three hours permits replacement.
- Access expiry opens the expiration dialog. Recovery requires an explicit Extend action.
- The existing dialog starts logout two seconds before refresh expiry. The logout action waits one second.
- A refresh cutoff can end the session while a renewed access credential remains valid.
- BFF validation, extension, acquisition, and relogin reject revoked session identifiers.
- The UI clears authentication when an error contains `TOKEN_INVALID_EXPIRED`. A bare 401 follows another error branch.

Fixture times are controlled inputs. They do not establish approved or deployed policy values.
The fixture access lifetime is 900 seconds. The server-derived refresh fixture uses 13524 seconds.

## Review findings

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| AUTH-F-001: Callback state checks are unproved. | [Callback reader](../../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L20) | Login-CSRF acceptance cannot rely on this reader alone. | unknown | Review the identity-provider boundary and the proposed SSO security cases. |
| AUTH-F-002: Relogin returns no request promise. | [Relogin caller](../../../repos/ui/mfe-base/src/hooks/service/index.ts#L89), [dialog action](../../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L54) | The dialog can close before the recovery response completes. | unknown | Execute pending, rejected, and late response cases before acceptance. |
| AUTH-F-003: Timeout decoding lacks a local error catch. | [Timeout setup](../../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25) | Malformed refresh credentials can interrupt dialog setup. Source predicts this risk; no reproduction occurred. | unknown | Review the proposed malformed-credential recovery case. |
| AUTH-F-004: Empty drawers do not update drawer state. | [Drawer handler](../../../repos/ui/mfe-base/src/utils/login.ts#L98) | Existing catalog state can remain when a new response contains an empty drawer list. | unknown | Execute cross-user and permission-removal cases. |
| AUTH-F-005: Password values are trimmed. | [Credential controller](../../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L57) | Whitespace-sensitive passwords can change before authentication. Intended policy is unknown. | unknown | Confirm the credential whitespace policy before business acceptance. |
| AUTH-F-006: Error strings are rendered from service responses. | [Error mapper](../../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L20) | Sensitive response text can reach the UI. Source does not establish redaction. | unknown | Review permitted error content and execute the proposed secret-redaction case. |

These are source risks and design gaps. They are not executed defect reproductions.
Old-versus-new release comparison is outside this case-design request. No implementation change is attributed.

## Inspected assertion evidence

The lifecycle test asserts visible dialogs, manual Extend, stored credential removal, and sign-in state.
Its Axios adapter and controlled clocks replace live service and browser timing.
The refresh helper tests assert reuse boundaries, shared requests, cancellation, and retry.
The BFF controller test asserts HTTP status, result, and expiration with mocked token services.
These inspections establish assertion scope only. The commands did not run the tests.

| Assertion source | Inspected area | Limits |
| --- | --- | --- |
| [Lifecycle tests](../../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L198) | Acquisition, Extend, suspension, cutoff, and cleanup assertions. | Controlled clock and adapter. Not executed. |
| [Refresh tests](../../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82) | Three-hour boundary, malformed payloads, shared requests, retry, and cancellation. | Helper assertions. Not UI execution. |
| [BFF controller tests](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationControllerTest.java#L700) | Extension status, result, and expiration assertions. | Mocked token and session collaborators. Not executed. |

## Source locators and hashes

Paths resolve from this report. Hashes identify inspected working bytes.

| Source path and locator | Revision | SHA-256 |
| --- | --- | --- |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java:161](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L161) | `834b4155232222347220e47139a502ee43a9cbdf` | `6f8f759d314d97b41a6d0ad35a26a5cce475cc4c40d7ccf06f729668c8f15b3b` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java:202](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L202) | `834b4155232222347220e47139a502ee43a9cbdf` | `6f8f759d314d97b41a6d0ad35a26a5cce475cc4c40d7ccf06f729668c8f15b3b` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java:252](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L252) | `834b4155232222347220e47139a502ee43a9cbdf` | `6f8f759d314d97b41a6d0ad35a26a5cce475cc4c40d7ccf06f729668c8f15b3b` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java:335](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L335) | `834b4155232222347220e47139a502ee43a9cbdf` | `6f8f759d314d97b41a6d0ad35a26a5cce475cc4c40d7ccf06f729668c8f15b3b` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java:365](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L365) | `834b4155232222347220e47139a502ee43a9cbdf` | `6f8f759d314d97b41a6d0ad35a26a5cce475cc4c40d7ccf06f729668c8f15b3b` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java:28](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28) | `834b4155232222347220e47139a502ee43a9cbdf` | `548150730664b0417dcc115ede889b74536a207938a2912e7da2231d6184b41e` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java:87](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L87) | `834b4155232222347220e47139a502ee43a9cbdf` | `c5cb0cb4a7a00663deaaa169837cd607bbaf35f8bf3eda04ffbe951b246d06af` |
| [repos/ui/mfe-base/src/components/Survey/common/useController.ts:21](../../../repos/ui/mfe-base/src/components/Survey/common/useController.ts#L21) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `0a4da02b278358476a8b2396037023d4db87f6d2c1d18ee73cc3b946020fd1a4` |
| [repos/ui/mfe-base/src/components/Survey/index.tsx:24](../../../repos/ui/mfe-base/src/components/Survey/index.tsx#L24) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `0be1b4364773a4a7830ebd453d84965011c8859dafcb261e2b5eefcc5d5ecc59` |
| [repos/ui/mfe-base/src/components/Timeout/common/useController.ts:25](../../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `d1e40e3d9c804870b33c239908024e3faab9c2e185cad3b1866a950cd0976bb8` |
| [repos/ui/mfe-base/src/components/Timeout/index.tsx:16](../../../repos/ui/mfe-base/src/components/Timeout/index.tsx#L16) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `e1b53e638523ae42786277503581c96fe197e54218a04c48dbc312badb0356c2` |
| [repos/ui/mfe-base/src/hooks/service/config.ts:6](../../../repos/ui/mfe-base/src/hooks/service/config.ts#L6) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `f3856b594a5930ee9f66e28e91e4a345873850f501b8768315a8e7c9ae889266` |
| [repos/ui/mfe-base/src/hooks/service/index.ts:37](../../../repos/ui/mfe-base/src/hooks/service/index.ts#L37) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `2ca3cabee0e457fbf4032ee4dfb3952ad3e352f11016c17e60fa108747adacbc` |
| [repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts:82](../../../repos/ui/mfe-base/src/hooks/service/refreshToken.test.ts#L82) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `7e5ba4d16b487e4479e83139280fc11c9463478f99aa7f5d3e7552e93b67bd20` |
| [repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts:6](../../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `9e49eeb3288a4b574b7eee1c5e90462a34c6bd794bd4965f06899942791f00e3` |
| [repos/ui/mfe-base/src/hooks/service/util/extend.ts:8](../../../repos/ui/mfe-base/src/hooks/service/util/extend.ts#L8) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `d936faf947274dbb6c2c7157eb0872c1b165e404fabf82851851ec8bfa823669` |
| [repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts:25](../../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L25) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `4f7aa44caa1f969e6f4a6a877330278710508a8b5af9c85046a39a3ad4e91a9a` |
| [repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts:18](../../../repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts#L18) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `ed3a4cbd70d4d23390534b11fb8cae1fde9b0e82ad340464a7f26a9582d9c21d` |
| [repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx:215](../../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L215) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `f316ac6a98e7d3bd8c4ae3417080c43c5cbec76b8f1bb9349ac8697ea45e72ac` |
| [repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx:510](../../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L510) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `f316ac6a98e7d3bd8c4ae3417080c43c5cbec76b8f1bb9349ac8697ea45e72ac` |
| [repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx:572](../../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L572) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `f316ac6a98e7d3bd8c4ae3417080c43c5cbec76b8f1bb9349ac8697ea45e72ac` |
| [repos/ui/mfe-base/src/pages/Home/common/useController.ts:60](../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L60) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `1b500b9f6ad3ad755a98a4cd912613baf737a4ff97a048e0d7abd773d3dacfbb` |
| [repos/ui/mfe-base/src/pages/Home/common/useController.ts:90](../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L90) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `1b500b9f6ad3ad755a98a4cd912613baf737a4ff97a048e0d7abd773d3dacfbb` |
| [repos/ui/mfe-base/src/pages/Home/common/useController.ts:104](../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L104) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `1b500b9f6ad3ad755a98a4cd912613baf737a4ff97a048e0d7abd773d3dacfbb` |
| [repos/ui/mfe-base/src/pages/Login/common/useController.ts:20](../../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L20) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `5e97ec2a4065cbef8ef9033b326bc7e9c9dfdbb038656f22fecbbf90a62e5dfb` |
| [repos/ui/mfe-base/src/pages/Login/common/useController.ts:38](../../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L38) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `5e97ec2a4065cbef8ef9033b326bc7e9c9dfdbb038656f22fecbbf90a62e5dfb` |
| [repos/ui/mfe-base/src/pages/Login/index.tsx:43](../../../repos/ui/mfe-base/src/pages/Login/index.tsx#L43) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `c20f1cad91ab20560a141d1099d245ccb26634888d90336cb4d186bd5960b37f` |
| [repos/ui/mfe-base/src/services/index.ts:20](../../../repos/ui/mfe-base/src/services/index.ts#L20) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `dd7a772b8b6f69266bd6d7e498635268920c749036548d5f2858252d011ed118` |
| [repos/ui/mfe-base/src/utils/common.ts:50](../../../repos/ui/mfe-base/src/utils/common.ts#L50) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `93d6fb57f00f656117c994868399f2cd39750239f6679f78e14b0f95c6e8d764` |
| [repos/ui/mfe-base/src/utils/common.ts:134](../../../repos/ui/mfe-base/src/utils/common.ts#L134) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `93d6fb57f00f656117c994868399f2cd39750239f6679f78e14b0f95c6e8d764` |
| [repos/ui/mfe-base/src/utils/login.ts:65](../../../repos/ui/mfe-base/src/utils/login.ts#L65) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `364c29cab3c107b14e2a914e27c38bd7073a271811c67071fa8d8f1bed738730` |
| [repos/ui/mfe-base/src/utils/login.ts:141](../../../repos/ui/mfe-base/src/utils/login.ts#L141) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `364c29cab3c107b14e2a914e27c38bd7073a271811c67071fa8d8f1bed738730` |

## Handoff limits

The [canonical catalog](../test-cases.md) defines these cases. It is not an executable test suite.
Assertions classified IMPLEMENTATION describe expected source behavior. They do not establish approved business intent.
Assertions classified PROPOSED need an owner decision before acceptance. Their fixture values do not create business limits.
External providers, deployed service bindings, effective settings, supported browsers, and test accounts remain unproved.
Use isolated test data before execution. Preserve each completed execution under the owning task.
