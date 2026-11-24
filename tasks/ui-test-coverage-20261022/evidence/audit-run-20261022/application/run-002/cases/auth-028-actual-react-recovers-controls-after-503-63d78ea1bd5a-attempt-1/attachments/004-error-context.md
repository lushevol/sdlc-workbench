# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: login-environment.spec.ts >> AUTH-028 actual React recovers controls after 503
- Location: e2e/audit-specs/login-environment.spec.ts:261:3

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator: getByTestId('MicroWebUI_base_snackbar').getByRole('alert')
Expected: "/api/auth/v2/sso/login : Request failed with status code 503"
Error: strict mode violation: getByTestId('MicroWebUI_base_snackbar').getByRole('alert') resolved to 2 elements:
    1) <div role="alert" direction="up" class="MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation6 MuiAlert-root MuiAlert-colorError MuiAlert-standardError MuiAlert-standard css-rgg0t8-MuiPaper-root-MuiAlert-root">…</div> aka getByRole('alert').first()
    2) <div role="alert" class="MuiPaper-root MuiPaper-elevation MuiPaper-elevation6 MuiSnackbarContent-root css-11hfw37-MuiPaper-root-MuiSnackbarContent-root">…</div> aka getByRole('alert').nth(1)

Call log:
  - Expect "toHaveText" getByTestId('MicroWebUI_base_snackbar').getByRole('alert') with timeout 5000ms
  - waiting for getByTestId('MicroWebUI_base_snackbar').getByRole('alert')

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - generic [ref=e5]:
    - main [ref=e7]:
      - heading "Sign In" [level=3] [ref=e8]
      - generic [ref=e9]:
        - generic [ref=e10]:
          - generic [ref=e11]: Username
          - textbox "Enter Username" [ref=e17]: user-a
        - generic [ref=e18]:
          - generic [ref=e19]: Password
          - textbox "Enter Password" [ref=e25]: FixturePass1!
        - button "Sign In" [ref=e26] [cursor=pointer]
        - separator [ref=e27]
      - link "Sign In With SSO" [ref=e29] [cursor=pointer]:
        - /url: https://login.microsoftonline.com/cd823f6b-31c5-4241-b504-3707cbc03fb7/oauth2/v2.0/authorize?client_id=80c8b904-1b64-443b-a651-7548764d534d&response_type=code&redirect_uri=http://localhost:8128/mfa/callback&response_mode=query&scope=openid+profile+offline_access+email
    - main [ref=e31]:
      - tabpanel [ref=e32]:
        - generic [ref=e33]:
          - heading "Markets Operations One" [level=2] [ref=e34]
          - paragraph [ref=e35]: Markets Operations One Portal (MO1) is a single, evolving workspace for Operations processing, integrating post-trade applications, and progressively delivering a more connected, intelligent, and efficient processing.
      - tablist "login tabs" [ref=e39]:
        - tab "login-tabpanel" [selected] [ref=e40] [cursor=pointer]
  - alert [ref=e42]:
    - alert [ref=e47]:
      - generic [ref=e48]: "/api/auth/v2/sso/login : Request failed with status code 503"
    - button "Close" [ref=e50] [cursor=pointer]
