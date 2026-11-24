import {test,expect} from '../support/audit-fixture.js';
import {LoginPage} from '../pages/login.page.js';
import {PortalPage} from '../pages/portal.page.js';
import {blockExternal,localPrefix,openLogin,seedWorkspaces,workspace} from '../support/local-app.js';

test.describe.configure({mode:'default'});
test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',serviceWorkers:'block',auditFixture:'Actual MFE and current single-ui-bff auth controller, AdminModuleUtil catalog filtering, AuthFilterExecutor, PostgreSQL18.4 with exact migrations, and JPA repositories. Synthetic local OUD identity Alice and controlled EMS2 entity response. External EMS3 adapter disabled; isolated Spring Boot3 bootstrap replaces production Boot4 configuration. No production provider acceptance is measured.'});
const bff='http://127.0.0.1:8090/api/auth';
const sourceRevision='834b4155232222347220e47139a502ee43a9cbdf';
const common={ems2Role:'FMO_ADMIN',active:true,createdAt:'2026-10-22T00:00:00Z',updatedAt:'2026-10-22T00:00:00Z',createdBy:'admin-a',updatedBy:'admin-a',orderNo:1};
const catalog={categories:[{...common,applicationCategoryId:1,label:'Fixture Policy'}],importMaps:[{...common,importMapId:1,keyName:'test_container',path:'http://localhost:8128/audit-fixtures/test-container.js'}],tiles:[
 {title:'T-TRADE',ems2Entities:'E-TRADE',ems2Subject:'S-VIEW'},
 {title:'T-CASH',ems2Entities:'E-CASH',ems2Subject:'S-VIEW'},
 {title:'T-REPORT',ems2Entities:'E-RR-A,E-RR-B',ems2Subject:''},
].map((tile,index)=>({...common,...tile,applicationTileId:index+1,subtitle:'Controlled policy tile',module:'test',tile:'tile-global',entryName:'Global',filterRule:null,template:false,imageLightTheme:'',imageDarkTheme:'',emailSupport:'support@example.test',applicationCategory:{applicationCategoryId:1},importMap:{importMapId:1}}))};
const entity=(name:string,subjects:string[]=[],id=1)=>({id,name,applicationName:'Fixture',roleId:id,roleName:'Viewer',subjects:subjects.map((subject,index)=>({id:index+1,name:subject,longName:subject,actions:[]}))});
const permissions:Record<string,ReturnType<typeof entity>[]>={
 'KNOW-001':[entity('E-RR-B')], 'KNOW-002':[entity('E-TRADE',['S-VIEW'])],
 'KNOW-003':[entity('E-TRADE',['S-EDIT'])], 'KNOW-004':[entity('E-CASH',['S-VIEW'])],
 'KNOW-005':[entity('E-RR-A')], 'KNOW-006':[entity('E-TRADE')],
 'KNOW-007':[entity('E-UNREGISTERED')], 'KNOW-008':[entity('E-TRADE',['S-VIEW'])],
 'KNOW-009':[entity('E-RR-A')], 'KNOW-010':[entity('E-RR-A'),entity('E-RR-B',[],2)],
};

