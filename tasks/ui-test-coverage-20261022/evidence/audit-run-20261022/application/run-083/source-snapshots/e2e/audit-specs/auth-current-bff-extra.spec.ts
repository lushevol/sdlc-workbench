import { test, expect } from '../support/audit-fixture.js';
import { commonAssertion, equalsToken, runSessionCase, sessionSetup, type Session, type SystemWindow } from '../support/auth-session.js';
import { blockExternal, localBase, localPrefix, openLogin, seedWorkspaces, workspace } from '../support/local-app.js';
import { LoginPage } from '../pages/login.page.js';
const bff='http://127.0.0.1:8090/api/auth';
test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',serviceWorkers:'block',
  auditFixture:'Actual MFE and exact-current BFF with disposable PostgreSQL migrations. Synthetic external identity and entitlements; isolated bootstrap. Request-scoped analytics or entitlement fault injection. No remote provider or production Boot4 claim.'});
for(const id of ['AUTH-136','AUTH-139']as const){
  test(`${id} actual current BFF external dependency failure`,async({page,audit})=>{
    const steps=await audit.defineCase(id);let login!:LoginPage;let status=0;let body:unknown;
    for(const step of steps)await audit.step(step.number,async()=>{
      if(step.number===1){await blockExternal(page);await seedWorkspaces(page,[workspace('WS-A','WS-A')]);login=await openLogin(page);return;}
      if(step.number===2){
        await page.route('**/api/auth/v2/sso/login',async route=>{const response=await route.fetch({url:`${bff}/v2/sso/login`,headers:{...route.request().headers(),'X-UI-Audit-Fault':id==='AUTH-136'?'analytics':'entitlements'}});status=response.status();body=await response.json();await route.fulfill({response});});
        await audit.record('fault-boundary',{fault:id==='AUTH-136'?'Actual BFF analytics insert callback throws':'Actual BFF authorization service callback throws',owner:'Local fixture external dependency',fabricatedResponse:false});return;
      }
      if(step.number===3){await login.fillUsername('user-a');return;}
      if(step.number===4){await login.fillPassword('FixturePass1!');return;}
      if(step.number===5){await login.clickSignInButton();await expect.poll(()=>status).toBeGreaterThan(0);await audit.record('actual-login-response',{status,body});return;}
      if(step.text.includes('tab labelled "WS-A"')){await expect(page.getByTestId('workspaces-tab-WS-A')).toBeVisible();return;}
      if(step.text.includes('textbox with placeholder')){await expect(login.usernameInput).toBeVisible();return;}
      if(step.text.includes('text input with placeholder')){await expect(login.passwordInput).toBeVisible();return;}
      if(step.text.includes('button labelled "Sign In"')){await expect(login.signInButton).toBeVisible();return;}
      if(step.text.includes('alert in the portal notification')){await expect(page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toHaveText('Invalid username and password combination or SSO service is unavailable.');return;}
      if(step.text.includes('tablist named "workspaces"')){await expect(page.getByRole('tablist',{name:'workspaces',exact:true})).toHaveCount(0);return;}
      throw new Error(`Missing ${id} step${step.number}`);
    });
  });
}
test('AUTH-111 actual current BFF logout invalidates replay',async({page,audit})=>{
  const steps=await audit.defineCase('AUTH-111');let s!:Session;let access='';let rejected=false;
  for(const step of steps)await audit.step(step.number,async()=>{
    if(step.number===1){
      s=await sessionSetup(page,audit,{});
      const signed=await page.request.post(`${bff}/local/fixture/token`,{data:{expiresInSeconds:600}});access=(await signed.json()).token;
      const response=await page.request.post(`${bff}/v2/sso/logout`,{data:{singleUIAuthorization:access}});expect(response.status()).toBe(200);
      await s.portal.avatarButton.click({force:true});await s.portal.logoutMenuItem.click({force:true});
      await page.getByRole('dialog',{name:'Leave Now?',exact:true}).getByRole('button',{name:'Logout',exact:true}).click({force:true});await page.clock.runFor(1000);await s.login.expectVisible();return;
    }
    if(step.number===2){const payload=JSON.parse(Buffer.from(access.split('.')[1],'base64url').toString());expect(payload.exp*1000).toBeGreaterThan(Date.now());await audit.record('captured-access-metadata',{expiry:payload.exp,rawTokenRetained:false});return;}
    if(step.number===3){
      await page.route('**/api/auth/v2/sso/validate',async route=>{const response=await route.fetch({url:`${bff}/v2/sso/validate`});const body=await response.json();rejected=response.status()===401&&body.errorMessage.includes('TOKEN_INVALID_EXPIRED');await audit.record('revoked-session-response',{status:response.status(),body});await route.fulfill({response});});
      await page.evaluate(async value=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');void m.Service.postService('/auth/v2/sso/validate',{singleUIAuthorization:value}).catch(()=>{});},access);return;
    }
    if(step.number===4){await expect.poll(()=>rejected).toBe(true);return;}
    if(!await commonAssertion(page,s,step.text))throw new Error(`Missing AUTH111 step${step.number}`);
  });
});
