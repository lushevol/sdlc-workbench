import { test, expect } from '../support/audit-fixture.js';
import { CatalogApp, fixtureCategory, fixtureContainer, fixtureEntity, fixtureTile, loginCatalog } from '../support/catalog-app.js';
import { workspace } from '../support/local-app.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual current React shell and internal admin modules. Controlled login, validation, activity renewal, UI-USER-01 entity roles, and empty administration endpoint responses. Controlled tenant component is used only for the disabled-default risk case. No BFF permission or business tenant acceptance.' });

for (const [id, module, title] of [
  ['UI-MFE-008', '/importmap', 'Import Map'],
  ['UI-MFE-009', '/category', 'Category'],
  ['UI-MFE-010', '/tile', 'Tile'],
] as const) {
  test(`${id} open the internal ${title} module`, async ({ page, audit }) => {
    await audit.defineCase(id);
    let app: CatalogApp;
    const entity = { ...fixtureEntity('FMO PORTAL ADMIN', 'Portal'), roleName: 'TEST_OWNER' };
    const tile = fixtureTile({ container: '@fm/base', module, tile: '', isTemplate: true,
      entity: ['FMO PORTAL ADMIN'], subject: 'TEST_SUBJECT' });
    await audit.step(1, async () => {
      await page.route('**/api/auth/v1/fmo/admin/**', route => route.fulfill({ status: 200, json: { data: [] } }));
      app = await loginCatalog(page, { drawers: [fixtureCategory([tile])], entities: [entity], includeEntitlementsToken: true });
    });
    await audit.step(2, async () => {
      expect(tile.container).toBe('@fm/base'); expect(tile.module).toBe(module);
      await app.openDrawer(); await expect(app.entry('Global')).toBeEnabled();
    });
    await audit.step(3, async () => {
      await audit.record('source-resolved-admin-target', { canonicalTarget: 'UNVERIFIED admin tile title and subtitle',
        actualTarget: 'The unique Test Tile / Demo card in Fixture Category', container: '@fm/base', module,
        source: 'repos/ui/mfe-base/src/pages/Home/common/Container.tsx',
        limit: 'This run characterizes the chosen fixture title and subtitle. It does not approve the unresolved canonical target.' });
      await app.clickCard();
    });
    await audit.step(4, async () => { await expect(app.selectedPanel().getByRole('button', { name: `Create New ${title}`, exact: true })).toBeVisible(); });
    if (id === 'UI-MFE-010') await audit.step(5, async () => { await expect(app.selectedPanel().getByRole('combobox', { name: 'Application Category', exact: true })).toBeVisible(); });
  });
}

test('UI-RISK-001 reject the disabled Global default', async ({ page, audit }) => {
  await audit.defineCase('UI-RISK-001');
  let app: CatalogApp;
  const tiles = [fixtureTile({ disabled: true }), fixtureTile({ entryName: 'Indonesia', tile: '/tile-id' })];
  const w1 = { ...workspace(), containers: [{ ...fixtureContainer({ marker: 'Initial permitted Indonesia tile' }), tile: '/tile-id', entryName: 'Indonesia' }] };
  await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory(tiles)], workspaces: [w1] }); });
  await audit.step(2, async () => {
    await app.expectRoute('/tile-id'); await app.openDrawer();
    await expect(app.entry('Global')).toBeDisabled(); await expect(app.entry('Indonesia')).toBeEnabled();
  });
  await audit.step(3, async () => { await app.clickCard(); });
  await audit.step(4, async () => {
    // A new tab can precede its lazy component. Wait for that component before a negative assertion.
    if (await app.allWorkspaceTabs().count() > 1)
      await expect(app.selectedPanel().getByTestId('fixture-tile-route')).toBeVisible();
    await audit.record('disabled-default-result', { preActionWorkspace: 'W1 has /tile-id',
      postActionTabs: await app.allWorkspaceTabs().count(), selectedPanelText: await app.selectedPanel().innerText(),
      source: 'repos/ui/mfe-base/src/components/Drawer/MenuItem.tsx',
      expected: 'No newly added workspace displays /tile-global' });
    await expect(app.selectedPanel().getByTestId('fixture-tile-route').filter({ hasText: /^\/tile-global$/ })).toHaveCount(0);
  });
  await audit.step(5, async () => { await expect(app.entry('Indonesia')).toBeEnabled(); });
});

test('UI-RISK-010 show an explicit unsupported internal module message', async ({ page, audit }) => {
  await audit.defineCase('UI-RISK-010');
  let app: CatalogApp;
  const tile = fixtureTile({ container: '@fm/base', module: '/unknown', tile: '', isTemplate: true });
  await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory([tile])] }); });
  await audit.step(2, async () => { expect(tile.module).toBe('/unknown'); await app.openDrawer(); });
  await audit.step(3, async () => {
    await audit.record('source-resolved-admin-target', { canonicalTarget: 'UNVERIFIED admin tile title and subtitle',
      actualTarget: 'The unique Test Tile / Demo card in Fixture Category', module: '/unknown',
      source: 'repos/ui/mfe-base/src/admin/Routing.tsx', limit: 'The canonical admin tile target remains unverified.' });
    await app.clickCard();
  });
  await audit.step(4, async () => {
    await audit.record('unknown-module-result', { module: '/unknown', panelText: await app.selectedPanel().innerText(),
      source: 'repos/ui/mfe-base/src/admin/Routing.tsx', expected: 'An explicit unsupported-module message is visible.' });
    await expect(app.selectedPanel().getByText(/unsupported.*module|unknown.*module|module.*(?:unsupported|not supported|not found)/i)).toBeVisible();
  });
});