for(const id of Object.keys(permissions))test(`${id} actual current BFF catalog eligibility`,async({page,audit})=>{
 const steps=await audit.defineCase(id);const portal=new PortalPage(page,localPrefix),login=new LoginPage(page,localPrefix);
 const drawer=page.getByTestId(`${localPrefix}_drawer`);let loginSettled=false;let loginStatus=0;let loginResult:unknown;let actualDrawers:any[]=[];
 async function fixture(operation:string,data:unknown={}){const result=await page.request.post(`${bff}/local/fixture/${operation}`,{data});expect(result.ok(),`Fixture ${operation}: HTTP${result.status()}`).toBe(true);return result.json();}
 async function databaseTile(title:string){const result=await fixture('sql',{statements:[`SELECT title,ems2_entities AS entities,ems2_subject AS subject FROM post_trade_portal_service.application_tile WHERE title='${title}'`]});return result.results[0].rows;}
 async function signIn(){await login.fillUsername('alice');await login.fillPassword('FixturePass1!');await login.clickSignInButton();await expect.poll(()=>loginSettled).toBe(true);}
 for(const step of steps)await audit.step(step.number,async()=>{
  if(step.number===1){await blockExternal(page);await seedWorkspaces(page,[workspace('WS-A','WS-A')]);await page.route('**/api/auth/**',async route=>{const pathname=new URL(route.request().url()).pathname;const response=await route.fetch({url:`${bff}${pathname.replace('/api/auth','')}`});if(pathname.endsWith('/sso/login')){loginStatus=response.status();const body=await response.json();loginResult=body.result;actualDrawers=body.drawers??[];await audit.record('actual-filtered-login',{sourceRevision,status:loginStatus,result:loginResult,entities:body.entities?.map((value:any)=>({name:value.name,subjects:value.subjects?.map((subject:any)=>({name:subject.name,longName:subject.longName}))})),drawers:actualDrawers,limits:['Controlled EMS2 input; no canned catalog response. Current AdminModuleUtil and AuthFilterExecutor compute these drawers.']});loginSettled=true;}await route.fulfill({response});});await openLogin(page);return;}
  if(step.number===2){await fixture('reset');await fixture('seed',catalog);const titles=await fixture('sql',{statements:['SELECT title FROM post_trade_portal_service.application_tile ORDER BY application_tile_id']});expect(titles.results[0].rows.map((row:any)=>row.title)).toEqual(['T-TRADE','T-CASH','T-REPORT']);await audit.record('actual-catalog-seed',{sourceRevision,database:'Disposable PostgreSQL18.4',catalog});return;}
  if(step.number===3){expect(await databaseTile('T-TRADE')).toEqual([{title:'T-TRADE',entities:'E-TRADE',subject:'S-VIEW'}]);return;}
  if(step.number===4){expect(await databaseTile('T-CASH')).toEqual([{title:'T-CASH',entities:'E-CASH',subject:'S-VIEW'}]);return;}
  if(step.number===5){expect(await databaseTile('T-REPORT')).toEqual([{title:'T-REPORT',entities:'E-RR-A,E-RR-B',subject:''}]);return;}
  if(step.number===6){await fixture('seed',{entities:permissions[id]});await audit.record('controlled-ems2-input',{subject:'alice',entities:permissions[id],externalProvider:'SUBSTITUTED'});if(!['KNOW-001','KNOW-007'].includes(id))await signIn();return;}
  if(step.text.includes('deployment enables')){await login.expectVisible();return;}
  if(step.text.includes('fills the textbox')){await login.fillUsername('alice');return;}
  if(step.text.includes('fills the text input')){await login.fillPassword('FixturePass1!');return;}
  if(step.text.includes('clicks the button labeled "Sign In"')){await login.clickSignInButton();await expect.poll(()=>loginSettled).toBe(true);return;}
  if(step.text.includes('clicks the text "New Tile"')){await portal.expectVisible();await portal.root.getByTestId(`${localPrefix}_new_tile`).click();return;}
  if(step.text.includes('authenticated portal workspace is absent')){expect(loginSettled).toBe(true);await expect(portal.workspaceList).toHaveCount(0);return;}
  if(step.text.includes('no content from T-TRADE')){for(const title of ['T-TRADE','T-CASH','T-REPORT'])await expect(page.getByText(title,{exact:true})).toHaveCount(0);return;}
  if(step.text.includes('panel headed by "Tile Options" is visible')){await expect(drawer.getByText('Tile Options',{exact:true})).toBeVisible();return;}
  const count=/contains exactly (\d+) occurrences of tile title text "([^"]+)"/.exec(step.text);
  if(count){await expect(drawer.getByText(count[2],{exact:true})).toHaveCount(Number(count[1]));const filtered=actualDrawers.flatMap((value:any)=>value.tiles??[]).filter((tile:any)=>tile.title===count[2]);expect(filtered).toHaveLength(Number(count[1]));return;}
  throw new Error(`Missing ${id} step ${step.number}: ${step.text}`);
 });
});
