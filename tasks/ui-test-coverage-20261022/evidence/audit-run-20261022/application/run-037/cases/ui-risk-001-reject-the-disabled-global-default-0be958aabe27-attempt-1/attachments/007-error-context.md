# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: module-risk-expanded.spec.ts >> UI-RISK-001 reject the disabled Global default
- Location: e2e/audit-specs/module-risk-expanded.spec.ts:39:1

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  getByRole('tabpanel').visible().getByTestId('fixture-tile-route').filter({ hasText: /^\/tile-global$/ })
Expected: 0
Received: 1
Timeout:  5000ms

Call log:
  - Expect "toHaveCount" getByRole('tabpanel').visible().getByTestId('fixture-tile-route').filter({ hasText: /^\/tile-global$/ }) with timeout 5000ms
  - waiting for getByRole('tabpanel').visible().getByTestId('fixture-tile-route').filter({ hasText: /^\/tile-global$/ })
    14 × locator resolved to 1 element
       - unexpected value "1"

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
        - generic [ref=e27]: 05:33 UTC
        - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
      - button "User Profiles" [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button "Share Feedback" [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist "workspaces" [ref=e45]:
      - tab [ref=e47] [cursor=pointer]:
        - region "Workspace 1" [ref=e48]:
          - img "Indonesia icon" [ref=e49]
          - textbox "Workspace Name" [ref=e53]: Workspace 1
          - button "delete" [ref=e54]
      - tab [selected] [ref=e57] [cursor=pointer]:
        - region "Test Tile Demo" [ref=e58]:
          - textbox "Workspace Name" [ref=e62]: Test Tile Demo
          - button "delete" [ref=e63]
      - button "Add Workspace" [ref=e67] [cursor=pointer]
    - tabpanel [ref=e72]:
      - generic [ref=e74]:
        - heading "Controlled test container" [level=2] [ref=e75]
        - paragraph [ref=e76]: /tile-global
        - paragraph
        - paragraph [ref=e77]: Version 1
        - generic [ref=e78]: "{}"
        - button "Counter" [ref=e79]
        - status [ref=e80]: "0"
```

# Test source

```ts
  1  | import { test, expect } from '../support/audit-fixture.js';
  2  | import { CatalogApp, fixtureCategory, fixtureContainer, fixtureEntity, fixtureTile, loginCatalog } from '../support/catalog-app.js';
  3  | import { workspace } from '../support/local-app.js';
  4  | 
  5  | test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  6  |   auditFixture: 'Actual current React shell and internal admin modules. Controlled login, validation, activity renewal, UI-USER-01 entity roles, and empty administration endpoint responses. Controlled tenant component is used only for the disabled-default risk case. No BFF permission or business tenant acceptance.' });
  7  | 
  8  | for (const [id, module, title] of [
  9  |   ['UI-MFE-008', '/importmap', 'Import Map'],
  10 |   ['UI-MFE-009', '/category', 'Category'],
  11 |   ['UI-MFE-010', '/tile', 'Tile'],
  12 | ] as const) {
  13 |   test(`${id} open the internal ${title} module`, async ({ page, audit }) => {
  14 |     await audit.defineCase(id);
  15 |     let app: CatalogApp;
  16 |     const entity = { ...fixtureEntity('FMO PORTAL ADMIN', 'Portal'), roleName: 'TEST_OWNER' };
  17 |     const tile = fixtureTile({ container: '@fm/base', module, tile: '', isTemplate: true,
  18 |       entity: ['FMO PORTAL ADMIN'], subject: 'TEST_SUBJECT' });
  19 |     await audit.step(1, async () => {
  20 |       await page.route('**/api/auth/v1/fmo/admin/**', route => route.fulfill({ status: 200, json: { data: [] } }));
  21 |       app = await loginCatalog(page, { drawers: [fixtureCategory([tile])], entities: [entity], includeEntitlementsToken: true });
  22 |     });
  23 |     await audit.step(2, async () => {
  24 |       expect(tile.container).toBe('@fm/base'); expect(tile.module).toBe(module);
  25 |       await app.openDrawer(); await expect(app.entry('Global')).toBeEnabled();
  26 |     });
  27 |     await audit.step(3, async () => {
  28 |       await audit.record('source-resolved-admin-target', { canonicalTarget: 'UNVERIFIED admin tile title and subtitle',
  29 |         actualTarget: 'The unique Test Tile / Demo card in Fixture Category', container: '@fm/base', module,
  30 |         source: 'repos/ui/mfe-base/src/pages/Home/common/Container.tsx',
  31 |         limit: 'This run characterizes the chosen fixture title and subtitle. It does not approve the unresolved canonical target.' });
  32 |       await app.clickCard();
  33 |     });
  34 |     await audit.step(4, async () => { await expect(app.selectedPanel().getByRole('button', { name: `Create New ${title}`, exact: true })).toBeVisible(); });
  35 |     if (id === 'UI-MFE-010') await audit.step(5, async () => { await expect(app.selectedPanel().getByRole('combobox', { name: 'Application Category', exact: true })).toBeVisible(); });
  36 |   });
  37 | }
  38 | 
  39 | test('UI-RISK-001 reject the disabled Global default', async ({ page, audit }) => {
  40 |   await audit.defineCase('UI-RISK-001');
  41 |   let app: CatalogApp;
  42 |   const tiles = [fixtureTile({ disabled: true }), fixtureTile({ entryName: 'Indonesia', tile: '/tile-id' })];
  43 |   const w1 = { ...workspace(), containers: [{ ...fixtureContainer({ marker: 'Initial permitted Indonesia tile' }), tile: '/tile-id', entryName: 'Indonesia' }] };
  44 |   await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory(tiles)], workspaces: [w1] }); });
  45 |   await audit.step(2, async () => {
  46 |     await app.expectRoute('/tile-id'); await app.openDrawer();
  47 |     await expect(app.entry('Global')).toBeDisabled(); await expect(app.entry('Indonesia')).toBeEnabled();
  48 |   });
  49 |   await audit.step(3, async () => { await app.clickCard(); });
  50 |   await audit.step(4, async () => {
  51 |     // A new tab can precede its lazy component. Wait for that component before a negative assertion.
  52 |     if (await app.allWorkspaceTabs().count() > 1)
  53 |       await expect(app.selectedPanel().getByTestId('fixture-tile-route')).toBeVisible();
  54 |     await audit.record('disabled-default-result', { preActionWorkspace: 'W1 has /tile-id',
  55 |       postActionTabs: await app.allWorkspaceTabs().count(), selectedPanelText: await app.selectedPanel().innerText(),
  56 |       source: 'repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx',
  57 |       expected: 'No newly added workspace displays /tile-global' });
> 58 |     await expect(app.selectedPanel().getByTestId('fixture-tile-route').filter({ hasText: /^\/tile-global$/ })).toHaveCount(0);
     |                                                                                                                ^ Error: expect(locator).toHaveCount(expected) failed
  59 |   });
  60 |   await audit.step(5, async () => { await expect(app.entry('Indonesia')).toBeEnabled(); });
  61 | });
  62 | 
  63 | test('UI-RISK-010 show an explicit unsupported internal module message', async ({ page, audit }) => {
  64 |   await audit.defineCase('UI-RISK-010');
  65 |   let app: CatalogApp;
  66 |   const tile = fixtureTile({ container: '@fm/base', module: '/unknown', tile: '', isTemplate: true });
  67 |   await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory([tile])] }); });
  68 |   await audit.step(2, async () => { expect(tile.module).toBe('/unknown'); await app.openDrawer(); });
  69 |   await audit.step(3, async () => {
  70 |     await audit.record('source-resolved-admin-target', { canonicalTarget: 'UNVERIFIED admin tile title and subtitle',
  71 |       actualTarget: 'The unique Test Tile / Demo card in Fixture Category', module: '/unknown',
  72 |       source: 'repos/ui/mfe-base/src/admin/Routing.tsx', limit: 'The canonical admin tile target remains unverified.' });
  73 |     await app.clickCard();
  74 |   });
  75 |   await audit.step(4, async () => {
  76 |     await audit.record('unknown-module-result', { module: '/unknown', panelText: await app.selectedPanel().innerText(),
  77 |       source: 'repos/ui/mfe-base/src/admin/Routing.tsx', expected: 'An explicit unsupported-module message is visible.' });
  78 |     await expect(app.selectedPanel().getByText(/unsupported.*module|unknown.*module|module.*(?:unsupported|not supported|not found)/i)).toBeVisible();
  79 |   });
  80 | });
  81 | 
```