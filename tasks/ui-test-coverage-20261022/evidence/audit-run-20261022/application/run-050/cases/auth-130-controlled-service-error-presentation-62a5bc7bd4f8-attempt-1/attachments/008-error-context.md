# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-boundary-expanded.spec.ts >> AUTH-130 controlled service error presentation
- Location: e2e/audit-specs/auth-boundary-expanded.spec.ts:36:3

# Error details

```
Error: expect(locator).not.toContainText(expected) failed

Locator: locator('body')
Expected substring: not "SYNTHETIC_SECRET_AUTH_130"
Received string: "New Tiledark00:00 UTCAStart customizing your workspacefind out what workspace preference options you have and how those options work.Find tileSYNTHETIC_SECRET_AUTH_130
  
  


Audit User AClick to view user profile detailsLogoutRoot Config Version: PACKAGE_VERSIONBase Container Version: PACKAGE_VERSION"
Timeout: 5000ms

Call log:
  - Expect "not toContainText" locator('body') with timeout 5000ms
  - waiting for locator('body')
    14 × locator resolved to <body>…</body>
       - unexpected value "New Tiledark00:00 UTCAStart customizing your workspacefind out what workspace preference options you have and how those options work.Find tileSYNTHETIC_SECRET_AUTH_130
  
  


Audit User AClick to view user profile detailsLogoutRoot Config Version: PACKAGE_VERSIONBase Container Version: PACKAGE_VERSION"

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 00:00 UTC
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
- alert:
  - alert: SYNTHETIC_SECRET_AUTH_130
  - button "Close"
```

# Test source

