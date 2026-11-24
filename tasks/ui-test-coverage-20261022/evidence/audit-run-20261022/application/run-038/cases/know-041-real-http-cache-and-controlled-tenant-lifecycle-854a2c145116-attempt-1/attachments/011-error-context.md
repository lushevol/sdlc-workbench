# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: cache-lifecycle.spec.ts >> KNOW-041 real HTTP cache and controlled tenant lifecycle
- Location: e2e/audit-specs/cache-lifecycle.spec.ts:14:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByRole('tabpanel').visible().getByTestId('cache-complete')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" getByRole('tabpanel').visible().getByTestId('cache-complete') with timeout 5000ms
  - waiting for getByRole('tabpanel').visible().getByTestId('cache-complete')

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 05:38 UTC
  - checkbox "Time Switch" [checked]
- button "User Profiles": A
- button "Share Feedback"
- main:
  - tablist "workspaces":
    - tab "T-CACHE" [selected]:
      - region "T-CACHE":
        - textbox "Workspace Name": T-CACHE
    - button "Add Workspace"
  - tabpanel:
    - heading "There is a problem in this Tile." [level=6]
    - paragraph: Please click the button below to send the Error detail to the Application Support Team.
    - link "Contact PSS":
      - /url: "mailto:support@example.test?subject=Error in 127.0.0.1&body=Error: Element type is invalid. Received a promise that resolves to: [object Object]. Lazy element type must resolve to a class or function. Did you wrap a component in React.lazy() more than once?\n    at mountLazyComponent (http://127.0.0.1:49343/js/external/react-dom.development.js:23725:11)\n    at beginWork (http://127.0.0.1:49343/js/external/react-dom.development.js:25756:16)\n    at beginWork$1 (http://127.0.0.1:49343/js/external/react-dom.development.js:32267:16)\n    at performUnitOfWork (http://127.0.0.1:49343/js/external/react-dom.development.js:31305:14)\n    at workLoopSync (http://127.0.0.1:49343/js/external/react-dom.development.js:31212:7)\n    at renderRootSync (http://127.0.0.1:49343/js/external/react-dom.development.js:31179:9)\n    at recoverFromConcurrentError (http://127.0.0.1:49343/js/external/react-dom.development.js:30522:22)\n    at performConcurrentWorkOnRoot (http://127.0.0.1:49343/js/external/react-dom.development.js:30420:24)\n    at workLoop (http://127.0.0.1:49343/js/external/react.development.js:2998:36)\n    at flushWork (http://127.0.0.1:49343/js/external/react.development.js:2968:16)"
