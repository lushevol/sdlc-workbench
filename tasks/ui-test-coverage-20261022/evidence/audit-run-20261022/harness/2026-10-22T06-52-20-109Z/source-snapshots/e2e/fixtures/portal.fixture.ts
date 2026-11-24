import type { Page, Route } from '@playwright/test';
import { test as base } from '../support/audit-fixture.js';

export const fixtureOrigin = 'http://pom.fixture.test';
export const fixturePrefix = 'fixture';
export const fixtureCredentials = {
  access: 'synthetic-expired-access-A',
  refresh: 'synthetic-refresh-R',
  renewedAccess: 'synthetic-renewed-access-B',
} as const;

export type FixtureOptions = {
  renewalStatus?: number;
  validationStatus?: number;
  validationResult?: boolean;
  installWrongToken?: boolean;
  wrongRefresh?: boolean;
  duplicateRenewal?: boolean;
  dialogCopies?: number;
  disabledExtend?: boolean;
  deferRenewal?: boolean;
  holdValidation?: boolean;
};

export type PortalFixture = {
  scope: 'synthetic-fixture';
  releaseRenewal(): void;
  cleanup(): Promise<void>;
};

// This controlled DOM tests harness mechanics. It is not the React application.
export async function installPortalFixture(page: Page, options: FixtureOptions = {}): Promise<PortalFixture> {
  let release!: () => void;
  const released = new Promise<void>(resolve => { release = resolve; });
  if (options.deferRenewal === false) release();
  let heldValidation: Route | undefined;
  const handler = async (route: Route) => {
    const url = new URL(route.request().url());
    if (url.origin !== fixtureOrigin) return route.abort('blockedbyclient');
    if (url.pathname === '/api/auth/v2/sso/relogin') {
      await released;
      return route.fulfill({
        status: options.renewalStatus ?? 200,
        contentType: 'application/json',
        headers: { 'single-ui-authorization': fixtureCredentials.renewedAccess },
        body: JSON.stringify({ result: (options.renewalStatus ?? 200) === 200 }),
      });
    }
    if (url.pathname === '/api/auth/v2/sso/validate') {
      if (options.holdValidation) { heldValidation = route; return; }
      return route.fulfill({ status: options.validationStatus ?? 200,
        contentType: 'application/json', body: JSON.stringify({ result: options.validationResult ?? true }) });
    }
    if (url.pathname === '/api/auth/v2/sso/logout') {
      return route.fulfill({ contentType: 'application/json', body: '{"result":true}' });
    }
    if (url.pathname === '/') return route.fulfill({ contentType: 'text/html', body: fixtureHtml(options) });
    return route.abort('blockedbyclient');
  };
  await page.route('**/*', handler);
  await page.goto(fixtureOrigin);
  return {
    scope: 'synthetic-fixture',
    releaseRenewal: release,
    async cleanup() { release(); await heldValidation?.abort().catch(() => {}); await page.unroute('**/*', handler); },
  };
}

function fixtureHtml(options: FixtureOptions): string {
  const dialog = `<section role="dialog" aria-labelledby="timeout-dialog-title" aria-describedby="timeout-dialog-description">
    <h2 id="timeout-dialog-title">Your session has been expired</h2>
    <p id="timeout-dialog-description">Do you want to logout or extend the session?</p>
    <button data-testid="Extend_Btn" ${options.disabledExtend ? 'disabled' : ''}>Extend</button>
    <button data-testid="Logout_Btn">Logout</button></section>`;
  return `<!doctype html><html><head><title>Synthetic POM fixture</title></head><body>
    <div id="shell" data-testid="fixture_home"><div role="tablist" aria-label="workspaces"><div role="tab" aria-selected="true"><input aria-label="Workspace Name" value="WS-A"></div></div>
    <button data-testid="fixture_avatar_IconButton">User menu</button>
    <div id="menu-appbar-avatar" role="menu" hidden><button role="menuitem" data-testid="fixture_avatar_Profile">user-a</button><button role="menuitem">Logout</button></div>
    <label>Theme Switch<input type="checkbox" aria-label="Theme Switch" checked></label></div>
    <main>${dialog.repeat(options.dialogCopies ?? 1)}</main>
    <script>
      localStorage.setItem('SET_TOKEN', ${JSON.stringify(fixtureCredentials.access)});
      const renew = async () => {
        const response = await fetch('/api/auth/v2/sso/relogin', {method:'POST',
          headers:{'Single-UI-Refresh':${JSON.stringify(options.wrongRefresh ? 'synthetic-wrong-refresh' : fixtureCredentials.refresh)}}});
        if (response.ok) localStorage.setItem('SET_TOKEN', ${options.installWrongToken ? "'synthetic-wrong-access'" : "response.headers.get('single-ui-authorization')"});
      };
      document.querySelectorAll('[data-testid="Extend_Btn"]').forEach(button => button.onclick = () => {
        renew(); ${options.duplicateRenewal ? 'renew();' : ''}
        document.querySelectorAll('[role="dialog"]').forEach(dialog => dialog.remove());
      });
      document.querySelectorAll('[data-testid="Logout_Btn"]').forEach(button => button.onclick = async () => {
        await fetch('/api/auth/v2/sso/logout', {method:'POST'});
        localStorage.clear(); document.querySelector('main').innerHTML = '<input placeholder="Enter Username"><input type="password" placeholder="Enter Password"><button>Sign In</button>';
      });
      document.querySelector('[data-testid="fixture_avatar_IconButton"]').onclick = () => document.querySelector('[role="menu"]').hidden = false;
    </script></body></html>`;
}

export const test = base.extend<{ portalFixture: PortalFixture }>({
  portalFixture: async ({ page }, use) => {
    const fixture = await installPortalFixture(page);
    try { await use(fixture); } finally { await fixture.cleanup(); }
  },
});
export { expect } from '@playwright/test';
