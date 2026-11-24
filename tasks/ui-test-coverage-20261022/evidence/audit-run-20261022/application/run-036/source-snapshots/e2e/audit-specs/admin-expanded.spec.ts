import { test, expect } from '../support/audit-fixture.js';
import { AdminApp, adminFields, type AdminKind } from '../support/admin-app.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual current React administration screens. Controlled browser login supplies UI-ADMIN-01 and TEST_OWNER, or the declared SUPER_USER. Controlled BFF routes return the case-declared records. Other controlled saves persist submitted field values. This run establishes frontend handling only. It does not execute BFF validation, storage, audit generation, or authorization.' });

const ids = [
  ...['CAT', 'MAP', 'TIL'].flatMap(group => Array.from({ length: 14 }, (_, i) => `UI-ADM-${group}-${String(i + 1).padStart(3, '0')}`)),
  ...Array.from({ length: 8 }, (_, i) => `UI-ADM-FLD-${String(i + 1).padStart(3, '0')}`),
  ...Array.from({ length: 15 }, (_, i) => `UI-ADM-SEL-${String(i + 1).padStart(3, '0')}`),
  ...Array.from({ length: 9 }, (_, i) => `UI-ADM-GRD-${String(i + 1).padStart(3, '0')}`),
];

for (const id of ids) {
  test(`${id} actual administration UI with step evidence`, async ({ page, audit }) => {
    const steps = await audit.defineCase(id);
    const description = steps.map(step => step.text).join('\n');
    const kind: AdminKind = id.includes('-MAP-') || ['UI-ADM-FLD-005', 'UI-ADM-FLD-006'].includes(id) ? 'Import Map'
      : id.includes('-TIL-') || id.includes('-SEL-') || ['UI-ADM-FLD-007', 'UI-ADM-FLD-008'].includes(id) ? 'Tile' : 'Category';
    const app = new AdminApp(page, kind, id);
    const field = (name: string) => name === 'Record Id' ? (kind === 'Category' ? 'applicationCategoryId' : kind === 'Import Map' ? 'importMapId' : 'applicationTileId') : adminFields[name];
    const input = (role: string, name: string) => app.field(name, role === 'textarea' ? 'textbox' : role);
    let clock = false;
    let newId = '';
    let comboName = '';

    for (const step of steps) await audit.step(step.number, async () => {
      const text = step.text;
      if (step.number === 1) { await app.setup(); return; }
      if (step.number === 2) {
        await app.open();
        if (id === 'UI-ADM-SEL-007' || id === 'UI-ADM-SEL-015') await app.selectCategory();
        if (description.includes('controlled field clock')) {
          const now = new Date(); await page.clock.install({ time: now }); await page.clock.pauseAt(new Date(now.getTime() + 20)); clock = true;
        }
        return;
      }
      if (/^the declared controlled field clock advances by 300 milliseconds$/.test(text)) {
        expect(clock).toBe(true); await page.clock.runFor(300); return;
      }
      if (/administration (?:grid|controls) finishes rendering|action cell for record/.test(text)) {
        await expect(app.grid).toBeVisible(); return;
      }
      let match: RegExpExecArray | null;
      if ((match = /^Admin A clicks button named "([^"]+)"/.exec(text))) {
        if (match[1].startsWith('Create New')) {
          await app.panel.getByRole('button', { name: match[1], exact: true }).click();
          newId = (await app.dialog().getAttribute('aria-labelledby')) ?? '';
          await audit.record('new-record-source-identity', { actualTitle: await app.dialog().innerText(), titleId: newId });
        } else {
          await app.footerButton(match[1]).click();
          if (['Create', 'Update', 'Verified', 'Deactivate'].includes(match[1])) await audit.record('ui-origin-admin-requests', app.requests);
        }
        return;
      }
      if ((match = /^Admin A clicks icon button named "(Edit|Verify|Deactivate|Audit)" inside row with Record Id "([^"]+)"/.exec(text))) {
        await app.action(match[1], match[2]).click(); return;
      }
      if ((match = /^Admin A (?:enters|enters exactly) "(.*)" into (textbox|textarea|spinbutton) named "([^"]+)"/.exec(text))) {
        await input(match[2], match[3]).fill(match[1].replaceAll('\\n', '\n')); return;
      }
      if ((match = /^Admin A replaces the value of (textbox|textarea|spinbutton) named "([^"]+)".* with "(.*)"$/.exec(text))) {
        await input(match[1], match[2]).fill(match[3].replaceAll('\\n', '\n')); return;
      }
      if ((match = /^Admin A opens combobox named "([^"]+)"/.exec(text))) {
        comboName = match[1];
        if (comboName === 'Is Template?') await audit.record('source-resolved-template-selector', {
          canonicalTarget: 'combobox named Is Template?', source: 'TableDetail/Field.tsx singleSelect',
          sourceIdentity: 'ModalInput-template-11', limit: 'The current MUI Select does not expose the declared label as its accessible name.' });
        await (comboName === 'Application Category' ? app.category : app.field(comboName, 'combobox')).click(); return;
      }
      if ((match = /^Admin A clicks option named "([^"]+)"/.exec(text))) {
        // MUI image alternatives contribute to option names. Text must still match the declared value.
        const option = page.getByRole('option', { includeHidden: true }).filter({ hasText: new RegExp(`^${match[1].replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`) });
        await expect(option).toHaveCount(1); await option.click(); return;
      }
      if ((match = /^column named "([^"]+)".* is visible$/.exec(text))) { await expect(await app.reveal(field(match[1]))).toBeVisible(); return; }
      if ((match = /^(textbox|textarea|spinbutton|combobox) named "([^"]+)".* (is disabled|is enabled|has value "(.*)"|has exactly the value "(.*)" where \\n represents one line break|has an empty value)$/.exec(text))) {
        const target = match[2] === 'Application Category' ? app.category : input(match[1], match[2]);
        if (match[3] === 'is disabled') await expect(target).toBeDisabled();
        else if (match[3] === 'is enabled') await expect(target).toBeEnabled();
        else await expect(target).toHaveValue((match[4] ?? match[5] ?? '').replaceAll('\\n', '\n'));
        return;
      }
      if ((match = /^button named "([^"]+)".* (is visible|is disabled|is enabled)$/.exec(text))) {
        const target = text.includes('dialog') ? app.footerButton(match[1]) : app.panel.getByRole('button', { name: match[1], exact: true });
        if (match[2] === 'is visible') await expect(target).toBeVisible();
        else if (match[2] === 'is disabled') await expect(target).toBeDisabled();
        else await expect(target).toBeEnabled();
        return;
      }
      if ((match = /^dialog (?:named|with source identity) "([^"]+)".* (is visible|is absent)$/.exec(text))) {
        const target = match[1] === 'Audit' ? app.auditDialog() : app.panel.locator('[role="dialog"]').filter({ has: page.getByText(match[1].startsWith('new ID:') ? /^new ID: \d+$/ : match[1], { exact: true }) });
        if (match[2] === 'is visible') await expect(target).toBeVisible(); else await expect(target).toHaveCount(0);
        return;
      }
      if ((match = /^icon button named "(Verify|Deactivate)" inside row with Record Id "([^"]+)".* (is enabled|is disabled)$/.exec(text))) {
        if (match[3] === 'is enabled') await expect(app.action(match[1], match[2])).toBeEnabled();
        else await expect(app.action(match[1], match[2])).toBeDisabled(); return;
      }
      if ((match = /^cell named "([^"]+)" inside row with Record Id "([^"]+)".* displays "(.*)"$/.exec(text))) {
        await expect(await app.reveal(field(match[1]), match[2].includes('Tile A') ? '101' : match[2])).toHaveText(match[3]); return;
      }
      if ((match = /^cell named "Verified\?" inside row with Record Id "([^"]+)".* tooltip "([^"]+)"$/.exec(text))) {
        const cell = await app.reveal('active', match[1]);
        await expect(cell.getByTestId(match[2] === 'Verified' ? 'CheckCircleIcon' : 'ErrorIcon')).toBeVisible();
        await cell.hover(); await expect(page.getByRole('tooltip', { name: match[2], exact: true })).toBeVisible(); return;
      }
      if ((match = /^exactly one row with Record Id "([^"]+)"/.exec(text))) { await expect(app.row(match[1])).toHaveCount(1); return; }
      if (text.includes('data row count') && /pre-action count/.test(text)) {
        await expect(app.grid.locator('[data-id]')).toHaveCount(app.beforeRows); return;
      }
      if (text.startsWith('no new row for the declared fixture')) { await expect(app.row('102')).toHaveCount(0); return; }
      if (text.startsWith('all displayed values of record 101')) { await expect(app.row()).toHaveText(app.beforeValues); return; }
      if ((match = /^row with source identity "([^"]+)" inside the data grid in the Audit dialog/.exec(text))) {
        await expect(app.auditDialog().locator(`[data-id="${match[1]}"]`)).toBeVisible(); return;
      }
      if ((match = /^the source-record identifier cell in row with source identity "([^"]+)".* equals "([^"]+)"$/.exec(text))) {
        await expect(app.auditDialog().locator(`[data-id="${match[1]}"] [data-field="${field('Record Id')}"]`)).toHaveText(match[2]); return;
      }
      if ((match = /^option named "([^"]+)".* (is visible|is absent)$/.exec(text))) {
        const target = page.getByRole('option', { name: match[1], exact: true });
        if (match[2] === 'is visible') await expect(target).toBeVisible(); else await expect(target).toHaveCount(0); return;
      }
      if ((match = /^icon button named "refresh".* (is enabled|is disabled)$/.exec(text))) {
        if (match[1] === 'is enabled') await expect(app.panel.getByRole('button', { name: 'refresh', exact: true })).toBeEnabled();
        else await expect(app.panel.getByRole('button', { name: 'refresh', exact: true })).toBeDisabled(); return;
      }
      if (text.startsWith('Admin A clicks icon button named "refresh"')) { await app.panel.getByRole('button', { name: 'refresh', exact: true }).click(); return; }
      if ((match = /^(?:no cell|a cell) in the "Tile Name" column.* displays "([^"]+)"$/.exec(text))) {
        const cells = app.grid.locator('[data-field="title"]').filter({ hasText: new RegExp(`^${match[1]}$`) });
        if (text.startsWith('no cell')) await expect(cells).toHaveCount(0); else await expect(cells).toBeVisible(); return;
      }
      if (text.startsWith('Admin A clicks icon button with source identity "UNVERIFIED category-clear')) {
        await audit.record('source-resolved-clear-target', { source: 'MUI Autocomplete', accessibleName: 'Clear', canonicalTarget: 'UNVERIFIED category-clear target' });
        await app.category.locator('..').getByRole('button', { name: 'Clear', exact: true }).click(); return;
      }
      if (text.includes('post-clear fetch remains pending')) { await expect(app.grid.locator('[data-id]')).toHaveCount(0); return; }
      if (text.includes('UNVERIFIED next-page target')) {
        await audit.record('source-resolved-pagination-target', { actualName: 'Go to next page', canonicalTarget: 'UNVERIFIED next-page target' });
        await app.grid.getByRole('button', { name: 'Go to next page', exact: true }).click(); return;
      }
      if (text.includes('UNVERIFIED page-size target')) {
        await audit.record('source-resolved-pagination-target', { actualRole: 'combobox', canonicalTarget: 'UNVERIFIED page-size target' });
        await app.grid.getByRole('combobox').click(); return;
      }
      if ((match = /current page.* contains (?:exactly )?(\d+) data records$/.exec(text))) {
        const size = Number(match[1]);
        await expect(app.grid.locator('.MuiTablePagination-displayedRows')).toHaveText(size === 5 ? '21–25 of 25' : `1–${size} of ${id === 'UI-ADM-GRD-002' ? 75 : id === 'UI-ADM-GRD-004' ? 105 : 25}`); return;
      }
      if ((match = /^row with source identity "([^"]+)" inside the Category administration data grid is visible$/.exec(text))) { await expect(app.row(match[1])).toBeVisible(); return; }
      if (text.startsWith('Admin A clicks chip with text "Close"')) { await app.auditDialog().getByRole('button', { name: 'Close', exact: true }).click(); return; }
      if (/^(?:the cell|no cell) in (?:the|that) "Audit ID" column/.test(text)) {
        const cells = app.auditDialog().locator('[data-field="id"]');
        if (text.startsWith('no cell')) await expect(cells.filter({ hasText: /^9001$/ })).toHaveCount(0);
        else await expect(cells.filter({ hasText: /^9002$/ })).toBeVisible(); return;
      }
      if (text.startsWith('Admin A clicks cell named "Category Label"')) { await (await app.reveal('label', '101')).click(); return; }
      if (text === 'the Category create request remains pending') { expect(app.requests.some(request => request.endpoint === 'category/create')).toBe(true); return; }
      if ((match = /^a circular loading indicator is visible inside button named "([^"]+)"/.exec(text))) { await expect(app.footerButton(match[1]).getByRole('progressbar')).toBeVisible(); return; }
      if (text.startsWith('Admin A clicks switch named "Time Switch"')) { await page.getByRole('checkbox', { name: 'Time Switch', exact: true }).click(); return; }
      if (text.startsWith('switch named "Time Switch"')) { await expect(page.getByRole('checkbox', { name: 'Time Switch', exact: true })).not.toBeChecked(); return; }
      if (text.startsWith('cell named "Updated At"') && (text.includes('represents date') || text.includes('declared en-locale'))) {
        const expected = new Intl.DateTimeFormat('en', { dateStyle: 'medium', timeStyle: 'medium', timeZone: id === 'UI-ADM-GRD-009' ? 'Asia/Singapore' : 'UTC' }).format(new Date('2026-10-22T00:05:00Z'));
        await expect(await app.reveal('updatedAt', '101')).toHaveText(expected); return;
      }
      throw new Error(`No administration UI binding for canonical step ${step.number}: ${text}`);
    });
    await audit.record('ui-origin-admin-requests', app.requests);
  });
}
