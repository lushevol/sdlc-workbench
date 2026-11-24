import { test, expect } from '../support/audit-fixture.js';
import { blockExternal, fixtureAccess, localBase, localPrefix, openLogin, seedWorkspaces, workspace } from '../support/local-app.js';
import { LoginPage } from '../pages/login.page.js';
import { PortalPage } from '../pages/portal.page.js';

test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',serviceWorkers:'block',
  auditFixture:'Actual MFE; controlled callback and credential responses. External destinations are fulfilled locally. No actual identity-provider acceptance, server fallback or OAuth security claim.'});
const alert=(page:LoginPage['page'])=>page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]');
for(const id of ['AUTH-041','AUTH-042'] as const){
  test(`${id} malformed successful credential response`,async({page,audit})=>{
    const steps=await audit.defineCase(id);const login=new LoginPage(page,localPrefix);
    for(const step of steps)await audit.step(step.number,async()=>{
      if(step.number===1){await blockExternal(page);await seedWorkspaces(page,[workspace('WS-A','WS-A')]);await openLogin(page);return;}
      if(step.number===2){await page.route('**/api/auth/v2/sso/login',route=>route.fulfill({status:200,
        headers:id==='AUTH-041'?{'single-ui-authorization':fixtureAccess()}:{},json:{result:true,userInfo:id==='AUTH-041'?'not-json':JSON.stringify({sub:'user-a'}),drawers:[],entities:[]}}));return;}
      if(step.number===3){await login.fillUsername('user-a');return;}
      if(step.number===4){await login.fillPassword('FixturePass1!');return;}
      if(step.number===5){await login.clickSignInButton();return;}
      if(step.text.includes('tablist named "workspaces"')){await expect(page.getByRole('tablist',{name:'workspaces',exact:true})).toHaveCount(0);return;}
      if(step.text.includes('textbox with placeholder')){await expect(login.usernameInput).toBeVisible();return;}
      if(step.text.includes('text input with placeholder')){await expect(login.passwordInput).toBeVisible();return;}
      if(step.text.includes('button labelled "Sign In"')){await expect(login.signInButton).toBeVisible();return;}
      if(step.text.includes('authentication error is visible')){await expect(alert(page)).toBeVisible();return;}
      throw new Error(`Missing ${id} step ${step.number}`);
    });
  });
}
for(const id of ['AUTH-029','AUTH-143'] as const){
  test(`${id} source configured SSO navigation`,async({page,audit})=>{
    const steps=await audit.defineCase(id);let login!:LoginPage;let expected='';let requested='';
    for(const step of steps)await audit.step(step.number,async()=>{
      if(step.number===1){await blockExternal(page);login=await openLogin(page);return;}
      if(step.number===2){await login.expectVisible();expected=(await login.ssoLink.getAttribute('href'))!;
        await page.route(expected,async route=>{requested=route.request().url();await route.fulfill({status:200,contentType:'text/html',body:'<main><h1>Controlled identity provider destination</h1></main>'});});
        await audit.record('sso-destination',{expected,cancelledAttempt:id==='AUTH-143'?'SSO-A fixture':null,externalNetworkUsed:false});return;}
      if(step.number===3){await login.clickSsoLink();return;}
      if(step.number===4){await expect.poll(()=>requested).toBe(new URL(expected).toString());expect(page.url()).toBe(new URL(expected).toString());return;}
      if(step.number===5){await expect(page.getByRole('tablist',{name:'workspaces',exact:true})).toHaveCount(0);return;}
      throw new Error(`Missing ${id} step ${step.number}`);
    });
  });
}
for(const id of ['AUTH-140','AUTH-141','AUTH-142'] as const){
  test(`${id} proposed callback safety probe`,async({page,audit})=>{
    const steps=await audit.defineCase(id);const login=new LoginPage(page,localPrefix);let posts=0;
    const query=id==='AUTH-140'?'code=STATE-CODE-A&state=STATE-B':id==='AUTH-141'?'code=OTHER-SESSION-CODE':'error=access_denied';
    for(const step of steps)await audit.step(step.number,async()=>{
      if(step.number===1){await blockExternal(page);await seedWorkspaces(page,[workspace('WS-A','WS-A')]);await openLogin(page);return;}
      if(step.number===2){
        if(id==='AUTH-140')await page.evaluate(()=>{sessionStorage.setItem('fixture.sso.state','STATE-A');});
        await page.route(/\/api\/auth\/v[23]\/sso\/login$/,async route=>{posts++;await route.fulfill({status:200,headers:{'single-ui-authorization':fixtureAccess()},
          json:{userInfo:JSON.stringify({sub:id==='AUTH-141'?'other-user':'user-a'}),drawers:[{label:'Fixture',tiles:[{title:'Fixture',entity:['ENTITY-A'],subject:'AUDIT',module:'/unused',tile:'/unused',container:'@fm/unused'}]}],entities:[{name:'ENTITY-A',subjects:[]}]}});});
        await audit.record('callback-safety-fixture',{query,stateStorageKey:id==='AUTH-140'?'fixture.sso.state':null,stateKeyStatus:'TEST_FIXTURE_KEY; no product state storage key exists in inspected MFE',serverSecurity:'NOT_VERIFIED'});return;
      }
      if(step.number===3){await page.goto(`${localBase}/?show_normal_login=Y&${query}`);if(id!=='AUTH-142')await expect.poll(()=>posts).toBe(1);return;}
      if(step.text.includes('textbox with placeholder')){await expect(login.usernameInput).toBeVisible();return;}
      if(step.text.includes('text input with placeholder')){await expect(login.passwordInput).toBeVisible();return;}
      if(step.text.includes('button labelled "Sign In"')){await expect(login.signInButton).toBeVisible();return;}
      if(step.text.includes('link labelled "Sign In With SSO"')){await expect(login.ssoLink).toBeVisible();return;}
      if(step.text.includes('tablist named "workspaces"')){await expect(page.getByRole('tablist',{name:'workspaces',exact:true})).toHaveCount(0);return;}
      if(step.text.includes('records zero callback-code POST')){expect(posts).toBe(0);return;}
      if(step.text.includes('authentication error is visible')){await expect(alert(page)).toBeVisible();return;}
      if(step.text.includes('no session for the other browser identity')){expect(await page.evaluate(()=>localStorage.getItem('SET_USER'))).not.toContain('other-user');return;}
      throw new Error(`Missing ${id} step ${step.number}`);
    });
  });
}
