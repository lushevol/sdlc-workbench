# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-current-bff-extra.spec.ts >> AUTH-136 actual current BFF external dependency failure
- Location: e2e/audit-specs/auth-current-bff-extra.spec.ts:9:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByTestId('workspaces-tab-WS-A')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" getByTestId('workspaces-tab-WS-A') with timeout 5000ms
  - waiting for getByTestId('workspaces-tab-WS-A')

```

```yaml
- main:
  - heading "Sign In" [level=3]
  - text: Username
  - textbox "Enter Username": user-a
  - text: Password
  - textbox "Enter Password": FixturePass1!
  - button "Sign In"
  - separator
  - link "Sign In With SSO":
    - /url: https://login.microsoftonline.com/cd823f6b-31c5-4241-b504-3707cbc03fb7/oauth2/v2.0/authorize?client_id=80c8b904-1b64-443b-a651-7548764d534d&response_type=code&redirect_uri=http://localhost:8128/mfa/callback&response_mode=query&scope=openid+profile+offline_access+email
- main:
  - tabpanel:
    - heading "Markets Operations One" [level=2]
    - paragraph: Markets Operations One Portal (MO1) is a single, evolving workspace for Operations processing, integrating post-trade applications, and progressively delivering a more connected, intelligent, and efficient processing.
  - tablist "login tabs":
    - tab "login-tabpanel" [selected]
- alert:
  - alert: Invalid username and password combination or SSO service is unavailable.
  - button "Close"
```

# Test source

```ts
  1  | import { test, expect } from '../support/audit-fixture.js';
  2  | import { commonAssertion, equalsToken, runSessionCase, sessionSetup, type Session, type SystemWindow } from '../support/auth-session.js';
  3  | import { blockExternal, localBase, localPrefix, openLogin, seedWorkspaces, workspace } from '../support/local-app.js';
  4  | import { LoginPage } from '../pages/login.page.js';
  5  | const bff='http://127.0.0.1:8090/api/auth';
  6  | test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',serviceWorkers:'block',
  7  |   auditFixture:'Actual MFE and exact-current BFF with disposable PostgreSQL migrations. Synthetic external identity and entitlements; isolated bootstrap. Request-scoped analytics or entitlement fault injection. No remote provider or production Boot4 claim.'});
  8  | for(const id of ['AUTH-136','AUTH-139']as const){
  9  |   test(`${id} actual current BFF external dependency failure`,async({page,audit})=>{
  10 |     const steps=await audit.defineCase(id);let login!:LoginPage;let status=0;let body:unknown;
  11 |     for(const step of steps)await audit.step(step.number,async()=>{
  12 |       if(step.number===1){await blockExternal(page);await seedWorkspaces(page,[workspace('WS-A','WS-A')]);login=await openLogin(page);return;}
  13 |       if(step.number===2){
  14 |         await page.route('**/api/auth/v2/sso/login',async route=>{const response=await route.fetch({url:`${bff}/v2/sso/login`,headers:{...route.request().headers(),'X-UI-Audit-Fault':id==='AUTH-136'?'analytics':'entitlements'}});status=response.status();body=await response.json();await route.fulfill({response});});
  15 |         await audit.record('fault-boundary',{fault:id==='AUTH-136'?'Actual BFF analytics insert callback throws':'Actual BFF authorization service callback throws',owner:'Local fixture external dependency',fabricatedResponse:false});return;
  16 |       }
  17 |       if(step.number===3){await login.fillUsername('user-a');return;}
  18 |       if(step.number===4){await login.fillPassword('FixturePass1!');return;}
  19 |       if(step.number===5){await login.clickSignInButton();await expect.poll(()=>status).toBeGreaterThan(0);await audit.record('actual-login-response',{status,body});return;}
> 20 |       if(step.text.includes('tab labelled "WS-A"')){await expect(page.getByTestId('workspaces-tab-WS-A')).toBeVisible();return;}
     |                                                                                                           ^ Error: expect(locator).toBeVisible() failed
  21 |       if(step.text.includes('textbox with placeholder')){await expect(login.usernameInput).toBeVisible();return;}
  22 |       if(step.text.includes('text input with placeholder')){await expect(login.passwordInput).toBeVisible();return;}
  23 |       if(step.text.includes('button labelled "Sign In"')){await expect(login.signInButton).toBeVisible();return;}
  24 |       if(step.text.includes('alert in the portal notification')){await expect(page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toHaveText('Invalid username and password combination or SSO service is unavailable.');return;}
  25 |       if(step.text.includes('tablist named "workspaces"')){await expect(page.getByRole('tablist',{name:'workspaces',exact:true})).toHaveCount(0);return;}
  26 |       throw new Error(`Missing ${id} step${step.number}`);
  27 |     });
  28 |   });
  29 | }
  30 | test('AUTH-111 actual current BFF logout invalidates replay',async({page,audit})=>{
  31 |   const steps=await audit.defineCase('AUTH-111');let s!:Session;let access='';let rejected=false;
  32 |   for(const step of steps)await audit.step(step.number,async()=>{
  33 |     if(step.number===1){
  34 |       s=await sessionSetup(page,audit,{});
  35 |       const signed=await page.request.post(`${bff}/local/fixture/token`,{data:{expiresInSeconds:600}});access=(await signed.json()).token;
  36 |       const response=await page.request.post(`${bff}/v2/sso/logout`,{data:{singleUIAuthorization:access}});expect(response.status()).toBe(200);
  37 |       await s.portal.avatarButton.click({force:true});await s.portal.logoutMenuItem.click({force:true});
  38 |       await page.getByRole('dialog',{name:'Leave Now?',exact:true}).getByRole('button',{name:'Logout',exact:true}).click({force:true});await page.clock.runFor(1000);await s.login.expectVisible();return;
  39 |     }
  40 |     if(step.number===2){const payload=JSON.parse(Buffer.from(access.split('.')[1],'base64url').toString());expect(payload.exp*1000).toBeGreaterThan(Date.now());await audit.record('captured-access-metadata',{expiry:payload.exp,rawTokenRetained:false});return;}
  41 |     if(step.number===3){
  42 |       await page.route('**/api/auth/v2/sso/validate',async route=>{const response=await route.fetch({url:`${bff}/v2/sso/validate`});const body=await response.json();rejected=response.status()===401&&body.errorMessage.includes('TOKEN_INVALID_EXPIRED');await audit.record('revoked-session-response',{status:response.status(),body});await route.fulfill({response});});
  43 |       await page.evaluate(async value=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');void m.Service.postService('/auth/v2/sso/validate',{singleUIAuthorization:value}).catch(()=>{});},access);return;
  44 |     }
  45 |     if(step.number===4){await expect.poll(()=>rejected).toBe(true);return;}
  46 |     if(!await commonAssertion(page,s,step.text))throw new Error(`Missing AUTH111 step${step.number}`);
  47 |   });
  48 | });
  49 | 
```