import type { Page, Route } from '@playwright/test';
import { expect, type AuditCapture } from './audit-fixture.js';
import { LoginPage } from '../pages/login.page.js';
import { PortalPage } from '../pages/portal.page.js';
import { acceptedLogin, blockExternal, credentials, localBase, localPrefix, openLogin,
  seedWorkspaces, workspace } from './local-app.js';

const loginPath = '/api/auth/v2/sso/login';
const hosts = ['localhost', 'fmo-mfe-dev.uk.dev.net', 'ratan-aws-sit-ns4-fmo-mfe.ir.standardchartered.com',
  'fmo-mfe.uk.dev.net', 'fmo-mfe-preprod.pi.dev.net', 'audit-prod.invalid'];
const errorAlert = (page: Page) => page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]');

/** Every branch performs the exact canonical action or predicate before automatic step capture. */
export async function runLoginCase(id: string, page: Page, audit: AuditCapture): Promise<void> {
  const steps = await audit.defineCase(id);
  const n = Number(id.slice(5));
  const posts: unknown[] = [];
  const pending: Route[] = [];
  let released = false;
  let login = new LoginPage(page, localPrefix);
  let hostname = 'localhost';
  let parameter: string | undefined;
  let started = 0;
  for (const step of steps) await audit.step(step.number, async () => {
    const text = step.text;
    if (step.number === 1) {
      const state = await page.context().storageState();
      expect(state.cookies).toHaveLength(0); expect(state.origins).toHaveLength(0);
      await blockExternal(page);
      await page.routeWebSocket('**/*', socket => socket.close());
      await audit.record('initial-context', { cookies: 0, origins: 0, isolatedPlaywrightContext: true,
        screenshotLimit: 'The initial browser page is about:blank because navigation has not occurred.' });
      return;
    }
    if (text.startsWith('the browser uses the ')) {
      hostname = hosts[Math.min(n - 1, 5)];
      parameter = ({ 7: 'Y', 8: 'y', 9: 'N', 10: 'true', 11: '1', 12: '' } as Record<number,string>)[n];
      if (hostname !== 'localhost') await page.route('**/*', async route => {
        const url = new URL(route.request().url());
        if (url.hostname === hostname) {
          const response = await route.fetch({ url: `${localBase}${url.pathname}${url.search}`, maxRedirects: 0 });
          await route.fulfill({ response });
        } else if (['localhost', '127.0.0.1', '[::1]'].includes(url.hostname)) {
          const response = await route.fetch({ maxRedirects: 0 }); await route.fulfill({ response });
        } else await route.abort('blockedbyclient');
      });
      await audit.record('environment-fixture', { hostname, parameter: parameter ?? null,
        limits: 'Hostname selection uses real source with local resource proxy. No deployed environment contacted.' });
      return;
    }
    if (text === 'the browser navigates to the configured portal entry URL') {
      await page.goto(`http://${hostname}:8128/${parameter === undefined ? '' : `?show_normal_login=${encodeURIComponent(parameter)}`}`);
      await login.expectVisible(); return;
    }
    if (text.startsWith('the LOCAL login page is visible')) {
      await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
      if (n === 25) {
        await page.addInitScript(() => {
          const state = { transitions: 0, writes: 0 };
          Object.defineProperty(window, '__auditAuthentication', { value: state });
          const original = Storage.prototype.setItem;
          Storage.prototype.setItem = function(key, value) {
            if (this === localStorage && key === 'SET_TOKEN') {
              state.writes += 1; if (!this.getItem(key) && value) state.transitions += 1;
            }
            return original.call(this, key, value);
          };
        });
      }
      await page.route(`**${loginPath}`, async route => {
        posts.push(route.request().postDataJSON());
        if (n === 22 || (n === 23 && posts.length === 1))
          await route.fulfill({ status: 401, contentType: 'application/json', body: JSON.stringify({ message: 'AuthenticationException' }) });
        else if ((n === 24 || n === 25) && !released || n === 27) pending.push(route);
        else if (n === 26) await route.abort('failed');
        else if (n === 28) await route.fulfill({ status: 503, body: '' });
        else await acceptedLogin(route);
      });
      login = await openLogin(page);
      await audit.record('controlled-service', { id, unsignedFixtureToken: true,
        identityAcceptance: 'NOT_VERIFIED', credentialService: 'Playwright route fixture', initialWorkspace: 'WS-A' });
      return;
    }
    const entered = /^User A enters "(.*)" into the .*placeholder "(Enter Username|Enter Password)"/.exec(text);
    if (entered) { await (entered[2] === 'Enter Username' ? login.fillUsername(entered[1]) : login.fillPassword(entered[1])); return; }
    if (text.startsWith('User A clears')) {
      await (text.includes('Enter Username') ? login.fillUsername('') : login.fillPassword('')); return;
    }
    if (text.startsWith('User A presses "Enter"')) {
      await (text.includes('Enter Username') ? login.usernameInput : login.passwordInput).press('Enter'); return;
    }
    if (text.startsWith('User A clicks the button labelled "Sign In"')) {
      started = Date.now();
      if (n === 25) {
        await expect(login.signInButton).toBeDisabled();
        const bounds = await login.signInButton.boundingBox(); expect(bounds).not.toBeNull();
        await page.mouse.click(bounds!.x + bounds!.width / 2, bounds!.y + bounds!.height / 2);
      } else await login.clickSignInButton();
      return;
    }
    if (text === 'the fixture releases all pending credential responses') {
      released = true; await Promise.all(pending.map(acceptedLogin)); return;
    }
    if (text.includes('tab labelled "WS-A"')) { await new PortalPage(page, localPrefix).expectWorkspaceTabVisible('WS-A'); return; }
    const visible = text.endsWith('is visible'), absent = text.endsWith('is absent');
    if ((visible || absent) && text.includes('on the login page')) {
      const locator = text.includes('Enter Username') ? login.usernameInput : text.includes('Enter Password') ? login.passwordInput
        : text.includes('Sign In With SSO') ? login.ssoLink : login.signInButton;
      if (absent) await expect(locator).toHaveCount(0); else await expect(locator).toBeVisible();
      return;
    }
    if (text.includes('has input type "password"')) { await login.expectPasswordMasked(); return; }
    if (text.includes('Sign In With SSO') && text.includes('disabled interaction')) { await expect(login.ssoLink).toHaveAttribute('aria-disabled', 'true'); return; }
    if (text.includes('button labelled "Sign In"') && text.endsWith('is disabled')) { await expect(login.signInButton).toBeDisabled(); return; }
    if (text.includes('button labelled "Sign In"') && text.endsWith('is enabled')) {
      await expect(login.signInButton).toBeEnabled({ timeout: n === 27 ? 70000 : 5000 }); return;
    }
    if (text.includes('progress indicator')) {
      await expect(login.signInButton.getByRole('progressbar')).toHaveCount(text.includes('contains one') ? 1 : 0); return;
    }
    if (text.includes('browser records zero')) {
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
      expect(posts).toHaveLength(0); await audit.record('credential-request-count', { count: posts.length }); return;
    }
    if (text.includes('browser records exactly one credential POST')) {
      expect(posts).toEqual([credentials]); await audit.record('credential-request-count', { count: posts.length, bodyMatched: true }); return;
    }
    if (text.startsWith('the credential POST body has ')) {
      const key = text.includes('username equal') ? 'username' : 'password';
      await expect.poll(() => posts.length).toBe(1);
      expect(posts[0]).toMatchObject({ [key]: credentials[key] });
      await audit.record('trimmed-field-observation', { key, matched: true, count: posts.length }); return;
    }
    if (text.includes('at most one effective transition')) {
      const observed = await page.evaluate(() => (window as unknown as { __auditAuthentication: { transitions: number; writes: number } }).__auditAuthentication);
      expect(observed.transitions).toBeLessThanOrEqual(1);
      await audit.record('authentication-transitions', { ...observed, requestCount: posts.length,
        limit: 'SET_TOKEN absent-to-present state; server transaction count remains unverified.' }); return;
    }
    if (text.includes('alert in the portal notification area displays exactly')) {
      const message = /displays exactly "(.*)"$/.exec(text)![1];
      await expect(errorAlert(page)).toHaveText(message, { timeout: n === 27 ? 70000 : 5000 });
      await audit.record('error-observation', { message, elapsedMs: Date.now() - started, requestCount: posts.length }); return;
    }
    if (text.startsWith('the alert containing ')) {
      await expect(errorAlert(page).filter({ hasText: /"(.*)"/.exec(text)![1] })).toHaveCount(0); return;
    }
    if (text === 'the portal notification area contains no authentication error alert') { await expect(errorAlert(page)).toHaveCount(0); return; }
    throw new Error(`Unbound canonical login step: ${text}`);
  });
}
