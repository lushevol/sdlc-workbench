import { test, expect } from '../support/audit-fixture.js';
import { CatalogApp, fixtureCategory, fixtureContainer, fixtureTile, loginCatalog, type FixtureWorkspace } from '../support/catalog-app.js';
import { workspace } from '../support/local-app.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual current React shell and browser storage. Controlled login/validation/activity renewal, UI-USER-01 permissions, catalog, and SystemJS React component. Markers, counter, and registered refresh callback are controlled fixture observations. No real business tenant or BFF authorization acceptance.' });

const occupied = (id = 'W1', label = 'Workspace 1', marker = 'Panel One', registerRefresh = false): FixtureWorkspace => ({
  ...workspace(label, id), containers: [{ ...fixtureContainer({ marker, registerRefresh }), id: `CONTAINER-${id}` }],
});

test('UI-SHL-006 switch the active workspace', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-006');
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { workspaces: [occupied(), occupied('W2', 'Workspace 2', 'Panel Two')] }); });
  await audit.step(2, async () => {
    await app.portal.workspace('W1').expectSelected(); await app.portal.expectWorkspaceTabVisible('Workspace 2');
  });
  await audit.step(3, async () => { await app.portal.workspace('W2').clickTab(); });
  await audit.step(4, async () => { await app.portal.workspace('W2').expectSelected(); });
  await audit.step(5, async () => { await expect(app.selectedPanel().getByTestId('fixture-marker')).toHaveText('Panel Two'); });
  await audit.step(6, async () => { await expect(page.getByTestId('workspaces-tabpanel-1')).toBeHidden(); });
});

test('UI-SHL-007 preserve mounted container state across switches', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-007');
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { workspaces: [occupied(), workspace('Workspace 2', 'W2')] }); });
  await audit.step(2, async () => {
    const button = app.selectedPanel().getByRole('button', { name: 'Counter', exact: true });
    for (let index = 0; index < 4; index++) await button.click();
    await expect(app.selectedPanel().locator('output')).toHaveText('4');
  });
  await audit.step(3, async () => { await app.portal.workspace('W2').clickTab(); });
  await audit.step(4, async () => { await app.portal.workspace('W1').clickTab(); });
  await audit.step(5, async () => { await expect(app.selectedPanel().locator('output')).toHaveText('4'); });
});

test('UI-SHL-012 remove selected middle workspace', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-012');
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { workspaces: [occupied(),
    occupied('W2', 'Workspace 2', 'Panel Two'), occupied('W3', 'Workspace 3', 'Panel Three')] }); });
  await audit.step(2, async () => { await app.portal.workspace('W2').clickTab(); await expect(app.selectedPanel().getByTestId('fixture-marker')).toHaveText('Panel Two'); });
  await audit.step(3, async () => { await app.portal.workspace('W2').clickDeleteButton(); });
  await audit.step(4, async () => { await app.portal.workspace('W2').expectTabAbsent(); });
  await audit.step(5, async () => { await app.portal.workspace('W1').expectSelected(); });
  await audit.step(6, async () => { await expect(app.allWorkspaceTabs()).toHaveCount(2); });
  await audit.step(7, async () => { await expect(page.getByTestId('fixture-marker').filter({ hasText: /^Panel Two$/ })).toHaveCount(0); });
});

test('UI-SHL-013 remove selected first workspace', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-013');
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { workspaces: [occupied(), occupied('W2', 'Workspace 2', 'Panel Two')] }); });
  await audit.step(2, async () => { await app.portal.workspace('W1').expectSelected(); await expect(app.allWorkspaceTabs()).toHaveCount(2); });
  await audit.step(3, async () => { await app.portal.workspace('W1').clickDeleteButton(); });
  await audit.step(4, async () => { await app.portal.workspace('W1').expectTabAbsent(); });
  await audit.step(5, async () => { await app.portal.workspace('W2').expectSelected(); });
  await audit.step(6, async () => { await expect(app.allWorkspaceTabs()).toHaveCount(1); });
  await audit.step(7, async () => { await expect(app.selectedPanel().getByTestId('fixture-marker')).toHaveText('Panel Two'); });
  await audit.step(8, async () => { await expect(app.portal.workspace('W2').deleteButton).toHaveCount(0); });
});

