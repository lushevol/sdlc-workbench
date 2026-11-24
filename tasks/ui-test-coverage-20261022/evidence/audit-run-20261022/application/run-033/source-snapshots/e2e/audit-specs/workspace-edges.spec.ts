import { type Page } from '@playwright/test';
import { test, expect, type AuditCapture } from '../support/audit-fixture.js';
import { acceptedLogin, blockExternal, credentials, fixtureAccess, localPrefix, openLogin, workspace } from '../support/local-app.js';
import { PortalPage } from '../pages/portal.page.js';

type StoredWorkspace = { id: string; label: string; isActive: boolean; containers: Record<string, unknown>[] };

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual current MFE; controlled accepted login; unsigned fixture JWT; explicit stored workspaces. No real identity, server authorization, or backend persistence verification.' });

// Seed once so browser reload assertions observe application storage changes.
async function openStored(page: Page, audit: AuditCapture, caseId: string, values: StoredWorkspace[], drawers: unknown[] = []): Promise<PortalPage> {
  await blockExternal(page);
  await page.addInitScript(values => {
    if (!localStorage.getItem('UI_AUDIT_INITIAL_WORKSPACES')) {
      localStorage.setItem('SET_WORKSPACES', JSON.stringify(values));
      localStorage.setItem('UI_AUDIT_INITIAL_WORKSPACES', 'seeded');
    }
  }, values);
  // Reload must retain the same controlled accepted session as the login fixture.
  const respond = async (route: Parameters<typeof acceptedLogin>[0]) => {
    if (!drawers.length) return acceptedLogin(route);
    await route.fulfill({ status: 200, headers: { 'content-type': 'application/json',
      'single-ui-authorization': fixtureAccess() },
      body: JSON.stringify({ userInfo: JSON.stringify({ sub: 'UI-USER-01', fullName: 'Audit User A' }),
        entities: [], drawers, result: true }) });
  };
  await page.route('**/api/auth/v2/sso/validate', respond);
  await page.route('**/api/auth/v2/sso/login', respond);
  const login = await openLogin(page);
  await audit.record('stored-workspace-setup', { workspaces: values, drawers, entities: [],
    response: 'CONTROLLED_ACCEPTED_LOGIN_AND_VALIDATE', persistence: 'LOCAL_BROWSER_ONLY' });
  await login.fillUsername(credentials.username);
  await login.fillPassword(credentials.password);
  await login.clickSignInButton();
  const portal = new PortalPage(page, localPrefix);
  await portal.expectVisible();
  return portal;
}

test('UI-SHL-005 number workspace after custom label', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-005');
  let portal: PortalPage;
  await audit.step(1, async () => { portal = await openStored(page, audit, 'UI-SHL-005', [workspace(), workspace('Operations', 'W2')]); });
  await audit.step(2, async () => { await portal.expectWorkspaceTabVisible('Operations'); await expect(portal.workspaceList.getByRole('tab')).toHaveCount(2); });
  await audit.step(3, async () => { await portal.clickAddWorkspaceButton(); });
  await audit.step(4, async () => {
    await expect(portal.workspaceList.getByRole('tab', { selected: true }).getByRole('textbox', { name: 'Workspace Name', exact: true })).toHaveValue('Workspace 3');
  });
});

test('UI-SHL-008 double-click focuses workspace name', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-008');
  let portal: PortalPage;
  await audit.step(1, async () => { portal = await openStored(page, audit, 'UI-SHL-008', [workspace()]); });
  await audit.step(2, async () => { await portal.workspace('W1').expectSelected(); });
  await audit.step(3, async () => { await portal.workspace('W1').tab.dblclick(); });
  await audit.step(4, async () => { await expect(portal.workspace('W1').nameInput).toBeFocused(); });
});

test('UI-SHL-009 rename workspace and show exact tooltip', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-009');
  let portal: PortalPage;
  await audit.step(1, async () => { portal = await openStored(page, audit, 'UI-SHL-009', [workspace()]); });
  await audit.step(2, async () => { await portal.workspace('W1').tab.dblclick(); await expect(portal.workspace('W1').nameInput).toBeFocused(); });
  await audit.step(3, async () => { await portal.workspace('W1').fillName('Operations Morning'); });
  await audit.step(4, async () => { await portal.workspace('W1').expectName('Operations Morning'); });
  await audit.step(5, async () => { await page.getByRole('tabpanel').filter({ visible: true }).hover(); await portal.workspace('W1').tab.hover(); });
  await audit.step(6, async () => { await expect(page.getByRole('tooltip', { name: 'Operations Morning', exact: true })).toBeVisible(); });
});

test('UI-SHL-010 restore renamed workspace after reload', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-010');
  let portal: PortalPage;
  await audit.step(1, async () => { portal = await openStored(page, audit, 'UI-SHL-010', [workspace()]); });
  await audit.step(2, async () => {
    await portal.workspace('W1').tab.dblclick(); await portal.workspace('W1').fillName('Operations Morning');
    await portal.workspace('W1').expectName('Operations Morning');
    await expect.poll(() => page.evaluate(() => JSON.parse(localStorage.getItem('SET_WORKSPACES') ?? '[]')[0]?.label)).toBe('Operations Morning');
  });
  await audit.step(3, async () => { await page.reload(); await portal.expectVisible(); });
  await audit.step(4, async () => { await portal.workspace('W1').expectName('Operations Morning'); });
});

