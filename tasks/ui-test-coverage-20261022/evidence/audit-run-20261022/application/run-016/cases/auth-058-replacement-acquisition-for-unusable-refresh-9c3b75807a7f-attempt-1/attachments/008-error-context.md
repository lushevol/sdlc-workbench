# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-session-expanded.spec.ts >> AUTH-058 replacement acquisition for unusable refresh
- Location: e2e/audit-specs/auth-session-expanded.spec.ts:62:3

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: 1
Received: 0

Call Log:
- Timeout 5000ms exceeded while waiting on the predicate
```

# Page snapshot

```yaml
- generic [ref=e4]:
  - generic [ref=e7]:
    - img "Markets Operations One logo" [ref=e9]
    - generic [ref=e10]:
      - generic [ref=e11] [cursor=pointer]:
        - img "new tile" [ref=e13]
        - generic [ref=e14]: New Tile
      - generic [ref=e15]:
        - img "dark" [ref=e17]
        - generic [ref=e19]:
          - text: dark
          - checkbox "Theme Switch" [ref=e22] [cursor=pointer]
      - group [ref=e26]:
        - generic [ref=e27]: 00:00 UTC
        - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
      - button "User Profiles" [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button "Share Feedback" [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist "workspaces" [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region "WS-A" [ref=e48]:
          - textbox "Workspace Name" [ref=e52]: WS-A
      - button "Add Workspace" [ref=e54] [cursor=pointer]
    - tabpanel [ref=e59]:
      - generic [ref=e63]:
        - paragraph [ref=e65]: Start customizing your workspace
        - paragraph [ref=e66]: find out what workspace preference options you have and how those options work.
        - button [ref=e67] [cursor=pointer]
```

# Test source

```ts
  1   | import type { Page, Route } from '@playwright/test';
  2   | import { expect, type AuditCapture } from './audit-fixture.js';
  3   | import { blockExternal, localBase, localPrefix, workspace } from './local-app.js';
  4   | import { PortalPage } from '../pages/portal.page.js';
  5   | import { LoginPage } from '../pages/login.page.js';
  6   | 
  7   | export const T = Date.parse('2030-01-01T00:00:00.000Z');
  8   | export type SessionStore = { token?: string; refreshToken?: string; expiredIn?: number; isOnLogout?: boolean; isLoading?: boolean; entities?: unknown[] };
  9   | export type Mfe = { Hooks: { getHooks(): { store: SessionStore } };
  10  |   Service: { getRefreshToken(): Promise<void> | void; signal: { getRefreshToken?: AbortController; relogin?: AbortController };
  11  |     postService(path: string, data: unknown, config?: unknown): Promise<{data: unknown}> };
  12  |   LoginUtil: { setAuthorization(value: string): void; setRefreshToken(value: string | undefined): void };
  13  |   ExtendService: { extendToken(): void } };
  14  | export type SystemWindow = Window & { System: { import(name: string): Promise<Mfe> } };
  15  | export const tokenPayload = (payload: unknown) => {
  16  |   const encode = (value: unknown) => Buffer.from(JSON.stringify(value)).toString('base64url');
  17  |   return `Bearer ${encode({ alg: 'none', typ: 'JWT' })}.${encode(payload)}.fixture`;
  18  | };
  19  | export const sessionToken = (seconds: number, name: string) => tokenPayload({ sub: 'user-a', iat: T / 1000 - 60, exp: T / 1000 + seconds, fixture: name });
  20  | export async function observe(page: Page) {
  21  |   return page.evaluate(async () => {
  22  |     const m = await (window as unknown as SystemWindow).System.import('@fm/base');
  23  |     const s = m.Hooks.getHooks().store;
  24  |     return { now: Date.now(), accessExpiryMs: (s.expiredIn ?? 0) * 1000, accessPresent: Boolean(s.token),
  25  |       refreshPresent: Boolean(s.refreshToken), isOnLogout: Boolean(s.isOnLogout), isLoading: Boolean(s.isLoading), visibility: document.visibilityState };
  26  |   });
  27  | }
  28  | export async function equalsToken(page: Page, field: 'token' | 'refreshToken', value?: string) {
  29  |   return page.evaluate(async ({field, value}) => (await (window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store[field] === value, {field, value});
  30  | }
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
  52  |   await page.addInitScript(({ access, workspaces }) => {
  53  |     if (localStorage.getItem('_AUDIT_AUTH_SEEDED_ONCE')) return;
  54  |     localStorage.setItem('_AUDIT_AUTH_SEEDED_ONCE','true'); localStorage.setItem('SET_TOKEN', access); sessionStorage.setItem('SET_TOKEN', access);
  55  |     localStorage.setItem('SET_USER', JSON.stringify({ sub: 'user-a', userId: 'user-a', fullName: 'Audit User A' }));
  56  |     localStorage.setItem('SET_WORKSPACES', JSON.stringify(workspaces)); }, { access: accessA, workspaces: [workspace('WS-A', 'WS-A')] });
  57  |   await page.clock.install({ time: new Date(T - 60000) });
  58  |   await page.route('**/api/**', async route => {
  59  |     const path = new URL(route.request().url()).pathname;
  60  |     if (!path.startsWith('/api/auth/v2/sso/')) { await route.fulfill({ status: 200, json: {} }); return; }
  61  |     const endpoint = path.split('/').at(-1)!;
  62  |     const body = route.request().postDataJSON() as { singleUIAuthorization?: string } | null;
  63  |     requests.push({ endpoint, time: await page.evaluate(() => Date.now()), accessMatchesA: body?.singleUIAuthorization === accessA, accessMatchesB: body?.singleUIAuthorization === sessionToken(1200, 'B'), refreshMatchesR: route.request().headers()['single-ui-refresh'] === refreshR });
  64  |     if (endpoint === 'validate') await route.fulfill({ status: 200, headers: { 'single-ui-authorization': accessA }, json: { result: true, drawers: [], entities: [], userInfo: JSON.stringify({ sub: 'user-a', fullName: 'Audit User A' }) } });
  65  |     else if (endpoint === 'refreshtoken') {
  66  |       if (control.acquisitionError === 'Network Error') await route.abort('failed');
  67  |       else if (control.holdAcquisition) acquisition.push(route);
  68  |       else if (control.failAcquisition) await route.fulfill({ status: 503, body: '' });
  69  |       else await route.fulfill({ status: 200, headers: { 'single-ui-refresh': refreshR ?? sessionToken(13524, 'R') }, json: { result: true } });
  70  |     } else if (endpoint === 'relogin') {
  71  |       if (control.reloginError === 'Network Error') await route.abort('failed');
  72  |       else if (control.reloginError) await route.fulfill({ status: 401, json: { message: control.reloginError } });
  73  |       else relogin.push(route);
  74  |     } else if (endpoint === 'extend') await route.fulfill({ status: 200, headers: { 'single-ui-authorization': control.extendAccess }, json: { result: true } });
  75  |     else await route.fulfill({ status: 200, json: { result: true } });
  76  |   });
  77  |   await page.goto(`${localBase}/?show_normal_login=Y`);
  78  |   const portal = new PortalPage(page, localPrefix), login = new LoginPage(page, localPrefix);
  79  |   await portal.expectVisible(); await portal.expectWorkspaceTabVisible('WS-A');
  80  |   if (refreshR !== undefined) {
  81  |     await page.evaluate(async () => { await (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.getRefreshToken(); });
  82  |     await expect.poll(() => equalsToken(page, 'refreshToken', refreshR)).toBe(true);
  83  |   }
  84  |   await page.clock.pauseAt(new Date(T)); requests.length = 0;
  85  |   await audit.record('session-fixture', { time: new Date(T).toISOString(), accessExpires: options.accessExpires ?? 900,
  86  |     refreshExpires: options.refreshExpires ?? null, refreshFixture: refreshR ? 'PRESENT_UNSIGNED_BROWSER_ONLY' : 'ABSENT',
  87  |     limits: ['Controlled clock and visibility adapter. No natural suspension or real credential acceptance is measured.'] });
  88  |   return { portal, login, accessA, refreshR, requests, acquisition, relogin, control, count: (endpoint: string) => requests.filter(x => x.endpoint === endpoint).length,
  89  |     acquire: () => page.evaluate(async () => { await (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.getRefreshToken(); }),
  90  |     startAcquire: () => page.evaluate(async () => { void (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.getRefreshToken(); }),
  91  |     acceptAcquisition: async (value = refreshR ?? sessionToken(13524, 'R')) => { for (const route of acquisition.splice(0)) await route.fulfill({ status: 200, headers: { 'single-ui-refresh': value }, json: { result: true } }); },
  92  |     acceptRelogin: async (value = sessionToken(900, 'B')) => { for (const route of relogin.splice(0)) await route.fulfill({ status: 200, headers: { 'single-ui-authorization': value }, json: { result: true, entities: [], userInfo: JSON.stringify({ sub: 'user-a', fullName: 'Audit User A' }) } }); },
  93  |   };
  94  | }
  95  | export type Session = Awaited<ReturnType<typeof sessionSetup>>;
  96  | export async function commonAssertion(page: Page, s: Session, text: string): Promise<boolean> {
  97  |   const timeout = s.portal.sessionTimeoutDialog;
  98  |   const count = /records exactly (\d+) new POST requests to "\/api\/auth\/v2\/sso\/(\w+)"/.exec(text);
> 99  |   if (count) { await expect.poll(() => s.count(count[2])).toBe(Number(count[1])); return true; }
      |                                                           ^ Error: expect(received).toBe(expected) // Object.is equality
  100 |   if (text.includes('tab labelled "WS-A"') && text.includes('visible')) { await s.portal.expectWorkspaceTabVisible('WS-A'); return true; }
  101 |   if (text.includes('tablist named "workspaces"') && text.includes('absent')) { await expect(s.portal.workspaceList).toHaveCount(0); return true; }
  102 |   if (text.includes('textbox with placeholder "Enter Username"') && text.includes('visible')) { await expect(s.login.usernameInput).toBeVisible(); return true; }
  103 |   if (text.includes('text input with placeholder "Enter Password"') && text.includes('visible')) { await expect(s.login.passwordInput).toBeVisible(); return true; }
  104 |   if (text.includes('button labelled "Sign In"') && text.includes('visible')) { await expect(s.login.signInButton).toBeVisible(); return true; }
  105 |   if (text.includes('dialog named "Your session has been expired"') && text.includes('absent')) { await timeout.expectAbsent(); return true; }
  106 |   if (text.includes('button labelled "Extend"') && text.includes('disabled')) { await expect(timeout.extendButton).toBeDisabled(); return true; }
  107 |   if (text.includes('button labelled "Extend"') && text.includes('enabled')) { await expect(timeout.extendButton).toBeEnabled(); return true; }
  108 |   if (text.includes('button labelled "Extend"') && text.includes('visible')) { await expect(timeout.extendButton).toBeVisible(); return true; }
  109 |   if (text.includes('button labelled "Logout"') && text.includes('enabled')) { await expect(timeout.logoutButton).toBeEnabled(); return true; }
  110 |   if (text.includes('button labelled "Logout"') && text.includes('visible')) { await expect(timeout.logoutButton).toBeVisible(); return true; }
  111 |   if (text.includes('dialog named "Your session has been expired"') && text.includes('visible')) { await timeout.expectVisible(); return true; }
  112 |   if (text.includes('isOnLogout=true')) {
  113 |     await expect.poll(async () => { await page.clock.runFor(0); return (await observe(page)).isOnLogout; }).toBe(true); return true;
  114 |   }
  115 |   if (text.includes('installed access credential') && (text.includes('absent') || text.includes('remains absent'))) { expect((await observe(page)).accessPresent).toBe(false); return true; }
  116 |   if (text.includes('installed refresh credential remains R')) { expect(await equalsToken(page, 'refreshToken', s.refreshR)).toBe(true); return true; }
  117 |   if (text.includes('alert in the portal notification area displays exactly ')) {
  118 |     const expected = text.split('displays exactly ')[1].replace(/^"|"$/g, '');
  119 |     await expect(page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toHaveText(expected); return true;
  120 |   }
  121 |   return false;
  122 | }
  123 | 
  124 | export async function runSessionCase(page: Page, audit: AuditCapture, id: string, options: SessionOptions,
  125 |   operations: Partial<Record<number, (s: Session) => Promise<unknown>>> = {}) {
  126 |   const steps = await audit.defineCase(id);
  127 |   let s!: Session;
  128 |   for (const step of steps) {
  129 |     await audit.step(step.number, async () => {
  130 |       if (step.number === 1) { s = await sessionSetup(page, audit, options); return; }
  131 |       if (operations[step.number]) { await operations[step.number]!(s); return; }
  132 |       if (step.number === 2 && step.text.includes('selected fixture tab')) {
  133 |         const tabs = s.portal.root.getByRole('tablist', { name: 'workspaces', exact: true, includeHidden: true });
  134 |         const name = tabs.getByTestId('workspaces-tab-WS-A').getByRole('textbox', { name: 'Workspace Name', exact: true, includeHidden: true });
  135 |         await expect(name).toHaveValue('WS-A'); return;
  136 |       }
  137 |       if (step.number === 3 && (step.text.startsWith('access A ') || step.text.startsWith('refresh R is valid;') || step.text.startsWith('the browser '))) {
  138 |         expect(await equalsToken(page, 'token', s.accessA)).toBe(true);
  139 |         expect(await equalsToken(page, 'refreshToken', s.refreshR)).toBe(true); return;
  140 |       }
  141 |       if (await commonAssertion(page, s, step.text)) return;
  142 |       throw new Error(`No executable binding for ${id} step ${step.number}: ${step.text}`);
  143 |     });
  144 |   }
  145 |   await audit.record('session-observations', { requests: s.requests, state: await observe(page) });
  146 | }
  147 | 
```