# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: module-risk-expanded.spec.ts >> UI-RISK-001 reject the disabled Global default
- Location: e2e/audit-specs/module-risk-expanded.spec.ts:39:1

# Error details

```
Error: expect(locator).toBeEnabled() failed

Locator: getByTestId('MicroWebUI_base_drawer').getByTestId('MicroWebUI_base_tile').filter({ has: locator('section').filter({ hasText: /^Test TileDemo$/ }) }).getByRole('button').filter({ hasText: /^Indonesia$/ })
Expected: enabled
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeEnabled" getByTestId('MicroWebUI_base_drawer').getByTestId('MicroWebUI_base_tile').filter({ has: locator('section').filter({ hasText: /^Test TileDemo$/ }) }).getByRole('button').filter({ hasText: /^Indonesia$/ }) with timeout 5000ms
  - waiting for getByTestId('MicroWebUI_base_drawer').getByTestId('MicroWebUI_base_tile').filter({ has: locator('section').filter({ hasText: /^Test TileDemo$/ }) }).getByRole('button').filter({ hasText: /^Indonesia$/ })

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 05:29 UTC
  - checkbox "Time Switch" [checked]
- button "User Profiles": A
- button "Share Feedback"
- main:
  - tablist "workspaces":
    - tab "Workspace 1":
      - region "Workspace 1":
        - img "Indonesia icon"
        - textbox "Workspace Name": Workspace 1
        - button "delete"
    - tab "Test Tile Demo" [selected]:
      - region "Test Tile Demo":
        - textbox "Workspace Name": Test Tile Demo
        - button "delete"
    - button "Add Workspace"
  - tabpanel:
    - heading "Controlled test container" [level=2]
    - paragraph: /tile-global
    - paragraph
    - paragraph: Version 1
    - text: "{}"
    - button "Counter"
    - status: "0"
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
  51 |     await audit.record('disabled-default-result', { preActionWorkspace: 'W1 has /tile-id',
  52 |       postActionTabs: await app.allWorkspaceTabs().count(), selectedPanelText: await app.selectedPanel().innerText(),
  53 |       source: 'repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx',
  54 |       expected: 'No newly added workspace displays /tile-global' });
  55 |     await expect(app.selectedPanel().getByTestId('fixture-tile-route').filter({ hasText: /^\/tile-global$/ })).toHaveCount(0);
  56 |   });
> 57 |   await audit.step(5, async () => { await expect(app.entry('Indonesia')).toBeEnabled(); });
     |                                                                          ^ Error: expect(locator).toBeEnabled() failed
  58 | });
  59 | 
  60 | test('UI-RISK-010 show an explicit unsupported internal module message', async ({ page, audit }) => {
  61 |   await audit.defineCase('UI-RISK-010');
  62 |   let app: CatalogApp;
  63 |   const tile = fixtureTile({ container: '@fm/base', module: '/unknown', tile: '', isTemplate: true });
  64 |   await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory([tile])] }); });
  65 |   await audit.step(2, async () => { expect(tile.module).toBe('/unknown'); await app.openDrawer(); });
  66 |   await audit.step(3, async () => {
  67 |     await audit.record('source-resolved-admin-target', { canonicalTarget: 'UNVERIFIED admin tile title and subtitle',
  68 |       actualTarget: 'The unique Test Tile / Demo card in Fixture Category', module: '/unknown',
  69 |       source: 'repos/ui/mfe-base/src/admin/Routing.tsx', limit: 'The canonical admin tile target remains unverified.' });
  70 |     await app.clickCard();
  71 |   });
  72 |   await audit.step(4, async () => {
  73 |     await audit.record('unknown-module-result', { module: '/unknown', panelText: await app.selectedPanel().innerText(),
  74 |       source: 'repos/ui/mfe-base/src/admin/Routing.tsx', expected: 'An explicit unsupported-module message is visible.' });
  75 |     await expect(app.selectedPanel().getByText(/unsupported.*module|unknown.*module|module.*(?:unsupported|not supported|not found)/i)).toBeVisible();
  76 |   });
  77 | });
  78 | 
```