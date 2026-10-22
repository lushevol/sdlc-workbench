---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Session interaction example

**UNVERIFIED: Complete semantic and automation reviews before execution handoff. Owner: unknown. Current bindings do not establish this revised example's coverage.**

This maintained tooling fixture demonstrates explicit UI references and separate functional assertions.
It does not replace the [canonical E2E-04 definition](../../../tasks/portal-background-session-20261019/test-cases.md#e2e-04).
The behavior intent is continued portal access after refresh-based renewal.
The [candidate AC-6](../../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L173) defines prompt closure after successful renewal.
Its publication review remains pending.

User A means one portal account with permission to access the portal Home page.
The fixture requires expired access credentials and usable refresh credentials from the actual authentication service.
The authentication validation probe reads current `SET_TOKEN`, navigates to `/`, and observes `POST /api/auth/v2/sso/validate`.
The probe retains token hashes rather than raw credentials.
Its request comparison uses the captured `SET_TOKEN` value.
These probe actions come from the [existing assertion helper](../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/support/browser.cjs#L4).

```gherkin
Feature: Explicit session renewal interaction and authentication observations
  @SESSION-UI-EXAMPLE
  Scenario: Request renewal with the verified timeout control
    Given User A has expired portal access credentials and usable refresh credentials
    And the dialog named "Your session has been expired" is visible in the portal
    And the text "Do you want to logout or extend the session?" is visible inside the dialog named "Your session has been expired"
    When User A clicks the button labeled "Extend" inside the dialog named "Your session has been expired"
    Then the dialog named "Your session has been expired" is hidden in the portal
    And the authentication validation probe returns HTTP 200 with JSON field "result" equal to true
    And the probe request field "singleUIAuthorization" equals the captured "SET_TOKEN" value
    And the tablist named "workspaces" is visible in the portal main region
```

The [source UI](../../../repos/ui/mfe-base/src/components/Timeout/index.tsx#L16) supplies the exact dialog title, description, and button label.
The [Home source](../../../repos/ui/mfe-base/src/pages/Home/index.tsx#L60) supplies the workspace tablist scope and accessible name.
The `tablist` vocabulary extension follows the inspected MUI `Tabs` component.
Rendered role, target uniqueness, and deployed revision still require verification.

Dialog closure alone cannot establish successful renewal.
The [controller](../../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L54) closes the dialog after calling `relogin()`.
The [request helper](../../../repos/ui/mfe-base/src/hooks/service/index.ts#L89) does not return its request promise at the inspected revision.
The [authentication controller](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L252) defines validation responses.
The probe verifies portal authentication validation only.
It does not establish downstream authorization, session lifetime, or uninterrupted page state.

The [existing Robot case](../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot#L31) uses Browser JavaScript keywords.
The [existing helper](../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/support/browser.cjs#L58) also checks pending-state behavior.
That implementation is related evidence, not an inspected binding for every revised step above.
The manifest therefore omits automation bindings and records an `UNVERIFIED` review.
No browser execution occurred for this tooling fixture.

Run the source-workspace demonstration with:

```sh
ai-sdlc gherkin docs/examples/gherkin-session/session.md --manifest docs/examples/gherkin-session/manifest.json --root .
```

The expected quality state is `UNVERIFIED`.
The [negative fixture](ambiguous.md) demonstrates mandatory rule failures.
