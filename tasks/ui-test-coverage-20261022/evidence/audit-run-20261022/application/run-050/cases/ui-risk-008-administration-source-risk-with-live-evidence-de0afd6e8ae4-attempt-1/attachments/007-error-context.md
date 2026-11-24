# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-ux.spec.ts >> UI-RISK-008 administration source risk with live evidence
- Location: e2e/audit-specs/admin-ux.spec.ts:187:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('[role="tabpanel"]:visible').getByRole('status').filter({ hasText: /(?:no|empty).*history/i })
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" locator('[role="tabpanel"]:visible').getByRole('status').filter({ hasText: /(?:no|empty).*history/i }) with timeout 5000ms
  - waiting for locator('[role="tabpanel"]:visible').getByRole('status').filter({ hasText: /(?:no|empty).*history/i })

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 06:03 UTC
  - checkbox "Time Switch" [checked]
- button "User Profiles": A
- button "Share Feedback"
- main:
  - tablist "workspaces":
    - tab "Category" [selected]:
      - region "Category":
        - textbox "Workspace Name": Category
        - button "refresh"
    - button "Add Workspace"
  - tabpanel:
    - button "Create New Category"
    - grid:
      - button "Export"
      - rowgroup:
        - row "Actions Category Label Owner Verified? Updated At Updated By Record Id Order No":
          - columnheader "Actions"
          - columnheader "Category Label"
          - columnheader "Owner"
          - columnheader "Verified?"
          - columnheader "Updated At"
          - columnheader "Updated By"
          - columnheader "Record Id"
          - columnheader "Order No"
      - rowgroup:
        - row "Fixture Category TEST_OWNER Oct 22, 2026, 12:05:00 AM UI-ADMIN-01 101 7":
          - cell:
            - menu:
              - menuitem "Edit"
              - menuitem "Verify"
              - menuitem "Deactivate" [disabled]
              - menuitem "Audit"
          - cell "Fixture Category"
          - cell "TEST_OWNER"
          - cell
          - cell "Oct 22, 2026, 12:05:00 AM"
          - cell "UI-ADMIN-01"
          - cell "101"
          - cell "7"
      - paragraph: "Rows per page:"
      - 'combobox "Rows per page: 20"': "20"
      - paragraph: 1–1 of 1
      - button "Go to previous page" [disabled]
      - button "Go to next page" [disabled]
- tooltip "Open Audit"
```

# Test source

```ts
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
  239 |       if ((match = /option displays record ID "(\d+)"/.exec(text))) { await expect(page.getByRole('option', { includeHidden: true }).filter({ hasText: new RegExp(match[1]) })).toHaveCount(1); return; }
  240 |       if ((match = /^Admin A clicks icon button named "Audit" inside row with Record Id "(\d+)"/.exec(text))) { await app.action('Audit', match[1]).click({ timeout: 5000 }); return; }
> 241 |       if (text.includes('explicit empty-history status')) { await expect(app.panel.getByRole('status').filter({ hasText: /(?:no|empty).*history/i })).toBeVisible(); return; }
      |                                                                                                                                                       ^ Error: expect(locator).toBeVisible() failed
  242 |       if (text.includes('identifies source record "102"') || text.includes('each cell in the "Category ID"')) { await expect(app.auditDialog().locator('[data-id] [data-field="applicationCategoryId"]')).toHaveText(['102']); return; }
  243 |       throw new Error(`No source-risk UI binding for ${id} step ${step.number}: ${text}`);
  244 |     });
  245 |   });
  246 | }
  247 | 
```