import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import type { Page, Route } from '@playwright/test';
import { test, expect, type AuditCapture } from '../support/audit-fixture.js';
import { blockExternal, localBase, localPrefix, workspace } from '../support/local-app.js';
import { PortalPage } from '../pages/portal.page.js';
import { LoginPage } from '../pages/login.page.js';

const T = Date.parse('2030-01-01T00:00:00.000Z');
const definitionPath = 'tasks/ui-test-coverage-20261022/test-cases.md';
const root = fileURLToPath(new URL('../../', import.meta.url));
const definitionHash = createHash('sha256').update(readFileSync(`${root}${definitionPath}`)).digest('hex');
const manifest = JSON.parse(readFileSync(`${root}tasks/ui-test-coverage-20261022/evidence/refinement/gherkin-manifest.json`, 'utf8'));
const authPath = '/api/auth/v2/sso/';
type RecordedRequest = { endpoint: string; controlledTimeMs: number; bodyMatchesAccessA: boolean; refreshMatchesR: boolean };
type StoreView = { token?: string; refreshToken?: string; expiredIn?: number; isOnLogout?: boolean };
type Mfe = {
  Hooks: { getHooks(): { store: StoreView } };
  Service: { getRefreshToken(): Promise<void> | void;
    postService(path: string, data: unknown, config?: unknown): Promise<{ data: { result?: boolean } }> };
};
type BrowserWithSystem = Window & { System: { import(name: string): Promise<Mfe> } };

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES', serviceWorkers: 'block',
  auditFixture: 'Actual mfe-base React with Playwright clock emulation. Unsigned browser-only JWT fixtures and controlled API responses. No natural lifecycle, real identity, or BFF expiry claim.' });

function token(expiryOffsetSeconds: number, name: string): string {
  const encode = (value: unknown) => Buffer.from(JSON.stringify(value)).toString('base64url');
  return `Bearer ${encode({ alg: 'none', typ: 'JWT' })}.${encode({ sub: 'user-a', iat: T / 1000 - 60,
    exp: T / 1000 + expiryOffsetSeconds, fixture: name })}.fixture`;
}

function ref(id: string): string {
  const steps = manifest.scenarios[id].steps as Record<string, { kind: string }>;
  return `${definitionPath}; ${id}; assertion lines ${Object.keys(steps).filter(line => steps[line].kind === 'assertion').join(', ')}`;
}

async function mapping(audit: AuditCapture, id: string): Promise<void> {
  const definition = manifest.scenarios[id];
  expect(definition.sha256).toBe(definitionHash);
  await audit.record('canonical-mapping', { id, definition: definitionPath, sha256: definitionHash,
    assertionLines: Object.entries(definition.steps).filter(([, value]) =>
      (value as { kind: string }).kind === 'assertion').map(([line]) => Number(line)),
    clock: { start: new Date(T).toISOString(), type: 'Playwright clock emulation installed before navigation' },
    limits: ['This run measures application timers under clock emulation.',
      'It does not establish natural background, visibility, suspension, or identity-provider behavior.',
      'All access and refresh credentials are unsigned local fixtures. No real service accepts these fixtures.'] });
}

async function storeObservation(page: Page, accessA: string, refreshR?: string) {
  return page.evaluate(async ({ accessA, refreshR }) => {
    const module = await (window as unknown as BrowserWithSystem).System.import('@fm/base');
    const store = module.Hooks.getHooks().store;
    return { controlledTimeMs: Date.now(), accessExpiryMs: (store.expiredIn ?? 0) * 1000,
      accessEqualsA: store.token === accessA, accessPresent: Boolean(store.token),
      refreshEqualsR: refreshR === undefined ? store.refreshToken === undefined : store.refreshToken === refreshR,
      refreshPresent: Boolean(store.refreshToken), isOnLogout: Boolean(store.isOnLogout),
      documentVisibility: document.visibilityState };
  }, { accessA, refreshR });
}

