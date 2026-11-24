# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-expanded.spec.ts >> UI-ADM-FLD-006 actual administration UI with step evidence
- Location: e2e/audit-specs/admin-expanded.spec.ts:15:3

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator: locator('[role="tabpanel"]:visible').getByTestId('MicroWebUI_base_simple_table').getByRole('grid', { includeHidden: true }).locator('[data-id="101"]')
Timeout: 5000ms
- Expected  - 6
+ Received  + 1

- @fm/test
- https://assets.example.test/v1.js
- TEST_OWNER
- Oct 22, 2026, 12:05:00 AM
- UI-ADMIN-01
- 101
+ @fm/testhttps://assets.example.test/v1.jsTEST_OWNEROct 22, 2026, 12:05:00 AMUI-ADMIN-01101

Call log:
  - Expect "toHaveText" locator('[role="tabpanel"]:visible').getByTestId('MicroWebUI_base_simple_table').getByRole('grid', { includeHidden: true }).locator('[data-id="101"]') with timeout 5000ms
  - waiting for locator('[role="tabpanel"]:visible').getByTestId('MicroWebUI_base_simple_table').getByRole('grid', { includeHidden: true }).locator('[data-id="101"]')
    14 × locator resolved to <div role="row" data-id="101" data-rowindex="0" aria-rowindex="2" aria-selected="false" class="MuiDataGrid-row MuiDataGrid-row--lastVisible">…</div>
       - unexpected value "@fm/testhttps://assets.example.test/v1.jsTEST_OWNEROct 22, 2026, 12:05:00 AMUI-ADMIN-01101"

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
      - generic [ref=e27]: 05:29 UTC
      - checkbox [checked] [ref=e30] [cursor=pointer]
    - button [ref=e34] [cursor=pointer]:
      - generic [ref=e35]: A
    - button [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region [ref=e48]:
          - textbox [ref=e52]: Import Map
          - button [ref=e53]
      - button [ref=e57] [cursor=pointer]
    - tabpanel [ref=e62]:
      - generic [ref=e65]:
        - button [ref=e66] [cursor=pointer]: Create New Import Map
        - generic [ref=e67]:
          - grid [ref=e68]:
            - button [ref=e70] [cursor=pointer]: Export
            - generic [ref=e74]:
              - rowgroup [ref=e75]:
                - row [ref=e76]:
                  - columnheader [ref=e77]:
                    - generic [ref=e78]: Actions
                  - columnheader [ref=e80] [cursor=pointer]:
                    - generic [ref=e81]: Module Name
                  - columnheader [ref=e83] [cursor=pointer]:
                    - generic [ref=e84]: Path
                  - columnheader [ref=e86] [cursor=pointer]:
                    - generic [ref=e87]: Owner
                  - columnheader [ref=e89] [cursor=pointer]:
                    - generic [ref=e90]: Verified?
                  - columnheader [ref=e92] [cursor=pointer]:
                    - generic [ref=e93]: Updated At
                  - columnheader [ref=e95] [cursor=pointer]:
                    - generic [ref=e96]: Updated By
                  - columnheader [ref=e98] [cursor=pointer]:
                    - generic [ref=e99]: Record Id
              - rowgroup [ref=e101]:
                - row [ref=e102]:
                  - cell [ref=e103]:
                    - menu [ref=e104]:
                      - menuitem [ref=e105] [cursor=pointer]
                      - menuitem [ref=e108] [cursor=pointer]
                      - menuitem [disabled]
                      - menuitem [ref=e111] [cursor=pointer]
                  - cell [ref=e114]: "@fm/test"
                  - cell [ref=e115]: https://assets.example.test/v1.js
                  - cell [ref=e116]: TEST_OWNER
                  - cell [ref=e117]
                  - cell [ref=e120]:
                    - generic [ref=e121]: Oct 22, 2026, 12:05:00 AM
                  - cell [ref=e122]: UI-ADMIN-01
                  - cell [ref=e123]: "101"
            - generic [ref=e126]:
              - paragraph [ref=e127]: "Rows per page:"
              - generic [ref=e128]:
                - combobox [ref=e129] [cursor=pointer]: "20"
                - textbox [aria-hidden]: "20"
              - paragraph [ref=e130]: 1–1 of 1
              - generic [ref=e131]:
                - button [disabled]
                - button [disabled]
          - dialog [ref=e134]:
            - heading [level=2] [ref=e135]:
              - generic [ref=e136]:
                - generic [ref=e137]: "edit ID: 101"
                - generic [ref=e138]:
                  - button [ref=e139] [cursor=pointer]: Maximize
                  - button [disabled]:
                    - generic: Close
            - generic [ref=e144]:
              - generic [ref=e145]:
                - generic [ref=e146]: Module Name
                - textbox [ref=e148]:
                  - /placeholder: Type here
                  - text: "@fm/test"
              - generic [ref=e149]:
                - generic [ref=e150]: Path
                - textbox [ref=e152]:
                  - /placeholder: Type here
                  - text: https://assets.example.test/v1.js
              - generic [ref=e153]:
                - generic [ref=e154]: Owner
                - textbox [disabled] [ref=e156]:
                  - /placeholder: Type here
                  - text: TEST_OWNER
              - generic [ref=e157]:
                - generic [ref=e158]: Verified?
                - textbox [disabled] [ref=e160]:
                  - /placeholder: Type here
                  - text: "false"
              - generic [ref=e161]:
                - generic [ref=e162]: Created At
                - textbox [disabled] [ref=e164]:
                  - /placeholder: Type here
                  - text: 2026-10-21T00:05:00Z
              - generic [ref=e165]:
                - generic [ref=e166]: Created By
                - textbox [disabled] [ref=e168]:
                  - /placeholder: Type here
                  - text: UI-ADMIN-01
              - generic [ref=e169]:
                - generic [ref=e170]: Updated At
                - textbox [disabled] [ref=e172]:
                  - /placeholder: Type here
                  - text: 2026-10-22T00:05:00Z
              - generic [ref=e173]:
                - generic [ref=e174]: Updated By
                - textbox [disabled] [ref=e176]:
                  - /placeholder: Type here
                  - text: UI-ADMIN-01
              - generic [ref=e177]:
                - generic [ref=e178]: Record Id
                - textbox [disabled] [ref=e180]:
                  - /placeholder: <<will be auto generated>>
                  - text: "101"
            - generic [ref=e181]:
              - button [ref=e182] [cursor=pointer]: Update
              - button [ref=e183] [cursor=pointer]: Reset
              - button [ref=e184] [cursor=pointer]: Close
            - button [ref=e185]
```

# Test source

```ts
  14  | for (const id of ids) {
  15  |   test(`${id} actual administration UI with step evidence`, async ({ page, audit }) => {
  16  |     const steps = await audit.defineCase(id);
  17  |     const description = steps.map(step => step.text).join('\n');
  18  |     const kind: AdminKind = id.includes('-MAP-') || ['UI-ADM-FLD-005', 'UI-ADM-FLD-006'].includes(id) ? 'Import Map'
  19  |       : id.includes('-TIL-') || id.includes('-SEL-') || ['UI-ADM-FLD-007', 'UI-ADM-FLD-008'].includes(id) ? 'Tile' : 'Category';
  20  |     const app = new AdminApp(page, kind, id);
  21  |     const field = (name: string) => name === 'Record Id' ? (kind === 'Category' ? 'applicationCategoryId' : kind === 'Import Map' ? 'importMapId' : 'applicationTileId') : adminFields[name];
  22  |     const input = (role: string, name: string) => app.field(name, role === 'textarea' ? 'textbox' : role);
  23  |     let clock = false;
  24  |     let newId = '';
  25  |     let comboName = '';
  26  | 
  27  |     for (const step of steps) await audit.step(step.number, async () => {
  28  |       const text = step.text;
  29  |       if (step.number === 1) { await app.setup(); return; }
  30  |       if (step.number === 2) {
  31  |         await app.open();
  32  |         if (id === 'UI-ADM-SEL-007' || id === 'UI-ADM-SEL-015') await app.selectCategory();
  33  |         if (description.includes('controlled field clock')) {
  34  |           const now = new Date(); await page.clock.install({ time: now }); await page.clock.pauseAt(new Date(now.getTime() + 20)); clock = true;
  35  |         }
  36  |         return;
  37  |       }
  38  |       if (/^the declared controlled field clock advances by 300 milliseconds$/.test(text)) {
  39  |         expect(clock).toBe(true); await page.clock.runFor(300); return;
  40  |       }
  41  |       if (/administration (?:grid|controls) finishes rendering|action cell for record/.test(text)) {
  42  |         await expect(app.grid).toBeVisible(); return;
  43  |       }
  44  |       let match: RegExpExecArray | null;
  45  |       if ((match = /^Admin A clicks button named "([^"]+)"/.exec(text))) {
  46  |         if (match[1].startsWith('Create New')) {
  47  |           await app.panel.getByRole('button', { name: match[1], exact: true }).click();
  48  |           newId = (await app.dialog().getAttribute('aria-labelledby')) ?? '';
  49  |           await audit.record('new-record-source-identity', { actualTitle: await app.dialog().innerText(), titleId: newId });
  50  |         } else {
  51  |           await app.footerButton(match[1]).click();
  52  |           if (['Create', 'Update', 'Verified', 'Deactivate'].includes(match[1])) await audit.record('ui-origin-admin-requests', app.requests);
  53  |         }
  54  |         return;
  55  |       }
  56  |       if ((match = /^Admin A clicks icon button named "(Edit|Verify|Deactivate|Audit)" inside row with Record Id "([^"]+)"/.exec(text))) {
  57  |         await app.action(match[1], match[2]).click(); return;
  58  |       }
  59  |       if ((match = /^Admin A (?:enters|enters exactly) "(.*)" into (textbox|textarea|spinbutton) named "([^"]+)"/.exec(text))) {
  60  |         await input(match[2], match[3]).fill(match[1].replaceAll('\\n', '\n')); return;
  61  |       }
  62  |       if ((match = /^Admin A replaces the value of (textbox|textarea|spinbutton) named "([^"]+)".* with "(.*)"$/.exec(text))) {
  63  |         await input(match[1], match[2]).fill(match[3].replaceAll('\\n', '\n')); return;
  64  |       }
  65  |       if ((match = /^Admin A opens combobox named "([^"]+)"/.exec(text))) {
  66  |         comboName = match[1];
  67  |         if (comboName === 'Is Template?') await audit.record('source-resolved-template-selector', {
  68  |           canonicalTarget: 'combobox named Is Template?', source: 'TableDetail/Field.tsx singleSelect',
  69  |           sourceIdentity: 'ModalInput-template-11', limit: 'The current MUI Select does not expose the declared label as its accessible name.' });
  70  |         await (comboName === 'Application Category' ? app.category : app.field(comboName, 'combobox')).click(); return;
  71  |       }
  72  |       if ((match = /^Admin A clicks option named "([^"]+)"/.exec(text))) {
  73  |         // MUI image alternatives contribute to option names. Text must still match the declared value.
  74  |         const option = page.getByRole('option', { includeHidden: true }).filter({ hasText: new RegExp(`^${match[1].replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`) });
  75  |         await expect(option).toHaveCount(1); await option.click(); return;
  76  |       }
  77  |       if ((match = /^column named "([^"]+)".* is visible$/.exec(text))) { await expect(await app.reveal(field(match[1]))).toBeVisible(); return; }
  78  |       if ((match = /^(textbox|textarea|spinbutton|combobox) named "([^"]+)".* (is disabled|is enabled|has value "(.*)"|has exactly the value "(.*)" where \\n represents one line break|has an empty value)$/.exec(text))) {
  79  |         const target = match[2] === 'Application Category' ? app.category : input(match[1], match[2]);
  80  |         if (match[3] === 'is disabled') await expect(target).toBeDisabled();
  81  |         else if (match[3] === 'is enabled') await expect(target).toBeEnabled();
  82  |         else await expect(target).toHaveValue((match[4] ?? match[5] ?? '').replaceAll('\\n', '\n'));
  83  |         return;
  84  |       }
  85  |       if ((match = /^button named "([^"]+)".* (is visible|is disabled|is enabled)$/.exec(text))) {
  86  |         const target = text.includes('dialog') ? app.footerButton(match[1]) : app.panel.getByRole('button', { name: match[1], exact: true });
  87  |         if (match[2] === 'is visible') await expect(target).toBeVisible();
  88  |         else if (match[2] === 'is disabled') await expect(target).toBeDisabled();
  89  |         else await expect(target).toBeEnabled();
  90  |         return;
  91  |       }
  92  |       if ((match = /^dialog (?:named|with source identity) "([^"]+)".* (is visible|is absent)$/.exec(text))) {
  93  |         const target = match[1] === 'Audit' ? app.auditDialog() : app.panel.locator('[role="dialog"]').filter({ has: page.getByText(match[1].startsWith('new ID:') ? /^new ID: \d+$/ : match[1], { exact: true }) });
  94  |         if (match[2] === 'is visible') await expect(target).toBeVisible(); else await expect(target).toHaveCount(0);
  95  |         return;
  96  |       }
  97  |       if ((match = /^icon button named "(Verify|Deactivate)" inside row with Record Id "([^"]+)".* (is enabled|is disabled)$/.exec(text))) {
  98  |         if (match[3] === 'is enabled') await expect(app.action(match[1], match[2])).toBeEnabled();
  99  |         else await expect(app.action(match[1], match[2])).toBeDisabled(); return;
  100 |       }
  101 |       if ((match = /^cell named "([^"]+)" inside row with Record Id "([^"]+)".* displays "(.*)"$/.exec(text))) {
  102 |         await expect(await app.reveal(field(match[1]), match[2].includes('Tile A') ? '101' : match[2])).toHaveText(match[3]); return;
  103 |       }
  104 |       if ((match = /^cell named "Verified\?" inside row with Record Id "([^"]+)".* tooltip "([^"]+)"$/.exec(text))) {
  105 |         const cell = await app.reveal('active', match[1]);
  106 |         await expect(cell.getByTestId(match[2] === 'Verified' ? 'CheckCircleIcon' : 'ErrorIcon')).toBeVisible();
  107 |         await cell.hover(); await expect(page.getByRole('tooltip', { name: match[2], exact: true })).toBeVisible(); return;
  108 |       }
  109 |       if ((match = /^exactly one row with Record Id "([^"]+)"/.exec(text))) { await expect(app.row(match[1])).toHaveCount(1); return; }
  110 |       if (text.includes('data row count') && /pre-action count/.test(text)) {
  111 |         await expect(app.grid.locator('[data-id]')).toHaveCount(app.beforeRows); return;
  112 |       }
  113 |       if (text.startsWith('no new row for the declared fixture')) { await expect(app.row('102')).toHaveCount(0); return; }
