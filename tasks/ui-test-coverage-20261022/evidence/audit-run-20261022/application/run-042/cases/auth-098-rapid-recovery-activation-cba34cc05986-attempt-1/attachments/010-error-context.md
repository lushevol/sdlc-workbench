# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-remaining.spec.ts >> AUTH-098 rapid recovery activation
- Location: e2e/audit-specs/auth-remaining.spec.ts:43:1

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
  1  | import {test,expect} from '../support/audit-fixture.js';
  2  | import {at,commonAssertion,equalsToken,observe,rotate,runSessionCase,sessionSetup,sessionToken,T,visibility,type Session,type SystemWindow} from '../support/auth-session.js';
  3  | import {localPrefix} from '../support/local-app.js';
  4  | const leave=(s:Session)=>s.portal.page.getByRole('dialog',{name:'Leave Now?',exact:true});
  5  | async function openLeave(s:Session){await s.portal.avatarButton.click({force:true});await s.portal.logoutMenuItem.click({force:true});await expect(leave(s)).toBeVisible();}
  6  | async function logout(s:Session){await openLeave(s);await leave(s).getByRole('button',{name:'Logout',exact:true}).click({force:true});await s.portal.page.clock.runFor(1000);}
  7  | const B=sessionToken(1200,'B');
  8  | test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',serviceWorkers:'block',auditFixture:'Actual MFE with controlled HTTP responses, clock, visibility and popup boundary. Browser-only unsigned credentials. No real provider or server security acceptance.'});
  9  | for(const id of ['AUTH-062','AUTH-063']as const){
  10 |  test(`${id} access acquisition race`,async({page,audit})=>{
  11 |   let aborted:AbortSignal|undefined;let old:any;let R=sessionToken(13524,'B-R');
  12 |   await runSessionCase(page,audit,id,{}, {
  13 |    4:async s=>{s.control.holdAcquisition=true;await s.startAcquire();await expect.poll(()=>s.acquisition.length).toBe(1);old=s.acquisition[0];
  14 |     await page.evaluate(async()=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');(window as unknown as {oldAuditSignal:AbortSignal}).oldAuditSignal=m.Service.signal.getRefreshToken!.signal;});
  15 |     await rotate(page,B);
  16 |     if(id==='AUTH-063'){await visibility(page,'hidden');await expect.poll(()=>s.acquisition.length).toBe(2);const current=s.acquisition.pop()!;await current.fulfill({status:200,headers:{'single-ui-refresh':R},json:{result:true}});await visibility(page,'visible');}
  17 |    },
  18 |    ...(id==='AUTH-062'?{
  19 |     5:async s=>{s.requests.length=0;},6:async()=>{await visibility(page,'hidden');},
  20 |     7:async()=>{expect(await page.evaluate(()=>(window as unknown as {oldAuditSignal:AbortSignal}).oldAuditSignal.aborted)).toBe(true);},
  21 |     9:async s=>{expect(s.requests.find(x=>x.endpoint==='refreshtoken')?.accessMatchesB).toBe(true);},
  22 |     10:async s=>{await s.acceptAcquisition(R);},11:async()=>{await visibility(page,'visible');},13:async()=>{expect(await equalsToken(page,'token',B)).toBe(true);},
  23 |    }:{
  24 |     5:async()=>{await old.fulfill({status:200,headers:{'single-ui-refresh':sessionToken(13524,'obsolete-A')},json:{result:true}}).catch(async(e:Error)=>{await audit.record('cancelled-late-transport',{error:e.message});});},
  25 |     6:async()=>{expect(await equalsToken(page,'token',B)).toBe(true);},7:async()=>{expect(await equalsToken(page,'refreshToken',R)).toBe(true);},
  26 |    }),
  27 |   });
  28 |  });
  29 | }
  30 | test('AUTH-093 logout blocks renewal paths',async({page,audit})=>{
  31 |  await runSessionCase(page,audit,'AUTH-093',{accessExpires:0,refreshExpires:600},{
  32 |   5:async s=>{await s.portal.sessionTimeoutDialog.logoutButton.click({force:true});expect((await observe(page)).isOnLogout).toBe(true);s.requests.length=0;},
  33 |   6:async()=>{await visibility(page,'hidden');},7:async()=>{await page.evaluate(async()=>{(await(window as unknown as SystemWindow).System.import('@fm/base')).ExtendService.extendToken();});},
  34 |   12:async()=>{await page.clock.runFor(1000);},
  35 |  });
  36 | });
  37 | test('AUTH-097 late recovery cannot restore logout',async({page,audit})=>{
  38 |  await runSessionCase(page,audit,'AUTH-097',{accessExpires:0,refreshExpires:600},{
  39 |   3:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});await expect.poll(()=>s.relogin.length).toBe(1);await logout(s);await s.login.expectVisible();},
  40 |   4:async s=>{await s.acceptRelogin();},
  41 |  });
  42 | });
  43 | test('AUTH-098 rapid recovery activation',async({page,audit})=>{
  44 |  let transitions=0;
  45 |  await runSessionCase(page,audit,'AUTH-098',{accessExpires:0,refreshExpires:600},{
  46 |   5:async s=>{expect(s.relogin.length).toBe(0);},6:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
> 47 |   7:async s=>{await expect(s.portal.sessionTimeoutDialog.extendButton).toBeVisible();await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
     |                                                                        ^ Error: expect(locator).toBeVisible() failed
  48 |   8:async s=>{await s.acceptRelogin();transitions++;},9:async()=>{expect(transitions).toBeLessThanOrEqual(1);},
  49 |   11:async()=>{await expect(page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toHaveCount(0);},
  50 |  });
  51 | });
  52 | test('AUTH-099 malformed refresh timeout mount',async({page,audit})=>{
  53 |  const steps=await audit.defineCase('AUTH-099');let s!:Session;
  54 |  for(const step of steps)await audit.step(step.number,async()=>{
  55 |   if(step.number===1){s=await sessionSetup(page,audit,{accessExpires:1,refreshExpires:600});await page.evaluate(async()=>{(await(window as unknown as SystemWindow).System.import('@fm/base')).LoginUtil.setRefreshToken('Bearer fixture.not-json.fixture');});return;}
  56 |   if(step.number===2){await page.clock.runFor(1000);return;}
  57 |   if(step.text.includes('authentication error')){await expect(page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toBeVisible();return;}
  58 |   if(!await commonAssertion(page,s,step.text))throw new Error(`Missing099step${step.number}`);
  59 |  });
  60 | });
  61 | for(const id of ['AUTH-104','AUTH-105','AUTH-106']as const){
  62 |  test(`${id} feedback popup boundary`,async({page,audit})=>{
  63 |   let calls:{url:string,name:string}[]=[];
  64 |   await runSessionCase(page,audit,id,{}, {
  65 |    3:openLeave,
  66 |    4:async()=>{await page.evaluate(blocked=>{const w=window as unknown as {auditPopupCalls:{url:string,name:string}[]};w.auditPopupCalls=[];window.open=((url?:string|URL,target?:string)=>{w.auditPopupCalls.push({url:String(url),name:String(target)});return blocked?null:{focus(){}} as Window;})as typeof window.open;},id==='AUTH-106');
  67 |     await audit.record('popup-boundary',{mode:id==='AUTH-106'?'Blocked window.open returns null':'Allowed window.open returns focusable synthetic popup',limit:'Popup creation boundary is controlled; external survey rendering is not measured.'});},
  68 |    5:async s=>{await leave(s).getByRole('button',{name:id==='AUTH-104'?'Share Feedback':'Share Feedback & Logout',exact:true}).click({force:true});},
  69 |    ...(id==='AUTH-106'?{6:async()=>{await page.clock.runFor(1000);}}:{
  70 |     6:async()=>{calls=await page.evaluate(()=>(window as unknown as {auditPopupCalls:{url:string,name:string}[]}).auditPopupCalls);expect(calls).toHaveLength(1);expect(calls[0].name).toBe('surveyLink');expect(calls[0].url).toMatch(/^https?:/);await audit.record('popup-request',calls);},
  71 |     ...(id==='AUTH-104'?{7:async s=>{await expect(leave(s)).toHaveCount(0);},9:async s=>{expect(s.count('logout')).toBe(0);}}:{7:async()=>{await page.clock.runFor(1000);}}),
  72 |    }),
  73 |   });
  74 |  });
  75 | }
  76 | 
```