async function runTo(page: Page, offsetMs: number): Promise<void> {
  const now = await page.evaluate(() => Date.now());
  const remaining = T + offsetMs - now;
  expect(remaining).toBeGreaterThanOrEqual(0);
  await page.clock.runFor(remaining);
  expect(await page.evaluate(() => Date.now())).toBe(T + offsetMs);
}

async function setup(page: Page, audit: AuditCapture, id: string,
  options: { accessExpires?: number; refreshExpires?: number; acquisitionFails?: boolean } = {}) {
  await mapping(audit, id);
  await blockExternal(page);
  await page.routeWebSocket('**/*', socket => socket.close());
  const accessA = token(options.accessExpires ?? 900, 'A');
  const refreshR = options.refreshExpires === undefined ? undefined : token(options.refreshExpires, 'R');
  const requests: RecordedRequest[] = [];
  const pending: Route[] = [];
  await page.addInitScript(({ access, workspaces }) => {
    localStorage.setItem('SET_TOKEN', access);
    sessionStorage.setItem('SET_TOKEN', access);
    localStorage.setItem('SET_USER', JSON.stringify({ sub: 'user-a', userId: 'user-a', fullName: 'Audit User A' }));
    localStorage.setItem('SET_WORKSPACES', JSON.stringify(workspaces));
  }, { access: accessA, workspaces: [workspace('WS-A', 'WS-A')] });
  await page.clock.install({ time: new Date(T - 60000) });
  await page.route('**/api/**', async route => {
    const request = route.request();
    const path = new URL(request.url()).pathname;
    if (!path.startsWith(authPath)) {
      await route.fulfill({ status: 200, json: {} });
      return;
    }
    const endpoint = path.slice(authPath.length);
    const body = request.postDataJSON() as { singleUIAuthorization?: string } | null;
    requests.push({ endpoint, controlledTimeMs: await page.evaluate(() => Date.now()),
      bodyMatchesAccessA: body?.singleUIAuthorization === accessA,
      refreshMatchesR: request.headers()['single-ui-refresh'] === refreshR });
    if (endpoint === 'validate') await route.fulfill({ status: 200,
      headers: { 'single-ui-authorization': accessA }, json: { result: true, entities: [],
        userInfo: JSON.stringify({ sub: 'user-a', fullName: 'Audit User A' }) } });
    else if (endpoint === 'refreshtoken') {
      if (options.acquisitionFails) await route.fulfill({ status: 503, body: '' });
      else await route.fulfill({ status: 200,
        headers: { 'single-ui-refresh': refreshR ?? token(13524, 'R') }, json: { result: true } });
    } else if (endpoint === 'relogin') pending.push(route);
    else await route.fulfill({ status: 200, json: { result: true } });
  });
  await page.goto(`${localBase}/?show_normal_login=Y`);
  const portal = new PortalPage(page, localPrefix);
  await portal.expectVisible();
  await portal.expectWorkspaceTabVisible('WS-A');
  if (refreshR) {
    // The fixture invokes the actual exported acquisition service to establish the canonical refresh setup.
    await page.evaluate(async () => {
      const module = await (window as unknown as BrowserWithSystem).System.import('@fm/base');
      await module.Service.getRefreshToken();
    });
    await expect.poll(async () => (await storeObservation(page, accessA, refreshR)).refreshEqualsR).toBe(true);
  }
  await page.clock.pauseAt(new Date(T));
  const initial = await storeObservation(page, accessA, refreshR);
  expect(initial.documentVisibility).toBe('visible');
  expect(initial.accessEqualsA).toBe(true);
  expect(initial.refreshEqualsR).toBe(true);
  await audit.record('controlled-setup', { ...initial, accessExpiryOffsetSeconds: options.accessExpires ?? 900,
    refreshExpiryOffsetSeconds: options.refreshExpires ?? null,
    refreshSetup: refreshR ? 'Fixture called actual exported acquisition service before T; counters reset afterward.' : 'No refresh credential at T.',
    noMouseActivityAfterSetup: true, credentials: 'Unsigned fixture values; equality booleans only in observation records.' });
  requests.length = 0;
  await audit.capture('controlled-session-start', 'WS-A is present at controlled time T before the named timer action.', ref(id));
  return { portal, accessA, refreshR, requests, pending };
}