> 114 |       if (text.startsWith('all displayed values of record 101')) { await expect(app.row()).toHaveText(app.beforeValues); return; }
      |                                                                                            ^ Error: expect(locator).toHaveText(expected) failed
  115 |       if ((match = /^row with source identity "([^"]+)" inside the data grid in the Audit dialog/.exec(text))) {
  116 |         await expect(app.auditDialog().locator(`[data-id="${match[1]}"]`)).toBeVisible(); return;
  117 |       }
  118 |       if ((match = /^the source-record identifier cell in row with source identity "([^"]+)".* equals "([^"]+)"$/.exec(text))) {
  119 |         await expect(app.auditDialog().locator(`[data-id="${match[1]}"] [data-field="${field('Record Id')}"]`)).toHaveText(match[2]); return;
  120 |       }
  121 |       if ((match = /^option named "([^"]+)".* (is visible|is absent)$/.exec(text))) {
  122 |         const target = page.getByRole('option', { name: match[1], exact: true });
  123 |         if (match[2] === 'is visible') await expect(target).toBeVisible(); else await expect(target).toHaveCount(0); return;
  124 |       }
  125 |       if ((match = /^icon button named "refresh".* (is enabled|is disabled)$/.exec(text))) {
  126 |         if (match[1] === 'is enabled') await expect(app.panel.getByRole('button', { name: 'refresh', exact: true })).toBeEnabled();
  127 |         else await expect(app.panel.getByRole('button', { name: 'refresh', exact: true })).toBeDisabled(); return;
  128 |       }
  129 |       if (text.startsWith('Admin A clicks icon button named "refresh"')) { await app.panel.getByRole('button', { name: 'refresh', exact: true }).click(); return; }
  130 |       if ((match = /^(?:no cell|a cell) in the "Tile Name" column.* displays "([^"]+)"$/.exec(text))) {
  131 |         const cells = app.grid.locator('[data-field="title"]').filter({ hasText: new RegExp(`^${match[1]}$`) });
  132 |         if (text.startsWith('no cell')) await expect(cells).toHaveCount(0); else await expect(cells).toBeVisible(); return;
  133 |       }
  134 |       if (text.startsWith('Admin A clicks icon button with source identity "UNVERIFIED category-clear')) {
  135 |         await audit.record('source-resolved-clear-target', { source: 'MUI Autocomplete', accessibleName: 'Clear', canonicalTarget: 'UNVERIFIED category-clear target' });
  136 |         await app.category.locator('..').getByRole('button', { name: 'Clear', exact: true }).click(); return;
  137 |       }
  138 |       if (text.includes('post-clear fetch remains pending')) { await expect(app.grid.locator('[data-id]')).toHaveCount(0); return; }
  139 |       if (text.includes('UNVERIFIED next-page target')) {
  140 |         await audit.record('source-resolved-pagination-target', { actualName: 'Go to next page', canonicalTarget: 'UNVERIFIED next-page target' });
  141 |         await app.grid.getByRole('button', { name: 'Go to next page', exact: true }).click(); return;
  142 |       }
  143 |       if (text.includes('UNVERIFIED page-size target')) {
  144 |         await audit.record('source-resolved-pagination-target', { actualRole: 'combobox', canonicalTarget: 'UNVERIFIED page-size target' });
  145 |         await app.grid.getByRole('combobox').click(); return;
  146 |       }
  147 |       if ((match = /current page.* contains (?:exactly )?(\d+) data records$/.exec(text))) {
  148 |         const size = Number(match[1]);
  149 |         await expect(app.grid.locator('.MuiTablePagination-displayedRows')).toHaveText(size === 5 ? '21–25 of 25' : `1–${size} of ${id === 'UI-ADM-GRD-002' ? 75 : id === 'UI-ADM-GRD-004' ? 105 : 25}`); return;
  150 |       }
  151 |       if ((match = /^row with source identity "([^"]+)" inside the Category administration data grid is visible$/.exec(text))) { await expect(app.row(match[1])).toBeVisible(); return; }
  152 |       if (text.startsWith('Admin A clicks chip with text "Close"')) { await app.auditDialog().getByRole('button', { name: 'Close', exact: true }).click(); return; }
  153 |       if (/^(?:the cell|no cell) in (?:the|that) "Audit ID" column/.test(text)) {
  154 |         const cells = app.auditDialog().locator('[data-field="id"]');
  155 |         if (text.startsWith('no cell')) await expect(cells.filter({ hasText: /^9001$/ })).toHaveCount(0);
  156 |         else await expect(cells.filter({ hasText: /^9002$/ })).toBeVisible(); return;
  157 |       }
  158 |       if (text.startsWith('Admin A clicks cell named "Category Label"')) { await (await app.reveal('label', '101')).click(); return; }
  159 |       if (text === 'the Category create request remains pending') { expect(app.requests.some(request => request.endpoint === 'category/create')).toBe(true); return; }
  160 |       if ((match = /^a circular loading indicator is visible inside button named "([^"]+)"/.exec(text))) { await expect(app.footerButton(match[1]).getByRole('progressbar')).toBeVisible(); return; }
  161 |       if (text.startsWith('Admin A clicks switch named "Time Switch"')) { await page.getByRole('checkbox', { name: 'Time Switch', exact: true }).click(); return; }
  162 |       if (text.startsWith('switch named "Time Switch"')) { await expect(page.getByRole('checkbox', { name: 'Time Switch', exact: true })).not.toBeChecked(); return; }
  163 |       if (text.startsWith('cell named "Updated At"') && (text.includes('represents date') || text.includes('declared en-locale'))) {
  164 |         const expected = new Intl.DateTimeFormat('en', { dateStyle: 'medium', timeStyle: 'medium', timeZone: id === 'UI-ADM-GRD-009' ? 'Asia/Singapore' : 'UTC' }).format(new Date('2026-10-22T00:05:00Z'));
  165 |         await expect(await app.reveal('updatedAt', '101')).toHaveText(expected); return;
  166 |       }
  167 |       throw new Error(`No administration UI binding for canonical step ${step.number}: ${text}`);
  168 |     });
  169 |     await audit.record('ui-origin-admin-requests', app.requests);
  170 |   });
  171 | }
  172 | 
```