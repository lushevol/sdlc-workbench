import { test, expect } from '../support/audit-fixture.js';
import { blockExternal, loginToWorkspace } from '../support/local-app.js';
import { type PortalPage } from '../pages/portal.page.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual current React MFE; controlled accepted login response; UI-USER-01; empty W1 seeded; no real permission or BFF persistence verification.' });

test('UI-SHL-001 empty workspace offers tile discovery', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-001');
  let portal: PortalPage;
  const panel = page.getByRole('tabpanel').filter({ visible: true });
  await audit.step(1, async () => { await blockExternal(page); portal = await loginToWorkspace(page); });
  await audit.step(2, async () => { await expect(panel.getByText('Start customizing your workspace', { exact: true })).toBeVisible(); });
  await audit.step(3, async () => { await portal.workspace('W1').clickTab(); });
  await audit.step(4, async () => { await expect(panel.getByText('Start customizing your workspace', { exact: true })).toBeVisible(); });
  await audit.step(5, async () => { await expect(panel.getByRole('button', { name: 'Find tile', exact: true })).toBeVisible(); });
});

test('UI-SHL-002 Find tile opens drawer', async ({ page, audit }) => {
  await audit.defineCase('UI-SHL-002');
  const drawer = page.getByTestId('MicroWebUI_base_drawer');
  await audit.step(1, async () => { await blockExternal(page); await loginToWorkspace(page); });
  await audit.step(2, async () => { await expect(drawer).toBeHidden(); await expect(page.getByRole('button', { name: 'Find tile', exact: true })).toBeVisible(); });
  await audit.step(3, async () => { await page.getByRole('button', { name: 'Find tile', exact: true }).click(); });
  await audit.step(4, async () => { await expect(drawer.getByText('Tile Options', { exact: true })).toBeVisible(); });
});

for (const [id, previous, next] of [
  ['UI-SHL-003', 'Workspace 1', 'Workspace 2'],
  ['UI-SHL-004', 'Workspace 7', 'Workspace 8'],
] as const) {
  test(`${id} add blank workspace after ${previous}`, async ({ page, audit }) => {
    await audit.defineCase(id);
    let portal: PortalPage;
    await audit.step(1, async () => { await blockExternal(page); portal = await loginToWorkspace(page, previous); });
    await audit.step(2, async () => { await portal.expectWorkspaceTabVisible(previous); await expect(portal.workspaceList.getByRole('tab')).toHaveCount(1); });
    await audit.step(3, async () => { await portal.clickAddWorkspaceButton(); });
    await audit.step(4, async () => {
      const selected = portal.workspaceList.getByRole('tab', { selected: true });
      await expect(selected.getByRole('textbox', { name: 'Workspace Name', exact: true })).toHaveValue(next);
    });
    if (id === 'UI-SHL-003') {
      await audit.step(5, async () => { await expect(portal.workspaceList.getByRole('tab')).toHaveCount(2); });
      await audit.step(6, async () => { await expect(page.getByRole('button', { name: 'Find tile', exact: true })).toBeVisible(); });
    }
  });
}
