# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-expanded.spec.ts >> UI-ADM-SEL-001 actual administration UI with step evidence
- Location: e2e/audit-specs/admin-expanded.spec.ts:15:3

# Error details

```
Error: No administration UI binding for canonical step 3: the Tile administration controls finish rendering
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
        - generic [ref=e27]: 05:29 UTC
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
              - combobox "Application Category" [ref=e67]
              - button "Open" [ref=e69] [cursor=pointer]
          - button "refresh" [disabled]
        - generic [ref=e72]:
          - button "Create New Tile" [disabled]
          - grid [ref=e74]:
            - button "Export" [ref=e76] [cursor=pointer]
            - generic [ref=e80]:
              - rowgroup [ref=e81]:
                - row [ref=e82]:
                  - columnheader "Actions" [ref=e83]
                  - columnheader "Tile Name" [ref=e86] [cursor=pointer]
                  - columnheader "Description" [ref=e89] [cursor=pointer]
                  - columnheader "Image URL for Dark Theme" [ref=e92] [cursor=pointer]
                  - columnheader "Image URL for Light Theme" [ref=e95] [cursor=pointer]
                  - columnheader "Container" [ref=e98] [cursor=pointer]
                  - columnheader "Module Path" [ref=e101] [cursor=pointer]
                  - columnheader "Tile Path" [ref=e104] [cursor=pointer]
                  - columnheader "Role Subject" [ref=e107] [cursor=pointer]
                  - columnheader "Role Entities" [ref=e110] [cursor=pointer]
              - rowgroup [ref=e113]:
                - row [ref=e114]:
                  - cell [ref=e115]:
                    - menu [ref=e116]:
                      - menuitem "Edit" [ref=e117] [cursor=pointer]
                      - menuitem "Verify" [ref=e120] [cursor=pointer]
                      - menuitem "Deactivate" [disabled]
                      - menuitem "Audit" [ref=e123] [cursor=pointer]
                  - cell "Fixture Tile" [ref=e126]
                  - cell "Demo" [ref=e127]
                  - cell "darkIcons/icon01.svg" [ref=e128]
                  - cell "lightIcons/icon01.svg" [ref=e129]
                  - cell "@fm/test" [ref=e130]
                  - cell "/test" [ref=e131]
                  - cell "/test-entry" [ref=e132]
                  - cell "TEST_SUBJECT" [ref=e133]
                  - cell "TEST_ENTITY" [ref=e134]
            - generic [ref=e137]:
              - paragraph [ref=e138]: "Rows per page:"
              - generic [ref=e139]:
                - 'combobox "Rows per page: 20" [ref=e140] [cursor=pointer]': "20"
                - textbox [aria-hidden]: "20"
              - paragraph [ref=e141]: 1–1 of 1
              - generic [ref=e142]:
                - button "Go to previous page" [disabled]
                - button "Go to next page" [disabled]
```

# Test source

```ts
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
  160 |       if ((match = /^a circular loading indicator is visible inside button named "([^"]+)"/.exec(text))) { await expect(app.footerButton(match[1]).getByRole('progressbar')).toBeVisible(); return; }
  161 |       if (text.startsWith('Admin A clicks switch named "Time Switch"')) { await page.getByRole('checkbox', { name: 'Time Switch', exact: true }).click(); return; }
  162 |       if (text.startsWith('switch named "Time Switch"')) { await expect(page.getByRole('checkbox', { name: 'Time Switch', exact: true })).not.toBeChecked(); return; }
  163 |       if (text.startsWith('cell named "Updated At"') && (text.includes('represents date') || text.includes('declared en-locale'))) {
  164 |         const expected = new Intl.DateTimeFormat('en', { dateStyle: 'medium', timeStyle: 'medium', timeZone: id === 'UI-ADM-GRD-009' ? 'Asia/Singapore' : 'UTC' }).format(new Date('2026-10-22T00:05:00Z'));
  165 |         await expect(await app.reveal('updatedAt', '101')).toHaveText(expected); return;
  166 |       }
> 167 |       throw new Error(`No administration UI binding for canonical step ${step.number}: ${text}`);
      |             ^ Error: No administration UI binding for canonical step 3: the Tile administration controls finish rendering
  168 |     });
  169 |     await audit.record('ui-origin-admin-requests', app.requests);
  170 |   });
  171 | }
  172 | 
```