import { type Page, type Route } from '@playwright/test';
import { LoginPage } from '../pages/login.page.js';
import { PortalPage } from '../pages/portal.page.js';

export const localBase = 'http://localhost:8128';
export const localPrefix = 'MicroWebUI_base';
export const credentials = { username: 'user-a', password: 'FixturePass1!' };
export const workspace = (label = 'Workspace 1', id = 'W1') => ({ id, label, isActive: true, containers: [] });

// This deliberately unsigned token is a browser fixture. No service accepts it as proof of identity.
export function fixtureAccess(): string {
  const now = Math.floor(Date.now() / 1000);
  const encode = (value: unknown) => Buffer.from(JSON.stringify(value)).toString('base64url');
  return `Bearer ${encode({ alg: 'none', typ: 'JWT' })}.${encode({ sub: 'UI-USER-01', iat: now, exp: now + 3600 })}.fixture`;
}

export async function blockExternal(page: Page): Promise<string[]> {
  const blocked: string[] = [];
  await page.context().route('**/*', async route => {
    const url = new URL(route.request().url());
    if (['localhost', '127.0.0.1', '[::1]'].includes(url.hostname)) await route.continue();
    else { blocked.push(`${url.origin}${url.pathname}`); await route.abort('blockedbyclient'); }
  });
  return blocked;
}

export async function seedWorkspaces(page: Page, values: ReturnType<typeof workspace>[]): Promise<void> {
  await page.addInitScript(values => {
    localStorage.setItem('SET_WORKSPACES', JSON.stringify(values));
  }, values);
}

export async function acceptedLogin(route: Route): Promise<void> {
  await route.fulfill({ status: 200, headers: { 'content-type': 'application/json',
    'single-ui-authorization': fixtureAccess() },
    body: JSON.stringify({ userInfo: JSON.stringify({ sub: 'UI-USER-01', fullName: 'Audit User A' }),
      entities: [], drawers: [], result: true }) });
}

export async function openLogin(page: Page): Promise<LoginPage> {
  await page.goto(`${localBase}/?show_normal_login=Y`);
  const login = new LoginPage(page, localPrefix);
  await login.expectVisible();
  return login;
}

export async function loginToWorkspace(page: Page, label = 'Workspace 1', id = 'W1'): Promise<PortalPage> {
  await seedWorkspaces(page, [workspace(label, id)]);
  await page.route('**/api/auth/v2/sso/login', acceptedLogin);
  await page.route('**/api/auth/v2/sso/extend', acceptedLogin);
  const login = await openLogin(page);
  await login.fillUsername(credentials.username);
  await login.fillPassword(credentials.password);
  await login.clickSignInButton();
  const portal = new PortalPage(page, localPrefix);
  await portal.expectVisible();
  await portal.expectWorkspaceTabVisible(label);
  return portal;
}
