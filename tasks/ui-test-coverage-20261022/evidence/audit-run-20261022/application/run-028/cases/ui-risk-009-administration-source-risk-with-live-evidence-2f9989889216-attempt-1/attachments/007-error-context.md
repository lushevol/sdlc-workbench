# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-ux.spec.ts >> UI-RISK-009 administration source risk with live evidence
- Location: e2e/audit-specs/admin-ux.spec.ts:170:3

# Error details

```
TimeoutError: locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for locator('[role="tabpanel"]:visible').getByTestId('MicroWebUI_base_simple_table').getByRole('grid', { includeHidden: true }).locator('[data-id="102"]').getByRole('menuitem', { name: 'Audit', exact: true })
    - locator resolved to <button tabindex="-1" type="button" role="menuitem" aria-label="Audit" data-testid="audit-102" class="MuiButtonBase-root MuiIconButton-root MuiIconButton-colorSecondary MuiIconButton-sizeSmall css-1491o59-MuiButtonBase-root-MuiIconButton-root">…</button>
  - attempting click action
    2 × waiting for element to be visible, enabled and stable
      - element is visible, enabled and stable
      - scrolling into view if needed
      - done scrolling
      - <div class="MicroWebUI_base_Loader-page">…</div> from <section data-testid="MicroWebUI_base_Loader_Page" class="MicroWebUI_base_Loader-root css-1dq995i">…</section> subtree intercepts pointer events
    - retrying click action
    - waiting 20ms
    2 × waiting for element to be visible, enabled and stable
      - element is visible, enabled and stable
      - scrolling into view if needed
      - done scrolling
      - <div class="MicroWebUI_base_Loader-page">…</div> from <section data-testid="MicroWebUI_base_Loader_Page" class="MicroWebUI_base_Loader-root css-1dq995i">…</section> subtree intercepts pointer events
    - retrying click action
      - waiting 100ms
    9 × waiting for element to be visible, enabled and stable
      - element is visible, enabled and stable
      - scrolling into view if needed
      - done scrolling
      - <div class="MicroWebUI_base_Loader-page">…</div> from <section data-testid="MicroWebUI_base_Loader_Page" class="MicroWebUI_base_Loader-root css-1dq995i">…</section> subtree intercepts pointer events
    - retrying click action
      - waiting 500ms

```

# Page snapshot

```yaml
- generic [ref=e1]:
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
          - generic [ref=e27]: 05:42 UTC
          - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
        - button "User Profiles" [ref=e34] [cursor=pointer]:
          - generic [ref=e35]: A
        - button "Share Feedback" [ref=e37] [cursor=pointer]
    - main [ref=e41]:
      - tablist "workspaces" [ref=e45]:
        - tab [selected] [ref=e47] [cursor=pointer]:
          - region "Category" [ref=e48]:
            - textbox "Workspace Name" [ref=e52]: Category
            - button "refresh" [ref=e53]
        - button "Add Workspace" [ref=e57] [cursor=pointer]
      - tabpanel [ref=e62]:
        - generic [ref=e65]:
          - button "Create New Category" [ref=e66] [cursor=pointer]
          - grid [ref=e68]:
            - button "Export" [ref=e70] [cursor=pointer]
            - generic [ref=e74]:
              - rowgroup [ref=e75]:
                - row [ref=e76]:
                  - columnheader "Actions" [ref=e77]
                  - columnheader "Category Label" [ref=e80] [cursor=pointer]
                  - columnheader "Owner" [ref=e83] [cursor=pointer]
                  - columnheader "Verified?" [ref=e86] [cursor=pointer]
                  - columnheader "Updated At" [ref=e89] [cursor=pointer]
                  - columnheader "Updated By" [ref=e92] [cursor=pointer]
                  - columnheader "Record Id" [ref=e95] [cursor=pointer]
                  - columnheader "Order No" [ref=e98] [cursor=pointer]
              - rowgroup [ref=e101]:
                - row [ref=e102]:
                  - cell [ref=e103]:
                    - menu [ref=e104]:
                      - menuitem "Edit" [ref=e105] [cursor=pointer]
                      - menuitem "Verify" [ref=e108] [cursor=pointer]
                      - menuitem "Deactivate" [disabled]
                      - menuitem "Audit" [active] [ref=e111] [cursor=pointer]
                  - cell "Fixture Category" [ref=e114]
                  - cell "TEST_OWNER" [ref=e115]
                  - cell [ref=e116]
                  - cell "Oct 22, 2026, 12:05:00 AM" [ref=e119]
                  - cell "UI-ADMIN-01" [ref=e121]
                  - cell "101" [ref=e122]
                  - cell "7" [ref=e123]
                - row [ref=e125]:
                  - cell [ref=e126]:
                    - menu [ref=e127]:
                      - menuitem "Edit" [ref=e128] [cursor=pointer]
                      - menuitem "Verify" [ref=e131] [cursor=pointer]
                      - menuitem "Deactivate" [disabled]
                      - menuitem "Audit" [ref=e134] [cursor=pointer]
                  - cell "Other Category" [ref=e137]
                  - cell "TEST_OWNER" [ref=e138]
                  - cell [ref=e139]
                  - cell "Oct 22, 2026, 12:05:00 AM" [ref=e142]
                  - cell "UI-ADMIN-01" [ref=e144]
                  - cell "102" [ref=e145]
                  - cell "7" [ref=e146]
            - generic [ref=e150]:
              - paragraph [ref=e151]: "Rows per page:"
              - generic [ref=e152]:
                - 'combobox "Rows per page: 20" [ref=e153] [cursor=pointer]': "20"
                - textbox [aria-hidden]: "20"
              - paragraph [ref=e154]: 1–2 of 2
              - generic [ref=e155]:
                - button "Go to previous page" [disabled]
                - button "Go to next page" [disabled]
  - tooltip "Open Audit" [ref=e156]
```