test('AUTH-043 acquire recovery at T+875 without moving access expiry', async ({ page, audit }) => {
  const { portal, accessA, requests } = await setup(page, audit, 'AUTH-043');
  await runTo(page, 875000);
  await expect.poll(() => requests.filter(request => request.endpoint === 'refreshtoken').length).toBe(1);
  await portal.expectWorkspaceTabVisible('WS-A');
  await portal.sessionTimeoutDialog.expectAbsent();
  const observation = await storeObservation(page, accessA);
  expect(observation.accessExpiryMs).toBe(T + 900000);
  expect(observation.accessEqualsA).toBe(true);
  await audit.record('deadline-assertions', { requests, observation,
    expectedRefreshPostCount: 1, expectedAccessExpiryMs: T + 900000 });
  await audit.capture('recovery-acquired-before-expiry', 'WS-A remains visible without the expiry dialog at T+875 seconds.', ref('AUTH-043'));
});

test('AUTH-044 do not acquire recovery at T+874.999', async ({ page, audit }) => {
  const { portal, accessA, requests } = await setup(page, audit, 'AUTH-044');
  await runTo(page, 874999);
  expect(requests.filter(request => request.endpoint === 'refreshtoken')).toHaveLength(0);
  await portal.expectWorkspaceTabVisible('WS-A');
  await portal.sessionTimeoutDialog.expectAbsent();
  await audit.record('deadline-assertions', { requests, observation: await storeObservation(page, accessA),
    expectedRefreshPostCount: 0 });
  await audit.capture('before-acquisition-deadline', 'WS-A remains visible without the expiry dialog immediately before acquisition.', ref('AUTH-044'));
});

for (const [id, target] of [['AUTH-076', 900000], ['AUTH-077', 899999]] as const) {
  test(`${id} access expiry boundary at T+${target}ms`, async ({ page, audit }) => {
    const { portal, accessA, refreshR, requests } = await setup(page, audit, id, { refreshExpires: 13524 });
    await runTo(page, target);
    if (id === 'AUTH-076') {
      await portal.sessionTimeoutDialog.expectVisible();
      await expect(portal.sessionTimeoutDialog.dialog).toHaveCount(1);
      await expect(portal.sessionTimeoutDialog.extendButton).toBeVisible();
      await expect(portal.sessionTimeoutDialog.logoutButton).toBeVisible();
      expect(requests.filter(request => request.endpoint === 'relogin')).toHaveLength(0);
    } else {
      await portal.sessionTimeoutDialog.expectAbsent();
      await portal.expectWorkspaceTabVisible('WS-A');
    }
    await audit.record('expiry-boundary-assertions', { requests, observation: await storeObservation(page, accessA, refreshR),
      targetOffsetMs: target, expiryDialogExpected: id === 'AUTH-076' });
    await audit.capture('access-expiry-boundary', id === 'AUTH-076'
      ? 'Exactly one expiry dialog presents Extend and Logout at T+900 seconds.'
      : 'WS-A is visible without the expiry dialog at T+899.999 seconds.', ref(id));
  });
}

async function expectSignedOut(page: Page, portal: PortalPage): Promise<void> {
  const login = new LoginPage(page, localPrefix);
  await login.expectVisible();
  await expect(login.usernameInput).toBeVisible();
  await expect(login.passwordInput).toBeVisible();
  await expect(login.signInButton).toBeVisible();
  await expect(portal.workspaceList).toHaveCount(0);
}

