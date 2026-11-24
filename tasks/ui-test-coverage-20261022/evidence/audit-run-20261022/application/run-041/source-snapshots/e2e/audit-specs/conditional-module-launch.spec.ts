import { test, expect } from '../support/audit-fixture.js';
import { fixtureCategory, fixtureContainer, fixtureTile, loginCatalog, type CatalogApp } from '../support/catalog-app.js';
import { localBase, workspace } from '../support/local-app.js';
import { deliverFdc3, installConditionalLaunch, installFdc3Fixture } from '../support/conditional-launch.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual React shell/provider/dispatcher, error boundary, and Home FDC3 hook. Controlled login, catalog, container and intent delivery. URL cases explicitly mount inspected useParameters source through declared base import adapters. No real OpenFin desktop or protected business tenant acceptance.' });

test('UI-MFE-007 another tile remains usable after a module failure', async ({ page, audit }) => {
  await audit.defineCase('UI-MFE-007');
  let app: CatalogApp;
  const w1 = { ...workspace(), containers: [fixtureContainer({ fail: true })] };
  const w2 = { ...workspace('Workspace 2', 'W2'), isActive: false, containers: [fixtureContainer({ marker: 'Panel Two' })] };
  await audit.step(1, async () => { app = await loginCatalog(page, { workspaces: [w1, w2] }); });
  await audit.step(2, async () => {
    await page.route('**/audit-fixtures/test-container.js', route => route.fulfill({ contentType: 'application/javascript',
      body: "System.register(['react'],function(exports){var React;return{setters:[function(v){React=v.default||v;}],execute:function(){exports('default',function(props){if(props.parameters.fail)throw new Error('CONTROLLED-W1-FAILURE');return React.createElement('section',null,React.createElement('h2',null,props.parameters.marker),React.createElement('button',null,'Controlled working tile action'));});}};});" }));
    await page.reload(); await app.portal.expectVisible();
    await expect(app.selectedPanel().getByTestId('FallbackError__page-id')).toBeVisible();
    await audit.record('module-isolation-fixture', { W1: 'Controlled render exception', W2: 'Controlled Panel Two component',
      actual: 'MFE Container error boundary and workspace switching', limit: 'No business tenant module executed.' });
  });
  await audit.step(3, async () => {
    await app.portal.workspace('W2').clickTab();
  });
  await audit.step(4, async () => {
    await expect(app.selectedPanel().getByRole('heading', { name: 'Panel Two', exact: true })).toBeVisible();
    await expect(app.selectedPanel().getByRole('button', { name: 'Controlled working tile action', exact: true })).toBeEnabled();
  });
});

for (const id of ['UI-MFE-011', 'UI-MFE-012'] as const) {
  test(`${id} explicitly mounted conditional URL hook`, async ({ page, audit }) => {
    await audit.defineCase(id);
    let app: CatalogApp;
    let declaredUrl: string;
    const target = fixtureTile({ title: 'T-GLOBAL', subtitle: undefined,
      entity: id === 'UI-MFE-012' ? ['UNAUTHORIZED_ENTITY'] : ['TEST_ENTITY'] });
    const controller = fixtureTile({ title: 'Conditional URL integration', subtitle: undefined,
      container: '@fm/url-launch-fixture', module: '/integration', tile: '/integration', isTemplate: true });
    await audit.step(1, async () => { app = await loginCatalog(page, { drawers: [fixtureCategory([controller, target])] }); });
    await audit.step(2, async () => {
      const source = await installConditionalLaunch(page);
      const initial = { ...workspace(), containers: [{ ...fixtureContainer(), container: '@fm/url-launch-fixture',
        module: '/integration', tile: '/integration', title: 'Conditional URL integration' }] };
      await page.evaluate(value => localStorage.setItem('SET_WORKSPACES', JSON.stringify([value])), initial);
      const query = new URLSearchParams({ container: 'test_container', module: 'test', tile: 'tile-global', parameters: JSON.stringify({ desk: 'SG' }) });
      declaredUrl = `${localBase}/?${query}`;
      await audit.record('conditional-hook-source-and-adapters', { ...source, declaredUrl,
        targetAuthorized: id === 'UI-MFE-011', catalog: { target, controller } });
    });
    await audit.step(3, async () => {
      await page.goto(declaredUrl); await app.portal.expectVisible();
      await expect(page.getByTestId('conditional-launch-mounted')).toBeAttached();
      await expect.poll(() => new URL(page.url()).search).toBe('');
    });
    await audit.step(4, async () => {
      if (id === 'UI-MFE-011') await expect(app.selectedPanel().getByTestId('fixture-parameter-desk')).toHaveText('desk: "SG"');
      else {
        await expect(app.portal.workspaceList.getByRole('tab')).toHaveCount(1);
        const values = await app.portal.workspaceList.getByRole('textbox', { name: 'Workspace Name', exact: true }).evaluateAll(inputs => inputs.map(input => (input as HTMLInputElement).value));
        expect(values).not.toContain('T-GLOBAL');
        await expect(page.getByTestId('fixture-parameter-desk')).toHaveCount(0);
      }
    });
    if (id === 'UI-MFE-011') await audit.step(5, async () => { expect(new URL(page.url()).pathname).toBe('/'); });
  });
}

