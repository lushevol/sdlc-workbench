import { test, expect } from '../support/audit-fixture.js';
import { CatalogApp, fixtureCategory, fixtureEntity, fixtureTile, loginCatalog } from '../support/catalog-app.js';
import { localBase, localPrefix } from '../support/local-app.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual current React shell. Controlled login, validation, and activity renewal responses supply UI-USER-01, catalog, and entities. A controlled SystemJS React container displays routes and parameters. Local fixture SVGs replace catalog images. Identity, entitlements, and business tenant behavior are not established.' });

test('UI-CAT-001 open catalog drawer', async ({ page, audit }) => {
  await audit.defineCase('UI-CAT-001');
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page); });
  await audit.step(2, async () => { await expect(app.drawer).toBeHidden(); });
  await audit.step(3, async () => { await app.openDrawer(); });
  await audit.step(4, async () => { await expect(app.drawer.getByText('Tile Options', { exact: true })).toBeVisible(); });
});

test('UI-CAT-002 close drawer without selecting a tile', async ({ page, audit }) => {
  await audit.defineCase('UI-CAT-002');
  let app: CatalogApp; let before = 0;
  await audit.step(1, async () => { app = await loginCatalog(page); });
  await audit.step(2, async () => { before = await app.allWorkspaceTabs().count(); await app.openDrawer(); });
  await audit.step(3, async () => {
    await audit.record('source-resolved-target', { canonicalTarget: 'UNVERIFIED drawer backdrop target',
      actualTarget: '.MuiDrawer-root containing MicroWebUI_base_drawer > .MuiBackdrop-root',
      source: 'repos/ui/mfe-base/src/components/Drawer/index.tsx', limit: 'Canonical target retains its unverified identity. This run characterizes the actual MUI backdrop.' });
    const backdrop = page.locator('.MuiDrawer-root').filter({ has: app.drawer }).locator('.MuiBackdrop-root');
    await expect(backdrop).toHaveCount(1);
    await backdrop.click({ position: { x: 8, y: 70 } });
  });
  await audit.step(4, async () => { await expect(app.drawer).toBeHidden(); });
  await audit.step(5, async () => { await expect(app.portal.workspaceList.getByRole('tab')).toHaveCount(before); });
});

test('UI-CAT-003 render category names and declared tiles', async ({ page, audit }) => {
  await audit.defineCase('UI-CAT-003');
  const drawers = [fixtureCategory([fixtureTile({ title: 'Settlement Fixture' })], 'Settlement', 1),
    fixtureCategory([fixtureTile({ title: 'Confirmations Fixture' })], 'Confirmations', 2)];
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { drawers }); });
  await audit.step(2, async () => { expect(drawers.map(category => [category.label, category.tiles.length])).toEqual([['Settlement', 1], ['Confirmations', 1]]); });
  await audit.step(3, async () => { await app.openDrawer(); });
  await audit.step(4, async () => { await expect(app.drawer.getByText('Settlement', { exact: true })).toBeVisible(); });
  await audit.step(5, async () => { await expect(app.drawer.getByText('Confirmations', { exact: true })).toBeVisible(); });
  await audit.step(6, async () => {
    for (const category of drawers) {
      const region = app.drawer.getByTestId(`${localPrefix}_menuItem`).filter({ has: page.getByText(category.label, { exact: true }) });
      await expect(region.getByTestId(`${localPrefix}_tile`).locator('main > section').first()).toContainText(category.tiles[0].title);
    }
  });
});

test('UI-CAT-004 combine regional entries into one card', async ({ page, audit }) => {
  await audit.defineCase('UI-CAT-004');
  const tiles = [fixtureTile(), fixtureTile({ entryName: 'Indonesia', tile: '/tile-id' })];
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory(tiles)] }); });
  await audit.step(2, async () => { expect(tiles.map(tile => [tile.title, tile.subtitle])).toEqual([['Test Tile', 'Demo'], ['Test Tile', 'Demo']]); });
  await audit.step(3, async () => { await app.openDrawer(); });
  await audit.step(4, async () => { await expect(app.card()).toHaveCount(1); });
  await audit.step(5, async () => { await expect(app.entry('Global')).toBeVisible(); });
  await audit.step(6, async () => { await expect(app.entry('Indonesia')).toBeVisible(); });
});

