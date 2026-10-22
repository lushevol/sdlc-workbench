import { test, expect } from '../support/audit-fixture.js';
import { blockExternal, credentials, fixtureAccess, localBase, localPrefix, openLogin, seedWorkspaces, workspace } from '../support/local-app.js';
import { LoginPage } from '../pages/login.page.js';
import { PortalPage } from '../pages/portal.page.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Current actual React; controlled SSO/login HTTP responses; unsigned fixture access token; seeded empty WS-A; external requests blocked. Provider acceptance and BFF fallback are not verified.' });

const drawers = [{ id: 'DRAWER-A', label: 'Audit catalog', tiles: [{ title: 'Audit tile', entity: ['ENTITY-A'],
  container: '@fm/audit-unused', module: '/unused', tile: '/unused', subject: 'AUDIT', isTemplate: true }] }];

for (const [id, query, version] of [
  ['AUTH-030', 'code=ENTRA-CODE-A', 'v3'],
  ['AUTH-031', 'code=MFA-CODE-A&iss=ISSUER-A&client_id=CLIENT-A', 'v2'],
  ['AUTH-032', 'code=MFA-CODE-A&iss=ISSUER-A', 'v2'],
  ['AUTH-033', 'code=MFA-CODE-A&client_id=CLIENT-A', 'v2'],
  ['AUTH-035', 'code=ENTRA-CODE-A', 'v3'],
] as const) {
  test(`${id} callback route and restored workspace`, async ({ page, audit }) => {
    await blockExternal(page);
    await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
    const requests: { pathname: string; body: unknown }[] = [];
    let release!: () => void;
    const held = new Promise<void>(resolve => { release = resolve; });
    await page.route(/\/api\/auth\/v[23]\/sso\/login$/, async route => {
      requests.push({ pathname: new URL(route.request().url()).pathname, body: route.request().postDataJSON() });
      await held;
      await route.fulfill({ status: 200, headers: { 'single-ui-authorization': fixtureAccess() },
        json: { userInfo: JSON.stringify({ sub: 'user-a', fullName: 'Audit User A' }), drawers,
          entities: [{ name: 'ENTITY-A', subjects: [] }] } });
    });
    await page.goto(`${localBase}/?${query}`);
    await expect.poll(() => requests.length).toBe(1);
    await audit.capture('callback-pending', 'The callback URL is loaded and its controlled exchange is pending.', `${id} When`);
    release();
    const portal = new PortalPage(page, localPrefix);
    await portal.expectVisible();
    await portal.expectWorkspaceTabVisible('WS-A');
    expect(requests).toHaveLength(1);
    expect(requests[0].pathname).toBe(`/api/auth/${version}/sso/login`);
    const expected = Object.fromEntries(new URLSearchParams(query));
    expect(requests[0].body).toMatchObject(expected);
    await expect.poll(() => new URL(page.url()).pathname + new URL(page.url()).search).toBe('/');
    await audit.record('callback-assertions', { requests, resultingPath: '/', providerAcceptance: 'CONTROLLED_FIXTURE' });
    await audit.capture('callback-home', 'WS-A is visible and the callback query has been removed.', `${id} Then`);
  });
}

for (const id of ['AUTH-034', 'AUTH-036'] as const) {
  test(`${id} rejected callback remains anonymous`, async ({ page, audit }) => {
    await blockExternal(page);
    await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
    let release!: () => void;
    const held = new Promise<void>(resolve => { release = resolve; });
    let count = 0;
    await page.route('**/api/auth/v3/sso/login', async route => {
      count++;
      await held;
      if (id === 'AUTH-034') await route.fulfill({ status: 401, json: { message: 'AuthenticationException' } });
      else await route.fulfill({ status: 200, headers: { 'single-ui-authorization': fixtureAccess() },
        json: { userInfo: JSON.stringify({ sub: 'user-a' }), drawers,
          entities: [{ name: 'ENTITY-X', subjects: [] }] } });
    });
    await page.goto(`${localBase}/?code=${id === 'AUTH-034' ? 'USED-CODE-A' : 'ENTRA-CODE-A'}`);
    await expect.poll(() => count).toBe(1);
    await audit.capture('callback-pending', 'The callback exchange is held before its rejected result.', `${id} Given`);
    release();
    const login = new LoginPage(page, localPrefix);
    await login.expectVisible();
    await expect(login.usernameInput).toBeVisible();
    await expect(login.passwordInput).toBeVisible();
    await expect(login.signInButton).toBeVisible();
    await expect(page.getByRole('tablist', { name: 'workspaces', exact: true })).toHaveCount(0);
    const alert = page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]');
    await expect(alert).toHaveCount(1);
    await expect(alert).toHaveText(id === 'AUTH-034'
      ? 'Invalid username and password combination or SSO service is unavailable.' : 'No entitlements found.');
    await audit.capture('callback-rejected', 'The exact rejection alert appears with login controls and no workspace tablist.', `${id} Then`);
  });
}

for (const [id, fullName] of [['AUTH-037', 'Alex Example'], ['AUTH-039', 'Álex 王'],
  ['AUTH-040', '<img src=x onerror=alert(1)>']] as const) {
  test(`${id} profile display preserves directory text`, async ({ page, audit }) => {
    await blockExternal(page);
    await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
    let alerts = 0;
    page.on('dialog', async dialog => { alerts++; await dialog.dismiss(); });
    await page.route('**/api/auth/v2/sso/login', route => route.fulfill({ status: 200,
      headers: { 'single-ui-authorization': fixtureAccess() },
      json: { userInfo: JSON.stringify({ sub: 'user-a', auth_time: Math.floor(Date.now() / 1000),
        oud: JSON.stringify({ fullName, userId: 'user-a' }) }), entities: [], drawers: [] } }));
    const login = await openLogin(page);
    await audit.capture('start-login', 'The login form is visible before the directory fixture is returned.', `${id} Given`);
    await login.fillUsername(credentials.username);
    await login.fillPassword(credentials.password);
    await login.clickSignInButton();
    const portal = new PortalPage(page, localPrefix);
    await portal.expectWorkspaceTabVisible('WS-A');
    await portal.clickAvatarButton();
    await expect(portal.profileMenuItem.getByText(fullName, { exact: true })).toBeVisible();
    await audit.capture('profile-menu', 'The avatar menu displays the fixture directory name.', `${id} When`);
    await portal.clickProfileMenuItem();
    // The source Modal uses a title node without an accessible dialog role.
    const profile = page.locator('[class*="profile"]').filter({ has: page.getByText('User Profile', { exact: true }) });
    await expect(page.getByText('User Profile', { exact: true })).toBeVisible();
    const details = page.getByTestId('entitlement-profile-label-box');
    await expect(details.getByText(fullName, { exact: true })).toBeVisible();
    expect(await details.textContent()).not.toContain('�');
    expect(alerts).toBe(0);
    if (id === 'AUTH-040') await expect(details.locator('img')).toHaveCount(0);
    await audit.record('profile-assertions', { fullName, alertCount: alerts,
      directoryMarkupImagesInNameRegion: 0, policyApproval: id === 'AUTH-037' ? 'IMPLEMENTATION_CHARACTERIZATION' : 'PROPOSED_EXPECTATION_ONLY' });
    await audit.capture('profile-details', 'User Profile displays the exact directory name as text.', `${id} Then`);
  });
}
