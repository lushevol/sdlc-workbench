import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import type { Page, Route } from '@playwright/test';
import { test, expect, type AuditCapture } from '../support/audit-fixture.js';
import { LoginPage } from '../pages/login.page.js';
import { PortalPage } from '../pages/portal.page.js';
import { acceptedLogin, blockExternal, credentials, localBase, localPrefix, openLogin,
  seedWorkspaces, workspace } from '../support/local-app.js';

const catalogPath = 'tasks/ui-test-coverage-20261022/test-cases.md';
const root = fileURLToPath(new URL('../../', import.meta.url));
const catalogBytes = readFileSync(`${root}${catalogPath}`);
const catalogSha256 = createHash('sha256').update(catalogBytes).digest('hex');
const manifest = JSON.parse(readFileSync(`${root}tasks/ui-test-coverage-20261022/evidence/refinement/gherkin-manifest.json`, 'utf8'));
const rejectedMessage = 'Invalid username and password combination or SSO service is unavailable.';
const loginPath = '/api/auth/v2/sso/login';

test.use({
  auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual mfe-base React application from the local webpack server. Controlled login API responses; no external identity service.',
  serviceWorkers: 'block',
});

test.beforeEach(async ({ page, audit }) => {
  const initial = await page.context().storageState();
  expect(initial.cookies).toHaveLength(0);
  expect(initial.origins).toHaveLength(0);
  await audit.record('initial-context', { cookies: 0, origins: 0, isolatedPlaywrightContext: true });
  await blockExternal(page);
  // Route every WebSocket before connection. The development client must not contact company hosts.
  await page.routeWebSocket('**/*', socket => socket.close());
});

async function canonical(audit: AuditCapture, id: string, limits: string[] = []): Promise<void> {
  const definition = manifest.scenarios[id];
  expect(catalogSha256).toBe(definition.sha256);
  await audit.record('canonical-mapping', { id, catalog: catalogPath, sha256: catalogSha256,
    assertionLines: Object.entries(definition.steps).filter(([, step]) =>
      (step as { kind: string }).kind === 'assertion').map(([line]) => Number(line)),
    scope: 'Actual React browser behavior with controlled API responses',
    limits: ['This run does not execute the BFF, SSO provider, or deployed environment.', ...limits] });
}

function reference(id: string): string {
  const lines = Object.keys(manifest.scenarios[id].steps).map(Number);
  return `${catalogPath}#L${Math.min(...lines)}; canonical assertion lines ${lines.filter(line =>
    manifest.scenarios[id].steps[String(line)].kind === 'assertion').join(', ')}`;
}

async function expectCredentials(login: LoginPage, visible = true): Promise<void> {
  for (const locator of [login.usernameInput, login.passwordInput, login.signInButton]) {
    if (visible) { await expect(locator).toHaveCount(1); await expect(locator).toBeVisible(); }
    else await expect(locator).toHaveCount(0);
  }
}

function errorAlert(page: Page) {
  // Snackbar/index.tsx nests SnackbarContent inside MuiAlert. Both expose alert roles.
  return page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]');
}

async function expectError(page: Page, message: string, timeout = 5000): Promise<void> {
  const content = errorAlert(page);
  await expect(content).toHaveCount(1, { timeout });
  await expect(content).toHaveText(message, { timeout });
}

async function fillValid(login: LoginPage): Promise<void> {
  await login.fillUsername(credentials.username);
  await login.fillPassword(credentials.password);
}

async function rejected(route: Route): Promise<void> {
  await route.fulfill({ status: 401, contentType: 'application/json',
    body: JSON.stringify({ message: 'AuthenticationException' }) });
}

