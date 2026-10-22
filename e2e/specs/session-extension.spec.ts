import { test, expect, installPortalFixture, fixtureCredentials, fixturePrefix } from '../fixtures/portal.fixture.js';
import { extendSessionAndVerifyAuthentication } from '../flows/session-extension.flow.js';
import { SessionTimeoutDialog } from '../components/session-timeout.dialog.js';
import { createActions, createPom, executeAction } from '../catalog/actions.js';
import { executeSteps, validateSteps } from '../ai/runner.js';
import { sha256 } from '../support/results.js';
import type { Route } from '@playwright/test';

const refreshCredentialSha256 = sha256(fixtureCredentials.refresh);

test.describe('Synthetic session fixture: harness mechanics only', () => {
  test('AUTH-078 partial binding: independent renewal and authentication predicates', async ({ page, portalFixture }) => {
    const result = await extendSessionAndVerifyAuthentication(createPom(page, fixturePrefix).portal, { scope: 'synthetic-fixture', workspaceName: 'WS-A',
      releaseRenewal: portalFixture.releaseRenewal, refreshCredentialSha256 });
    expect(result.status).toBe('passed');
    expect(result.assertions).toHaveLength(8);
    expect(result.assertions.every(assertion => assertion.status === 'passed')).toBe(true);
    expect(result.observations.sessionValid).toBe(true);
    const evidence = JSON.stringify(result);
    for (const credential of Object.values(fixtureCredentials)) expect(evidence).not.toContain(credential);
  });

  for (const options of [
    { validationResult: false }, { validationStatus: 500 }, { renewalStatus: 401 },
    { installWrongToken: true }, { wrongRefresh: true }, { duplicateRenewal: true },
  ]) {
    test(`fails independent predicates for ${JSON.stringify(options)}`, async ({ page }) => {
      const fixture = await installPortalFixture(page, options);
      try {
        const result = await extendSessionAndVerifyAuthentication(createPom(page, fixturePrefix).portal, { scope: 'synthetic-fixture', workspaceName: 'WS-A',
          releaseRenewal: fixture.releaseRenewal, timeoutMs: 500, refreshCredentialSha256 });
        expect(result.status).toBe('failed');
        expect(result.assertions.some(assertion => assertion.status === 'failed')).toBe(true);
        if ('validationResult' in options || 'validationStatus' in options) expect(result.observations.sessionValid).toBe(false);
      } finally { await fixture.cleanup(); }
    });
  }

  test('a completed click does not claim valid authentication', async ({ page, portalFixture }) => {
    const result = await executeAction(createActions(createPom(page, fixturePrefix)), 'session.extend', true);
    expect(result.status).toBe('passed');
    expect(result.observations).toMatchObject({ clickCompleted: true, sessionValid: null });
    expect(await page.evaluate(() => localStorage.getItem('SET_TOKEN'))).toBe(fixtureCredentials.access);
    portalFixture.releaseRenewal();
  });

  test('an unresponsive validation endpoint cannot hang the flow', async ({ page }) => {
    const fixture = await installPortalFixture(page, { holdValidation: true });
    try {
      const started = Date.now();
      const result = await extendSessionAndVerifyAuthentication(createPom(page, fixturePrefix).portal, {
        scope: 'synthetic-fixture', workspaceName: 'WS-A', releaseRenewal: fixture.releaseRenewal, timeoutMs: 300, refreshCredentialSha256,
      });
      expect(result.status).toBe('failed');
      expect(result.assertions).toContainEqual(expect.objectContaining({ id: 'validation-result', status: 'failed' }));
      expect(Date.now() - started).toBeLessThan(5000);
    } finally { await fixture.cleanup(); }
  });

  test('an earlier relogin response cannot satisfy the click request', async ({ page, portalFixture }) => {
    let backgroundRoute: Route | undefined;
    await page.route('**/api/auth/v2/sso/relogin', route => {
      if (route.request().headers()['x-background']) { backgroundRoute = route; return; }
      return route.fallback();
    });
    await page.evaluate(() => { void fetch('/api/auth/v2/sso/relogin', { method: 'POST', headers: { 'X-Background': 'true' } }); });
    await expect.poll(() => Boolean(backgroundRoute)).toBe(true);
    const earlierResponse = page.waitForResponse(response => response.request().headers()['x-background'] === 'true');
    const result = await extendSessionAndVerifyAuthentication(createPom(page, fixturePrefix).portal, {
      scope: 'synthetic-fixture', workspaceName: 'WS-A', refreshCredentialSha256,
      releaseRenewal() {
        void (async () => {
          await backgroundRoute!.fulfill({ contentType: 'application/json', body: '{"result":true}',
            headers: { 'single-ui-authorization': 'synthetic-unrelated-access' } });
          await earlierResponse;
          portalFixture.releaseRenewal();
        })();
      },
    });
    expect(result.status).toBe('passed');
    expect(result.assertions).toContainEqual({ id: 'one-relogin-request', status: 'passed', actual: 1 });
  });

  test('a background validation success cannot mask the controlled probe failure', async ({ page }) => {
    const fixture = await installPortalFixture(page, { validationResult: false });
    await page.route('**/api/auth/v2/sso/validate', async route => {
      if (route.request().headers()['x-workbench-pom-probe']) {
        await page.evaluate(async () => { await fetch('/api/auth/v2/sso/validate', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ singleUIAuthorization: localStorage.getItem('SET_TOKEN') }),
        }); });
        return route.fallback();
      }
      return route.fulfill({ contentType: 'application/json', body: '{"result":true}' });
    });
    try {
      const result = await extendSessionAndVerifyAuthentication(createPom(page, fixturePrefix).portal, {
        scope: 'synthetic-fixture', workspaceName: 'WS-A', refreshCredentialSha256, releaseRenewal: fixture.releaseRenewal,
      });
      expect(result.status).toBe('failed');
      expect(result.observations.sessionValid).toBe(false);
    } finally { await fixture.cleanup(); }
  });

  test('dependent actions share the same page and browser context', async ({ page, portalFixture }) => {
    const before = page.context();
    const results = await executeSteps([
      { command: 'action', id: 'portal.theme.dark' },
      { command: 'action', id: 'portal.avatar.open' },
      { command: 'inspect', area: 'portal' },
    ], { page, pom: createPom(page, fixturePrefix), fixture: portalFixture, captureUi: true,
      allowSessionChange: false, workspaceName: 'WS-A' });
    expect(results).toHaveLength(3);
    expect(results.every(result => (result as { status: string }).status === 'passed')).toBe(true);
    expect(page.context()).toBe(before);
    await expect(page.getByRole('checkbox', { name: 'Theme Switch' })).not.toBeChecked();
    await expect(page.getByRole('menu')).toBeVisible();
  });

  test('missing independent refresh evidence keeps the workflow unverified', async ({ page, portalFixture }) => {
    const result = await extendSessionAndVerifyAuthentication(createPom(page, fixturePrefix).portal, {
      scope: 'synthetic-fixture', workspaceName: 'WS-A', releaseRenewal: portalFixture.releaseRenewal,
    });
    expect(result.status).toBe('unverified');
    expect(result.assertions).toContainEqual(expect.objectContaining({ id: 'refresh-credential', status: 'unverified' }));
    expect(await page.evaluate(() => localStorage.getItem('SET_REFRESH_TOKEN'))).toBeNull();
  });

  test('unknown actions and missing session permission fail before interaction', async ({ page, portalFixture }) => {
    const environment = { page, pom: createPom(page, fixturePrefix), fixture: portalFixture,
      captureUi: false, allowSessionChange: false, workspaceName: 'WS-A' };
    await expect(executeSteps([{ command: 'action', id: 'eval' }], environment)).rejects.toThrow('Unknown action');
    await expect(executeSteps([{ command: 'action', id: 'session.extend' }], environment)).rejects.toThrow('--allow-session-change');
    await new SessionTimeoutDialog(page).expectVisible();
    expect(() => validateSteps([{ command: 'inspect', javascript: 'arbitrary' }])).toThrow('Invalid step fields');
  });

  test('validation cannot pass a page with no matching area controls', async ({ page }) => {
    await page.setContent('<p>Wrong application</p>');
    const results = await executeSteps([{ command: 'validate', area: 'portal' }], {
      page, pom: createPom(page, fixturePrefix), captureUi: false, allowSessionChange: false, workspaceName: 'WS-A',
    });
    expect(results[0]).toMatchObject({ status: 'failed' });
  });

  for (const options of [{ dialogCopies: 0 }, { dialogCopies: 2 }, { disabledExtend: true }]) {
    test(`rejects missing, duplicate, or disabled targets: ${JSON.stringify(options)}`, async ({ page }) => {
      const fixture = await installPortalFixture(page, options);
      try {
        const result = await executeAction(createActions(createPom(page, fixturePrefix)), 'session.extend', true);
        expect(result.status).toBe('failed');
        expect(result.observations).toMatchObject({ clickCompleted: false, sessionValid: null });
        expect(await page.evaluate(() => localStorage.getItem('SET_TOKEN'))).toBe(fixtureCredentials.access);
      } finally { await fixture.cleanup(); }
    });
  }
});