test('UI-CAT-005 keep distinct subtitles in separate cards', async ({ page, audit }) => {
  await audit.defineCase('UI-CAT-005');
  const tiles = [fixtureTile(), fixtureTile({ subtitle: 'Live', tile: '/tile-live' })];
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory(tiles)] }); });
  await audit.step(2, async () => { expect(tiles.map(tile => tile.subtitle)).toEqual(['Demo', 'Live']); });
  await audit.step(3, async () => { await app.openDrawer(); });
  await audit.step(4, async () => { await expect(app.card('Demo')).toBeVisible(); });
  await audit.step(5, async () => { await expect(app.card('Live')).toBeVisible(); });
  await audit.step(6, async () => { await expect(app.drawer.getByTestId(`${localPrefix}_tile`)).toHaveCount(2); });
});

for (const id of ['UI-CAT-006', 'UI-CAT-007', 'UI-CAT-010'] as const) {
  test(`${id} select the declared default regional entry`, async ({ page, audit }) => {
    await audit.defineCase(id);
    const tiles = id === 'UI-CAT-007'
      ? [fixtureTile({ entryName: 'Indonesia', tile: '/tile-id' }), fixtureTile({ entryName: 'Singapore', tile: '/tile-sg' })]
      : [fixtureTile({ entryName: 'Indonesia', tile: '/tile-id' }), fixtureTile({ entryName: id === 'UI-CAT-010' ? 'gLoBaL' : 'Global' })];
    let app: CatalogApp;
    await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory(tiles)] }); });
    await audit.step(2, async () => {
      expect(tiles[0].entryName).toBe('Indonesia');
      expect(tiles[1].entryName).toBe(id === 'UI-CAT-007' ? 'Singapore' : id === 'UI-CAT-010' ? 'gLoBaL' : 'Global');
      await app.openDrawer();
      if (id === 'UI-CAT-010') {
        await expect(app.entry('gLoBaL')).toHaveText('gLoBaL');
        await audit.record('source-resolved-route', { canonicalPlaceholder: '<fixture gLoBaL tile route>',
          fixtureRoute: '/tile-global', fixtureIdentity: 'T-GLOBAL with entryName gLoBaL',
          limit: 'The canonical expected route remains a placeholder. This assertion characterizes the stated T-GLOBAL route.' });
      }
    });
    await audit.step(3, async () => { await app.clickCard(); });
    await audit.step(4, async () => { await app.expectRoute(id === 'UI-CAT-007' ? '/tile-id' : '/tile-global'); });
  });
}

for (const id of ['UI-CAT-008', 'UI-CAT-015'] as const) {
  test(`${id} launch Indonesia once`, async ({ page, audit }) => {
    await audit.defineCase(id);
    let app: CatalogApp; let before = 0;
    await audit.step(1, async () => { app = await loginCatalog(page, { occupied: true,
      drawers: [fixtureCategory([fixtureTile(), fixtureTile({ entryName: 'Indonesia', tile: '/tile-id' })])] }); });
    await audit.step(2, async () => {
      await app.openDrawer();
      await expect(app.entry('Global')).toBeEnabled(); await expect(app.entry('Indonesia')).toBeEnabled();
      before = await app.allWorkspaceTabs().count();
    });
    await audit.step(3, async () => { await app.entry('Indonesia').click(); });
    await audit.step(4, async () => { await app.expectRoute('/tile-id'); });
    await audit.step(5, async () => { await expect(app.portal.workspaceList.getByRole('tab')).toHaveCount(before + 1); });
    if (id === 'UI-CAT-015') await audit.step(6, async () => {
      await expect(app.selectedPanel().getByTestId('fixture-tile-route').filter({ hasText: '/tile-global' })).toHaveCount(0);
    });
  });
}