for (const id of ['UI-MFE-013', 'UI-MFE-014', 'UI-MFE-015'] as const) {
  test(`${id} actual Home FDC3 handler with declared intent delivery`, async ({ page, audit }) => {
    await audit.defineCase(id);
    let app: CatalogApp;
    const cashflow = id === 'UI-MFE-014';
    const target = fixtureTile({ title: cashflow ? 'Cashflow fixture' : 'Trade fixture', subtitle: undefined,
      tile: cashflow ? '/cashflow_cn' : '/trade' });
    await audit.step(1, async () => {
      await installFdc3Fixture(page);
      app = await loginCatalog(page, { drawers: [fixtureCategory(id === 'UI-MFE-015' ? [] : [target])] });
    });
    await audit.step(2, async () => {
      await expect.poll(() => page.evaluate(() => Boolean((window as unknown as { __auditFdc3: { listeners: Record<string, unknown> } }).__auditFdc3.listeners['scb.ViewLaunch']))).toBe(true);
      await audit.record('declared-fdc3-runtime', { windowFin: 'Synthetic truthy object', provider: 'Synthetic window.fdc3.addIntentListener',
        intent: 'scb.ViewLaunch', catalog: id === 'UI-MFE-015' ? [] : [target],
        actualHandler: 'repos/ui/mfe-base/src/pages/Home/common/useOpenfin.ts',
        limits: ['No native OpenFin desktop or cross-application delivery executed.', 'Controlled tenant content only displays parameters from the actual shell.'] });
    });
    await audit.step(3, async () => { await deliverFdc3(page, { type: cashflow ? 'scb.fmptp.cashflows' : 'scb.fmptp.trade.query', id: { tradeId: 'TR-001' } }); });
    await audit.step(4, async () => {
      if (id === 'UI-MFE-015') await expect(page.getByText('Tile trade is unauthorized or does not exist', { exact: true })).toBeVisible();
      else if (cashflow) {
        await expect(app.selectedPanel().getByTestId('fixture-parameter-filters')).toHaveText('filters: [{"field":"Trade_Id","operator":"EQ","values":"TR-001"}]');
      } else await expect(app.selectedPanel().getByTestId('fixture-parameter-intent')).toHaveText('intent: "ViewTradeDetails"');
    });
    await audit.step(5, async () => {
      if (id === 'UI-MFE-015') {
        await expect(app.portal.workspaceList.getByRole('tab')).toHaveCount(1);
        await expect(page.getByTestId('fixture-tile-route')).toHaveCount(0);
      } else if (cashflow) {
        const parameters = JSON.parse(await app.selectedPanel().getByTestId('fixture-parameters').innerText());
        expect(parameters.filters[0].operator).toBe('EQ');
      } else await expect(app.selectedPanel().getByTestId('fixture-parameter-context')).toHaveText('context: {"tradeId":"TR-001"}');
    });
    if (cashflow) await audit.step(6, async () => {
      const parameters = JSON.parse(await app.selectedPanel().getByTestId('fixture-parameters').innerText());
      expect(parameters.filters[0].values).toBe('TR-001');
    });
    await audit.record('fdc3-deliveries', await page.evaluate(() => (window as unknown as { __auditFdc3: unknown }).__auditFdc3));
  });
}
