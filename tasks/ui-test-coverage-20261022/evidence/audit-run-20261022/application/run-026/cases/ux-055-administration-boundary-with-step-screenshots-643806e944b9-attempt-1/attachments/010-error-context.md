# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-ux.spec.ts >> UX-055 administration boundary with step screenshots
- Location: e2e/audit-specs/admin-ux.spec.ts:12:3

# Error details

```
Error: expect(locator).toHaveValue(expected) failed

Locator: locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText(/^(?:new|edit|verify|deactivate) ID:/) }).getByRole('textbox', { name: 'Tile Name', exact: true, includeHidden: true })
Expected: "Old"
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toHaveValue" locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText(/^(?:new|edit|verify|deactivate) ID:/) }).getByRole('textbox', { name: 'Tile Name', exact: true, includeHidden: true }) with timeout 5000ms
  - waiting for locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText(/^(?:new|edit|verify|deactivate) ID:/) }).getByRole('textbox', { name: 'Tile Name', exact: true, includeHidden: true })

```

# Page snapshot

```yaml
- generic [ref=e4]:
  - generic [ref=e10]:
    - generic [ref=e11] [cursor=pointer]: New Tile
    - generic [ref=e19]:
      - text: dark
      - checkbox [ref=e22] [cursor=pointer]
    - group [ref=e26]:
      - generic [ref=e27]: 05:35 UTC
      - checkbox [checked] [ref=e30] [cursor=pointer]
    - button [ref=e34] [cursor=pointer]:
      - generic [ref=e35]: A
    - button [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region [ref=e48]:
          - textbox [ref=e52]: Tile
      - button [ref=e54] [cursor=pointer]
    - tabpanel [ref=e59]:
      - generic [ref=e61]:
        - generic [ref=e62]:
          - generic [ref=e64]:
            - generic [ref=e65]: Application Category
            - generic [ref=e66]:
              - combobox [ref=e67]: Fixture Category
              - button [ref=e69] [cursor=pointer]
          - button [ref=e72] [cursor=pointer]
        - generic [ref=e75]:
          - button [ref=e76] [cursor=pointer]: Create New Tile
          - generic [ref=e77]:
            - grid [ref=e78]:
              - button [ref=e80] [cursor=pointer]: Export
              - generic [ref=e84]:
                - rowgroup [ref=e85]:
                  - row [ref=e86]:
                    - columnheader [ref=e87]:
                      - generic [ref=e88]: Actions
                    - columnheader [ref=e90] [cursor=pointer]:
                      - generic [ref=e91]: Tile Name
                    - columnheader [ref=e93] [cursor=pointer]:
                      - generic [ref=e94]: Description
                    - columnheader [ref=e96] [cursor=pointer]:
                      - generic [ref=e97]: Image URL for Dark Theme
                    - columnheader [ref=e99] [cursor=pointer]:
                      - generic [ref=e100]: Image URL for Light Theme
                    - columnheader [ref=e102] [cursor=pointer]:
                      - generic [ref=e103]: Container
                    - columnheader [ref=e105] [cursor=pointer]:
                      - generic [ref=e106]: Module Path
                    - columnheader [ref=e108] [cursor=pointer]:
                      - generic [ref=e109]: Tile Path
                    - columnheader [ref=e111] [cursor=pointer]:
                      - generic [ref=e112]: Role Subject
                    - columnheader [ref=e114] [cursor=pointer]:
                      - generic [ref=e115]: Role Entities
                - rowgroup [ref=e117]:
                  - row [ref=e118]:
                    - cell [ref=e119]:
                      - menu [ref=e120]:
                        - menuitem [ref=e121] [cursor=pointer]
                        - menuitem [ref=e124] [cursor=pointer]
                        - menuitem [disabled]
                        - menuitem [ref=e127] [cursor=pointer]
                    - cell [ref=e130]: Old
                    - cell [ref=e131]: Before
                    - cell [ref=e132]: darkIcons/icon01.svg
                    - cell [ref=e133]: lightIcons/icon01.svg
                    - cell [ref=e134]: "@fm/test"
                    - cell [ref=e135]: /test
                    - cell [ref=e136]: /test-entry
                    - cell [ref=e137]: TEST_SUBJECT
                    - cell [ref=e138]: TEST_ENTITY
              - generic [ref=e141]:
                - paragraph [ref=e142]: "Rows per page:"
                - generic [ref=e143]:
                  - combobox [ref=e144] [cursor=pointer]: "20"
                  - textbox [aria-hidden]: "20"
                - paragraph [ref=e145]: 1–1 of 1
                - generic [ref=e146]:
                  - button [disabled]
                  - button [disabled]
            - dialog [ref=e149]:
              - heading [level=2] [ref=e150]:
                - generic [ref=e151]:
                  - generic [ref=e152]: "undefined ID: 101"
                  - generic [ref=e153]:
                    - button [ref=e154] [cursor=pointer]: Maximize
                    - button [disabled]:
                      - generic: Close
              - generic [ref=e159]:
                - generic [ref=e161]:
                  - generic [ref=e162]: Aplication Category
                  - generic [ref=e163]:
                    - combobox [ref=e164]: Fixture Category
                    - button [ref=e166] [cursor=pointer]
                - generic [ref=e169]:
                  - generic [ref=e170]: Tile Name
                  - textbox [ref=e172]:
                    - /placeholder: Type here
                    - text: Old
                - generic [ref=e173]:
                  - generic [ref=e174]: Description
                  - textbox [ref=e176]:
                    - /placeholder: Type here
                    - text: Before
                - generic [ref=e178]:
                  - generic [ref=e179]: Image URL for Dark Theme
                  - generic [ref=e180]:
                    - combobox [ref=e181]: darkIcons/icon01.svg
                    - button [ref=e183] [cursor=pointer]
                - generic [ref=e187]:
                  - generic [ref=e188]: Image URL for Light Theme
                  - generic [ref=e189]:
                    - combobox [ref=e190]: lightIcons/icon01.svg
                    - button [ref=e192] [cursor=pointer]
                - generic [ref=e196]:
                  - generic [ref=e197]: Container
                  - generic [ref=e198]:
                    - combobox [ref=e199]: "@fm/test"
                    - button [ref=e201] [cursor=pointer]
                - generic [ref=e204]:
                  - generic [ref=e205]: Module Path
                  - textbox [ref=e207]:
                    - /placeholder: Type here
                    - text: /test
                - generic [ref=e208]:
                  - generic [ref=e209]: Tile Path
                  - textbox [ref=e211]:
                    - /placeholder: Type here
                    - text: /test-entry
                - generic [ref=e212]:
                  - generic [ref=e213]: Role Subject
                  - textbox [ref=e215]:
                    - /placeholder: Type here
                    - text: TEST_SUBJECT
                - generic [ref=e216]:
                  - generic [ref=e217]: Role Entities
                  - textbox [ref=e219]:
                    - /placeholder: Type here
                    - text: TEST_ENTITY
                - generic [ref=e220]:
                  - generic [ref=e221]: Is Template?
                  - generic [ref=e222]:
                    - combobox [ref=e223] [cursor=pointer]: "false"
                    - textbox [aria-hidden]: "false"
                - generic [ref=e224]:
                  - generic [ref=e225]: Email Support
                  - textbox [ref=e227]:
                    - /placeholder: Type here
                    - text: support@example.test
                - generic [ref=e228]:
                  - generic [ref=e229]: Owner
                  - textbox [disabled] [ref=e231]:
                    - /placeholder: Type here
                    - text: TEST_OWNER
                - generic [ref=e232]:
                  - generic [ref=e233]: Verified?
                  - textbox [disabled] [ref=e235]:
                    - /placeholder: Type here
                    - text: "false"
                - generic [ref=e236]:
                  - generic [ref=e237]: Created At
                  - textbox [disabled] [ref=e239]:
                    - /placeholder: Type here
                    - text: 2026-10-21T00:05:00Z
                - generic [ref=e240]:
                  - generic [ref=e241]: Created By
                  - textbox [disabled] [ref=e243]:
                    - /placeholder: Type here
                    - text: UI-ADMIN-01
                - generic [ref=e244]:
                  - generic [ref=e245]: Updated At
                  - textbox [disabled] [ref=e247]:
                    - /placeholder: Type here
                    - text: 2026-10-22T00:05:00Z
                - generic [ref=e248]:
                  - generic [ref=e249]: Updated By
                  - textbox [disabled] [ref=e251]:
                    - /placeholder: Type here
                    - text: UI-ADMIN-01
                - generic [ref=e252]:
                  - generic [ref=e253]: Record Id
                  - textbox [disabled] [ref=e255]:
                    - /placeholder: <<will be auto generated>>
                    - text: "101"
                - generic [ref=e256]:
                  - generic [ref=e257]: Aplication Category Record Id
                  - textbox [disabled] [ref=e259]:
                    - /placeholder: <<will be auto generated>>
                    - text: "81"
                - generic [ref=e260]:
                  - generic [ref=e261]: Container Record Id
                  - textbox [disabled] [ref=e263]:
                    - /placeholder: <<will be auto generated>>
                    - text: "71"
                - generic [ref=e264]:
                  - generic [ref=e265]: Order No
                  - spinbutton [ref=e267]: "7"
                - generic [ref=e268]:
                  - generic [ref=e269]: Filter Rule
                  - textbox [ref=e271]:
                    - /placeholder: Type here
                - generic [ref=e272]:
                  - generic [ref=e273]: Entry Name
                  - textbox [ref=e275]:
                    - /placeholder: Type here
                    - text: Global
              - generic [ref=e276]:
                - button [active] [ref=e277] [cursor=pointer]: Reset
                - button [ref=e278] [cursor=pointer]: Close
              - button [ref=e279]
```

