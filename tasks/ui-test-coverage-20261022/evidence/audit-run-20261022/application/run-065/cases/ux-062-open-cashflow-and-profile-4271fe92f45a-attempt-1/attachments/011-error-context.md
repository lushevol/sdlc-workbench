# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: browser-compatibility.spec.ts >> UX-062 webkit >> UX-062 open Cashflow and profile
- Location: e2e/audit-specs/browser-compatibility.spec.ts:21:3

# Error details

```
Error: expect(locator).toHaveValue(expected) failed

Locator:  getByTestId('MicroWebUI_base_home').getByRole('tablist', { name: 'workspaces', exact: true }).getByRole('tab', { selected: true }).getByRole('textbox')
Expected: "Cashflow"
Received: "Cashflow "
Timeout:  5000ms

Call log:
  - Expect "toHaveValue" getByTestId('MicroWebUI_base_home').getByRole('tablist', { name: 'workspaces', exact: true }).getByRole('tab', { selected: true }).getByRole('textbox') with timeout 5000ms
  - waiting for getByTestId('MicroWebUI_base_home').getByRole('tablist', { name: 'workspaces', exact: true }).getByRole('tab', { selected: true }).getByRole('textbox')
    14 × locator resolved to <input type="text" id="edit-W1" value="Cashflow " aria-invalid="false" aria-label="Workspace Name" class="MuiInputBase-input MuiInput-input MuiInputBase-inputSizeSmall css-4zzs6-MuiInputBase-input-MuiInput-input"/>
       - unexpected value "Cashflow "

```

```yaml
- textbox "Workspace Name": Cashflow
```

# Test source

