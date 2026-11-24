# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-final.spec.ts >> AUTH-144 forged entitlement is rejected by current server
- Location: e2e/audit-specs/auth-final.spec.ts:76:1

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText(/^(?:new|edit|verify|deactivate) ID:/) })
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText(/^(?:new|edit|verify|deactivate) ID:/) }) with timeout 5000ms
  - waiting for locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText(/^(?:new|edit|verify|deactivate) ID:/) })

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 05:55 UTC
  - checkbox "Time Switch" [checked]
- button "User Profiles": A
- button "Share Feedback"
- main:
  - tablist "workspaces":
    - tab "Category" [selected]:
      - region "Category":
        - textbox "Workspace Name": Category
        - button "refresh"
    - button "Add Workspace"
  - tabpanel:
    - button "Create New Category"
    - grid:
      - button "Export"
      - rowgroup:
        - row "Actions Category Label Owner Verified? Updated At Updated By Record Id Order No":
          - columnheader "Actions"
          - columnheader "Category Label"
          - columnheader "Owner"
          - columnheader "Verified?"
          - columnheader "Updated At"
          - columnheader "Updated By"
          - columnheader "Record Id"
          - columnheader "Order No"
      - rowgroup:
        - row "Fixture Category TEST_OWNER Oct 22, 2026, 12:05:00 AM UI-ADMIN-01 101 7":
          - cell:
            - menu:
              - menuitem "Edit"
              - menuitem "Verify"
              - menuitem "Deactivate" [disabled]
              - menuitem "Audit"
          - cell "Fixture Category"
          - cell "TEST_OWNER"
          - cell
          - cell "Oct 22, 2026, 12:05:00 AM"
          - cell "UI-ADMIN-01"
          - cell "101"
          - cell "7"
      - paragraph: "Rows per page:"
      - 'combobox "Rows per page: 20"': "20"
      - paragraph: 1–1 of 1
      - button "Go to previous page" [disabled]
      - button "Go to next page" [disabled]
- alert:
  - alert: "Error happened, service is unavailable, pls check with support team: /api/auth/v1/fmo/admin/category/update: API request failed"
  - button "Close"
