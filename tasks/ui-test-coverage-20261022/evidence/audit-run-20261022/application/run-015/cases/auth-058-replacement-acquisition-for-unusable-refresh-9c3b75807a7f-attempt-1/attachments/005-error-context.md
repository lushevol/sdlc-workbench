# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-session-expanded.spec.ts >> AUTH-058 replacement acquisition for unusable refresh
- Location: e2e/audit-specs/auth-session-expanded.spec.ts:62:3

# Error details

```
Error: expect(locator).toHaveValue(expected) failed

Locator: getByTestId('MicroWebUI_base_home').getByRole('tablist', { name: 'workspaces', exact: true, includeHidden: true }).getByTestId('workspaces-tab-WS-A').getByRole('textbox', { name: 'Workspace Name', exact: true, includeHidden: true })
Expected: "WS-A"
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toHaveValue" getByTestId('MicroWebUI_base_home').getByRole('tablist', { name: 'workspaces', exact: true, includeHidden: true }).getByTestId('workspaces-tab-WS-A').getByRole('textbox', { name: 'Workspace Name', exact: true, includeHidden: true }) with timeout 5000ms
  - waiting for getByTestId('MicroWebUI_base_home').getByRole('tablist', { name: 'workspaces', exact: true, includeHidden: true }).getByTestId('workspaces-tab-WS-A').getByRole('textbox', { name: 'Workspace Name', exact: true, includeHidden: true })

```

```yaml
- main:
  - heading "Sign In" [level=3]
  - text: Username
  - textbox "Enter Username"
  - text: Password
  - textbox "Enter Password"
  - button "Sign In"
  - separator
  - link "Sign In With SSO":
    - /url: https://login.microsoftonline.com/cd823f6b-31c5-4241-b504-3707cbc03fb7/oauth2/v2.0/authorize?client_id=80c8b904-1b64-443b-a651-7548764d534d&response_type=code&redirect_uri=http://localhost:8128/mfa/callback&response_mode=query&scope=openid+profile+offline_access+email
- main:
  - tabpanel:
    - heading "Markets Operations One" [level=2]
    - paragraph: Markets Operations One Portal (MO1) is a single, evolving workspace for Operations processing, integrating post-trade applications, and progressively delivering a more connected, intelligent, and efficient processing.
  - tablist "login tabs":
    - tab "login-tabpanel" [selected]
```

# Test source

