import { test, expect } from '../support/audit-fixture.js';
import { blockExternal, loginToWorkspace } from '../support/local-app.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual current React MFE; controlled accepted login response; UI-USER-01; empty W1 seeded; no real permission or BFF persistence verification.' });

test('UI-SHL-001 empty workspace offers tile discovery', async ({ page, audit }) => {
  await blockExternal(page);
  const portal = await loginToWorkspace(page);
  await audit.capture('start-empty-w1', 'W1 exists before workspace selection.', 'UI-SHL-001 Given');
  await portal.workspace('W1').clickTab();
  const panel = page.getByRole('tabpanel').filter({ visible: true });
  await expect(panel.getByText('Start customizing your workspace', { exact: true })).toBeVisible();
  await expect(panel.getByRole('button', { name: 'Find tile', exact: true })).toBeVisible();
  await audit.capture('discovery-controls', 'The selected W1 offers customization and Find tile.', 'UI-SHL-001 Then');
});

test('UI-SHL-002 Find tile opens drawer', async ({ page, audit }) => {
  await blockExternal(page);
  await loginToWorkspace(page);
  const drawer = page.getByTestId('MicroWebUI_base_drawer');
  await expect(page.getByText('Tile Options', { exact: true })).not.toBeVisible();
  await audit.capture('start-drawer-closed', 'The empty workspace has no visible Tile Options drawer.', 'UI-SHL-002 Given');
  await page.getByRole('button', { name: 'Find tile', exact: true }).click();
  await expect(page.getByText('Tile Options', { exact: true })).toBeVisible();
  await audit.capture('drawer-open', 'Tile Options appears after Find tile.', 'UI-SHL-002 Then');
});

for (const [id, previous, next] of [
  ['UI-SHL-003', 'Workspace 1', 'Workspace 2'],
  ['UI-SHL-004', 'Workspace 7', 'Workspace 8'],
] as const) {
  test(`${id} add blank workspace after ${previous}`, async ({ page, audit }) => {
    await blockExternal(page);
    const portal = await loginToWorkspace(page, previous);
    await expect(portal.workspaceList.getByRole('tab')).toHaveCount(1);
    await audit.capture('start-one-workspace', `${previous} is the only workspace before Add Workspace.`, `${id} Given`);
    await portal.clickAddWorkspaceButton();
    await portal.expectWorkspaceTabVisible(next);
    await expect(portal.workspaceList.getByRole('tab')).toHaveCount(2);
    const selected = portal.workspaceList.getByRole('tab', { selected: true });
    await expect(selected.getByRole('textbox', { name: 'Workspace Name', exact: true })).toHaveValue(next);
    await expect(page.getByRole('button', { name: 'Find tile', exact: true })).toBeVisible();
    await audit.capture('new-workspace-selected', `${next} is selected, with two tabs and Find tile.`, `${id} Then`);
  });
}
