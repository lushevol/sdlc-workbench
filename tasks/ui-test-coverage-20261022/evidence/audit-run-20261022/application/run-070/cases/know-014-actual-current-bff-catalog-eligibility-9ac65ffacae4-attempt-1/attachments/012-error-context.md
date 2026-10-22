# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: knowledge-current-bff.spec.ts >> KNOW-014 actual current BFF catalog eligibility
- Location: e2e/audit-specs/knowledge-current-bff.spec.ts:26:42

# Error details

```
Error: Canonical open-authorization operation and agreed denial state have no approved current shell binding.
```

# Page snapshot

```yaml
- generic [ref=e4]:
  - generic [ref=e7]:
    - img "Markets Operations One logo" [ref=e9]
    - generic [ref=e10]:
      - generic [ref=e11] [cursor=pointer]:
        - img "new tile" [ref=e13]
        - generic [ref=e14]: New Tile
      - generic [ref=e15]:
        - img "dark" [ref=e17]
        - generic [ref=e19]:
          - text: dark
          - checkbox "Theme Switch" [ref=e22] [cursor=pointer]
      - group [ref=e26]:
        - generic [ref=e27]: 06:34 UTC
        - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
      - button "User Profiles" [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button "Share Feedback" [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist "workspaces" [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region "T-TRADE" [ref=e48]:
          - textbox "Workspace Name" [ref=e52]: T-TRADE
      - button "Add Workspace" [ref=e54] [cursor=pointer]
    - tabpanel [ref=e59]
```

# Test source