```ts
  31  | export async function visibility(page: Page, state: 'hidden' | 'visible') {
  32  |   await page.evaluate(state => { Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => state }); document.dispatchEvent(new Event('visibilitychange')); }, state);
  33  | }
  34  | export async function at(page: Page, offsetMs: number, jump = false) {
  35  |   const remaining = T + offsetMs - await page.evaluate(() => Date.now());
  36  |   expect(remaining).toBeGreaterThanOrEqual(0);
  37  |   if (jump) await page.clock.fastForward(remaining); else await page.clock.runFor(remaining);
  38  |   expect(await page.evaluate(() => Date.now())).toBe(T + offsetMs);
  39  | }
  40  | export async function rotate(page: Page, value: string) {
  41  |   await page.evaluate(async value => { (await (window as unknown as SystemWindow).System.import('@fm/base')).LoginUtil.setAuthorization(value); }, value);
  42  |   await expect.poll(() => equalsToken(page, 'token', value)).toBe(true);
  43  | }
  44  | export type SessionOptions = { accessExpires?: number; refreshExpires?: number; refreshValue?: string; acquisitionFails?: boolean };
  45  | export async function sessionSetup(page: Page, audit: AuditCapture, options: SessionOptions = {}) {
  46  |   await blockExternal(page); await page.routeWebSocket('**/*', socket => socket.close());
  47  |   const accessA = sessionToken(options.accessExpires ?? 900, 'A');
  48  |   const refreshR = options.refreshValue ?? (options.refreshExpires === undefined ? undefined : sessionToken(options.refreshExpires, 'R'));
  49  |   const requests: { endpoint: string; time: number; accessMatchesA: boolean; accessMatchesB: boolean; refreshMatchesR: boolean }[] = [];
  50  |   const acquisition: Route[] = [], relogin: Route[] = [];
  51  |   const control = { holdAcquisition: false, acquisitionError: '', failAcquisition: Boolean(options.acquisitionFails), holdRelogin: true, reloginError: '', extendAccess: sessionToken(1500, 'B') };
  52  |   await page.addInitScript(({ access, workspaces }) => { localStorage.setItem('SET_TOKEN', access); sessionStorage.setItem('SET_TOKEN', access);
  53  |     localStorage.setItem('SET_USER', JSON.stringify({ sub: 'user-a', userId: 'user-a', fullName: 'Audit User A' }));
  54  |     localStorage.setItem('SET_WORKSPACES', JSON.stringify(workspaces)); }, { access: accessA, workspaces: [workspace('WS-A', 'WS-A')] });
  55  |   await page.clock.install({ time: new Date(T - 60000) });
  56  |   await page.route('**/api/**', async route => {
  57  |     const path = new URL(route.request().url()).pathname;
  58  |     if (!path.startsWith('/api/auth/v2/sso/')) { await route.fulfill({ status: 200, json: {} }); return; }
  59  |     const endpoint = path.split('/').at(-1)!;
  60  |     const body = route.request().postDataJSON() as { singleUIAuthorization?: string } | null;
  61  |     requests.push({ endpoint, time: await page.evaluate(() => Date.now()), accessMatchesA: body?.singleUIAuthorization === accessA, accessMatchesB: body?.singleUIAuthorization === sessionToken(1200, 'B'), refreshMatchesR: route.request().headers()['single-ui-refresh'] === refreshR });
  62  |     if (endpoint === 'validate') await route.fulfill({ status: 200, headers: { 'single-ui-authorization': accessA }, json: { result: true, drawers: [], entities: [], userInfo: JSON.stringify({ sub: 'user-a', fullName: 'Audit User A' }) } });
  63  |     else if (endpoint === 'refreshtoken') {
  64  |       if (control.acquisitionError === 'Network Error') await route.abort('failed');
  65  |       else if (control.holdAcquisition) acquisition.push(route);
  66  |       else if (control.failAcquisition) await route.fulfill({ status: 503, body: '' });
  67  |       else await route.fulfill({ status: 200, headers: { 'single-ui-refresh': refreshR ?? sessionToken(13524, 'R') }, json: { result: true } });
  68  |     } else if (endpoint === 'relogin') {
  69  |       if (control.reloginError === 'Network Error') await route.abort('failed');
  70  |       else if (control.reloginError) await route.fulfill({ status: 401, json: { message: control.reloginError } });
  71  |       else relogin.push(route);
  72  |     } else if (endpoint === 'extend') await route.fulfill({ status: 200, headers: { 'single-ui-authorization': control.extendAccess }, json: { result: true } });
  73  |     else await route.fulfill({ status: 200, json: { result: true } });
  74  |   });
  75  |   await page.goto(`${localBase}/?show_normal_login=Y`);
  76  |   const portal = new PortalPage(page, localPrefix), login = new LoginPage(page, localPrefix);
  77  |   await portal.expectVisible(); await portal.expectWorkspaceTabVisible('WS-A');
  78  |   if (refreshR !== undefined) {
  79  |     await page.evaluate(async () => { await (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.getRefreshToken(); });
  80  |     await expect.poll(() => equalsToken(page, 'refreshToken', refreshR)).toBe(true);
  81  |   }
  82  |   await page.clock.pauseAt(new Date(T)); requests.length = 0;
  83  |   await audit.record('session-fixture', { time: new Date(T).toISOString(), accessExpires: options.accessExpires ?? 900,
  84  |     refreshExpires: options.refreshExpires ?? null, refreshFixture: refreshR ? 'PRESENT_UNSIGNED_BROWSER_ONLY' : 'ABSENT',
  85  |     limits: ['Controlled clock and visibility adapter. No natural suspension or real credential acceptance is measured.'] });
  86  |   return { portal, login, accessA, refreshR, requests, acquisition, relogin, control, count: (endpoint: string) => requests.filter(x => x.endpoint === endpoint).length,
  87  |     acquire: () => page.evaluate(async () => { await (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.getRefreshToken(); }),
  88  |     startAcquire: () => page.evaluate(async () => { void (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.getRefreshToken(); }),
  89  |     acceptAcquisition: async (value = refreshR ?? sessionToken(13524, 'R')) => { for (const route of acquisition.splice(0)) await route.fulfill({ status: 200, headers: { 'single-ui-refresh': value }, json: { result: true } }); },
  90  |     acceptRelogin: async (value = sessionToken(900, 'B')) => { for (const route of relogin.splice(0)) await route.fulfill({ status: 200, headers: { 'single-ui-authorization': value }, json: { result: true, entities: [], userInfo: JSON.stringify({ sub: 'user-a', fullName: 'Audit User A' }) } }); },
  91  |   };
  92  | }
  93  | export type Session = Awaited<ReturnType<typeof sessionSetup>>;
  94  | export async function commonAssertion(page: Page, s: Session, text: string): Promise<boolean> {
  95  |   const timeout = s.portal.sessionTimeoutDialog;
  96  |   const count = /records exactly (\d+) new POST requests to "\/api\/auth\/v2\/sso\/(\w+)"/.exec(text);
  97  |   if (count) { await expect.poll(() => s.count(count[2])).toBe(Number(count[1])); return true; }
  98  |   if (text.includes('tab labelled "WS-A"') && text.includes('visible')) { await s.portal.expectWorkspaceTabVisible('WS-A'); return true; }
  99  |   if (text.includes('tablist named "workspaces"') && text.includes('absent')) { await expect(s.portal.workspaceList).toHaveCount(0); return true; }
  100 |   if (text.includes('textbox with placeholder "Enter Username"') && text.includes('visible')) { await expect(s.login.usernameInput).toBeVisible(); return true; }
  101 |   if (text.includes('text input with placeholder "Enter Password"') && text.includes('visible')) { await expect(s.login.passwordInput).toBeVisible(); return true; }
  102 |   if (text.includes('button labelled "Sign In"') && text.includes('visible')) { await expect(s.login.signInButton).toBeVisible(); return true; }
  103 |   if (text.includes('dialog named "Your session has been expired"') && text.includes('absent')) { await timeout.expectAbsent(); return true; }
  104 |   if (text.includes('button labelled "Extend"') && text.includes('disabled')) { await expect(timeout.extendButton).toBeDisabled(); return true; }
  105 |   if (text.includes('button labelled "Extend"') && text.includes('enabled')) { await expect(timeout.extendButton).toBeEnabled(); return true; }
  106 |   if (text.includes('button labelled "Extend"') && text.includes('visible')) { await expect(timeout.extendButton).toBeVisible(); return true; }
  107 |   if (text.includes('button labelled "Logout"') && text.includes('enabled')) { await expect(timeout.logoutButton).toBeEnabled(); return true; }
  108 |   if (text.includes('button labelled "Logout"') && text.includes('visible')) { await expect(timeout.logoutButton).toBeVisible(); return true; }
  109 |   if (text.includes('dialog named "Your session has been expired"') && text.includes('visible')) { await timeout.expectVisible(); return true; }
  110 |   if (text.includes('isOnLogout=true')) { await expect.poll(async () => (await observe(page)).isOnLogout).toBe(true); return true; }
  111 |   if (text.includes('installed access credential') && (text.includes('absent') || text.includes('remains absent'))) { expect((await observe(page)).accessPresent).toBe(false); return true; }
  112 |   if (text.includes('installed refresh credential remains R')) { expect(await equalsToken(page, 'refreshToken', s.refreshR)).toBe(true); return true; }
  113 |   if (text.includes('alert in the portal notification area displays exactly ')) {
  114 |     const expected = text.split('displays exactly ')[1].replace(/^"|"$/g, '');
  115 |     await expect(page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toHaveText(expected); return true;
  116 |   }
  117 |   return false;
  118 | }
  119 | 
  120 | export async function runSessionCase(page: Page, audit: AuditCapture, id: string, options: SessionOptions,
  121 |   operations: Partial<Record<number, (s: Session) => Promise<unknown>>> = {}) {
  122 |   const steps = await audit.defineCase(id);
  123 |   let s!: Session;
  124 |   for (const step of steps) {
  125 |     await audit.step(step.number, async () => {
  126 |       if (step.number === 1) { s = await sessionSetup(page, audit, options); return; }
  127 |       if (operations[step.number]) { await operations[step.number]!(s); return; }
  128 |       if (step.number === 2 && step.text.includes('selected fixture tab')) {
  129 |         const tabs = s.portal.root.getByRole('tablist', { name: 'workspaces', exact: true, includeHidden: true });
  130 |         const name = tabs.getByTestId('workspaces-tab-WS-A').getByRole('textbox', { name: 'Workspace Name', exact: true, includeHidden: true });
> 131 |         await expect(name).toHaveValue('WS-A'); return;
      |                            ^ Error: expect(locator).toHaveValue(expected) failed
  132 |       }
  133 |       if (step.number === 3 && (step.text.startsWith('access A ') || step.text.startsWith('the browser '))) {
  134 |         expect(await equalsToken(page, 'token', s.accessA)).toBe(true);
  135 |         expect(await equalsToken(page, 'refreshToken', s.refreshR)).toBe(true); return;
  136 |       }
  137 |       if (await commonAssertion(page, s, step.text)) return;
  138 |       throw new Error(`No executable binding for ${id} step ${step.number}: ${step.text}`);
  139 |     });
  140 |   }
  141 |   await audit.record('session-observations', { requests: s.requests, state: await observe(page) });
  142 | }
  143 | 
```