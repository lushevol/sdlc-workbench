# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-ux.spec.ts >> UI-RISK-003 administration source risk with live evidence
- Location: e2e/audit-specs/admin-ux.spec.ts:171:3

# Error details

```
Error: expect(locator).toHaveValue(expected) failed

Locator:  locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText(/^(?:new|edit|verify|deactivate) ID:/) }).getByRole('textbox', { name: 'Category Label', exact: true, includeHidden: true })
Expected: ""
Received: "Unsaved"
Timeout:  5000ms

Call log:
  - Expect "toHaveValue" locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText(/^(?:new|edit|verify|deactivate) ID:/) }).getByRole('textbox', { name: 'Category Label', exact: true, includeHidden: true }) with timeout 5000ms
  - waiting for locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText(/^(?:new|edit|verify|deactivate) ID:/) }).getByRole('textbox', { name: 'Category Label', exact: true, includeHidden: true })
    14 × locator resolved to <input id=":r23:" type="text" value="Unsaved" aria-invalid="false" placeholder="Type here" class="MuiInputBase-input MuiOutlinedInput-input MuiInputBase-inputSizeSmall css-1yzpw69-MuiInputBase-input-MuiOutlinedInput-input"/>
       - unexpected value "Unsaved"

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
      - generic [ref=e27]: 05:37 UTC
      - checkbox [checked] [ref=e30] [cursor=pointer]
    - button [ref=e34] [cursor=pointer]:
      - generic [ref=e35]: A
    - button [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region [ref=e48]:
          - textbox [ref=e52]: Category
          - button [ref=e53]
      - button [ref=e57] [cursor=pointer]
    - tabpanel [ref=e62]:
      - generic [ref=e65]:
        - button [ref=e66] [cursor=pointer]: Create New Category
        - generic [ref=e67]:
          - grid [ref=e68]:
            - button [ref=e70] [cursor=pointer]: Export
            - generic [ref=e74]:
              - rowgroup [ref=e75]:
                - row [ref=e76]:
                  - columnheader [ref=e77]:
                    - generic [ref=e78]: Actions
                  - columnheader [ref=e80] [cursor=pointer]:
                    - generic [ref=e81]: Category Label
                  - columnheader [ref=e83] [cursor=pointer]:
                    - generic [ref=e84]: Owner
                  - columnheader [ref=e86] [cursor=pointer]:
                    - generic [ref=e87]: Verified?
                  - columnheader [ref=e89] [cursor=pointer]:
                    - generic [ref=e90]: Updated At
                  - columnheader [ref=e92] [cursor=pointer]:
                    - generic [ref=e93]: Updated By
                  - columnheader [ref=e95] [cursor=pointer]:
                    - generic [ref=e96]: Record Id
                  - columnheader [ref=e98] [cursor=pointer]:
                    - generic [ref=e99]: Order No
              - rowgroup [ref=e101]:
                - row [ref=e102]:
                  - cell [ref=e103]:
                    - menu [ref=e104]:
                      - menuitem [ref=e105] [cursor=pointer]
                      - menuitem [ref=e108] [cursor=pointer]
                      - menuitem [disabled]
                      - menuitem [ref=e111] [cursor=pointer]
                  - cell [ref=e114]: Fixture Category
                  - cell [ref=e115]: TEST_OWNER
                  - cell [ref=e116]
                  - cell [ref=e119]:
                    - generic [ref=e120]: Oct 22, 2026, 12:05:00 AM
                  - cell [ref=e121]: UI-ADMIN-01
                  - cell [ref=e122]: "101"
                  - cell [ref=e123]: "7"
            - generic [ref=e127]:
              - paragraph [ref=e128]: "Rows per page:"
              - generic [ref=e129]:
                - combobox [ref=e130] [cursor=pointer]: "20"
                - textbox [aria-hidden]: "20"
              - paragraph [ref=e131]: 1–1 of 1
              - generic [ref=e132]:
                - button [disabled]
                - button [disabled]
          - dialog [ref=e135]:
            - heading [level=2] [ref=e136]:
              - generic [ref=e137]:
                - generic [ref=e138]: "new ID: 1792647462945"
                - generic [ref=e139]:
                  - button [ref=e140] [cursor=pointer]: Maximize
                  - button [disabled]:
                    - generic: Close
            - generic [ref=e145]:
              - generic [ref=e146]:
                - generic [ref=e147]: Category Label
                - textbox [ref=e149]:
                  - /placeholder: Type here
                  - text: Unsaved
              - generic [ref=e150]:
                - generic [ref=e151]: Owner
                - textbox [disabled] [ref=e153]:
                  - /placeholder: Type here
                  - text: TEST_OWNER
              - generic [ref=e154]:
                - generic [ref=e155]: Verified?
                - textbox [disabled] [ref=e157]:
                  - /placeholder: Type here
                  - text: "false"
              - generic [ref=e158]:
                - generic [ref=e159]: Created At
                - textbox [disabled] [ref=e161]:
                  - /placeholder: Type here
                  - text: 2026-10-22T05:37:42.945Z
              - generic [ref=e162]:
                - generic [ref=e163]: Created By
                - textbox [disabled] [ref=e165]:
                  - /placeholder: Type here
                  - text: UI-ADMIN-01
              - generic [ref=e166]:
                - generic [ref=e167]: Updated At
                - textbox [disabled] [ref=e169]:
                  - /placeholder: Type here
                  - text: 2026-10-22T05:37:42.945Z
              - generic [ref=e170]:
                - generic [ref=e171]: Updated By
                - textbox [disabled] [ref=e173]:
                  - /placeholder: Type here
                  - text: UI-ADMIN-01
              - generic [ref=e174]:
                - generic [ref=e175]: Record Id
                - textbox [disabled] [ref=e177]:
                  - /placeholder: <<will be auto generated>>
              - generic [ref=e178]:
                - generic [ref=e179]: Order No
                - spinbutton [ref=e181]
            - generic [ref=e182]:
              - button [ref=e183] [cursor=pointer]: Create
              - button [active] [ref=e184] [cursor=pointer]: Reset
              - button [ref=e185] [cursor=pointer]: Close
            - button [ref=e186]
```