```ts
  1  | import {test,expect} from '../support/audit-fixture.js';
  2  | import {LoginPage} from '../pages/login.page.js';
  3  | import {PortalPage} from '../pages/portal.page.js';
  4  | import {blockExternal,localBase,localPrefix,openLogin,seedWorkspaces,workspace} from '../support/local-app.js';
  5  | 
  6  | test.describe.configure({mode:'default'});
  7  | test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',serviceWorkers:'block',auditFixture:'Actual MFE and current single-ui-bff auth controller, AdminModuleUtil catalog filtering, AuthFilterExecutor, PostgreSQL18.4 with exact migrations, and JPA repositories. Synthetic local OUD identity Alice and controlled EMS2 entity response. External EMS3 adapter disabled; isolated Spring Boot3 bootstrap replaces production Boot4 configuration. KNOW014 records the missing shell open-authorization operation. KNOW015/017 use proposed URL navigation overlays because canonical targets remain undefined. No protected tenant fields, denial states, or production provider acceptance are fabricated.'});
  8  | const bff='http://127.0.0.1:8090/api/auth';
  9  | const sourceRevision='834b4155232222347220e47139a502ee43a9cbdf';
  10 | const common={ems2Role:'FMO_ADMIN',active:true,createdAt:'2026-10-22T00:00:00Z',updatedAt:'2026-10-22T00:00:00Z',createdBy:'admin-a',updatedBy:'admin-a',orderNo:1};
  11 | const catalog={categories:[{...common,applicationCategoryId:1,label:'Fixture Policy'}],importMaps:[{...common,importMapId:1,keyName:'test_container',path:'http://localhost:8128/audit-fixtures/test-container.js'}],tiles:[
  12 |  {title:'T-TRADE',ems2Entities:'E-TRADE',ems2Subject:'S-VIEW'},
  13 |  {title:'T-CASH',ems2Entities:'E-CASH',ems2Subject:'S-VIEW'},
  14 |  {title:'T-REPORT',ems2Entities:'E-RR-A,E-RR-B',ems2Subject:''},
  15 | ].map((tile,index)=>({...common,...tile,applicationTileId:index+1,subtitle:'',module:'test',tile:tile.title==='T-TRADE'?'trade':tile.title==='T-CASH'?'cash':'report',entryName:'Global',filterRule:null,template:false,imageLightTheme:'',imageDarkTheme:'',emailSupport:'support@example.test',applicationCategory:{applicationCategoryId:1},importMap:{importMapId:1}}))};
  16 | const entity=(name:string,subjects:string[]=[],id=1)=>({id,name,applicationName:'Fixture',roleId:id,roleName:'Viewer',subjects:subjects.map((subject,index)=>({id:index+1,name:subject,longName:subject,actions:[]}))});
  17 | const permissions:Record<string,ReturnType<typeof entity>[]>={
  18 |  'KNOW-001':[entity('E-RR-B')], 'KNOW-002':[entity('E-TRADE',['S-VIEW'])],
  19 |  'KNOW-003':[entity('E-TRADE',['S-EDIT'])], 'KNOW-004':[entity('E-CASH',['S-VIEW'])],
  20 |  'KNOW-005':[entity('E-RR-A')], 'KNOW-006':[entity('E-TRADE')],
  21 |  'KNOW-007':[entity('E-UNREGISTERED')], 'KNOW-008':[entity('E-TRADE',['S-VIEW'])],
  22 |  'KNOW-009':[entity('E-RR-A')], 'KNOW-010':[entity('E-RR-A'),entity('E-RR-B',[],2)],
  23 |  'KNOW-014':[entity('E-TRADE',['S-VIEW'])], 'KNOW-015':[], 'KNOW-017':[],
  24 | };
  25 | 
  26 | for(const id of Object.keys(permissions))test(`${id} actual current BFF catalog eligibility`,async({page,audit})=>{
  27 |  const steps=await audit.defineCase(id);const portal=new PortalPage(page,localPrefix),login=new LoginPage(page,localPrefix);
  28 |  const drawer=page.getByTestId(`${localPrefix}_drawer`);let loginSettled=false;let loginStatus=0;let loginResult:unknown;let actualDrawers:any[]=[];
  29 |  const requests:{method:string,url:string}[]=[];let openStart=0;let guest=false;
  30 |  async function fixture(operation:string,data:unknown={}){const result=await page.request.post(`${bff}/local/fixture/${operation}`,{data});expect(result.ok(),`Fixture ${operation}: HTTP${result.status()}`).toBe(true);return result.json();}
  31 |  async function databaseTile(title:string){const result=await fixture('sql',{statements:[`SELECT title,ems2_entities AS entities,ems2_subject AS subject FROM post_trade_portal_service.application_tile WHERE title='${title}'`]});return result.results[0].rows;}
  32 |  async function signIn(){await login.fillUsername('alice');await login.fillPassword('FixturePass1!');await login.clickSignInButton();await expect.poll(()=>loginSettled).toBe(true);await page.waitForLoadState('networkidle');}
  33 |  for(const step of steps)await audit.step(step.number,async()=>{
  34 |   if(step.number===1){await blockExternal(page);await seedWorkspaces(page,[workspace('WS-A','WS-A')]);page.on('request',request=>requests.push({method:request.method(),url:request.url()}));await page.route('**/api/auth/**',async route=>{const pathname=new URL(route.request().url()).pathname;const response=await route.fetch({url:`${bff}${pathname.replace('/api/auth','')}`});if(pathname.endsWith('/sso/login')){loginStatus=response.status();const body=await response.json();loginResult=body.result;actualDrawers=body.drawers??[];await audit.record('actual-filtered-login',{sourceRevision,status:loginStatus,result:loginResult,entities:body.entities?.map((value:any)=>({name:value.name,subjects:value.subjects?.map((subject:any)=>({name:subject.name,longName:subject.longName}))})),drawers:actualDrawers,limits:['Controlled EMS2 input; no canned catalog response. Current AdminModuleUtil and AuthFilterExecutor compute these drawers.']});loginSettled=true;}await route.fulfill({response});});await openLogin(page);return;}
  35 |   if(step.number===2){await fixture('reset');await fixture('seed',catalog);const titles=await fixture('sql',{statements:['SELECT title FROM post_trade_portal_service.application_tile ORDER BY application_tile_id']});expect(titles.results[0].rows.map((row:any)=>row.title)).toEqual(['T-TRADE','T-CASH','T-REPORT']);await audit.record('actual-catalog-seed',{sourceRevision,database:'Disposable PostgreSQL18.4',catalog});return;}
  36 |   if(step.number===3){expect(await databaseTile('T-TRADE')).toEqual([{title:'T-TRADE',entities:'E-TRADE',subject:'S-VIEW'}]);return;}
  37 |   if(step.number===4){expect(await databaseTile('T-CASH')).toEqual([{title:'T-CASH',entities:'E-CASH',subject:'S-VIEW'}]);return;}
  38 |   if(step.number===5&&id!=='KNOW-015'){expect(await databaseTile('T-REPORT')).toEqual([{title:'T-REPORT',entities:'E-RR-A,E-RR-B',subject:''}]);return;}
  39 |   if(step.number===6&&!['KNOW-014','KNOW-015','KNOW-017'].includes(id)){await fixture('seed',{entities:permissions[id]});await audit.record('controlled-ems2-input',{subject:'alice',entities:permissions[id],externalProvider:'SUBSTITUTED'});if(!['KNOW-001','KNOW-007'].includes(id))await signIn();return;}
  40 |   if(step.text.includes('visible catalog contains')){await fixture('seed',{entities:permissions[id]});await signIn();await portal.expectVisible();await portal.root.getByTestId(`${localPrefix}_new_tile`).click();await expect(drawer.getByText('T-TRADE',{exact:true})).toBeVisible();return;}
  41 |   if(step.text.includes('next tile authorization response')){await fixture('seed',{entities:[]});openStart=requests.length;await audit.record('revoked-provider-state',{sourceRevision,nextControlledEMS2Entities:[],openAuthorizationEndpoint:'NONE_DECLARED_BY_CURRENT_SHELL',limit:'The fixture changes real local EMS2 input. No tile authorization endpoint or response is invented.'});return;}
  42 |   if(step.text.includes('clicks the text "T-TRADE"')){await drawer.getByText('T-TRADE',{exact:true}).click();await page.waitForLoadState('networkidle');return;}
> 43 |   if(step.text.includes('after the open authorization response settles')){const after=requests.slice(openStart);const serviceRequests=after.filter(request=>new URL(request.url).pathname.startsWith('/api/'));await audit.record('open-operation-observation',{sourceRevision,requests:after,serviceRequests,expected:'Canonical tile open authorization response',observed:'Current shell loads a SystemJS container. No shell tile authorization operation is declared.',limits:['The protected business tenant is unavailable.','A missing shell request cannot establish tenant API authorization behavior.','Canonical protected field identities and the agreed denial state remain undefined.']});expect(serviceRequests,'No service authorization response followed the actual shell open action.').not.toHaveLength(0);throw new Error('Canonical open-authorization operation and agreed denial state have no approved current shell binding.');}
     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        ^ Error: Canonical open-authorization operation and agreed denial state have no approved current shell binding.
  44 |   if(step.text.includes('no tenant entities')||step.text.includes('no registered portal entity')){await fixture('seed',{entities:[]});return;}
  45 |   if(step.text.includes('overrides its configured entity list')){await fixture('sql',{statements:["UPDATE post_trade_portal_service.application_tile SET ems2_entities='',ems2_subject='' WHERE title='T-REPORT'"]});expect(await databaseTile('T-REPORT')).toEqual([{title:'T-REPORT',entities:'',subject:''}]);await signIn();return;}
  46 |   if(step.text.includes('synthetic guest flag')){guest=true;await page.evaluate(()=>localStorage.setItem('UI_AUDIT_SYNTHETIC_GUEST','true'));await audit.record('synthetic-guest-overlay',{key:'UI_AUDIT_SYNTHETIC_GUEST',value:'true',sourceConsumer:'No current MFE guest-flag consumer was found.',limit:'Synthetic flag only; no production guest policy is inferred.'});await signIn();return;}
  47 |   if(step.text.includes('requests opening report tile')){const url=`${localBase}/?show_normal_login=Y&container=test_container&module=test&tile=report`;openStart=requests.length;await audit.record('proposed-navigation-overlay',{url,target:'Actual browser navigation to portal with controlled report module coordinates',guest,canonicalBinding:'UNVERIFIED',limits:['Canonical request-opening control identity is undefined.','No protected report fields are fabricated.','Only actual catalog exclusion and lack of module loading are measured.']});await page.goto(url);await page.waitForLoadState('networkidle');return;}
  48 |   if(step.text.includes('no protected T-REPORT business field')){const report=actualDrawers.flatMap((value:any)=>value.tiles??[]).filter((tile:any)=>tile.title==='T-REPORT');expect(report).toHaveLength(0);const after=requests.slice(openStart);expect(after.filter(request=>new URL(request.url).pathname.endsWith('/audit-fixtures/test-container.js'))).toHaveLength(0);const workspaceVisible=await portal.workspaceList.isVisible();if(workspaceVisible)await expect(page.getByText('Start customizing your workspace',{exact:true})).toBeVisible();else await login.expectVisible();await audit.record('unloaded-report-probe',{filteredReportEntries:report.length,postNavigationRequests:after,workspaceVisible,visibleState:workspaceVisible?'Empty workspace':'Login',limit:'Catalog exclusion, empty-workspace or login state, and no module request are asserted. Protected tenant fields remain undefined and unavailable.'});return;}
  49 |   if(step.text.includes('effective catalog response contains no T-REPORT')){expect(actualDrawers.flatMap((value:any)=>value.tiles??[]).filter((tile:any)=>tile.title==='T-REPORT')).toHaveLength(0);return;}
  50 |   if(step.text.includes('deployment enables')){await login.expectVisible();return;}
  51 |   if(step.text.includes('fills the textbox')){await login.fillUsername('alice');return;}
  52 |   if(step.text.includes('fills the text input')){await login.fillPassword('FixturePass1!');return;}
  53 |   if(step.text.includes('clicks the button labeled "Sign In"')){await login.clickSignInButton();await expect.poll(()=>loginSettled).toBe(true);await page.waitForLoadState('networkidle');return;}
  54 |   if(step.text.includes('clicks the text "New Tile"')){await portal.expectVisible();await portal.root.getByTestId(`${localPrefix}_new_tile`).click();return;}
  55 |   if(step.text.includes('authenticated portal workspace is absent')){expect(loginSettled).toBe(true);await expect(portal.workspaceList).toHaveCount(0);return;}
  56 |   if(step.text.includes('no content from T-TRADE')){for(const title of ['T-TRADE','T-CASH','T-REPORT'])await expect(page.getByText(title,{exact:true})).toHaveCount(0);return;}
  57 |   if(step.text.includes('panel headed by "Tile Options" is visible')){await expect(drawer.getByText('Tile Options',{exact:true})).toBeVisible();return;}
  58 |   const count=/contains exactly (\d+) occurrences of tile title text "([^"]+)"/.exec(step.text);
  59 |   if(count){await expect(drawer.getByText(count[2],{exact:true})).toHaveCount(Number(count[1]));const filtered=actualDrawers.flatMap((value:any)=>value.tiles??[]).filter((tile:any)=>tile.title===count[2]);expect(filtered).toHaveLength(Number(count[1]));return;}
  60 |   throw new Error(`Missing ${id} step ${step.number}: ${step.text}`);
  61 |  });
  62 | });
  63 | 
```