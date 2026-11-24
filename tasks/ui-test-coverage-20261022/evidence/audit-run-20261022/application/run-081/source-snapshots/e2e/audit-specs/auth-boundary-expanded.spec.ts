import { test, expect } from '../support/audit-fixture.js';
import { commonAssertion, equalsToken, observe, runSessionCase, sessionSetup, sessionToken, T, type Session, type SystemWindow } from '../support/auth-session.js';
import { localPrefix } from '../support/local-app.js';

test.use({ auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES', serviceWorkers:'block',
  auditFixture:'Actual MFE response handlers; controlled service rejection and cancellation. Signature enforcement, revocation, upstream identity, and service policy are not verified.' });
const alert=(page:Session['portal']['page'])=>page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]');

for(const [id,condition] of [
  ['AUTH-118','missing access credential'],['AUTH-119','malformed access credential'],['AUTH-120','invalid signature'],
  ['AUTH-121','expired access credential'],['AUTH-122','wrong issuer'],['AUTH-123','revoked session identifier'],
] as const){
  test(`${id} declared validation rejection clears UI`,async({page,audit})=>{
    let release!:()=>void;const held=new Promise<void>(resolve=>{release=resolve;});let pending=false;
    await runSessionCase(page,audit,id,{}, {
      3:async()=>{
        await page.route('**/api/auth/v2/sso/validate',async route=>{pending=true;await held;await route.fulfill({status:401,json:{message:'TOKEN_INVALID_EXPIRED'}});});
        await page.evaluate(async condition=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');
          const fixture=condition==='missing access credential'?undefined:`UNTRUSTED_FIXTURE_${condition.replaceAll(' ','_')}`;
          void m.Service.postService('/auth/v2/sso/validate',{singleUIAuthorization:fixture}).catch(()=>{});},condition);
        await expect.poll(()=>pending).toBe(true);await audit.record('validation-input',{condition,responseSubstitution:'TOKEN_INVALID_EXPIRED',serverEnforcement:'NOT_VERIFIED'});
      },
      4:async()=>{expect(pending).toBe(true);},5:async()=>{release();},
    });
  });
}
for(const [id,condition] of [['AUTH-124','missing'],['AUTH-125','access-as-refresh'],['AUTH-126','expired'],['AUTH-127','revoked']] as const){
  test(`${id} declared recovery rejection clears UI`,async({page,audit})=>{
    await runSessionCase(page,audit,id,{accessExpires:0,refreshExpires:600},{
      5:async()=>{await audit.record('recovery-request-substitution',{condition,substitutionBoundary:'Controlled upstream response adapter',realServerValidation:'NOT_VERIFIED'});},
      6:async s=>{s.control.reloginError='TOKEN_INVALID_EXPIRED';},7:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
    });
  });
}
for(const id of ['AUTH-130','AUTH-132','AUTH-133','AUTH-135'] as const){
  test(`${id} controlled service error presentation`,async({page,audit})=>{
    let release!:()=>void;const held=new Promise<void>(resolve=>{release=resolve;});let pending=false;let before:string[]=[];
    const path=id==='AUTH-135'?'/sse/audit-probe':'/audit/protected-probe';
    await runSessionCase(page,audit,id,{}, {
      3:async()=>{
        before=await alert(page).allTextContents();
        await page.route(`**/api${path}`,async route=>{pending=true;await held;await route.fulfill({status:503,json:id==='AUTH-130'?{message:'SYNTHETIC_SECRET_AUTH_130'}:id==='AUTH-132'?{message:'Primary error',errorMessage:'Secondary error'}:{message:'Fixture unavailable'}});});
        await page.evaluate(async({path,cancel})=>{
          const m=await(window as unknown as SystemWindow).System.import('@fm/base');const controller=new AbortController();
          (window as unknown as {auditAbort?:AbortController}).auditAbort=controller;
          void m.Service.postService(path,{},cancel?{signal:controller.signal}:undefined).catch(()=>{});
        },{path,cancel:id==='AUTH-133'});
        await expect.poll(()=>pending).toBe(true);
        await audit.record('error-fixture',{path,response:id==='AUTH-130'?'SYNTHETIC_SECRET_AUTH_130':id==='AUTH-132'?'Primary error / Secondary error':'Fixture unavailable',beforeAlerts:before});
      },
      4:async()=>{if(id==='AUTH-133')await page.evaluate(()=>{(window as unknown as {auditAbort?:AbortController}).auditAbort?.abort();});else release();},
      ...(id==='AUTH-130'?{
        5:async()=>{await expect(alert(page)).toBeVisible();await expect(page.locator('body')).not.toContainText('SYNTHETIC_SECRET_AUTH_130');},
        6:async()=>{await expect(alert(page)).toBeVisible();},
      }:id==='AUTH-132'?{
        6:async()=>{await expect(alert(page)).not.toContainText('Secondary error');},
      }:id==='AUTH-133'?{
        5:async()=>{expect(await alert(page).allTextContents()).toEqual(before);},6:async()=>{await expect.poll(async()=> (await observe(page)).isLoading).toBe(false);},
      }:{6:async()=>{expect(await alert(page).allTextContents()).toEqual(before);}}),
    });
  });
}
test('AUTH-134 failed analytics leaves theme and alerts intact',async({page,audit})=>{
  let release!:()=>void;const held=new Promise<void>(resolve=>{release=resolve;});const bodies:unknown[]=[];let before:string[]=[];
  await runSessionCase(page,audit,'AUTH-134',{}, {
    3:async s=>{await s.portal.expectThemeLight(false);before=await alert(page).allTextContents();await page.route('**/api/analytics/v1/fmo/print',async route=>{bodies.push(route.request().postDataJSON());await held;await route.fulfill({status:503,json:{message:'Fixture analytics unavailable'}});});},
    4:async s=>{await s.portal.themeCheckbox.check({force:true});},
    5:async()=>{await expect.poll(()=>bodies.length).toBeGreaterThan(0);expect(JSON.stringify(bodies)).toContain('toggle theme');expect(JSON.stringify(bodies)).toContain('switch');await audit.record('analytics-requests',bodies);},
    6:async()=>{release();},8:async s=>{await s.portal.expectThemeLight(true);},9:async()=>{expect(await alert(page).allTextContents()).toEqual(before);},
  });
});
