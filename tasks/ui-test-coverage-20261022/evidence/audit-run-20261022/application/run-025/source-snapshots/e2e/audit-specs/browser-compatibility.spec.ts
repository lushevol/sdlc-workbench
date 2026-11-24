import { test, expect } from '../support/audit-fixture.js';
import { LoginPage } from '../pages/login.page.js';
import { PortalPage } from '../pages/portal.page.js';
import { blockExternal, fixtureAccess, localBase, localPrefix, openLogin, workspace } from '../support/local-app.js';

const browser = process.env.E2E_BROWSER === 'msedge' ? 'msedge' : 'chromium';
const id = browser === 'msedge' ? 'UX-060' : 'UX-059';
{
 test.describe(`${id} ${browser}`, () => {
  test.use({ auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',
   auditFixture:`Actual React shell in ${browser}; controlled accepted identity and Cashflow SystemJS module. Real identity and business tenant results remain unverified.` });
  test(`${id} open Cashflow and profile`, async({page,audit})=>{
   await audit.defineCase(id);let login:LoginPage;const portal=new PortalPage(page,localPrefix);
   const drawer=page.getByTestId(`${localPrefix}_drawer`);
   await audit.step(1,async()=>{
    const state=await page.context().storageState();expect(state.origins).toHaveLength(0);expect(state.cookies).toHaveLength(0);
    await blockExternal(page);await page.routeWebSocket('**/*',socket=>socket.close());
    await page.addInitScript(value=>localStorage.setItem('SET_WORKSPACES',JSON.stringify([value])),workspace('Home','W1'));
    await page.route('**/importmap*.json',async route=>{const response=await route.fetch();const map=await response.json();await route.fulfill({response,json:{...map,imports:{...map.imports,'@fm/audit_cashflow':`${localBase}/audit-cashflow.js`}}});});
    await page.route('**/audit-cashflow.js',route=>route.fulfill({contentType:'application/javascript',body:"System.register(['react'],function(e){var R;return{setters:[function(v){R=v.default||v}],execute:function(){e('default',function(){return R.createElement('section',null,'Controlled Cashflow tenant')})}}});"}));
    const entity={id:1,name:'TEST_ENTITY',roleId:1,roleName:'Viewer',applicationName:'Fixture',subjects:[{id:1,name:'TEST_SUBJECT',actions:[]}]};
    const tile={title:'Cashflow',subtitle:'',entryName:'Global',tile:'/cashflow',module:'/cashflow',container:'@fm/audit_cashflow',entity:['TEST_ENTITY'],subject:'TEST_SUBJECT',imageDarkTheme:'',emailSupport:''};
    for(const endpoint of ['login','validate','extend'])await page.route(`**/api/auth/v2/sso/${endpoint}`,route=>route.fulfill({status:200,headers:{'single-ui-authorization':fixtureAccess()},json:{result:true,entities:[entity],drawers:[{id:1,label:'Fixture',tiles:[tile]}],userInfo:JSON.stringify({sub:'USER-A',fullName:'USER-A'})}}));
    login=await openLogin(page);await audit.record('browser-environment',{engine:'chromium',channel:browser,version:page.context().browser()?.version(),isolation:state,tenant:'CONTROLLED_CASHFLOW_MODULE'});
   });
   await audit.step(2,async()=>{await login.fillUsername('USER-A');});
   await audit.step(3,async()=>{await login.fillPassword('FixturePass1!');});
   await audit.step(4,async()=>{await login.clickSignInButton();});
   await audit.step(5,async()=>{await expect(page.getByTestId(`${localPrefix}_new_tile`)).toBeVisible();});
   await audit.step(6,async()=>{await page.getByTestId(`${localPrefix}_new_tile`).click();});
   await audit.step(7,async()=>{await drawer.getByTestId(`${localPrefix}_tile`).getByText('Cashflow',{exact:true}).click();});
   await audit.step(8,async()=>{await expect(portal.workspaceList.getByRole('tab',{selected:true}).getByRole('textbox')).toHaveValue('Cashflow');});
   await audit.step(9,async()=>{await portal.clickAvatarButton();});
   await audit.step(10,async()=>{await portal.clickProfileMenuItem();});
   await audit.step(11,async()=>{await expect(page.getByText('User Profile',{exact:true})).toBeVisible();});
   await audit.step(12,async()=>{await expect(page.getByTestId('entitlement-profile-label-box')).toContainText('USER-A');});
   await audit.step(13,async()=>{const tabs=page.getByRole('tablist',{name:'workspaces',includeHidden:true});await expect(tabs.getByRole('textbox',{name:'Workspace Name',includeHidden:true})).toHaveValue('Cashflow');});
  });
 });
}
