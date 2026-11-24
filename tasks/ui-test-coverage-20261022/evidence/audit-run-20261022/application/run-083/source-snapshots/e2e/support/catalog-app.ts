import { expect, type Locator, type Page } from '@playwright/test';
import { PortalPage } from '../pages/portal.page.js';
import { blockExternal, credentials, fixtureAccess, localBase, localPrefix, openLogin, workspace } from './local-app.js';

export type FixtureTile = {
  title: string; subtitle?: string; entryName?: string | null; tile: string;
  container: string; module: string; emailSupport: string;
  imageDarkTheme: string; imageLightTheme?: string; disabled?: boolean; isTemplate?: boolean;
  entity: string[]; subject: string; parameters?: Record<string, unknown>;
};
export type FixtureEntity = {
  id: number; name: string; applicationName: string; roleId: number; roleName: string;
  subjects: { id: number; name: string; actions: { id: number; entitlementId: number; name: string }[] }[];
};
export type CatalogFixture = {
  drawers?: { id: number; label: string; tiles: FixtureTile[] }[];
  entities?: FixtureEntity[]; user?: Record<string, unknown>; occupied?: boolean;
  workspaces?: FixtureWorkspace[];
  includeEntitlementsToken?: boolean;
};
export type FixtureContainer = {
  id: string; container: string; module: string; tile: string; title: string;
  emailSupport: string; panelId: string; tabId: string; entryName?: string | null;
  parameters?: Record<string, unknown>;
};
export type FixtureWorkspace = { id: string; label: string; isActive: boolean; containers: FixtureContainer[] };
export const fixtureContainer = (parameters: Record<string, unknown> = {}, entryName = 'Global'): FixtureContainer => ({
  id: 'CONTROLLED-CONTAINER', container: '@fm/test_container', module: '/test', tile: '/tile-global',
  title: 'Test Tile Demo', emailSupport: 'support@example.test', panelId: '', tabId: '', entryName, parameters,
});

export const fixtureTile = (overrides: Partial<FixtureTile> = {}): FixtureTile => ({
  title: 'Test Tile', subtitle: 'Demo', entryName: 'Global', tile: '/tile-global',
  container: '@fm/test_container', module: '/test', emailSupport: 'support@example.test',
  imageDarkTheme: 'audit-fixtures/dark.svg', imageLightTheme: 'audit-fixtures/light.svg',
  entity: ['TEST_ENTITY'], subject: 'TEST_SUBJECT', ...overrides,
});
export const fixtureCategory = (tiles: FixtureTile[], label = 'Fixture Category', id = 101) => ({ id, label, tiles });
export const fixtureEntity = (name = 'TEST_ENTITY', applicationName = 'Test App', id = 1): FixtureEntity => ({
  id, name, applicationName, roleId: id, roleName: 'Viewer',
  subjects: [{ id, name: 'TEST_SUBJECT', actions: [{ id, entitlementId: id, name: 'READ' }] }],
});

// The actual shell imports this controlled component through its normal SystemJS boundary.
// Its route, parameters, and counter are fixture observations, not business application output.
const containerModule = `System.register(['react', '@fm/base'], function (exports) {
  var React, base;
  return { setters: [function (value) { React = value.default || value; }, function (value) { base = value; }], execute: function () {
    exports('default', function AuditFixtureContainer(props) {
      var counter = React.useState(0);
      var version = React.useState(1);
      var parameters = props.parameters || {};
      var dispatcher = base.Dispatcher.default();
      React.useEffect(function () {
        if (parameters.registerRefresh) dispatcher.registerRefreshTab(props.tabId, function () { version[1](2); });
      }, []);
      return React.createElement('section', { 'data-testid': 'audit-controlled-container' },
        React.createElement('h2', null, 'Controlled test container'),
        React.createElement('p', { 'data-testid': 'fixture-tile-route' }, props.tile),
        React.createElement('p', { 'data-testid': 'fixture-marker' }, parameters.marker || ''),
        React.createElement('p', { 'data-testid': 'fixture-version' }, 'Version ' + version[0]),
        React.createElement('pre', { 'data-testid': 'fixture-parameters' }, JSON.stringify(parameters)),
        Object.keys(parameters).map(function (key) {
          return React.createElement('p', { key: key, 'data-testid': 'fixture-parameter-' + key },
            key + ': ' + JSON.stringify(parameters[key]));
        }),
        React.createElement('button', { onClick: function () { counter[1](counter[0] + 1); } }, 'Counter'),
        React.createElement('output', null, String(counter[0])));
    });
  }};
});`;

export class CatalogApp {
  readonly portal: PortalPage;
  readonly drawer: Locator;
  readonly newTile: Locator;
  readonly profileIdentity: Locator;
  readonly functionalProfile: Locator;
  readonly entitlementProfile: Locator;

