import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';

const root = process.cwd();
const output = path.join(root, 'tasks/portal-background-session-20261019/evidence/comprehensive-renewal-20261028');
const {chromium} = await import(pathToFileURL(path.join(root, 'adapters/browser/node_modules/playwright/index.mjs')));
const binding = JSON.parse(await fs.readFile(path.join(output, 'execution-source-binding.json'), 'utf8'));
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const jwt = (id, now, lifetime) => 'Bearer e30.' + Buffer.from(JSON.stringify({sub:'synthetic-renewal-user',jti:id,iat:Math.floor(now/1000),exp:Math.floor((now+lifetime)/1000)})).toString('base64url') + '.synthetic';
const browserArgs = ['--disable-background-networking','--disable-component-update','--disable-sync','--disable-edgeupdater','--disable-updater-scheduler','--disable-features=msForceBrowserSignIn,msEdgeUpdateLaunchServicesPreferredVersion'];
const summary = {started_at:new Date().toISOString(),runner_sha256:hash(await fs.readFile(new URL(import.meta.url))),revision:binding.revision,results:[],limits:['Actual portal DOM, React, Axios, reducers, session controller and dialog execute.','Authentication/entitlement setup uses the existing isolated BFF fixture. Renewal credentials and responses are synthetic.','Controlled browser time; no real four-hour soak, native sleep, WebSocket server, target deployment or production parity.']};
const persist = async () => fs.writeFile(path.join(output,'new-e2e-summary.json'),JSON.stringify(summary,null,2)+'\n');
let browser;
try {
 browser = await chromium.launch({executablePath:'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless:true,args:browserArgs});
 summary.browser_version = browser.version(); summary.browser_args = browserArgs;
 for (const id of ['RN-X001','RN-X002','RN-X003']) {
  const folder=path.join(output,id.toLowerCase()); await fs.mkdir(folder,{recursive:true});
  const result={id,revision:binding.revision,started_at:new Date().toISOString(),status:'RUNNING',assertions:[],cycles:[],requests:[],screenshots:[],source_binding:'../execution-source-binding.json'};
  const save=async()=>fs.writeFile(path.join(folder,'result.json'),JSON.stringify(result,null,2)+'\n');
  const check=(name,actual,expected)=>{assert.deepEqual(actual,expected,name);result.assertions.push({name,actual,expected,status:'PASSED'});};
  const context=await browser.newContext({viewport:{width:1150,height:760}}); const page=await context.newPage();
  let access,refresh,loginBody,attempt=0,held,mode='success';
  const capture=async phase=>{const file=phase+'.png';await page.screenshot({path:path.join(folder,file),mask:[page.locator('[data-testid=Username] input'),page.locator('[data-testid=password] input')]});result.screenshots.push({file,phase,captured_at:new Date().toISOString(),sha256:hash(await fs.readFile(path.join(folder,file)))});};
  try {
   await page.clock.install({time:new Date('2026-10-28T00:00:00Z')});
   await page.addInitScript(()=>{window.__renewalProbe={opens:0,closures:0,events:[]};let visible=false;new MutationObserver(()=>{const next=!!document.querySelector('#timeout-dialog-title')?.getClientRects().length;if(next!==visible){window.__renewalProbe[next?'opens':'closures']++;window.__renewalProbe.events.push({visible:next,at:Date.now()});visible=next;}}).observe(document,{subtree:true,childList:true,attributes:true});});
   await page.route('**/api/auth/v2/sso/*',async route=>{
    const endpoint=new URL(route.request().url()).pathname.split('/').pop(); const now=await page.evaluate(()=>Date.now());
    const request={endpoint,at:now};result.requests.push(request);
    if(endpoint==='login') {const response=await route.fetch();assert.equal(response.status(),200,'local fixture login');loginBody=await response.text();access=jwt(id+'-initial-access',now,60_000);return route.fulfill({response,headers:{...response.headers(),'single-ui-authorization':access},body:loginBody});}
    if(endpoint==='refreshtoken') {refresh=refresh||jwt(id+'-refresh',now,4*60*60_000);return route.fulfill({status:200,contentType:'application/json',headers:{'single-ui-refresh':refresh},body:'{"result":true}'});}
    if(endpoint==='extend')return route.fulfill({status:200,contentType:'application/json',headers:{'single-ui-authorization':access},body:loginBody});
    if(endpoint==='relogin') {attempt++;request.attempt=attempt;request.mode=mode;if(mode==='hold'){held=route;return;}if(mode==='reject')return route.fulfill({status:503,contentType:'application/json',body:'{"errorMessage":"Synthetic temporary renewal failure"}'});access=jwt(id+'-access-'+attempt,now,60_000);return route.fulfill({status:200,contentType:'application/json',headers:{'single-ui-authorization':access},body:loginBody});}
    if(endpoint==='validate')return route.fulfill({status:200,contentType:'application/json',headers:{'single-ui-authorization':access},body:loginBody||'{"result":true}'});
    if(endpoint==='logout')return route.fulfill({status:200,contentType:'application/json',body:'{"result":true}'});
    return route.continue();
   });
   await page.goto('http://127.0.0.1:8243/?show_normal_login=Y');
   await page.locator('[data-testid=Username] input').fill(process.env.SESSION_E2E_USERNAME);
   await page.locator('[data-testid=password] input').fill(process.env.SESSION_E2E_PASSWORD);
   await page.locator('button[data-testid$="_login"]').click();
   await page.locator('[aria-label=workspaces]').waitFor({state:'visible'});
   await page.clock.pauseAt(await page.evaluate(()=>Date.now()+100));
   await page.evaluate(async()=>{window.__renewalBase=await System.import('@fm/base');await window.__renewalBase.Service.getRefreshToken();});
   await page.waitForFunction(()=>!!window.__renewalBase.Hooks.getHooks().store.refreshToken);
   await page.getByRole('button',{name:'Add Workspace',exact:true}).click();
   await page.getByRole('button',{name:'Add Workspace',exact:true}).click();
   const snapshot=async()=>page.evaluate(()=>{const s=window.__renewalBase.Hooks.getHooks().store;return {authenticated:!!s.token,expiry:s.expiredIn*1000,workspaceIds:s.workspaces.map(w=>w.id),workspaceLabels:s.workspaces.map(w=>w.label),dialog:!!document.querySelector('#timeout-dialog-title'),isOnLogout:!!s.isOnLogout,events:window.__renewalProbe,token:s.token};});
   const baseline=await snapshot();check('three workspace descriptors',baseline.workspaceIds.length,3);result.initial={...baseline,token_sha256:hash(baseline.token)};delete result.initial.token;
   const open=async()=>{const expiry=await page.evaluate(()=>window.__renewalBase.Hooks.getHooks().store.expiredIn*1000);const now=await page.evaluate(()=>Date.now());await page.clock.fastForward(Math.max(1,expiry-now+1));await page.getByTestId('Extend_Btn').waitFor({state:'visible'});};
   if(id==='RN-X001'){
    for(let cycle=1;cycle<=6;cycle++){
     await open();const before=await snapshot();mode='reject';await page.getByTestId('Extend_Btn').click();await page.waitForFunction(()=>document.querySelector('[data-testid=Extend_Btn]')?.disabled===false);
     let state=await snapshot();check('cycle '+cycle+' failure preserves dialog',state.dialog,true);check('cycle '+cycle+' zero early closure',state.events.closures,before.events.closures);check('cycle '+cycle+' preserves workspace IDs after failure',state.workspaceIds,baseline.workspaceIds);
     mode='success';await page.getByTestId('Extend_Btn').click();await page.waitForFunction(()=>!document.querySelector('#timeout-dialog-title'));
     state=await snapshot();check('cycle '+cycle+' current access changes',state.token!==before.token,true);check('cycle '+cycle+' usable access',state.expiry>await page.evaluate(()=>Date.now()),true);check('cycle '+cycle+' exactly one closure',state.events.closures,before.events.closures+1);check('cycle '+cycle+' preserves workspace IDs after success',state.workspaceIds,baseline.workspaceIds);
     result.cycles.push({cycle,attempts:attempt,access_sha256:hash(state.token),expiry:state.expiry,workspaceIds:state.workspaceIds,closures:state.events.closures});await save();
    }
    check('six failed and six successful attempts',attempt,12);await capture('six-cycles-complete');
   } else if(id==='RN-X002'){
    await open();const before=await snapshot();mode='hold';await page.getByTestId('Extend_Btn').click({clickCount:25});await page.waitForFunction(()=>document.querySelector('[data-testid=Extend_Btn]')?.disabled===true);await capture('pending-after-rapid-clicks');
    const pending=await snapshot();check('one relogin for 25 click events',attempt,1);check('pending dialog stays visible',pending.dialog,true);check('pending zero closure',pending.events.closures,before.events.closures);check('pending workspace IDs',pending.workspaceIds,baseline.workspaceIds);
    access=jwt(id+'-released-access',await page.evaluate(()=>Date.now()),60_000);await held.fulfill({status:200,contentType:'application/json',headers:{'single-ui-authorization':access},body:loginBody});await page.waitForFunction(()=>!document.querySelector('#timeout-dialog-title'));
    const after=await snapshot();check('held success installs access',hash(after.token),hash(access));check('held success closes once',after.events.closures,before.events.closures+1);check('held success workspace IDs',after.workspaceIds,baseline.workspaceIds);await capture('held-renewal-complete');
   } else {
    await open();mode='hold';await page.getByTestId('Extend_Btn').click();await page.waitForFunction(()=>document.querySelector('[data-testid=Extend_Btn]')?.disabled===true);await page.getByTestId('Logout_Btn').click();
    let state=await snapshot();check('Logout sets logout state while renewal held',state.isOnLogout,true);await capture('logout-during-pending');
    let delivery='fulfilled';try{await held.fulfill({status:200,contentType:'application/json',headers:{'single-ui-authorization':jwt(id+'-late-access',await page.evaluate(()=>Date.now()),60_000)},body:loginBody});}catch {delivery='request-already-aborted';}result.late_delivery=delivery;
    await page.clock.runFor(1001);await page.waitForFunction(()=>!window.__renewalBase.Hooks.getHooks().store.token);
    state=await snapshot();check('late renewal cannot authenticate after Logout',state.authenticated,false);check('single held renewal request',attempt,1);await capture('logged-out');
   }
   result.status='PASSED';
  }catch(error){result.status='FAILED';result.error=String(error.message).replace(/(?:Bearer\s+)?eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g,'[TOKEN]');await capture('failed').catch(()=>{});}
  finally {result.completed_at=new Date().toISOString();await save();summary.results.push({id:result.id,status:result.status,assertions:result.assertions.length,result:path.relative(output,path.join(folder,'result.json')),error:result.error});await persist();await context.close();}
 }
}catch(error){summary.runner_error=String(error.message);}
finally {summary.completed_at=new Date().toISOString();await persist();if(browser)await browser.close();}
console.log(JSON.stringify(summary.results));process.exitCode=summary.results.length===3&&summary.results.every(r=>r.status==='PASSED')?0:1;