- complementary: Portal fixture base V1
```

# Test source

```ts
  1   | import { test, expect } from '../support/audit-fixture.js';
  2   | import { CacheApp, type CacheVersion } from '../support/cache-app.js';
  3   | import { LoginPage } from '../pages/login.page.js';
  4   | import { localPrefix } from '../support/local-app.js';
  5   | 
  6   | test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  7   |   auditFixture: 'Actual current React shell and real Chromium HTTP cache. Local HTTP fixture server supplies synthetic Alice, permissions, base entry wrapper, container, tile, trade, lazy content, CSS and images. V1/V2 markers identify controlled fixture assets. No browser routing, production CDN, real business tenant, or changed base binary acceptance.' });
  8   | 
  9   | const allVersions = (version: CacheVersion) => ({ base: version, container: version, tile: version, lazy: version, css: version, image: version });
  10  | const ids = ['KNOW-041', 'KNOW-042', 'KNOW-043', 'KNOW-044', 'KNOW-045', 'KNOW-046',
  11  |   'KNOW-047', 'KNOW-048', 'KNOW-049', 'KNOW-050', 'KNOW-051', 'KNOW-052'] as const;
  12  | 
  13  | for (const id of ids) {
  14  |   test(`${id} real HTTP cache and controlled tenant lifecycle`, async ({ page, audit }) => {
  15  |     test.setTimeout(60000);
  16  |     await audit.defineCase(id);
  17  |     const app = new CacheApp(page);
  18  |     const login = new LoginPage(page, localPrefix);
  19  |     const tileVersion = () => app.panel().getByTestId('cache-tile-version');
  20  |     const drawerVisible = () => expect(app.drawer().getByText('Tile Options', { exact: true })).toBeVisible();
  21  |     const noChunkError = async () => {
  22  |       await expect(app.complete()).toBeVisible();
  23  |       await expect(app.panel().getByTestId('FallbackError__page-id')).toHaveCount(0);
  24  |       expect(app.events.filter(event => String(event.path).includes('/cache/tile-') && Number(event.status) >= 400)).toEqual([]);
  25  |     };
  26  |     const expectMarkers = async (version: CacheVersion) => {
> 27  |       await expect(app.complete()).toBeVisible();
      |                                    ^ Error: expect(locator).toBeVisible() failed
  28  |       for (const kind of ['base', 'container', 'tile'])
  29  |         await expect(app.panel().getByTestId(`cache-${kind}-version`)).toHaveText(version);
  30  |     };
  31  |     const noActiveVersion = (version: CacheVersion) => expect(tileVersion().filter({ hasText: new RegExp(`^${version}$`) })).toHaveCount(0);
  32  |     try {
  33  |       await audit.step(1, async () => {
  34  |         if (id === 'KNOW-052') app.versions = allVersions('V2');
  35  |         await app.start();
  36  |         await audit.record('cache-fixture-scope', app.observations());
  37  |       });
  38  |       await audit.step(2, async () => {
  39  |         await app.portal.expectVisible();
  40  |         await audit.record('catalog-permission', { actor: 'alice', exactTileTitle: 'T-CACHE',
  41  |           source: 'Controlled local HTTP login/validate responses', container: '@fm/cache-container', tile: '/cache' });
  42  |       });
  43  | 
  44  |       if (id === 'KNOW-041') {
  45  |         await audit.step(3, async () => {
  46  |           await app.cdp.send('Network.clearBrowserCache');
  47  |           expect(app.events.some(event => event.path === '/cache/tile-entry.js')).toBe(false);
  48  |           await audit.record('empty-tenant-cache', { method: 'CDP Network.clearBrowserCache', tileEntryPreviouslyRequested: false });
  49  |         });
  50  |         await audit.step(4, async () => { app.versions = allVersions('V1'); });
  51  |         await audit.step(5, () => app.openDrawer());
  52  |         await audit.step(6, drawerVisible);
  53  |         await audit.step(7, () => app.openTile());
  54  |         await audit.step(8, () => expectMarkers('V1'));
  55  |         await audit.step(9, noChunkError);
  56  |       } else if (id === 'KNOW-045') {
  57  |         await audit.step(3, async () => { await expect(page.getByTestId('cache-base-entry-version')).toHaveText('Portal fixture base V1'); });
  58  |         await audit.step(4, async () => { app.versions.base = 'V2'; await app.saveBlankWorkspace(); });
  59  |         await audit.step(5, () => app.reload());
  60  |         await audit.step(6, async () => { await expect(page.getByTestId('cache-base-entry-version')).toHaveText('Portal fixture base V2'); });
  61  |         await audit.step(7, () => app.openDrawer());
  62  |         await audit.step(8, drawerVisible);
  63  |       } else if (id === 'KNOW-046') {
  64  |         await audit.step(3, () => app.warm('V1'));
  65  |         await audit.step(4, async () => { app.versions = allVersions('V2'); });
  66  |         await audit.step(5, async () => { expect(new URL(page.url()).searchParams.get('show_normal_login')).toBe('Y'); });
  67  |         await audit.step(6, () => app.portal.clickAvatarButton());
  68  |         await audit.step(7, () => app.portal.clickLogoutMenuItem());
  69  |         await audit.step(8, async () => {
  70  |           await page.getByRole('dialog', { name: 'Leave Now?', exact: true }).getByRole('button', { name: 'Logout', exact: true }).click();
  71  |           await login.expectVisible();
  72  |         });
  73  |         await audit.step(9, () => login.fillUsername('alice'));
  74  |         await audit.step(10, () => login.fillPassword('FixturePass1!'));
  75  |         await audit.step(11, async () => { await login.clickSignInButton(); await app.portal.expectVisible(); });
  76  |         await audit.step(12, () => app.openDrawer());
  77  |         await audit.step(13, drawerVisible);
  78  |         await audit.step(14, () => app.openTile());
  79  |         await audit.step(15, async () => { await expect(tileVersion()).toHaveText('V2'); });
  80  |         await audit.step(16, () => noActiveVersion('V1'));
  81  |       } else if (id === 'KNOW-047') {
  82  |         await audit.step(3, async () => {
  83  |           const entry = await page.evaluate(async origin => {
  84  |             const response = await fetch(`${origin}/cache/tile-entry.js`);
  85  |             return { status: response.status, body: await response.text(), cacheControl: response.headers.get('cache-control') };
  86  |           }, app.origin);
  87  |           expect(entry.status).toBe(200); expect(entry.body).toContain('tile-V1.js');
  88  |           await audit.record('held-v1-entry', entry);
  89  |         });
  90  |         await audit.step(4, async () => { app.removedV1Chunk = true; });
  91  |         await audit.step(5, () => app.openDrawer());
  92  |         await audit.step(6, drawerVisible);
  93  |         await audit.step(7, () => app.openTile());
  94  |         await audit.step(8, async () => {
  95  |           await expect(app.panel().getByTestId('FallbackError__page-id')).toBeVisible();
  96  |           await expect(app.complete()).toHaveCount(0);
  97  |           expect(app.events.some(event => event.path === '/cache/tile-V1.js' && event.status === 404)).toBe(true);
  98  |         });
  99  |         await audit.step(9, () => app.openDrawer());
  100 |         await audit.step(10, drawerVisible);
  101 |       } else if (id === 'KNOW-048') {
  102 |         await audit.step(3, async () => { await app.warm('V1'); await expect(app.panel().getByTestId('cache-trade-id')).toHaveText('TR-1001'); });
  103 |         await audit.step(4, async () => { app.failTileEntry = true; await app.saveBlankWorkspace(); });
  104 |         await audit.step(5, async () => {
  105 |           app.versions = allVersions('V2');
  106 |           await audit.record('versioned-trade-fixtures', { V1: { identifier: 'TR-1001', amount: '100' }, V2: { identifier: 'TR-1002', amount: '200' },
  107 |             loadFailureState: 'Actual MFE FallbackError__page-id: There is a problem in this Tile.',
  108 |             limit: 'This source-defined failure state is used for characterization. Business agreement remains unverified.' });
  109 |         });
  110 |         await audit.step(6, () => app.reload());
  111 |         await audit.step(7, () => app.openDrawer());
  112 |         await audit.step(8, drawerVisible);
  113 |         await audit.step(9, () => app.openTile());
  114 |         await audit.step(10, async () => {
  115 |           await expect(app.panel().getByTestId('FallbackError__page-id')).toBeVisible();
  116 |           await expect(app.panel().getByTestId('cache-trade-id')).toHaveCount(0);
  117 |           await expect(app.panel().getByTestId('cache-trade-amount')).toHaveCount(0);
  118 |           expect(app.events.some(event => event.path === '/cache/tile-entry.js' && event.status === 503)).toBe(true);
  119 |         });
  120 |         await audit.step(11, async () => { await expect(app.panel().getByText('There is a problem in this Tile.', { exact: true })).toBeVisible(); });
  121 |       } else {
  122 |         await audit.step(3, async () => {
  123 |           await app.warm(id === 'KNOW-052' ? 'V2' : 'V1');
  124 |           if (id === 'KNOW-049') {
  125 |             await app.panel().getByRole('button', { name: 'Open lazy search', exact: true }).click();
  126 |             await expect(app.panel().getByTestId('cache-lazy-version')).toHaveText('V1');
  127 |           }
```