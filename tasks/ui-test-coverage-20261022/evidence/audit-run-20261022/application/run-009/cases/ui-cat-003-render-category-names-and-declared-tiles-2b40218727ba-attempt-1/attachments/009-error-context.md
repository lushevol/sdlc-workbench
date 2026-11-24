# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: catalog-profile-expanded.spec.ts >> UI-CAT-003 render category names and declared tiles
- Location: e2e/audit-specs/catalog-profile-expanded.spec.ts:34:1

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByTestId('MicroWebUI_base_drawer').getByTestId('MicroWebUI_base_menuItem').filter({ has: getByText('Settlement', { exact: true }) }).getByText('Settlement Fixture', { exact: true })
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" getByTestId('MicroWebUI_base_drawer').getByTestId('MicroWebUI_base_menuItem').filter({ has: getByText('Settlement', { exact: true }) }).getByText('Settlement Fixture', { exact: true }) with timeout 5000ms
  - waiting for getByTestId('MicroWebUI_base_drawer').getByTestId('MicroWebUI_base_menuItem').filter({ has: getByText('Settlement', { exact: true }) }).getByText('Settlement Fixture', { exact: true })

```

```yaml
- img
- text: Tile Options Settlement
- main:
  - text: Settlement Fixture
  - paragraph: Demo
  - button "Global Global icon":
    - text: Global
    - img "Global icon"
- text: Confirmations
- main:
  - text: Confirmations Fixture
  - paragraph: Demo
  - button "Global Global icon":
    - text: Global
    - img "Global icon"
