# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-expanded.spec.ts >> UI-ADM-TIL-001 actual administration UI with step evidence
- Location: e2e/audit-specs/admin-expanded.spec.ts:15:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByRole('tabpanel').visible().getByTestId('MicroWebUI_base_simple_table').getByRole('grid')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" getByRole('tabpanel').visible().getByTestId('MicroWebUI_base_simple_table').getByRole('grid') with timeout 5000ms
  - waiting for getByRole('tabpanel').visible().getByTestId('MicroWebUI_base_simple_table').getByRole('grid')

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 05:20 UTC
  - checkbox "Time Switch" [checked]
- button "User Profiles": A
- button "Share Feedback"
- main:
  - tablist "workspaces":
    - tab "Workspace 1" [selected]:
      - region "Workspace 1":
        - textbox "Workspace Name": Workspace 1
    - button "Add Workspace"
  - tabpanel:
    - paragraph: Start customizing your workspace
    - paragraph: find out what workspace preference options you have and how those options work.
    - button "Find tile"
```

# Test source

```ts
  12  |   'Container Record Id': 'importMapId', 'Aplication Category Record Id': 'applicationCategoryId',
  13  |   'Aplication Category': 'applicationCategory', 'Role Entities': 'ems2Entities', 'Role Subject': 'ems2Subject',
  14  |   'Filter Rule': 'filterRule', 'Email Support': 'emailSupport',
  15  | };
  16  | const identity = { Category: 'applicationCategoryId', 'Import Map': 'importMapId', Tile: 'applicationTileId' };
  17  | const endpoint = { Category: 'category', 'Import Map': 'importmap', Tile: 'tile' };
  18  | export const categoryRecord = (id = 101, label = 'Fixture Category'): Row => ({ applicationCategoryId: id, label,
  19  |   active: false, ems2Role: 'TEST_OWNER', orderNo: 7, createdAt: '2026-10-21T00:05:00Z',
  20  |   updatedAt: '2026-10-22T00:05:00Z', createdBy: 'UI-ADMIN-01', updatedBy: 'UI-ADMIN-01' });
  21  | export const importMapRecord = (): Row => ({ ...categoryRecord(), importMapId: 101, keyName: '@fm/test', path: 'https://assets.example.test/v1.js' });
  22  | export const tileRecord = (): Row => ({ ...categoryRecord(), applicationTileId: 101, title: 'Fixture Tile', subtitle: 'Demo',
  23  |   applicationCategory: categoryRecord(81), applicationCategoryId: 81, importMap: { ...importMapRecord(), importMapId: 71 },
  24  |   importMapId: 71, module: '/test', tile: '/test-entry', entryName: 'Global', ems2Subject: 'TEST_SUBJECT',
  25  |   ems2Entities: 'TEST_ENTITY', emailSupport: 'support@example.test', template: false,
  26  |   imageDarkTheme: 'darkIcons/icon01.svg', imageLightTheme: 'lightIcons/icon01.svg', filterRule: '' });
  27  | 
  28  | export class AdminApp {
  29  |   readonly portal: PortalPage;
  30  |   readonly panel: Locator;
  31  |   readonly table: Locator;
  32  |   readonly grid: Locator;
  33  |   readonly category: Locator;
  34  |   readonly requests: { endpoint: string; body: Row }[] = [];
  35  |   rows: Row[];
  36  |   beforeRows = 1;
  37  |   beforeValues = '';
  38  |   refreshCount = 0;
  39  | 
  40  |   constructor(readonly page: Page, readonly kind: AdminKind, readonly caseId: string) {
  41  |     this.portal = new PortalPage(page, localPrefix);
  42  |     this.panel = page.getByRole('tabpanel').filter({ visible: true });
  43  |     this.table = this.panel.getByTestId(`${localPrefix}_simple_table`);
  44  |     this.grid = this.table.getByRole('grid');
  45  |     this.category = this.panel.getByRole('combobox', { name: 'Application Category', exact: true });
  46  |     this.rows = [kind === 'Category' ? categoryRecord() : kind === 'Import Map' ? importMapRecord() : tileRecord()];
  47  |     if (/-00[7]$|-010$|-011$/.test(caseId) && !caseId.includes('-SEL-')) this.rows[0].active = true;
  48  |     if (caseId === 'UI-ADM-SEL-006' || caseId === 'UI-ADM-SEL-007' || caseId === 'UI-ADM-SEL-015') this.rows[0].title = 'Tile A';
  49  |     if (caseId === 'UI-ADM-SEL-012') this.rows[0].template = true;
  50  |     const rowCount = caseId === 'UI-ADM-GRD-002' ? 75 : caseId === 'UI-ADM-GRD-004' ? 105
  51  |       : ['UI-ADM-GRD-001', 'UI-ADM-GRD-003'].includes(caseId) ? 25 : caseId === 'UI-ADM-GRD-005' ? 2 : 1;
  52  |     if (kind === 'Category' && rowCount > 1) this.rows = Array.from({ length: rowCount }, (_, i) => categoryRecord(101 + i, `Fixture Category ${101 + i}`));
  53  |   }
  54  | 
  55  |   dialog(): Locator { return this.panel.getByRole('dialog').filter({ has: this.page.getByText(/^(?:new|edit|verify|deactivate) ID:/) }); }
  56  |   auditDialog(): Locator { return this.panel.getByRole('dialog', { name: 'Audit', exact: true }); }
  57  |   row(id = '101'): Locator { return this.grid.locator(`[data-id="${id}"]`); }
  58  |   action(name: string, id = '101'): Locator { return this.row(id).getByRole('menuitem', { name, exact: true }); }
  59  |   footerButton(name: string): Locator { return this.dialog().locator('button').filter({ hasText: new RegExp(`^${name}$`) }); }
  60  |   field(name: string, role = 'textbox'): Locator { return this.dialog().getByRole(role as 'textbox', { name, exact: true }); }
  61  | 
  62  |   async setup(): Promise<void> {
  63  |     await blockExternal(this.page);
  64  |     const categories = [categoryRecord(81), categoryRecord(82, 'Other Category')];
  65  |     const oneCategory = this.caseId === 'UI-ADM-SEL-003';
  66  |     const app = this;
  67  |     await this.page.route('**/api/auth/v1/fmo/admin/**', async route => {
  68  |       const name = new URL(route.request().url()).pathname.split('/').slice(-2).join('/');
  69  |       const body = route.request().postDataJSON() ?? {};
  70  |       app.requests.push({ endpoint: name, body });
  71  |       const [resource, operation] = name.split('/');
  72  |       let data: any;
  73  |       if (operation === 'data') {
  74  |         if (resource === 'category' && app.kind === 'Tile') data = oneCategory ? categories.slice(0, 1) : categories;
  75  |         else if (resource === 'importmap' && app.kind === 'Tile') data = [{ ...importMapRecord(), importMapId: 71 }];
  76  |         else data = app.rows;
  77  |         if (app.caseId === 'UI-ADM-SEL-015' && resource === 'tile' && ++app.refreshCount > 2) data = [{ ...app.rows[0], title: 'Tile B' }];
  78  |       } else if (operation === 'audit') {
  79  |         data = [9001, 9002].map(id => ({ ...app.rows[0], [identity[app.kind]]: body[identity[app.kind]],
  80  |           applicationCategoryAuditId: id, importMapAuditId: id, applicationTileAuditId: id, transactionMode: 'maker' }));
  81  |         if (app.caseId === 'UI-ADM-GRD-005') data = [data[body.applicationCategoryId === 102 ? 1 : 0]];
  82  |       } else {
  83  |         if (app.caseId === 'UI-ADM-GRD-007') { await new Promise<void>(() => {}); return; }
  84  |         if (/UI-ADM-FLD-00[5-8]/.test(app.caseId)) data = {};
  85  |         else {
  86  |           data = { ...app.rows[0], ...body, [identity[app.kind]]: operation === 'create' ? 102 : body[identity[app.kind]],
  87  |             updatedBy: 'UI-ADMIN-01' };
  88  |           if (body.mode === 'checker') data.active = true;
  89  |           if (body.mode === 'deactivate') data.active = false;
  90  |           if (operation === 'create') app.rows = [data, ...app.rows];
  91  |           else app.rows = app.rows.map(row => row[identity[app.kind]] === data[identity[app.kind]] ? data : row);
  92  |         }
  93  |       }
  94  |       await route.fulfill({ status: 200, json: { data } });
  95  |     });
  96  |     const initial = { ...workspace(this.kind), containers: [{ id: 'ADMIN-CONTAINER', container: '@fm/base',
  97  |       module: `/${endpoint[this.kind]}`, tile: '', title: this.kind, emailSupport: 'support@example.test', panelId: '', tabId: '', parameters: {} }] };
  98  |     await this.page.addInitScript(initial => localStorage.setItem('SET_WORKSPACES', JSON.stringify([initial])), initial);
  99  |     const superUser = this.caseId === 'UI-ADM-FLD-004';
  100 |     for (const name of ['login', 'validate']) await this.page.route(`**/api/auth/v2/sso/${name}`, route => route.fulfill({ status: 200,
  101 |       headers: { 'content-type': 'application/json', 'single-ui-authorization': fixtureAccess() },
  102 |       json: { userInfo: JSON.stringify({ sub: superUser ? 'UI-SUPER-01' : 'UI-ADMIN-01', fullName: 'Audit Admin', auth_time: Math.floor(Date.now() / 1000) }),
  103 |         entitlementsToken: fixtureAccess().replace('Bearer ', ''), drawers: [],
  104 |         entities: [{ id: 1, name: 'FMO PORTAL ADMIN', applicationName: 'Portal', roleId: 1,
  105 |           roleName: superUser ? 'SUPER_USER' : 'TEST_OWNER', subjects: [] }], result: true } }));
  106 |     const login = await openLogin(this.page);
  107 |     await login.fillUsername(credentials.username); await login.fillPassword(credentials.password); await login.clickSignInButton();
  108 |     await this.portal.expectVisible();
  109 |   }
  110 | 
  111 |   async open(): Promise<void> {
> 112 |     await expect(this.grid).toBeVisible();
      |                             ^ Error: expect(locator).toBeVisible() failed
  113 |     if (this.kind === 'Tile' && !/^UI-ADM-SEL-00[1-7]$/.test(this.caseId)) await this.selectCategory();
  114 |     this.beforeRows = await this.grid.locator('[data-id]').count();
  115 |     this.beforeValues = await this.row().innerText().catch(() => '');
  116 |     if (/-012$/.test(this.caseId) && !this.caseId.includes('-SEL-')) {
  117 |       await this.action('Edit').click(); await this.field(this.kind === 'Category' ? 'Category Label' : this.kind === 'Import Map' ? 'Module Name' : 'Tile Name').fill(`Changed ${this.kind}`);
  118 |     }
  119 |     if (/UI-ADM-FLD-00[5-8]/.test(this.caseId) || /^UI-ADM-SEL-0(?:09|10|11|12|13|14)$/.test(this.caseId)) {
  120 |       if (['UI-ADM-FLD-005', 'UI-ADM-FLD-007', 'UI-ADM-SEL-009'].includes(this.caseId)) await this.panel.getByRole('button', { name: `Create New ${this.kind}`, exact: true }).click();
  121 |       else await this.action('Edit').click();
  122 |       if (this.caseId === 'UI-ADM-FLD-005') { await this.field('Module Name').fill('@fm/test'); await this.field('Path').fill('https://assets.example.test/v1.js'); }
  123 |     }
  124 |     if (this.caseId === 'UI-ADM-GRD-005') await this.action('Audit').click();
  125 |     if (this.caseId === 'UI-ADM-GRD-007') { await this.panel.getByRole('button', { name: 'Create New Category', exact: true }).click(); await this.footerButton('Create').click(); }
  126 |   }
  127 | 
  128 |   async selectCategory(name = 'Fixture Category'): Promise<void> {
  129 |     await this.category.click(); await this.page.getByRole('option', { name, exact: true }).click();
  130 |     await expect(this.category).toHaveValue(name);
  131 |   }
  132 | 
  133 |   async reveal(field: string, id?: string): Promise<Locator> {
  134 |     const selector = id ? this.row(id).locator(`[data-field="${field}"]`) : this.grid.getByRole('columnheader').filter({ has: this.page.locator(`[data-field="${field}"]`) });
  135 |     const target = id ? selector : this.grid.locator(`[role="columnheader"][data-field="${field}"]`);
  136 |     const scroller = this.grid.locator('.MuiDataGrid-virtualScroller');
  137 |     await scroller.evaluate(node => { node.scrollLeft = 0; });
  138 |     for (let index = 0; index < 25; index++) {
  139 |       if (await target.count() && await target.isVisible()) { await target.scrollIntoViewIfNeeded(); return target; }
  140 |       await scroller.evaluate(node => { node.scrollLeft += 500; });
  141 |       await this.page.waitForTimeout(20);
  142 |     }
  143 |     await expect(target).toBeVisible(); return target;
  144 |   }
  145 | }
  146 | 
```