# Test source

```ts
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
> 208 |       if ((match = /^textbox named "([^"]+)".* has value "([^"]*)"$/.exec(text))) { await expect(app.field(match[1])).toHaveValue(match[2]); return; }
      |                                                                                                                       ^ Error: expect(locator).toHaveValue(expected) failed
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
  219 |       if (text.includes('every displayed tile row')) { await app.reveal('title', '101'); await expect(app.grid.locator('[data-id] [data-field="title"]')).toHaveText(['Tile B']); return; }
  220 |       if (text.includes('data row count') && text.endsWith('equals 0')) { await expect(app.grid.locator('[data-id]')).toHaveCount(0); return; }
  221 |       if (text.includes('Create New Tile') && text.endsWith('is disabled')) { await expect(app.panel.getByRole('button', { name: 'Create New Tile', exact: true })).toBeDisabled(); return; }
  222 |       if (text.startsWith('exactly 2 options')) { await expect(page.getByRole('option', { includeHidden: true }).filter({ hasText: /^@fm\/test$/ })).toHaveCount(2); return; }
  223 |       if ((match = /option displays record ID "(\d+)"/.exec(text))) { await expect(page.getByRole('option', { includeHidden: true }).filter({ hasText: new RegExp(match[1]) })).toHaveCount(1); return; }
  224 |       if ((match = /^Admin A clicks icon button named "Audit" inside row with Record Id "(\d+)"/.exec(text))) { await app.action('Audit', match[1]).click(); return; }
  225 |       if (text.includes('explicit empty-history status')) { await expect(app.panel.getByRole('status').filter({ hasText: /(?:no|empty).*history/i })).toBeVisible(); return; }
  226 |       if (text.includes('identifies source record "102"') || text.includes('each cell in the "Category ID"')) { await expect(app.auditDialog().locator('[data-id] [data-field="applicationCategoryId"]')).toHaveText(['102']); return; }
  227 |       throw new Error(`No source-risk UI binding for ${id} step ${step.number}: ${text}`);
  228 |     });
  229 |   });
  230 | }
  231 | 
```