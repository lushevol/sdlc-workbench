import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
const root=process.cwd(), ev=path.join(root,'tasks/portal-background-session-20261019/evidence/remaining-execution-20261029');
const out=path.join(ev,process.env.CORE_OUTPUT||'core-browser'); await fs.mkdir(out,{recursive:true});
const binding=JSON.parse(await fs.readFile(path.join(ev,'execution-source-binding.json'),'utf8'));
const all=JSON.parse(await fs.readFile(path.join(root,'tasks/portal-background-session-20261019/evidence/comprehensive-renewal-20261028/core-cases.json'),'utf8'));
const integration=new Set([...Array.from({length:9},(_,i)=>`RN-B${String(i+1).padStart(3,'0')}`),...Array.from({length:13},(_,i)=>`RN-P${String(i+1).padStart(3,'0')}`),'RN-P018',...Array.from({length:6},(_,i)=>`RN-R${String(i+9).padStart(3,'0')}`)]);
const selected=process.env.CASE_IDS?.split(',');
const cases=all.filter(c=>!integration.has(c.id)&&(!selected||selected.includes(c.id)));
const {chromium}=await import(pathToFileURL(path.join(root,'adapters/browser/node_modules/playwright/index.mjs')));
const hash=v=>crypto.createHash('sha256').update(v).digest('hex');
const jwt=(id,now,life=60000,extra={})=>'Bearer e30.'+Buffer.from(JSON.stringify({sub:'synthetic-renewal-user',jti:id,iat:now/1000,exp:(now+life)/1000,...extra})).toString('base64url')+'.synthetic';
const browserArgs=['--disable-background-networking','--disable-component-update','--disable-sync','--disable-edgeupdater','--disable-updater-scheduler','--disable-features=msForceBrowserSignIn,msEdgeUpdateLaunchServicesPreferredVersion'];
const summary={started_at:new Date().toISOString(),revision:binding.revision,runner_sha256:hash(await fs.readFile(new URL(import.meta.url))),planned:cases.length,results:[],limits:['Actual Chromium portal, React hooks, reducers, Axios interceptors and services.','Controlled browser time, synthetic identity and auth responses. Protected peer assertions are fixture-level, not production RSA authorization.','Native device, VPN, real sleep, independent devices and unavailable target boundaries remain blocked.']};
const persist=()=>fs.writeFile(path.join(out,'summary.json'),JSON.stringify(summary,null,2)+'\n');
class Blocked extends Error{}
const browser=await chromium.launch({executablePath:'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless:true,args:browserArgs});summary.browser_version=browser.version();await persist();
for(const c of cases){
 const folder=path.join(out,c.id);await fs.mkdir(folder,{recursive:true});
 const r={id:c.id,title:c.title,basis:c.basis,started_at:new Date().toISOString(),status:'RUNNING',stage:'setup',expected:c.then,assertions:[],observations:{},source_revision:binding.revision,source_binding:'../../execution-source-binding.json',source_refs:c.sources,limits:[...summary.limits],screenshots:[]};
 const save=()=>fs.writeFile(path.join(folder,'result.json'),JSON.stringify(r,null,2)+'\n');
 const check=(name,actual,expected)=>{const ok=JSON.stringify(actual)===JSON.stringify(expected);r.assertions.push({name,actual,expected,status:ok?'PASSED':'FAILED'});if(!ok)throw new assert.AssertionError({message:name,actual,expected});};
 const block=reason=>{r.blocked_predicates=[reason];throw new Blocked(reason);};
 let ctx,page,state,held=[];
 const watchdog=setTimeout(()=>{r.watchdog_timeout=true;ctx?.close().catch(()=>{});},c.id==='RN-L004'||c.id==='RN-L011'?1200000:90000);
 const capture=async label=>{try{if(!page||page.isClosed())return;const f=label+'.png';await page.screenshot({path:path.join(folder,f),mask:[page.locator('[data-testid=Username] input'),page.locator('[data-testid=password] input')],timeout:4000});r.screenshots.push({file:f,sha256:hash(await fs.readFile(path.join(folder,f)))});}catch(e){r.screenshot_gaps??=[];r.screenshot_gaps.push(String(e.message).slice(0,200));}};
 try{
  if(['RN-H004','RN-H006','RN-H012','RN-A011','RN-A012','RN-F008'].includes(c.id))block({'RN-H004':'Actual device sleep and a second elapsed-time observer are unavailable. Changing the user device power state is outside isolated browser execution.','RN-H006':'A separate controlled VPN and service route are unavailable. The user network remains unchanged.','RN-H012':'Two independent devices and an observed shared revocation service are unavailable.','RN-A011':'No touch device or native swipe fixture is available. Synthetic touch events cannot establish emitted native shell events.','RN-F008':'A real TLS-validation failure endpoint is unavailable. A generic request abort would replace the stated failure mode.','RN-A012':'A real IME composition driver is unavailable. Synthetic composition events would replace the required browser input behavior.'}[c.id]);
  ctx=await browser.newContext({viewport:{width:1150,height:760},timezoneId:c.id==='RN-B016'?'Asia/Singapore':'UTC'});page=await ctx.newPage();page.setDefaultTimeout(15000);
  await page.clock.install({time:new Date('2026-10-29T00:00:00Z')});
  await page.addInitScript(()=>{
   window.__probe={opens:0,closures:0,events:[],activity:[],activeTimers:{},listeners:[]};let visible=false;
   const p=window.__probe;new MutationObserver(()=>{const next=!!document.querySelector('#timeout-dialog-title')?.getClientRects().length;if(next!==visible){p[next?'opens':'closures']++;p.events.push({visible:next,at:Date.now()});visible=next;}}).observe(document,{subtree:true,childList:true,attributes:true});
   for(const type of ['mousemove','keydown','scroll','compositionstart','compositionupdate','compositionend','touchstart','touchmove'])window.addEventListener(type,e=>{p.activity.push({type,trusted:e.isTrusted,at:Date.now()});},true);
   const set=window.setTimeout.bind(window),clear=window.clearTimeout.bind(window);
   window.setTimeout=(fn,delay,...args)=>{let id;const stack=new Error().stack;id=set(()=>{delete p.activeTimers[id];if(typeof fn==='function')fn(...args);else (0,eval)(fn);},delay);p.activeTimers[id]={delay,stack};return id;};
   window.clearTimeout=id=>{delete p.activeTimers[id];return clear(id);};
  });
  state={mode:'success',access:null,refresh:null,body:null,attempts:0,requests:[],refreshLife:4*3600000};
  await ctx.route('**/api/auth/v2/sso/*',async route=>{
   const endpoint=new URL(route.request().url()).pathname.split('/').pop();const owner=route.request().headers()['single-ui-authorization'];const now=await page.evaluate(()=>Date.now()).catch(()=>Date.now());
   const req={endpoint,at:now,owner_sha256:owner?hash(owner):null};state.requests.push(req);
   const fulfill=(status,headers={},body=state.body||'{"result":true}')=>route.fulfill({status,contentType:'application/json',headers,body});
   if(endpoint==='login'){
    const response=await route.fetch();if(response.status()!==200)throw new Error('Synthetic local login setup status '+response.status());state.body=await response.text();state.access=jwt(c.id+'-initial',now);return route.fulfill({response,headers:{...response.headers(),'single-ui-authorization':state.access},body:state.body});
   }
   if(endpoint==='refreshtoken'){
    if(state.holdAcquisition){held.push({route,endpoint});return;}
    if(!state.refresh||state.rotateRefresh)state.refresh=jwt(c.id+'-refresh-'+state.requests.length,now,state.refreshLife);
    return fulfill(200,{'single-ui-refresh':state.refresh});
   }
   if(endpoint==='extend'){
    if(state.activityRenew){state.access=jwt(c.id+'-activity-'+state.requests.length,now);}
    return fulfill(200,{'single-ui-authorization':state.access});
   }
   if(endpoint==='relogin'){
    state.attempts++;req.attempt=state.attempts;req.mode=state.mode;
    if(state.mode==='hold'){held.push({route,endpoint});return;}
    if(state.mode==='abort')return route.abort(state.abortCode||'connectionreset');
    if(state.mode==='reject')return fulfill(state.status||503, state.headers||{},'{"errorMessage":"Controlled renewal rejection"}');
    if(state.mode==='malformed')return fulfill(200,{},'{"result":true}');
    state.access=jwt(c.id+'-renewed-'+state.attempts,now,state.accessLife||60000,state.payloadExtra||{});
    return fulfill(200,{[state.headerCase||'single-ui-authorization']:state.access});
   }
   if(endpoint==='validate'){
    req.fixture_validation=owner===state.access;req.principal=req.fixture_validation?'synthetic-renewal-user':null;
    return fulfill(req.fixture_validation?200:401,{},JSON.stringify({result:req.fixture_validation,principal:req.principal}));
   }
   if(endpoint==='logout')return fulfill(200,{},'{"result":true}');
   return route.continue();
  });
  await page.goto('http://127.0.0.1:8343/?show_normal_login=Y',{waitUntil:'domcontentloaded',timeout:30000});
  await page.locator('[data-testid=Username] input').fill(process.env.SESSION_E2E_USERNAME);await page.locator('[data-testid=password] input').fill(process.env.SESSION_E2E_PASSWORD);await page.locator('button[data-testid$="_login"]').click();await page.locator('[aria-label=workspaces]').waitFor({state:'visible'});
  await page.clock.pauseAt(await page.evaluate(()=>Date.now()+100));
  await page.evaluate(async()=>{window.__base=await System.import('@fm/base');await window.__base.Service.getRefreshToken();});
  await page.waitForFunction(()=>!!window.__base.Hooks.getHooks().store.refreshToken);
  const snap=()=>page.evaluate(()=>{const s=window.__base.Hooks.getHooks().store;return {token:s.token,refresh:s.refreshToken,expiry:s.expiredIn*1000,isOnLogout:s.isOnLogout,loading:s.isLoading,dialog:!!document.querySelector('#timeout-dialog-title'),extendDisabled:document.querySelector('[data-testid=Extend_Btn]')?.disabled,workspaceIds:s.workspaces.map(x=>x.id),selected:s.currentWorkspace?.id,probe:window.__probe};});
  const safe=v=>{const z=structuredClone(v);if(z.token){z.token_sha256=hash(z.token);delete z.token;}if(z.refresh){z.refresh_sha256=hash(z.refresh);delete z.refresh;}return z;};
  const now=()=>page.evaluate(()=>Date.now());
  const open=async()=>{const s=await snap();await page.clock.runFor(Math.max(1,s.expiry-await now()+1));await page.getByTestId('Extend_Btn').waitFor({state:'visible'});};
  const click=async()=>page.getByTestId('Extend_Btn').click({force:true});
  const settle=()=>page.waitForFunction(()=>!window.__base.Hooks.getHooks().store.isLoading);
  const recover=async()=>{await click();await page.waitForFunction(()=>!document.querySelector('#timeout-dialog-title'));};
  const setAccess=async(token,fresh=false)=>{state.access=token;await page.evaluate(async fresh=>{await window.__base.Service.postService('/auth/v2/sso/'+(fresh?'login':'extend'),{});},fresh);};
  const setRefresh=async token=>{state.refresh=token;await page.evaluate(token=>window.__base.LoginUtil.setRefreshToken(token),token);};
  const release=async(success=true)=>{const pending=held.shift();if(!pending)throw new Error('No held request');state.access=jwt(c.id+'-released-'+state.requests.length,await now());try{await pending.route.fulfill({status:success?200:503,contentType:'application/json',headers:success?{'single-ui-authorization':state.access}:{},body:success?state.body:'{"errorMessage":"controlled failure"}'});}catch(e){r.observations.delivery=String(e.message).slice(0,150);}};
  const validate=async()=>{const d=await page.evaluate(async()=>{try{return (await window.__base.Service.postService('/auth/v2/sso/validate',{})).data;}catch{return {result:false};}});check('controlled protected peer accepts installed access',d.result,true);r.observations.validation=d;};
  await page.evaluate(()=>{window.__probe.activity=[];});
  const base=await snap();r.initial=safe(base);
  r.stage='execute';
  const n=Number(c.id.slice(-3));
  if(c.id.startsWith('RN-A')){
   state.activityRenew=true;const initialExtend=state.requests.filter(x=>x.endpoint==='extend').length;
   if(n<=6||n===13){
    if(n===6)await page.evaluate(()=>{const el=document.createElement('div');el.id='same-origin-pane';el.style.cssText='overflow:auto;height:100px';el.innerHTML='<div style="height:1000px">Synthetic nested application pane</div>';document.body.append(el);});
    for(let i=0;i<150;i++){
     const type=n===1?'mouse':n===2||n===5||n===13?'key':n===3||n===6?'scroll':['mouse','key','scroll'][i%3];
     if(type==='mouse')await page.mouse.move(30+(i%80),30+(i%60));
     if(type==='key'){if(n===13){await page.keyboard.down('a');}else await page.keyboard.press(n===5?'Tab':'a');}
     if(type==='scroll')await page.evaluate(n=>{const target=n===6?document.querySelector('#same-origin-pane'):window;target.dispatchEvent(new Event('scroll'));},n);
     await page.clock.runFor(100);
    }
    if(n===13)await page.keyboard.up('a');
    const count=state.requests.filter(x=>x.endpoint==='extend').length-initialExtend;r.observations.successful_renewals=count;check('successful renewal count at least one in fifteen seconds',count>=1,true);if(n<=3)await validate();
   }else if(n===7){
    await ctx.route('**/probe-child.html',route=>route.fulfill({status:200,contentType:'text/html',body:'<textarea aria-label="Cross-origin editor"></textarea>'}));
    await page.evaluate(()=>{const f=document.createElement('iframe');f.src='http://127.0.0.1:8342/probe-child.html';document.body.append(f);});
    const frame=page.frameLocator('iframe[src$="probe-child.html"]');await frame.getByRole('textbox').fill('Synthetic cross-origin edit');
    for(let i=0;i<150;i++){await frame.getByRole('textbox').press('a');await page.clock.runFor(100);}
    const events=(await snap()).probe.activity;check('shell does not receive cross-origin typing',events.filter(x=>x.type==='keydown').length,0);r.observations.iframe_input_actions=150;
   }else if(n===8){await open();check('timeout visible after expiry',(await snap()).dialog,true);}
   else if(n===9){await open();const events=(await snap()).probe.activity;check('zero shell activity input',events.filter(x=>['mousemove','keydown','scroll'].includes(x.type)).length,0);block('No real WebSocket heartbeat peer ran; zero-input expiry observation is supplementary.');}
   else if(n===10){await page.evaluate(()=>{for(let i=0;i<100;i++)window.dispatchEvent(new MouseEvent('mousemove',{bubbles:true}));});const events=(await snap()).probe.activity.filter(x=>x.type==='mousemove');check('all one hundred synthetic event flags recorded',events.length,100);check('all synthetic events untrusted',events.every(x=>x.trusted===false),true);}
   else if(n===14){for(let i=0;i<26;i++){await page.mouse.move(20+i,20+i);await page.clock.runFor(4900);if(i===12||i===25){r.observations['deadline-'+i]={state:safe(await snap()),renewals:state.requests.filter(x=>x.endpoint==='extend').length};await save();}}check('both deadline traces retained',Object.keys(r.observations).length,2);}
   else if(n===15){await page.mouse.move(50,50);await page.clock.runFor(5000);await page.waitForFunction(()=>!window.__base.Hooks.getHooks().store.isLoading);check('one trailing activity callback',state.requests.filter(x=>x.endpoint==='extend').length-initialExtend,1);}
  }else if(c.id.startsWith('RN-M')){
   await open();const before=await snap();
   if([1,5,6,7,8,9,10].includes(n))state.mode='hold';
   if(n===3||n===4)state.mode='reject';
   if(n===11||n===12){await setAccess(jwt('replacement-B',await now()),true);const pre=state.requests.length;await page.getByTestId(n===11?'Extend_Btn':'Logout_Btn').click({force:true});await page.clock.runFor(1001);check('stale action sends no new auth request',state.requests.slice(pre).filter(x=>x.endpoint===(n===11?'relogin':'logout')).length,0);}
   else if(n===2){await recover();check('one successful closure',(await snap()).probe.closures-before.probe.closures,1);await validate();}
   else if(n===3){await click();await settle();const s=await snap();check('rejection zero closure',s.probe.closures-before.probe.closures,0);check('retry enabled',s.extendDisabled,false);}
   else if(n===4){await click();await settle();state.mode='success';await recover();check('two relogin attempts',state.attempts,2);check('one closure',(await snap()).probe.closures-before.probe.closures,1);}
   else if(n===5){await page.evaluate(()=>{for(let i=0;i<20;i++)document.querySelector('[data-testid=Extend_Btn]').click();});await page.waitForFunction(()=>window.__base.Hooks.getHooks().store.isLoading);check('one pending manual call',state.attempts,1);check('zero pending closure',(await snap()).probe.closures-before.probe.closures,0);}
   else if(n===1){await click();await page.waitForFunction(()=>window.__base.Hooks.getHooks().store.isLoading);check('zero pending closure',(await snap()).probe.closures-before.probe.closures,0);}
   else if(n===6){await click();await page.waitForFunction(()=>window.__base.Hooks.getHooks().store.isLoading);await page.getByTestId('Logout_Btn').click({force:true});const beforeDelivery=await snap();await release();await page.clock.runFor(1001);check('late response installs no access',!!(await snap()).token,false);r.observations.logoutStarted=beforeDelivery.isOnLogout;block('The browser request cancellation is observed indirectly. The internal AbortSignal was not exposed for its explicit aborted predicate.');}
   else if(n===7){await click();await page.waitForFunction(()=>window.__base.Hooks.getHooks().store.isLoading);await page.evaluate(()=>window.__base.LoginUtil.setAuthorization(''));const pre=(await snap()).probe.closures;await release();check('unmounted response adds zero UI closure',(await snap()).probe.closures-pre,0);block('Actual Timeout unmount ran through routing. The explicit callback spy is unavailable; UI closure observation is narrower.');}
   else if(n===8||n===9){await click();await page.waitForFunction(()=>window.__base.Hooks.getHooks().store.isLoading);const refreshExpiry=JSON.parse(Buffer.from((await snap()).refresh.split('.')[1],'base64').toString()).exp*1000;await page.clock.fastForward(refreshExpiry-2000-await now()+1);await release(n===9);await settle();if(n===8){const count=state.attempts;const btn=page.getByTestId('Extend_Btn');if(await btn.count())await btn.click({force:true});check('no retry after deadline',state.attempts,count);}else {r.observations.after=safe(await snap());await validate();}}
   else if(n===10){block('Mounting the Timeout hook while an access-only acquisition is already pending needs a hook fixture. No browser binding was supplied for that exact mount order.');}
  }else if(c.id.startsWith('RN-P')){
   if(n===14||n===15||n===16||n===17){await open();state.headerCase=n===15?'Single-UI-Authorization':'single-ui-authorization';if(n===17)state.payloadExtra={iat:(await now()+10000)/1000};await recover();r.observations.installed=safe(await snap());await validate();r.limits.push('Protected validation is a controlled peer matching exact credential bytes, not actual RSA acceptance.');block('Actual service-side principal acceptance is not established for the synthetic renewal JWT. Client installation and fixture acceptance are executed.');}
  }else if(c.id.startsWith('RN-F')){
   await open();const before=await snap();
   if(n<=5){state.mode='reject';state.status=[401,403,429,500,503][n-1];if(n===3)state.headers={'Retry-After':'1'};}
   else if(n>=6&&n<=8){state.mode='abort';state.abortCode={6:'connectionreset',7:'namenotresolved',8:'sslprotocolerror'}[n];}
   else if(n===12)state.mode='malformed';else state.mode='hold';
   await click();
   if(n===9||n===10){await page.waitForFunction(()=>window.__base.Hooks.getHooks().store.isLoading);await page.evaluate(()=>window.__base.Service.signal.relogin.abort());await settle();r.observations.cancellation=true;if(n===9)block('Explicit AbortController cancellation ran. No configured client timeout was present, so the required automatic timeout did not execute.');}
   else if(n===11){await page.waitForFunction(()=>window.__base.Hooks.getHooks().store.isLoading);const exp=JSON.parse(Buffer.from((await snap()).refresh.split('.')[1],'base64').toString()).exp*1000;await page.clock.fastForward(exp-2000-await now()+1);r.observations.deadline=safe(await snap());check('zero closure while permanently pending',(await snap()).probe.closures-before.probe.closures,0);}
   else await settle();
   const after=await snap();check('failure zero successful closure',after.probe.closures-before.probe.closures,0);
   if(n<=10)check('explicit retry remains available',after.extendDisabled,false);
   if(n===12){check('malformed response installs no usable access',after.token, before.token);check('loader released',after.loading,false);}
  }else if(c.id.startsWith('RN-B')){
   if(n===10||n===11||n===12){
    await setRefresh(jwt('one-hour-refresh',await now(),3600000));
    let beforeCount=state.requests.filter(x=>x.endpoint==='refreshtoken').length;const t=await now();
    if(n===12){await page.evaluate(()=>{Object.defineProperty(document,'visibilityState',{configurable:true,get:()=> 'hidden'});document.dispatchEvent(new Event('visibilitychange'));});await page.waitForTimeout(40);r.observations.hidden_transition_acquisitions=state.requests.filter(x=>x.endpoint==='refreshtoken').length-beforeCount;beforeCount=state.requests.filter(x=>x.endpoint==='refreshtoken').length;}
    if(n===11)await page.clock.setSystemTime(t+70000);else await page.clock.setSystemTime(t+1);
    await page.clock.runFor(35000);await page.waitForTimeout(30);
    check('scheduled acquisition count',state.requests.filter(x=>x.endpoint==='refreshtoken').length-beforeCount,n===10?1:0);
    if(n===12)r.limits.push('Document visibility is a controlled property, not native OS background throttling.');
   }else if(n===13||n===15){await page.clock.setSystemTime((await now())+(n===15?86400000:70000));await page.evaluate(()=>{Object.defineProperty(document,'visibilityState',{configurable:true,value:'hidden'});document.dispatchEvent(new Event('visibilitychange'));Object.defineProperty(document,'visibilityState',{configurable:true,value:'visible'});document.dispatchEvent(new Event('visibilitychange'));});await page.getByTestId('Extend_Btn').waitFor({state:'visible'});check('timeout visible',(await snap()).dialog,true);if(n===13)block('Controlled resume reconciliation ran. Actual browser or device suspension was not performed.');}
   else if(n===14){const expiry=(await snap()).expiry;await page.clock.setSystemTime((await now())-600000);r.observations.clock={effective:await now(),absoluteExpiry:expiry};check('absolute expiry unchanged',(await snap()).expiry,expiry);}
   else if(n===16){const epoch=(await snap()).expiry;const z=await page.evaluate(()=>Intl.DateTimeFormat().resolvedOptions().timeZone);r.observations.timezone=z;check('Singapore timezone fixture',z,'Asia/Singapore');check('same epoch computation',(await snap()).expiry,epoch);block('A Singapore context ran, but this driver did not change timezone within the same running context. Exact transition remains unexecuted.');}
   else if(n===17){await setRefresh(jwt('equal-refresh',await now(),60000));await setAccess(jwt('equal-access',await now(),60000));const cutoff=(await snap()).expiry;await page.clock.fastForward(cutoff-await now()+1);check('zero acquisition after equal expiry',state.requests.filter(x=>x.endpoint==='refreshtoken'&&x.at>=cutoff).length,0);}
  }else if(c.id.startsWith('RN-R')){
   if(n<=8){await open();state.mode='hold';await click();await page.waitForFunction(()=>window.__base.Hooks.getHooks().store.isLoading);const old=(await snap()).token;
    if(n===1||n===2){await page.getByTestId('Logout_Btn').click({force:true});await page.clock.runFor(1001);}
    else if(n===5){await page.evaluate(()=>window.__base.Service.signal.relogin.abort());}
    else{await setAccess(jwt('replacement-B',await now()),true);if(n===8)await setAccess(jwt('replacement-A',await now()),true);}
    const expected=(await snap()).token;await release(n!==2&&n!==4&&n!==7);await page.waitForTimeout(30);check('old response does not change current access',(await snap()).token,expected);r.observations.old_access_sha256=hash(old);if(n===6||n===7)block('Completed replacement login was exercised. The separate fresh-login-pending interval was not held.');
   }else if(n>=15&&n<=17){state.holdAcquisition=true;await setRefresh(jwt('short-refresh',await now(),3600000));await page.evaluate(()=>{window.__oldAcq=window.__base.Service.getRefreshToken();});await page.waitForTimeout(30);await setAccess(jwt('new-access',await now()),n===17);await page.evaluate(()=>{window.__newAcq=window.__base.Service.getRefreshToken();});await page.waitForTimeout(30);r.observations.pending_count=held.length;await release();await page.waitForTimeout(30);if(n===15){check('new request starts',held.length>=1,true);block('Old network work is canceled, but internal acquisition owner and AbortSignal predicates require integration access.');}else if(n===16){const p=await page.evaluate(()=>!!window.__base.Service.getPendingRefreshToken());check('new acquisition remains pending',p,true);}else{await release();r.observations.final=safe(await snap());block('Refresh header ownership requires a distinct owner-bearing refresh fixture for complete current-epoch installation assertions.');}}
   else if(n===18||n===19){block('Exact simultaneous-delivery order requires a dedicated deterministic two-response hook fixture. Generic page delays would not establish both required orders.');}
   else if(n===20){block('A held protected request plus explicit unauthorized response is not bound in this browser runner. The old-response ownership assertion remains unexecuted.');}
  }else if(c.id.startsWith('RN-L')){
   if(n<=6){const total={1:1,2:2,3:10,4:1000,5:2,6:10}[n];const baselineTimers=Object.values((await snap()).probe.activeTimers).map(x=>x.delay).sort((a,b)=>a-b);
    for(let i=0;i<total;i++){await open();const before=await snap();if(n===5||n===6){state.mode='reject';await click();await settle();}state.mode='success';await recover();const after=await snap();check('cycle '+(i+1)+' exactly one closure',after.probe.closures-before.probe.closures,1);check('cycle '+(i+1)+' access installed',after.token,state.access);r.observations.completed_cycles=i+1;if((i+1)%10===0)await save();}
    const final=await snap();check('no unresolved owned requests',held.length,0);r.observations.final_timer_delays=Object.values(final.probe.activeTimers).map(x=>x.delay);r.observations.baseline_timer_delays=baselineTimers;
    block('All requested renewal cycles ran. Complete mounted listener counts were not instrumented, so the final listener-baseline predicate remains unverified.');
   }else if(n===9){for(let i=0;i<100;i++)await page.evaluate(()=>{Object.defineProperty(document,'visibilityState',{configurable:true,value:'hidden'});document.dispatchEvent(new Event('visibilitychange'));Object.defineProperty(document,'visibilityState',{configurable:true,value:'visible'});document.dispatchEvent(new Event('visibilitychange'));});r.observations.completed_cycles=100;check('authenticated owner retained',!!(await snap()).token,true);block('One hundred visibility reconciliations ran; mounted listener/timer baseline and native visibility behavior remain unverified.');}
   else if(n===10){await page.getByRole('button',{name:'Add Workspace',exact:true}).click();const ids=(await snap()).workspaceIds;for(let i=0;i<100;i++){const tabs=page.getByRole('tab');if(await tabs.count()<2)block('The workspace-switch UI did not expose two role=tab targets.');await tabs.nth(i%2).click({force:true});}r.observations.completed_cycles=100;check('workspace descriptors retained',(await snap()).workspaceIds,ids);block('One hundred workspace switches ran. Mounted listener/timer final baseline predicates remain unverified.');}
   else if(n===11){state.activityRenew=true;state.rotateRefresh=true;state.refreshLife=60000;const start=await now();await setRefresh(jwt('initial-short-refresh',start,60000));for(let i=0;i<960;i++){await page.clock.runFor(10000);await page.mouse.move(20+i%20,20+i%40);await page.clock.runFor(5000);if(i%120===0){r.observations.elapsed=await now()-start;await save();}}check('four controlled hours elapsed',await now()-start>=14400000,true);check('no fresh login prompt',await page.locator('[data-testid=Username] input').isVisible(),false);await validate();block('Four-hour controlled continuation and peer validation ran. A real fresh-SSO prompt observer and RSA protected endpoint are unavailable.');}
   else block(n===7?'One hundred complete logout/login cycles require a separate reauthentication fixture and listener baseline oracle.':'One hundred actual component mount/unmount cycles and final listener baseline are not bound in this browser runner.');
  }else if(c.id.startsWith('RN-H')){
   if(n===2){await open();state.mode='hold';await click();await page.waitForFunction(()=>window.__base.Hooks.getHooks().store.isLoading);r.observations.beforeReload=safe(await snap());await page.reload({waitUntil:'domcontentloaded',timeout:30000});await page.waitForTimeout(100);r.observations.afterReload=await page.evaluate(()=>({tokenPresent:!!localStorage.getItem('SET_TOKEN'),loginVisible:!!document.querySelector('[data-testid=Username] input')}));block('Reload ran. The first post-reload protected request with actual service-side principal validation remains unavailable.');}
   else if(n===5){await open();state.mode='hold';await click();await page.waitForFunction(()=>window.__base.Hooks.getHooks().store.isLoading);await ctx.setOffline(true);await page.evaluate(()=>window.__base.Service.signal.relogin.abort());await ctx.setOffline(false);state.mode='success';await settle();await recover();await validate();r.observations.reconnected=true;}
   else if(n===7){await ctx.setOffline(true);await page.clock.fastForward(4*3600000+1000);await ctx.setOffline(false);block('Offline expiry and reconnect ran. Real service rejection of expired RSA credentials requires a signed-token service fixture.');}
   else if(n===8||n===9){if(n===8){await page.evaluate(()=>{Storage.prototype.setItem=function(){throw new DOMException('Storage writes disabled','SecurityError');};});}else{r.observations.quota=await page.evaluate(()=>{let i=0;try{const payload='x'.repeat(262144);for(;i<100;i++)localStorage.setItem('quota-'+i,payload);}catch(e){return {writes:i,error:e.name};}return {writes:i,error:null};});check('actual local quota reached',r.observations.quota.error,'QuotaExceededError');}
    await open();state.mode='success';await click();await page.waitForTimeout(50);r.observations.afterStorageFailure=safe(await snap());check('storage failure observation retained',typeof r.observations.afterStorageFailure.token_sha256,'string');if(n===8)r.limits.push('Storage.setItem throws a controlled browser SecurityError; browser permission settings were not changed.');}
   else if(n===11){const other=await browser.newContext();const otherPage=await other.newPage();await otherPage.goto('http://127.0.0.1:8343/');const before=await otherPage.evaluate(()=>JSON.stringify({...localStorage}));await page.evaluate(()=>localStorage.setItem('isolation-probe','normal-context-write'));check('other isolated context storage unchanged',await otherPage.evaluate(()=>JSON.stringify({...localStorage})),before);await other.close();block('Two isolated contexts are separated. Complete renewal in normal persistent versus private windows was not executed.');}
   else block({'1':'A verified BFCache entry and restored pageshow.persisted event are unavailable in the development-server composition.','3':'A recoverable native renderer-crash driver with pre-navigation delivery checkpoint is not configured.','10':'Native duplicate-tab sessionStorage inheritance and first protected service observation lack an executable binding.'}[n]||'Required native lifecycle fixture is unavailable.');
  }else block('No exact executable binding for the complete canonical assertions.');
  r.final=safe(await snap());await capture('final');r.status='PASSED';
 }catch(e){r.status=e instanceof Blocked?(r.assertions.length?'PARTIALLY_EXECUTED':'BLOCKED'):(e instanceof assert.AssertionError?'FAILED':'ERROR');r.error=String(e.message).replace(/Bearer\s+[^\s]+/g,'[TOKEN]');if(r.status==='FAILED'||r.status==='ERROR')await capture('failure').catch(()=>{});}
 finally{clearTimeout(watchdog);r.completed_at=new Date().toISOString();if(state){r.requests=state.requests;r.observations.relogin_count=state.attempts;}await save();summary.results.push({id:r.id,status:r.status,assertions:r.assertions.length,failed_assertions:r.assertions.filter(x=>x.status==='FAILED').length,result:path.relative(out,path.join(folder,'result.json')),error:r.error});summary.counts=summary.results.reduce((a,x)=>(a[x.status]=(a[x.status]||0)+1,a),{});await persist();for(const h of held)await h.route.abort().catch(()=>{});if(ctx)await Promise.race([ctx.close().catch(()=>{}),new Promise(resolve=>setTimeout(resolve,3000))]);}
}
summary.completed_at=new Date().toISOString();await persist();await browser.close();console.log(JSON.stringify(summary.counts));
