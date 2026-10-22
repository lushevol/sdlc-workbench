# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-remaining.spec.ts >> AUTH-098 rapid recovery activation
- Location: e2e/audit-specs/auth-remaining.spec.ts:44:1

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByRole('dialog', { name: 'Your session has been expired', exact: true }).getByRole('button', { name: 'Extend', exact: true })
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" getByRole('dialog', { name: 'Your session has been expired', exact: true }).getByRole('button', { name: 'Extend', exact: true }) with timeout 5000ms
  - waiting for getByRole('dialog', { name: 'Your session has been expired', exact: true }).getByRole('button', { name: 'Extend', exact: true })

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
```

# Test source

```ts
  1  | import type {Page} from '@playwright/test';
  2  | import {test,expect} from '../support/audit-fixture.js';
  3  | import {at,commonAssertion,equalsToken,observe,rotate,runSessionCase,sessionSetup,sessionToken,T,visibility,type Session,type SystemWindow} from '../support/auth-session.js';
  4  | import {localPrefix} from '../support/local-app.js';
  5  | const leave=(s:Session)=>s.portal.page.getByRole('dialog',{name:'Leave Now?',exact:true});
  6  | async function openLeave(s:Session){await s.portal.avatarButton.click({force:true});await s.portal.logoutMenuItem.click({force:true});await expect(leave(s)).toBeVisible();}
  7  | async function logout(s:Session){await openLeave(s);await leave(s).getByRole('button',{name:'Logout',exact:true}).click({force:true});await s.portal.page.clock.runFor(1000);}
  8  | const B=sessionToken(1200,'B');
  9  | test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',serviceWorkers:'block',auditFixture:'Actual MFE with controlled HTTP responses, clock, visibility and popup boundary. Browser-only unsigned credentials. No real provider or server security acceptance.'});
  10 | for(const id of ['AUTH-062','AUTH-063']as const){
  11 |  test(`${id} access acquisition race`,async({page,audit})=>{
  12 |   let aborted:AbortSignal|undefined;let old:any;let R=sessionToken(13524,'B-R');
  13 |   await runSessionCase(page,audit,id,{}, {
  14 |    4:async s=>{s.control.holdAcquisition=true;await s.startAcquire();await expect.poll(()=>s.acquisition.length).toBe(1);old=s.acquisition[0];
  15 |     await page.evaluate(async()=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');(window as unknown as {oldAuditSignal:AbortSignal}).oldAuditSignal=m.Service.signal.getRefreshToken!.signal;});
  16 |     await rotate(page,B);
  17 |     if(id==='AUTH-063'){await visibility(page,'hidden');await expect.poll(()=>s.acquisition.length).toBe(2);const current=s.acquisition.pop()!;await current.fulfill({status:200,headers:{'single-ui-refresh':R},json:{result:true}});await visibility(page,'visible');}
  18 |    },
  19 |    ...(id==='AUTH-062'?{
  20 |     5:async s=>{s.requests.length=0;},6:async()=>{await visibility(page,'hidden');},
  21 |     7:async()=>{expect(await page.evaluate(()=>(window as unknown as {oldAuditSignal:AbortSignal}).oldAuditSignal.aborted)).toBe(true);},
  22 |     9:async s=>{expect(s.requests.find(x=>x.endpoint==='refreshtoken')?.accessMatchesB).toBe(true);},
  23 |     10:async s=>{await s.acceptAcquisition(R);},11:async()=>{await visibility(page,'visible');},13:async()=>{expect(await equalsToken(page,'token',B)).toBe(true);},
  24 |    }:{
  25 |     5:async()=>{await old.fulfill({status:200,headers:{'single-ui-refresh':sessionToken(13524,'obsolete-A')},json:{result:true}}).catch(async(e:Error)=>{await audit.record('cancelled-late-transport',{error:e.message});});},
  26 |     6:async()=>{expect(await equalsToken(page,'token',B)).toBe(true);},7:async()=>{expect(await equalsToken(page,'refreshToken',R)).toBe(true);},
  27 |    }),
  28 |   });
  29 |  });
  30 | }
  31 | test('AUTH-093 logout blocks renewal paths',async({page,audit})=>{
  32 |  await runSessionCase(page,audit,'AUTH-093',{accessExpires:0,refreshExpires:600},{
  33 |   5:async s=>{await s.portal.sessionTimeoutDialog.logoutButton.click({force:true});expect((await observe(page)).isOnLogout).toBe(true);s.requests.length=0;},
  34 |   6:async()=>{await visibility(page,'hidden');},7:async()=>{await page.evaluate(async()=>{(await(window as unknown as SystemWindow).System.import('@fm/base')).ExtendService.extendToken();});},
  35 |   12:async()=>{await page.clock.runFor(1000);},
  36 |  });
  37 | });
  38 | test('AUTH-097 late recovery cannot restore logout',async({page,audit})=>{
  39 |  await runSessionCase(page,audit,'AUTH-097',{accessExpires:0,refreshExpires:600},{
  40 |   3:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});await expect.poll(()=>s.relogin.length).toBe(1);await logout(s);await s.login.expectVisible();},
  41 |   4:async s=>{await s.acceptRelogin();},
  42 |  });
  43 | });
  44 | test('AUTH-098 rapid recovery activation',async({page,audit})=>{
  45 |  let transitions=0;
  46 |  await runSessionCase(page,audit,'AUTH-098',{accessExpires:0,refreshExpires:600},{
  47 |   5:async s=>{expect(s.relogin.length).toBe(0);},6:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
> 48 |   7:async s=>{await expect(s.portal.sessionTimeoutDialog.extendButton).toBeVisible();await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
     |                                                                        ^ Error: expect(locator).toBeVisible() failed
  49 |   8:async s=>{await s.acceptRelogin();transitions++;},9:async()=>{expect(transitions).toBeLessThanOrEqual(1);},
  50 |   11:async()=>{await expect(page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toHaveCount(0);},
  51 |  });
  52 | });
  53 | test('AUTH-099 malformed refresh timeout mount',async({page,audit})=>{
  54 |  const steps=await audit.defineCase('AUTH-099');let s!:Session;
  55 |  for(const step of steps)await audit.step(step.number,async()=>{
  56 |   if(step.number===1){s=await sessionSetup(page,audit,{accessExpires:1,refreshExpires:600});await page.evaluate(async()=>{(await(window as unknown as SystemWindow).System.import('@fm/base')).LoginUtil.setRefreshToken('Bearer fixture.not-json.fixture');});return;}
  57 |   if(step.number===2){await page.clock.runFor(1000);return;}
  58 |   if(step.text.includes('authentication error')){await expect(page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toBeVisible();return;}
  59 |   if(!await commonAssertion(page,s,step.text))throw new Error(`Missing099step${step.number}`);
  60 |  });
  61 | });
  62 | for(const id of ['AUTH-104','AUTH-105','AUTH-106']as const){
  63 |  test(`${id} feedback popup boundary`,async({page,audit})=>{
  64 |   let calls:{url:string,name:string}[]=[];let popups:Page[]=[];const surveyUrl='https://surveys.sc.com/jfe/preview/previewId/b35e7b90-467e-473f-9ff3-8b6a099569d5/SV_cUVyvBdVELMVr02?Q_CHL=preview&Q_SurveyVersionID=current';
  65 |   await runSessionCase(page,audit,id,{}, {
  66 |    3:openLeave,
  67 |    4:async()=>{
  68 |     if(id==='AUTH-106')await page.evaluate(()=>{window.open=(()=>null)as typeof window.open;});
  69 |     else {await page.context().route('https://surveys.sc.com/**',route=>route.fulfill({status:200,contentType:'text/html',body:'<main><h1>Controlled local survey destination</h1></main>'}));page.on('popup',popup=>popups.push(popup));}
  70 |     await audit.record('popup-boundary',{mode:id==='AUTH-106'?'Blocked window.open returns null':'Native browser popup; external destination fulfilled locally',limit:'External survey content is substituted.'});},
  71 |    5:async s=>{await leave(s).getByRole('button',{name:id==='AUTH-104'?'Share Feedback':'Share Feedback & Logout',exact:true}).click({force:true});},
  72 |    ...(id==='AUTH-106'?{6:async()=>{await page.clock.runFor(1000);}}:{
  73 |     6:async()=>{await expect.poll(()=>popups.length).toBe(1);await expect.poll(()=>popups[0].url()).toBe(surveyUrl);expect(await popups[0].evaluate(()=>window.name)).toBe('surveyLink');await audit.record('popup-request',{name:'surveyLink',url:popups[0].url(),nativePopup:true});},
  74 |     ...(id==='AUTH-104'?{7:async s=>{await expect(leave(s)).toHaveCount(0);},9:async s=>{expect(s.count('logout')).toBe(0);}}:{7:async()=>{await page.clock.runFor(1000);}}),
  75 |    }),
  76 |   });
  77 |  });
  78 | }
  79 | 
```