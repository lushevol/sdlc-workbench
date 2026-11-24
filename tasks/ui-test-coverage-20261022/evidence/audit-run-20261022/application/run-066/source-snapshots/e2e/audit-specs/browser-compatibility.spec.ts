import { test, expect } from '../support/audit-fixture.js';
import { LoginPage } from '../pages/login.page.js';
import { PortalPage } from '../pages/portal.page.js';
import { blockExternal, fixtureAccess, localBase, localPrefix, openLogin, workspace } from '../support/local-app.js';

const selectedBrowser = process.env.E2E_COMPAT_BROWSER ?? (process.env.E2E_BROWSER === 'msedge' ? 'msedge' : 'chromium');
if (!['chromium', 'msedge', 'firefox', 'webkit'].includes(selectedBrowser)) {
 throw new Error('E2E_COMPAT_BROWSER must be chromium, msedge, firefox, or webkit.');
}
const browser = selectedBrowser as 'chromium' | 'msedge' | 'firefox' | 'webkit';
const browserName = browser === 'msedge' ? 'chromium' : browser;
const id = {chromium:'UX-059',msedge:'UX-060',firefox:'UX-061',webkit:'UX-062'}[browser];
const distribution = browser === 'msedge' ? 'Installed Microsoft Edge' : `Playwright ${browser} automation build`;
test.use({ browserName,
 launchOptions:{headless:process.env.E2E_HEADED!=='1',channel:browserName==='chromium'?browser:undefined,
  chromiumSandbox:browserName==='chromium'?true:undefined,
  firefoxUserPrefs:browser==='firefox'?{'network.proxy.type':0}:undefined} });
{
 test.describe(`${id} ${browser}`, () => {
  test.use({ auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',
   auditFixture:`Actual React shell in ${distribution}; controlled accepted identity and Cashflow SystemJS module. Firefox uses explicit direct-local transport after inherited proxy navigation returned HTTP503. External requests remain blocked. Real identity and business tenant results remain unverified. Firefox and WebKit use Playwright automation builds. WebKit execution does not establish Safari product compatibility.` });
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
    const tile={title:'Cashflow',entryName:'Global',tile:'/cashflow',module:'/cashflow',container:'@fm/audit_cashflow',entity:['TEST_ENTITY'],subject:'TEST_SUBJECT',imageDarkTheme:'',emailSupport:''};
    for(const endpoint of ['login','validate','extend'])await page.route(`**/api/auth/v2/sso/${endpoint}`,route=>route.fulfill({status:200,headers:{'single-ui-authorization':fixtureAccess()},json:{result:true,entities:[entity],drawers:[{id:1,label:'Fixture',tiles:[tile]}],userInfo:JSON.stringify({sub:'USER-A',fullName:'USER-A'})}}));
    login=await openLogin(page);await audit.record('browser-environment',{engine:browserName,channel:browserName==='chromium'?browser:null,
     distribution,version:page.context().browser()?.version(),isolation:state,tenant:'CONTROLLED_CASHFLOW_MODULE',
     localTransport:browser==='firefox'?'FIREFOX_PROXY_DISABLED_FOR_ISOLATED_LOCAL_AUDIT':'DEFAULT_BROWSER_LOCAL_TRANSPORT',
     limits:['Accepted identity and Cashflow tenant are controlled fixtures.','Firefox and WebKit use Playwright automation builds.','WebKit execution does not establish Safari product compatibility.']});
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
