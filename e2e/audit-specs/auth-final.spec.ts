import type {Page} from '@playwright/test';
import {test,expect} from '../support/audit-fixture.js';
import {commonAssertion,equalsToken,observe,rotate,runSessionCase,sessionSetup,sessionToken,T,visibility,type Session,type SystemWindow} from '../support/auth-session.js';
import {blockExternal,localBase,localPrefix,openLogin,seedWorkspaces,workspace} from '../support/local-app.js';
import {AdminApp} from '../support/admin-app.js';
import {LoginPage} from '../pages/login.page.js';
test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',serviceWorkers:'block',auditFixture:'Actual MFE; controlled identity, catalog, API responses and browser time. Signed current-BFF validation is used only where declared. Synthetic credentials and user aliases; no real identity provider acceptance.'});
const entity=(name='ENTITY-A')=>({id:1,name,applicationName:'Fixture',roleId:1,roleName:'Viewer',subjects:[]});
const drawer=[{id:1,label:'ENTITY-A catalog',tiles:[{title:'ENTITY-A App',subtitle:'Fixture',entryName:'Global',imageDarkTheme:'',imageLightTheme:'',emailSupport:'support@example.test',container:'@fm/unused',module:'/unused',tile:'/unused',entity:['ENTITY-A'],subject:'',isTemplate:true}]}];
async function setCatalog(page:Page){await page.evaluate(async data=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base')as any;m.LoginUtil.handleEntities({data:{entities:[data.entity]}});m.LoginUtil.handleDrawers({data:{drawers:data.drawers}});},{entity:entity(),drawers:drawer});}
async function logout(s:Session){await s.portal.avatarButton.click({force:true});await s.portal.logoutMenuItem.click({force:true});await s.portal.page.getByRole('dialog',{name:'Leave Now?',exact:true}).getByRole('button',{name:'Logout',exact:true}).click({force:true});await s.portal.page.clock.runFor(1000);await s.login.expectVisible();}
async function acceptLogin(page:Page,access:string,user='user-a',entities=[entity()],drawers=drawer){await page.route('**/api/auth/v2/sso/login',route=>route.fulfill({status:200,headers:{'single-ui-authorization':access},json:{result:true,userInfo:JSON.stringify({sub:user,fullName:user}),entities,drawers}}));}
test('AUTH-066 short access Home mount acquires recovery',async({page,audit})=>{
 const steps=await audit.defineCase('AUTH-066');let s!:Session;const R=sessionToken(600,'R'),B=sessionToken(900,'recovered');
 for(const step of steps)await audit.step(step.number,async()=>{
  if(step.number===1){s=await sessionSetup(page,audit,{accessExpires:10,holdInitialAcquisition:true,clockStartAtT:true,preserveInitialRequests:true});return;}
  if(step.number===2){expect((await observe(page)).refreshPresent).toBe(false);return;}
  if(step.number===3){await s.portal.expectVisible();return;}
  if(step.number===4){await page.clock.runFor(0);await expect.poll(()=>s.count('refreshtoken')).toBe(1);return;}
  if(step.number===5){await s.acceptAcquisition(R);return;}
  if(step.number===6){await page.clock.runFor(10000);return;}
  if(step.number===8){await s.portal.sessionTimeoutDialog.extendButton.click({force:true});return;}
  if(step.number===9){await expect.poll(()=>s.count('relogin')).toBe(1);return;}
  if(step.number===10){expect(await page.evaluate(async r=>(await(window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store.refreshToken===r,R)).toBe(true);return;}
  if(step.number===11){await s.acceptRelogin(B);return;}
  if(step.number===13){await expect.poll(()=>equalsToken(page,'token',B)).toBe(true);return;}
  if(!await commonAssertion(page,s,step.text))throw new Error(`Missing066step${step.number}`);
 });
});
test('AUTH-112 fresh login acquires distinct recovery',async({page,audit})=>{
 const steps=await audit.defineCase('AUTH-112');let s!:Session;const B=sessionToken(1200,'SESSION-B'),RB=sessionToken(14000,'R-B');
 for(const step of steps)await audit.step(step.number,async()=>{
  if(step.number===1){s=await sessionSetup(page,audit,{refreshExpires:13524,expectedAcquisitionAccess:B});await logout(s);return;}
  if(step.number===2){await s.login.expectVisible();return;}
  if(step.number===3){await acceptLogin(page,B);s.control.holdAcquisition=true;s.requests.length=0;return;}
  if(step.number===4){await s.login.fillUsername('user-a');return;}
  if(step.number===5){await s.login.fillPassword('FixturePass1!');return;}
  if(step.number===6){await s.login.clickSignInButton();return;}
  if(step.number===8){await visibility(page,'hidden');return;}
  if(step.number===9){await expect.poll(()=>s.count('refreshtoken')).toBe(1);expect(s.requests.find(x=>x.endpoint==='refreshtoken')?.accessMatchesB).toBe(true);return;}
  if(step.number===10){await s.acceptAcquisition(RB);return;}
  if(step.number===11){await expect.poll(()=>equalsToken(page,'refreshToken',RB)).toBe(true);expect(RB).not.toBe(s.refreshR);return;}
  if(!await commonAssertion(page,s,step.text))throw new Error(`Missing112step${step.number}`);
 });
});
test('AUTH-117 stale prior-user response cannot overwrite new user',async({page,audit})=>{
 let release!:()=>void;const held=new Promise<void>(resolve=>{release=resolve;});let pending=false;
 await runSessionCase(page,audit,'AUTH-117',{}, {
  3:async s=>{await page.route('**/api/audit/prior-user',async route=>{pending=true;await held;await route.fulfill({status:200,headers:{'single-ui-authorization':s.accessA},json:{userInfo:JSON.stringify({sub:'user-a'}),entities:[entity()]}});});
   await page.evaluate(async()=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');void m.Service.postService('/audit/prior-user',{}).catch(()=>{});});await expect.poll(()=>pending).toBe(true);await logout(s);await acceptLogin(page,sessionToken(1200,'user-b'),'user-b');await s.login.fillUsername('user-b');await s.login.fillPassword('FixturePass1!');await s.login.clickSignInButton();await s.portal.expectVisible();},
  4:async()=>{release();},5:async s=>{await s.portal.avatarButton.click({force:true});},6:async s=>{await s.portal.avatarMenu.getByRole('menuitem').filter({hasText:'user-b'}).click({force:true});},
  7:async()=>{await expect(page.getByTestId('entitlement-profile-label-box').locator('.MuiTypography-h5')).toHaveText('user-b');},
  8:async()=>{const identity=await page.evaluate(async()=>{const s=(await(window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store as any;return s.user?.sub;});expect(identity).toBe('user-b');},
 });
});
test('AUTH-138 recovery removes old entity and controls',async({page,audit})=>{
 await runSessionCase(page,audit,'AUTH-138',{accessExpires:0,refreshExpires:600},{
  5:async()=>{await setCatalog(page);},6:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
  7:async s=>{await expect.poll(()=>s.relogin.length).toBe(1);for(const route of s.relogin.splice(0))await route.fulfill({status:200,headers:{'single-ui-authorization':sessionToken(900,'B')},json:{result:true,entities:[],drawers:[],userInfo:JSON.stringify({sub:'user-a',fullName:'user-a'})}});},8:async s=>{await s.portal.root.getByText('New Tile',{exact:true}).click({force:true});await page.clock.runFor(500);await page.waitForLoadState('networkidle');await audit.record('drawer-inspection',{action:'Open New Tile to inspect chosen controlled ENTITY-A App title; Escape closes this inspection before the canonical avatar action.',limit:'Canonical control identity remains UNVERIFIED.'});await audit.capture('removed-entity-drawer-inspection','Drawer state for the controlled ENTITY-A App probe.');await expect(page.getByText('ENTITY-A App',{exact:true})).toHaveCount(0);await page.keyboard.press('Escape');await page.clock.runFor(300);await expect(page.getByTestId(`${localPrefix}_drawer`).getByText('Tile Options',{exact:true})).not.toBeVisible();},
  9:async s=>{await s.portal.avatarButton.click({force:true});},10:async s=>{await s.portal.avatarMenu.getByRole('menuitem').filter({hasText:'user-a'}).click({force:true});},
  11:async()=>{await expect(page.getByTestId('entitlement-profile-label-box').locator('.MuiTypography-h5')).toHaveText('user-a');},12:async()=>{expect(await page.evaluate(async()=>JSON.stringify((await(window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store.entities))).not.toContain('ENTITY-A');},
 });
});
test('AUTH-137 empty new login removes old catalog',async({page,audit})=>{
 const steps=await audit.defineCase('AUTH-137');const login=new LoginPage(page,localPrefix);
 for(const step of steps)await audit.step(step.number,async()=>{
  if(step.number===1){await blockExternal(page);await seedWorkspaces(page,[workspace('WS-A','WS-A')]);await openLogin(page);return;}
  if(step.number===2){await setCatalog(page);await acceptLogin(page,sessionToken(1200,'new'),'user-a',[],[]);return;}
  if(step.number===3){await login.fillUsername('user-a');return;}
  if(step.number===4){await login.fillPassword('FixturePass1!');return;}
  if(step.number===5){await login.clickSignInButton();return;}
  if(step.number===6){await page.getByText('New Tile',{exact:true}).click({force:true});await expect(page.getByText('ENTITY-A App',{exact:true})).toHaveCount(0);return;}
  if(step.number===7){expect(await page.evaluate(async()=>JSON.stringify((await(window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store as any))).not.toContain('ENTITY-A App');return;}
 });
});
test('AUTH-144 forged entitlement is rejected by current server',async({page,audit})=>{
 const steps=await audit.defineCase('AUTH-144');const app=new AdminApp(page,'Category','AUTH-144');let status=0;
 for(const step of steps)await audit.step(step.number,async()=>{
  if(step.number===1){app.principal='user-a';app.workspaceLabel='WS-A';await app.setup();await app.open();return;}
  if(step.number===2){await app.portal.expectWorkspaceTabVisible('WS-A');return;}
  if(step.number===3){const token=await page.request.post('http://127.0.0.1:8090/api/auth/local/fixture/token',{data:{subject:'user-a',expiresInSeconds:600}});await rotate(page,(await token.json()).token);await audit.record('forged-entitlement',{accessSignature:'Valid local server-signed fixture',entitlementSignature:'Unsigned forged admin fixture from AdminApp',target:'Actual Category editor update control; canonical exact identity remains unapproved'});
   await page.route('**/api/auth/v1/fmo/admin/category/update',async route=>{const response=await route.fetch({url:'http://127.0.0.1:8090/api/auth/v1/fmo/admin/category/update'});status=response.status();await audit.record('actual-admin-rejection',{status,body:await response.text(),access:'Valid current-server signature',entitlement:'Unsigned forged browser token',signatureCheck:'Current AdminModuleUtil.validate invokes JwtTokenUtil.validateToken before entitlement issuer and role checks.'});await route.fulfill({response});});return;}
  if(step.number===4){await app.action('Edit').click({force:true});await app.footerButton('Update').click({force:true});return;}
  if(step.number===5){await expect.poll(()=>status).toBeGreaterThanOrEqual(400);return;}
  if(step.number===6){const alert=page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]');await expect(alert).toContainText('API request failed');await expect(alert).not.toContainText(/success/i);await audit.record('server-rejection',{status,sourceRevision:'834b4155232222347220e47139a502ee43a9cbdf',successObservation:'Chosen admin notification text',limit:'Canonical success observation identity remains UNVERIFIED.'});return;}
 });
});
test('AUTH-116 independent contexts preserve separate server sessions',async({page,browser,audit},testInfo)=>{
 const steps=await audit.defineCase('AUTH-116');let a!:Session,b!:Session;let second:Page|undefined;let context:Awaited<ReturnType<typeof browser.newContext>>|undefined;let B='';let validation:any;
 const base='http://127.0.0.1:8090/api/auth';
 try{for(const step of steps)await audit.step(step.number,async()=>{
  if(step.number===1){a=await sessionSetup(page,audit,{});context=await browser.newContext({serviceWorkers:'block'});second=await context.newPage();b=await sessionSetup(second,audit,{});
   for(const [target,name]of [[page,'SESSION-A'],[second,'SESSION-B']]as const){const response=await target.request.post(`${base}/local/fixture/token`,{data:{id:`${name}-${Date.now()}`,expiresInSeconds:Math.ceil((T-Date.now())/1000)+900}});const token=(await response.json()).token;await rotate(target,token);if(name==='SESSION-B')B=token;}
   await page.route('**/api/auth/v2/sso/logout',async route=>{const response=await route.fetch({url:`${base}/v2/sso/logout`});await route.fulfill({response});});return;}
  if(step.number===2){await a.portal.avatarButton.click({force:true});await a.portal.logoutMenuItem.click({force:true});return;}
  if(step.number===3){await page.getByRole('dialog',{name:'Leave Now?',exact:true}).getByRole('button',{name:'Logout',exact:true}).click({force:true});return;}
  if(step.number===4){await page.clock.runFor(1000);return;}
  if(step.number===8){const response=await second!.request.post(`${base}/v2/sso/validate`,{data:{singleUIAuthorization:B}});validation=await response.json();await audit.record('context-b-validation',{status:response.status(),result:validation.result});return;}
  if(step.number===9){expect(validation.result).toBe(true);expect(await equalsToken(second!,'token',B)).toBe(true);return;}
  if(step.number===10){await b.portal.expectWorkspaceTabVisible('WS-A');const path=testInfo.outputPath('context-b-final.png');await second!.screenshot({path,fullPage:true});await testInfo.attach('CTX-B separate session visible',{path,contentType:'image/png'});return;}
  if(!await commonAssertion(page,a,step.text))throw new Error(`Missing116step${step.number}`);
 });}finally{await context?.close();}
});
