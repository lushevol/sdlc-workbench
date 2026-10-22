# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: session-timing.spec.ts >> AUTH-083 open-dialog refresh cutoff at T+598000ms
- Location: e2e/audit-specs/session-timing.spec.ts:229:3

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: page.evaluate: Target page, context or browser has been closed
```

# Page snapshot

```yaml
- generic [ref=e1]:
  - generic [ref=e4]:
    - generic [ref=e10]:
      - generic [ref=e11] [cursor=pointer]: New Tile
      - generic [ref=e19]:
        - text: dark
        - checkbox [ref=e22] [cursor=pointer]
      - group [ref=e26]:
        - generic [ref=e27]: 00:05 UTC
        - checkbox [checked] [ref=e30] [cursor=pointer]
      - button [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button [ref=e37] [cursor=pointer]
    - main [ref=e41]:
      - tablist [ref=e45]:
        - tab [selected] [ref=e47] [cursor=pointer]:
          - region [ref=e48]:
            - textbox [ref=e52]: WS-A
        - button [ref=e54] [cursor=pointer]
      - tabpanel [ref=e59]:
        - generic [ref=e63]:
          - paragraph [ref=e65]: Start customizing your workspace
          - paragraph [ref=e66]: find out what workspace preference options you have and how those options work.
          - button [ref=e67] [cursor=pointer]: Find tile
  - dialog [ref=e73]:
    - heading "Your session has been expired" [level=2] [ref=e74]
    - paragraph [ref=e76]: Do you want to logout or extend the session?
    - generic [ref=e77]:
      - button "Extend" [active] [ref=e78] [cursor=pointer]
      - button "Logout" [ref=e79] [cursor=pointer]
```

# Test source

```ts
  1   | import { createHash } from 'node:crypto';
  2   | import { readFileSync } from 'node:fs';
  3   | import { fileURLToPath } from 'node:url';
  4   | import type { Page, Route } from '@playwright/test';
  5   | import { test, expect, type AuditCapture } from '../support/audit-fixture.js';
  6   | import { blockExternal, localBase, localPrefix, workspace } from '../support/local-app.js';
  7   | import { PortalPage } from '../pages/portal.page.js';
  8   | import { LoginPage } from '../pages/login.page.js';
  9   | 
  10  | const T = Date.parse('2030-01-01T00:00:00.000Z');
  11  | const definitionPath = 'tasks/ui-test-coverage-20261022/test-cases.md';
  12  | const root = fileURLToPath(new URL('../../', import.meta.url));
  13  | const definitionHash = createHash('sha256').update(readFileSync(`${root}${definitionPath}`)).digest('hex');
  14  | const manifest = JSON.parse(readFileSync(`${root}tasks/ui-test-coverage-20261022/evidence/refinement/gherkin-manifest.json`, 'utf8'));
  15  | const authPath = '/api/auth/v2/sso/';
  16  | type RecordedRequest = { endpoint: string; controlledTimeMs: number; bodyMatchesAccessA: boolean; refreshMatchesR: boolean };
  17  | type StoreView = { token?: string; refreshToken?: string; expiredIn?: number; isOnLogout?: boolean };
  18  | type Mfe = {
  19  |   Hooks: { getHooks(): { store: StoreView } };
  20  |   Service: { getRefreshToken(): Promise<void> | void;
  21  |     postService(path: string, data: unknown, config?: unknown): Promise<{ data: { result?: boolean } }> };
  22  | };
  23  | type BrowserWithSystem = Window & { System: { import(name: string): Promise<Mfe> } };
  24  | 
  25  | test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES', serviceWorkers: 'block',
  26  |   auditFixture: 'Actual mfe-base React with Playwright clock emulation. Unsigned browser-only JWT fixtures and controlled API responses. No natural lifecycle, real identity, or BFF expiry claim.' });
  27  | 
  28  | function token(expiryOffsetSeconds: number, name: string): string {
  29  |   const encode = (value: unknown) => Buffer.from(JSON.stringify(value)).toString('base64url');
  30  |   return `Bearer ${encode({ alg: 'none', typ: 'JWT' })}.${encode({ sub: 'user-a', iat: T / 1000 - 60,
  31  |     exp: T / 1000 + expiryOffsetSeconds, fixture: name })}.fixture`;
  32  | }
  33  | 
  34  | function ref(id: string): string {
  35  |   const steps = manifest.scenarios[id].steps as Record<string, { kind: string }>;
  36  |   return `${definitionPath}; ${id}; assertion lines ${Object.keys(steps).filter(line => steps[line].kind === 'assertion').join(', ')}`;
  37  | }
  38  | 
  39  | async function mapping(audit: AuditCapture, id: string): Promise<void> {
  40  |   const definition = manifest.scenarios[id];
  41  |   expect(definition.sha256).toBe(definitionHash);
  42  |   await audit.record('canonical-mapping', { id, definition: definitionPath, sha256: definitionHash,
  43  |     assertionLines: Object.entries(definition.steps).filter(([, value]) =>
  44  |       (value as { kind: string }).kind === 'assertion').map(([line]) => Number(line)),
  45  |     clock: { start: new Date(T).toISOString(), type: 'Playwright clock emulation installed before navigation' },
  46  |     limits: ['This run measures application timers under clock emulation.',
  47  |       'It does not establish natural background, visibility, suspension, or identity-provider behavior.',
  48  |       'All access and refresh credentials are unsigned local fixtures. No real service accepts these fixtures.'] });
  49  | }
  50  | 
  51  | async function storeObservation(page: Page, accessA: string, refreshR?: string) {
  52  |   return page.evaluate(async ({ accessA, refreshR }) => {
  53  |     const module = await (window as unknown as BrowserWithSystem).System.import('@fm/base');
  54  |     const store = module.Hooks.getHooks().store;
  55  |     return { controlledTimeMs: Date.now(), accessExpiryMs: (store.expiredIn ?? 0) * 1000,
  56  |       accessEqualsA: store.token === accessA, accessPresent: Boolean(store.token),
  57  |       refreshEqualsR: refreshR === undefined ? store.refreshToken === undefined : store.refreshToken === refreshR,
  58  |       refreshPresent: Boolean(store.refreshToken), isOnLogout: Boolean(store.isOnLogout),
  59  |       documentVisibility: document.visibilityState };
  60  |   }, { accessA, refreshR });
  61  | }
  62  | 
  63  | async function runTo(page: Page, offsetMs: number): Promise<void> {
  64  |   const now = await page.evaluate(() => Date.now());
  65  |   const remaining = T + offsetMs - now;
  66  |   expect(remaining).toBeGreaterThanOrEqual(0);
  67  |   await page.clock.runFor(remaining);
> 68  |   expect(await page.evaluate(() => Date.now())).toBe(T + offsetMs);
      |                     ^ Error: page.evaluate: Target page, context or browser has been closed
  69  | }
  70  | 
  71  | async function setup(page: Page, audit: AuditCapture, id: string,
  72  |   options: { accessExpires?: number; refreshExpires?: number; acquisitionFails?: boolean } = {}) {
  73  |   await mapping(audit, id);
  74  |   await blockExternal(page);
  75  |   await page.routeWebSocket('**/*', socket => socket.close());
  76  |   const accessA = token(options.accessExpires ?? 900, 'A');
  77  |   const refreshR = options.refreshExpires === undefined ? undefined : token(options.refreshExpires, 'R');
  78  |   const requests: RecordedRequest[] = [];
  79  |   const pending: Route[] = [];
  80  |   await page.addInitScript(({ access, workspaces }) => {
  81  |     localStorage.setItem('SET_TOKEN', access);
  82  |     sessionStorage.setItem('SET_TOKEN', access);
  83  |     localStorage.setItem('SET_USER', JSON.stringify({ sub: 'user-a', userId: 'user-a', fullName: 'Audit User A' }));
  84  |     localStorage.setItem('SET_WORKSPACES', JSON.stringify(workspaces));
  85  |   }, { access: accessA, workspaces: [workspace('WS-A', 'WS-A')] });
  86  |   await page.clock.install({ time: new Date(T - 60000) });
  87  |   await page.route('**/api/**', async route => {
  88  |     const request = route.request();
  89  |     const path = new URL(request.url()).pathname;
  90  |     if (!path.startsWith(authPath)) {
  91  |       await route.fulfill({ status: 200, json: {} });
  92  |       return;
  93  |     }
  94  |     const endpoint = path.slice(authPath.length);
  95  |     const body = request.postDataJSON() as { singleUIAuthorization?: string } | null;
  96  |     requests.push({ endpoint, controlledTimeMs: await page.evaluate(() => Date.now()),
  97  |       bodyMatchesAccessA: body?.singleUIAuthorization === accessA,
  98  |       refreshMatchesR: request.headers()['single-ui-refresh'] === refreshR });
  99  |     if (endpoint === 'validate') await route.fulfill({ status: 200,
  100 |       headers: { 'single-ui-authorization': accessA }, json: { result: true, entities: [],
  101 |         userInfo: JSON.stringify({ sub: 'user-a', fullName: 'Audit User A' }) } });
  102 |     else if (endpoint === 'refreshtoken') {
  103 |       if (options.acquisitionFails) await route.fulfill({ status: 503, body: '' });
  104 |       else await route.fulfill({ status: 200,
  105 |         headers: { 'single-ui-refresh': refreshR ?? token(13524, 'R') }, json: { result: true } });
  106 |     } else if (endpoint === 'relogin') pending.push(route);
  107 |     else await route.fulfill({ status: 200, json: { result: true } });
  108 |   });
  109 |   await page.goto(`${localBase}/?show_normal_login=Y`);
  110 |   const portal = new PortalPage(page, localPrefix);
  111 |   await portal.expectVisible();
  112 |   await portal.expectWorkspaceTabVisible('WS-A');
  113 |   if (refreshR) {
  114 |     // The fixture invokes the actual exported acquisition service to establish the canonical refresh setup.
  115 |     await page.evaluate(async () => {
  116 |       const module = await (window as unknown as BrowserWithSystem).System.import('@fm/base');
  117 |       await module.Service.getRefreshToken();
  118 |     });
  119 |     await expect.poll(async () => (await storeObservation(page, accessA, refreshR)).refreshEqualsR).toBe(true);
  120 |   }
  121 |   await page.clock.pauseAt(new Date(T));
  122 |   const initial = await storeObservation(page, accessA, refreshR);
  123 |   expect(initial.documentVisibility).toBe('visible');
  124 |   expect(initial.accessEqualsA).toBe(true);
  125 |   expect(initial.refreshEqualsR).toBe(true);
  126 |   await audit.record('controlled-setup', { ...initial, accessExpiryOffsetSeconds: options.accessExpires ?? 900,
  127 |     refreshExpiryOffsetSeconds: options.refreshExpires ?? null,
  128 |     refreshSetup: refreshR ? 'Fixture called actual exported acquisition service before T; counters reset afterward.' : 'No refresh credential at T.',
  129 |     noMouseActivityAfterSetup: true, credentials: 'Unsigned fixture values; equality booleans only in observation records.' });
  130 |   requests.length = 0;
  131 |   await audit.capture('controlled-session-start', 'WS-A is present at controlled time T before the named timer action.', ref(id));
  132 |   return { portal, accessA, refreshR, requests, pending };
  133 | }
  134 | 
  135 | test('AUTH-043 acquire recovery at T+875 without moving access expiry', async ({ page, audit }) => {
  136 |   const { portal, accessA, requests } = await setup(page, audit, 'AUTH-043');
  137 |   await runTo(page, 875000);
  138 |   await expect.poll(() => requests.filter(request => request.endpoint === 'refreshtoken').length).toBe(1);
  139 |   await portal.expectWorkspaceTabVisible('WS-A');
  140 |   await portal.sessionTimeoutDialog.expectAbsent();
  141 |   const observation = await storeObservation(page, accessA);
  142 |   expect(observation.accessExpiryMs).toBe(T + 900000);
  143 |   expect(observation.accessEqualsA).toBe(true);
  144 |   await audit.record('deadline-assertions', { requests, observation,
  145 |     expectedRefreshPostCount: 1, expectedAccessExpiryMs: T + 900000 });
  146 |   await audit.capture('recovery-acquired-before-expiry', 'WS-A remains visible without the expiry dialog at T+875 seconds.', ref('AUTH-043'));
  147 | });
  148 | 
  149 | test('AUTH-044 do not acquire recovery at T+874.999', async ({ page, audit }) => {
  150 |   const { portal, accessA, requests } = await setup(page, audit, 'AUTH-044');
  151 |   await runTo(page, 874999);
  152 |   expect(requests.filter(request => request.endpoint === 'refreshtoken')).toHaveLength(0);
  153 |   await portal.expectWorkspaceTabVisible('WS-A');
  154 |   await portal.sessionTimeoutDialog.expectAbsent();
  155 |   await audit.record('deadline-assertions', { requests, observation: await storeObservation(page, accessA),
  156 |     expectedRefreshPostCount: 0 });
  157 |   await audit.capture('before-acquisition-deadline', 'WS-A remains visible without the expiry dialog immediately before acquisition.', ref('AUTH-044'));
  158 | });
  159 | 
  160 | for (const [id, target] of [['AUTH-076', 900000], ['AUTH-077', 899999]] as const) {
  161 |   test(`${id} access expiry boundary at T+${target}ms`, async ({ page, audit }) => {
  162 |     const { portal, accessA, refreshR, requests } = await setup(page, audit, id, { refreshExpires: 13524 });
  163 |     await runTo(page, target);
  164 |     if (id === 'AUTH-076') {
  165 |       await portal.sessionTimeoutDialog.expectVisible();
  166 |       await expect(portal.sessionTimeoutDialog.dialog).toHaveCount(1);
  167 |       await expect(portal.sessionTimeoutDialog.extendButton).toBeVisible();
  168 |       await expect(portal.sessionTimeoutDialog.logoutButton).toBeVisible();
```