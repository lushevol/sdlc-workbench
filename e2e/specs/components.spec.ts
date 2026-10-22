import { expect, test } from '@playwright/test';
import { LoginPage } from '../pages/login.page.js';
import { PortalPage } from '../pages/portal.page.js';
import { CategoryAdministrationPage } from '../pages/category-administration.page.js';
import { inspectTarget } from '../components/target.js';
import { checkSourceContracts } from '../support/source-quality.js';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';

// These source-shaped synthetic DOM fixtures test POM mechanics only.
// They do not execute the MFE React bundle or verify business behavior.
test.describe('synthetic source-shaped POM mechanics', () => {
  test('missing source checkout fails validation without claiming runtime verification', async () => {
    const root = await mkdtemp(path.join(tmpdir(), 'pom-source-quality-'));
    try {
      const result = await checkSourceContracts(root);
      expect(result.status).toBe('failed');
      expect(result.runtimeVerification).toBe('unverified');
      expect(result.errors.length).toBeGreaterThan(0);
      expect(result.errors.every(error => error.code === 'source-unavailable')).toBe(true);
    } finally {
      await rm(root, { recursive: true, force: true });
    }
  });

  test('login fills native masked inputs inside the configured page scope', async ({ page }) => {
    await page.setContent(`
      <input placeholder="Enter Username" value="outside-user">
      <input placeholder="Enter Password" value="outside-password">
      <section data-testid="contract_login">
        <div data-testid="Username"><input placeholder="Enter Username"></div>
        <div data-testid="password"><input type="password" placeholder="Enter Password"></div>
        <button onclick="this.dataset.clicked='true'">Sign In</button>
        <a href="#sso">Sign In With SSO</a>
      </section>`);
    const login = new LoginPage(page, 'contract');
    await login.expectVisible();
    await login.fillUsername('user-1');
    await login.fillPassword('synthetic-password');
    await login.expectUsernameValue('user-1');
    await login.expectPasswordValue('synthetic-password');
    await login.expectPasswordMasked();
    await login.clickSignInButton();
    await expect(login.signInButton).toHaveAttribute('data-clicked', 'true');
    await expect(page.locator('body > input').nth(0)).toHaveValue('outside-user');
    await expect(page.locator('body > input').nth(1)).toHaveValue('outside-password');
    await expect(login.ssoLink).toHaveAttribute('href', '#sso');
  });

  test('inspection reports duplicate or disabled controls without choosing a fallback', async ({ page }) => {
    await page.setContent(`<section data-testid="contract_login">
      <input placeholder="Enter Username"><input placeholder="Enter Username">
      <button disabled>Sign In</button><a href="#sso">Sign In With SSO</a>
    </section>`);
    const login = new LoginPage(page, 'contract');
    const duplicate = await inspectTarget(login.targets.usernameInput);
    expect(duplicate).toMatchObject({ count: 2, visible: null, enabled: null, available: false, reason: 'ambiguous' });
    const disabled = await inspectTarget(login.targets.signInButton);
    expect(disabled).toMatchObject({ count: 1, visible: true, enabled: false, available: false, reason: 'disabled' });
    const absent = await inspectTarget(login.targets.passwordInput);
    expect(absent).toMatchObject({ count: 0, available: false, reason: 'not-found' });
  });

  test('portal uses checkbox semantics and a portal-mounted avatar menu', async ({ page }) => {
    await page.setContent(`
      <input type="checkbox" aria-label="Theme Switch" checked>
      <section data-testid="contract_home">
        <div role="tablist" aria-label="workspaces"><button aria-label="Add Workspace">+</button></div>
        <input type="checkbox" aria-label="Theme Switch" checked>
        <button data-testid="contract_avatar_IconButton"
          onclick="document.getElementById('menu-appbar-avatar').hidden=false">Avatar</button>
      </section>
      <div id="menu-appbar-avatar" hidden><div role="menu">
        <div role="menuitem" data-testid="contract_avatar_Profile"
          onclick="this.dataset.clicked='true'">User A Click to view user profile details</div>
        <div role="menuitem">Logout</div>
      </div></div>`);
    const portal = new PortalPage(page, 'contract');
    await portal.expectVisible();
    await portal.setThemeLight(false);
    await portal.expectThemeLight(false);
    await expect(page.locator('body > input')).toBeChecked();
    await portal.clickAvatarButton();
    await portal.expectAvatarMenuVisible();
    await portal.clickProfileMenuItem();
    await expect(portal.profileMenuItem).toHaveAttribute('data-clicked', 'true');
  });

  test('workspace actions use stable IDs when visible labels repeat', async ({ page }) => {
    await page.setContent(`<section data-testid="contract_home">
      <div role="tablist" aria-label="workspaces">
        <div role="tab" aria-selected="false" data-testid="workspaces-tab-WS-A">
          <input aria-label="Workspace Name" value="Repeated label">
          <button aria-label="refresh" onclick="this.dataset.clicked='true'">Refresh</button>
        </div>
        <div role="tab" aria-selected="true" data-testid="workspaces-tab-WS-B">
          <input aria-label="Workspace Name" value="Repeated label">
          <button aria-label="refresh" onclick="this.dataset.clicked='true'">Refresh</button>
          <button aria-label="delete" onclick="this.closest('[role=tab]').remove()">Delete</button>
        </div>
        <button aria-label="Add Workspace">+</button>
      </div>
    </section>`);
    const portal = new PortalPage(page, 'contract');
    const workspace = portal.workspace('WS-B');
    await workspace.expectSelected();
    await workspace.fillName('Renamed B');
    await workspace.expectName('Renamed B');
    await portal.expectWorkspaceTabVisible('Renamed B');
    await portal.workspace('WS-A').expectName('Repeated label');
    await workspace.clickRefreshButton();
    await expect(workspace.refreshButton).toHaveAttribute('data-clicked', 'true');
    await expect(portal.workspace('WS-A').refreshButton).not.toHaveAttribute('data-clicked');
    await workspace.clickDeleteButton();
    await workspace.expectTabAbsent();
    await portal.workspace('WS-A').expectName('Repeated label');
  });

  test('category controls use stable record IDs and distinguish disabled header Close', async ({ page }) => {
    await page.setContent(`
      <button data-testid="edit-CAT-A" onclick="this.dataset.clicked='true'">Unrelated Edit</button>
      <section data-testid="contract_category">
        <button>Create New Category</button>
        <section data-testid="contract_simple_table">
          <div role="grid"><div role="row">
            <div role="columnheader">Category Label</div><div role="columnheader">Owner</div>
            <div role="columnheader">Verified?</div>
          </div><div role="row">
            <button role="menuitem" aria-label="Edit" data-testid="edit-CAT-A"
              onclick="document.getElementById('detail').hidden=false">Edit</button>
            <button role="menuitem" aria-label="Audit" data-testid="audit-CAT-A">Audit</button>
          </div></div>
          <section role="dialog" id="detail" aria-labelledby="detail-title" hidden>
            <h2 id="detail-title"><span>edit ID: CAT-A</span><button aria-label="resize">Maximize</button>
              <span role="button" aria-disabled="true">Close</span></h2>
            <div>Record fields</div>
            <footer><button onclick="this.dataset.clicked='true'">Reset</button>
              <button onclick="document.getElementById('detail').hidden=true">Close</button></footer>
          </section>
        </section>
      </section>`);
    const category = new CategoryAdministrationPage(page, 'contract');
    await category.expectVisible();
    await category.expectCoreColumnHeaders();
    const actions = category.recordActions('CAT-A');
    await actions.clickEditMenuItem();
    await expect(page.locator('body > button')).not.toHaveAttribute('data-clicked');
    const detail = category.detailDialog('edit', 'CAT-A');
    await detail.expectVisible();
    await expect(detail.dialog).toHaveAccessibleName('edit ID: CAT-A resize Close');
    await expect(detail.closeButton).toHaveCount(1);
    await detail.clickResetButton();
    await expect(detail.resetButton).toHaveAttribute('data-clicked', 'true');
    await detail.clickCloseButton();
    await detail.expectClosed();
  });
});
