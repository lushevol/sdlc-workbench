import type { Page, Route } from '@playwright/test';
import { expect, type AuditCapture } from './audit-fixture.js';
import { blockExternal, localBase, localPrefix, workspace } from './local-app.js';
import { PortalPage } from '../pages/portal.page.js';
import { LoginPage } from '../pages/login.page.js';

export const T = Date.parse('2030-01-01T00:00:00.000Z');
export type SessionStore = { token?: string; refreshToken?: string; expiredIn?: number; isOnLogout?: boolean; isLoading?: boolean; entities?: unknown[] };
export type Mfe = { Hooks: { getHooks(): { store: SessionStore } };
  Service: { getRefreshToken(): Promise<void> | void; signal: { getRefreshToken?: AbortController; relogin?: AbortController };
    postService(path: string, data: unknown, config?: unknown): Promise<{data: unknown}> };
  LoginUtil: { setAuthorization(value: string): void; setRefreshToken(value: string | undefined): void };
  ExtendService: { extendToken(): void } };
export type SystemWindow = Window & { System: { import(name: string): Promise<Mfe> } };
export const tokenPayload = (payload: unknown) => {
  const encode = (value: unknown) => Buffer.from(JSON.stringify(value)).toString('base64url');
  return `Bearer ${encode({ alg: 'none', typ: 'JWT' })}.${encode(payload)}.fixture`;
};
export const sessionToken = (seconds: number, name: string) => tokenPayload({ sub: 'user-a', iat: T / 1000 - 60, exp: T / 1000 + seconds, fixture: name });
export async function observe(page: Page) {
  return page.evaluate(async () => {
    const m = await (window as unknown as SystemWindow).System.import('@fm/base');
    const s = m.Hooks.getHooks().store;
    return { now: Date.now(), accessExpiryMs: (s.expiredIn ?? 0) * 1000, accessPresent: Boolean(s.token),
      refreshPresent: Boolean(s.refreshToken), isOnLogout: Boolean(s.isOnLogout), isLoading: Boolean(s.isLoading), visibility: document.visibilityState };
  });
}
export async function equalsToken(page: Page, field: 'token' | 'refreshToken', value?: string) {
  return page.evaluate(async ({field, value}) => (await (window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store[field] === value, {field, value});
}
export async function visibility(page: Page, state: 'hidden' | 'visible') {
  await page.evaluate(state => { Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => state }); document.dispatchEvent(new Event('visibilitychange')); }, state);
}
export async function at(page: Page, offsetMs: number, jump = false) {
  const remaining = T + offsetMs - await page.evaluate(() => Date.now());
  expect(remaining).toBeGreaterThanOrEqual(0);
  if (jump) await page.clock.fastForward(remaining); else await page.clock.runFor(remaining);
  expect(await page.evaluate(() => Date.now())).toBe(T + offsetMs);
}
export async function rotate(page: Page, value: string) {
  await page.evaluate(async value => { (await (window as unknown as SystemWindow).System.import('@fm/base')).LoginUtil.setAuthorization(value); }, value);
  await expect.poll(() => equalsToken(page, 'token', value)).toBe(true);
}
export type SessionOptions = { accessExpires?: number; refreshExpires?: number; refreshValue?: string; acquisitionFails?: boolean };
export async function sessionSetup(page: Page, audit: AuditCapture, options: SessionOptions = {}) {
  await blockExternal(page); await page.routeWebSocket('**/*', socket => socket.close());
  const accessA = sessionToken(options.accessExpires ?? 900, 'A');
  const refreshR = options.refreshValue ?? (options.refreshExpires === undefined ? undefined : sessionToken(options.refreshExpires, 'R'));
  const requests: { endpoint: string; time: number; accessMatchesA: boolean; accessMatchesB: boolean; refreshMatchesR: boolean }[] = [];
  const acquisition: Route[] = [], relogin: Route[] = [];
  const control = { holdAcquisition: false, acquisitionError: '', failAcquisition: Boolean(options.acquisitionFails), holdRelogin: true, reloginError: '', extendAccess: sessionToken(1500, 'B') };
  await page.addInitScript(({ access, workspaces }) => {
    if (localStorage.getItem('_AUDIT_AUTH_SEEDED_ONCE')) return;
    localStorage.setItem('_AUDIT_AUTH_SEEDED_ONCE','true'); localStorage.setItem('SET_TOKEN', access); sessionStorage.setItem('SET_TOKEN', access);
    localStorage.setItem('SET_USER', JSON.stringify({ sub: 'user-a', userId: 'user-a', fullName: 'Audit User A' }));
    localStorage.setItem('SET_WORKSPACES', JSON.stringify(workspaces)); }, { access: accessA, workspaces: [workspace('WS-A', 'WS-A')] });
  await page.clock.install({ time: new Date(T - 60000) });
  await page.route('**/api/**', async route => {
    const path = new URL(route.request().url()).pathname;
    if (!path.startsWith('/api/auth/v2/sso/')) { await route.fulfill({ status: 200, json: {} }); return; }
    const endpoint = path.split('/').at(-1)!;
    const body = route.request().postDataJSON() as { singleUIAuthorization?: string } | null;
    requests.push({ endpoint, time: await page.evaluate(() => Date.now()), accessMatchesA: body?.singleUIAuthorization === accessA, accessMatchesB: body?.singleUIAuthorization === sessionToken(1200, 'B'), refreshMatchesR: route.request().headers()['single-ui-refresh'] === refreshR });
    if (endpoint === 'validate') await route.fulfill({ status: 200, headers: { 'single-ui-authorization': accessA }, json: { result: true, drawers: [], entities: [], userInfo: JSON.stringify({ sub: 'user-a', fullName: 'Audit User A' }) } });
    else if (endpoint === 'refreshtoken') {
      if (control.acquisitionError === 'Network Error') await route.abort('failed');
      else if (control.holdAcquisition) acquisition.push(route);
      else if (control.failAcquisition) await route.fulfill({ status: 503, body: '' });
      else await route.fulfill({ status: 200, headers: { 'single-ui-refresh': refreshR ?? sessionToken(13524, 'R') }, json: { result: true } });
    } else if (endpoint === 'relogin') {
      if (control.reloginError === 'Network Error') await route.abort('failed');
      else if (control.reloginError) await route.fulfill({ status: 401, json: { message: control.reloginError } });
      else relogin.push(route);
    } else if (endpoint === 'extend') await route.fulfill({ status: 200, headers: { 'single-ui-authorization': control.extendAccess }, json: { result: true } });
    else await route.fulfill({ status: 200, json: { result: true } });
  });
  await page.goto(`${localBase}/?show_normal_login=Y`);
  const portal = new PortalPage(page, localPrefix), login = new LoginPage(page, localPrefix);
  await portal.expectVisible(); await portal.expectWorkspaceTabVisible('WS-A');
  if (refreshR !== undefined) {
    await page.evaluate(async () => { await (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.getRefreshToken(); });
    await expect.poll(() => equalsToken(page, 'refreshToken', refreshR)).toBe(true);
  }
  await page.clock.pauseAt(new Date(T)); requests.length = 0;
  await audit.record('session-fixture', { time: new Date(T).toISOString(), accessExpires: options.accessExpires ?? 900,
    refreshExpires: options.refreshExpires ?? null, refreshFixture: refreshR ? 'PRESENT_UNSIGNED_BROWSER_ONLY' : 'ABSENT',
    limits: ['Controlled clock and visibility adapter. No natural suspension or real credential acceptance is measured.'] });
  return { portal, login, accessA, refreshR, requests, acquisition, relogin, control, count: (endpoint: string) => requests.filter(x => x.endpoint === endpoint).length,
    acquire: () => page.evaluate(async () => { await (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.getRefreshToken(); }),
    startAcquire: () => page.evaluate(async () => { void (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.getRefreshToken(); }),
    acceptAcquisition: async (value = refreshR ?? sessionToken(13524, 'R')) => { for (const route of acquisition.splice(0)) await route.fulfill({ status: 200, headers: { 'single-ui-refresh': value }, json: { result: true } }); },
    acceptRelogin: async (value = sessionToken(900, 'B')) => { for (const route of relogin.splice(0)) await route.fulfill({ status: 200, headers: { 'single-ui-authorization': value }, json: { result: true, entities: [], userInfo: JSON.stringify({ sub: 'user-a', fullName: 'Audit User A' }) } }); },
  };
}
export type Session = Awaited<ReturnType<typeof sessionSetup>>;
export async function commonAssertion(page: Page, s: Session, text: string): Promise<boolean> {
  const timeout = s.portal.sessionTimeoutDialog;
  const count = /records exactly (\d+) new POST requests to "\/api\/auth\/v2\/sso\/(\w+)"/.exec(text);
  if (count) { await expect.poll(() => s.count(count[2])).toBe(Number(count[1])); return true; }
  if (text.includes('tab labelled "WS-A"') && text.includes('visible')) { await s.portal.expectWorkspaceTabVisible('WS-A'); return true; }
  if (text.includes('tablist named "workspaces"') && text.includes('absent')) { await expect(s.portal.workspaceList).toHaveCount(0); return true; }
  if (text.includes('textbox with placeholder "Enter Username"') && text.includes('visible')) { await expect(s.login.usernameInput).toBeVisible(); return true; }
  if (text.includes('text input with placeholder "Enter Password"') && text.includes('visible')) { await expect(s.login.passwordInput).toBeVisible(); return true; }
  if (text.includes('button labelled "Sign In"') && text.includes('visible')) { await expect(s.login.signInButton).toBeVisible(); return true; }
  if (text.includes('dialog named "Your session has been expired"') && text.includes('absent')) { await timeout.expectAbsent(); return true; }
  if (text.includes('button labelled "Extend"') && text.includes('disabled')) { await expect(timeout.extendButton).toBeDisabled(); return true; }
  if (text.includes('button labelled "Extend"') && text.includes('enabled')) { await expect(timeout.extendButton).toBeEnabled(); return true; }
  if (text.includes('button labelled "Extend"') && text.includes('visible')) { await expect(timeout.extendButton).toBeVisible(); return true; }
  if (text.includes('button labelled "Logout"') && text.includes('enabled')) { await expect(timeout.logoutButton).toBeEnabled(); return true; }
  if (text.includes('button labelled "Logout"') && text.includes('visible')) { await expect(timeout.logoutButton).toBeVisible(); return true; }
  if (text.includes('dialog named "Your session has been expired"') && text.includes('visible')) { await timeout.expectVisible(); return true; }
  if (text.includes('isOnLogout=true')) {
    await expect.poll(async () => { await page.clock.runFor(0); return (await observe(page)).isOnLogout; }).toBe(true); return true;
  }
  if (text.includes('installed access credential') && (text.includes('absent') || text.includes('remains absent'))) { expect((await observe(page)).accessPresent).toBe(false); return true; }
  if (text.includes('installed refresh credential remains R')) { expect(await equalsToken(page, 'refreshToken', s.refreshR)).toBe(true); return true; }
  if (text.includes('alert in the portal notification area displays exactly ')) {
    const expected = text.split('displays exactly ')[1].replace(/^"|"$/g, '');
    await expect(page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toHaveText(expected); return true;
  }
  return false;
}

export async function runSessionCase(page: Page, audit: AuditCapture, id: string, options: SessionOptions,
  operations: Partial<Record<number, (s: Session) => Promise<unknown>>> = {}) {
  const steps = await audit.defineCase(id);
  let s!: Session;
  for (const step of steps) {
    await audit.step(step.number, async () => {
      if (step.number === 1) { s = await sessionSetup(page, audit, options); return; }
      if (operations[step.number]) { await operations[step.number]!(s); return; }
      if (step.number === 2 && step.text.includes('selected fixture tab')) {
        const tabs = s.portal.root.getByRole('tablist', { name: 'workspaces', exact: true, includeHidden: true });
        const name = tabs.getByTestId('workspaces-tab-WS-A').getByRole('textbox', { name: 'Workspace Name', exact: true, includeHidden: true });
        await expect(name).toHaveValue('WS-A'); return;
      }
      if (step.number === 3 && (step.text.startsWith('access A ') || step.text.startsWith('refresh R is valid;') || step.text.startsWith('the browser '))) {
        expect(await equalsToken(page, 'token', s.accessA)).toBe(true);
        expect(await equalsToken(page, 'refreshToken', s.refreshR)).toBe(true); return;
      }
      if (await commonAssertion(page, s, step.text)) return;
      throw new Error(`No executable binding for ${id} step ${step.number}: ${step.text}`);
    });
  }
  await audit.record('session-observations', { requests: s.requests, state: await observe(page) });
}