test('UI-SHL-014 remove an earlier tab and retain selected workspace', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-014');
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { workspaces: [occupied(),
    occupied('W2', 'Workspace 2', 'Panel Two'), occupied('W3', 'Workspace 3', 'Panel Three')] }); });
  await audit.step(2, async () => { await app.portal.workspace('W3').clickTab(); await app.portal.workspace('W3').expectSelected(); });
  await audit.step(3, async () => { await app.portal.workspace('W1').clickDeleteButton(); });
  await audit.step(4, async () => { await app.portal.workspace('W1').expectTabAbsent(); });
  await audit.step(5, async () => { await app.portal.workspace('W3').expectSelected(); });
  await audit.step(6, async () => { await expect(app.selectedPanel().getByTestId('fixture-marker')).toHaveText('Panel Three'); });
});

test('UI-SHL-017 place the first tile in an empty workspace', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-017');
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page); });
  await audit.step(2, async () => { await expect(app.selectedPanel().getByRole('button', { name: 'Find tile', exact: true })).toBeVisible(); await app.openDrawer(); });
  await audit.step(3, async () => { await app.clickCard(); });
  await audit.step(4, async () => { await expect(app.allWorkspaceTabs()).toHaveCount(1); });
  await audit.step(5, async () => { await expect(app.portal.workspaceList.getByRole('tab', { selected: true }).getByRole('textbox', { name: 'Workspace Name', exact: true })).toHaveValue('Test Tile Demo'); });
  await audit.step(6, async () => { await app.expectRoute('/tile-global'); });
  await audit.step(7, async () => { await expect(app.drawer).toBeHidden(); });
});

test('UI-SHL-018 open a tile from an occupied workspace', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-018');
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { workspaces: [occupied()] }); });
  await audit.step(2, async () => { await expect(app.selectedPanel().getByTestId('fixture-marker')).toHaveText('Panel One'); await app.openDrawer(); });
  await audit.step(3, async () => { await app.clickCard(); });
  await audit.step(4, async () => { await expect(app.allWorkspaceTabs()).toHaveCount(2); });
  await audit.step(5, async () => { await expect(app.portal.workspaceList.getByRole('tab', { selected: true }).getByRole('textbox', { name: 'Workspace Name', exact: true })).toHaveValue('Test Tile Demo'); });
  await audit.step(6, async () => { await app.portal.workspace('W1').clickTab(); });
  await audit.step(7, async () => { await expect(app.selectedPanel().getByTestId('fixture-marker')).toHaveText('Panel One'); });
});

test('UI-SHL-019 open the same tile in a second workspace', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-019');
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { workspaces: [occupied('W1', 'Test Tile Demo')] }); });
  await audit.step(2, async () => { await app.expectRoute('/tile-global'); await app.portal.expectWorkspaceTabVisible('Test Tile Demo'); });
  await audit.step(3, async () => { await app.openDrawer(); });
  await audit.step(4, async () => { await app.clickCard(); });
  await audit.step(5, async () => { await expect(app.allWorkspaceTabs()).toHaveCount(2); });
  await audit.step(6, async () => { await expect(app.portal.workspaceList.getByRole('tab', { selected: true }).getByRole('textbox', { name: 'Workspace Name', exact: true })).toHaveValue('Test Tile Demo'); });
  await audit.step(7, async () => {
    const inputs = app.portal.workspaceList.getByRole('textbox', { name: 'Workspace Name', exact: true });
    await expect(inputs).toHaveCount(2); expect(await inputs.evaluateAll(elements => elements.map(element => (element as HTMLInputElement).value))).toEqual(['Test Tile Demo', 'Test Tile Demo']);
  });
});

