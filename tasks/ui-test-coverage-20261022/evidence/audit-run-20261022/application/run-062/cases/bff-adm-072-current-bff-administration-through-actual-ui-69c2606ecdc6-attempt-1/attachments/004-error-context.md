# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: bff-admin.spec.ts >> BFF-ADM-072 current BFF administration through actual UI
- Location: e2e/audit-specs/bff-admin.spec.ts:10:2

# Error details

```
TimeoutError: locator.click: Timeout 8000ms exceeded.
Call log:
  - waiting for getByRole('option', { name: 'category-a', exact: true })

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
        - generic [ref=e27]: 06:04 UTC
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
          - generic [ref=e63]:
            - generic [ref=e64]:
              - generic [ref=e65]: Application Category
              - generic [ref=e66]:
                - combobox "Application Category" [expanded] [active] [ref=e67]
                - button "Close" [ref=e69] [cursor=pointer]
            - listbox "Application Category" [ref=e72]:
              - option "All" [ref=e73] [cursor=pointer]
          - button "refresh" [disabled]
        - generic [ref=e75]:
          - button "Create New Tile" [disabled]
          - grid [ref=e77]:
            - button "Export" [ref=e79] [cursor=pointer]
            - generic [ref=e83]:
              - rowgroup [ref=e84]:
                - row [ref=e85]:
                  - columnheader "Actions" [ref=e86]
                  - columnheader "Tile Name" [ref=e89] [cursor=pointer]
                  - columnheader "Description" [ref=e92] [cursor=pointer]
                  - columnheader "Image URL for Dark Theme" [ref=e95] [cursor=pointer]
                  - columnheader "Image URL for Light Theme" [ref=e98] [cursor=pointer]
                  - columnheader "Container" [ref=e101] [cursor=pointer]
                  - columnheader "Module Path" [ref=e104] [cursor=pointer]
                  - columnheader "Tile Path" [ref=e107] [cursor=pointer]
                  - columnheader "Role Subject" [ref=e110] [cursor=pointer]
                  - columnheader "Role Entities" [ref=e113] [cursor=pointer]
              - generic: No rows
              - rowgroup
            - generic [ref=e120]:
              - paragraph [ref=e121]: "Rows per page:"
              - generic [ref=e122]:
                - 'combobox "Rows per page: 20" [ref=e123] [cursor=pointer]': "20"
                - textbox [aria-hidden]: "20"
              - paragraph [ref=e124]: 0–0 of 0
              - generic [ref=e125]:
                - button "Go to previous page" [disabled]
                - button "Go to next page" [disabled]
```

# Test source

