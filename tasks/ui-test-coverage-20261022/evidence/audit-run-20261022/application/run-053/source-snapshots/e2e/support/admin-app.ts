import { expect, type Locator, type Page } from '@playwright/test';
import { PortalPage } from '../pages/portal.page.js';
import { blockExternal, credentials, fixtureAccess, localPrefix, openLogin, workspace } from './local-app.js';

export type AdminKind = 'Category' | 'Import Map' | 'Tile';
type Row = Record<string, any>;
export const adminFields: Record<string, string> = {
  'Category Label': 'label', 'Module Name': 'keyName', Path: 'path', Owner: 'ems2Role', 'Verified?': 'active',
  'Created At': 'createdAt', 'Created By': 'createdBy', 'Updated At': 'updatedAt', 'Updated By': 'updatedBy',
  'Order No': 'orderNo', 'Tile Name': 'title', Description: 'subtitle', Container: 'importMap',
  'Module Path': 'module', 'Tile Path': 'tile', 'Entry Name': 'entryName', 'Is Template?': 'template',
  'Container Record Id': 'importMapId', 'Aplication Category Record Id': 'applicationCategoryId',
  'Aplication Category': 'applicationCategory', 'Role Entities': 'ems2Entities', 'Role Subject': 'ems2Subject',
  'Filter Rule': 'filterRule', 'Email Support': 'emailSupport',
};
const identity = { Category: 'applicationCategoryId', 'Import Map': 'importMapId', Tile: 'applicationTileId' };
const endpoint = { Category: 'category', 'Import Map': 'importmap', Tile: 'tile' };
export const categoryRecord = (id = 101, label = 'Fixture Category'): Row => ({ applicationCategoryId: id, label,
  active: false, ems2Role: 'TEST_OWNER', orderNo: 7, createdAt: '2026-10-21T00:05:00Z',
  updatedAt: '2026-10-22T00:05:00Z', createdBy: 'UI-ADMIN-01', updatedBy: 'UI-ADMIN-01' });
export const importMapRecord = (): Row => ({ ...categoryRecord(), importMapId: 101, keyName: '@fm/test', path: 'https://assets.example.test/v1.js' });
export const tileRecord = (): Row => ({ ...categoryRecord(), applicationTileId: 101, title: 'Fixture Tile', subtitle: 'Demo',
  applicationCategory: categoryRecord(81), applicationCategoryId: 81, importMap: { ...importMapRecord(), importMapId: 71 },
  importMapId: 71, module: '/test', tile: '/test-entry', entryName: 'Global', ems2Subject: 'TEST_SUBJECT',
  ems2Entities: 'TEST_ENTITY', emailSupport: 'support@example.test', template: false,
  imageDarkTheme: 'darkIcons/icon01.svg', imageLightTheme: 'lightIcons/icon01.svg', filterRule: '' });

export class AdminApp {
  readonly portal: PortalPage;
  readonly panel: Locator;
  readonly table: Locator;
  readonly grid: Locator;
  readonly category: Locator;
  readonly requests: { endpoint: string; body: Row }[] = [];
  rows: Row[];
  beforeRows = 1;
  beforeValues = '';
  refreshCount = 0;
  principal = '';
  workspaceLabel = '';

  constructor(readonly page: Page, readonly kind: AdminKind, readonly caseId: string) {
    this.portal = new PortalPage(page, localPrefix);
    // disablePortal dialogs remain under an aria-hidden ancestor in the current MUI implementation.
    this.panel = page.locator('[role="tabpanel"]:visible');
    this.table = this.panel.getByTestId(`${localPrefix}_simple_table`);
    this.grid = this.table.getByRole('grid', { includeHidden: true });
    this.category = this.panel.getByRole('combobox', { name: 'Application Category', exact: true });
    this.rows = [kind === 'Category' ? categoryRecord() : kind === 'Import Map' ? importMapRecord() : tileRecord()];
    if (/-00[7]$|-010$|-011$/.test(caseId) && !caseId.includes('-SEL-')) this.rows[0].active = true;
    if (caseId === 'UI-ADM-SEL-006' || caseId === 'UI-ADM-SEL-007' || caseId === 'UI-ADM-SEL-015') this.rows[0].title = 'Tile A';
    if (caseId === 'UI-ADM-SEL-012') this.rows[0].template = true;
    const rowCount = caseId === 'UI-ADM-GRD-002' ? 75 : caseId === 'UI-ADM-GRD-004' ? 105
      : ['UI-ADM-GRD-001', 'UI-ADM-GRD-003'].includes(caseId) ? 25 : caseId === 'UI-ADM-GRD-005' ? 2 : 1;
    if (kind === 'Category' && rowCount > 1) this.rows = Array.from({ length: rowCount }, (_, i) => categoryRecord(101 + i, `Fixture Category ${101 + i}`));
  }

