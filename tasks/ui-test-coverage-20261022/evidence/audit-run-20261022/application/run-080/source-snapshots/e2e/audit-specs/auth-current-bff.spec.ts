import type { APIResponse } from '@playwright/test';
import { test, expect } from '../support/audit-fixture.js';
import { runSessionCase, type Session, type SystemWindow } from '../support/auth-session.js';

const bff='http://127.0.0.1:8090/api/auth';
test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',serviceWorkers:'block',
  auditFixture:'Actual MFE handlers and exact-current BFF controller/JWT/JPA/PG source. Local synthetic OUD/EMS2, signing fixture, selected Spring Boot3 bootstrap. Production Boot4 wiring and remote providers are unverified.'});
async function signed(page:Session['portal']['page'],issuer='single-ui-bff',expiresInSeconds=600,id?:string){
  const response=await page.request.post(`${bff}/local/fixture/token`,{data:{issuer,expiresInSeconds,...(id?{id}:{})}});expect(response.status()).toBe(200);return (await response.json()).token as string;
}
async function rejected(response:APIResponse){expect(response.status()).toBe(401);const body=await response.json();expect(body.result).toBe(false);expect(body.errorMessage).toContain('TOKEN_INVALID_EXPIRED');return body;}
for(const id of ['AUTH-118','AUTH-119','AUTH-120','AUTH-121','AUTH-122','AUTH-123']as const){
  test(`${id} actual current BFF validation rejection`,async({page,audit})=>{
    let release!:()=>void;const held=new Promise<void>(resolve=>{release=resolve;});let completed=false;let responseBody:unknown;let credential:string|undefined;
    await runSessionCase(page,audit,id,{}, {
      3:async()=>{
        if(id==='AUTH-119')credential='Bearer malformed';
        if(id==='AUTH-120'){credential=await signed(page);const last=credential.at(-1);credential=credential.slice(0,-1)+(last==='a'?'b':'a');}
        if(id==='AUTH-121')credential=await signed(page,'single-ui-bff',-10);
        if(id==='AUTH-122')credential=await signed(page,'single-ui-bff-refresh');
        if(id==='AUTH-123'){credential=await signed(page);const response=await page.request.post(`${bff}/v2/sso/logout`,{data:{singleUIAuthorization:credential}});expect(response.status()).toBe(200);}
        await page.route('**/api/auth/v2/sso/validate',async route=>{
          const response=await route.fetch({url:`${bff}/v2/sso/validate`,maxRedirects:0});responseBody=await rejected(response);completed=true;await held;await route.fulfill({response});
        });
        await page.evaluate(async value=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');void m.Service.postService('/auth/v2/sso/validate',{singleUIAuthorization:value}).catch(()=>{});},credential);
      },
      4:async()=>{await expect.poll(()=>completed).toBe(true);await audit.record('actual-bff-rejection',{revision:'834b4155232222347220e47139a502ee43a9cbdf',condition:id,response:responseBody,signature:'Actual RSA verifier',database:'PostgreSQL18.4 exact migration DDL'});},
      5:async()=>{release();},
    });
  });
}
for(const id of ['AUTH-124','AUTH-125','AUTH-126','AUTH-127']as const){
  test(`${id} actual current BFF recovery rejection`,async({page,audit})=>{
    let credential:string|undefined;let rejection:unknown;let actualStatus=0;
    await runSessionCase(page,audit,id,{accessExpires:0,refreshExpires:600},{
      5:async()=>{
        if(id==='AUTH-125')credential=await signed(page);
        if(id==='AUTH-126')credential=await signed(page,'single-ui-bff-refresh',-10);
        if(id==='AUTH-127'){
          const sessionId=`revoked-${id}-${Date.now()}`;credential=await signed(page,'single-ui-bff-refresh',600,sessionId);
          const access=await signed(page,'single-ui-bff',600,sessionId);const logout=await page.request.post(`${bff}/v2/sso/logout`,{data:{singleUIAuthorization:access}});expect(logout.status()).toBe(200);
        }
      },
      6:async()=>{
        const response=await page.request.post(`${bff}/v2/sso/relogin`,{data:{},headers:credential?{'Single-UI-Refresh':credential}:{}});rejection=await rejected(response);
        await audit.record('actual-bff-preflight-rejection',{condition:id,response:rejection,boundary:'Actual current BFF with request substitution; UI refresh fixture remains valid until actual request'});
        await page.route('**/api/auth/v2/sso/relogin',async route=>{
          const headers={...route.request().headers()};delete headers['single-ui-refresh'];if(credential)headers['single-ui-refresh']=credential;
          const response=await route.fetch({url:`${bff}/v2/sso/relogin`,headers,maxRedirects:0});actualStatus=response.status();await rejected(response);await route.fulfill({response});
        });
      },
      7:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});await expect.poll(()=>actualStatus).toBe(401);},
    });
  });
}