/** Preserve the real hostname decision while fetching every application byte from localhost. */
async function openEnvironment(page: Page, hostname: string, parameter?: string): Promise<LoginPage> {
  const local = new URL(localBase);
  if (hostname !== 'localhost') {
    await page.route('**/*', async route => {
      const url = new URL(route.request().url());
      if (url.hostname === hostname) {
        const response = await route.fetch({ url: `${local.origin}${url.pathname}${url.search}`, maxRedirects: 0 });
        await route.fulfill({ response });
      } else if (['localhost', '127.0.0.1', '[::1]'].includes(url.hostname)) {
        // The emulated hostname must not make a browser connection into loopback.
        // API transport retains source bytes without Chromium's private-network block.
        const response = await route.fetch({ maxRedirects: 0 });
        await route.fulfill({ response });
      }
      else await route.abort('blockedbyclient');
    });
  }
  const query = parameter === undefined ? '' : `?show_normal_login=${encodeURIComponent(parameter)}`;
  await page.goto(`http://${hostname}:${local.port}/${query}`);
  const login = new LoginPage(page, localPrefix);
  await login.expectVisible();
  return login;
}

const environments = [
  { id: 'AUTH-001', environment: 'LOCAL', hostname: 'localhost', visible: true },
  { id: 'AUTH-002', environment: 'DEV', hostname: 'fmo-mfe-dev.uk.dev.net', visible: true },
  { id: 'AUTH-003', environment: 'SIT', hostname: 'ratan-aws-sit-ns4-fmo-mfe.ir.standardchartered.com', visible: true },
  { id: 'AUTH-004', environment: 'UAT', hostname: 'fmo-mfe.uk.dev.net', visible: true },
  { id: 'AUTH-005', environment: 'PRE-PROD', hostname: 'fmo-mfe-preprod.pi.dev.net', visible: true },
  { id: 'AUTH-006', environment: 'PROD', hostname: 'audit-prod.invalid', visible: false },
  { id: 'AUTH-007', environment: 'PROD', hostname: 'audit-prod.invalid', parameter: 'Y', visible: true },
  { id: 'AUTH-008', environment: 'PROD', hostname: 'audit-prod.invalid', parameter: 'y', visible: true },
  { id: 'AUTH-009', environment: 'PROD', hostname: 'audit-prod.invalid', parameter: 'N', visible: false },
  { id: 'AUTH-010', environment: 'PROD', hostname: 'audit-prod.invalid', parameter: 'true', visible: false },
  { id: 'AUTH-011', environment: 'PROD', hostname: 'audit-prod.invalid', parameter: '1', visible: false },
  { id: 'AUTH-012', environment: 'PROD', hostname: 'audit-prod.invalid', parameter: '', visible: false },
];

for (const setting of environments) {
  test(`${setting.id} actual React ${setting.environment} credential visibility ${setting.parameter ?? 'without parameter'}`, async ({ page, audit }) => {
    await canonical(audit, setting.id, ['The hostname is a local route proxy. No deployed environment was contacted.']);
    const login = await openEnvironment(page, setting.hostname, setting.parameter);
    await audit.capture('entry-page', `The actual React entry page for ${setting.environment}.`, reference(setting.id));
    await expectCredentials(login, setting.visible);
    if (setting.id === 'AUTH-001' || !setting.visible) await expect(login.ssoLink).toBeVisible();
    if (setting.id === 'AUTH-001') await login.expectPasswordMasked();
    await audit.record('environment-observation', { hostname: await page.evaluate(() => location.hostname),
      expectedEnvironment: setting.environment, parameter: setting.parameter ?? null,
      credentialsVisible: setting.visible, allNonlocalRequestsInterceptedOrBlocked: true });
    await audit.capture('asserted-entry-state', 'The credential controls have the canonical visibility state.', reference(setting.id));
  });
}

const incomplete = [
  { id: 'AUTH-013', username: '', password: credentials.password },
  { id: 'AUTH-014', username: credentials.username, password: '' },
  { id: 'AUTH-015', username: '', password: '' },
  { id: 'AUTH-021', username: '   ', password: '   ' },
];
for (const input of incomplete) {
  test(`${input.id} actual React prevents incomplete credential submission`, async ({ page, audit }) => {
    await canonical(audit, input.id);
    const requests: { method: string; pathname: string }[] = [];
    page.on('request', request => {
      if (request.method() === 'POST' && new URL(request.url()).pathname === loginPath)
        requests.push({ method: 'POST', pathname: loginPath });
    });
    await page.route(`**${loginPath}`, route => route.fulfill({ status: 400, body: '' }));
    const login = await openLogin(page);
    await audit.capture('login-ready', 'The LOCAL login page is visible before credential input.', reference(input.id));
    await login.fillUsername(input.username);
    await login.fillPassword(input.password);
    await audit.capture('input-ready', 'The canonical incomplete input is present before submission.', reference(input.id));
    await login.clickSignInButton();
    await expectCredentials(login);
    // The click and two animation frames complete the synchronous React submission handler.
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    await audit.record('credential-request-observation', { requests, count: requests.length,
      boundary: 'From page creation through the completed click handler and two animation frames.' });
    expect(requests).toHaveLength(0);
    await audit.capture('submission-prevented', 'The sign-in controls remain visible after the incomplete submission.', reference(input.id));
  });
}

