# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-ux.spec.ts >> UI-RISK-007 administration source risk with live evidence
- Location: e2e/audit-specs/admin-ux.spec.ts:187:3

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  getByRole('option', { includeHidden: true }).filter({ hasText: /71/ })
Expected: 1
Received: 0
Timeout:  5000ms

Call log:
  - Expect "toHaveCount" getByRole('option', { includeHidden: true }).filter({ hasText: /71/ }) with timeout 5000ms
  - waiting for getByRole('option', { includeHidden: true }).filter({ hasText: /71/ })
    14 × locator resolved to 0 elements
       - unexpected value "0"

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
      - generic [ref=e27]: 06:03 UTC
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
                        - menuitem [disabled]
                        - menuitem [ref=e124] [cursor=pointer]
                        - menuitem [ref=e127] [cursor=pointer]
                    - cell [ref=e130]: Fixture Tile
                    - cell [ref=e131]: Demo
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
                  - generic [ref=e152]: "new ID: 1792648983179"
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
                - generic [ref=e173]:
                  - generic [ref=e174]: Description
                  - textbox [ref=e176]:
                    - /placeholder: Type here
                - generic [ref=e178]:
                  - generic [ref=e179]: Image URL for Dark Theme
                  - generic [ref=e180]:
                    - combobox [ref=e181]
                    - button [ref=e183] [cursor=pointer]
                - generic [ref=e187]:
                  - generic [ref=e188]: Image URL for Light Theme
                  - generic [ref=e189]:
                    - combobox [ref=e190]
                    - button [ref=e192] [cursor=pointer]
                - generic [ref=e195]:
                  - generic [ref=e196]:
                    - generic [ref=e197]: Container
                    - generic [ref=e198]:
                      - combobox [expanded] [active] [ref=e199]
                      - button [ref=e201] [cursor=pointer]
                  - listbox "Container" [ref=e204]:
                    - option "@fm/test" [ref=e205] [cursor=pointer]
                    - option "@fm/test" [ref=e206] [cursor=pointer]
                - generic [ref=e207]:
                  - generic [ref=e208]: Module Path
                  - textbox [ref=e210]:
                    - /placeholder: Type here
                - generic [ref=e211]:
                  - generic [ref=e212]: Tile Path
                  - textbox [ref=e214]:
                    - /placeholder: Type here
                - generic [ref=e215]:
                  - generic [ref=e216]: Role Subject
                  - textbox [ref=e218]:
                    - /placeholder: Type here
                - generic [ref=e219]:
                  - generic [ref=e220]: Role Entities
                  - textbox [ref=e222]:
                    - /placeholder: Type here
                - generic [ref=e223]:
                  - generic: Is Template?
                  - generic [ref=e224]:
                    - combobox [ref=e225] [cursor=pointer]
                    - textbox [aria-hidden]
                - generic [ref=e226]:
                  - generic [ref=e227]: Email Support
                  - textbox [ref=e229]:
                    - /placeholder: Type here
                - generic [ref=e230]:
                  - generic [ref=e231]: Owner
                  - textbox [disabled] [ref=e233]:
                    - /placeholder: Type here
                    - text: TEST_OWNER
                - generic [ref=e234]:
                  - generic [ref=e235]: Verified?
                  - textbox [disabled] [ref=e237]:
                    - /placeholder: Type here
                    - text: "false"
                - generic [ref=e238]:
                  - generic [ref=e239]: Created At
                  - textbox [disabled] [ref=e241]:
                    - /placeholder: Type here
                    - text: 2026-10-22T06:03:03.179Z
                - generic [ref=e242]:
                  - generic [ref=e243]: Created By
                  - textbox [disabled] [ref=e245]:
                    - /placeholder: Type here
                    - text: UI-ADMIN-01
                - generic [ref=e246]:
                  - generic [ref=e247]: Updated At
                  - textbox [disabled] [ref=e249]:
                    - /placeholder: Type here
                    - text: 2026-10-22T06:03:03.179Z
                - generic [ref=e250]:
                  - generic [ref=e251]: Updated By
                  - textbox [disabled] [ref=e253]:
                    - /placeholder: Type here
                    - text: UI-ADMIN-01
                - generic [ref=e254]:
                  - generic [ref=e255]: Record Id
                  - textbox [disabled] [ref=e257]:
                    - /placeholder: <<will be auto generated>>
                - generic [ref=e258]:
                  - generic [ref=e259]: Aplication Category Record Id
                  - textbox [disabled] [ref=e261]:
                    - /placeholder: <<will be auto generated>>
                    - text: "81"
                - generic [ref=e262]:
                  - generic [ref=e263]: Container Record Id
                  - textbox [disabled] [ref=e265]:
                    - /placeholder: <<will be auto generated>>
                - generic [ref=e266]:
                  - generic [ref=e267]: Order No
                  - spinbutton [ref=e269]
                - generic [ref=e270]:
                  - generic [ref=e271]: Filter Rule
                  - textbox [ref=e273]:
                    - /placeholder: Type here
                - generic [ref=e274]:
                  - generic [ref=e275]: Entry Name
                  - textbox [ref=e277]:
                    - /placeholder: Type here
              - generic [ref=e278]:
                - button [ref=e279] [cursor=pointer]: Create
                - button [ref=e280] [cursor=pointer]: Reset
                - button [ref=e281] [cursor=pointer]: Close
              - button [ref=e282]
```

# Test source

```ts
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
  235 |       if (text.includes('every displayed tile row')) { await app.reveal('title', '101'); await expect(app.grid.locator('[data-id] [data-field="title"]')).toHaveText(['Tile B']); return; }
  236 |       if (text.includes('data row count') && text.endsWith('equals 0')) { await expect(app.grid.locator('[data-id]')).toHaveCount(0); return; }
  237 |       if (text.includes('Create New Tile') && text.endsWith('is disabled')) { await expect(app.panel.getByRole('button', { name: 'Create New Tile', exact: true })).toBeDisabled(); return; }
  238 |       if (text.startsWith('exactly 2 options')) { await expect(page.getByRole('option', { includeHidden: true }).filter({ hasText: /^@fm\/test$/ })).toHaveCount(2); return; }
> 239 |       if ((match = /option displays record ID "(\d+)"/.exec(text))) { await expect(page.getByRole('option', { includeHidden: true }).filter({ hasText: new RegExp(match[1]) })).toHaveCount(1); return; }
      |                                                                                                                                                                                 ^ Error: expect(locator).toHaveCount(expected) failed
  240 |       if ((match = /^Admin A clicks icon button named "Audit" inside row with Record Id "(\d+)"/.exec(text))) { await app.action('Audit', match[1]).click({ timeout: 5000 }); return; }
  241 |       if (text.includes('explicit empty-history status')) { await expect(app.panel.getByRole('status').filter({ hasText: /(?:no|empty).*history/i })).toBeVisible(); return; }
  242 |       if (text.includes('identifies source record "102"') || text.includes('each cell in the "Category ID"')) { await expect(app.auditDialog().locator('[data-id] [data-field="applicationCategoryId"]')).toHaveText(['102']); return; }
  243 |       throw new Error(`No source-risk UI binding for ${id} step ${step.number}: ${text}`);
  244 |     });
  245 |   });
  246 | }
  247 | 
```