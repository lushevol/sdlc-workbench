# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-expanded.spec.ts >> UI-ADM-CAT-011 actual administration UI with step evidence
- Location: e2e/audit-specs/admin-expanded.spec.ts:15:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('[role="tabpanel"]:visible').getByTestId('MicroWebUI_base_simple_table').getByRole('grid', { includeHidden: true }).locator('[data-id="101"]').locator('[data-field="active"]').getByTestId('ErrorIcon')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" locator('[role="tabpanel"]:visible').getByTestId('MicroWebUI_base_simple_table').getByRole('grid', { includeHidden: true }).locator('[data-id="101"]').locator('[data-field="active"]').getByTestId('ErrorIcon') with timeout 5000ms
  - waiting for locator('[role="tabpanel"]:visible').getByTestId('MicroWebUI_base_simple_table').getByRole('grid', { includeHidden: true }).locator('[data-id="101"]').locator('[data-field="active"]').getByTestId('ErrorIcon')

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 05:26 UTC
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
```

# Test source

```ts
  6   | 
  7   | const ids = [
  8   |   ...['CAT', 'MAP', 'TIL'].flatMap(group => Array.from({ length: 14 }, (_, i) => `UI-ADM-${group}-${String(i + 1).padStart(3, '0')}`)),
  9   |   ...Array.from({ length: 8 }, (_, i) => `UI-ADM-FLD-${String(i + 1).padStart(3, '0')}`),
  10  |   ...Array.from({ length: 15 }, (_, i) => `UI-ADM-SEL-${String(i + 1).padStart(3, '0')}`),
  11  |   ...Array.from({ length: 9 }, (_, i) => `UI-ADM-GRD-${String(i + 1).padStart(3, '0')}`),
  12  | ];
  13  | 
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
> 106 |         await expect(cell.getByTestId(match[2] === 'Verified' ? 'CheckCircleIcon' : 'ErrorIcon')).toBeVisible();
      |                                                                                                   ^ Error: expect(locator).toBeVisible() failed
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
  167 |       throw new Error(`No administration UI binding for canonical step ${step.number}: ${text}`);
  168 |     });
  169 |     await audit.record('ui-origin-admin-requests', app.requests);
  170 |   });
  171 | }
  172 | 
```