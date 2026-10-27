import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
const root=process.cwd();
const {chromium}=await import(pathToFileURL(path.join(root,'adapters/browser/node_modules/playwright/index.mjs')));
const output=process.env.AC4_OUTPUT;
await fs.mkdir(output,{recursive:false});
const hash=value=>crypto.createHash('sha256').update(value).digest('hex');
const claim=token=>JSON.parse(Buffer.from(token.trim().split(/\s+/).pop().split('.')[1],'base64url'));
const jwt=(label,now,lifetime)=>'Bearer '+Buffer.from(JSON.stringify({alg:'none',typ:'JWT'})).toString('base64url')+'.'+Buffer.from(JSON.stringify({sub:'controlled-ac4',jti:label,iat:Math.floor(now/1000),exp:Math.floor((now+lifetime)/1000)})).toString('base64url')+'.controlled';
const record={case_id:'FOUR-AC4-BROWSER',candidate_commit:process.env.AC4_COMMIT||'1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303',status:'RUNNING',started_at:new Date().toISOString(),clock:'PLAYWRIGHT_CONTROLLED_BROWSER_CLOCK',execution_scope:'ACTUAL_UI_WITH_SYNTHETIC_AUTHENTICATION_RESPONSES',assertions:[],cycles:[],requests:[],screenshots:[],limits:['Synthetic authentication credentials and response headers bypass server credential validation.','Actual MFE composition, DOM, Axios, reducers, Home timers, and trusted mouse events execute unchanged.','Headless Edge does not establish native tab suspension or PROD parity.']};
const persist=()=>fs.writeFile(path.join(output,'result.json'),JSON.stringify(record,null,2)+'\n');
const check=(id,actual,expected)=>{assert.deepEqual(actual,expected,id);record.assertions.push({id,actual,expected,status:'PASSED'});};
let browser,page,currentAccess,initialRefresh,latestRefresh,loginBody,start;
const secretValues=new Set();
try{
 browser=await chromium.launch({executablePath:'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless:true,args:['--disable-background-networking','--disable-component-update','--disable-sync','--disable-edgeupdater','--disable-updater-scheduler','--disable-features=msForceBrowserSignIn,msEdgeUpdateLaunchServicesPreferredVersion']});
 record.browser_version=browser.version();
 const context=await browser.newContext({viewport:{width:1000,height:650}});page=await context.newPage();
 await page.clock.install({time:new Date('2026-10-27T00:00:00Z')});
 await page.addInitScript(()=>{
   window.__fourCheck={events:[],trusted:0};
   document.addEventListener('mousemove',event=>{if(event.isTrusted)window.__fourCheck.trusted++;},{capture:true});
   let visible=false;
   new MutationObserver(()=>{const element=document.querySelector('#timeout-dialog-title');const next=!!element&&element.getClientRects().length>0;if(next!==visible){window.__fourCheck.events.push({event:next?'prompt_opened':'prompt_closed',at:Date.now()});visible=next;}}).observe(document,{subtree:true,childList:true,attributes:true});
 });
 const navigations=[];page.on('framenavigated',frame=>{if(frame===page.mainFrame())navigations.push(new URL(frame.url()).pathname);});
 await page.route('**/api/auth/v2/sso/*',async route=>{
   const name=new URL(route.request().url()).pathname.split('/').pop();
   const now=await page.evaluate(()=>Date.now());
   const item={name,at:now};record.requests.push(item);
   if(name==='login'){
     const response=await route.fetch();assert.equal(response.status(),200,'Real local form login setup');
     loginBody=await response.text();currentAccess=jwt('initial-access',now,15*60_000);secretValues.add(currentAccess);
     return route.fulfill({response,headers:{...response.headers(),'single-ui-authorization':currentAccess},body:loginBody});
   }
   if(name==='extend'){
     const sent=route.request().postDataJSON().singleUIAuthorization;
     item.input_access_valid=claim(sent).exp*1000>now;
     item.input_access_matches_current=sent===currentAccess;
     assert.ok(item.input_access_valid,'Accepted activity must precede access expiry');
     assert.ok(item.input_access_matches_current,'Activity must use current access');
     currentAccess=jwt('extension-'+record.requests.length,now,15*60_000);secretValues.add(currentAccess);
     item.output_exp=claim(currentAccess).exp;
     return route.fulfill({status:200,contentType:'application/json',headers:{'single-ui-authorization':currentAccess},body:'{"result":true}'});
   }
   if(name==='refreshtoken'){
     const sent=route.request().postDataJSON().singleUIAuthorization;
     item.input_access_valid=claim(sent).exp*1000>now;assert.ok(item.input_access_valid,'Refresh acquisition must use usable access');
     if(!initialRefresh){initialRefresh=jwt('initial-refresh',now,2*60*60_000);latestRefresh=initialRefresh;secretValues.add(initialRefresh);}
     else if(claim(latestRefresh).exp*1000<=now){latestRefresh=jwt('replacement-refresh-'+record.requests.length,now,4*60*60_000);secretValues.add(latestRefresh);}
     item.refresh_sha256=hash(latestRefresh);item.refresh_exp=claim(latestRefresh).exp;
     return route.fulfill({status:200,contentType:'application/json',headers:{'single-ui-refresh':latestRefresh},body:'{"result":true}'});
   }
   if(name==='validate')return route.fulfill({status:200,contentType:'application/json',headers:{'single-ui-authorization':currentAccess},body:loginBody||'{"result":true}'});
   if(name==='logout'||name==='relogin')return route.fulfill({status:500,contentType:'application/json',body:'{"result":false}'});
   return route.continue();
 });
 await page.goto((process.env.AC4_TARGET||'http://127.0.0.1:8153/')+'?show_normal_login=Y');
 await page.locator('[data-testid=Username] input').fill(process.env.SESSION_E2E_USERNAME);secretValues.add(process.env.SESSION_E2E_USERNAME);
 await page.locator('[data-testid=password] input').fill(process.env.SESSION_E2E_PASSWORD);secretValues.add(process.env.SESSION_E2E_PASSWORD);
 await page.locator('button[data-testid$="_login"]').click();
 await page.locator('[aria-label=workspaces]').waitFor({state:'visible'});
 await page.clock.pauseAt(await page.evaluate(()=>Date.now()+100));
 await page.evaluate(async()=>{window.__fourBase=await System.import('@fm/base');await window.__fourBase.Service.getRefreshToken();});
 await page.waitForFunction(()=>!!window.__fourBase.Hooks.getHooks().store.refreshToken);
 start=await page.evaluate(()=>Date.now());record.start_clock_ms=start;
 record.initial_access={sha256:hash(currentAccess),exp:claim(currentAccess).exp};
 record.initial_refresh={sha256:hash(initialRefresh),exp:claim(initialRefresh).exp};
 const initialNavigations=navigations.length,initialLogins=record.requests.filter(r=>r.name==='login').length;
 await page.screenshot({path:path.join(output,'before.png')});record.screenshots.push({file:'before.png',phase:'authenticated assertion baseline',method:'Playwright page.screenshot',captured_at:new Date().toISOString()});
 for(let cycle=1;cycle<=24;cycle++){
   const target=start+cycle*10*60_000;
   // Five seconds of the next interval deliver the current cycle's debounce.
   const eventTime=target-5000;
   const remaining=eventTime-await page.evaluate(()=>Date.now());
   if(remaining>0)await page.clock.fastForward(remaining);
   const count=record.requests.filter(r=>r.name==='extend').length;
   await page.mouse.move(130+cycle,180+cycle);
   await page.clock.runFor(5000);
   await page.waitForFunction(expected=>{const s=window.__fourBase.Hooks.getHooks().store;return s.token&&s.expiredIn*1000-Date.now()>14*60_000;},null,{timeout:10000});
   const observation=await page.evaluate(()=>{const s=window.__fourBase.Hooks.getHooks().store;return {now:Date.now(),accessExpiry:s.expiredIn*1000,authenticated:!!s.token,logout:s.isOnLogout,promptOpen:!!document.querySelector('#timeout-dialog-title'),workspace:!!document.querySelector('[aria-label=workspaces]'),promptEvents:window.__fourCheck.events.filter(e=>e.event==='prompt_opened').length,trusted:window.__fourCheck.trusted,refresh:s.refreshToken};});
   const refresh=observation.refresh;delete observation.refresh;
   check('cycle-'+cycle+' exact clock',observation.now,target);
   check('cycle-'+cycle+' successful renewal',record.requests.filter(r=>r.name==='extend').length,count+1);
   check('cycle-'+cycle+' current access remains usable',observation.accessExpiry>observation.now,true);
   check('cycle-'+cycle+' authenticated workspace',observation.authenticated&&observation.workspace,true);
   check('cycle-'+cycle+' zero logout/prompt',!!observation.logout||observation.promptOpen||observation.promptEvents>0,false);
   record.cycles.push({cycle,...observation,refresh_sha256:refresh?hash(refresh):null,refresh_exp:refresh?claim(refresh).exp:null});
   await persist();
   if(cycle===12||cycle===24){const file='cycle-'+cycle+'.png';await page.screenshot({path:path.join(output,file)});record.screenshots.push({file,phase:'controlled cycle '+cycle,method:'Playwright page.screenshot',captured_at:new Date().toISOString()});}
 }
 const final=record.cycles.at(-1);
 check('exact four hours',final.now-start,4*60*60_000);
 check('initial refresh expires inside interval',record.initial_refresh.exp*1000>start&&record.initial_refresh.exp*1000<final.now,true);
 check('24 successful activity cycles',record.requests.filter(r=>r.name==='extend').length,24);
 check('zero extra fresh login',record.requests.filter(r=>r.name==='login').length-initialLogins,0);
 check('zero logout and manual relogin',record.requests.filter(r=>['logout','relogin'].includes(r.name)).length,0);
 check('zero additional main-frame navigation',navigations.length-initialNavigations,0);
 record.core_ac4_status='PASSED';
 check('replacement refresh differs',!!final.refresh_sha256&&final.refresh_sha256!==record.initial_refresh.sha256,true);
 check('replacement refresh usable',final.refresh_exp*1000>final.now,true);
 record.status='PASSED';
}catch(error){record.status='FAILED';record.error=String(error.message);for(const secret of secretValues)if(secret)record.error=record.error.split(secret).join('[REDACTED]');record.error=record.error.replace(/(?:Bearer\s+)?eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g,'[TOKEN]');if(page)await page.screenshot({path:path.join(output,'failed.png'),mask:[page.locator('[data-testid=Username] input'),page.locator('[data-testid=password] input')]}).catch(()=>{});}
finally{record.completed_at=new Date().toISOString();await persist();if(browser)await browser.close();}
console.log(JSON.stringify({status:record.status,cycles:record.cycles.length,assertions:record.assertions.length,error:record.error}));process.exitCode=record.status==='PASSED'?0:1;