```

# Test source

```ts
  179 |   await login.clickSignInButton();
  180 |   await expect(errorAlert(page)).toHaveText(rejectedMessage);
  181 |   await audit.capture('first-login-rejected', 'The first login displays the canonical error.', reference('AUTH-023'));
  182 |   await login.fillPassword(credentials.password);
  183 |   await login.clickSignInButton();
  184 |   await expect(errorAlert(page).filter({ hasText: rejectedMessage })).toHaveCount(0);
  185 |   const portal = new PortalPage(page, localPrefix);
  186 |   await portal.expectVisible();
  187 |   await portal.expectWorkspaceTabVisible('WS-A');
  188 |   await audit.record('retry-observation', { submissions, fixtureResponseOrder: ['AuthenticationException', 'valid user-a data'] });
  189 |   await audit.capture('recovered-workspace', 'WS-A is visible and the rejected-login error is absent.', reference('AUTH-023'));
  190 | });
  191 | 
  192 | test('AUTH-024 actual React disables sign-in controls during a pending request', async ({ page, audit }) => {
  193 |   await canonical(audit, 'AUTH-024');
  194 |   const pending: Route[] = [];
  195 |   await page.route(`**${loginPath}`, route => { pending.push(route); });
  196 |   const login = await openLogin(page);
  197 |   await audit.capture('login-ready', 'The LOCAL login page is visible.', reference('AUTH-024'));
  198 |   await fillValid(login);
  199 |   await login.clickSignInButton();
  200 |   await expect.poll(() => pending.length).toBe(1);
  201 |   await expect(login.signInButton).toBeDisabled();
  202 |   await expect(login.signInButton.getByRole('progressbar')).toHaveCount(1);
  203 |   await expect(login.ssoLink).toHaveAttribute('aria-disabled', 'true');
  204 |   await audit.record('pending-observation', { pendingRequests: pending.length, responseReleased: false,
  205 |     ssoDisabledPredicate: 'aria-disabled=true', signInProgressIndicators: 1 });
  206 |   await audit.capture('pending-controls-disabled', 'Sign In and SSO are disabled while the credential response remains pending.', reference('AUTH-024'));
  207 | });
  208 | 
  209 | test('AUTH-025 actual React handles repeated sign-in input', async ({ page, audit }) => {
  210 |   await canonical(audit, 'AUTH-025', ['Effective transition means the local SET_TOKEN value changes from absent to present.',
  211 |     'This browser predicate does not prove one server-side session or one identity-provider transaction.']);
  212 |   test.info().annotations.push({ type: 'canonical-limit', description: 'Effective transition is scoped to local SET_TOKEN absent-to-present state.' });
  213 |   await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
  214 |   await page.addInitScript(() => {
  215 |     const state = { transitions: 0, writes: 0 };
  216 |     Object.defineProperty(window, '__auditAuthentication', { value: state });
  217 |     const original = Storage.prototype.setItem;
  218 |     Storage.prototype.setItem = function (key, value) {
  219 |       if (this === localStorage && key === 'SET_TOKEN') {
  220 |         state.writes += 1;
  221 |         if (!this.getItem(key) && value) state.transitions += 1;
  222 |       }
  223 |       return original.call(this, key, value);
  224 |     };
  225 |   });
  226 |   const pending: Route[] = [];
  227 |   let released = false;
  228 |   await page.route(`**${loginPath}`, async route => {
  229 |     if (released) await acceptedLogin(route);
  230 |     else pending.push(route);
  231 |   });
  232 |   const login = await openLogin(page);
  233 |   await audit.capture('login-ready', 'The LOCAL login page is visible.', reference('AUTH-025'));
  234 |   await fillValid(login);
  235 |   await login.usernameInput.press('Enter');
  236 |   await login.usernameInput.press('Enter');
  237 |   await expect(login.signInButton).toBeDisabled();
  238 |   const bounds = await login.signInButton.boundingBox();
  239 |   expect(bounds).not.toBeNull();
  240 |   await page.mouse.click(bounds!.x + bounds!.width / 2, bounds!.y + bounds!.height / 2);
  241 |   await audit.capture('repeated-input-pending', 'Repeated Enter and the pointer click occurred while login responses remained pending.', reference('AUTH-025'));
  242 |   released = true;
  243 |   await Promise.all(pending.map(acceptedLogin));
  244 |   const portal = new PortalPage(page, localPrefix);
  245 |   await portal.expectWorkspaceTabVisible('WS-A');
  246 |   const observations = await page.evaluate(() =>
  247 |     (window as unknown as { __auditAuthentication: { transitions: number; writes: number } }).__auditAuthentication);
  248 |   await audit.record('authentication-observation', { ...observations, credentialRequests: pending.length,
  249 |     predicate: 'SET_TOKEN absent-to-present transitions; no token values retained' });
  250 |   expect(observations.transitions).toBeLessThanOrEqual(1);
  251 |   await expect(errorAlert(page)).toHaveCount(0);
  252 |   await audit.capture('authenticated-after-repeated-input', 'WS-A is visible without an authentication error.', reference('AUTH-025'));
  253 | });
  254 | 
  255 | const failures = [
  256 |   { id: 'AUTH-026', mode: 'network', expected: 'Error happened, service is unavailable, pls check with support team: /api/auth/v2/sso/login: API request failed' },
  257 |   { id: 'AUTH-027', mode: 'timeout', expected: '/api/auth/v2/sso/login : timeout of 60000ms exceeded' },
  258 |   { id: 'AUTH-028', mode: '503', expected: '/api/auth/v2/sso/login : Request failed with status code 503' },
  259 | ];
  260 | for (const failure of failures) {
  261 |   test(`${failure.id} actual React recovers controls after ${failure.mode}`, async ({ page, audit }) => {
  262 |     if (failure.mode === 'timeout') test.setTimeout(85000);
  263 |     await canonical(audit, failure.id);
  264 |     const pending: Route[] = [];
  265 |     await page.route(`**${loginPath}`, async route => {
  266 |       if (failure.mode === 'network') await route.abort('failed');
  267 |       else if (failure.mode === '503') await route.fulfill({ status: 503, body: '' });
  268 |       else pending.push(route);
  269 |     });
  270 |     const login = await openLogin(page);
  271 |     await audit.capture('login-ready', 'The LOCAL login page is visible before the transport failure.', reference(failure.id));
  272 |     await fillValid(login);
  273 |     const started = Date.now();
  274 |     await login.clickSignInButton();
  275 |     if (failure.mode === 'timeout') {
  276 |       await expect(login.signInButton).toBeDisabled();
  277 |       await audit.capture('request-pending', 'The credential request is pending before its native Axios timeout.', reference(failure.id));
  278 |     }
> 279 |     await expect(errorAlert(page)).toHaveText(failure.expected, { timeout: failure.mode === 'timeout' ? 70000 : 5000 });
      |                                    ^ Error: expect(locator).toHaveText(expected) failed
  280 |     await expectCredentials(login);
  281 |     await expect(login.signInButton).toBeEnabled();
  282 |     await expect(login.signInButton.getByRole('progressbar')).toHaveCount(0);
  283 |     await audit.record('transport-failure-observation', { mode: failure.mode, elapsedMs: Date.now() - started,
  284 |       responseBody: null, exactError: failure.expected, nativeAxiosTimeoutMs: failure.mode === 'timeout' ? 60000 : null });
  285 |     await audit.capture('transport-failure-recovered', 'Sign In is enabled without a progress indicator and the exact error is visible.', reference(failure.id));
  286 |   });
  287 | }
  288 | 
```