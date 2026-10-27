### FOUR-AC4-BROWSER

Title: retain the portal through four controlled hours of accepted activity.
Level: controlled browser integration with the actual MFE, root composition, DOM, store, and HTTP interceptors.
Intent: [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria), requirement candidate version 5.
Actor: Playwright drives headless Edge. The fixture controls browser time and authentication responses.
Setup: perform local sign-in through the actual form and retain its noncredential response fields.
Return synthetic access credentials valid for fifteen minutes and initial refresh credentials valid for two hours.
The response fixture replaces refresh credentials after their expiry while current access remains usable.
The driver emits trusted mouse movement every ten controlled minutes and permits the existing five-second debounce.
All runtime source remains unchanged. Token verification and live identity-provider behavior are outside this controlled case.

1. Sign in through the rendered local portal form.
2. Pause the installed browser clock after setup.
3. Seed initial refresh through the exported shared service and its actual response interceptor.
4. Advance ten controlled minutes before each trusted mouse movement.
5. Run the debounce clock and wait for the successful extension response.
6. Continue until the controlled clock reaches exactly four hours from the assertion baseline.
7. Inspect authentication, prompt transitions, navigation, refresh replacement, and successful renewal counts.

```gherkin
Feature: Preserve accepted activity across elapsed session duration
  Scenario: FOUR-AC4-BROWSER
    Given the rendered portal has fifteen-minute access and two-hour initial refresh credentials
    And authentication responses issue usable credentials for the current controlled clock
    When accepted trusted mouse activity renews access before every access deadline
    And the controlled browser clock advances through exactly four hours
    Then each activity cycle completes a successful extension
    And current access remains usable
    And the initial refresh token expires within the interval
    And the portal installs a different usable refresh token
    And the portal records zero timeout prompt openings
    And the portal records zero additional fresh-login requests
    And the portal records zero logout or manual-relogin requests
    And the portal records zero additional main-frame navigations
    And the authenticated workspace remains visible
```

Assertions and retained execution: [controlled browser evidence](evidence/four-checks-20261027/ac4-browser/).
This case establishes the declared controlled predicates. It does not establish four hours of live BFF acceptance.

