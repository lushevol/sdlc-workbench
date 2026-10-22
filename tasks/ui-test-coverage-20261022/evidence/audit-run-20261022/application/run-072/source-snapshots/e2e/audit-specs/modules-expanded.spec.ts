import type { Route } from '@playwright/test';
import { test, expect } from '../support/audit-fixture.js';
import { CatalogApp, fixtureCategory, fixtureTile, loginCatalog } from '../support/catalog-app.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual React shell and error boundary. Controlled catalog and SystemJS container; held imports, rejected imports, and render exceptions. No real identity or business tenant execution.' });

for (const n of [1, 2, 3, 4, 5, 6]) {
  const id = `UI-MFE-${String(n).padStart(3, '0')}`;
  test(`${id} actual module lifecycle`, async ({ page, audit }) => {
    await audit.defineCase(id);
    let app: CatalogApp;
    let pending: Route | undefined;
    let release: (() => void) | undefined;
    const waiting = new Promise<void>(resolve => { release = resolve; });
    const fallback = page.getByTestId('FallbackError__page-id');
    await audit.step(1, async () => {
      app = await loginCatalog(page, { drawers: [fixtureCategory([fixtureTile({ emailSupport: n === 6 ? '' : 'support@example.test' })])] });
    });
    await audit.step(2, async () => {
      await page.route('**/audit-fixtures/test-container.js', async route => {
        if (n <= 2) { pending = route; await waiting; await route.fallback(); }
        else if (n === 4) await route.fulfill({ contentType: 'application/javascript',
          body: "System.register([],function(e){return {execute:function(){e('default',function(){throw new Error('RENDER-01')})}}});" });
        else await route.fulfill({ contentType: 'application/javascript',
          body: "System.register([],function(){return {execute:function(){throw new Error('MODULE-LOAD-01')}}});" });
      });
      await app.openDrawer();
      if (n === 2 || n >= 5) {
        await app.clickCard();
        if (n === 2) { await expect.poll(() => Boolean(pending)).toBe(true); await expect(app.selectedPanel().getByText('Please wait...', { exact: true })).toBeVisible(); }
        else await expect(fallback).toBeVisible();
      }
      await audit.record('module-fixture', { importMode: n <= 2 ? 'HELD_PENDING' : n === 4 ? 'RENDER_EXCEPTION' : 'IMPORT_EXCEPTION',
        emailSupport: n === 6 ? null : 'support@example.test', businessTenantExecuted: false });
    });
    await audit.step(3, async () => {
      if (n === 2) release!();
      else if (n <= 4) await app.clickCard();
      else await expect(fallback.getByText('There is a problem in this Tile.', { exact: true })).toBeVisible();
    });
    await audit.step(4, async () => {
      if (n === 1) {
        await expect.poll(() => Boolean(pending)).toBe(true);
        await expect(app.selectedPanel().getByText('Please wait...', { exact: true })).toBeVisible();
      } else if (n === 2) await expect(app.selectedPanel().getByTestId('audit-controlled-container')).toBeVisible();
      else if (n <= 4) await expect(fallback.getByText('There is a problem in this Tile.', { exact: true })).toBeVisible();
      else if (n === 5) await expect(fallback.getByRole('link', { name: 'Contact PSS', exact: true })).toBeVisible();
      else await expect(fallback.getByRole('link', { name: 'Contact PSS', exact: true })).toHaveCount(0);
    });
    if (n === 2) await audit.step(5, async () => { await expect(app.selectedPanel().getByText('Please wait...', { exact: true })).toHaveCount(0); });
    if (n === 3) await audit.step(5, async () => { await expect(page.getByRole('img', { name: 'Markets Operations One logo', exact: true })).toBeVisible(); });
    if (n === 5) await audit.step(5, async () => { await expect(fallback.getByRole('link', { name: 'Contact PSS', exact: true })).toHaveAttribute('href', /^mailto:support@example\.test/); });
    // A held pending import is intentionally left pending through its assertion and screenshot.
  });
}
