import { test, expect } from '../support/audit-fixture.js';
import { AdminApp, categoryRecord, tileRecord, type AdminKind } from '../support/admin-app.js';
import type { Route } from '@playwright/test';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES', timezoneId: 'Asia/Singapore',
  auditFixture: 'Actual React administration screens. Controlled browser credentials, role, records, and BFF responses. Save probes persist the received UI payload without replacing it with expected values. Declared clock emulation controls field timers. Proposed accessibility and source-risk expectations remain separate from business approval.' });

const ux = [14, 15, 16, 17, 18, 21, 31, 38, 45, 47, 51, 52, 53, 54, 55, 56, 57, 58, 65, 66, 67, 68, 69, 70];

for (const number of ux) {
  const id = `UX-${String(number).padStart(3, '0')}`;
  test(`${id} administration boundary with step screenshots`, async ({ page, audit }) => {
    const steps = await audit.defineCase(id);
    const category = [17, 21, 38, 65, 66, 67, 68, 69, 70].includes(number);
    const app = new AdminApp(page, category ? 'Category' : 'Tile', id);
    const alerts: string[] = [];
    let csv = ''; let rows: string[][] = [];
    let disabledCount = 0;
    let baseline: { label: string; x: number; y: number }[] = [];
    const clockCase = number === 38 || number >= 51 && number <= 58;
    const field = (name: string) => app.field(name);
    const menu = async (name: string) => {
      const header = await app.reveal('label');
      await header.hover(); await header.getByRole('button', { name: /menu/i }).click();
      await page.getByRole('menuitem', { name, exact: true }).click();
    };
    const filter = async () => {
      await menu('Filter');
      const panel = page.locator('.MuiDataGrid-filterForm');
      await panel.locator('.MuiDataGrid-filterFormOperatorInput').getByRole('combobox').selectOption({ label: 'equals' });
      await panel.getByRole('textbox', { name: 'Value', exact: true }).fill('Missing');
      await page.keyboard.press('Escape');
    };
    const positions = () => app.dialog().locator('label, .MuiDialogActions-root button').evaluateAll(nodes => nodes.map(node => {
      const box = node.getBoundingClientRect(); return { label: node.textContent ?? '', x: box.x, y: box.y };
    }));
    for (const step of steps) await audit.step(step.number, async () => {
      const text = step.text;
      if (step.number === 1) {
        if (number === 31) await page.setViewportSize({ width: 1024, height: 600 });
        page.on('dialog', async dialog => {
          if (dialog.type() === 'beforeunload') { await dialog.accept(); return; }
          alerts.push(dialog.type()); await dialog.dismiss();
        });
        if ([17, 21, 65, 66, 67, 68, 70].includes(number)) app.rows = [categoryRecord(101, 'Alpha'), categoryRecord(102, 'Beta')];
        if (number === 21) app.rows[0].active = true;
        if (number >= 51 && number <= 58) app.rows[0] = { ...tileRecord(), title: 'Old', subtitle: 'Before' };
        if (number === 56) app.rows.push({ ...tileRecord(), applicationTileId: 102, title: 'Second Tile' });
        if (number === 47) app.rows[0].title = 'ABC\u202eDEF';
        await app.setup();
        if (number === 16) { await page.route('**/api/auth/v1/fmo/admin/category/data', route => route.fulfill({ status: 200, json: { data: [categoryRecord(81, 'Cashflow')] } })); await page.reload({ waitUntil: 'domcontentloaded' }); }
        if (number === 18) await page.route('**/api/auth/v1/fmo/admin/tile/update', route => route.fulfill({ status: 500, json: { message: 'Save failed' } }));
        if (number === 16) { await expect(app.grid).toBeVisible(); await app.selectCategory('Cashflow'); }
        else await app.open();
        if ([14, 16, 18, 31, 38, 45].includes(number) || number >= 51 && number <= 58) await app.action('Edit').click();
        if (number === 15) await app.action('Verify').click();
        if (number === 17) await (await app.reveal('label', '101')).focus();
        if (number === 68) await filter();
        if (clockCase) { const now = new Date(); await page.clock.install({ time: now }); await page.clock.pauseAt(new Date(now.getTime() + 60_000)); }
        if (number === 47) { await app.action('Edit').click(); await field('Tile Name').fill('ABCDEF'); baseline = await positions(); await field('Tile Name').fill('ABC\u202eDEF'); await app.footerButton('Close').click(); }
        return;
      }
      let match: RegExpExecArray | null;
      if (text.includes('accessibility probe captures')) {
        disabledCount = await app.dialog().locator('input:disabled,textarea:disabled').count().catch(() => 0);
        await audit.record('accessibility-snapshot', { tree: await app.panel.ariaSnapshot(), disabledCount }); return;
      }
      if ((match = /textbox labelled "([^"]+)".* accessible name (?:equal to|retains accessible name) "([^"]+)"/.exec(text))) { await expect(field(match[1])).toHaveAccessibleName(match[2]); return; }
      if (text.includes('retains accessible name "Description"')) { await expect(field('Description')).toHaveAccessibleName('Description'); return; }
      if (text.includes('For each disabled input')) {
        expect(disabledCount).toBeGreaterThan(0);
        const snapshot = await app.dialog().ariaSnapshot(); await audit.record('verification-accessibility-tree', snapshot);
        expect((snapshot.match(/\[disabled\]/g) ?? []).length).toBeGreaterThanOrEqual(disabledCount); return;
      }
      if ((match = /ADMIN-A (?:types|types exactly) "(.*)"(?: as the replacement value| through IME composition)? (?:into|in) the (textbox|combobox) labelled "([^"]+)"/.exec(text))) {
        const target = app.field(match[3], match[2]);
        if (text.includes('through IME composition')) {
          await target.dispatchEvent('compositionstart', { data: '' });
          await target.fill(match[1]); await target.dispatchEvent('compositionupdate', { data: match[1] });
          await audit.record('controlled-ime-events', { events: ['compositionstart', 'input', 'compositionupdate'], value: match[1], limit: 'Programmatic composition fixture; native operating-system IME is not exercised.' });
        } else await target.fill(match[1]);
        return;
      }
      if ((match = /ADMIN-A presses "([^"]+)" on the (?:textbox|combobox|cell) labelled "([^"]+)"/.exec(text))) {
        if (match[2] === 'Category Label') await (await app.reveal('label', '101')).press(match[1]);
        else await app.field(match[2], match[2] === 'Aplication Category' ? 'combobox' : 'textbox').press(match[1]); return;
      }
      if (text.includes('option labelled "Cashflow"') && text.includes('highlighted')) {
        const combo = app.field('Aplication Category', 'combobox');
        const selected = await combo.getAttribute('aria-activedescendant'); expect(selected).toBeTruthy();
        await expect(page.locator(`[id="${selected}"]`)).toHaveText('Cashflow'); return;
      }
      if ((match = /(?:textbox|combobox) labelled "([^"]+)".* has value equal to "(.*)"$/.exec(text))) {
        await expect(app.field(match[1], match[1] === 'Aplication Category' ? 'combobox' : 'textbox')).toHaveValue(match[2]); return;
      }
      if (text.includes('exact fixture Unicode sequence')) { await expect(field('Tile Name')).toHaveValue('ABC\u202eDEF'); return; }
      if (text.includes('visual reading order')) { expect(await positions()).toEqual(baseline); return; }
      if (text.includes('retains visible label "Update"')) { await expect(app.footerButton('Update')).toHaveText('Update'); return; }
      if ((match = /ADMIN-A clicks the button labelled "(Update|Reset|Close|Edit)"/.exec(text))) {
        if (match[1] === 'Edit') {
          const idMatch = /"Record Id" equal to "(\d+)"/.exec(text); await app.action('Edit', idMatch?.[1] ?? '101').click();
        } else { await app.footerButton(match[1]).click(); if (match[1] === 'Update') await audit.record('ui-origin-admin-requests', app.requests); }
        return;
      }
      if (text.includes('alert inside the snackbar')) {
        const snackbar = page.getByTestId('MicroWebUI_base_snackbar');
        await expect(snackbar.locator('.MuiSnackbarContent-root[role="alert"]')).toHaveText('Save failed');
        const tree = await snackbar.ariaSnapshot(); await audit.record('save-error-accessibility-tree', tree);
        expect(tree).toContain('alert'); expect(tree).toContain('Save failed'); return;
      }
      if (text.includes('exposes a text or accessible state distinct')) {
        const first = await app.reveal('active', '101'), second = await app.reveal('active', '102');
        const value = (cell: typeof first) => cell.evaluate(node => ({ text: node.textContent,
          labels: Array.from(node.querySelectorAll('[aria-label],title')).map(item => item.getAttribute('aria-label') ?? item.textContent) }));
        const values = [await value(first), await value(second)]; await audit.record('status-accessibility-values', values);
        expect(values[0]).not.toEqual(values[1]); return;
      }
      if (text.includes('scrolls to the footer')) { await app.footerButton('Close').scrollIntoViewIfNeeded(); return; }
      if ((match = /button labelled "(Update|Reset|Close)".* is visible and enabled$/.exec(text))) {
        await expect(app.footerButton(match[1])).toBeVisible(); await expect(app.footerButton(match[1])).toBeEnabled(); return;
      }
      if ((match = /controlled event loop advances (\d+) milliseconds/.exec(text))) { await page.clock.runFor(Number(match[1])); return; }
      if (text.includes('controlled event loop') && text.includes('completes')) { await page.clock.runFor(1000); return; }
      if (text.includes('save fixture acknowledges') || text.includes('browser fixture reloads')) {
        await audit.record('persisted-received-payload', { rows: app.rows, requests: app.requests });
        await page.reload({ waitUntil: 'domcontentloaded' }); await app.portal.expectVisible(); await app.open(); return;
      }
      if (text.includes('captured update payload has title')) {
        const expected = /"(New|ABC)"/.exec(text)![1];
        const request = app.requests.filter(request => request.endpoint === 'tile/update').at(-1);
        await audit.record('captured-update-payload', request); expect(request?.body.title).toBe(expected); return;
      }
      if ((match = /Tile grid row.* contains "Tile Name" equal to "([^"]+)"/.exec(text))) { await expect(await app.reveal('title', '101')).toHaveText(match[1]); return; }
      if (text.includes('contains literal text')) { await expect(await app.reveal('label', '101')).toHaveText('<script>alert(1)</script>'); return; }
      if (text.includes('zero alert events')) { await audit.record('script-dialog-events', alerts); expect(alerts).toEqual([]); return; }
      if (text.includes('compositionend before blur')) { await field('Tile Name').dispatchEvent('compositionend', { data: '東京' }); return; }
      if (text.includes('Category Label') && text.endsWith('is focused')) { await expect(await app.reveal('label', '102')).toBeFocused(); return; }
      if (text.includes('Category Label') && text.endsWith('contains "Beta"')) { await expect(await app.reveal('label', '102')).toHaveText('Beta'); return; }
      if (text.includes('selects ascending sort')) { await (await app.reveal('label')).click(); return; }
      if (text.includes('selects descending sort')) { await (await app.reveal('label')).click(); await (await app.reveal('label')).click(); return; }
      if (text.includes('ordered Category grid label values')) {
        await expect(app.grid.locator('[data-id] [data-field="label"]')).toHaveText(number === 65 ? ['Alpha', 'Beta'] : ['Beta', 'Alpha']); return;
      }
      if (text.includes('selects an equals filter')) { await filter(); return; }
      if (text.includes('clears the filter')) {
        await menu('Filter'); await page.locator('.MuiDataGrid-filterForm').getByRole('button', { name: 'Delete', exact: true }).click(); await page.keyboard.press('Escape'); return;
      }
      if (text.includes('filtered Category grid data row count')) { await expect(app.grid.locator('[data-id]')).toHaveCount(0); return; }
      if ((match = /filtered pagination total equals (\d+)/.exec(text))) { await expect(app.grid.locator('.MuiTablePagination-displayedRows')).toHaveText(match[1] === '0' ? '0–0 of 0' : '1–2 of 2'); return; }
      if ((match = /Category Label.*"Record Id" equal to "(101|102)".* contains "(Alpha|Beta)"/.exec(text))) { await expect(await app.reveal('label', match[1])).toHaveText(match[2]); return; }
      if (text.includes('hidden visibility') || text.includes('visible state for "Owner"')) {
        await menu('Manage columns'); const checkbox = page.getByRole('checkbox', { name: 'Owner', exact: true }); await checkbox.setChecked(text.includes('visible state')); await page.keyboard.press('Escape'); return;
      }
      if (text.includes('column labelled "Owner"') && text.endsWith('is hidden')) { await expect(app.grid.locator('[role="columnheader"][data-field="ems2Role"]')).toHaveCount(0); return; }
      if (text.includes('column labelled "Owner"') && text.endsWith('is visible')) { await expect(await app.reveal('ems2Role')).toBeVisible(); return; }
      if (text.includes('cell for Owner')) { await expect(await app.reveal('ems2Role', '101')).toHaveText('TEST_OWNER'); return; }
      if (text.includes('selects CSV export')) {
        const wait = page.waitForEvent('download'); await app.grid.getByRole('button', { name: 'Export', exact: true }).click();
        await page.getByRole('menuitem', { name: 'Download as CSV', exact: true }).click(); const download = await wait;
        const stream = await download.createReadStream(); const chunks: Buffer[] = []; for await (const chunk of stream!) chunks.push(Buffer.from(chunk));
        csv = Buffer.concat(chunks).toString('utf8'); await audit.record('exported-csv', { filename: download.suggestedFilename(), csv }); return;
      }
      if (text.includes('artifact probe parses')) {
        // This fixture uses simple values. A CSV parser still preserves quoted commas and doubled quotes.
        rows = []; let row: string[] = [], value = '', quoted = false;
        for (let i = 0; i < csv.length; i++) { const c = csv[i]; if (c === '"') { if (quoted && csv[i + 1] === '"') { value += '"'; i++; } else quoted = !quoted; }
          else if (c === ',' && !quoted) { row.push(value); value = ''; } else if (c === '\n' && !quoted) { row.push(value.replace(/\r$/, '')); rows.push(row); row = []; value = ''; } else value += c; }
        if (row.length || value) { row.push(value); rows.push(row); } if (rows[0]?.[0]) rows[0][0] = rows[0][0].replace(/^\uFEFF/, '');
        await audit.record('parsed-export-csv', rows); return;
      }
      if (text.includes('exported Record Id') || text.includes('Each record appears exactly once')) {
        const idColumn = rows[0].indexOf('Record Id'), labelColumn = rows[0].indexOf('Category Label'); expect(idColumn).toBeGreaterThanOrEqual(0); expect(labelColumn).toBeGreaterThanOrEqual(0);
        const mapping = rows.slice(1).filter(row => row.some(Boolean)).map(row => [row[idColumn], row[labelColumn]]);
        expect(mapping).toEqual([['101', 'Alpha'], ['102', 'Beta']]); return;
      }
      throw new Error(`No administration UX binding for ${id} step ${step.number}: ${text}`);
    });
  });
}