test('AUTH-080 Logout clears local access after the 1000ms delay', async ({ page, audit }) => {
  const { portal, accessA, refreshR, requests } = await setup(page, audit, 'AUTH-080', { accessExpires: 0, refreshExpires: 600 });
  await portal.sessionTimeoutDialog.expectVisible();
  await audit.capture('expiry-decision', 'The expired-access dialog presents Logout and Extend.', ref('AUTH-080'));
  await expect(portal.sessionTimeoutDialog.logoutButton).toBeEnabled();
  // Forced pointer dispatch avoids Playwright stability frames while requestAnimationFrame is paused.
  await portal.sessionTimeoutDialog.logoutButton.click({ force: true });
  await audit.capture('logout-delay-pending', 'Logout has started while the 1000-millisecond application delay is pending.', ref('AUTH-080'));
  await page.clock.runFor(1000);
  await expectSignedOut(page, portal);
  await portal.sessionTimeoutDialog.expectAbsent();
  const storage = await page.evaluate(() => ({ localAccessPresent: Boolean(localStorage.getItem('SET_TOKEN')),
    sessionAccessPresent: Boolean(sessionStorage.getItem('SET_TOKEN')) }));
  expect(storage).toEqual({ localAccessPresent: false, sessionAccessPresent: false });
  await audit.record('logout-assertions', { requests, storage, observation: await storeObservation(page, accessA, refreshR) });
  await audit.capture('signed-out-after-delay', 'Login controls are visible without the workspace tablist or expiry dialog.', ref('AUTH-080'));
});

test('AUTH-081 missing refresh logs out at access expiry', async ({ page, audit }) => {
  const { portal, accessA, requests } = await setup(page, audit, 'AUTH-081', { acquisitionFails: true });
  await runTo(page, 875000);
  await expect.poll(() => requests.filter(request => request.endpoint === 'refreshtoken').length).toBe(1);
  await expect(page.getByRole('alert')).toHaveText('/api/auth/v2/sso/refreshtoken : Request failed with status code 503');
  const beforeExpiry = await storeObservation(page, accessA);
  expect(beforeExpiry.refreshPresent).toBe(false);
  await audit.capture('recovery-acquisition-failed', 'WS-A remains visible after the controlled acquisition failure.', ref('AUTH-081'));
  await runTo(page, 900000);
  await portal.sessionTimeoutDialog.expectVisible();
  await audit.capture('expiry-without-refresh', 'The expiry component mounted without a refresh credential.', ref('AUTH-081'));
  await page.clock.runFor(1000);
  await expectSignedOut(page, portal);
  expect(requests.filter(request => request.endpoint === 'relogin')).toHaveLength(0);
  await audit.record('missing-refresh-assertions', { requests, observation: await storeObservation(page, accessA),
    recoveryCredentialAbsentBeforeExpiry: true, expectedReloginPosts: 0 });
  await audit.capture('signed-out-without-recovery', 'Login controls replace Home after the logout delay.', ref('AUTH-081'));
});

for (const [id, target] of [['AUTH-083', 598000], ['AUTH-084', 597999]] as const) {
  test(`${id} open-dialog refresh cutoff at T+${target}ms`, async ({ page, audit }) => {
    const { portal, accessA, refreshR, requests } = await setup(page, audit, id, { accessExpires: 0, refreshExpires: 600 });
    await portal.sessionTimeoutDialog.expectVisible();
    await audit.capture('expiry-decision', 'The expired-access dialog is visible before its refresh cutoff.', ref(id));
    await runTo(page, target);
    if (id === 'AUTH-084') {
      await expect(portal.sessionTimeoutDialog.extendButton).toBeEnabled();
      await portal.sessionTimeoutDialog.expectVisible();
    } else {
      await expect(portal.sessionTimeoutDialog.extendButton).toBeDisabled();
      const state = await storeObservation(page, accessA, refreshR);
      expect(state.isOnLogout).toBe(true);
      await audit.record('cutoff-state', state);
      await audit.capture('cutoff-starts-logout', 'Extend is disabled at the two-second refresh cutoff.', ref(id));
      await runTo(page, 599000);
      await expectSignedOut(page, portal);
    }
    await audit.record('cutoff-assertions', { requests, observation: await storeObservation(page, accessA, refreshR), targetOffsetMs: target });
    await audit.capture('refresh-cutoff-result', id === 'AUTH-084'
      ? 'Extend is available at T+597.999 seconds.' : 'Login controls replace Home at T+599 seconds.', ref(id));
  });
}