test('UI-SHL-011 only workspace has no delete action', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-011');
  let portal: PortalPage;
  await audit.step(1, async () => { portal = await openStored(page, audit, 'UI-SHL-011', [workspace()]); });
  await audit.step(2, async () => { await expect(portal.workspaceList.getByRole('tab')).toHaveCount(1); });
  await audit.step(3, async () => { await portal.workspace('W1').clickTab(); });
  await audit.step(4, async () => { await expect(portal.workspace('W1').deleteButton).toHaveCount(0); });
});

test('UI-SHL-015 removing later tab preserves selected workspace', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-015');
  let portal: PortalPage;
  await audit.step(1, async () => { portal = await openStored(page, audit, 'UI-SHL-015', [workspace(), workspace('Workspace 2', 'W2'), workspace('Workspace 3', 'W3')]); });
  await audit.step(2, async () => { await expect(portal.workspaceList.getByRole('tab')).toHaveCount(3); await portal.workspace('W1').expectSelected(); });
  await audit.step(3, async () => { await portal.workspace('W3').clickDeleteButton(); });
  await audit.step(4, async () => { await portal.workspace('W3').expectTabAbsent(); });
  await audit.step(5, async () => { await portal.workspace('W1').expectSelected(); });
});

test('UI-SHL-016 deleted workspace stays absent after reload', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-016');
  let portal: PortalPage;
  await audit.step(1, async () => { portal = await openStored(page, audit, 'UI-SHL-016', [workspace(), workspace('Workspace 2', 'W2')]); });
  await audit.step(2, async () => {
    await portal.expectWorkspaceTabVisible('Workspace 2'); await portal.workspace('W2').clickDeleteButton(); await portal.workspace('W2').expectTabAbsent();
    await expect.poll(() => page.evaluate(() => JSON.parse(localStorage.getItem('SET_WORKSPACES') ?? '[]').length)).toBe(1);
  });
  await audit.step(3, async () => { await page.reload(); await portal.expectVisible(); });
  await audit.step(4, async () => { await portal.workspace('W2').expectTabAbsent(); });
});

test('UI-SHL-021 unregistered workspace has no refresh action', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-021');
  let portal: PortalPage;
  await audit.step(1, async () => { portal = await openStored(page, audit, 'UI-SHL-021', [workspace(), workspace('Workspace 2', 'W2')]); });
  await audit.step(2, async () => { await expect(portal.workspace('W2').refreshButton).toHaveCount(0); });
  await audit.step(3, async () => { await portal.workspace('W2').clickTab(); await portal.workspace('W2').expectSelected(); });
  await audit.step(4, async () => { await expect(portal.workspace('W2').refreshButton).toHaveCount(0); });
});

const removedTile = { id: 'C1', container: '@fixture/removed', module: 'tile', tile: 'removed',
  title: 'Removed Tile', emailSupport: '', panelId: 'workspaces-tabpanel-1', tabId: 'W1' };

test('UI-SHL-024 discard unauthorized saved workspace', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-024');
  let portal: PortalPage;
  const drawers = [{ id: 1, label: 'Fixture restricted catalog', tiles: [{ ...removedTile,
    entity: ['ENTITY_WITHOUT_ACCESS'], subject: 'SUBJECT_WITHOUT_ACCESS', isTemplate: false,
    imageDarkTheme: '', imageLightTheme: '' }] }];
  await audit.step(1, async () => { portal = await openStored(page, audit, 'UI-SHL-024', [workspace()], drawers); });
  await audit.step(2, async () => {
    const saved = [{ ...workspace(), containers: [removedTile] }, workspace('Workspace 2', 'W2')];
    await page.evaluate(saved => localStorage.setItem('SET_WORKSPACES', JSON.stringify(saved)), saved);
    await audit.record('canonical-saved-workspaces', { workspaces: saved, entities: [], drawers });
  });
  await audit.step(3, async () => { await page.reload(); await portal.expectVisible(); });
  await audit.step(4, async () => { await portal.workspace('W1').expectTabAbsent(); });
  await audit.step(5, async () => { await portal.expectWorkspaceTabVisible('Workspace 2'); });
});

test('UI-SHL-025 replace wholly invalid saved workspaces', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-025');
  let portal: PortalPage;
  const selected = page.getByRole('tabpanel').filter({ visible: true });
  await audit.step(1, async () => { portal = await openStored(page, audit, 'UI-SHL-025', [workspace()]); });
  await audit.step(2, async () => {
    const saved = [{ ...workspace(), containers: [removedTile] }];
    await page.evaluate(saved => localStorage.setItem('SET_WORKSPACES', JSON.stringify(saved)), saved);
    await audit.record('canonical-saved-workspaces', { workspaces: saved, drawers: [] });
  });
  await audit.step(3, async () => { await page.reload(); await portal.expectVisible(); });
  await audit.step(4, async () => { await expect(portal.workspaceList.getByRole('tab')).toHaveCount(1); });
  await audit.step(5, async () => { await expect(selected.getByText('Start customizing your workspace', { exact: true })).toBeVisible(); });
  await audit.step(6, async () => { await expect(selected.getByRole('button', { name: 'Find tile', exact: true })).toBeVisible(); });
});
