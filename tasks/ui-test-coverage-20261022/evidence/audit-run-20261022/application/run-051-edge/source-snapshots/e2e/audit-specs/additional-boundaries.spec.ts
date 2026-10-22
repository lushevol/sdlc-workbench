import { test, expect } from '../support/audit-fixture.js';
import { AdminApp, categoryRecord } from '../support/admin-app.js';
import { fixtureContainer, loginCatalog, type CatalogApp } from '../support/catalog-app.js';
import { equalsToken, type SystemWindow } from '../support/auth-session.js';
import { localPrefix, workspace } from '../support/local-app.js';
import { LoginPage } from '../pages/login.page.js';
import type { Page, Route } from '@playwright/test';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual React shell, Category grid, and response handler. Controlled browser identity and service responses. Cross-tab rejection does not establish BFF global revocation. Spreadsheet formula execution requires a separate viewer.' });

test('UX-036 thirty workspace tabs remain operable', async ({ page, audit }) => {
  const steps = await audit.defineCase('UX-036');
  let app: CatalogApp;
  const last = () => app.portal.workspaceList.getByRole('tab', { name: 'Workspace 30', exact: true });
  for (const step of steps) await audit.step(step.number, async () => {
    if (step.number === 1) {
      app = await loginCatalog(page, { workspaces: Array.from({ length: 30 }, (_, i) => ({ ...workspace(`Workspace ${i + 1}`, `W${i + 1}`),
        isActive: i === 0, containers: [{ ...fixtureContainer({ registerRefresh: true }), id: `FIXTURE-CONTAINER-${i + 1}` }] })) });
      await expect(app.allWorkspaceTabs()).toHaveCount(30); return;
    }
    if (step.number === 2) { await last().scrollIntoViewIfNeeded(); await last().click(); return; }
    if (step.number === 3) { await expect(last()).toHaveAttribute('aria-selected', 'true'); await expect(last()).toBeInViewport(); return; }
    const name = step.number === 4 ? 'refresh' : 'delete';
    await last().hover(); await expect(last().getByRole('button', { name, exact: true })).toBeVisible();
    await expect(last().getByRole('button', { name, exact: true })).toBeEnabled();
  });
});

test('UX-043 captured CSV retains a spreadsheet-viewer prerequisite', async ({ page, audit }) => {
  const steps = await audit.defineCase('UX-043');
  const app = new AdminApp(page, 'Category', 'UX-043');
  for (const step of steps) {
    if (step.number === 3) {
      await audit.record('execution-blocker', { code: 'FORMULA_ENABLED_SPREADSHEET_VIEWER_UNAVAILABLE',
        blockedStep: step.number, owner: 'Unknown', nextAction: 'Provide a formula-enabled spreadsheet viewer for captured CSV imports.',
        consequence: 'Export and screenshot evidence exist. Formula execution and cell data types remain unverified.' });
      test.skip(true, 'FORMULA_ENABLED_SPREADSHEET_VIEWER_UNAVAILABLE: export completed; viewer steps cannot execute.');
    }
    await audit.step(step.number, async () => {
      if (step.number === 1) {
        app.rows = ['=1+1', '+1+1', '-1+1', '@SUM(1)'].map((label, i) => categoryRecord(101 + i, label));
        await app.setup(); await app.open();
        await expect(app.grid.locator('[data-id] [data-field="label"]')).toHaveText(['=1+1', '+1+1', '-1+1', '@SUM(1)']); return;
      }
      if (step.number === 2) {
        const waiting = page.waitForEvent('download'); await app.grid.getByRole('button', { name: 'Export', exact: true }).click();
        await page.getByRole('menuitem', { name: 'Download as CSV', exact: true }).click();
        const download = await waiting; const stream = await download.createReadStream(); const chunks: Buffer[] = [];
        for await (const chunk of stream!) chunks.push(Buffer.from(chunk));
        const bytes = Buffer.concat(chunks); await audit.record('formula-label-csv-artifact', { filename: download.suggestedFilename(), csv: bytes.toString('utf8'),
          limit: 'Raw CSV bytes do not establish spreadsheet data types or formula nonexecution.' });
        await test.info().attach('formula-label-export.csv', { body: bytes, contentType: 'text/csv' }); return;
      }
      throw new Error('Spreadsheet viewer prerequisite was not handled.');
    });
  }
});