test('AUTH-078 manual Extend installs response B and sends controlled validation with B', async ({ page, audit }) => {
  const { portal, accessA, refreshR, requests, pending } = await setup(page, audit, 'AUTH-078', { accessExpires: 0, refreshExpires: 600 });
  await portal.sessionTimeoutDialog.expectVisible();
  await audit.capture('expiry-decision', 'The expiration dialog is visible with a valid browser refresh fixture.', ref('AUTH-078'));
  await expect(portal.sessionTimeoutDialog.extendButton).toBeEnabled();
  await portal.sessionTimeoutDialog.extendButton.click({ force: true });
  await expect.poll(() => pending.length).toBe(1);
  await portal.sessionTimeoutDialog.expectAbsent();
  const recoveryRequests = requests.filter(request => request.endpoint === 'relogin');
  expect(recoveryRequests).toHaveLength(1);
  expect(recoveryRequests[0].refreshMatchesR).toBe(true);
  await audit.capture('recovery-pending', 'The dialog is absent while the controlled relogin response remains pending.', ref('AUTH-078'));
  const accessB = token(900, 'B');
  await pending[0].fulfill({ status: 200, headers: { 'single-ui-authorization': accessB },
    json: { result: true, entities: [], userInfo: JSON.stringify({ sub: 'user-a', fullName: 'Audit User A' }) } });
  await portal.expectWorkspaceTabVisible('WS-A');
  await expect.poll(async () => page.evaluate(async expected => {
    const module = await (window as unknown as BrowserWithSystem).System.import('@fm/base');
    return module.Hooks.getHooks().store.token === expected;
  }, accessB)).toBe(true);
  // This is an independent application HTTP operation after response installation.
  let validationMatchesB = false;
  await page.route('**/api/auth/v2/sso/validate', async route => {
    validationMatchesB = route.request().postDataJSON()?.singleUIAuthorization === accessB;
    await route.fulfill({ status: 200, json: { result: validationMatchesB } });
  });
  const validation = await page.evaluate(async expected => {
    const module = await (window as unknown as BrowserWithSystem).System.import('@fm/base');
    const installed = module.Hooks.getHooks().store.token;
    const response = await module.Service.postService('/auth/v2/sso/validate', { singleUIAuthorization: installed },
      { headers: { 'show-loading': 'false' } });
    return { installedMatchesB: installed === expected, result: response.data.result === true };
  }, accessB);
  expect(validation).toEqual({ installedMatchesB: true, result: true });
  expect(validationMatchesB).toBe(true);
  await audit.record('recovery-independent-assertions', { reloginPosts: recoveryRequests.length,
    refreshHeaderEqualsR: recoveryRequests[0].refreshMatchesR, installedAccessEqualsB: validation.installedMatchesB,
    controlledValidationBodyEqualsB: validationMatchesB, controlledValidationResult: validation.result,
    responseAcceptance: 'CONTROLLED_FIXTURE', realAuthenticationAcceptance: 'NOT_VERIFIED',
    observation: await storeObservation(page, accessA, refreshR) });
  await audit.capture('recovered-and-validated', 'WS-A is visible after installing B and the controlled validation operation.', ref('AUTH-078'));
});
