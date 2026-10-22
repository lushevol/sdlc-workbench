# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-ux.spec.ts >> UX-054 administration boundary with step screenshots
- Location: e2e/audit-specs/admin-ux.spec.ts:12:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('[role="tabpanel"]:visible').getByTestId('MicroWebUI_base_simple_table').getByRole('grid', { includeHidden: true })
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" locator('[role="tabpanel"]:visible').getByTestId('MicroWebUI_base_simple_table').getByRole('grid', { includeHidden: true }) with timeout 5000ms
  - waiting for locator('[role="tabpanel"]:visible').getByTestId('MicroWebUI_base_simple_table').getByRole('grid', { includeHidden: true })

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 05:45 UTC
  - checkbox "Time Switch" [checked]
- button "User Profiles": A
- button "Share Feedback"
- main:
  - tablist "workspaces":
    - tab "Tile" [selected]:
      - region "Tile":
        - textbox "Workspace Name": Tile
    - button "Add Workspace"
  - tabpanel
```

# Test source

```ts
  31  |   readonly table: Locator;
  32  |   readonly grid: Locator;
  33  |   readonly category: Locator;
  34  |   readonly requests: { endpoint: string; body: Row }[] = [];
  35  |   rows: Row[];
  36  |   beforeRows = 1;
  37  |   beforeValues = '';
  38  |   refreshCount = 0;
  39  |   principal = '';
  40  |   workspaceLabel = '';
  41  | 
  42  |   constructor(readonly page: Page, readonly kind: AdminKind, readonly caseId: string) {
  43  |     this.portal = new PortalPage(page, localPrefix);
  44  |     // disablePortal dialogs remain under an aria-hidden ancestor in the current MUI implementation.
  45  |     this.panel = page.locator('[role="tabpanel"]:visible');
  46  |     this.table = this.panel.getByTestId(`${localPrefix}_simple_table`);
  47  |     this.grid = this.table.getByRole('grid', { includeHidden: true });
  48  |     this.category = this.panel.getByRole('combobox', { name: 'Application Category', exact: true });
  49  |     this.rows = [kind === 'Category' ? categoryRecord() : kind === 'Import Map' ? importMapRecord() : tileRecord()];
  50  |     if (/-00[7]$|-010$|-011$/.test(caseId) && !caseId.includes('-SEL-')) this.rows[0].active = true;
  51  |     if (caseId === 'UI-ADM-SEL-006' || caseId === 'UI-ADM-SEL-007' || caseId === 'UI-ADM-SEL-015') this.rows[0].title = 'Tile A';
  52  |     if (caseId === 'UI-ADM-SEL-012') this.rows[0].template = true;
  53  |     const rowCount = caseId === 'UI-ADM-GRD-002' ? 75 : caseId === 'UI-ADM-GRD-004' ? 105
  54  |       : ['UI-ADM-GRD-001', 'UI-ADM-GRD-003'].includes(caseId) ? 25 : caseId === 'UI-ADM-GRD-005' ? 2 : 1;
  55  |     if (kind === 'Category' && rowCount > 1) this.rows = Array.from({ length: rowCount }, (_, i) => categoryRecord(101 + i, `Fixture Category ${101 + i}`));
  56  |   }
  57  | 
  58  |   dialog(): Locator { return this.panel.locator('[role="dialog"]').filter({ has: this.page.getByText(/^(?:new|edit|verify|deactivate) ID:/) }); }
  59  |   auditDialog(): Locator { return this.panel.locator('[role="dialog"]').filter({ has: this.page.getByText('Audit', { exact: true }) }); }
  60  |   row(id = '101'): Locator { return this.grid.locator(`[data-id="${id}"]`); }
  61  |   action(name: string, id = '101'): Locator { return this.row(id).getByRole('menuitem', { name, exact: true }); }
  62  |   footerButton(name: string): Locator { return this.dialog().locator('button').filter({ hasText: new RegExp(`^${name}$`) }); }
  63  |   field(name: string, role = 'textbox'): Locator {
  64  |     if (name === 'Is Template?') return this.dialog().getByTestId('ModalInput-template-11').locator('[role="button"], [role="combobox"]');
  65  |     return this.dialog().getByRole(role as 'textbox', { name, exact: true, includeHidden: true });
  66  |   }
  67  | 
  68  |   async setup(): Promise<void> {
  69  |     await blockExternal(this.page);
  70  |     const accessToken = fixtureAccess();
  71  |     const categories = [categoryRecord(81), categoryRecord(82, 'Other Category')];
  72  |     const oneCategory = this.caseId === 'UI-ADM-SEL-003';
  73  |     const app = this;
  74  |     await this.page.route('**/api/auth/v1/fmo/admin/**', async route => {
  75  |       const name = new URL(route.request().url()).pathname.split('/').slice(-2).join('/');
  76  |       const body = route.request().postDataJSON() ?? {};
  77  |       app.requests.push({ endpoint: name, body });
  78  |       const [resource, operation] = name.split('/');
  79  |       let data: any;
  80  |       if (operation === 'data') {
  81  |         if (app.caseId === 'UI-ADM-SEL-007' && resource === 'tile' && !body.applicationCategory?.applicationCategoryId
  82  |           && app.requests.filter(request => request.endpoint === 'tile/data').length > 2) { await new Promise<void>(() => {}); return; }
  83  |         if (resource === 'category' && app.kind === 'Tile') data = oneCategory ? categories.slice(0, 1) : categories;
  84  |         else if (resource === 'importmap' && app.kind === 'Tile') data = [{ ...importMapRecord(), importMapId: 71 }];
  85  |         else data = app.rows;
  86  |         if (app.caseId === 'UI-ADM-SEL-015' && resource === 'tile' && ++app.refreshCount > 2) data = [{ ...app.rows[0], title: 'Tile B' }];
  87  |       } else if (operation === 'audit') {
  88  |         data = [9001, 9002].map(id => ({ ...app.rows[0], [identity[app.kind]]: body[identity[app.kind]],
  89  |           applicationCategoryAuditId: id, importMapAuditId: id, applicationTileAuditId: id, transactionMode: 'maker' }));
  90  |         if (app.caseId === 'UI-ADM-GRD-005') data = [data[body.applicationCategoryId === 102 ? 1 : 0]];
  91  |       } else {
  92  |         if (app.caseId === 'UI-ADM-GRD-007') { await new Promise<void>(() => {}); return; }
  93  |         if (/UI-ADM-FLD-00[5-8]/.test(app.caseId)) data = {};
  94  |         else {
  95  |           data = { ...app.rows[0], ...body, [identity[app.kind]]: operation === 'create' ? 102 : body[identity[app.kind]],
  96  |             updatedBy: 'UI-ADMIN-01' };
  97  |           // These six cases declare fixed response records. Request persistence is checked by separate UX cases.
  98  |           if (/^UI-ADM-(CAT|MAP|TIL)-00[35]$/.test(app.caseId)) {
  99  |             if (app.kind === 'Category') data.label = 'Changed Category';
  100 |             if (app.kind === 'Import Map') data.path = 'https://assets.example.test/v2.js';
  101 |             if (app.kind === 'Tile') data.title = 'Changed Tile';
  102 |           }
  103 |           if (body.mode === 'checker') data.active = true;
  104 |           if (body.mode === 'deactivate') data.active = false;
  105 |           if (operation === 'create') app.rows = [data, ...app.rows];
  106 |           else app.rows = app.rows.map(row => row[identity[app.kind]] === data[identity[app.kind]] ? data : row);
  107 |         }
  108 |       }
  109 |       await route.fulfill({ status: 200, json: { data } });
  110 |     });
  111 |     const initial = { ...workspace(this.workspaceLabel || this.kind), containers: [{ id: 'ADMIN-CONTAINER', container: '@fm/base',
  112 |       module: `/${endpoint[this.kind]}`, tile: '', title: this.kind, emailSupport: 'support@example.test', panelId: '', tabId: '', parameters: {} }] };
  113 |     await this.page.addInitScript(initial => localStorage.setItem('SET_WORKSPACES', JSON.stringify([initial])), initial);
  114 |     const superUser = ['UI-ADM-FLD-004', 'UI-RISK-004'].includes(this.caseId);
  115 |     for (const name of ['login', 'validate', 'extend']) await this.page.route(`**/api/auth/v2/sso/${name}`, route => route.fulfill({ status: 200,
  116 |       headers: { 'content-type': 'application/json', 'single-ui-authorization': accessToken },
  117 |       json: { userInfo: JSON.stringify({ sub: this.principal || (superUser ? 'UI-SUPER-01' : 'UI-ADMIN-01'), fullName: 'Audit Admin', auth_time: Math.floor(Date.now() / 1000) }),
  118 |         entitlementsToken: accessToken.replace('Bearer ', ''),
  119 |         drawers: [{ id: 1, label: 'Administration fixture', tiles: [{ ...initial.containers[0],
  120 |           isTemplate: true, imageDarkTheme: '', entity: ['FMO PORTAL ADMIN'], subject: 'ADMIN_UI' }] }],
  121 |         entities: [{ id: 1, name: 'FMO PORTAL ADMIN', applicationName: 'Portal', roleId: 1,
  122 |           roleName: superUser ? 'SUPER_USER' : 'TEST_OWNER', subjects: [] }], result: true } }));
  123 |     await this.page.route('**/api/auth/v2/sso/refreshtoken', route => route.fulfill({ status: 200,
  124 |       headers: { 'single-ui-refresh': accessToken }, json: {} }));
  125 |     const login = await openLogin(this.page);
  126 |     await login.fillUsername(credentials.username); await login.fillPassword(credentials.password); await login.clickSignInButton();
  127 |     await this.portal.expectVisible();
  128 |   }
  129 | 
  130 |   async open(): Promise<void> {
> 131 |     await expect(this.grid).toBeVisible();
      |                             ^ Error: expect(locator).toBeVisible() failed
  132 |     if (this.kind === 'Tile' && !/^UI-ADM-SEL-00[1-7]$/.test(this.caseId)) await this.selectCategory();
  133 |     this.beforeRows = await this.grid.locator('[data-id]').count();
  134 |     this.beforeValues = await this.row().textContent().then(value => value ?? '').catch(() => '');
  135 |     if (/-012$/.test(this.caseId) && !this.caseId.includes('-SEL-')) {
  136 |       await this.action('Edit').click(); await this.field(this.kind === 'Category' ? 'Category Label' : this.kind === 'Import Map' ? 'Module Name' : 'Tile Name').fill(`Changed ${this.kind}`);
  137 |     }
  138 |     if (/UI-ADM-FLD-00[5-8]/.test(this.caseId) || /^UI-ADM-SEL-0(?:09|10|11|12|13|14)$/.test(this.caseId)) {
  139 |       if (['UI-ADM-FLD-005', 'UI-ADM-FLD-007', 'UI-ADM-SEL-009'].includes(this.caseId)) await this.panel.getByRole('button', { name: `Create New ${this.kind}`, exact: true }).click();
  140 |       else await this.action('Edit').click();
  141 |       if (this.caseId === 'UI-ADM-FLD-005') { await this.field('Module Name').fill('@fm/test'); await this.field('Path').fill('https://assets.example.test/v1.js'); }
  142 |     }
  143 |     if (this.caseId === 'UI-ADM-GRD-005') await this.action('Audit').click();
  144 |     if (this.caseId === 'UI-ADM-GRD-007') { await this.panel.getByRole('button', { name: 'Create New Category', exact: true }).click(); await this.footerButton('Create').click(); }
  145 |   }
  146 | 
  147 |   async selectCategory(name = 'Fixture Category'): Promise<void> {
  148 |     await this.category.click(); await this.page.getByRole('option', { name, exact: true }).click();
  149 |     await expect(this.category).toHaveValue(name);
  150 |   }
  151 | 
  152 |   async reveal(field: string, id?: string): Promise<Locator> {
  153 |     const selector = id ? this.row(id).locator(`[data-field="${field}"]`) : this.grid.getByRole('columnheader').filter({ has: this.page.locator(`[data-field="${field}"]`) });
  154 |     const target = id ? selector : this.grid.locator(`[role="columnheader"][data-field="${field}"]`);
  155 |     const scroller = this.grid.locator('.MuiDataGrid-virtualScroller');
  156 |     await scroller.evaluate(node => { node.scrollLeft = 0; });
  157 |     for (let index = 0; index < 25; index++) {
  158 |       if (await target.count() && await target.isVisible()) { await target.scrollIntoViewIfNeeded(); return target; }
  159 |       await scroller.evaluate(node => { node.scrollLeft += 500; });
  160 |       await this.page.waitForTimeout(20);
  161 |     }
  162 |     await expect(target).toBeVisible(); return target;
  163 |   }
  164 | }
  165 | 
```