# Test source

```ts
  123 |       if (text.includes('Category Label') && text.endsWith('is focused')) { await expect(await app.reveal('label', '102')).toBeFocused(); return; }
  124 |       if (text.includes('Category Label') && text.endsWith('contains "Beta"')) { await expect(await app.reveal('label', '102')).toHaveText('Beta'); return; }
  125 |       if (text.includes('selects ascending sort')) { await (await app.reveal('label')).click(); return; }
  126 |       if (text.includes('selects descending sort')) { await (await app.reveal('label')).click(); await (await app.reveal('label')).click(); return; }
  127 |       if (text.includes('ordered Category grid label values')) {
  128 |         await expect(app.grid.locator('[data-id] [data-field="label"]')).toHaveText(number === 65 ? ['Alpha', 'Beta'] : ['Beta', 'Alpha']); return;
  129 |       }
  130 |       if (text.includes('selects an equals filter')) { await filter(); return; }
  131 |       if (text.includes('clears the filter')) {
  132 |         await menu('Filter'); await page.locator('.MuiDataGrid-filterForm').getByRole('button', { name: 'Delete', exact: true }).click(); await page.keyboard.press('Escape'); return;
  133 |       }
  134 |       if (text.includes('filtered Category grid data row count')) { await expect(app.grid.locator('[data-id]')).toHaveCount(0); return; }
  135 |       if ((match = /filtered pagination total equals (\d+)/.exec(text))) { await expect(app.grid.locator('.MuiTablePagination-displayedRows')).toHaveText(match[1] === '0' ? '0–0 of 0' : '1–2 of 2'); return; }
  136 |       if ((match = /Category Label.*"Record Id" equal to "(101|102)".* contains "(Alpha|Beta)"/.exec(text))) { await expect(await app.reveal('label', match[1])).toHaveText(match[2]); return; }
  137 |       if (text.includes('hidden visibility') || text.includes('visible state for "Owner"')) {
  138 |         await menu('Manage columns'); const checkbox = page.getByRole('checkbox', { name: 'Owner', exact: true }); await checkbox.setChecked(text.includes('visible state')); await page.keyboard.press('Escape'); return;
  139 |       }
  140 |       if (text.includes('column labelled "Owner"') && text.endsWith('is hidden')) { await expect(app.grid.locator('[role="columnheader"][data-field="ems2Role"]')).toHaveCount(0); return; }
  141 |       if (text.includes('column labelled "Owner"') && text.endsWith('is visible')) { await expect(await app.reveal('ems2Role')).toBeVisible(); return; }
  142 |       if (text.includes('cell for Owner')) { await expect(await app.reveal('ems2Role', '101')).toHaveText('TEST_OWNER'); return; }
  143 |       if (text.includes('selects CSV export')) {
  144 |         const wait = page.waitForEvent('download'); await app.grid.getByRole('button', { name: 'Export', exact: true }).click();
  145 |         await page.getByRole('menuitem', { name: 'Download as CSV', exact: true }).click(); const download = await wait;
  146 |         const stream = await download.createReadStream(); const chunks: Buffer[] = []; for await (const chunk of stream!) chunks.push(Buffer.from(chunk));
  147 |         csv = Buffer.concat(chunks).toString('utf8'); await audit.record('exported-csv', { filename: download.suggestedFilename(), csv }); return;
  148 |       }
  149 |       if (text.includes('artifact probe parses')) {
  150 |         // This fixture uses simple values. A CSV parser still preserves quoted commas and doubled quotes.
  151 |         rows = []; let row: string[] = [], value = '', quoted = false;
  152 |         for (let i = 0; i < csv.length; i++) { const c = csv[i]; if (c === '"') { if (quoted && csv[i + 1] === '"') { value += '"'; i++; } else quoted = !quoted; }
  153 |           else if (c === ',' && !quoted) { row.push(value); value = ''; } else if (c === '\n' && !quoted) { row.push(value.replace(/\r$/, '')); rows.push(row); row = []; value = ''; } else value += c; }
  154 |         if (row.length || value) { row.push(value); rows.push(row); } if (rows[0]?.[0]) rows[0][0] = rows[0][0].replace(/^\uFEFF/, '');
  155 |         await audit.record('parsed-export-csv', rows); return;
  156 |       }
  157 |       if (text.includes('exported Record Id') || text.includes('Each record appears exactly once')) {
  158 |         const idColumn = rows[0].indexOf('Record Id'), labelColumn = rows[0].indexOf('Category Label'); expect(idColumn).toBeGreaterThanOrEqual(0); expect(labelColumn).toBeGreaterThanOrEqual(0);
  159 |         const mapping = rows.slice(1).filter(row => row.some(Boolean)).map(row => [row[idColumn], row[labelColumn]]);
  160 |         expect(mapping).toEqual([['101', 'Alpha'], ['102', 'Beta']]); return;
  161 |       }
  162 |       throw new Error(`No administration UX binding for ${id} step ${step.number}: ${text}`);
  163 |     });
  164 |   });
  165 | }
  166 | 
  167 | type Pending = { route: Route; finish: () => void; key: number };
  168 | for (const number of [2, 3, 4, 5, 6, 7, 8, 9]) {
  169 |   const id = `UI-RISK-${String(number).padStart(3, '0')}`;
  170 |   test(`${id} administration source risk with live evidence`, async ({ page, audit }) => {
  171 |     const steps = await audit.defineCase(id);
  172 |     const kind: AdminKind = [5, 6, 7].includes(number) ? 'Tile' : 'Category';
  173 |     const app = new AdminApp(page, kind, id);
  174 |     const pending: Pending[] = [];
  175 |     const resolve = async (key: number) => {
  176 |       const entry = pending.find(item => item.key === key); expect(entry).toBeTruthy();
  177 |       const data = kind === 'Tile' ? [{ ...tileRecord(), title: key === 81 ? 'Tile A' : 'Tile B', applicationCategory: categoryRecord(key, key === 81 ? 'Fixture Category' : 'Other Category') }]
  178 |         : [{ ...categoryRecord(key), applicationCategoryAuditId: key === 101 ? 9001 : 9002 }];
  179 |       const outcome = await entry!.route.fulfill({ status: 200, json: { data } }).then(() => 'FULFILLED', () => 'REQUEST_ALREADY_ABORTED');
  180 |       entry!.finish(); await audit.record(`controlled-response-${key}`, { outcome, data });
  181 |     };
  182 |     for (const step of steps) await audit.step(step.number, async () => {
  183 |       const text = step.text;
  184 |       if (step.number === 1) { if (number === 9) app.rows.push(categoryRecord(102, 'Other Category')); await app.setup(); return; }
  185 |       if (step.number === 2) {
  186 |         if ([5, 6, 9].includes(number)) {
  187 |           await page.route(`**/api/auth/v1/fmo/admin/${kind === 'Tile' ? 'tile/data' : 'category/audit'}`, route => new Promise<void>(finish => {
  188 |             const body = route.request().postDataJSON(); pending.push({ route, finish, key: body.applicationCategory?.applicationCategoryId ?? body.applicationCategoryId ?? 0 });
  189 |           }));
  190 |           await expect(app.grid).toBeVisible();
  191 |           if (number === 6) await app.selectCategory();
  192 |         } else {
  193 |           if (number === 7) await page.route('**/api/auth/v1/fmo/admin/importmap/data', route => route.fulfill({ status: 200, json: { data: [71, 72].map(importMapId => ({ importMapId, keyName: '@fm/test', path: 'https://assets.example.test/v1.js' })) } }));
  194 |           if (number === 8) await page.route('**/api/auth/v1/fmo/admin/category/audit', route => route.fulfill({ status: 200, json: { data: [] } }));
  195 |           await app.open();
  196 |           if (number === 2) { await app.action('Edit').click(); await app.field('Category Label').fill('Unsaved'); }
  197 |           if (number === 3) { await app.panel.getByRole('button', { name: 'Create New Category', exact: true }).click(); await app.field('Category Label').fill('Unsaved'); }
  198 |           if (number === 4) await app.action('Verify').click();
  199 |           if (number === 7) await app.panel.getByRole('button', { name: 'Create New Tile', exact: true }).click();
  200 |         }
  201 |         return;
  202 |       }
  203 |       let match: RegExpExecArray | null;
  204 |       if ((match = /^Admin A clicks button named "([^"]+)"/.exec(text))) { await app.footerButton(match[1]).click(); return; }
  205 |       if (text === 'the verification dialog finishes rendering') { await expect(app.dialog()).toBeVisible(); return; }
  206 |       if (text.includes('Owner') && text.endsWith('is disabled')) { await expect(app.field('Owner')).toBeDisabled(); return; }
  207 |       if ((match = /^textbox named "([^"]+)".* has value "([^"]*)"$/.exec(text))) { await expect(app.field(match[1])).toHaveValue(match[2]); return; }
  208 |       if ((match = /^button named "([^"]+)".* is visible$/.exec(text))) { await expect(app.footerButton(match[1])).toBeVisible(); return; }
  209 |       if ((match = /^Admin A opens combobox named "([^"]+)"/.exec(text))) { await (match[1] === 'Application Category' ? app.category : app.field(match[1], 'combobox')).click(); return; }
  210 |       if ((match = /^Admin A clicks option named "([^"]+)"/.exec(text))) { await page.getByRole('option', { name: match[1], exact: true, includeHidden: true }).click(); return; }
  211 |       if (text.includes('resolves the Other Category')) { await resolve(82); return; }
  212 |       if (text.includes('resolves the earlier Fixture') || text.includes('resolves the pending Fixture')) { await resolve(81); return; }
  213 |       if (text.includes('resolves record 102 audit')) { await resolve(102); return; }
  214 |       if (text.includes('resolves the earlier record 101')) { await resolve(101); return; }
  215 |       if (text.includes('category-clear target')) { await app.category.locator('..').getByRole('button', { name: 'Clear', exact: true }).click(); return; }
  216 |       if (text.includes('Application Category') && text.includes('has an empty value')) { await expect(app.category).toHaveValue(''); return; }
  217 |       if (text.includes('Application Category') && text.includes('has value "Other Category"')) { await expect(app.category).toHaveValue('Other Category'); return; }
  218 |       if (text.includes('every displayed tile row')) { await app.reveal('title', '101'); await expect(app.grid.locator('[data-id] [data-field="title"]')).toHaveText(['Tile B']); return; }
  219 |       if (text.includes('data row count') && text.endsWith('equals 0')) { await expect(app.grid.locator('[data-id]')).toHaveCount(0); return; }
  220 |       if (text.includes('Create New Tile') && text.endsWith('is disabled')) { await expect(app.panel.getByRole('button', { name: 'Create New Tile', exact: true })).toBeDisabled(); return; }
  221 |       if (text.startsWith('exactly 2 options')) { await expect(page.getByRole('option', { includeHidden: true }).filter({ hasText: /^@fm\/test$/ })).toHaveCount(2); return; }
  222 |       if ((match = /option displays record ID "(\d+)"/.exec(text))) { await expect(page.getByRole('option', { includeHidden: true }).filter({ hasText: new RegExp(match[1]) })).toHaveCount(1); return; }
> 223 |       if ((match = /^Admin A clicks icon button named "Audit" inside row with Record Id "(\d+)"/.exec(text))) { await app.action('Audit', match[1]).click({ timeout: 5000 }); return; }
      |                                                                                                                                                     ^ TimeoutError: locator.click: Timeout 5000ms exceeded.
  224 |       if (text.includes('explicit empty-history status')) { await expect(app.panel.getByRole('status').filter({ hasText: /(?:no|empty).*history/i })).toBeVisible(); return; }
  225 |       if (text.includes('identifies source record "102"') || text.includes('each cell in the "Category ID"')) { await expect(app.auditDialog().locator('[data-id] [data-field="applicationCategoryId"]')).toHaveText(['102']); return; }
  226 |       throw new Error(`No source-risk UI binding for ${id} step ${step.number}: ${text}`);
  227 |     });
  228 |   });
  229 | }
  230 | 
```