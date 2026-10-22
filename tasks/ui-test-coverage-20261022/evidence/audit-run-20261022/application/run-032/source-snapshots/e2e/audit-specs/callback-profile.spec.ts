import { test, expect } from '../support/audit-fixture.js';
import { blockExternal, credentials, fixtureAccess, localBase, localPrefix, openLogin, seedWorkspaces, workspace } from '../support/local-app.js';
import { LoginPage } from '../pages/login.page.js';
import { PortalPage } from '../pages/portal.page.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual React; controlled callback/login responses; unsigned browser-only credentials; empty seeded WS-A. Provider acceptance and BFF fallback are not verified.' });

const drawers = [{ id: 'DRAWER-A', label: 'Audit catalog', tiles: [{ title: 'Audit tile', entity: ['ENTITY-A'],
  container: '@fm/audit-unused', module: '/unused', tile: '/unused', subject: 'AUDIT', isTemplate: true }] }];
const response = (fullName = 'Audit User A') => ({ userInfo: JSON.stringify({ sub: 'user-a', fullName }),
  drawers, entities: [{ name: 'ENTITY-A', subjects: [] }] });

for (const [id, query, version] of [
  ['AUTH-030', 'code=ENTRA-CODE-A', 'v3'],
  ['AUTH-031', 'code=MFA-CODE-A&iss=ISSUER-A&client_id=CLIENT-A', 'v2'],
  ['AUTH-032', 'code=MFA-CODE-A&iss=ISSUER-A', 'v2'],
  ['AUTH-033', 'code=MFA-CODE-A&client_id=CLIENT-A', 'v2'],
] as const) {
  test(`${id} callback route and restored workspace`, async ({ page, audit }) => {
    await audit.defineCase(id);
    const requests: { pathname: string; body: unknown }[] = [];
    const portal = new PortalPage(page, localPrefix);
    const callback = `${localBase}/?${query}`;
    await audit.step(1, async () => { await blockExternal(page); await openLogin(page); expect(await page.context().cookies()).toHaveLength(0); });
    await audit.step(2, async () => { await audit.record('configured-callback', { callback }); expect(new URL(callback).search).toBe(`?${query}`); });
    await audit.step(3, async () => {
      await page.route(/\/api\/auth\/v[23]\/sso\/login$/, async route => {
        requests.push({ pathname: new URL(route.request().url()).pathname, body: route.request().postDataJSON() });
        await route.fulfill({ status: 200, headers: { 'single-ui-authorization': fixtureAccess() }, json: response() });
      });
    });
    await audit.step(4, async () => { await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]); });
    await audit.step(5, async () => { await page.goto(callback); await portal.expectVisible(); });
    await audit.step(6, async () => { await portal.expectWorkspaceTabVisible('WS-A'); });
    await audit.step(7, async () => {
      expect(requests).toHaveLength(1); expect(requests[0].pathname).toBe(`/api/auth/${version}/sso/login`);
      expect(requests[0].body).toMatchObject(Object.fromEntries(new URLSearchParams(query)));
      await audit.record('callback-requests', requests);
    });
  });
}

test('AUTH-035 accepted callback removes query after entitlement validation', async ({ page, audit }) => {
  await audit.defineCase('AUTH-035');
  const portal = new PortalPage(page, localPrefix);
  let release!: () => void;
  const held = new Promise<void>(resolve => { release = resolve; });
  await audit.step(1, async () => {
    await blockExternal(page); await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
    await page.route('**/api/auth/v3/sso/login', async route => { await held;
      await route.fulfill({ status: 200, headers: { 'single-ui-authorization': fixtureAccess() }, json: response() }); });
    await page.goto(`${localBase}/?code=ENTRA-CODE-A`);
  });
  await audit.step(2, async () => { expect(workspace('WS-A', 'WS-A').label).toBe('WS-A'); });
  await audit.step(3, async () => { expect(new URL(page.url()).searchParams.get('code')).toBe('ENTRA-CODE-A'); await audit.record('callback-fixture', { entity: 'ENTITY-A', drawer: 'DRAWER-A' }); });
  await audit.step(4, async () => { release(); await portal.expectVisible(); });
  await audit.step(5, async () => { await expect.poll(() => new URL(page.url()).pathname + new URL(page.url()).search).toBe('/'); });
  await audit.step(6, async () => { await portal.expectWorkspaceTabVisible('WS-A'); });
});