```ts
  52  |     if (caseId === 'UI-ADM-SEL-006' || caseId === 'UI-ADM-SEL-007' || caseId === 'UI-ADM-SEL-015') this.rows[0].title = 'Tile A';
  53  |     if (caseId === 'UI-ADM-SEL-012') this.rows[0].template = true;
  54  |     const rowCount = caseId === 'UI-ADM-GRD-002' ? 75 : caseId === 'UI-ADM-GRD-004' ? 105
  55  |       : ['UI-ADM-GRD-001', 'UI-ADM-GRD-003'].includes(caseId) ? 25 : caseId === 'UI-ADM-GRD-005' ? 2 : 1;
  56  |     if (kind === 'Category' && rowCount > 1) this.rows = Array.from({ length: rowCount }, (_, i) => categoryRecord(101 + i, `Fixture Category ${101 + i}`));
  57  |   }
  58  | 
  59  |   dialog(): Locator { return this.panel.locator('[role="dialog"]').filter({ has: this.page.getByText(/^(?:new|edit|verify|deactivate) ID:/) }); }
  60  |   auditDialog(): Locator { return this.panel.locator('[role="dialog"]').filter({ has: this.page.getByText('Audit', { exact: true }) }); }
  61  |   row(id = '101'): Locator { return this.grid.locator(`[data-id="${id}"]`); }
  62  |   action(name: string, id = '101'): Locator { return this.row(id).getByRole('menuitem', { name, exact: true }); }
  63  |   footerButton(name: string): Locator { return this.dialog().locator('button').filter({ hasText: new RegExp(`^${name}$`) }); }
  64  |   field(name: string, role = 'textbox'): Locator {
  65  |     if (name === 'Is Template?') return this.dialog().getByTestId('ModalInput-template-11').locator('[role="button"], [role="combobox"]');
  66  |     return this.dialog().getByRole(role as 'textbox', { name, exact: true, includeHidden: true });
  67  |   }
  68  | 
  69  |   async setup(reuseSession = false): Promise<void> {
  70  |     await blockExternal(this.page);
  71  |     const accessToken = this.access || fixtureAccess();
  72  |     const categories = [categoryRecord(81), categoryRecord(82, 'Other Category')];
  73  |     const oneCategory = this.caseId === 'UI-ADM-SEL-003';
  74  |     const app = this;
  75  |     await this.page.route('**/api/auth/v1/fmo/admin/**', async route => {
  76  |       const name = new URL(route.request().url()).pathname.split('/').slice(-2).join('/');
  77  |       const body = route.request().postDataJSON() ?? {};
  78  |       app.requests.push({ endpoint: name, body });
  79  |       const [resource, operation] = name.split('/');
  80  |       let data: any;
  81  |       if (operation === 'data') {
  82  |         if (app.caseId === 'UI-ADM-SEL-007' && resource === 'tile' && !body.applicationCategory?.applicationCategoryId
  83  |           && app.requests.filter(request => request.endpoint === 'tile/data').length > 2) { await new Promise<void>(() => {}); return; }
  84  |         if (resource === 'category' && app.kind === 'Tile') data = oneCategory ? categories.slice(0, 1) : categories;
  85  |         else if (resource === 'importmap' && app.kind === 'Tile') data = [{ ...importMapRecord(), importMapId: 71 }];
  86  |         else data = app.rows;
  87  |         if (app.caseId === 'UI-ADM-SEL-015' && resource === 'tile' && ++app.refreshCount > 2) data = [{ ...app.rows[0], title: 'Tile B' }];
  88  |       } else if (operation === 'audit') {
  89  |         data = [9001, 9002].map(id => ({ ...app.rows[0], [identity[app.kind]]: body[identity[app.kind]],
  90  |           applicationCategoryAuditId: id, importMapAuditId: id, applicationTileAuditId: id, transactionMode: 'maker' }));
  91  |         if (app.caseId === 'UI-ADM-GRD-005') data = [data[body.applicationCategoryId === 102 ? 1 : 0]];
  92  |       } else {
  93  |         if (app.caseId === 'UI-ADM-GRD-007') { await new Promise<void>(() => {}); return; }
  94  |         if (/UI-ADM-FLD-00[5-8]/.test(app.caseId)) data = {};
  95  |         else {
  96  |           data = { ...app.rows[0], ...body, [identity[app.kind]]: operation === 'create' ? 102 : body[identity[app.kind]],
  97  |             updatedBy: 'UI-ADMIN-01' };
  98  |           // These six cases declare fixed response records. Request persistence is checked by separate UX cases.
  99  |           if (/^UI-ADM-(CAT|MAP|TIL)-00[35]$/.test(app.caseId)) {
  100 |             if (app.kind === 'Category') data.label = 'Changed Category';
  101 |             if (app.kind === 'Import Map') data.path = 'https://assets.example.test/v2.js';
  102 |             if (app.kind === 'Tile') data.title = 'Changed Tile';
  103 |           }
  104 |           if (body.mode === 'checker') data.active = true;
  105 |           if (body.mode === 'deactivate') data.active = false;
  106 |           if (operation === 'create') app.rows = [data, ...app.rows];
  107 |           else app.rows = app.rows.map(row => row[identity[app.kind]] === data[identity[app.kind]] ? data : row);
  108 |         }
  109 |       }
  110 |       await route.fulfill({ status: 200, json: { data } });
  111 |     });
  112 |     const initial = { ...workspace(this.workspaceLabel || this.kind), containers: [{ id: 'ADMIN-CONTAINER', container: '@fm/base',
  113 |       module: `/${endpoint[this.kind]}`, tile: '', title: this.kind, emailSupport: 'support@example.test', panelId: '', tabId: '', parameters: {} }] };
  114 |     await this.page.addInitScript(initial => localStorage.setItem('SET_WORKSPACES', JSON.stringify([initial])), initial);
  115 |     const superUser = ['UI-ADM-FLD-004', 'UI-RISK-004'].includes(this.caseId);
  116 |     for (const name of ['login', 'validate', 'extend']) await this.page.route(`**/api/auth/v2/sso/${name}`, route => route.fulfill({ status: 200,
  117 |       headers: { 'content-type': 'application/json', 'single-ui-authorization': accessToken },
  118 |       json: { userInfo: JSON.stringify({ sub: this.principal || (superUser ? 'UI-SUPER-01' : 'UI-ADMIN-01'), fullName: 'Audit Admin', auth_time: Math.floor(Date.now() / 1000) }),
  119 |         entitlementsToken: accessToken.replace('Bearer ', ''),
  120 |         drawers: [{ id: 1, label: 'Administration fixture', tiles: [{ ...initial.containers[0],
  121 |           isTemplate: true, imageDarkTheme: '', entity: ['FMO PORTAL ADMIN'], subject: 'ADMIN_UI' }] }],
  122 |         entities: [{ id: 1, name: 'FMO PORTAL ADMIN', applicationName: 'Portal', roleId: 1,
  123 |           roleName: superUser ? 'SUPER_USER' : 'TEST_OWNER', subjects: [] }], result: true } }));
  124 |     await this.page.route('**/api/auth/v2/sso/refreshtoken', route => route.fulfill({ status: 200,
  125 |       headers: { 'single-ui-refresh': accessToken }, json: {} }));
  126 |     if (reuseSession) await this.page.goto(`${localBase}/?show_normal_login=Y`);
  127 |     else {
  128 |       const login = await openLogin(this.page);
  129 |       await login.fillUsername(credentials.username); await login.fillPassword(credentials.password); await login.clickSignInButton();
  130 |     }
  131 |     await this.portal.expectVisible();
  132 |   }
  133 | 
  134 |   async open(): Promise<void> {
  135 |     await expect(this.grid).toBeVisible();
  136 |     if (this.kind === 'Tile' && !/^UI-ADM-SEL-00[1-7]$/.test(this.caseId)) await this.selectCategory();
  137 |     this.beforeRows = await this.grid.locator('[data-id]').count();
  138 |     this.beforeValues = await this.row().textContent().then(value => value ?? '').catch(() => '');
  139 |     if (/-012$/.test(this.caseId) && !this.caseId.includes('-SEL-')) {
  140 |       await this.action('Edit').click(); await this.field(this.kind === 'Category' ? 'Category Label' : this.kind === 'Import Map' ? 'Module Name' : 'Tile Name').fill(`Changed ${this.kind}`);
  141 |     }
  142 |     if (/UI-ADM-FLD-00[5-8]/.test(this.caseId) || /^UI-ADM-SEL-0(?:09|10|11|12|13|14)$/.test(this.caseId)) {
  143 |       if (['UI-ADM-FLD-005', 'UI-ADM-FLD-007', 'UI-ADM-SEL-009'].includes(this.caseId)) await this.panel.getByRole('button', { name: `Create New ${this.kind}`, exact: true }).click();
  144 |       else await this.action('Edit').click();
  145 |       if (this.caseId === 'UI-ADM-FLD-005') { await this.field('Module Name').fill('@fm/test'); await this.field('Path').fill('https://assets.example.test/v1.js'); }
  146 |     }
  147 |     if (this.caseId === 'UI-ADM-GRD-005') await this.action('Audit').click();
  148 |     if (this.caseId === 'UI-ADM-GRD-007') { await this.panel.getByRole('button', { name: 'Create New Category', exact: true }).click(); await this.footerButton('Create').click(); }
  149 |   }
  150 | 
  151 |   async selectCategory(name = 'Fixture Category'): Promise<void> {
> 152 |     await this.category.click(); await this.page.getByRole('option', { name, exact: true }).click();
      |                                                                                             ^ TimeoutError: locator.click: Timeout 8000ms exceeded.
  153 |     await expect(this.category).toHaveValue(name);
  154 |   }
  155 | 
  156 |   async reveal(field: string, id?: string): Promise<Locator> {
  157 |     const selector = id ? this.row(id).locator(`[data-field="${field}"]`) : this.grid.getByRole('columnheader').filter({ has: this.page.locator(`[data-field="${field}"]`) });
  158 |     const target = id ? selector : this.grid.locator(`[role="columnheader"][data-field="${field}"]`);
  159 |     const scroller = this.grid.locator('.MuiDataGrid-virtualScroller');
  160 |     await scroller.evaluate(node => { node.scrollLeft = 0; });
  161 |     for (let index = 0; index < 25; index++) {
  162 |       if (await target.count() && await target.isVisible()) { await target.scrollIntoViewIfNeeded(); return target; }
  163 |       await scroller.evaluate(node => { node.scrollLeft += 500; });
  164 |       await this.page.waitForTimeout(20);
  165 |     }
  166 |     await expect(target).toBeVisible(); return target;
  167 |   }
  168 | }
  169 | 
```