```ts
  1  | import { test, expect } from '../support/audit-fixture.js';
  2  | import { LoginPage } from '../pages/login.page.js';
  3  | import { PortalPage } from '../pages/portal.page.js';
  4  | import { blockExternal, fixtureAccess, localBase, localPrefix, openLogin, workspace } from '../support/local-app.js';
  5  | 
  6  | const selectedBrowser = process.env.E2E_COMPAT_BROWSER ?? (process.env.E2E_BROWSER === 'msedge' ? 'msedge' : 'chromium');
  7  | if (!['chromium', 'msedge', 'firefox', 'webkit'].includes(selectedBrowser)) {
  8  |  throw new Error('E2E_COMPAT_BROWSER must be chromium, msedge, firefox, or webkit.');
  9  | }
  10 | const browser = selectedBrowser as 'chromium' | 'msedge' | 'firefox' | 'webkit';
  11 | const browserName = browser === 'msedge' ? 'chromium' : browser;
  12 | const id = {chromium:'UX-059',msedge:'UX-060',firefox:'UX-061',webkit:'UX-062'}[browser];
  13 | const distribution = browser === 'msedge' ? 'Installed Microsoft Edge' : `Playwright ${browser} automation build`;
  14 | test.use({ browserName,
  15 |  launchOptions:{headless:process.env.E2E_HEADED!=='1',channel:browserName==='chromium'?browser:undefined,
  16 |   chromiumSandbox:browserName==='chromium'?true:undefined} });
  17 | {
  18 |  test.describe(`${id} ${browser}`, () => {
  19 |   test.use({ auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',
  20 |    auditFixture:`Actual React shell in ${distribution}; controlled accepted identity and Cashflow SystemJS module. Real identity and business tenant results remain unverified. Firefox and WebKit use Playwright automation builds. WebKit execution does not establish Safari product compatibility.` });
  21 |   test(`${id} open Cashflow and profile`, async({page,audit})=>{
  22 |    await audit.defineCase(id);let login:LoginPage;const portal=new PortalPage(page,localPrefix);
  23 |    const drawer=page.getByTestId(`${localPrefix}_drawer`);
  24 |    await audit.step(1,async()=>{
  25 |     const state=await page.context().storageState();expect(state.origins).toHaveLength(0);expect(state.cookies).toHaveLength(0);
  26 |     await blockExternal(page);await page.routeWebSocket('**/*',socket=>socket.close());
  27 |     await page.addInitScript(value=>localStorage.setItem('SET_WORKSPACES',JSON.stringify([value])),workspace('Home','W1'));
  28 |     await page.route('**/importmap*.json',async route=>{const response=await route.fetch();const map=await response.json();await route.fulfill({response,json:{...map,imports:{...map.imports,'@fm/audit_cashflow':`${localBase}/audit-cashflow.js`}}});});
  29 |     await page.route('**/audit-cashflow.js',route=>route.fulfill({contentType:'application/javascript',body:"System.register(['react'],function(e){var R;return{setters:[function(v){R=v.default||v}],execute:function(){e('default',function(){return R.createElement('section',null,'Controlled Cashflow tenant')})}}});"}));
  30 |     const entity={id:1,name:'TEST_ENTITY',roleId:1,roleName:'Viewer',applicationName:'Fixture',subjects:[{id:1,name:'TEST_SUBJECT',actions:[]}]};
  31 |     const tile={title:'Cashflow',entryName:'Global',tile:'/cashflow',module:'/cashflow',container:'@fm/audit_cashflow',entity:['TEST_ENTITY'],subject:'TEST_SUBJECT',imageDarkTheme:'',emailSupport:''};
  32 |     for(const endpoint of ['login','validate','extend'])await page.route(`**/api/auth/v2/sso/${endpoint}`,route=>route.fulfill({status:200,headers:{'single-ui-authorization':fixtureAccess()},json:{result:true,entities:[entity],drawers:[{id:1,label:'Fixture',tiles:[tile]}],userInfo:JSON.stringify({sub:'USER-A',fullName:'USER-A'})}}));
  33 |     login=await openLogin(page);await audit.record('browser-environment',{engine:browserName,channel:browserName==='chromium'?browser:null,
  34 |      distribution,version:page.context().browser()?.version(),isolation:state,tenant:'CONTROLLED_CASHFLOW_MODULE',
  35 |      limits:['Accepted identity and Cashflow tenant are controlled fixtures.','Firefox and WebKit use Playwright automation builds.','WebKit execution does not establish Safari product compatibility.']});
  36 |    });
  37 |    await audit.step(2,async()=>{await login.fillUsername('USER-A');});
  38 |    await audit.step(3,async()=>{await login.fillPassword('FixturePass1!');});
  39 |    await audit.step(4,async()=>{await login.clickSignInButton();});
  40 |    await audit.step(5,async()=>{await expect(page.getByTestId(`${localPrefix}_new_tile`)).toBeVisible();});
  41 |    await audit.step(6,async()=>{await page.getByTestId(`${localPrefix}_new_tile`).click();});
  42 |    await audit.step(7,async()=>{await drawer.getByTestId(`${localPrefix}_tile`).getByText('Cashflow',{exact:true}).click();});
> 43 |    await audit.step(8,async()=>{await expect(portal.workspaceList.getByRole('tab',{selected:true}).getByRole('textbox')).toHaveValue('Cashflow');});
     |                                                                                                                          ^ Error: expect(locator).toHaveValue(expected) failed
  44 |    await audit.step(9,async()=>{await portal.clickAvatarButton();});
  45 |    await audit.step(10,async()=>{await portal.clickProfileMenuItem();});
  46 |    await audit.step(11,async()=>{await expect(page.getByText('User Profile',{exact:true})).toBeVisible();});
  47 |    await audit.step(12,async()=>{await expect(page.getByTestId('entitlement-profile-label-box')).toContainText('USER-A');});
  48 |    await audit.step(13,async()=>{const tabs=page.getByRole('tablist',{name:'workspaces',includeHidden:true});await expect(tabs.getByRole('textbox',{name:'Workspace Name',includeHidden:true})).toHaveValue('Cashflow');});
  49 |   });
  50 |  });
  51 | }
  52 | 
```