for (const id of ['AUTH-034', 'AUTH-036'] as const) {
  test(`${id} rejected callback remains anonymous`, async ({ page, audit }) => {
    await audit.defineCase(id);
    let release!: () => void;
    const held = new Promise<void>(resolve => { release = resolve; });
    let count = 0;
    const login = new LoginPage(page, localPrefix);
    const alert = page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]');
    const tablist = page.getByRole('tablist', { name: 'workspaces', exact: true });
    await audit.step(1, async () => { await blockExternal(page); await openLogin(page); await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]); });
    const configure = async () => {
      await page.route('**/api/auth/v3/sso/login', async route => {
        count++; await held;
        if (id === 'AUTH-034') await route.fulfill({ status: 401, json: { message: 'AuthenticationException' } });
        else await route.fulfill({ status: 200, headers: { 'single-ui-authorization': fixtureAccess() },
          json: { userInfo: JSON.stringify({ sub: 'user-a' }), drawers, entities: [{ name: 'ENTITY-X', subjects: [] }] } });
      });
    };
    if (id === 'AUTH-034') {
      await audit.step(2, async () => { await audit.record('callback-url', { url: `${localBase}/?code=USED-CODE-A` }); });
      await audit.step(3, configure);
      await audit.step(4, async () => { await page.goto(`${localBase}/?code=USED-CODE-A`); await expect.poll(() => count).toBe(1); release(); await login.expectVisible(); });
      await audit.step(5, async () => { await expect(login.usernameInput).toBeVisible(); });
      await audit.step(6, async () => { await expect(login.passwordInput).toBeVisible(); });
      await audit.step(7, async () => { await expect(login.signInButton).toBeVisible(); });
      await audit.step(8, async () => { await expect(alert).toHaveText('Invalid username and password combination or SSO service is unavailable.'); });
      await audit.step(9, async () => { await expect(tablist).toHaveCount(0); });
    } else {
      await audit.step(2, async () => { await configure(); await page.goto(`${localBase}/?code=ENTRA-CODE-A`); await expect.poll(() => count).toBe(1); });
      await audit.step(3, async () => { release(); await login.expectVisible(); });
      await audit.step(4, async () => { await expect(login.usernameInput).toBeVisible(); });
      await audit.step(5, async () => { await expect(login.passwordInput).toBeVisible(); });
      await audit.step(6, async () => { await expect(login.signInButton).toBeVisible(); });
      await audit.step(7, async () => { await expect(tablist).toHaveCount(0); });
      await audit.step(8, async () => { await expect(alert).toHaveText('No entitlements found.'); });
    }
  });
}

for (const [id, fullName] of [['AUTH-037', 'Alex Example'], ['AUTH-038', 'user-a'], ['AUTH-039', 'Álex 王'],
  ['AUTH-040', '<img src=x onerror=alert(1)>']] as const) {
  test(`${id} profile preserves directory text`, async ({ page, audit }) => {
    await audit.defineCase(id);
    const login = new LoginPage(page, localPrefix);
    const portal = new PortalPage(page, localPrefix);
    const details = page.getByTestId('entitlement-profile-label-box');
    let alerts = 0;
    await audit.step(1, async () => {
      await blockExternal(page); await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
      page.on('dialog', async dialog => { alerts++; await dialog.dismiss(); }); await openLogin(page);
    });
    await audit.step(2, async () => {
      await page.route('**/api/auth/v2/sso/login', route => route.fulfill({ status: 200,
        headers: { 'single-ui-authorization': fixtureAccess() },
        json: { userInfo: JSON.stringify({ sub: 'user-a', auth_time: Math.floor(Date.now() / 1000),
          oud: JSON.stringify({ fullName, userId: 'user-a' }) }), entities: [], drawers: [] } }));
      await audit.record('directory-response-fixture', { fullName, fallback: id === 'AUTH-038' ? 'BFF fallback substituted by response fixture' : null });
      await login.expectVisible();
    });
    await audit.step(3, async () => { await login.fillUsername(credentials.username); });
    await audit.step(4, async () => { await login.fillPassword(credentials.password); });
    await audit.step(5, async () => { await login.clickSignInButton(); await portal.expectVisible(); });
    let n = 6;
    if (id !== 'AUTH-040') { await audit.step(n++, async () => { await portal.expectWorkspaceTabVisible('WS-A'); }); }
    await audit.step(n++, async () => { await portal.clickAvatarButton(); });
    await audit.step(n++, async () => { await expect(portal.profileMenuItem.getByText(fullName, { exact: true })).toBeVisible(); await portal.clickProfileMenuItem(); });
    await audit.step(n++, async () => { await expect(page.getByText('User Profile', { exact: true })).toBeVisible(); await expect(details.locator('.MuiTypography-h5').filter({ hasText: fullName })).toBeVisible(); });
    if (id === 'AUTH-039') await audit.step(n++, async () => { expect(await details.textContent()).not.toContain('�'); });
    if (id === 'AUTH-040') {
      await audit.step(n++, async () => { expect(alerts).toBe(0); });
      await audit.step(n++, async () => { await expect(details.locator('img')).toHaveCount(0); });
    }
    await audit.record('profile-assertions', { fullName, alertCount: alerts, BffFallback: 'NOT_VERIFIED', providerAcceptance: 'CONTROLLED_FIXTURE' });
  });
}
