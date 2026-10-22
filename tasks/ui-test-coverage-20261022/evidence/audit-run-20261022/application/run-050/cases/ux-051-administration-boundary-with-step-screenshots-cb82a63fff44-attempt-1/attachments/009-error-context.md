# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-ux.spec.ts >> UX-051 administration boundary with step screenshots
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
        - generic [ref=e27]: 06:01 UTC
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
  34  |       await page.keyboard.press('Escape');
  35  |     };
  36  |     const positions = () => app.dialog().locator('label, .MuiDialogActions-root button').evaluateAll(nodes => nodes.map(node => {
  37  |       const box = node.getBoundingClientRect(); return { label: node.textContent ?? '', x: box.x, y: box.y };
  38  |     }));
  39  |     for (const step of steps) await audit.step(step.number, async () => {
  40  |       const text = step.text;
  41  |       if (step.number === 1) {
  42  |         if (number === 31) await page.setViewportSize({ width: 1024, height: 600 });
  43  |         page.on('dialog', async dialog => {
  44  |           if (dialog.type() === 'beforeunload') { await dialog.accept(); return; }
  45  |           alerts.push(dialog.type()); await dialog.dismiss();
  46  |         });
  47  |         if ([17, 21, 65, 66, 67, 68, 70].includes(number)) app.rows = [categoryRecord(101, 'Alpha'), categoryRecord(102, 'Beta')];
  48  |         if (number === 21) app.rows[0].active = true;
  49  |         if (number >= 51 && number <= 58) app.rows[0] = { ...tileRecord(), title: 'Old', subtitle: 'Before' };
  50  |         if (number === 56) app.rows.push({ ...tileRecord(), applicationTileId: 102, title: 'Second Tile' });
  51  |         if (number === 47) app.rows[0].title = 'ABC\u202eDEF';
  52  |         await app.setup();
  53  |         if (number === 16) { await page.route('**/api/auth/v1/fmo/admin/category/data', route => route.fulfill({ status: 200, json: { data: [categoryRecord(81, 'Cashflow')] } })); await page.reload({ waitUntil: 'domcontentloaded' }); }
  54  |         if (number === 18) await page.route('**/api/auth/v1/fmo/admin/tile/update', route => route.fulfill({ status: 500, json: { message: 'Save failed' } }));
  55  |         if (number === 16) { await expect(app.grid).toBeVisible(); await app.selectCategory('Cashflow'); }
  56  |         else await app.open();
  57  |         if ([14, 16, 18, 31, 38, 45].includes(number) || number >= 51 && number <= 58) await app.action('Edit').click();
  58  |         if (number === 15) await app.action('Verify').click();
  59  |         if (number === 17) await (await app.reveal('label', '101')).focus();
  60  |         if (number === 68) await filter();
  61  |         if (clockCase) { const now = new Date(); await page.clock.install({ time: now }); await page.clock.pauseAt(new Date(now.getTime() + 60_000)); }
  62  |         if (number === 47) { await app.action('Edit').click(); await field('Tile Name').fill('ABCDEF'); baseline = await positions(); await field('Tile Name').fill('ABC\u202eDEF'); await app.footerButton('Close').click(); }
  63  |         return;
  64  |       }
  65  |       let match: RegExpExecArray | null;
  66  |       if (text.includes('accessibility probe captures')) {
  67  |         disabledCount = await app.dialog().locator('input:disabled,textarea:disabled').count().catch(() => 0);
  68  |         await audit.record('accessibility-snapshot', { tree: await app.panel.ariaSnapshot(), disabledCount }); return;
  69  |       }
  70  |       if ((match = /textbox labelled "([^"]+)".* accessible name (?:equal to|retains accessible name) "([^"]+)"/.exec(text))) { await expect(field(match[1])).toHaveAccessibleName(match[2]); return; }
  71  |       if (text.includes('retains accessible name "Description"')) { await expect(field('Description')).toHaveAccessibleName('Description'); return; }
  72  |       if (text.includes('For each disabled input')) {
  73  |         expect(disabledCount).toBeGreaterThan(0);
  74  |         const snapshot = await app.dialog().ariaSnapshot(); await audit.record('verification-accessibility-tree', snapshot);
  75  |         expect((snapshot.match(/\[disabled\]/g) ?? []).length).toBeGreaterThanOrEqual(disabledCount); return;
  76  |       }
  77  |       if ((match = /ADMIN-A (?:types|types exactly) "(.*)"(?: as the replacement value| through IME composition)? (?:into|in) the (textbox|combobox) labelled "([^"]+)"/.exec(text))) {
  78  |         const target = app.field(match[3], match[2]);
  79  |         if (text.includes('through IME composition')) {
  80  |           await target.dispatchEvent('compositionstart', { data: '' });
  81  |           await target.fill(match[1]); await target.dispatchEvent('compositionupdate', { data: match[1] });
  82  |           await audit.record('controlled-ime-events', { events: ['compositionstart', 'input', 'compositionupdate'], value: match[1], limit: 'Programmatic composition fixture; native operating-system IME is not exercised.' });
  83  |         } else await target.fill(match[1]);
  84  |         return;
  85  |       }
  86  |       if ((match = /ADMIN-A presses "([^"]+)" on the (?:textbox|combobox|cell) labelled "([^"]+)"/.exec(text))) {
  87  |         if (match[2] === 'Category Label') await (await app.reveal('label', '101')).press(match[1]);
  88  |         else await app.field(match[2], match[2] === 'Aplication Category' ? 'combobox' : 'textbox').press(match[1]); return;
  89  |       }
  90  |       if (text.includes('option labelled "Cashflow"') && text.includes('highlighted')) {
  91  |         const combo = app.field('Aplication Category', 'combobox');
  92  |         const selected = await combo.getAttribute('aria-activedescendant'); expect(selected).toBeTruthy();
  93  |         await expect(page.locator(`[id="${selected}"]`)).toHaveText('Cashflow'); return;
  94  |       }
  95  |       if ((match = /(?:textbox|combobox) labelled "([^"]+)".* has value equal to "(.*)"$/.exec(text))) {
  96  |         await expect(app.field(match[1], match[1] === 'Aplication Category' ? 'combobox' : 'textbox')).toHaveValue(match[2]); return;
  97  |       }
  98  |       if (text.includes('exact fixture Unicode sequence')) { await expect(field('Tile Name')).toHaveValue('ABC\u202eDEF'); return; }
  99  |       if (text.includes('visual reading order')) { expect(await positions()).toEqual(baseline); return; }
  100 |       if (text.includes('retains visible label "Update"')) { await expect(app.footerButton('Update')).toHaveText('Update'); return; }
  101 |       if ((match = /ADMIN-A clicks the button labelled "(Update|Reset|Close|Edit)"/.exec(text))) {
  102 |         if (match[1] === 'Edit') {
  103 |           const idMatch = /"Record Id" equal to "(\d+)"/.exec(text); await app.action('Edit', idMatch?.[1] ?? '101').click();
  104 |         } else { await app.footerButton(match[1]).click(); if (match[1] === 'Update') await audit.record('ui-origin-admin-requests', app.requests); }
  105 |         return;
  106 |       }
  107 |       if (text.includes('alert inside the snackbar')) {
  108 |         const snackbar = page.getByTestId('MicroWebUI_base_snackbar');
  109 |         await expect(snackbar.locator('.MuiSnackbarContent-root[role="alert"]')).toHaveText('Save failed');
  110 |         const tree = await snackbar.ariaSnapshot(); await audit.record('save-error-accessibility-tree', tree);
  111 |         expect(tree).toContain('alert'); expect(tree).toContain('Save failed'); return;
  112 |       }
  113 |       if (text.includes('exposes a text or accessible state distinct')) {
  114 |         const first = await app.reveal('active', '101'), second = await app.reveal('active', '102');
  115 |         const value = (cell: typeof first) => cell.evaluate(node => ({ text: node.textContent,
  116 |           labels: Array.from(node.querySelectorAll('[aria-label],title')).map(item => item.getAttribute('aria-label') ?? item.textContent) }));
  117 |         const values = [await value(first), await value(second)]; await audit.record('status-accessibility-values', values);
  118 |         expect(values[0]).not.toEqual(values[1]); return;
  119 |       }
  120 |       if (text.includes('scrolls to the footer')) { await app.footerButton('Close').scrollIntoViewIfNeeded(); return; }
  121 |       if ((match = /button labelled "(Update|Reset|Close)".* is visible and enabled$/.exec(text))) {
  122 |         await expect(app.footerButton(match[1])).toBeVisible(); await expect(app.footerButton(match[1])).toBeEnabled(); return;
  123 |       }
  124 |       if ((match = /controlled event loop advances (\d+) milliseconds/.exec(text))) { await page.clock.runFor(Number(match[1])); return; }
  125 |       if (text.includes('controlled event loop') && text.includes('completes')) { await page.clock.runFor(1000); return; }
  126 |       if (text.includes('save fixture acknowledges') || text.includes('browser fixture reloads')) {
  127 |         await audit.record('persisted-received-payload', { rows: app.rows, requests: app.requests });
  128 |         if (clockCase) await page.clock.resume();
  129 |         await page.reload({ waitUntil: 'domcontentloaded' }); await app.portal.expectVisible(); await app.open(); return;
  130 |       }
  131 |       if (text.includes('captured update payload has title')) {
  132 |         const expected = /"(New|ABC)"/.exec(text)![1];
  133 |         const request = app.requests.filter(request => request.endpoint === 'tile/update').at(-1);
> 134 |         await audit.record('captured-update-payload', request); expect(request?.body.title).toBe(expected); return;
      |                                                                                             ^ Error: expect(received).toBe(expected) // Object.is equality
  135 |       }
  136 |       if ((match = /Tile grid row.* contains "Tile Name" equal to "([^"]+)"/.exec(text))) { await expect(await app.reveal('title', '101')).toHaveText(match[1]); return; }
  137 |       if (text.includes('contains literal text')) { await expect(await app.reveal('label', '101')).toHaveText('<script>alert(1)</script>'); return; }
  138 |       if (text.includes('zero alert events')) { await audit.record('script-dialog-events', alerts); expect(alerts).toEqual([]); return; }
  139 |       if (text.includes('compositionend before blur')) { await field('Tile Name').dispatchEvent('compositionend', { data: '東京' }); return; }
  140 |       if (text.includes('Category Label') && text.endsWith('is focused')) { await expect(await app.reveal('label', '102')).toBeFocused(); return; }
  141 |       if (text.includes('Category Label') && text.endsWith('contains "Beta"')) { await expect(await app.reveal('label', '102')).toHaveText('Beta'); return; }
  142 |       if (text.includes('selects ascending sort')) { await (await app.reveal('label')).click(); return; }
  143 |       if (text.includes('selects descending sort')) { await (await app.reveal('label')).click(); await (await app.reveal('label')).click(); return; }
  144 |       if (text.includes('ordered Category grid label values')) {
  145 |         await expect(app.grid.locator('[data-id] [data-field="label"]')).toHaveText(number === 65 ? ['Alpha', 'Beta'] : ['Beta', 'Alpha']); return;
  146 |       }
  147 |       if (text.includes('selects an equals filter')) { await filter(); return; }
  148 |       if (text.includes('clears the filter')) {
  149 |         await menu('Filter'); await page.locator('.MuiDataGrid-filterForm').getByRole('button', { name: 'Delete', exact: true }).click(); await page.keyboard.press('Escape'); return;
  150 |       }
  151 |       if (text.includes('filtered Category grid data row count')) { await expect(app.grid.locator('[data-id]')).toHaveCount(0); return; }
  152 |       if ((match = /filtered pagination total equals (\d+)/.exec(text))) { await expect(app.grid.locator('.MuiTablePagination-displayedRows')).toHaveText(match[1] === '0' ? '0–0 of 0' : '1–2 of 2'); return; }
  153 |       if ((match = /Category Label.*"Record Id" equal to "(101|102)".* contains "(Alpha|Beta)"/.exec(text))) { await expect(await app.reveal('label', match[1])).toHaveText(match[2]); return; }
  154 |       if (text.includes('hidden visibility') || text.includes('visible state for "Owner"')) {
  155 |         await menu('Manage columns'); const checkbox = page.getByRole('checkbox', { name: 'Owner', exact: true }); await checkbox.setChecked(text.includes('visible state')); await page.keyboard.press('Escape'); return;
  156 |       }
  157 |       if (text.includes('column labelled "Owner"') && text.endsWith('is hidden')) { await expect(app.grid.locator('[role="columnheader"][data-field="ems2Role"]')).toHaveCount(0); return; }
  158 |       if (text.includes('column labelled "Owner"') && text.endsWith('is visible')) { await expect(await app.reveal('ems2Role')).toBeVisible(); return; }
  159 |       if (text.includes('cell for Owner')) { await expect(await app.reveal('ems2Role', '101')).toHaveText('TEST_OWNER'); return; }
  160 |       if (text.includes('selects CSV export')) {
  161 |         const wait = page.waitForEvent('download'); await app.grid.getByRole('button', { name: 'Export', exact: true }).click();
  162 |         await page.getByRole('menuitem', { name: 'Download as CSV', exact: true }).click(); const download = await wait;
  163 |         const stream = await download.createReadStream(); const chunks: Buffer[] = []; for await (const chunk of stream!) chunks.push(Buffer.from(chunk));
  164 |         csv = Buffer.concat(chunks).toString('utf8'); await audit.record('exported-csv', { filename: download.suggestedFilename(), csv }); return;
  165 |       }
  166 |       if (text.includes('artifact probe parses')) {
  167 |         // This fixture uses simple values. A CSV parser still preserves quoted commas and doubled quotes.
  168 |         rows = []; let row: string[] = [], value = '', quoted = false;
  169 |         for (let i = 0; i < csv.length; i++) { const c = csv[i]; if (c === '"') { if (quoted && csv[i + 1] === '"') { value += '"'; i++; } else quoted = !quoted; }
  170 |           else if (c === ',' && !quoted) { row.push(value); value = ''; } else if (c === '\n' && !quoted) { row.push(value.replace(/\r$/, '')); rows.push(row); row = []; value = ''; } else value += c; }
  171 |         if (row.length || value) { row.push(value); rows.push(row); } if (rows[0]?.[0]) rows[0][0] = rows[0][0].replace(/^\uFEFF/, '');
  172 |         await audit.record('parsed-export-csv', rows); return;
  173 |       }
  174 |       if (text.includes('exported Record Id') || text.includes('Each record appears exactly once')) {
  175 |         const idColumn = rows[0].indexOf('Record Id'), labelColumn = rows[0].indexOf('Category Label'); expect(idColumn).toBeGreaterThanOrEqual(0); expect(labelColumn).toBeGreaterThanOrEqual(0);
  176 |         const mapping = rows.slice(1).filter(row => row.some(Boolean)).map(row => [row[idColumn], row[labelColumn]]);
  177 |         expect(mapping).toEqual([['101', 'Alpha'], ['102', 'Beta']]); return;
  178 |       }
  179 |       throw new Error(`No administration UX binding for ${id} step ${step.number}: ${text}`);
  180 |     });
  181 |   });
  182 | }
  183 | 
  184 | type Pending = { route: Route; finish: () => void; key: number };
  185 | for (const number of [2, 3, 4, 5, 6, 7, 8, 9]) {
  186 |   const id = `UI-RISK-${String(number).padStart(3, '0')}`;
  187 |   test(`${id} administration source risk with live evidence`, async ({ page, audit }) => {
  188 |     const steps = await audit.defineCase(id);
  189 |     const kind: AdminKind = [5, 6, 7].includes(number) ? 'Tile' : 'Category';
  190 |     const app = new AdminApp(page, kind, id);
  191 |     const pending: Pending[] = [];
  192 |     const resolve = async (key: number) => {
  193 |       const entry = pending.find(item => item.key === key); expect(entry).toBeTruthy();
  194 |       const data = kind === 'Tile' ? [{ ...tileRecord(), title: key === 81 ? 'Tile A' : 'Tile B', applicationCategory: categoryRecord(key, key === 81 ? 'Fixture Category' : 'Other Category') }]
  195 |         : [{ ...categoryRecord(key), applicationCategoryAuditId: key === 101 ? 9001 : 9002 }];
  196 |       const outcome = await entry!.route.fulfill({ status: 200, json: { data } }).then(() => 'FULFILLED', () => 'REQUEST_ALREADY_ABORTED');
  197 |       entry!.finish(); await audit.record(`controlled-response-${key}`, { outcome, data });
  198 |     };
  199 |     for (const step of steps) await audit.step(step.number, async () => {
  200 |       const text = step.text;
  201 |       if (step.number === 1) { if (number === 9) app.rows.push(categoryRecord(102, 'Other Category')); await app.setup(); return; }
  202 |       if (step.number === 2) {
  203 |         if ([5, 6, 9].includes(number)) {
  204 |           await page.route(`**/api/auth/v1/fmo/admin/${kind === 'Tile' ? 'tile/data' : 'category/audit'}`, route => new Promise<void>(finish => {
  205 |             const body = route.request().postDataJSON(); pending.push({ route, finish, key: body.applicationCategory?.applicationCategoryId ?? body.applicationCategoryId ?? 0 });
  206 |           }));
  207 |           await expect(app.grid).toBeVisible();
  208 |           if (number === 6) await app.selectCategory();
  209 |         } else {
  210 |           if (number === 7) await page.route('**/api/auth/v1/fmo/admin/importmap/data', route => route.fulfill({ status: 200, json: { data: [71, 72].map(importMapId => ({ importMapId, keyName: '@fm/test', path: 'https://assets.example.test/v1.js' })) } }));
  211 |           if (number === 8) await page.route('**/api/auth/v1/fmo/admin/category/audit', route => route.fulfill({ status: 200, json: { data: [] } }));
  212 |           await app.open();
  213 |           if (number === 2) { await app.action('Edit').click(); await app.field('Category Label').fill('Unsaved'); }
  214 |           if (number === 3) { await app.panel.getByRole('button', { name: 'Create New Category', exact: true }).click(); await app.field('Category Label').fill('Unsaved'); }
  215 |           if (number === 4) await app.action('Verify').click();
  216 |           if (number === 7) await app.panel.getByRole('button', { name: 'Create New Tile', exact: true }).click();
  217 |         }
  218 |         return;
  219 |       }
  220 |       let match: RegExpExecArray | null;
  221 |       if ((match = /^Admin A clicks button named "([^"]+)"/.exec(text))) { await app.footerButton(match[1]).click(); return; }
  222 |       if (text === 'the verification dialog finishes rendering') { await expect(app.dialog()).toBeVisible(); return; }
  223 |       if (text.includes('Owner') && text.endsWith('is disabled')) { await expect(app.field('Owner')).toBeDisabled(); return; }
  224 |       if ((match = /^textbox named "([^"]+)".* has value "([^"]*)"$/.exec(text))) { await expect(app.field(match[1])).toHaveValue(match[2]); return; }
  225 |       if ((match = /^button named "([^"]+)".* is visible$/.exec(text))) { await expect(app.footerButton(match[1])).toBeVisible(); return; }
  226 |       if ((match = /^Admin A opens combobox named "([^"]+)"/.exec(text))) { await (match[1] === 'Application Category' ? app.category : app.field(match[1], 'combobox')).click(); return; }
  227 |       if ((match = /^Admin A clicks option named "([^"]+)"/.exec(text))) { await page.getByRole('option', { name: match[1], exact: true, includeHidden: true }).click(); return; }
  228 |       if (text.includes('resolves the Other Category')) { await resolve(82); return; }
  229 |       if (text.includes('resolves the earlier Fixture') || text.includes('resolves the pending Fixture')) { await resolve(81); return; }
  230 |       if (text.includes('resolves record 102 audit')) { await resolve(102); return; }
  231 |       if (text.includes('resolves the earlier record 101')) { await resolve(101); return; }
  232 |       if (text.includes('category-clear target')) { await app.category.locator('..').getByRole('button', { name: 'Clear', exact: true }).click(); return; }
  233 |       if (text.includes('Application Category') && text.includes('has an empty value')) { await expect(app.category).toHaveValue(''); return; }
  234 |       if (text.includes('Application Category') && text.includes('has value "Other Category"')) { await expect(app.category).toHaveValue('Other Category'); return; }
```