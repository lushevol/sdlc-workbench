import { test, expect } from '../support/audit-fixture.js';
import { acceptedLogin, blockExternal, credentials, localPrefix, openLogin, seedWorkspaces, workspace } from '../support/local-app.js';
import { PortalPage } from '../pages/portal.page.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual current MFE implementation; intercepted accepted credential response; unsigned fixture JWT; WS-A seeded before navigation. No real identity acceptance.' });

for (const [id, username, password, action] of [
  ['AUTH-016', 'user-a', 'FixturePass1!', 'click'],
  ['AUTH-017', 'user-a', 'FixturePass1!', 'username-enter'],
  ['AUTH-018', 'user-a', 'FixturePass1!', 'password-enter'],
  ['AUTH-019', '  user-a  ', 'FixturePass1!', 'click'],
  ['AUTH-020', 'user-a', '  FixturePass1!  ', 'click'],
] as const) {
  test(`${id} accepted credential interaction`, async ({ page, audit }) => {
    const blocked = await blockExternal(page);
    await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
    const posts: unknown[] = [];
    await page.route('**/api/auth/v2/sso/login', async route => {
      posts.push(route.request().postDataJSON());
      await acceptedLogin(route);
    });
    const login = await openLogin(page);
    await audit.capture('start-login', 'Credential controls are visible before input.', `${id} Given`);
    await login.fillUsername(username);
    await login.fillPassword(password);
    await audit.capture('credentials-ready', 'Username is populated and the password is masked before submission.', `${id} When`);
    if (action === 'username-enter') await login.usernameInput.press('Enter');
    else if (action === 'password-enter') await login.passwordInput.press('Enter');
    else await login.clickSignInButton();
    const portal = new PortalPage(page, localPrefix);
    await portal.expectVisible();
    await portal.expectWorkspaceTabVisible('WS-A');
    await expect(login.usernameInput).toHaveCount(0);
    await expect(login.passwordInput).toHaveCount(0);
    await expect(login.signInButton).toHaveCount(0);
    expect(posts).toEqual([credentials]);
    await audit.record('request-assertions', { count: posts.length,
      usernameMatched: true, passwordMatched: true, externalRequestsBlocked: blocked,
      serviceResult: 'CONTROLLED_ACCEPTED_RESPONSE', identityAcceptance: 'NOT_VERIFIED' });
    await audit.capture('home-ws-a', 'WS-A is visible and login controls are absent.', `${id} Then`);
  });
}