test('AUTH-022 actual React displays the rejected-login message', async ({ page, audit }) => {
  await canonical(audit, 'AUTH-022');
  await page.route(`**${loginPath}`, rejected);
  const login = await openLogin(page);
  await audit.capture('login-ready', 'The LOCAL login page is visible.', reference('AUTH-022'));
  await login.fillUsername(credentials.username);
  await login.fillPassword('WrongPass');
  await login.clickSignInButton();
  await expectCredentials(login);
  await expectError(page, rejectedMessage);
  await audit.capture('rejected-login', 'The notification displays the exact canonical authentication error.', reference('AUTH-022'));
});

test('AUTH-023 actual React recovers after an invalid password', async ({ page, audit }) => {
  await canonical(audit, 'AUTH-023', ['WS-A is seeded in local browser workspace storage.']);
  await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
  let submissions = 0;
  await page.route(`**${loginPath}`, async route => {
    submissions += 1;
    if (submissions === 1) await rejected(route);
    else await acceptedLogin(route);
  });
  const login = await openLogin(page);
  await audit.capture('login-ready', 'The LOCAL login page is visible.', reference('AUTH-023'));
  await login.fillUsername(credentials.username);
  await login.fillPassword('WrongPass');
  await login.clickSignInButton();
  await expectError(page, rejectedMessage);
  await audit.capture('first-login-rejected', 'The first login displays the canonical error.', reference('AUTH-023'));
  await login.fillPassword(credentials.password);
  await login.clickSignInButton();
  await expect(errorAlert(page).filter({ hasText: rejectedMessage })).toHaveCount(0);
  const portal = new PortalPage(page, localPrefix);
  await portal.expectVisible();
  await portal.expectWorkspaceTabVisible('WS-A');
  await audit.record('retry-observation', { submissions, fixtureResponseOrder: ['AuthenticationException', 'valid user-a data'] });
  await audit.capture('recovered-workspace', 'WS-A is visible and the rejected-login error is absent.', reference('AUTH-023'));
});

test('AUTH-024 actual React disables sign-in controls during a pending request', async ({ page, audit }) => {
  await canonical(audit, 'AUTH-024');
  const pending: Route[] = [];
  await page.route(`**${loginPath}`, route => { pending.push(route); });
  const login = await openLogin(page);
  await audit.capture('login-ready', 'The LOCAL login page is visible.', reference('AUTH-024'));
  await fillValid(login);
  await login.clickSignInButton();
  await expect.poll(() => pending.length).toBe(1);
  await expect(login.signInButton).toBeDisabled();
  await expect(login.signInButton.getByRole('progressbar')).toHaveCount(1);
  await expect(login.ssoLink).toHaveAttribute('aria-disabled', 'true');
  await audit.record('pending-observation', { pendingRequests: pending.length, responseReleased: false,
    ssoDisabledPredicate: 'aria-disabled=true', signInProgressIndicators: 1 });
  await audit.capture('pending-controls-disabled', 'Sign In and SSO are disabled while the credential response remains pending.', reference('AUTH-024'));
});

