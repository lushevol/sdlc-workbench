import { test, expect } from '../support/audit-fixture.js';
import { AdminApp } from '../support/admin-app.js';
import { equalsToken, observe, type SystemWindow } from '../support/auth-session.js';
import { localPrefix } from '../support/local-app.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual Category editor and Axios response handler. Controlled login supplies user-a with TEST_OWNER. Controlled update responses establish frontend error handling only. BFF authorization and storage are not verified.' });

for (const id of ['AUTH-128', 'AUTH-129', 'AUTH-131']) {
  test(`${id} Category update response handling with step evidence`, async ({ page, audit }) => {
    const steps = await audit.defineCase(id);
    const app = new AdminApp(page, 'Category', id);
    app.principal = 'user-a'; app.workspaceLabel = 'WS-A';
    let installed: string | undefined;
    let response: { status: number; body: string } | undefined;
    const alert = page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]');
    for (const step of steps) await audit.step(step.number, async () => {
      const text = step.text;
      if (step.number === 1) {
        await app.setup();
        installed = await page.evaluate(async () => (await (window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store.token);
        expect(installed).toBeTruthy(); return;
      }
      if (text.includes('selected fixture tab') || text.startsWith('the tab labelled')) { await app.portal.expectWorkspaceTabVisible('WS-A'); return; }
      if (text.startsWith('User A has entity')) {
        const entities = await page.evaluate(async () => (await (window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store.entities);
        expect(entities).toEqual(expect.arrayContaining([expect.objectContaining({ name: 'FMO PORTAL ADMIN', roleName: 'TEST_OWNER' })])); return;
      }
      if (text.startsWith('the Category editor')) { await app.open(); await app.action('Edit').click(); await expect(app.dialog()).toContainText('edit ID: 101'); return; }
      if (text.startsWith('the Category update POST returns')) {
        response = id === 'AUTH-128' ? { status: 403, body: JSON.stringify({ message: 'Access denied' }) }
          : id === 'AUTH-129' ? { status: 401, body: '' } : { status: 503, body: 'Fixture service unavailable' };
        await page.route('**/api/auth/v1/fmo/admin/category/update', route => route.fulfill({ status: response!.status,
          contentType: id === 'AUTH-128' ? 'application/json' : 'text/plain', body: response!.body }));
        await audit.record('declared-controlled-update-response', { ...response, serverAuthorization: 'NOT_VERIFIED' }); return;
      }
      if (text.startsWith('User A clicks')) {
        const received = page.waitForResponse(value => new URL(value.url()).pathname === '/api/auth/v1/fmo/admin/category/update');
        await app.footerButton('Update').click();
        const actual = await received; response = { status: actual.status(), body: await actual.text() };
        await audit.record('received-update-response', response); return;
      }
      const message = /^the alert .* displays exactly "(.*)"$/.exec(text);
      if (message) { await expect(alert).toHaveText(message[1]); return; }
      if (text.startsWith('the POST to')) { expect(response?.status).toBe(403); expect(JSON.parse(response!.body)).not.toHaveProperty('data'); return; }
      if (text.startsWith('the visible Category record')) { await expect(app.row()).toHaveText(app.beforeValues); return; }
      if (text.startsWith('the installed access credential')) { expect(await equalsToken(page, 'token', installed)).toBe(true); return; }
      if (text.startsWith('the application global isLoading')) { await expect.poll(async () => (await observe(page)).isLoading).toBe(false); return; }
      throw new Error(`No Category auth binding for ${id} step ${step.number}: ${text}`);
    });
  });
}