# Test source

```ts
  1   | import { test, expect } from '../support/audit-fixture.js';
  2   | import { AdminApp, categoryRecord, tileRecord, type AdminKind } from '../support/admin-app.js';
  3   | import type { Route } from '@playwright/test';
  4   | 
  5   | test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES', timezoneId: 'Asia/Singapore',
  6   |   auditFixture: 'Actual React administration screens. Controlled browser credentials, role, records, and BFF responses. Save probes persist the received UI payload without replacing it with expected values. Declared clock emulation controls field timers. Proposed accessibility and source-risk expectations remain separate from business approval.' });
  7   | 
  8   | const ux = [14, 15, 16, 17, 18, 21, 31, 38, 45, 47, 51, 52, 53, 54, 55, 56, 57, 58, 65, 66, 67, 68, 69, 70];
  9   | 
  10  | for (const number of ux) {
  11  |   const id = `UX-${String(number).padStart(3, '0')}`;
  12  |   test(`${id} administration boundary with step screenshots`, async ({ page, audit }) => {
  13  |     const steps = await audit.defineCase(id);
  14  |     const category = [17, 21, 38, 65, 66, 67, 68, 69, 70].includes(number);
  15  |     const app = new AdminApp(page, category ? 'Category' : 'Tile', id);
  16  |     const alerts: string[] = [];
  17  |     let csv = ''; let rows: string[][] = [];
  18  |     let disabledCount = 0;
  19  |     let baseline: { label: string; x: number; y: number }[] = [];
  20  |     const clockCase = number === 38 || number >= 51 && number <= 58;
  21  |     const field = (name: string) => app.field(name);
  22  |     const menu = async (name: string) => {
  23  |       const header = await app.reveal('label');
  24  |       await header.hover(); await header.getByRole('button', { name: /menu/i }).click();
  25  |       await page.getByRole('menuitem', { name, exact: true }).click();
  26  |     };
  27  |     const filter = async () => {
  28  |       await menu('Filter');
  29  |       const panel = page.locator('.MuiDataGrid-filterForm');
  30  |       await panel.locator('.MuiDataGrid-filterFormOperatorInput').getByRole('combobox').click();
  31  |       await page.getByRole('option', { name: 'equals', exact: true }).click();
  32  |       await panel.getByRole('textbox', { name: 'Value', exact: true }).fill('Missing');
  33  |       await page.keyboard.press('Escape');
  34  |     };
  35  |     const positions = () => app.dialog().locator('label, .MuiDialogActions-root button').evaluateAll(nodes => nodes.map(node => {
  36  |       const box = node.getBoundingClientRect(); return { label: node.textContent ?? '', x: box.x, y: box.y };
  37  |     }));
  38  |     for (const step of steps) await audit.step(step.number, async () => {
  39  |       const text = step.text;
  40  |       if (step.number === 1) {
  41  |         if (number === 31) await page.setViewportSize({ width: 1024, height: 600 });
  42  |         page.on('dialog', async dialog => { alerts.push(dialog.type()); await dialog.dismiss(); });
  43  |         if ([17, 21, 65, 66, 67, 68, 70].includes(number)) app.rows = [categoryRecord(101, 'Alpha'), categoryRecord(102, 'Beta')];
  44  |         if (number === 21) app.rows[0].active = true;
  45  |         if (number >= 51 && number <= 58) app.rows[0] = { ...tileRecord(), title: 'Old', subtitle: 'Before' };
  46  |         if (number === 56) app.rows.push({ ...tileRecord(), applicationTileId: 102, title: 'Second Tile' });
  47  |         if (number === 47) app.rows[0].title = 'ABC\u202eDEF';
  48  |         await app.setup();
  49  |         if (number === 16) { await page.route('**/api/auth/v1/fmo/admin/category/data', route => route.fulfill({ status: 200, json: { data: [categoryRecord(81, 'Cashflow')] } })); await page.reload(); }
  50  |         if (number === 18) await page.route('**/api/auth/v1/fmo/admin/tile/update', route => route.fulfill({ status: 500, json: { message: 'Save failed' } }));
  51  |         if (number === 16) { await expect(app.grid).toBeVisible(); await app.selectCategory('Cashflow'); }
  52  |         else await app.open();
  53  |         if ([14, 16, 18, 31, 38, 45].includes(number) || number >= 51 && number <= 58) await app.action('Edit').click();
  54  |         if (number === 15) await app.action('Verify').click();
  55  |         if (number === 17) await (await app.reveal('label', '101')).focus();
  56  |         if (number === 68) await filter();
  57  |         if (clockCase) { const now = new Date(); await page.clock.install({ time: now }); await page.clock.pauseAt(new Date(now.getTime() + 60_000)); }
  58  |         if (number === 47) { await app.action('Edit').click(); await field('Tile Name').fill('ABCDEF'); baseline = await positions(); await field('Tile Name').fill('ABC\u202eDEF'); await app.footerButton('Close').click(); }
  59  |         return;
  60  |       }
  61  |       let match: RegExpExecArray | null;
  62  |       if (text.includes('accessibility probe captures')) {
  63  |         disabledCount = await app.dialog().locator('input:disabled,textarea:disabled').count().catch(() => 0);
  64  |         await audit.record('accessibility-snapshot', { tree: await app.panel.ariaSnapshot(), disabledCount }); return;
  65  |       }
  66  |       if ((match = /textbox labelled "([^"]+)".* accessible name (?:equal to|retains accessible name) "([^"]+)"/.exec(text))) { await expect(field(match[1])).toHaveAccessibleName(match[2]); return; }
  67  |       if (text.includes('retains accessible name "Description"')) { await expect(field('Description')).toHaveAccessibleName('Description'); return; }
  68  |       if (text.includes('For each disabled input')) {
  69  |         expect(disabledCount).toBeGreaterThan(0);
  70  |         const snapshot = await app.dialog().ariaSnapshot(); await audit.record('verification-accessibility-tree', snapshot);
  71  |         expect((snapshot.match(/\[disabled\]/g) ?? []).length).toBeGreaterThanOrEqual(disabledCount); return;
  72  |       }
  73  |       if ((match = /ADMIN-A (?:types|types exactly) "(.*)"(?: as the replacement value| through IME composition)? (?:into|in) the (textbox|combobox) labelled "([^"]+)"/.exec(text))) {
  74  |         await app.field(match[3], match[2]).fill(match[1]); return;
  75  |       }
  76  |       if ((match = /ADMIN-A presses "([^"]+)" on the (?:textbox|combobox|cell) labelled "([^"]+)"/.exec(text))) {
  77  |         if (match[2] === 'Category Label') await (await app.reveal('label', '101')).press(match[1]);
  78  |         else await app.field(match[2], match[2] === 'Aplication Category' ? 'combobox' : 'textbox').press(match[1]); return;
  79  |       }
  80  |       if (text.includes('option labelled "Cashflow"') && text.includes('highlighted')) {
  81  |         const combo = app.field('Aplication Category', 'combobox');
  82  |         const selected = await combo.getAttribute('aria-activedescendant'); expect(selected).toBeTruthy();
  83  |         await expect(page.locator(`[id="${selected}"]`)).toHaveText('Cashflow'); return;
  84  |       }
  85  |       if ((match = /(?:textbox|combobox) labelled "([^"]+)".* has value equal to "(.*)"$/.exec(text))) {
> 86  |         await expect(app.field(match[1], match[1] === 'Aplication Category' ? 'combobox' : 'textbox')).toHaveValue(match[2]); return;
      |                                                                                                        ^ Error: expect(locator).toHaveValue(expected) failed
  87  |       }
  88  |       if (text.includes('exact fixture Unicode sequence')) { await expect(field('Tile Name')).toHaveValue('ABC\u202eDEF'); return; }
  89  |       if (text.includes('visual reading order')) { expect(await positions()).toEqual(baseline); return; }
  90  |       if (text.includes('retains visible label "Update"')) { await expect(app.footerButton('Update')).toHaveText('Update'); return; }
  91  |       if ((match = /ADMIN-A clicks the button labelled "(Update|Reset|Close|Edit)"/.exec(text))) {
  92  |         if (match[1] === 'Edit') {
  93  |           const idMatch = /"Record Id" equal to "(\d+)"/.exec(text); await app.action('Edit', idMatch?.[1] ?? '101').click();
  94  |         } else { await app.footerButton(match[1]).click(); if (match[1] === 'Update') await audit.record('ui-origin-admin-requests', app.requests); }
  95  |         return;
  96  |       }
  97  |       if (text.includes('alert inside the snackbar')) { await expect(page.getByRole('alert').filter({ hasText: /^Save failed$/ })).toBeVisible(); return; }
  98  |       if (text.includes('exposes a text or accessible state distinct')) {
  99  |         const first = await app.reveal('active', '101'), second = await app.reveal('active', '102');
  100 |         const value = (cell: typeof first) => cell.evaluate(node => ({ text: node.textContent,
  101 |           labels: Array.from(node.querySelectorAll('[aria-label],title')).map(item => item.getAttribute('aria-label') ?? item.textContent) }));
  102 |         const values = [await value(first), await value(second)]; await audit.record('status-accessibility-values', values);
  103 |         expect(values[0]).not.toEqual(values[1]); return;
  104 |       }
  105 |       if (text.includes('scrolls to the footer')) { await app.footerButton('Close').scrollIntoViewIfNeeded(); return; }
  106 |       if ((match = /button labelled "(Update|Reset|Close)".* is visible and enabled$/.exec(text))) {
  107 |         await expect(app.footerButton(match[1])).toBeVisible(); await expect(app.footerButton(match[1])).toBeEnabled(); return;
  108 |       }
  109 |       if ((match = /controlled event loop advances (\d+) milliseconds/.exec(text))) { await page.clock.runFor(Number(match[1])); return; }
  110 |       if (text.includes('controlled event loop') && text.includes('completes')) { await page.clock.runFor(1000); return; }
  111 |       if (text.includes('save fixture acknowledges') || text.includes('browser fixture reloads')) {
  112 |         await audit.record('persisted-received-payload', { rows: app.rows, requests: app.requests });
  113 |         await page.reload(); await app.portal.expectVisible(); await app.open(); return;
  114 |       }
  115 |       if (text.includes('captured update payload has title')) {
  116 |         const expected = /"(New|ABC)"/.exec(text)![1];
  117 |         const request = app.requests.filter(request => request.endpoint === 'tile/update').at(-1);
  118 |         await audit.record('captured-update-payload', request); expect(request?.body.title).toBe(expected); return;
  119 |       }
  120 |       if ((match = /Tile grid row.* contains "Tile Name" equal to "([^"]+)"/.exec(text))) { await expect(await app.reveal('title', '101')).toHaveText(match[1]); return; }
  121 |       if (text.includes('contains literal text')) { await expect(await app.reveal('label', '101')).toHaveText('<script>alert(1)</script>'); return; }
  122 |       if (text.includes('zero alert events')) { await audit.record('script-dialog-events', alerts); expect(alerts).toEqual([]); return; }
  123 |       if (text.includes('compositionend before blur')) { await field('Tile Name').dispatchEvent('compositionend', { data: '東京' }); return; }
  124 |       if (text.includes('Category Label') && text.endsWith('is focused')) { await expect(await app.reveal('label', '102')).toBeFocused(); return; }
  125 |       if (text.includes('Category Label') && text.endsWith('contains "Beta"')) { await expect(await app.reveal('label', '102')).toHaveText('Beta'); return; }
  126 |       if (text.includes('selects ascending sort')) { await (await app.reveal('label')).click(); return; }
  127 |       if (text.includes('selects descending sort')) { await (await app.reveal('label')).click(); await (await app.reveal('label')).click(); return; }
  128 |       if (text.includes('ordered Category grid label values')) {
  129 |         await expect(app.grid.locator('[data-id] [data-field="label"]')).toHaveText(number === 65 ? ['Alpha', 'Beta'] : ['Beta', 'Alpha']); return;
  130 |       }
  131 |       if (text.includes('selects an equals filter')) { await filter(); return; }
  132 |       if (text.includes('clears the filter')) {
  133 |         await menu('Filter'); await page.locator('.MuiDataGrid-filterForm').getByRole('button', { name: 'Delete', exact: true }).click(); await page.keyboard.press('Escape'); return;
  134 |       }
  135 |       if (text.includes('filtered Category grid data row count')) { await expect(app.grid.locator('[data-id]')).toHaveCount(0); return; }
  136 |       if ((match = /filtered pagination total equals (\d+)/.exec(text))) { await expect(app.grid.locator('.MuiTablePagination-displayedRows')).toHaveText(match[1] === '0' ? '0–0 of 0' : '1–2 of 2'); return; }
  137 |       if ((match = /Category Label.*"Record Id" equal to "(101|102)".* contains "(Alpha|Beta)"/.exec(text))) { await expect(await app.reveal('label', match[1])).toHaveText(match[2]); return; }
  138 |       if (text.includes('hidden visibility') || text.includes('visible state for "Owner"')) {
  139 |         await menu('Manage columns'); const checkbox = page.getByRole('checkbox', { name: 'Owner', exact: true }); await checkbox.setChecked(text.includes('visible state')); await page.keyboard.press('Escape'); return;
  140 |       }
  141 |       if (text.includes('column labelled "Owner"') && text.endsWith('is hidden')) { await expect(app.grid.locator('[role="columnheader"][data-field="ems2Role"]')).toHaveCount(0); return; }
  142 |       if (text.includes('column labelled "Owner"') && text.endsWith('is visible')) { await expect(await app.reveal('ems2Role')).toBeVisible(); return; }
  143 |       if (text.includes('cell for Owner')) { await expect(await app.reveal('ems2Role', '101')).toHaveText('TEST_OWNER'); return; }
  144 |       if (text.includes('selects CSV export')) {
  145 |         const wait = page.waitForEvent('download'); await app.grid.getByRole('button', { name: 'Export', exact: true }).click();
  146 |         await page.getByRole('menuitem', { name: 'Download as CSV', exact: true }).click(); const download = await wait;
  147 |         const stream = await download.createReadStream(); const chunks: Buffer[] = []; for await (const chunk of stream!) chunks.push(Buffer.from(chunk));
  148 |         csv = Buffer.concat(chunks).toString('utf8'); await audit.record('exported-csv', { filename: download.suggestedFilename(), csv }); return;
  149 |       }
  150 |       if (text.includes('artifact probe parses')) {
  151 |         // This fixture uses simple values. A CSV parser still preserves quoted commas and doubled quotes.
  152 |         rows = []; let row: string[] = [], value = '', quoted = false;
  153 |         for (let i = 0; i < csv.length; i++) { const c = csv[i]; if (c === '"') { if (quoted && csv[i + 1] === '"') { value += '"'; i++; } else quoted = !quoted; }
  154 |           else if (c === ',' && !quoted) { row.push(value); value = ''; } else if (c === '\n' && !quoted) { row.push(value.replace(/\r$/, '')); rows.push(row); row = []; value = ''; } else value += c; }
  155 |         if (row.length || value) { row.push(value); rows.push(row); } if (rows[0]?.[0]) rows[0][0] = rows[0][0].replace(/^\uFEFF/, '');
  156 |         await audit.record('parsed-export-csv', rows); return;
  157 |       }
  158 |       if (text.includes('exported Record Id') || text.includes('Each record appears exactly once')) {
  159 |         const idColumn = rows[0].indexOf('Record Id'), labelColumn = rows[0].indexOf('Category Label'); expect(idColumn).toBeGreaterThanOrEqual(0); expect(labelColumn).toBeGreaterThanOrEqual(0);
  160 |         const mapping = rows.slice(1).filter(row => row.some(Boolean)).map(row => [row[idColumn], row[labelColumn]]);
  161 |         expect(mapping).toEqual([['101', 'Alpha'], ['102', 'Beta']]); return;
  162 |       }
  163 |       throw new Error(`No administration UX binding for ${id} step ${step.number}: ${text}`);
  164 |     });
  165 |   });
  166 | }
  167 | 
  168 | type Pending = { route: Route; finish: () => void; key: number };
  169 | for (const number of [2, 3, 4, 5, 6, 7, 8, 9]) {
  170 |   const id = `UI-RISK-${String(number).padStart(3, '0')}`;
  171 |   test(`${id} administration source risk with live evidence`, async ({ page, audit }) => {
  172 |     const steps = await audit.defineCase(id);
  173 |     const kind: AdminKind = [5, 6, 7].includes(number) ? 'Tile' : 'Category';
  174 |     const app = new AdminApp(page, kind, id);
  175 |     const pending: Pending[] = [];
  176 |     const resolve = async (key: number) => {
  177 |       const entry = pending.find(item => item.key === key); expect(entry).toBeTruthy();
  178 |       const data = kind === 'Tile' ? [{ ...tileRecord(), title: key === 81 ? 'Tile A' : 'Tile B', applicationCategory: categoryRecord(key, key === 81 ? 'Fixture Category' : 'Other Category') }]
  179 |         : [{ ...categoryRecord(key), applicationCategoryAuditId: key === 101 ? 9001 : 9002 }];
  180 |       const outcome = await entry!.route.fulfill({ status: 200, json: { data } }).then(() => 'FULFILLED', () => 'REQUEST_ALREADY_ABORTED');
  181 |       entry!.finish(); await audit.record(`controlled-response-${key}`, { outcome, data });
  182 |     };
  183 |     for (const step of steps) await audit.step(step.number, async () => {
  184 |       const text = step.text;
  185 |       if (step.number === 1) { if (number === 9) app.rows.push(categoryRecord(102, 'Other Category')); await app.setup(); return; }
  186 |       if (step.number === 2) {
```