  constructor(readonly page: Page, readonly fixture: CatalogFixture) {
    this.portal = new PortalPage(page, localPrefix);
    this.drawer = page.getByTestId(`${localPrefix}_drawer`);
    this.newTile = page.getByTestId(`${localPrefix}_appBar`).getByTestId(`${localPrefix}_new_tile`);
    this.profileIdentity = page.getByTestId('entitlement-profile-label-box');
    this.functionalProfile = page.getByTestId('functional-profile-label-card');
    this.entitlementProfile = page.getByTestId('entitlement-profile-label');
  }

  card(subtitle = 'Demo', title = 'Test Tile'): Locator {
    return this.drawer.getByTestId(`${localPrefix}_tile`).filter({
      has: this.page.locator('section').filter({ hasText: new RegExp(`^${title}${subtitle}$`) }),
    });
  }

  entry(name: string, subtitle = 'Demo'): Locator {
    // MUI's image alt contributes to the accessible name; visible text is checked separately.
    return this.card(subtitle).getByRole('button').filter({ hasText: new RegExp(`^${name}$`) });
  }

  selectedPanel(): Locator { return this.page.getByRole('tabpanel').filter({ visible: true }); }
  allWorkspaceTabs(): Locator {
    return this.page.getByRole('tablist', { name: 'workspaces', exact: true, includeHidden: true })
      .getByRole('tab', { includeHidden: true });
  }

  async openDrawer(): Promise<void> {
    await expect(this.newTile).toHaveCount(1);
    await this.newTile.click();
    await expect(this.drawer.getByText('Tile Options', { exact: true })).toBeVisible();
  }

  async clickCard(): Promise<void> {
    await expect(this.card()).toHaveCount(1);
    await this.card().locator('main > section').first().click();
  }

  async expectRoute(route: string): Promise<void> {
    await expect(this.selectedPanel().getByTestId('fixture-tile-route')).toHaveText(route);
  }

  async openProfile(): Promise<void> {
    await this.portal.clickProfileMenuItem();
    await expect(this.page.getByText('User Profile', { exact: true })).toBeVisible();
    await expect(this.profileIdentity).toBeVisible();
  }
}

export async function loginCatalog(page: Page, fixture: CatalogFixture = {}): Promise<CatalogApp> {
  await blockExternal(page);
  await page.route('**/importmap*.json', async route => {
    const response = await route.fetch();
    const map = await response.json();
    await route.fulfill({ response, json: { ...map, imports: { ...map.imports,
      '@fm/test_container': `${localBase}/audit-fixtures/test-container.js` } } });
  });
  await page.route('**/audit-fixtures/test-container.js', route => route.fulfill({
    status: 200, contentType: 'application/javascript', body: containerModule,
  }));
  await page.route('**/audit-fixtures/*.svg', route => route.fulfill({ status: 200, contentType: 'image/svg+xml',
    body: `<svg xmlns="http://www.w3.org/2000/svg" width="240" height="120"><rect width="240" height="120" fill="${route.request().url().includes('light') ? '#d9f2ff' : '#173f5f'}"/><text x="16" y="60" fill="${route.request().url().includes('light') ? '#123' : '#fff'}">Controlled tile image</text></svg>`,
  }));
  const initial = { ...workspace(), containers: fixture.occupied ? [{ id: 'INITIAL-CONTAINER',
    container: '@fm/test_container', module: '/test', tile: '/tile-global', title: 'Initial fixture',
    emailSupport: 'support@example.test', panelId: '', tabId: '', parameters: {} }] : [] };
  await page.addInitScript(initial => {
    if (!localStorage.getItem('UI_CATALOG_INITIALIZED')) {
      localStorage.setItem('SET_WORKSPACES', JSON.stringify(initial));
      localStorage.setItem('SET_THEME', 'dark');
      localStorage.setItem('UI_CATALOG_INITIALIZED', 'true');
    }
  }, fixture.workspaces ?? [initial]);
  const entities = fixture.entities ?? [fixtureEntity()];
  const entitlements = Object.fromEntries(entities.map(entity => [`${entity.name}:${entity.roleName}`,
    Object.fromEntries(entity.subjects.map(subject => [subject.name, subject.actions.map(action => action.name)]))]));
  const user = { sub: 'UI-USER-01', fullName: 'Audit User A', auth_time: Math.floor(Date.now() / 1000),
    entitlements, ...fixture.user };
  const response = { userInfo: JSON.stringify(user), entities,
    drawers: fixture.drawers ?? [fixtureCategory([fixtureTile()])], result: true,
    ...(fixture.includeEntitlementsToken ? { entitlementsToken: fixtureAccess().replace('Bearer ', '') } : {}) };
  for (const endpoint of ['login', 'validate', 'extend']) await page.route(`**/api/auth/v2/sso/${endpoint}`, route =>
    route.fulfill({ status: 200, headers: { 'content-type': 'application/json', 'single-ui-authorization': fixtureAccess() },
      body: JSON.stringify(response) }));
  const login = await openLogin(page);
  await login.fillUsername(credentials.username);
  await login.fillPassword(credentials.password);
  await login.clickSignInButton();
  const app = new CatalogApp(page, fixture);
  await app.portal.expectVisible();
  if (fixture.occupied) await app.expectRoute('/tile-global');
  return app;
}