```

# Test source

```ts
  1   | import { test, expect } from '../support/audit-fixture.js';
  2   | import { CatalogApp, fixtureCategory, fixtureEntity, fixtureTile, loginCatalog } from '../support/catalog-app.js';
  3   | import { localBase, localPrefix } from '../support/local-app.js';
  4   | 
  5   | test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  6   |   auditFixture: 'Actual current React shell. Controlled login and validation responses supply UI-USER-01, catalog, and entities. A controlled SystemJS React container displays routes and parameters. Local fixture SVGs replace catalog images. Identity, entitlements, and business tenant behavior are not established.' });
  7   | 
  8   | test('UI-CAT-001 open catalog drawer', async ({ page, audit }) => {
  9   |   await audit.defineCase('UI-CAT-001');
  10  |   let app: CatalogApp;
  11  |   await audit.step(1, async () => { app = await loginCatalog(page); });
  12  |   await audit.step(2, async () => { await expect(app.drawer).toBeHidden(); });
  13  |   await audit.step(3, async () => { await app.openDrawer(); });
  14  |   await audit.step(4, async () => { await expect(app.drawer.getByText('Tile Options', { exact: true })).toBeVisible(); });
  15  | });
  16  | 
  17  | test('UI-CAT-002 close drawer without selecting a tile', async ({ page, audit }) => {
  18  |   await audit.defineCase('UI-CAT-002');
  19  |   let app: CatalogApp; let before = 0;
  20  |   await audit.step(1, async () => { app = await loginCatalog(page); });
  21  |   await audit.step(2, async () => { await app.openDrawer(); before = await app.portal.workspaceList.getByRole('tab').count(); });
  22  |   await audit.step(3, async () => {
  23  |     await audit.record('source-resolved-target', { canonicalTarget: 'UNVERIFIED drawer backdrop target',
  24  |       actualTarget: '.MuiDrawer-root containing MicroWebUI_base_drawer > .MuiBackdrop-root',
  25  |       source: 'repos/ui/mfe-base/src/components/Drawer/index.tsx', limit: 'Canonical target retains its unverified identity. This run characterizes the actual MUI backdrop.' });
  26  |     const backdrop = page.locator('.MuiDrawer-root').filter({ has: app.drawer }).locator('.MuiBackdrop-root');
  27  |     await expect(backdrop).toHaveCount(1);
  28  |     await backdrop.click({ position: { x: 8, y: 70 } });
  29  |   });
  30  |   await audit.step(4, async () => { await expect(app.drawer).toBeHidden(); });
  31  |   await audit.step(5, async () => { await expect(app.portal.workspaceList.getByRole('tab')).toHaveCount(before); });
  32  | });
  33  | 
  34  | test('UI-CAT-003 render category names and declared tiles', async ({ page, audit }) => {
  35  |   await audit.defineCase('UI-CAT-003');
  36  |   const drawers = [fixtureCategory([fixtureTile({ title: 'Settlement Fixture' })], 'Settlement', 1),
  37  |     fixtureCategory([fixtureTile({ title: 'Confirmations Fixture' })], 'Confirmations', 2)];
  38  |   let app: CatalogApp;
  39  |   await audit.step(1, async () => { app = await loginCatalog(page, { drawers }); });
  40  |   await audit.step(2, async () => { expect(drawers.map(category => [category.label, category.tiles.length])).toEqual([['Settlement', 1], ['Confirmations', 1]]); });
  41  |   await audit.step(3, async () => { await app.openDrawer(); });
  42  |   await audit.step(4, async () => { await expect(app.drawer.getByText('Settlement', { exact: true })).toBeVisible(); });
  43  |   await audit.step(5, async () => { await expect(app.drawer.getByText('Confirmations', { exact: true })).toBeVisible(); });
  44  |   await audit.step(6, async () => {
  45  |     for (const category of drawers) {
  46  |       const region = app.drawer.getByTestId(`${localPrefix}_menuItem`).filter({ has: page.getByText(category.label, { exact: true }) });
> 47  |       await expect(region.getByText(category.tiles[0].title, { exact: true })).toBeVisible();
      |                                                                                ^ Error: expect(locator).toBeVisible() failed
  48  |     }
  49  |   });
  50  | });
  51  | 
  52  | test('UI-CAT-004 combine regional entries into one card', async ({ page, audit }) => {
  53  |   await audit.defineCase('UI-CAT-004');
  54  |   const tiles = [fixtureTile(), fixtureTile({ entryName: 'Indonesia', tile: '/tile-id' })];
  55  |   let app: CatalogApp;
  56  |   await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory(tiles)] }); });
  57  |   await audit.step(2, async () => { expect(tiles.map(tile => [tile.title, tile.subtitle])).toEqual([['Test Tile', 'Demo'], ['Test Tile', 'Demo']]); });
  58  |   await audit.step(3, async () => { await app.openDrawer(); });
  59  |   await audit.step(4, async () => { await expect(app.card()).toHaveCount(1); });
  60  |   await audit.step(5, async () => { await expect(app.entry('Global')).toBeVisible(); });
  61  |   await audit.step(6, async () => { await expect(app.entry('Indonesia')).toBeVisible(); });
  62  | });
  63  | 
  64  | test('UI-CAT-005 keep distinct subtitles in separate cards', async ({ page, audit }) => {
  65  |   await audit.defineCase('UI-CAT-005');
  66  |   const tiles = [fixtureTile(), fixtureTile({ subtitle: 'Live', tile: '/tile-live' })];
  67  |   let app: CatalogApp;
  68  |   await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory(tiles)] }); });
  69  |   await audit.step(2, async () => { expect(tiles.map(tile => tile.subtitle)).toEqual(['Demo', 'Live']); });
  70  |   await audit.step(3, async () => { await app.openDrawer(); });
  71  |   await audit.step(4, async () => { await expect(app.card('Demo')).toBeVisible(); });
  72  |   await audit.step(5, async () => { await expect(app.card('Live')).toBeVisible(); });
  73  |   await audit.step(6, async () => { await expect(app.drawer.getByTestId(`${localPrefix}_tile`)).toHaveCount(2); });
  74  | });
  75  | 
  76  | for (const id of ['UI-CAT-006', 'UI-CAT-007', 'UI-CAT-010'] as const) {
  77  |   test(`${id} select the declared default regional entry`, async ({ page, audit }) => {
  78  |     await audit.defineCase(id);
  79  |     const tiles = id === 'UI-CAT-007'
  80  |       ? [fixtureTile({ entryName: 'Indonesia', tile: '/tile-id' }), fixtureTile({ entryName: 'Singapore', tile: '/tile-sg' })]
  81  |       : [fixtureTile({ entryName: 'Indonesia', tile: '/tile-id' }), fixtureTile({ entryName: id === 'UI-CAT-010' ? 'gLoBaL' : 'Global' })];
  82  |     let app: CatalogApp;
  83  |     await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory(tiles)] }); });
  84  |     await audit.step(2, async () => {
  85  |       expect(tiles[0].entryName).toBe('Indonesia');
  86  |       expect(tiles[1].entryName).toBe(id === 'UI-CAT-007' ? 'Singapore' : id === 'UI-CAT-010' ? 'gLoBaL' : 'Global');
  87  |       await app.openDrawer();
  88  |       if (id === 'UI-CAT-010') {
  89  |         await expect(app.entry('gLoBaL')).toHaveText('gLoBaL');
  90  |         await audit.record('source-resolved-route', { canonicalPlaceholder: '<fixture gLoBaL tile route>',
  91  |           fixtureRoute: '/tile-global', fixtureIdentity: 'T-GLOBAL with entryName gLoBaL',
  92  |           limit: 'The canonical expected route remains a placeholder. This assertion characterizes the stated T-GLOBAL route.' });
  93  |       }
  94  |     });
  95  |     await audit.step(3, async () => { await app.clickCard(); });
  96  |     await audit.step(4, async () => { await app.expectRoute(id === 'UI-CAT-007' ? '/tile-id' : '/tile-global'); });
  97  |   });
  98  | }
  99  | 
  100 | for (const id of ['UI-CAT-008', 'UI-CAT-015'] as const) {
  101 |   test(`${id} launch Indonesia once`, async ({ page, audit }) => {
  102 |     await audit.defineCase(id);
  103 |     let app: CatalogApp; let before = 0;
  104 |     await audit.step(1, async () => { app = await loginCatalog(page, { occupied: true,
  105 |       drawers: [fixtureCategory([fixtureTile(), fixtureTile({ entryName: 'Indonesia', tile: '/tile-id' })])] }); });
  106 |     await audit.step(2, async () => {
  107 |       await app.openDrawer();
  108 |       await expect(app.entry('Global')).toBeEnabled(); await expect(app.entry('Indonesia')).toBeEnabled();
  109 |       before = await app.portal.workspaceList.getByRole('tab').count();
  110 |     });
  111 |     await audit.step(3, async () => { await app.entry('Indonesia').click(); });
  112 |     await audit.step(4, async () => { await app.expectRoute('/tile-id'); });
  113 |     await audit.step(5, async () => { await expect(app.portal.workspaceList.getByRole('tab')).toHaveCount(before + 1); });
  114 |     if (id === 'UI-CAT-015') await audit.step(6, async () => {
  115 |       await expect(page.getByTestId('fixture-tile-route').filter({ hasText: '/tile-global' })).toHaveCount(0);
  116 |     });
  117 |   });
  118 | }
  119 | 
  120 | test('UI-CAT-009 trim regional display labels', async ({ page, audit }) => {
  121 |   await audit.defineCase('UI-CAT-009');
  122 |   let app: CatalogApp;
  123 |   const tile = fixtureTile({ entryName: '  Indonesia  ', tile: '/tile-id' });
  124 |   await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory([tile])] }); });
  125 |   await audit.step(2, async () => { expect(tile.entryName).toBe('  Indonesia  '); });
  126 |   await audit.step(3, async () => { await app.openDrawer(); });
  127 |   await audit.step(4, async () => { await expect(app.entry('Indonesia')).toHaveText('Indonesia'); });
  128 |   await audit.step(5, async () => { await expect(app.entry('Indonesia').getByRole('img', { name: 'Indonesia icon', exact: true })).toBeVisible(); });
  129 | });
  130 | 
  131 | for (const id of ['UI-CAT-011', 'UI-CAT-012'] as const) {
  132 |   test(`${id} render unnamed entry controls`, async ({ page, audit }) => {
  133 |     await audit.defineCase(id);
  134 |     const count = id === 'UI-CAT-011' ? 1 : 2;
  135 |     const tiles = Array.from({ length: count }, (_, index) => fixtureTile({ entryName: null, tile: `/unnamed-${index}` }));
  136 |     let app: CatalogApp;
  137 |     await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory(tiles)] }); });
  138 |     await audit.step(2, async () => { expect(tiles.every(tile => tile.entryName === null)).toBe(true); });
  139 |     await audit.step(3, async () => { await app.openDrawer(); });
  140 |     await audit.step(4, async () => { await expect(app.card().getByRole('button')).toHaveCount(count); });
  141 |     if (id === 'UI-CAT-011') {
  142 |       await audit.step(5, async () => {
  143 |         await audit.record('source-resolved-target', { canonicalTarget: 'UNVERIFIED unnamed entry button',
  144 |           actualTarget: 'The sole button within the unique Test Tile / Demo card',
  145 |           source: 'repos/ui/mfe-base/src/components/Tile/index.tsx',
  146 |           limit: 'The count assertion establishes this target. The canonical source identity remains unverified.' });
  147 |         await expect(app.card().getByRole('button')).toHaveText('');
```