  dialog(): Locator { return this.panel.locator('[role="dialog"]').filter({ has: this.page.getByText(/^(?:new|edit|verify|deactivate) ID:/) }); }
  auditDialog(): Locator { return this.panel.locator('[role="dialog"]').filter({ has: this.page.getByText('Audit', { exact: true }) }); }
  row(id = '101'): Locator { return this.grid.locator(`[data-id="${id}"]`); }
  action(name: string, id = '101'): Locator { return this.row(id).getByRole('menuitem', { name, exact: true }); }
  footerButton(name: string): Locator { return this.dialog().locator('button').filter({ hasText: new RegExp(`^${name}$`) }); }
  field(name: string, role = 'textbox'): Locator {
    if (name === 'Is Template?') return this.dialog().getByTestId('ModalInput-template-11').locator('[role="button"], [role="combobox"]');
    return this.dialog().getByRole(role as 'textbox', { name, exact: true, includeHidden: true });
  }

  async setup(): Promise<void> {
    await blockExternal(this.page);
    const accessToken = fixtureAccess();
    const categories = [categoryRecord(81), categoryRecord(82, 'Other Category')];
    const oneCategory = this.caseId === 'UI-ADM-SEL-003';
    const app = this;
    await this.page.route('**/api/auth/v1/fmo/admin/**', async route => {
      const name = new URL(route.request().url()).pathname.split('/').slice(-2).join('/');
      const body = route.request().postDataJSON() ?? {};
      app.requests.push({ endpoint: name, body });
      const [resource, operation] = name.split('/');
      let data: any;
      if (operation === 'data') {
        if (app.caseId === 'UI-ADM-SEL-007' && resource === 'tile' && !body.applicationCategory?.applicationCategoryId
          && app.requests.filter(request => request.endpoint === 'tile/data').length > 2) { await new Promise<void>(() => {}); return; }
        if (resource === 'category' && app.kind === 'Tile') data = oneCategory ? categories.slice(0, 1) : categories;
        else if (resource === 'importmap' && app.kind === 'Tile') data = [{ ...importMapRecord(), importMapId: 71 }];
        else data = app.rows;
        if (app.caseId === 'UI-ADM-SEL-015' && resource === 'tile' && ++app.refreshCount > 2) data = [{ ...app.rows[0], title: 'Tile B' }];
      } else if (operation === 'audit') {
        data = [9001, 9002].map(id => ({ ...app.rows[0], [identity[app.kind]]: body[identity[app.kind]],
          applicationCategoryAuditId: id, importMapAuditId: id, applicationTileAuditId: id, transactionMode: 'maker' }));
        if (app.caseId === 'UI-ADM-GRD-005') data = [data[body.applicationCategoryId === 102 ? 1 : 0]];
      } else {
        if (app.caseId === 'UI-ADM-GRD-007') { await new Promise<void>(() => {}); return; }
        if (/UI-ADM-FLD-00[5-8]/.test(app.caseId)) data = {};
        else {
          data = { ...app.rows[0], ...body, [identity[app.kind]]: operation === 'create' ? 102 : body[identity[app.kind]],
            updatedBy: 'UI-ADMIN-01' };
          // These six cases declare fixed response records. Request persistence is checked by separate UX cases.
          if (/^UI-ADM-(CAT|MAP|TIL)-00[35]$/.test(app.caseId)) {
            if (app.kind === 'Category') data.label = 'Changed Category';
            if (app.kind === 'Import Map') data.path = 'https://assets.example.test/v2.js';
            if (app.kind === 'Tile') data.title = 'Changed Tile';
          }
          if (body.mode === 'checker') data.active = true;
          if (body.mode === 'deactivate') data.active = false;
          if (operation === 'create') app.rows = [data, ...app.rows];
          else app.rows = app.rows.map(row => row[identity[app.kind]] === data[identity[app.kind]] ? data : row);
        }
      }
      await route.fulfill({ status: 200, json: { data } });
    });
    const initial = { ...workspace(this.workspaceLabel || this.kind), containers: [{ id: 'ADMIN-CONTAINER', container: '@fm/base',
      module: `/${endpoint[this.kind]}`, tile: '', title: this.kind, emailSupport: 'support@example.test', panelId: '', tabId: '', parameters: {} }] };
    await this.page.addInitScript(initial => localStorage.setItem('SET_WORKSPACES', JSON.stringify([initial])), initial);
    const superUser = ['UI-ADM-FLD-004', 'UI-RISK-004'].includes(this.caseId);
    for (const name of ['login', 'validate', 'extend']) await this.page.route(`**/api/auth/v2/sso/${name}`, route => route.fulfill({ status: 200,
      headers: { 'content-type': 'application/json', 'single-ui-authorization': accessToken },
      json: { userInfo: JSON.stringify({ sub: this.principal || (superUser ? 'UI-SUPER-01' : 'UI-ADMIN-01'), fullName: 'Audit Admin', auth_time: Math.floor(Date.now() / 1000) }),
        entitlementsToken: accessToken.replace('Bearer ', ''),
        drawers: [{ id: 1, label: 'Administration fixture', tiles: [{ ...initial.containers[0],
          isTemplate: true, imageDarkTheme: '', entity: ['FMO PORTAL ADMIN'], subject: 'ADMIN_UI' }] }],
        entities: [{ id: 1, name: 'FMO PORTAL ADMIN', applicationName: 'Portal', roleId: 1,
          roleName: superUser ? 'SUPER_USER' : 'TEST_OWNER', subjects: [] }], result: true } }));
    await this.page.route('**/api/auth/v2/sso/refreshtoken', route => route.fulfill({ status: 200,
      headers: { 'single-ui-refresh': accessToken }, json: {} }));
    const login = await openLogin(this.page);
    await login.fillUsername(credentials.username); await login.fillPassword(credentials.password); await login.clickSignInButton();
    await this.portal.expectVisible();
  }