type Pending = { route: Route; finish: () => void; key: number };
for (const number of [2, 3, 4, 5, 6, 7, 8, 9]) {
  const id = `UI-RISK-${String(number).padStart(3, '0')}`;
  test(`${id} administration source risk with live evidence`, async ({ page, audit }) => {
    const steps = await audit.defineCase(id);
    const kind: AdminKind = [5, 6, 7].includes(number) ? 'Tile' : 'Category';
    const app = new AdminApp(page, kind, id);
    const pending: Pending[] = [];
    const resolve = async (key: number) => {
      const entry = pending.find(item => item.key === key); expect(entry).toBeTruthy();
      const data = kind === 'Tile' ? [{ ...tileRecord(), title: key === 81 ? 'Tile A' : 'Tile B', applicationCategory: categoryRecord(key, key === 81 ? 'Fixture Category' : 'Other Category') }]
        : [{ ...categoryRecord(key), applicationCategoryAuditId: key === 101 ? 9001 : 9002 }];
      const outcome = await entry!.route.fulfill({ status: 200, json: { data } }).then(() => 'FULFILLED', () => 'REQUEST_ALREADY_ABORTED');
      entry!.finish(); await audit.record(`controlled-response-${key}`, { outcome, data });
    };
    for (const step of steps) await audit.step(step.number, async () => {
      const text = step.text;
      if (step.number === 1) { if (number === 9) app.rows.push(categoryRecord(102, 'Other Category')); await app.setup(); return; }
      if (step.number === 2) {
        if ([5, 6, 9].includes(number)) {
          await page.route(`**/api/auth/v1/fmo/admin/${kind === 'Tile' ? 'tile/data' : 'category/audit'}`, route => new Promise<void>(finish => {
            const body = route.request().postDataJSON(); pending.push({ route, finish, key: body.applicationCategory?.applicationCategoryId ?? body.applicationCategoryId ?? 0 });
          }));
          await expect(app.grid).toBeVisible();
          if (number === 6) await app.selectCategory();
        } else {
          if (number === 7) await page.route('**/api/auth/v1/fmo/admin/importmap/data', route => route.fulfill({ status: 200, json: { data: [71, 72].map(importMapId => ({ importMapId, keyName: '@fm/test', path: 'https://assets.example.test/v1.js' })) } }));
          if (number === 8) await page.route('**/api/auth/v1/fmo/admin/category/audit', route => route.fulfill({ status: 200, json: { data: [] } }));
          await app.open();
          if (number === 2) { await app.action('Edit').click(); await app.field('Category Label').fill('Unsaved'); }
          if (number === 3) { await app.panel.getByRole('button', { name: 'Create New Category', exact: true }).click(); await app.field('Category Label').fill('Unsaved'); }
          if (number === 4) await app.action('Verify').click();
          if (number === 7) await app.panel.getByRole('button', { name: 'Create New Tile', exact: true }).click();
        }
        return;
      }
      let match: RegExpExecArray | null;
      if ((match = /^Admin A clicks button named "([^"]+)"/.exec(text))) { await app.footerButton(match[1]).click(); return; }
      if (text === 'the verification dialog finishes rendering') { await expect(app.dialog()).toBeVisible(); return; }
      if (text.includes('Owner') && text.endsWith('is disabled')) { await expect(app.field('Owner')).toBeDisabled(); return; }
      if ((match = /^textbox named "([^"]+)".* has value "([^"]*)"$/.exec(text))) { await expect(app.field(match[1])).toHaveValue(match[2]); return; }
      if ((match = /^button named "([^"]+)".* is visible$/.exec(text))) { await expect(app.footerButton(match[1])).toBeVisible(); return; }
      if ((match = /^Admin A opens combobox named "([^"]+)"/.exec(text))) { await (match[1] === 'Application Category' ? app.category : app.field(match[1], 'combobox')).click(); return; }
      if ((match = /^Admin A clicks option named "([^"]+)"/.exec(text))) { await page.getByRole('option', { name: match[1], exact: true, includeHidden: true }).click(); return; }
      if (text.includes('resolves the Other Category')) { await resolve(82); return; }
      if (text.includes('resolves the earlier Fixture') || text.includes('resolves the pending Fixture')) { await resolve(81); return; }
      if (text.includes('resolves record 102 audit')) { await resolve(102); return; }
      if (text.includes('resolves the earlier record 101')) { await resolve(101); return; }
      if (text.includes('category-clear target')) { await app.category.locator('..').getByRole('button', { name: 'Clear', exact: true }).click(); return; }
      if (text.includes('Application Category') && text.includes('has an empty value')) { await expect(app.category).toHaveValue(''); return; }
      if (text.includes('Application Category') && text.includes('has value "Other Category"')) { await expect(app.category).toHaveValue('Other Category'); return; }
      if (text.includes('every displayed tile row')) { await app.reveal('title', '101'); await expect(app.grid.locator('[data-id] [data-field="title"]')).toHaveText(['Tile B']); return; }
      if (text.includes('data row count') && text.endsWith('equals 0')) { await expect(app.grid.locator('[data-id]')).toHaveCount(0); return; }
      if (text.includes('Create New Tile') && text.endsWith('is disabled')) { await expect(app.panel.getByRole('button', { name: 'Create New Tile', exact: true })).toBeDisabled(); return; }
      if (text.startsWith('exactly 2 options')) { await expect(page.getByRole('option', { includeHidden: true }).filter({ hasText: /^@fm\/test$/ })).toHaveCount(2); return; }
      if ((match = /option displays record ID "(\d+)"/.exec(text))) { await expect(page.getByRole('option', { includeHidden: true }).filter({ hasText: new RegExp(match[1]) })).toHaveCount(1); return; }
      if ((match = /^Admin A clicks icon button named "Audit" inside row with Record Id "(\d+)"/.exec(text))) { await app.action('Audit', match[1]).click({ timeout: 5000 }); return; }
      if (text.includes('explicit empty-history status')) { await expect(app.panel.getByRole('status').filter({ hasText: /(?:no|empty).*history/i })).toBeVisible(); return; }
      if (text.includes('identifies source record "102"') || text.includes('each cell in the "Category ID"')) { await expect(app.auditDialog().locator('[data-id] [data-field="applicationCategoryId"]')).toHaveText(['102']); return; }
      throw new Error(`No source-risk UI binding for ${id} step ${step.number}: ${text}`);
    });
  });
}
