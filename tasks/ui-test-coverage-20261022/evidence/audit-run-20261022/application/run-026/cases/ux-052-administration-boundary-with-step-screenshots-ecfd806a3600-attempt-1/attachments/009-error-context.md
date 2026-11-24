# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-ux.spec.ts >> UX-052 administration boundary with step screenshots
- Location: e2e/audit-specs/admin-ux.spec.ts:12:3

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: "New"
Received: "Old"
```

# Page snapshot

```yaml
- generic [ref=e4]:
  - generic [ref=e7]:
    - img "Markets Operations One logo" [ref=e9]
    - generic [ref=e10]:
      - generic [ref=e11] [cursor=pointer]:
        - img "new tile" [ref=e13]
        - generic [ref=e14]: New Tile
      - generic [ref=e15]:
        - img "dark" [ref=e17]
        - generic [ref=e19]:
          - text: dark
          - checkbox "Theme Switch" [ref=e22] [cursor=pointer]
      - group [ref=e26]:
        - generic [ref=e27]: 05:35 UTC
        - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
      - button "User Profiles" [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button "Share Feedback" [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist "workspaces" [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region "Tile" [ref=e48]:
          - textbox "Workspace Name" [ref=e52]: Tile
      - button "Add Workspace" [ref=e54] [cursor=pointer]
    - tabpanel [ref=e59]:
      - generic [ref=e61]:
        - generic [ref=e62]:
          - generic [ref=e64]:
            - generic [ref=e65]: Application Category
            - generic [ref=e66]:
              - combobox "Application Category" [ref=e67]: Fixture Category
              - button "Open" [ref=e69] [cursor=pointer]
          - button "refresh" [ref=e72] [cursor=pointer]
        - generic [ref=e75]:
          - button "Create New Tile" [ref=e76] [cursor=pointer]
          - grid [ref=e78]:
            - button "Export" [ref=e80] [cursor=pointer]
            - generic [ref=e84]:
              - rowgroup [ref=e85]:
                - row [ref=e86]:
                  - columnheader "Actions" [ref=e87]
                  - columnheader "Tile Name" [ref=e90] [cursor=pointer]
                  - columnheader "Description" [ref=e93] [cursor=pointer]
                  - columnheader "Image URL for Dark Theme" [ref=e96] [cursor=pointer]
                  - columnheader "Image URL for Light Theme" [ref=e99] [cursor=pointer]
                  - columnheader "Container" [ref=e102] [cursor=pointer]
                  - columnheader "Module Path" [ref=e105] [cursor=pointer]
                  - columnheader "Tile Path" [ref=e108] [cursor=pointer]
                  - columnheader "Role Subject" [ref=e111] [cursor=pointer]
                  - columnheader "Role Entities" [ref=e114] [cursor=pointer]
              - rowgroup [ref=e117]:
                - row [ref=e118]:
                  - cell [ref=e119]:
                    - menu [ref=e120]:
                      - menuitem "Edit" [active] [ref=e121] [cursor=pointer]
                      - menuitem "Verify" [ref=e124] [cursor=pointer]
                      - menuitem "Deactivate" [disabled]
                      - menuitem "Audit" [ref=e127] [cursor=pointer]
                  - cell "Old" [ref=e130]
                  - cell "Before" [ref=e131]
                  - cell "darkIcons/icon01.svg" [ref=e132]
                  - cell "lightIcons/icon01.svg" [ref=e133]
                  - cell "@fm/test" [ref=e134]
                  - cell "/test" [ref=e135]
                  - cell "/test-entry" [ref=e136]
                  - cell "TEST_SUBJECT" [ref=e137]
                  - cell "TEST_ENTITY" [ref=e138]
            - generic [ref=e141]:
              - paragraph [ref=e142]: "Rows per page:"
              - generic [ref=e143]:
                - 'combobox "Rows per page: 20" [ref=e144] [cursor=pointer]': "20"
                - textbox [aria-hidden]: "20"
              - paragraph [ref=e145]: 1–1 of 1
              - generic [ref=e146]:
                - button "Go to previous page" [disabled]
                - button "Go to next page" [disabled]
```

# Test source

```ts
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
  86  |         await expect(app.field(match[1], match[1] === 'Aplication Category' ? 'combobox' : 'textbox')).toHaveValue(match[2]); return;
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
> 118 |         await audit.record('captured-update-payload', request); expect(request?.body.title).toBe(expected); return;
      |                                                                                             ^ Error: expect(received).toBe(expected) // Object.is equality
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
  187 |         if ([5, 6, 9].includes(number)) {
  188 |           await page.route(`**/api/auth/v1/fmo/admin/${kind === 'Tile' ? 'tile/data' : 'category/audit'}`, route => new Promise<void>(finish => {
  189 |             const body = route.request().postDataJSON(); pending.push({ route, finish, key: body.applicationCategory?.applicationCategoryId ?? body.applicationCategoryId ?? 0 });
  190 |           }));
  191 |           await expect(app.grid).toBeVisible();
  192 |           if (number === 6) await app.selectCategory();
  193 |         } else {
  194 |           if (number === 7) await page.route('**/api/auth/v1/fmo/admin/importmap/data', route => route.fulfill({ status: 200, json: { data: [71, 72].map(importMapId => ({ importMapId, keyName: '@fm/test', path: 'https://assets.example.test/v1.js' })) } }));
  195 |           if (number === 8) await page.route('**/api/auth/v1/fmo/admin/category/audit', route => route.fulfill({ status: 200, json: { data: [] } }));
  196 |           await app.open();
  197 |           if (number === 2) { await app.action('Edit').click(); await app.field('Category Label').fill('Unsaved'); }
  198 |           if (number === 3) { await app.panel.getByRole('button', { name: 'Create New Category', exact: true }).click(); await app.field('Category Label').fill('Unsaved'); }
  199 |           if (number === 4) await app.action('Verify').click();
  200 |           if (number === 7) await app.panel.getByRole('button', { name: 'Create New Tile', exact: true }).click();
  201 |         }
  202 |         return;
  203 |       }
  204 |       let match: RegExpExecArray | null;
  205 |       if ((match = /^Admin A clicks button named "([^"]+)"/.exec(text))) { await app.footerButton(match[1]).click(); return; }
  206 |       if (text === 'the verification dialog finishes rendering') { await expect(app.dialog()).toBeVisible(); return; }
  207 |       if (text.includes('Owner') && text.endsWith('is disabled')) { await expect(app.field('Owner')).toBeDisabled(); return; }
  208 |       if ((match = /^textbox named "([^"]+)".* has value "([^"]*)"$/.exec(text))) { await expect(app.field(match[1])).toHaveValue(match[2]); return; }
  209 |       if ((match = /^button named "([^"]+)".* is visible$/.exec(text))) { await expect(app.footerButton(match[1])).toBeVisible(); return; }
  210 |       if ((match = /^Admin A opens combobox named "([^"]+)"/.exec(text))) { await (match[1] === 'Application Category' ? app.category : app.field(match[1], 'combobox')).click(); return; }
  211 |       if ((match = /^Admin A clicks option named "([^"]+)"/.exec(text))) { await page.getByRole('option', { name: match[1], exact: true, includeHidden: true }).click(); return; }
  212 |       if (text.includes('resolves the Other Category')) { await resolve(82); return; }
  213 |       if (text.includes('resolves the earlier Fixture') || text.includes('resolves the pending Fixture')) { await resolve(81); return; }
  214 |       if (text.includes('resolves record 102 audit')) { await resolve(102); return; }
  215 |       if (text.includes('resolves the earlier record 101')) { await resolve(101); return; }
  216 |       if (text.includes('category-clear target')) { await app.category.locator('..').getByRole('button', { name: 'Clear', exact: true }).click(); return; }
  217 |       if (text.includes('Application Category') && text.includes('has an empty value')) { await expect(app.category).toHaveValue(''); return; }
  218 |       if (text.includes('Application Category') && text.includes('has value "Other Category"')) { await expect(app.category).toHaveValue('Other Category'); return; }
```