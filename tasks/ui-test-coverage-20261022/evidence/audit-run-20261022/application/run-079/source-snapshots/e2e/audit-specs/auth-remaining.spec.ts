import type {Page} from '@playwright/test';
import {test,expect} from '../support/audit-fixture.js';
import {at,commonAssertion,equalsToken,observe,rotate,runSessionCase,sessionSetup,sessionToken,T,visibility,type Session,type SessionStore,type SystemWindow} from '../support/auth-session.js';
import {localPrefix} from '../support/local-app.js';
const leave=(s:Session)=>s.portal.page.getByRole('dialog',{name:'Leave Now?',exact:true});
async function openLeave(s:Session){await s.portal.avatarButton.click({force:true});await s.portal.logoutMenuItem.click({force:true});await expect(leave(s)).toBeVisible();}
async function logout(s:Session){await openLeave(s);await leave(s).getByRole('button',{name:'Logout',exact:true}).click({force:true});await s.portal.page.clock.runFor(1000);}
const B=sessionToken(1200,'B');
test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',serviceWorkers:'block',auditFixture:'Actual MFE with controlled HTTP responses, clock, visibility and popup boundary. Browser-only unsigned credentials. No real provider or server security acceptance.'});
for(const id of ['AUTH-062','AUTH-063']as const){
 test(`${id} access acquisition race`,async({page,audit})=>{
  let aborted:AbortSignal|undefined;let old:any;let R=sessionToken(13524,'B-R');
  await runSessionCase(page,audit,id,{}, {
   4:async s=>{s.control.holdAcquisition=true;await s.startAcquire();await expect.poll(()=>s.acquisition.length).toBe(1);old=s.acquisition[0];
    await page.evaluate(async()=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');(window as unknown as {oldAuditSignal:AbortSignal}).oldAuditSignal=m.Service.signal.getRefreshToken!.signal;});
    await rotate(page,B);
    if(id==='AUTH-063'){await visibility(page,'hidden');await expect.poll(()=>s.acquisition.length).toBe(2);const current=s.acquisition.pop()!;await current.fulfill({status:200,headers:{'single-ui-refresh':R},json:{result:true}});await visibility(page,'visible');}
   },
   ...(id==='AUTH-062'?{
    5:async s=>{s.requests.length=0;},6:async()=>{await visibility(page,'hidden');},
    7:async()=>{expect(await page.evaluate(()=>(window as unknown as {oldAuditSignal:AbortSignal}).oldAuditSignal.aborted)).toBe(true);},
    9:async s=>{expect(s.requests.find(x=>x.endpoint==='refreshtoken')?.accessMatchesB).toBe(true);},
    10:async s=>{await s.acceptAcquisition(R);},11:async()=>{await visibility(page,'visible');},13:async()=>{expect(await equalsToken(page,'token',B)).toBe(true);},
   }:{
    5:async()=>{await old.fulfill({status:200,headers:{'single-ui-refresh':sessionToken(13524,'obsolete-A')},json:{result:true}}).catch(async(e:Error)=>{await audit.record('cancelled-late-transport',{error:e.message});});},
    6:async()=>{expect(await equalsToken(page,'token',B)).toBe(true);},7:async()=>{expect(await equalsToken(page,'refreshToken',R)).toBe(true);},
   }),
  });
 });
}
test('AUTH-093 logout blocks renewal paths',async({page,audit})=>{
 await runSessionCase(page,audit,'AUTH-093',{accessExpires:0,refreshExpires:600},{
  5:async s=>{await s.portal.sessionTimeoutDialog.logoutButton.click({force:true});expect((await observe(page)).isOnLogout).toBe(true);s.requests.length=0;},
  6:async()=>{await visibility(page,'hidden');},7:async()=>{await page.evaluate(async()=>{(await(window as unknown as SystemWindow).System.import('@fm/base')).ExtendService.extendToken();});},
  12:async()=>{await page.clock.runFor(1000);},
 });
});
test('AUTH-097 late recovery cannot restore logout',async({page,audit})=>{
 await runSessionCase(page,audit,'AUTH-097',{accessExpires:0,refreshExpires:600},{
  3:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});await expect.poll(()=>s.relogin.length).toBe(1);await logout(s);await s.login.expectVisible();},
  4:async s=>{await s.acceptRelogin();},
 });
});
test('AUTH-098 rapid recovery activation',async({page,audit})=>{
 await runSessionCase(page,audit,'AUTH-098',{accessExpires:0,refreshExpires:600},{
  5:async s=>{
   expect(s.relogin.length).toBe(0);
   const initial=await page.evaluate(async()=>{
    const m=await(window as unknown as SystemWindow).System.import('@fm/base');
    const hooks=m.Hooks.getHooks() as {store:SessionStore;setStore(store:SessionStore):void};
    const project=(store:SessionStore)=>({time:Date.now(),authenticated:Boolean(store.token)&&Number(store.expiredIn)*1000>Date.now()&&!store.isOnLogout});
    const observations=[project(hooks.store)];
    (window as unknown as {auditRecoveryStates:typeof observations}).auditRecoveryStates=observations;
    const original=hooks.setStore;
    hooks.setStore=function(store){original.call(this,store);observations.push(project(this.store));};
    return observations[0];
   });
   expect(initial.authenticated).toBe(false);
   await audit.record('recovery-observer',{initial,method:'Call-through observer on actual Hooks.setStore.',predicate:'A present unexpired access token with isOnLogout=false.',limit:'This measures effective browser authentication state. It does not establish server authentication or an approved anonymous-state policy.'});
  },6:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
  7:async s=>{await expect(s.portal.sessionTimeoutDialog.extendButton).toBeVisible();await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
  8:async s=>{await s.acceptRelogin();await expect.poll(()=>equalsToken(page,'token',sessionToken(900,'B'))).toBe(true);},
  9:async()=>{
   const states=await page.evaluate(()=>(window as unknown as {auditRecoveryStates:{time:number;authenticated:boolean}[]}).auditRecoveryStates);
   const transitions=states.slice(1).filter((state,index)=>state.authenticated&&!states[index].authenticated).length;
   await audit.record('observed-recovery-transitions',{states,transitions});
   expect(transitions).toBeLessThanOrEqual(1);
  },
  11:async()=>{await expect(page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toHaveCount(0);},
 });
});
test('AUTH-099 malformed refresh timeout mount',async({page,audit})=>{
 const steps=await audit.defineCase('AUTH-099');let s!:Session;
 for(const step of steps)await audit.step(step.number,async()=>{
  if(step.number===1){s=await sessionSetup(page,audit,{accessExpires:1,refreshExpires:600});await page.evaluate(async()=>{(await(window as unknown as SystemWindow).System.import('@fm/base')).LoginUtil.setRefreshToken('Bearer fixture.not-json.fixture');});return;}
  if(step.number===2){await page.clock.runFor(1000);return;}
  if(step.text.includes('authentication error')){await expect(page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toBeVisible();return;}
  if(!await commonAssertion(page,s,step.text))throw new Error(`Missing099step${step.number}`);
 });
});
for(const id of ['AUTH-104','AUTH-105','AUTH-106']as const){
 test(`${id} feedback popup boundary`,async({page,audit})=>{
  let calls:{url:string,name:string}[]=[];let popups:Page[]=[];const surveyUrl='https://surveys.sc.com/jfe/preview/previewId/b35e7b90-467e-473f-9ff3-8b6a099569d5/SV_cUVyvBdVELMVr02?Q_CHL=preview&Q_SurveyVersionID=current';
  await runSessionCase(page,audit,id,{}, {
   3:openLeave,
   4:async()=>{
    if(id==='AUTH-106')await page.evaluate(()=>{window.open=(()=>null)as typeof window.open;});
    else {await page.context().route('https://surveys.sc.com/**',route=>route.fulfill({status:200,contentType:'text/html',body:'<main><h1>Controlled local survey destination</h1></main>'}));page.on('popup',popup=>popups.push(popup));}
    await audit.record('popup-boundary',{mode:id==='AUTH-106'?'Blocked window.open returns null':'Native browser popup; external destination fulfilled locally',limit:'External survey content is substituted.'});},
   5:async s=>{await leave(s).getByRole('button',{name:id==='AUTH-104'?'Share Feedback':'Share Feedback & Logout',exact:true}).click({force:true});},
   ...(id==='AUTH-106'?{6:async()=>{await page.clock.runFor(1000);}}:{
    6:async()=>{await expect.poll(()=>popups.length).toBe(1);await expect.poll(()=>popups[0].url()).toBe(surveyUrl);expect(await popups[0].evaluate(()=>window.name)).toBe('surveyLink');await audit.record('popup-request',{name:'surveyLink',url:popups[0].url(),nativePopup:true});},
    ...(id==='AUTH-104'?{7:async s=>{await expect(leave(s)).toHaveCount(0);},9:async s=>{expect(s.count('logout')).toBe(0);}}:{7:async()=>{await page.clock.runFor(1000);}}),
   }),
  });
 });
}