  async open(): Promise<void> {
    await expect(this.grid).toBeVisible();
    if (this.kind === 'Tile' && !/^UI-ADM-SEL-00[1-7]$/.test(this.caseId)) await this.selectCategory();
    this.beforeRows = await this.grid.locator('[data-id]').count();
    this.beforeValues = await this.row().textContent().then(value => value ?? '').catch(() => '');
    if (/-012$/.test(this.caseId) && !this.caseId.includes('-SEL-')) {
      await this.action('Edit').click(); await this.field(this.kind === 'Category' ? 'Category Label' : this.kind === 'Import Map' ? 'Module Name' : 'Tile Name').fill(`Changed ${this.kind}`);
    }
    if (/UI-ADM-FLD-00[5-8]/.test(this.caseId) || /^UI-ADM-SEL-0(?:09|10|11|12|13|14)$/.test(this.caseId)) {
      if (['UI-ADM-FLD-005', 'UI-ADM-FLD-007', 'UI-ADM-SEL-009'].includes(this.caseId)) await this.panel.getByRole('button', { name: `Create New ${this.kind}`, exact: true }).click();
      else await this.action('Edit').click();
      if (this.caseId === 'UI-ADM-FLD-005') { await this.field('Module Name').fill('@fm/test'); await this.field('Path').fill('https://assets.example.test/v1.js'); }
    }
    if (this.caseId === 'UI-ADM-GRD-005') await this.action('Audit').click();
    if (this.caseId === 'UI-ADM-GRD-007') { await this.panel.getByRole('button', { name: 'Create New Category', exact: true }).click(); await this.footerButton('Create').click(); }
  }

  async selectCategory(name = 'Fixture Category'): Promise<void> {
    await this.category.click(); await this.page.getByRole('option', { name, exact: true }).click();
    await expect(this.category).toHaveValue(name);
  }

  async reveal(field: string, id?: string): Promise<Locator> {
    const selector = id ? this.row(id).locator(`[data-field="${field}"]`) : this.grid.getByRole('columnheader').filter({ has: this.page.locator(`[data-field="${field}"]`) });
    const target = id ? selector : this.grid.locator(`[role="columnheader"][data-field="${field}"]`);
    const scroller = this.grid.locator('.MuiDataGrid-virtualScroller');
    await scroller.evaluate(node => { node.scrollLeft = 0; });
    for (let index = 0; index < 25; index++) {
      if (await target.count() && await target.isVisible()) { await target.scrollIntoViewIfNeeded(); return target; }
      await scroller.evaluate(node => { node.scrollLeft += 500; });
      await this.page.waitForTimeout(20);
    }
    await expect(target).toBeVisible(); return target;
  }
}
