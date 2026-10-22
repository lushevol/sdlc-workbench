# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-expanded.spec.ts >> UI-ADM-GRD-007 actual administration UI with step evidence
- Location: e2e/audit-specs/admin-expanded.spec.ts:15:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText(/^(?:new|edit|verify|deactivate) ID:/) }).locator('button').filter({ hasText: /^Create$/ }).getByRole('progressbar')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText(/^(?:new|edit|verify|deactivate) ID:/) }).locator('button').filter({ hasText: /^Create$/ }).getByRole('progressbar') with timeout 5000ms
  - waiting for locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText(/^(?:new|edit|verify|deactivate) ID:/) }).locator('button').filter({ hasText: /^Create$/ }).getByRole('progressbar')

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
      - generic [ref=e27]: 05:31 UTC
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
                      - menuitem [disabled]
                      - menuitem [ref=e108] [cursor=pointer]
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
                - generic [ref=e138]: "new ID: 1792647067506"
                - generic [ref=e139]:
                  - button [ref=e140] [cursor=pointer]: Maximize
                  - button [disabled]:
                    - generic: Close
            - generic [ref=e145]:
              - generic [ref=e146]:
                - generic [ref=e147]: Category Label
                - textbox [ref=e149]:
                  - /placeholder: Type here
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
                  - text: 2026-10-22T05:31:07.506Z
              - generic [ref=e162]:
                - generic [ref=e163]: Created By
                - textbox [disabled] [ref=e165]:
                  - /placeholder: Type here
                  - text: UI-ADMIN-01
              - generic [ref=e166]:
                - generic [ref=e167]: Updated At
                - textbox [disabled] [ref=e169]:
                  - /placeholder: Type here
                  - text: 2026-10-22T05:31:07.506Z
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
              - button [disabled]:
                - progressbar
                - text: Create
              - button [disabled]:
                - progressbar
                - text: Reset
              - button [disabled]:
                - progressbar
                - text: Close
            - button [ref=e183]
```

# Test source

```ts
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
  114 |       if (text.startsWith('all displayed values of record 101')) { await expect(app.row()).toHaveText(app.beforeValues); return; }
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
> 160 |       if ((match = /^a circular loading indicator is visible inside button named "([^"]+)"/.exec(text))) { await expect(app.footerButton(match[1]).getByRole('progressbar')).toBeVisible(); return; }
      |                                                                                                                                                                              ^ Error: expect(locator).toBeVisible() failed
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