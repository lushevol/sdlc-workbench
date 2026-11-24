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
    const providerVisits:{attempt:string;url:string;at:string}[]=[];
    const callbackPosts:string[]=[];
    const cancellationUrl=`${localBase}/?show_normal_login=Y&error=access_denied&state=SSO-A`;
    for(const step of steps)await audit.step(step.number,async()=>{
      if(step.number===1){await blockExternal(page);login=await openLogin(page);return;}
      if(step.number===2){await login.expectVisible();expected=(await login.ssoLink.getAttribute('href'))!;
        if(id==='AUTH-143')page.on('request',request=>{if(request.method()==='POST'&&/\/api\/auth\/v[23]\/sso\/login$/.test(new URL(request.url()).pathname))callbackPosts.push(request.url());});
        await page.route(expected,async route=>{
          requested=route.request().url();
          if(id==='AUTH-143')providerVisits.push({attempt:providerVisits.length===0?'SSO-A':'SSO-B',url:requested,at:new Date().toISOString()});
          await route.fulfill({status:200,contentType:'text/html',body:id==='AUTH-143'&&providerVisits.length===1
            ?`<main><h1>Controlled identity provider: SSO-A</h1><p>The provider fixture can cancel this attempt.</p><a href="${cancellationUrl.replaceAll('&','&amp;')}">Cancel SSO-A</a></main>`
            :'<main><h1>Controlled identity provider destination</h1></main>'});
        });
        if(id==='AUTH-143'){
          await login.clickSsoLink();
          await expect(page.getByRole('heading',{name:'Controlled identity provider: SSO-A',exact:true})).toBeVisible();
          expect(providerVisits).toHaveLength(1);expect(providerVisits[0].url).toBe(new URL(expected).toString());
          await audit.capture('sso-a-provider-before-cancel','The first actual SSO navigation reached the controlled provider cancellation boundary.');
          await page.getByRole('link',{name:'Cancel SSO-A',exact:true}).click();
          await login.expectVisible();await expect(login.passwordInput).toBeVisible();await expect(login.signInButton).toBeVisible();
          expect(page.url()).toBe(cancellationUrl);expect(callbackPosts).toEqual([]);
          expect(await page.evaluate(()=>({local:localStorage.getItem('SET_TOKEN'),session:sessionStorage.getItem('SET_TOKEN')}))).toEqual({local:null,session:null});
          await expect(page.getByRole('tablist',{name:'workspaces',exact:true})).toHaveCount(0);
          await audit.capture('sso-a-cancelled-return','The provider cancellation returned to the anonymous LOCAL login page.');
        }
        await audit.record('sso-destination',{expected,cancelledAttempt:id==='AUTH-143'?'SSO-A':null,providerVisits,cancellationReturn:id==='AUTH-143'?page.url():null,callbackPosts,externalNetworkUsed:false,
          limits:['Provider HTML and cancellation response are controlled locally. Real identity-provider cancellation is not verified.']});return;}
      if(step.number===3){await login.clickSsoLink();return;}
      if(step.number===4){await expect.poll(()=>requested).toBe(new URL(expected).toString());expect(page.url()).toBe(new URL(expected).toString());
        if(id==='AUTH-143'){
          await expect(page.getByRole('heading',{name:'Controlled identity provider destination',exact:true})).toBeVisible();
          expect(providerVisits.map(visit=>visit.attempt)).toEqual(['SSO-A','SSO-B']);expect(callbackPosts).toEqual([]);
          await audit.record('sso-retry-navigation',{providerVisits,cancelledAttempt:'SSO-A',newAttempt:'SSO-B',cancellationUrl,callbackPosts});
        }return;}
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