test('AUTH-115 shared-session rejection across two live pages', async ({ page, context, audit }) => {
  const steps = await audit.defineCase('AUTH-115');
  const appA = new AdminApp(page, 'Category', 'AUTH-115'); appA.principal = 'user-a';
  let tabB: Page; let appB: AdminApp;
  let installed: string | undefined;
  let held: Route | undefined; let release!: () => void;
  const pending = new Promise<void>(resolve => { release = resolve; });
  const rejected = { message: 'TOKEN_INVALID_EXPIRED' };
  const logout = page.getByRole('dialog', { name: 'Leave Now?', exact: true });
  for (const step of steps) await audit.step(step.number, async () => {
    if (step.number === 1) {
      await appA.setup();
      installed = await page.evaluate(async () => (await (window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store.token);
      expect(installed).toBeTruthy();
      tabB = await context.newPage(); appB = new AdminApp(tabB, 'Category', 'AUTH-115'); appB.principal = 'user-a'; appB.access = installed!;
      await appB.setup(true); expect(await equalsToken(tabB, 'token', installed)).toBe(true);
      expect(new URL(page.url()).origin).toBe(new URL(tabB.url()).origin);
      await audit.record('shared-session-fixture', { session: 'SESSION-A', principal: 'user-a', sameContext: page.context() === tabB.context(), sameAccess: true,
        limit: 'Controlled credentials and rejection. Actual BFF revocation is not executed.' });
      await audit.capture('tab-b-initial', 'TAB-B authenticated under the shared SESSION-A fixture.', 'AUTH-115 step 1', tabB); return;
    }
    if (step.number === 2) {
      await appA.portal.clickAvatarButton(); await appA.portal.clickLogoutMenuItem(); await expect(logout).toBeVisible();
      const now = new Date(); await page.clock.install({ time: now }); await page.clock.pauseAt(new Date(now.getTime() + 60_000));
      await page.route('**/api/auth/v2/sso/logout', route => route.fulfill({ status: 200, json: {} }));
      await page.route('**/api/ssiplus/imeta/logout', route => route.fulfill({ status: 200, json: {} })); return;
    }
    if (step.number === 3) {
      await appB.open(); await appB.action('Edit').click(); await expect(appB.dialog()).toContainText('edit ID: 101');
      await tabB.route('**/api/auth/v1/fmo/admin/category/update', async route => { held = route; await pending;
        await route.fulfill({ status: 401, json: rejected }); });
    } else if (step.number === 4) { await logout.getByRole('button', { name: 'Logout', exact: true }).click(); return; }
    else if (step.number === 5) { await page.clock.runFor(1000); await new LoginPage(page, localPrefix).expectVisible(); return; }
    else if (step.number === 6) { await appB.footerButton('Update').click(); await expect.poll(() => Boolean(held)).toBe(true); }
    else if (step.number === 7) {
      const response = tabB.waitForResponse(value => new URL(value.url()).pathname === '/api/auth/v1/fmo/admin/category/update'); release();
      const actual = await response; expect(actual.status()).toBe(401); expect(await actual.json()).toEqual(rejected);
      await audit.record('rejected-category-response', { status: actual.status(), body: await actual.json() });
    } else if (step.number === 8) await expect(new LoginPage(tabB, localPrefix).usernameInput).toBeVisible();
    else if (step.number === 9) await expect(new LoginPage(tabB, localPrefix).passwordInput).toBeVisible();
    else if (step.number === 10) await expect(new LoginPage(tabB, localPrefix).signInButton).toBeVisible();
    else if (step.number === 11) await expect(tabB.getByRole('tablist', { name: 'workspaces', exact: true })).toHaveCount(0);
    else if (step.number === 12) await expect(tabB.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toHaveText('Expired Session, please login again.');
    else if (step.number === 13) expect(rejected).not.toHaveProperty('data');
    else throw new Error(`No shared-session binding for step ${step.number}.`);
    await audit.capture(`tab-b-step-${step.number}`, `TAB-B state for canonical step ${step.number}: ${step.text}`, 'AUTH-115', tabB);
  });
});
