#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const workspace=process.env.WORKBENCH_ROOT||process.cwd();
const output=path.join(workspace,'tasks/portal-background-session-20261019/evidence/review-e2e-20261028');
const bindingBytes=fs.readFileSync(path.join(output,'source-binding.json'));
const binding=JSON.parse(bindingBytes);
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const source=fs.readFileSync(path.join(workspace,'.workbench/portal-session-real-20261019/local-bff/runner/local/portalsession/LocalSessionApplication.java'),'utf8');
for(const [name,key] of [['USER','REVIEW_CONTRACT_USER'],['PASSWORD','REVIEW_CONTRACT_PASSWORD']]){
 const found=source.match(new RegExp('public\\s+static\\s+final\\s+String\\s+'+name+'\\s*=\\s*"([^"\\n]+)"'));assert.ok(found,'Local fixture credential must be available.');process.env[key]=found[1];
}
const safe=error=>{let text=String(error?.message||error);for(const key of ['REVIEW_CONTRACT_USER','REVIEW_CONTRACT_PASSWORD'])text=text.split(process.env[key]||'__unset__').join('[REDACTED]');return text.replace(/(?:Bearer\s+)?eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g,'[TOKEN]');};
const tokenSummary=token=>{if(!token)return null;let claims={};try{claims=JSON.parse(Buffer.from(token.replace(/^\S+ /,'').split('.')[1],'base64url'));}catch{}return {sha256:hash(token),exp:claims.exp??null,iat:claims.iat??null};};
const runnerBytes=fs.readFileSync(__filename),runnerSha256=hash(runnerBytes);
fs.writeFileSync(path.join(output,'reviewContractE2e.snapshot.cjs'),runnerBytes);
const summary={startedAt:new Date().toISOString(),runnerSha256,sourceBindingSha256:hash(bindingBytes),status:'RUNNING',cases:[]};
const saveSummary=()=>fs.writeFileSync(path.join(output,'contracts-summary.json'),JSON.stringify(summary,null,2)+'\n');
let browser;
async function snapshot(page){return page.evaluate(async()=>{
 const f=window.__contract,s=f.base.Hooks.getHooks().store;
 const sum=async token=>{if(!token)return null;let p={};try{p=JSON.parse(atob(token.replace(/^\S+ /,'').split('.')[1].replace(/-/g,'+').replace(/_/g,'/')));}catch{}return {sha256:Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(token)))).map(x=>x.toString(16).padStart(2,'0')).join(''),exp:p.exp??null,iat:p.iat??null};};
 const extend=document.querySelector('[data-testid=Extend_Btn]'),logout=document.querySelector('[data-testid=Logout_Btn]');
 return {at:new Date().toISOString(),authenticated:!!s.token,access:await sum(s.token),refresh:await sum(s.refreshToken),dialogVisible:!!document.querySelector('#timeout-dialog-title'),extendDisabled:extend?.disabled??null,logoutDisabled:logout?.disabled??null,isLoading:s.isLoading,homeVisible:!!document.querySelector('[aria-label=workspaces]'),signInVisible:!!document.querySelector('[data-testid=Username] input')};
});}
async function protectedCheck(page){return page.evaluate(async()=>{const token=window.__contract.base.Hooks.getHooks().store.token;if(!token)return {called:false};const response=await fetch('/api/auth/v2/sso/validate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({singleUIAuthorization:token})});let data={};try{data=await response.json();}catch{}return {called:true,status:response.status,result:data.result??null};});}
async function login(context,side){const page=await context.newPage();page.setDefaultTimeout(15000);await page.goto(`http://127.0.0.1:${side==='candidate'?8143:8153}/?show_normal_login=Y`,{waitUntil:'domcontentloaded'});await page.locator('[data-testid=Username] input').fill(process.env.REVIEW_CONTRACT_USER);await page.locator('input[type=password]').fill(process.env.REVIEW_CONTRACT_PASSWORD);await page.locator('button[data-testid$="_login"]').click();await page.locator('[aria-label=workspaces]').waitFor({state:'visible'});await page.evaluate(async()=>{const base=await System.import('@fm/base');window.__contract={base};await base.Service.getRefreshToken();});await page.waitForFunction(()=>!!window.__contract.base.Hooks.getHooks().store.refreshToken);return page;}
async function run(id,variant,side){
 const name=id==='02'?`contracts-02-${variant}-${side}`:`contracts17-${side}`;
 const dir=path.join(output,name);fs.mkdirSync(dir,{recursive:false});
 const row={caseId:`REVIEW-E2E-${id}`,variant,side,sourceRevision:binding[side],sourceBindingSha256:hash(bindingBytes),runnerSha256,status:'RUNNING',startedAt:new Date().toISOString(),clock:'REAL_WALL_CLOCK',browserVersion:browser.version(),assertions:[],screenshots:[],events:[],limits:['Local BFF authentication/entitlement fixture and toolkit substitute; source-bound local development build; production applicability unverified.']};
 summary.cases.push({name,caseId:row.caseId,variant,side,status:'RUNNING',result:`${name}/result.json`});
 const entry=summary.cases[summary.cases.length-1];
 const save=()=>{fs.writeFileSync(path.join(dir,'result.json'),JSON.stringify(row,null,2)+'\n');entry.status=row.status;entry.phase=row.phase;saveSummary();};
 const context=await browser.newContext({viewport:{width:1100,height:750}});let controlContext;
 let page;
 const capture=async(phase,target=page)=>{const file=phase+'.png';try{await target.screenshot({path:path.join(dir,file),mask:[target.locator('[data-testid=Username] input'),target.locator('input[type=password]')],timeout:10000});row.screenshots.push({phase,file,sha256:hash(fs.readFileSync(path.join(dir,file))),capturedAt:new Date().toISOString(),method:'Playwright page.screenshot with credential fields masked',claim:'Actual portal route and Timeout controls at this phase.'});}catch(error){row.screenshots.push({phase,captureGap:safe(error)});}save();};
 const check=(predicate,actual)=>{row.assertions.push({predicate,passed:!!actual});save();assert.ok(actual,predicate);};
 save();
 try{
  page=await login(context,side);
  page.on('response',x=>{const p=new URL(x.url()).pathname;if(p.startsWith('/api/'))row.events.push({event:'response',pathname:p,status:x.status(),at:new Date().toISOString()});});
  row.loadedScriptResources=await page.evaluate(()=>performance.getEntriesByType('resource').filter(x=>/\.js(?:[?#]|$)/.test(x.name)).map(x=>x.name));
  row.initial=await snapshot(page);row.phase='WAITING_FOR_NATURAL_ACCESS_EXPIRY';save();await capture('initial-home');
  await page.locator('[data-testid=Extend_Btn]').waitFor({state:'visible',timeout:75000});
  row.prompt=await snapshot(page);row.phase='NATURAL_EXPIRY_PROMPT';save();await capture('natural-expiry-prompt');
  if(id==='02'){
   row.limits.push(`Successful local relogin authorization is replaced with ${variant}. Modified JWT signature is invalid; local BFF never emits this malformed shape.`);
   let substitutedHash,providerHash,requestCount=0;
   const pattern='**/api/auth/v2/sso/relogin';
   await page.route(pattern,async route=>{
    requestCount++;const response=await route.fetch();const headers=response.headers();const actual=headers['single-ui-authorization'];
    check('Malformed-token experiment first obtains successful real BFF renewal with authorization',response.status()===200&&!!actual);
    providerHash=hash(actual);let substituted;
    if(variant==='opaque')substituted='Bearer opaque-local-contract-probe';
    else{const prefix=actual.startsWith('Bearer ')?'Bearer ':'';const parts=actual.replace(/^\S+ /,'').split('.');const p=JSON.parse(Buffer.from(parts[1],'base64url'));delete p.iat;parts[1]=Buffer.from(JSON.stringify(p)).toString('base64url');substituted=prefix+parts.join('.');}
    substitutedHash=hash(substituted);row.substitution={variant,provider:tokenSummary(actual),substituted:tokenSummary(substituted),providerAcceptedAt:new Date().toISOString()};save();
    delete headers['content-length'];headers['single-ui-authorization']=substituted;await route.fulfill({response,headers});
   });
   await page.locator('[data-testid=Extend_Btn]').click();
   await page.waitForTimeout(1300);row.malformed=await snapshot(page);row.malformedProtected=await protectedCheck(page);row.malformedRequestCount=requestCount;await capture('malformed-response-outcome');
   check('Exactly one correlated malformed-token relogin occurred',requestCount===1);
   row.malformedInstalled=substitutedHash===row.malformed.access?.sha256;
   row.malformedRealProviderAccessInstalled=providerHash===row.malformed.access?.sha256;
   if(side==='candidate'){
    check('Candidate does not install substituted authorization',!row.malformedInstalled);
    check('Candidate retains recovery dialog after unsupported access',row.malformed.dialogVisible);
   }
   await page.unroute(pattern);
   let controlPage=page;
   if(!row.malformed.dialogVisible||row.malformed.extendDisabled){
    controlContext=await browser.newContext({viewport:{width:1100,height:750}});controlPage=await login(controlContext,side);
    row.validControlContext='FRESH_CONTEXT_AFTER_MALFORMED_VARIANT';row.phase='WAITING_FOR_NORMAL_CONTROL_EXPIRY';save();
    await controlPage.locator('[data-testid=Extend_Btn]').waitFor({state:'visible',timeout:75000});
   }else row.validControlContext='SAME_PROMPT_RETRY';
   const responsePromise=controlPage.waitForResponse(x=>new URL(x.url()).pathname.endsWith('/sso/relogin'),{timeout:15000});
   await controlPage.locator('[data-testid=Extend_Btn]').click();const response=await responsePromise;const returned=response.headers()['single-ui-authorization'];
   row.validResponse={status:response.status(),access:tokenSummary(returned),receivedAt:new Date().toISOString()};save();
   check('Valid control obtains real BFF success and access',response.status()===200&&!!returned);
   await controlPage.waitForFunction(expected=>window.__contract.base.Hooks.getHooks().store.token===expected,returned,{timeout:10000});
   await controlPage.locator('#timeout-dialog-title').waitFor({state:'hidden',timeout:10000});
   row.valid=await snapshot(controlPage);row.validProtected=await protectedCheck(controlPage);await capture('valid-normal-control',controlPage);
   check('Valid control installs exactly returned access',row.valid.access.sha256===hash(returned));
   check('Valid control closes Timeout dialog',!row.valid.dialogVisible);
   check('Valid control BFF validation succeeds',row.validProtected.status===200&&row.validProtected.result===true);
   row.disposition=side==='candidate'?'UNSUPPORTED_ACCESS_REJECTED_VALID_RETRY_RECOVERS':row.malformedInstalled?'BASELINE_INSTALLED_UNSUPPORTED_ACCESS_VALID_FRESH_CONTROL_RECOVERS':'BASELINE_MALFORMED_OUTCOME_RECORDED_VALID_CONTROL_RECOVERS';
  }else{
   const refreshDeadline=row.prompt.refresh.exp*1000;
   check('Refresh remains usable when manual Extend starts',refreshDeadline>Date.now()+2000);
   let held,accepted;const pattern='**/api/auth/v2/sso/relogin';
   await page.route(pattern,async route=>{
    held=route;const response=await route.fetch();const access=response.headers()['single-ui-authorization'];
    accepted={response,access,acceptedAt:Date.now(),status:response.status()};
    row.provider={status:accepted.status,acceptedAt:new Date(accepted.acceptedAt).toISOString(),returnedAccess:tokenSummary(access),refreshDeadline:new Date(refreshDeadline).toISOString()};row.phase='SUCCESSFUL_RESPONSE_HELD';save();
   });
   row.extendStartedAt=new Date().toISOString();await page.locator('[data-testid=Extend_Btn]').click();
   const waitUntil=Date.now()+15000;while(!accepted&&Date.now()<waitUntil)await page.waitForTimeout(25);
   check('Local BFF accepted renewal before refresh expiry',accepted&&accepted.status===200&&accepted.acceptedAt<refreshDeadline);
   check('Accepted response initially contains usable access',accepted.access&&tokenSummary(accepted.access).exp*1000>accepted.acceptedAt);
   row.pending=await snapshot(page);await capture('provider-success-response-held');
   const remaining=refreshDeadline-Date.now()+1100;check('Natural held-response experiment is bounded below three minutes',remaining>0&&remaining<180000);
   row.limits.push('Provider accepted the request before refresh expiry. Its successful response is withheld until natural wall time passes refresh expiry. Returned access can expire during that hold; acceptance is not required.');
   while(Date.now()<refreshDeadline+1100){await page.waitForTimeout(Math.min(5000,refreshDeadline+1100-Date.now()));row.lastWaitObservationAt=new Date().toISOString();save();}
   row.beforeRelease=await snapshot(page);row.deliveryAt=new Date().toISOString();row.returnedAccessExpiredAtDelivery=tokenSummary(accepted.access).exp*1000<=Date.now();await capture('natural-deadline-before-delivery');
   await held.fulfill({response:accepted.response});await page.waitForTimeout(1700);row.after=await snapshot(page);row.protected=await protectedCheck(page);await capture('late-success-delivery-final');
   row.acceptedAccessInstalled=row.after.access?.sha256===hash(accepted.access);
   check('Successful response delivery occurs after captured refresh expiry',Date.parse(row.deliveryAt)>refreshDeadline);
   row.disposition=row.returnedAccessExpiredAtDelivery&&!row.acceptedAccessInstalled?'EXPIRED_RETURNED_ACCESS_NOT_INSTALLED':row.acceptedAccessInstalled?'ACCEPTED_RESPONSE_ACCESS_INSTALLED':'LATE_SUCCESS_OUTCOME_RECORDED';
  }
  row.phase='FINISHED';row.status='COMPLETED';save();
 }catch(error){row.status='SETUP_OR_EXECUTION_FAILED';row.error=safe(error);if(page){try{row.failure=await snapshot(page);await capture('execution-failed');}catch{}}}
 finally{row.completedAt=new Date().toISOString();save();entry.disposition=row.disposition;entry.resultSha256=hash(fs.readFileSync(path.join(dir,'result.json')));saveSummary();await context.close();if(controlContext)await controlContext.close();process.stdout.write(JSON.stringify({caseId:row.caseId,variant,side,status:row.status,disposition:row.disposition,error:row.error})+'\n');}
}
async function main(){saveSummary();const{chromium}=require(path.join(workspace,'adapters/browser/node_modules/playwright'));browser=await chromium.launch({executablePath:'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless:true});
 try{await Promise.allSettled(['candidate','baseline'].flatMap(side=>[run('17','accepted-before-expiry-late-delivery',side),run('02','opaque',side),run('02','missingiat',side)]));}
 finally{await browser.close();summary.completedAt=new Date().toISOString();summary.status=summary.cases.length===6&&summary.cases.every(x=>x.status==='COMPLETED')?'COMPLETED':'INCOMPLETE';saveSummary();}}
main().catch(error=>{summary.status='RUNNER_FAILED';summary.error=safe(error);saveSummary();process.stderr.write(summary.error+'\n');process.exitCode=1;}).finally(()=>{delete process.env.REVIEW_CONTRACT_USER;delete process.env.REVIEW_CONTRACT_PASSWORD;});