test('UI-CAT-009 trim regional display labels', async ({ page, audit }) => {
  await audit.defineCase('UI-CAT-009');
  let app: CatalogApp;
  const tile = fixtureTile({ entryName: '  Indonesia  ', tile: '/tile-id' });
  await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory([tile])] }); });
  await audit.step(2, async () => { expect(tile.entryName).toBe('  Indonesia  '); });
  await audit.step(3, async () => { await app.openDrawer(); });
  await audit.step(4, async () => { await expect(app.entry('Indonesia')).toHaveText('Indonesia'); });
  await audit.step(5, async () => { await expect(app.entry('Indonesia').getByRole('img', { name: 'Indonesia icon', exact: true })).toBeVisible(); });
});

for (const id of ['UI-CAT-011', 'UI-CAT-012'] as const) {
  test(`${id} render unnamed entry controls`, async ({ page, audit }) => {
    await audit.defineCase(id);
    const count = id === 'UI-CAT-011' ? 1 : 2;
    const tiles = Array.from({ length: count }, (_, index) => fixtureTile({ entryName: null, tile: `/unnamed-${index}` }));
    let app: CatalogApp;
    await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory(tiles)] }); });
    await audit.step(2, async () => { expect(tiles.every(tile => tile.entryName === null)).toBe(true); });
    await audit.step(3, async () => { await app.openDrawer(); });
    await audit.step(4, async () => { await expect(app.card().getByRole('button')).toHaveCount(count); });
    if (id === 'UI-CAT-011') {
      await audit.step(5, async () => {
        await audit.record('source-resolved-target', { canonicalTarget: 'UNVERIFIED unnamed entry button',
          actualTarget: 'The sole button within the unique Test Tile / Demo card',
          source: 'repos/ui/mfe-base/src/components/Tile/index.tsx',
          limit: 'The count assertion establishes this target. The canonical source identity remains unverified.' });
        await expect(app.card().getByRole('button')).toHaveText('');
      });
      await audit.step(6, async () => { await expect(app.card().getByRole('button').getByRole('img')).toHaveCount(0); });
    }
  });
}

test('UI-CAT-013 keep every disabled entry inactive', async ({ page, audit }) => {
  await audit.defineCase('UI-CAT-013');
  let app: CatalogApp; let before = 0;
  await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory([
    fixtureTile({ disabled: true }), fixtureTile({ entryName: 'Indonesia', tile: '/tile-id', disabled: true })])] }); });
  await audit.step(2, async () => {
    await app.openDrawer();
    await expect(app.entry('Global')).toBeDisabled(); await expect(app.entry('Indonesia')).toBeDisabled();
    before = await app.allWorkspaceTabs().count();
  });
  await audit.step(3, async () => { await app.clickCard(); });
  await audit.step(4, async () => {
    const box = await app.entry('Global').boundingBox(); expect(box).not.toBeNull();
    await page.mouse.click(box!.x + box!.width / 2, box!.y + box!.height / 2);
  });
  await audit.step(5, async () => { await expect(app.entry('Global')).toBeDisabled(); });
  await audit.step(6, async () => {
    const box = await app.entry('Indonesia').boundingBox(); expect(box).not.toBeNull();
    await page.mouse.click(box!.x + box!.width / 2, box!.y + box!.height / 2);
  });
  await audit.step(7, async () => { await expect(app.entry('Indonesia')).toBeDisabled(); });
  await audit.step(8, async () => { await expect(app.allWorkspaceTabs()).toHaveCount(before); });
});

test('UI-CAT-014 disable only the unavailable entry', async ({ page, audit }) => {
  await audit.defineCase('UI-CAT-014');
  let app: CatalogApp;
  const tiles = [fixtureTile(), fixtureTile({ entryName: 'Indonesia', tile: '/tile-id', disabled: true })];
  await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory(tiles)] }); });
  await audit.step(2, async () => { expect(tiles.map(tile => Boolean(tile.disabled))).toEqual([false, true]); });
  await audit.step(3, async () => { await app.openDrawer(); });
  await audit.step(4, async () => { await expect(app.entry('Global')).toBeEnabled(); });
  await audit.step(5, async () => { await expect(app.entry('Indonesia')).toBeDisabled(); });
});

