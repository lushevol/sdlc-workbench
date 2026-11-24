# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-login-security-expanded.spec.ts >> AUTH-141 proposed callback safety probe
- Location: e2e/audit-specs/auth-login-security-expanded.spec.ts:44:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByTestId('MicroWebUI_base_login').getByPlaceholder('Enter Username', { exact: true })
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" getByTestId('MicroWebUI_base_login').getByPlaceholder('Enter Username', { exact: true }) with timeout 5000ms
  - waiting for getByTestId('MicroWebUI_base_login').getByPlaceholder('Enter Username', { exact: true })

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 05:31 UTC
  - checkbox "Time Switch" [checked]
- button "User Profiles": A
- button "Share Feedback"
- main:
  - tablist "workspaces":
    - tab "WS-A" [selected]:
      - region "WS-A":
        - textbox "Workspace Name": WS-A
    - button "Add Workspace"
  - tabpanel:
    - paragraph: Start customizing your workspace
    - paragraph: find out what workspace preference options you have and how those options work.
    - button "Find tile"
```

# Test source

```ts
  1  | import { test, expect } from '../support/audit-fixture.js';
  2  | import { blockExternal, fixtureAccess, localBase, localPrefix, openLogin, seedWorkspaces, workspace } from '../support/local-app.js';
  3  | import { LoginPage } from '../pages/login.page.js';
  4  | import { PortalPage } from '../pages/portal.page.js';
  5  | 
  6  | test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',serviceWorkers:'block',
  7  |   auditFixture:'Actual MFE; controlled callback and credential responses. External destinations are fulfilled locally. No actual identity-provider acceptance, server fallback or OAuth security claim.'});
  8  | const alert=(page:LoginPage['page'])=>page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]');
  9  | for(const id of ['AUTH-041','AUTH-042'] as const){
  10 |   test(`${id} malformed successful credential response`,async({page,audit})=>{
  11 |     const steps=await audit.defineCase(id);const login=new LoginPage(page,localPrefix);
  12 |     for(const step of steps)await audit.step(step.number,async()=>{
  13 |       if(step.number===1){await blockExternal(page);await seedWorkspaces(page,[workspace('WS-A','WS-A')]);await openLogin(page);return;}
  14 |       if(step.number===2){await page.route('**/api/auth/v2/sso/login',route=>route.fulfill({status:200,
  15 |         headers:id==='AUTH-041'?{'single-ui-authorization':fixtureAccess()}:{},json:{result:true,userInfo:id==='AUTH-041'?'not-json':JSON.stringify({sub:'user-a'}),drawers:[],entities:[]}}));return;}
  16 |       if(step.number===3){await login.fillUsername('user-a');return;}
  17 |       if(step.number===4){await login.fillPassword('FixturePass1!');return;}
  18 |       if(step.number===5){await login.clickSignInButton();return;}
  19 |       if(step.text.includes('tablist named "workspaces"')){await expect(page.getByRole('tablist',{name:'workspaces',exact:true})).toHaveCount(0);return;}
  20 |       if(step.text.includes('textbox with placeholder')){await expect(login.usernameInput).toBeVisible();return;}
  21 |       if(step.text.includes('text input with placeholder')){await expect(login.passwordInput).toBeVisible();return;}
  22 |       if(step.text.includes('button labelled "Sign In"')){await expect(login.signInButton).toBeVisible();return;}
  23 |       if(step.text.includes('authentication error is visible')){await expect(alert(page)).toBeVisible();return;}
  24 |       throw new Error(`Missing ${id} step ${step.number}`);
  25 |     });
  26 |   });
  27 | }
  28 | for(const id of ['AUTH-029','AUTH-143'] as const){
  29 |   test(`${id} source configured SSO navigation`,async({page,audit})=>{
  30 |     const steps=await audit.defineCase(id);let login!:LoginPage;let expected='';let requested='';
  31 |     for(const step of steps)await audit.step(step.number,async()=>{
  32 |       if(step.number===1){await blockExternal(page);login=await openLogin(page);return;}
  33 |       if(step.number===2){await login.expectVisible();expected=(await login.ssoLink.getAttribute('href'))!;
  34 |         await page.route(expected,async route=>{requested=route.request().url();await route.fulfill({status:200,contentType:'text/html',body:'<main><h1>Controlled identity provider destination</h1></main>'});});
  35 |         await audit.record('sso-destination',{expected,cancelledAttempt:id==='AUTH-143'?'SSO-A fixture':null,externalNetworkUsed:false});return;}
  36 |       if(step.number===3){await login.clickSsoLink();return;}
  37 |       if(step.number===4){await expect.poll(()=>requested).toBe(new URL(expected).toString());expect(page.url()).toBe(new URL(expected).toString());return;}
  38 |       if(step.number===5){await expect(page.getByRole('tablist',{name:'workspaces',exact:true})).toHaveCount(0);return;}
  39 |       throw new Error(`Missing ${id} step ${step.number}`);
  40 |     });
  41 |   });
  42 | }
  43 | for(const id of ['AUTH-140','AUTH-141','AUTH-142'] as const){
  44 |   test(`${id} proposed callback safety probe`,async({page,audit})=>{
  45 |     const steps=await audit.defineCase(id);const login=new LoginPage(page,localPrefix);let posts=0;
  46 |     const query=id==='AUTH-140'?'code=STATE-CODE-A&state=STATE-B':id==='AUTH-141'?'code=OTHER-SESSION-CODE':'error=access_denied';
  47 |     for(const step of steps)await audit.step(step.number,async()=>{
  48 |       if(step.number===1){await blockExternal(page);await seedWorkspaces(page,[workspace('WS-A','WS-A')]);await openLogin(page);return;}
  49 |       if(step.number===2){
  50 |         if(id==='AUTH-140')await page.evaluate(()=>{sessionStorage.setItem('fixture.sso.state','STATE-A');});
  51 |         await page.route(/\/api\/auth\/v[23]\/sso\/login$/,async route=>{posts++;await route.fulfill({status:200,headers:{'single-ui-authorization':fixtureAccess()},
  52 |           json:{userInfo:JSON.stringify({sub:id==='AUTH-141'?'other-user':'user-a'}),drawers:[{label:'Fixture',tiles:[{title:'Fixture',entity:['ENTITY-A'],subject:'AUDIT',module:'/unused',tile:'/unused',container:'@fm/unused'}]}],entities:[{name:'ENTITY-A',subjects:[]}]}});});
  53 |         await audit.record('callback-safety-fixture',{query,stateStorageKey:id==='AUTH-140'?'fixture.sso.state':null,stateKeyStatus:'TEST_FIXTURE_KEY; no product state storage key exists in inspected MFE',serverSecurity:'NOT_VERIFIED'});return;
  54 |       }
  55 |       if(step.number===3){await page.goto(`${localBase}/?show_normal_login=Y&${query}`);if(id!=='AUTH-142')await expect.poll(()=>posts).toBe(1);return;}
> 56 |       if(step.text.includes('textbox with placeholder')){await expect(login.usernameInput).toBeVisible();return;}
     |                                                                                            ^ Error: expect(locator).toBeVisible() failed
  57 |       if(step.text.includes('text input with placeholder')){await expect(login.passwordInput).toBeVisible();return;}
  58 |       if(step.text.includes('button labelled "Sign In"')){await expect(login.signInButton).toBeVisible();return;}
  59 |       if(step.text.includes('link labelled "Sign In With SSO"')){await expect(login.ssoLink).toBeVisible();return;}
  60 |       if(step.text.includes('tablist named "workspaces"')){await expect(page.getByRole('tablist',{name:'workspaces',exact:true})).toHaveCount(0);return;}
  61 |       if(step.text.includes('records zero callback-code POST')){expect(posts).toBe(0);return;}
  62 |       if(step.text.includes('authentication error is visible')){await expect(alert(page)).toBeVisible();return;}
  63 |       if(step.text.includes('no session for the other browser identity')){expect(await page.evaluate(()=>localStorage.getItem('SET_USER'))).not.toContain('other-user');return;}
  64 |       throw new Error(`Missing ${id} step ${step.number}`);
  65 |     });
  66 |   });
  67 | }
  68 | 
```