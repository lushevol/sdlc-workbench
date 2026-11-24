# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: catalog-profile-expanded.spec.ts >> UI-CAT-008 launch Indonesia once
- Location: e2e/audit-specs/catalog-profile-expanded.spec.ts:101:3

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator: getByRole('tabpanel').visible().getByTestId('fixture-tile-route')
Expected: "/fixture-existing"
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toHaveText" getByRole('tabpanel').visible().getByTestId('fixture-tile-route') with timeout 5000ms
  - waiting for getByRole('tabpanel').visible().getByTestId('fixture-tile-route')

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 05:16 UTC
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
  1   | import { expect, type Locator, type Page } from '@playwright/test';
  2   | import { PortalPage } from '../pages/portal.page.js';
  3   | import { blockExternal, credentials, fixtureAccess, localBase, localPrefix, openLogin, workspace } from './local-app.js';
  4   | 
  5   | export type FixtureTile = {
  6   |   title: string; subtitle?: string; entryName?: string | null; tile: string;
  7   |   container: string; module: string; emailSupport: string;
  8   |   imageDarkTheme: string; imageLightTheme?: string; disabled?: boolean;
  9   |   entity: string[]; subject: string; parameters?: Record<string, unknown>;
  10  | };
  11  | export type FixtureEntity = {
  12  |   id: number; name: string; applicationName: string; roleId: number; roleName: string;
  13  |   subjects: { id: number; name: string; actions: { id: number; entitlementId: number; name: string }[] }[];
  14  | };
  15  | export type CatalogFixture = {
  16  |   drawers?: { id: number; label: string; tiles: FixtureTile[] }[];
  17  |   entities?: FixtureEntity[]; user?: Record<string, unknown>; occupied?: boolean;
  18  | };
  19  | 
  20  | export const fixtureTile = (overrides: Partial<FixtureTile> = {}): FixtureTile => ({
  21  |   title: 'Test Tile', subtitle: 'Demo', entryName: 'Global', tile: '/tile-global',
  22  |   container: '@fm/test_container', module: '/test', emailSupport: 'support@example.test',
  23  |   imageDarkTheme: 'audit-fixtures/dark.svg', imageLightTheme: 'audit-fixtures/light.svg',
  24  |   entity: ['TEST_ENTITY'], subject: 'TEST_SUBJECT', ...overrides,
  25  | });
  26  | export const fixtureCategory = (tiles: FixtureTile[], label = 'Fixture Category', id = 101) => ({ id, label, tiles });
  27  | export const fixtureEntity = (name = 'TEST_ENTITY', applicationName = 'Test App', id = 1): FixtureEntity => ({
  28  |   id, name, applicationName, roleId: id, roleName: 'Viewer',
  29  |   subjects: [{ id, name: 'TEST_SUBJECT', actions: [{ id, entitlementId: id, name: 'READ' }] }],
  30  | });
  31  | 
  32  | // The actual shell imports this controlled component through its normal SystemJS boundary.
  33  | // Its route, parameters, and counter are fixture observations, not business application output.
  34  | const containerModule = `System.register(['react'], function (exports) {
  35  |   var React;
  36  |   return { setters: [function (value) { React = value.default || value; }], execute: function () {
  37  |     exports('default', function AuditFixtureContainer(props) {
  38  |       var counter = React.useState(0);
  39  |       var parameters = props.parameters || {};
  40  |       return React.createElement('section', { 'data-testid': 'audit-controlled-container' },
  41  |         React.createElement('h2', null, 'Controlled test container'),
  42  |         React.createElement('p', { 'data-testid': 'fixture-tile-route' }, props.tile),
  43  |         React.createElement('pre', { 'data-testid': 'fixture-parameters' }, JSON.stringify(parameters)),
  44  |         Object.keys(parameters).map(function (key) {
  45  |           return React.createElement('p', { key: key, 'data-testid': 'fixture-parameter-' + key },
  46  |             key + ': ' + JSON.stringify(parameters[key]));
  47  |         }),
  48  |         React.createElement('button', { onClick: function () { counter[1](counter[0] + 1); } }, 'Counter'),
  49  |         React.createElement('output', null, String(counter[0])));
  50  |     });
  51  |   }};
  52  | });`;
  53  | 
  54  | export class CatalogApp {
  55  |   readonly portal: PortalPage;
  56  |   readonly drawer: Locator;
  57  |   readonly newTile: Locator;
  58  |   readonly profileIdentity: Locator;
  59  |   readonly functionalProfile: Locator;
  60  |   readonly entitlementProfile: Locator;
  61  | 
  62  |   constructor(readonly page: Page, readonly fixture: CatalogFixture) {
  63  |     this.portal = new PortalPage(page, localPrefix);
  64  |     this.drawer = page.getByTestId(`${localPrefix}_drawer`);
  65  |     this.newTile = page.getByTestId(`${localPrefix}_appBar`).getByTestId(`${localPrefix}_new_tile`);
  66  |     this.profileIdentity = page.getByTestId('entitlement-profile-label-box');
  67  |     this.functionalProfile = page.getByTestId('functional-profile-label-card');
  68  |     this.entitlementProfile = page.getByTestId('entitlement-profile-label');
  69  |   }
  70  | 
  71  |   card(subtitle = 'Demo', title = 'Test Tile'): Locator {
  72  |     return this.drawer.getByTestId(`${localPrefix}_tile`).filter({
  73  |       has: this.page.locator('section').filter({ hasText: new RegExp(`^${title}${subtitle}$`) }),
  74  |     });
  75  |   }
  76  | 
  77  |   entry(name: string, subtitle = 'Demo'): Locator {
  78  |     // MUI's image alt contributes to the accessible name; visible text is checked separately.
  79  |     return this.card(subtitle).getByRole('button').filter({ hasText: new RegExp(`^${name}$`) });
  80  |   }
  81  | 
  82  |   selectedPanel(): Locator { return this.page.getByRole('tabpanel').filter({ visible: true }); }
  83  | 
  84  |   async openDrawer(): Promise<void> {
  85  |     await expect(this.newTile).toHaveCount(1);
  86  |     await this.newTile.click();
  87  |     await expect(this.drawer.getByText('Tile Options', { exact: true })).toBeVisible();
  88  |   }
  89  | 
  90  |   async clickCard(): Promise<void> {
  91  |     await expect(this.card()).toHaveCount(1);
  92  |     await this.card().locator('main > section').first().click();
  93  |   }
  94  | 
  95  |   async expectRoute(route: string): Promise<void> {
> 96  |     await expect(this.selectedPanel().getByTestId('fixture-tile-route')).toHaveText(route);
      |                                                                          ^ Error: expect(locator).toHaveText(expected) failed
  97  |   }
  98  | 
  99  |   async openProfile(): Promise<void> {
  100 |     await this.portal.clickProfileMenuItem();
  101 |     await expect(this.page.getByText('User Profile', { exact: true })).toBeVisible();
  102 |     await expect(this.profileIdentity).toBeVisible();
  103 |   }
  104 | }
  105 | 
  106 | export async function loginCatalog(page: Page, fixture: CatalogFixture = {}): Promise<CatalogApp> {
  107 |   await blockExternal(page);
  108 |   await page.route('**/importmap*.json', async route => {
  109 |     const response = await route.fetch();
  110 |     const map = await response.json();
  111 |     await route.fulfill({ response, json: { ...map, imports: { ...map.imports,
  112 |       '@fm/test_container': `${localBase}/audit-fixtures/test-container.js` } } });
  113 |   });
  114 |   await page.route('**/audit-fixtures/test-container.js', route => route.fulfill({
  115 |     status: 200, contentType: 'application/javascript', body: containerModule,
  116 |   }));
  117 |   await page.route('**/audit-fixtures/*.svg', route => route.fulfill({ status: 200, contentType: 'image/svg+xml',
  118 |     body: `<svg xmlns="http://www.w3.org/2000/svg" width="240" height="120"><rect width="240" height="120" fill="${route.request().url().includes('light') ? '#d9f2ff' : '#173f5f'}"/><text x="16" y="60" fill="${route.request().url().includes('light') ? '#123' : '#fff'}">Controlled tile image</text></svg>`,
  119 |   }));
  120 |   const initial = { ...workspace(), containers: fixture.occupied ? [{ id: 'INITIAL-CONTAINER',
  121 |     container: '@fm/test_container', module: '/test', tile: '/fixture-existing', title: 'Initial fixture',
  122 |     emailSupport: 'support@example.test', panelId: '', tabId: '', parameters: {} }] : [] };
  123 |   await page.addInitScript(initial => {
  124 |     localStorage.setItem('SET_WORKSPACES', JSON.stringify([initial]));
  125 |     localStorage.setItem('SET_THEME', 'dark');
  126 |   }, initial);
  127 |   const entities = fixture.entities ?? [fixtureEntity()];
  128 |   const entitlements = Object.fromEntries(entities.map(entity => [`${entity.name}:${entity.roleName}`,
  129 |     Object.fromEntries(entity.subjects.map(subject => [subject.name, subject.actions.map(action => action.name)]))]));
  130 |   const user = { sub: 'UI-USER-01', fullName: 'Audit User A', auth_time: Math.floor(Date.now() / 1000),
  131 |     entitlements, ...fixture.user };
  132 |   const response = { userInfo: JSON.stringify(user), entities,
  133 |     drawers: fixture.drawers ?? [fixtureCategory([fixtureTile()])], result: true };
  134 |   for (const endpoint of ['login', 'validate']) await page.route(`**/api/auth/v2/sso/${endpoint}`, route =>
  135 |     route.fulfill({ status: 200, headers: { 'content-type': 'application/json', 'single-ui-authorization': fixtureAccess() },
  136 |       body: JSON.stringify(response) }));
  137 |   const login = await openLogin(page);
  138 |   await login.fillUsername(credentials.username);
  139 |   await login.fillPassword(credentials.password);
  140 |   await login.clickSignInButton();
  141 |   const app = new CatalogApp(page, fixture);
  142 |   await app.portal.expectVisible();
  143 |   if (fixture.occupied) await app.expectRoute('/fixture-existing');
  144 |   return app;
  145 | }
  146 | 
```