for (const id of ['UI-CAT-016', 'UI-CAT-017'] as const) {
  test(`${id} choose the active theme image`, async ({ page, audit }) => {
    await audit.defineCase(id);
    const tile = fixtureTile();
    if (id === 'UI-CAT-017') delete tile.imageLightTheme;
    let app: CatalogApp;
    await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory([tile])] }); });
    await audit.step(2, async () => {
      expect(tile.imageDarkTheme).toBe('audit-fixtures/dark.svg');
      if (id === 'UI-CAT-016') expect(tile.imageLightTheme).toBe('audit-fixtures/light.svg');
      else {
        expect(tile.imageLightTheme).toBeUndefined();
        await app.portal.setThemeLight(true);
        await audit.record('fallback-precondition', { theme: 'light', omittedField: 'imageLightTheme',
          reason: 'A light theme exercises the dark-image fallback.' });
      }
    });
    let next = 3;
    if (id === 'UI-CAT-016') await audit.step(next++, async () => { await app.portal.themeCheckbox.click(); });
    await audit.step(next++, async () => { await app.openDrawer(); });
    await audit.step(next, async () => {
      const expected = `${localBase}/${id === 'UI-CAT-016' ? tile.imageLightTheme : tile.imageDarkTheme}`;
      await expect(app.card().locator('main')).toHaveCSS('background-image', `url("${expected}")`);
    });
  });
}

for (const id of ['UI-CAT-018', 'UI-CAT-019'] as const) {
  test(`${id} transfer the declared parameter object`, async ({ page, audit }) => {
    await audit.defineCase(id);
    const tile = fixtureTile(id === 'UI-CAT-018' ? { parameters: { desk: 'SG', includeClosed: false } } : {});
    let app: CatalogApp;
    await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory([tile])] }); });
    await audit.step(2, async () => {
      if (id === 'UI-CAT-018') expect(tile.parameters).toEqual({ desk: 'SG', includeClosed: false });
      else expect(tile.parameters).toBeUndefined();
      await app.openDrawer();
    });
    await audit.step(3, async () => { await app.entry('Global').click(); });
    await audit.step(4, async () => {
      const container = app.selectedPanel().getByTestId('audit-controlled-container');
      await expect(container).toBeVisible();
      if (id === 'UI-CAT-018') await expect(container.getByTestId('fixture-parameter-desk')).toHaveText('desk: "SG"');
      else await expect(container.getByTestId('fixture-parameters')).toHaveText('{}');
    });
    if (id === 'UI-CAT-018') await audit.step(5, async () => {
      await expect(app.selectedPanel().getByTestId('fixture-parameter-includeClosed')).toHaveText('includeClosed: false');
      const value = await app.selectedPanel().getByTestId('fixture-parameters').textContent();
      expect(JSON.parse(value!).includeClosed).toBe(false);
    });
  });
}

test('UI-CAT-020 show the empty catalog', async ({ page, audit }) => {
  await audit.defineCase('UI-CAT-020');
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [] }); });
  await audit.step(2, async () => { expect(app.fixture.drawers).toEqual([]); });
  await audit.step(3, async () => { await app.openDrawer(); });
  await audit.step(4, async () => { await expect(app.drawer.getByText('Tile Options', { exact: true })).toBeVisible(); });
  await audit.step(5, async () => { await expect(app.drawer.getByTestId(`${localPrefix}_tile`)).toHaveCount(0); });
});

test('UI-PREF-006 show profile identity fields', async ({ page, audit }) => {
  await audit.defineCase('UI-PREF-006');
  const oud = { fullName: 'Test User', userId: 'U001', title: 'Analyst', emailId: 'ui@example.test', country: 'SG' };
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { user: { fullName: 'Test User', oud: JSON.stringify(oud) } }); });
  await audit.step(2, async () => { expect(oud).toEqual({ fullName: 'Test User', userId: 'U001', title: 'Analyst', emailId: 'ui@example.test', country: 'SG' }); });
  await audit.step(3, async () => { await app.portal.clickAvatarButton(); });
  await audit.step(4, async () => { await app.openProfile(); });
  for (const [index, value] of ['Test User', 'U001', 'Analyst', 'ui@example.test', 'SG'].entries()) {
    await audit.step(index + 5, async () => { await expect(app.profileIdentity.getByText(value, { exact: true })).toBeVisible(); });
  }
});

