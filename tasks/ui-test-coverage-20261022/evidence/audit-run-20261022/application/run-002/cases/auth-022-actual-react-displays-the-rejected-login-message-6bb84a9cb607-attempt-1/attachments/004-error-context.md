# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: login-environment.spec.ts >> AUTH-022 actual React displays the rejected-login message
- Location: e2e/audit-specs/login-environment.spec.ts:153:1

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator: getByTestId('MicroWebUI_base_snackbar').getByRole('alert')
Expected: "Invalid username and password combination or SSO service is unavailable."
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
          - textbox "Enter Password" [ref=e25]: WrongPass
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
      - generic [ref=e48]: Invalid username and password combination or SSO service is unavailable.
    - button "Close" [ref=e50] [cursor=pointer]
```

# Test source

```ts
  62  | async function fillValid(login: LoginPage): Promise<void> {
  63  |   await login.fillUsername(credentials.username);
  64  |   await login.fillPassword(credentials.password);
  65  | }
  66  | 
  67  | async function rejected(route: Route): Promise<void> {
  68  |   await route.fulfill({ status: 401, contentType: 'application/json',
  69  |     body: JSON.stringify({ message: 'AuthenticationException' }) });
  70  | }
  71  | 
  72  | /** Preserve the real hostname decision while fetching every application byte from localhost. */
  73  | async function openEnvironment(page: Page, hostname: string, parameter?: string): Promise<LoginPage> {
  74  |   const local = new URL(localBase);
  75  |   if (hostname !== 'localhost') {
  76  |     await page.route('**/*', async route => {
  77  |       const url = new URL(route.request().url());
  78  |       if (url.hostname === hostname) {
  79  |         const response = await route.fetch({ url: `${local.origin}${url.pathname}${url.search}`, maxRedirects: 0 });
  80  |         await route.fulfill({ response });
  81  |       } else if (['localhost', '127.0.0.1', '[::1]'].includes(url.hostname)) await route.continue();
  82  |       else await route.abort('blockedbyclient');
  83  |     });
  84  |   }
  85  |   const query = parameter === undefined ? '' : `?show_normal_login=${encodeURIComponent(parameter)}`;
  86  |   await page.goto(`http://${hostname}:${local.port}/${query}`);
  87  |   const login = new LoginPage(page, localPrefix);
  88  |   await login.expectVisible();
  89  |   return login;
  90  | }
  91  | 
  92  | const environments = [
  93  |   { id: 'AUTH-001', environment: 'LOCAL', hostname: 'localhost', visible: true },
  94  |   { id: 'AUTH-002', environment: 'DEV', hostname: 'fmo-mfe-dev.uk.dev.net', visible: true },
  95  |   { id: 'AUTH-003', environment: 'SIT', hostname: 'ratan-aws-sit-ns4-fmo-mfe.ir.standardchartered.com', visible: true },
  96  |   { id: 'AUTH-004', environment: 'UAT', hostname: 'fmo-mfe.uk.dev.net', visible: true },
  97  |   { id: 'AUTH-005', environment: 'PRE-PROD', hostname: 'fmo-mfe-preprod.pi.dev.net', visible: true },
  98  |   { id: 'AUTH-006', environment: 'PROD', hostname: 'audit-prod.invalid', visible: false },
  99  |   { id: 'AUTH-007', environment: 'PROD', hostname: 'audit-prod.invalid', parameter: 'Y', visible: true },
  100 |   { id: 'AUTH-008', environment: 'PROD', hostname: 'audit-prod.invalid', parameter: 'y', visible: true },
  101 |   { id: 'AUTH-009', environment: 'PROD', hostname: 'audit-prod.invalid', parameter: 'N', visible: false },
  102 |   { id: 'AUTH-010', environment: 'PROD', hostname: 'audit-prod.invalid', parameter: 'true', visible: false },
  103 |   { id: 'AUTH-011', environment: 'PROD', hostname: 'audit-prod.invalid', parameter: '1', visible: false },
  104 |   { id: 'AUTH-012', environment: 'PROD', hostname: 'audit-prod.invalid', parameter: '', visible: false },
  105 | ];
  106 | 
  107 | for (const setting of environments) {
  108 |   test(`${setting.id} actual React ${setting.environment} credential visibility ${setting.parameter ?? 'without parameter'}`, async ({ page, audit }) => {
  109 |     await canonical(audit, setting.id, ['The hostname is a local route proxy. No deployed environment was contacted.']);
  110 |     const login = await openEnvironment(page, setting.hostname, setting.parameter);
  111 |     await audit.capture('entry-page', `The actual React entry page for ${setting.environment}.`, reference(setting.id));
  112 |     await expectCredentials(login, setting.visible);
  113 |     if (setting.id === 'AUTH-001' || !setting.visible) await expect(login.ssoLink).toBeVisible();
  114 |     if (setting.id === 'AUTH-001') await login.expectPasswordMasked();
  115 |     await audit.record('environment-observation', { hostname: await page.evaluate(() => location.hostname),
  116 |       expectedEnvironment: setting.environment, parameter: setting.parameter ?? null,
  117 |       credentialsVisible: setting.visible, allNonlocalRequestsInterceptedOrBlocked: true });
  118 |     await audit.capture('asserted-entry-state', 'The credential controls have the canonical visibility state.', reference(setting.id));
  119 |   });
  120 | }
  121 | 
  122 | const incomplete = [
  123 |   { id: 'AUTH-013', username: '', password: credentials.password },
  124 |   { id: 'AUTH-014', username: credentials.username, password: '' },
  125 |   { id: 'AUTH-015', username: '', password: '' },
  126 |   { id: 'AUTH-021', username: '   ', password: '   ' },
  127 | ];
  128 | for (const input of incomplete) {
  129 |   test(`${input.id} actual React prevents incomplete credential submission`, async ({ page, audit }) => {
  130 |     await canonical(audit, input.id);
  131 |     const requests: { method: string; pathname: string }[] = [];
  132 |     page.on('request', request => {
  133 |       if (request.method() === 'POST' && new URL(request.url()).pathname === loginPath)
  134 |         requests.push({ method: 'POST', pathname: loginPath });
  135 |     });
  136 |     await page.route(`**${loginPath}`, route => route.fulfill({ status: 400, body: '' }));
  137 |     const login = await openLogin(page);
  138 |     await audit.capture('login-ready', 'The LOCAL login page is visible before credential input.', reference(input.id));
  139 |     await login.fillUsername(input.username);
  140 |     await login.fillPassword(input.password);
  141 |     await audit.capture('input-ready', 'The canonical incomplete input is present before submission.', reference(input.id));
  142 |     await login.clickSignInButton();
  143 |     await expectCredentials(login);
  144 |     // The click and two animation frames complete the synchronous React submission handler.
  145 |     await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  146 |     await audit.record('credential-request-observation', { requests, count: requests.length,
  147 |       boundary: 'From page creation through the completed click handler and two animation frames.' });
  148 |     expect(requests).toHaveLength(0);
  149 |     await audit.capture('submission-prevented', 'The sign-in controls remain visible after the incomplete submission.', reference(input.id));
  150 |   });
  151 | }
  152 | 
  153 | test('AUTH-022 actual React displays the rejected-login message', async ({ page, audit }) => {
  154 |   await canonical(audit, 'AUTH-022');
  155 |   await page.route(`**${loginPath}`, rejected);
  156 |   const login = await openLogin(page);
  157 |   await audit.capture('login-ready', 'The LOCAL login page is visible.', reference('AUTH-022'));
  158 |   await login.fillUsername(credentials.username);
  159 |   await login.fillPassword('WrongPass');
  160 |   await login.clickSignInButton();
  161 |   await expectCredentials(login);
> 162 |   await expect(errorAlert(page)).toHaveText(rejectedMessage);
      |                                  ^ Error: expect(locator).toHaveText(expected) failed
  163 |   await audit.capture('rejected-login', 'The notification displays the exact canonical authentication error.', reference('AUTH-022'));
  164 | });
  165 | 
  166 | test('AUTH-023 actual React recovers after an invalid password', async ({ page, audit }) => {
  167 |   await canonical(audit, 'AUTH-023', ['WS-A is seeded in local browser workspace storage.']);
  168 |   await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
  169 |   let submissions = 0;
  170 |   await page.route(`**${loginPath}`, async route => {
  171 |     submissions += 1;
  172 |     if (submissions === 1) await rejected(route);
  173 |     else await acceptedLogin(route);
  174 |   });
  175 |   const login = await openLogin(page);
  176 |   await audit.capture('login-ready', 'The LOCAL login page is visible.', reference('AUTH-023'));
  177 |   await login.fillUsername(credentials.username);
  178 |   await login.fillPassword('WrongPass');
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
```