```

# Test source

```ts
  1   | import type {Page} from '@playwright/test';
  2   | import {test,expect} from '../support/audit-fixture.js';
  3   | import {commonAssertion,equalsToken,observe,rotate,runSessionCase,sessionSetup,sessionToken,T,visibility,type Session,type SystemWindow} from '../support/auth-session.js';
  4   | import {blockExternal,localBase,localPrefix,openLogin,seedWorkspaces,workspace} from '../support/local-app.js';
  5   | import {AdminApp} from '../support/admin-app.js';
  6   | import {LoginPage} from '../pages/login.page.js';
  7   | test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',serviceWorkers:'block',auditFixture:'Actual MFE; controlled identity, catalog, API responses and browser time. Signed current-BFF validation is used only where declared. Synthetic credentials and user aliases; no real identity provider acceptance.'});
  8   | const entity=(name='ENTITY-A')=>({id:1,name,applicationName:'Fixture',roleId:1,roleName:'Viewer',subjects:[]});
  9   | const drawer=[{id:1,label:'ENTITY-A catalog',tiles:[{title:'ENTITY-A App',container:'@fm/unused',module:'/unused',tile:'/unused',entity:['ENTITY-A'],subject:'',isTemplate:true}]}];
  10  | async function setCatalog(page:Page){await page.evaluate(async data=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base')as any;m.LoginUtil.handleEntities({data:{entities:[data.entity]}});m.LoginUtil.handleDrawers({data:{drawers:data.drawers}});},{entity:entity(),drawers:drawer});}
  11  | async function logout(s:Session){await s.portal.avatarButton.click({force:true});await s.portal.logoutMenuItem.click({force:true});await s.portal.page.getByRole('dialog',{name:'Leave Now?',exact:true}).getByRole('button',{name:'Logout',exact:true}).click({force:true});await s.portal.page.clock.runFor(1000);await s.login.expectVisible();}
  12  | async function acceptLogin(page:Page,access:string,user='user-a',entities=[entity()],drawers=drawer){await page.route('**/api/auth/v2/sso/login',route=>route.fulfill({status:200,headers:{'single-ui-authorization':access},json:{result:true,userInfo:JSON.stringify({sub:user,fullName:user}),entities,drawers}}));}
  13  | test('AUTH-066 short access Home mount acquires recovery',async({page,audit})=>{
  14  |  const steps=await audit.defineCase('AUTH-066');let s!:Session;const R=sessionToken(600,'R'),B=sessionToken(900,'recovered');
  15  |  for(const step of steps)await audit.step(step.number,async()=>{
  16  |   if(step.number===1){s=await sessionSetup(page,audit,{accessExpires:10,holdInitialAcquisition:true,clockStartAtT:true,preserveInitialRequests:true});return;}
  17  |   if(step.number===2){expect((await observe(page)).refreshPresent).toBe(false);return;}
  18  |   if(step.number===3){await s.portal.expectVisible();return;}
  19  |   if(step.number===4){await page.clock.runFor(0);await expect.poll(()=>s.count('refreshtoken')).toBe(1);return;}
  20  |   if(step.number===5){await s.acceptAcquisition(R);return;}
  21  |   if(step.number===6){await page.clock.runFor(10000);return;}
  22  |   if(step.number===8){await s.portal.sessionTimeoutDialog.extendButton.click({force:true});return;}
  23  |   if(step.number===9){await expect.poll(()=>s.count('relogin')).toBe(1);return;}
  24  |   if(step.number===10){expect(await page.evaluate(async r=>(await(window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store.refreshToken===r,R)).toBe(true);return;}
  25  |   if(step.number===11){await s.acceptRelogin(B);return;}
  26  |   if(step.number===13){await expect.poll(()=>equalsToken(page,'token',B)).toBe(true);return;}
  27  |   if(!await commonAssertion(page,s,step.text))throw new Error(`Missing066step${step.number}`);
  28  |  });
  29  | });
  30  | test('AUTH-112 fresh login acquires distinct recovery',async({page,audit})=>{
  31  |  const steps=await audit.defineCase('AUTH-112');let s!:Session;const B=sessionToken(1200,'SESSION-B'),RB=sessionToken(14000,'R-B');
  32  |  for(const step of steps)await audit.step(step.number,async()=>{
  33  |   if(step.number===1){s=await sessionSetup(page,audit,{refreshExpires:13524,expectedAcquisitionAccess:B});await logout(s);return;}
  34  |   if(step.number===2){await s.login.expectVisible();return;}
  35  |   if(step.number===3){await acceptLogin(page,B);s.control.holdAcquisition=true;s.requests.length=0;return;}
  36  |   if(step.number===4){await s.login.fillUsername('user-a');return;}
  37  |   if(step.number===5){await s.login.fillPassword('FixturePass1!');return;}
  38  |   if(step.number===6){await s.login.clickSignInButton();return;}
  39  |   if(step.number===8){await visibility(page,'hidden');return;}
  40  |   if(step.number===9){await expect.poll(()=>s.count('refreshtoken')).toBe(1);expect(s.requests.find(x=>x.endpoint==='refreshtoken')?.accessMatchesB).toBe(true);return;}
  41  |   if(step.number===10){await s.acceptAcquisition(RB);return;}
  42  |   if(step.number===11){await expect.poll(()=>equalsToken(page,'refreshToken',RB)).toBe(true);expect(RB).not.toBe(s.refreshR);return;}
  43  |   if(!await commonAssertion(page,s,step.text))throw new Error(`Missing112step${step.number}`);
  44  |  });
  45  | });
  46  | test('AUTH-117 stale prior-user response cannot overwrite new user',async({page,audit})=>{
  47  |  let release!:()=>void;const held=new Promise<void>(resolve=>{release=resolve;});let pending=false;
  48  |  await runSessionCase(page,audit,'AUTH-117',{}, {
  49  |   3:async s=>{await page.route('**/api/audit/prior-user',async route=>{pending=true;await held;await route.fulfill({status:200,headers:{'single-ui-authorization':s.accessA},json:{userInfo:JSON.stringify({sub:'user-a'}),entities:[entity()]}});});
  50  |    await page.evaluate(async()=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');void m.Service.postService('/audit/prior-user',{}).catch(()=>{});});await expect.poll(()=>pending).toBe(true);await logout(s);await acceptLogin(page,sessionToken(1200,'user-b'),'user-b');await s.login.fillUsername('user-b');await s.login.fillPassword('FixturePass1!');await s.login.clickSignInButton();await s.portal.expectVisible();},
  51  |   4:async()=>{release();},5:async s=>{await s.portal.avatarButton.click({force:true});},6:async s=>{await s.portal.avatarMenu.getByRole('menuitem').filter({hasText:'user-b'}).click({force:true});},
  52  |   7:async()=>{await expect(page.getByTestId('entitlement-profile-label-box').locator('.MuiTypography-h5')).toHaveText('user-b');},
  53  |   8:async()=>{const identity=await page.evaluate(async()=>{const s=(await(window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store as any;return s.user?.sub;});expect(identity).toBe('user-b');},
  54  |  });
  55  | });
  56  | test('AUTH-138 recovery removes old entity and controls',async({page,audit})=>{
  57  |  await runSessionCase(page,audit,'AUTH-138',{accessExpires:0,refreshExpires:600},{
  58  |   5:async()=>{await setCatalog(page);},6:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
  59  |   7:async s=>{for(const route of s.relogin.splice(0))await route.fulfill({status:200,headers:{'single-ui-authorization':sessionToken(900,'B')},json:{result:true,entities:[],userInfo:JSON.stringify({sub:'user-a',fullName:'user-a'})}});},8:async s=>{await s.portal.root.getByText('New Tile',{exact:true}).click({force:true});await expect(page.getByText('ENTITY-A App',{exact:true})).toHaveCount(0);},
  60  |   9:async s=>{await s.portal.avatarButton.click({force:true});},10:async s=>{await s.portal.avatarMenu.getByRole('menuitem').filter({hasText:'user-a'}).click({force:true});},
  61  |   11:async()=>{await expect(page.getByTestId('entitlement-profile-label-box').locator('.MuiTypography-h5')).toHaveText('user-a');},12:async()=>{expect(await page.evaluate(async()=>JSON.stringify((await(window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store.entities))).not.toContain('ENTITY-A');},
  62  |  });
  63  | });
  64  | test('AUTH-137 empty new login removes old catalog',async({page,audit})=>{
  65  |  const steps=await audit.defineCase('AUTH-137');const login=new LoginPage(page,localPrefix);
  66  |  for(const step of steps)await audit.step(step.number,async()=>{
  67  |   if(step.number===1){await blockExternal(page);await seedWorkspaces(page,[workspace('WS-A','WS-A')]);await openLogin(page);return;}
  68  |   if(step.number===2){await setCatalog(page);await acceptLogin(page,sessionToken(1200,'new'),'user-a',[],[]);return;}
  69  |   if(step.number===3){await login.fillUsername('user-a');return;}
  70  |   if(step.number===4){await login.fillPassword('FixturePass1!');return;}
  71  |   if(step.number===5){await login.clickSignInButton();return;}
  72  |   if(step.number===6){await page.getByText('New Tile',{exact:true}).click({force:true});await expect(page.getByText('ENTITY-A App',{exact:true})).toHaveCount(0);return;}
  73  |   if(step.number===7){expect(await page.evaluate(async()=>JSON.stringify((await(window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store as any))).not.toContain('ENTITY-A App');return;}
  74  |  });
  75  | });
  76  | test('AUTH-144 forged entitlement is rejected by current server',async({page,audit})=>{
  77  |  const steps=await audit.defineCase('AUTH-144');const app=new AdminApp(page,'Category','AUTH-144');let status=0;
  78  |  for(const step of steps)await audit.step(step.number,async()=>{
  79  |   if(step.number===1){app.principal='user-a';await app.setup();await app.open();return;}
  80  |   if(step.number===2){await app.portal.expectVisible();return;}
  81  |   if(step.number===3){const token=await page.request.post('http://127.0.0.1:8090/api/auth/local/fixture/token',{data:{subject:'user-a',expiresInSeconds:600}});await rotate(page,(await token.json()).token);await audit.record('forged-entitlement',{accessSignature:'Valid local server-signed fixture',entitlementSignature:'Unsigned forged admin fixture from AdminApp',target:'Actual Category editor update control; canonical exact identity remains unapproved'});
  82  |    await page.route('**/api/auth/v1/fmo/admin/category/update',async route=>{const response=await route.fetch({url:'http://127.0.0.1:8090/api/auth/v1/fmo/admin/category/update'});status=response.status();await route.fulfill({response});});return;}
  83  |   if(step.number===4){await app.action('Edit').click({force:true});await app.footerButton('Update').click({force:true});return;}
  84  |   if(step.number===5){await expect.poll(()=>status).toBeGreaterThanOrEqual(400);return;}
> 85  |   if(step.number===6){await expect(app.dialog()).toBeVisible();await audit.record('server-rejection',{status,sourceRevision:'834b4155232222347220e47139a502ee43a9cbdf'});return;}
      |                                                  ^ Error: expect(locator).toBeVisible() failed
  86  |  });
  87  | });
  88  | test('AUTH-116 independent contexts preserve separate server sessions',async({page,browser,audit},testInfo)=>{
  89  |  const steps=await audit.defineCase('AUTH-116');let a!:Session,b!:Session;let second:Page|undefined;let context:Awaited<ReturnType<typeof browser.newContext>>|undefined;let B='';let validation:any;
  90  |  const base='http://127.0.0.1:8090/api/auth';
  91  |  try{for(const step of steps)await audit.step(step.number,async()=>{
  92  |   if(step.number===1){a=await sessionSetup(page,audit,{});context=await browser.newContext({serviceWorkers:'block'});second=await context.newPage();b=await sessionSetup(second,audit,{});
  93  |    for(const [target,name]of [[page,'SESSION-A'],[second,'SESSION-B']]as const){const response=await target.request.post(`${base}/local/fixture/token`,{data:{id:`${name}-${Date.now()}`,expiresInSeconds:Math.ceil((T-Date.now())/1000)+900}});const token=(await response.json()).token;await rotate(target,token);if(name==='SESSION-B')B=token;}
  94  |    await page.route('**/api/auth/v2/sso/logout',async route=>{const response=await route.fetch({url:`${base}/v2/sso/logout`});await route.fulfill({response});});return;}
  95  |   if(step.number===2){await a.portal.avatarButton.click({force:true});await a.portal.logoutMenuItem.click({force:true});return;}
  96  |   if(step.number===3){await page.getByRole('dialog',{name:'Leave Now?',exact:true}).getByRole('button',{name:'Logout',exact:true}).click({force:true});return;}
  97  |   if(step.number===4){await page.clock.runFor(1000);return;}
  98  |   if(step.number===8){const response=await second!.request.post(`${base}/v2/sso/validate`,{data:{singleUIAuthorization:B}});validation=await response.json();await audit.record('context-b-validation',{status:response.status(),result:validation.result});return;}
  99  |   if(step.number===9){expect(validation.result).toBe(true);expect(await equalsToken(second!,'token',B)).toBe(true);return;}
  100 |   if(step.number===10){await b.portal.expectWorkspaceTabVisible('WS-A');const path=testInfo.outputPath('context-b-final.png');await second!.screenshot({path,fullPage:true});await testInfo.attach('CTX-B separate session visible',{path,contentType:'image/png'});return;}
  101 |   if(!await commonAssertion(page,a,step.text))throw new Error(`Missing116step${step.number}`);
  102 |  });}finally{await context?.close();}
  103 | });
  104 | 
```