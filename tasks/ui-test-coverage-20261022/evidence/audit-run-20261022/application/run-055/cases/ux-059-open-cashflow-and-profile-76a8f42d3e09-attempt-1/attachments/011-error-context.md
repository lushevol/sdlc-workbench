# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: browser-compatibility.spec.ts >> UX-059 chromium >> UX-059 open Cashflow and profile
- Location: e2e/audit-specs/browser-compatibility.spec.ts:12:3

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
  6  | const browser = process.env.E2E_BROWSER === 'msedge' ? 'msedge' : 'chromium';
  7  | const id = browser === 'msedge' ? 'UX-060' : 'UX-059';
  8  | {
  9  |  test.describe(`${id} ${browser}`, () => {
  10 |   test.use({ auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',
  11 |    auditFixture:`Actual React shell in ${browser}; controlled accepted identity and Cashflow SystemJS module. Real identity and business tenant results remain unverified.` });
  12 |   test(`${id} open Cashflow and profile`, async({page,audit})=>{
  13 |    await audit.defineCase(id);let login:LoginPage;const portal=new PortalPage(page,localPrefix);
  14 |    const drawer=page.getByTestId(`${localPrefix}_drawer`);
  15 |    await audit.step(1,async()=>{
  16 |     const state=await page.context().storageState();expect(state.origins).toHaveLength(0);expect(state.cookies).toHaveLength(0);
  17 |     await blockExternal(page);await page.routeWebSocket('**/*',socket=>socket.close());
  18 |     await page.addInitScript(value=>localStorage.setItem('SET_WORKSPACES',JSON.stringify([value])),workspace('Home','W1'));
  19 |     await page.route('**/importmap*.json',async route=>{const response=await route.fetch();const map=await response.json();await route.fulfill({response,json:{...map,imports:{...map.imports,'@fm/audit_cashflow':`${localBase}/audit-cashflow.js`}}});});
  20 |     await page.route('**/audit-cashflow.js',route=>route.fulfill({contentType:'application/javascript',body:"System.register(['react'],function(e){var R;return{setters:[function(v){R=v.default||v}],execute:function(){e('default',function(){return R.createElement('section',null,'Controlled Cashflow tenant')})}}});"}));
  21 |     const entity={id:1,name:'TEST_ENTITY',roleId:1,roleName:'Viewer',applicationName:'Fixture',subjects:[{id:1,name:'TEST_SUBJECT',actions:[]}]};
  22 |     const tile={title:'Cashflow',entryName:'Global',tile:'/cashflow',module:'/cashflow',container:'@fm/audit_cashflow',entity:['TEST_ENTITY'],subject:'TEST_SUBJECT',imageDarkTheme:'',emailSupport:''};
  23 |     for(const endpoint of ['login','validate','extend'])await page.route(`**/api/auth/v2/sso/${endpoint}`,route=>route.fulfill({status:200,headers:{'single-ui-authorization':fixtureAccess()},json:{result:true,entities:[entity],drawers:[{id:1,label:'Fixture',tiles:[tile]}],userInfo:JSON.stringify({sub:'USER-A',fullName:'USER-A'})}}));
  24 |     login=await openLogin(page);await audit.record('browser-environment',{engine:'chromium',channel:browser,version:page.context().browser()?.version(),isolation:state,tenant:'CONTROLLED_CASHFLOW_MODULE'});
  25 |    });
  26 |    await audit.step(2,async()=>{await login.fillUsername('USER-A');});
  27 |    await audit.step(3,async()=>{await login.fillPassword('FixturePass1!');});
  28 |    await audit.step(4,async()=>{await login.clickSignInButton();});
  29 |    await audit.step(5,async()=>{await expect(page.getByTestId(`${localPrefix}_new_tile`)).toBeVisible();});
  30 |    await audit.step(6,async()=>{await page.getByTestId(`${localPrefix}_new_tile`).click();});
  31 |    await audit.step(7,async()=>{await drawer.getByTestId(`${localPrefix}_tile`).getByText('Cashflow',{exact:true}).click();});
> 32 |    await audit.step(8,async()=>{await expect(portal.workspaceList.getByRole('tab',{selected:true}).getByRole('textbox')).toHaveValue('Cashflow');});
     |                                                                                                                          ^ Error: expect(locator).toHaveValue(expected) failed
  33 |    await audit.step(9,async()=>{await portal.clickAvatarButton();});
  34 |    await audit.step(10,async()=>{await portal.clickProfileMenuItem();});
  35 |    await audit.step(11,async()=>{await expect(page.getByText('User Profile',{exact:true})).toBeVisible();});
  36 |    await audit.step(12,async()=>{await expect(page.getByTestId('entitlement-profile-label-box')).toContainText('USER-A');});
  37 |    await audit.step(13,async()=>{const tabs=page.getByRole('tablist',{name:'workspaces',includeHidden:true});await expect(tabs.getByRole('textbox',{name:'Workspace Name',includeHidden:true})).toHaveValue('Cashflow');});
  38 |   });
  39 |  });
  40 | }
  41 | 
```