test('UI-SHL-020 show refresh only for the registered active tab', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-020');
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { workspaces: [occupied('W1', 'Workspace 1', 'Panel One', true), workspace('Workspace 2', 'W2')] }); });
  await audit.step(2, async () => { await expect(app.portal.workspace('W1').refreshButton).toBeVisible(); await expect(app.portal.workspace('W2').refreshButton).toHaveCount(0); });
  await audit.step(3, async () => { await app.portal.workspace('W1').clickTab(); });
  await audit.step(4, async () => { await expect(app.portal.workspace('W1').refreshButton).toHaveCount(1); await expect(app.portal.workspace('W1').refreshButton).toBeVisible(); });
});

test('UI-SHL-022 refresh data without adding a workspace', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-022');
  let app: CatalogApp; let before = 0;
  await audit.step(1, async () => { app = await loginCatalog(page, { workspaces: [occupied('W1', 'Workspace 1', 'Panel One', true)] }); });
  await audit.step(2, async () => {
    await expect(app.selectedPanel().getByTestId('fixture-version')).toHaveText('Version 1');
    await expect(app.portal.workspace('W1').refreshButton).toBeVisible(); before = await app.allWorkspaceTabs().count();
  });
  await audit.step(3, async () => { await app.portal.workspace('W1').refreshButton.click(); });
  await audit.step(4, async () => { await expect(app.selectedPanel().getByTestId('fixture-version')).toHaveText('Version 2'); });
  await audit.step(5, async () => { await expect(app.allWorkspaceTabs()).toHaveCount(before); });
  await audit.step(6, async () => { await app.portal.workspace('W1').expectSelected(); });
});

for (const id of ['UI-SHL-023', 'UI-SHL-026'] as const) {
  test(`${id} restore the declared permitted workspace`, async ({ page, audit }) => {
    await audit.defineCase(id);
    let app: CatalogApp;
    const tile = fixtureTile(id === 'UI-SHL-026' ? { isTemplate: true } : {});
    await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory([tile])], entities: id === 'UI-SHL-026' ? [] : undefined }); });
    await audit.step(2, async () => {
      const saved = [occupied()];
      await page.evaluate(saved => localStorage.setItem('SET_WORKSPACES', JSON.stringify(saved)), saved);
      await audit.record('canonical-saved-workspace', { workspaces: saved, catalog: [tile],
        matchingEntitlement: id === 'UI-SHL-023', template: id === 'UI-SHL-026' });
    });
    await audit.step(3, async () => { await page.reload(); await app.portal.expectVisible(); });
    await audit.step(4, async () => { await app.portal.expectWorkspaceTabVisible('Workspace 1'); });
    if (id === 'UI-SHL-023') await audit.step(5, async () => { await app.expectRoute('/tile-global'); });
  });
}

for (const id of ['UI-SHL-027', 'UI-SHL-028'] as const) {
  test(`${id} render the regional workspace marker`, async ({ page, audit }) => {
    await audit.defineCase(id);
    const entryName = id === 'UI-SHL-027' ? 'Indonesia' : 'Global';
    const w1 = { ...workspace(), containers: [fixtureContainer({}, entryName)] };
    let app: CatalogApp;
    await audit.step(1, async () => { app = await loginCatalog(page, { workspaces: [w1] }); });
    await audit.step(2, async () => { expect(w1.containers[0].entryName).toBe(entryName); await app.expectRoute('/tile-global'); });
    await audit.step(3, async () => { await app.portal.workspace('W1').clickTab(); });
    await audit.step(4, async () => {
      const icon = app.portal.workspace('W1').tab.getByRole('img', { name: 'Indonesia icon', exact: true });
      if (id === 'UI-SHL-027') await expect(icon).toBeVisible(); else await expect(icon).toHaveCount(0);
    });
  });
}