```ts
  1  | import { test, expect } from '../support/audit-fixture.js';
  2  | import { commonAssertion, equalsToken, observe, runSessionCase, sessionSetup, sessionToken, T, type Session, type SystemWindow } from '../support/auth-session.js';
  3  | import { localPrefix } from '../support/local-app.js';
  4  | 
  5  | test.use({ auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES', serviceWorkers:'block',
  6  |   auditFixture:'Actual MFE response handlers; controlled service rejection and cancellation. Signature enforcement, revocation, upstream identity, and service policy are not verified.' });
  7  | const alert=(page:Session['portal']['page'])=>page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]');
  8  | 
  9  | for(const [id,condition] of [
  10 |   ['AUTH-118','missing access credential'],['AUTH-119','malformed access credential'],['AUTH-120','invalid signature'],
  11 |   ['AUTH-121','expired access credential'],['AUTH-122','wrong issuer'],['AUTH-123','revoked session identifier'],
  12 | ] as const){
  13 |   test(`${id} declared validation rejection clears UI`,async({page,audit})=>{
  14 |     let release!:()=>void;const held=new Promise<void>(resolve=>{release=resolve;});let pending=false;
  15 |     await runSessionCase(page,audit,id,{}, {
  16 |       3:async()=>{
  17 |         await page.route('**/api/auth/v2/sso/validate',async route=>{pending=true;await held;await route.fulfill({status:401,json:{message:'TOKEN_INVALID_EXPIRED'}});});
  18 |         await page.evaluate(async condition=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');
  19 |           const fixture=condition==='missing access credential'?undefined:`UNTRUSTED_FIXTURE_${condition.replaceAll(' ','_')}`;
  20 |           void m.Service.postService('/auth/v2/sso/validate',{singleUIAuthorization:fixture}).catch(()=>{});},condition);
  21 |         await expect.poll(()=>pending).toBe(true);await audit.record('validation-input',{condition,responseSubstitution:'TOKEN_INVALID_EXPIRED',serverEnforcement:'NOT_VERIFIED'});
  22 |       },
  23 |       4:async()=>{expect(pending).toBe(true);},5:async()=>{release();},
  24 |     });
  25 |   });
  26 | }
  27 | for(const [id,condition] of [['AUTH-124','missing'],['AUTH-125','access-as-refresh'],['AUTH-126','expired'],['AUTH-127','revoked']] as const){
  28 |   test(`${id} declared recovery rejection clears UI`,async({page,audit})=>{
  29 |     await runSessionCase(page,audit,id,{accessExpires:0,refreshExpires:600},{
  30 |       5:async()=>{await audit.record('recovery-request-substitution',{condition,substitutionBoundary:'Controlled upstream response adapter',realServerValidation:'NOT_VERIFIED'});},
  31 |       6:async s=>{s.control.reloginError='TOKEN_INVALID_EXPIRED';},7:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
  32 |     });
  33 |   });
  34 | }
  35 | for(const id of ['AUTH-130','AUTH-132','AUTH-133','AUTH-135'] as const){
  36 |   test(`${id} controlled service error presentation`,async({page,audit})=>{
  37 |     let release!:()=>void;const held=new Promise<void>(resolve=>{release=resolve;});let pending=false;let before:string[]=[];
  38 |     const path=id==='AUTH-135'?'/sse/audit-probe':'/audit/protected-probe';
  39 |     await runSessionCase(page,audit,id,{}, {
  40 |       3:async()=>{
  41 |         before=await alert(page).allTextContents();
  42 |         await page.route(`**/api${path}`,async route=>{pending=true;await held;await route.fulfill({status:503,json:id==='AUTH-130'?{message:'SYNTHETIC_SECRET_AUTH_130'}:id==='AUTH-132'?{message:'Primary error',errorMessage:'Secondary error'}:{message:'Fixture unavailable'}});});
  43 |         await page.evaluate(async({path,cancel})=>{
  44 |           const m=await(window as unknown as SystemWindow).System.import('@fm/base');const controller=new AbortController();
  45 |           (window as unknown as {auditAbort?:AbortController}).auditAbort=controller;
  46 |           void m.Service.postService(path,{},cancel?{signal:controller.signal}:undefined).catch(()=>{});
  47 |         },{path,cancel:id==='AUTH-133'});
  48 |         await expect.poll(()=>pending).toBe(true);
  49 |         await audit.record('error-fixture',{path,response:id==='AUTH-130'?'SYNTHETIC_SECRET_AUTH_130':id==='AUTH-132'?'Primary error / Secondary error':'Fixture unavailable',beforeAlerts:before});
  50 |       },
  51 |       4:async()=>{if(id==='AUTH-133')await page.evaluate(()=>{(window as unknown as {auditAbort?:AbortController}).auditAbort?.abort();});else release();},
  52 |       ...(id==='AUTH-130'?{
> 53 |         5:async()=>{await expect(alert(page)).toBeVisible();await expect(page.locator('body')).not.toContainText('SYNTHETIC_SECRET_AUTH_130');},
     |                                                                                                    ^ Error: expect(locator).not.toContainText(expected) failed
  54 |         6:async()=>{await expect(alert(page)).toBeVisible();},
  55 |       }:id==='AUTH-132'?{
  56 |         6:async()=>{await expect(alert(page)).not.toContainText('Secondary error');},
  57 |       }:id==='AUTH-133'?{
  58 |         5:async()=>{expect(await alert(page).allTextContents()).toEqual(before);},6:async()=>{await expect.poll(async()=> (await observe(page)).isLoading).toBe(false);},
  59 |       }:{6:async()=>{expect(await alert(page).allTextContents()).toEqual(before);}}),
  60 |     });
  61 |   });
  62 | }
  63 | test('AUTH-134 failed analytics leaves theme and alerts intact',async({page,audit})=>{
  64 |   let release!:()=>void;const held=new Promise<void>(resolve=>{release=resolve;});const bodies:unknown[]=[];let before:string[]=[];
  65 |   await runSessionCase(page,audit,'AUTH-134',{}, {
  66 |     3:async s=>{await s.portal.expectThemeLight(false);before=await alert(page).allTextContents();await page.route('**/api/analytics/v1/fmo/print',async route=>{bodies.push(route.request().postDataJSON());await held;await route.fulfill({status:503,json:{message:'Fixture analytics unavailable'}});});},
  67 |     4:async s=>{await s.portal.themeCheckbox.check({force:true});},
  68 |     5:async()=>{await expect.poll(()=>bodies.length).toBeGreaterThan(0);expect(JSON.stringify(bodies)).toContain('toggle theme');expect(JSON.stringify(bodies)).toContain('switch');await audit.record('analytics-requests',bodies);},
  69 |     6:async()=>{release();},8:async s=>{await s.portal.expectThemeLight(true);},9:async()=>{expect(await alert(page).allTextContents()).toEqual(before);},
  70 |   });
  71 | });
  72 | 
```