for (const id of ['UI-PREF-007', 'UI-PREF-008'] as const) {
  test(`${id} separate functional and data entitlement profiles`, async ({ page, audit }) => {
    await audit.defineCase(id);
    const entities = [fixtureEntity('FMO PORTAL ADMIN')];
    if (id === 'UI-PREF-007') entities.push(fixtureEntity('RATAN_DATA_ENTITLEMENT', 'Test App', 2));
    let app: CatalogApp;
    await audit.step(1, async () => { app = await loginCatalog(page, { entities }); });
    await audit.step(2, async () => { expect(entities.map(entity => entity.name)).toEqual(id === 'UI-PREF-007'
      ? ['FMO PORTAL ADMIN', 'RATAN_DATA_ENTITLEMENT'] : ['FMO PORTAL ADMIN']); });
    await audit.step(3, async () => { await app.portal.clickAvatarButton(); });
    await audit.step(4, async () => { await app.openProfile(); });
    if (id === 'UI-PREF-008') await audit.step(5, async () => {
      // A populated functional entity proves the component's declared delayed population completed.
      await expect(app.functionalProfile.getByRole('button', { name: 'Test App :: FMO PORTAL ADMIN :: Viewer', exact: true })).toBeVisible();
      await expect(page.getByText('Entitlement User Profile', { exact: true })).toHaveCount(0);
    });
    else {
      await audit.step(5, async () => { await expect(app.functionalProfile.getByText('Functional User Profile', { exact: true })).toBeVisible(); });
      await audit.step(6, async () => { await expect(app.functionalProfile.getByRole('button', { name: 'Test App :: FMO PORTAL ADMIN :: Viewer', exact: true })).toBeVisible(); });
      await audit.step(7, async () => { await expect(app.entitlementProfile.getByText('Entitlement User Profile', { exact: true })).toBeVisible(); });
      await audit.step(8, async () => { await expect(app.entitlementProfile.getByRole('button', { name: 'Test App :: RATAN_DATA_ENTITLEMENT :: Viewer', exact: true })).toBeVisible(); });
    }
  });
}

test('UI-PREF-009 expand a role and its entitlement actions', async ({ page, audit }) => {
  await audit.defineCase('UI-PREF-009');
  const entity = fixtureEntity('Test Entity'); entity.subjects[0].name = 'Test Subject';
  let app: CatalogApp;
  await audit.step(1, async () => { app = await loginCatalog(page, { entities: [entity] }); });
  await audit.step(2, async () => {
    expect(entity.applicationName).toBe('Test App'); expect(entity.roleName).toBe('Viewer');
    expect(entity.subjects[0].name).toBe('Test Subject'); expect(entity.subjects[0].actions[0].name).toBe('READ');
  });
  await audit.step(3, async () => { await app.portal.clickAvatarButton(); });
  await audit.step(4, async () => { await app.openProfile(); });
  await audit.step(5, async () => { await app.functionalProfile.getByRole('button', { name: 'Test App :: Test Entity :: Viewer', exact: true }).click(); });
  await audit.step(6, async () => { await app.functionalProfile.getByRole('button', { name: 'Test Subject', exact: true }).click(); });
  await audit.step(7, async () => {
    const subject = app.functionalProfile.locator('.MuiAccordion-root').filter({ has: page.getByRole('button', { name: 'Test Subject', exact: true }) }).last();
    await expect(subject.getByText('Action:', { exact: true })).toBeVisible();
  });
  await audit.step(8, async () => {
    const subject = app.functionalProfile.locator('.MuiAccordion-root').filter({ has: page.getByRole('button', { name: 'Test Subject', exact: true }) }).last();
    await expect(subject.locator('.MuiChip-root').getByText('READ', { exact: true })).toBeVisible();
  });
});