test('AUTH-025 actual React handles repeated sign-in input', async ({ page, audit }) => {
  await canonical(audit, 'AUTH-025', ['Effective transition means the local SET_TOKEN value changes from absent to present.',
    'This browser predicate does not prove one server-side session or one identity-provider transaction.']);
  test.info().annotations.push({ type: 'canonical-limit', description: 'Effective transition is scoped to local SET_TOKEN absent-to-present state.' });
  await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
  await page.addInitScript(() => {
    const state = { transitions: 0, writes: 0 };
    Object.defineProperty(window, '__auditAuthentication', { value: state });
    const original = Storage.prototype.setItem;
    Storage.prototype.setItem = function (key, value) {
      if (this === localStorage && key === 'SET_TOKEN') {
        state.writes += 1;
        if (!this.getItem(key) && value) state.transitions += 1;
      }
      return original.call(this, key, value);
    };
  });
  const pending: Route[] = [];
  let released = false;
  await page.route(`**${loginPath}`, async route => {
    if (released) await acceptedLogin(route);
    else pending.push(route);
  });
  const login = await openLogin(page);
  await audit.capture('login-ready', 'The LOCAL login page is visible.', reference('AUTH-025'));
  await fillValid(login);
  await login.usernameInput.press('Enter');
  await login.usernameInput.press('Enter');
  await expect(login.signInButton).toBeDisabled();
  const bounds = await login.signInButton.boundingBox();
  expect(bounds).not.toBeNull();
  await page.mouse.click(bounds!.x + bounds!.width / 2, bounds!.y + bounds!.height / 2);
  await audit.capture('repeated-input-pending', 'Repeated Enter and the pointer click occurred while login responses remained pending.', reference('AUTH-025'));
  released = true;
  await Promise.all(pending.map(acceptedLogin));
  const portal = new PortalPage(page, localPrefix);
  await portal.expectWorkspaceTabVisible('WS-A');
  const observations = await page.evaluate(() =>
    (window as unknown as { __auditAuthentication: { transitions: number; writes: number } }).__auditAuthentication);
  await audit.record('authentication-observation', { ...observations, credentialRequests: pending.length,
    predicate: 'SET_TOKEN absent-to-present transitions; no token values retained' });
  expect(observations.transitions).toBeLessThanOrEqual(1);
  await expect(errorAlert(page)).toHaveCount(0);
  await audit.capture('authenticated-after-repeated-input', 'WS-A is visible without an authentication error.', reference('AUTH-025'));
});

const failures = [
  { id: 'AUTH-026', mode: 'network', expected: 'Error happened, service is unavailable, pls check with support team: /api/auth/v2/sso/login: API request failed' },
  { id: 'AUTH-027', mode: 'timeout', expected: '/api/auth/v2/sso/login : timeout of 60000ms exceeded' },
  { id: 'AUTH-028', mode: '503', expected: '/api/auth/v2/sso/login : Request failed with status code 503' },
];
for (const failure of failures) {
  test(`${failure.id} actual React recovers controls after ${failure.mode}`, async ({ page, audit }) => {
    if (failure.mode === 'timeout') test.setTimeout(85000);
    await canonical(audit, failure.id);
    const pending: Route[] = [];
    await page.route(`**${loginPath}`, async route => {
      if (failure.mode === 'network') await route.abort('failed');
      else if (failure.mode === '503') await route.fulfill({ status: 503, body: '' });
      else pending.push(route);
    });
    const login = await openLogin(page);
    await audit.capture('login-ready', 'The LOCAL login page is visible before the transport failure.', reference(failure.id));
    await fillValid(login);
    const started = Date.now();
    await login.clickSignInButton();
    if (failure.mode === 'timeout') {
      await expect(login.signInButton).toBeDisabled();
      await audit.capture('request-pending', 'The credential request is pending before its native Axios timeout.', reference(failure.id));
    }
    await expectError(page, failure.expected, failure.mode === 'timeout' ? 70000 : 5000);
    await expectCredentials(login);
    await expect(login.signInButton).toBeEnabled();
    await expect(login.signInButton.getByRole('progressbar')).toHaveCount(0);
    await audit.record('transport-failure-observation', { mode: failure.mode, elapsedMs: Date.now() - started,
      responseBody: null, exactError: failure.expected, nativeAxiosTimeoutMs: failure.mode === 'timeout' ? 60000 : null });
    await audit.capture('transport-failure-recovered', 'Sign In is enabled without a progress indicator and the exact error is visible.', reference(failure.id));
  });
}
