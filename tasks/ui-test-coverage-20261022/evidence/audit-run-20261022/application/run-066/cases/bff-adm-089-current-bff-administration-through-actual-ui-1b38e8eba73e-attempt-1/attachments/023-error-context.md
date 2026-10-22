# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: bff-admin.spec.ts >> BFF-ADM-089 current BFF administration through actual UI
- Location: e2e/audit-specs/bff-admin.spec.ts:11:2

# Error details

```
Error: Committed UI field Filter Rule

expect(received).toBe(expected) // Object.is equality

Expected: ""
Received: null
```

# Page snapshot

```yaml
- generic [ref=e4]:
  - generic [ref=e10]:
    - generic [ref=e11] [cursor=pointer]: New Tile
    - generic [ref=e19]:
      - text: dark
      - checkbox [ref=e22] [cursor=pointer]
    - group [ref=e26]:
      - generic [ref=e27]: 06:28 UTC
      - checkbox [checked] [ref=e30] [cursor=pointer]
    - button [ref=e34] [cursor=pointer]:
      - generic [ref=e35]: A
    - button [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region [ref=e48]:
          - textbox [ref=e52]: Tile
      - button [ref=e54] [cursor=pointer]
    - tabpanel [ref=e59]:
      - generic [ref=e61]:
        - generic [ref=e62]:
          - generic [ref=e64]:
            - generic [ref=e65]: Application Category
            - generic [ref=e66]:
              - combobox [ref=e67]: category-a
              - button [ref=e69] [cursor=pointer]
          - button [ref=e72] [cursor=pointer]
        - generic [ref=e75]:
          - button [ref=e76] [cursor=pointer]: Create New Tile
          - generic [ref=e77]:
            - grid [ref=e78]:
              - button [ref=e80] [cursor=pointer]: Export
              - generic [ref=e84]:
                - rowgroup [ref=e85]:
                  - row [ref=e86]:
                    - columnheader [ref=e87]:
                      - generic [ref=e88]: Actions
                    - columnheader [ref=e90] [cursor=pointer]:
                      - generic [ref=e91]: Tile Name
                    - columnheader [ref=e93] [cursor=pointer]:
                      - generic [ref=e94]: Description
                    - columnheader [ref=e96] [cursor=pointer]:
                      - generic [ref=e97]: Image URL for Dark Theme
                    - columnheader [ref=e99] [cursor=pointer]:
                      - generic [ref=e100]: Image URL for Light Theme
                    - columnheader [ref=e102] [cursor=pointer]:
                      - generic [ref=e103]: Container
                    - columnheader [ref=e105] [cursor=pointer]:
                      - generic [ref=e106]: Module Path
                    - columnheader [ref=e108] [cursor=pointer]:
                      - generic [ref=e109]: Tile Path
                    - columnheader [ref=e111] [cursor=pointer]:
                      - generic [ref=e112]: Role Subject
                    - columnheader [ref=e114] [cursor=pointer]:
                      - generic [ref=e115]: Role Entities
                - rowgroup [ref=e117]:
                  - row [ref=e118]:
                    - cell [ref=e119]:
                      - menu [ref=e120]:
                        - menuitem [ref=e121] [cursor=pointer]
                        - menuitem [ref=e124] [cursor=pointer]
                        - menuitem [disabled]
                        - menuitem [ref=e127] [cursor=pointer]
                    - cell [ref=e130]: OLD
                    - cell [ref=e131]: Fixture tile
                    - cell [ref=e132]: dark-a.png
                    - cell [ref=e133]: light-a.png
                    - cell [ref=e134]: container-a
                    - cell [ref=e135]: /fixture
                    - cell [ref=e136]: /case-089
                    - cell [ref=e137]
                    - cell [ref=e138]: E-TRADE
              - generic [ref=e141]:
                - paragraph [ref=e142]: "Rows per page:"
                - generic [ref=e143]:
                  - combobox [ref=e144] [cursor=pointer]: "20"
                  - textbox [aria-hidden]: "20"
                - paragraph [ref=e145]: 1–1 of 1
                - generic [ref=e146]:
                  - button [disabled]
                  - button [disabled]
            - dialog [ref=e149]:
              - heading [level=2] [ref=e150]:
                - generic [ref=e151]:
                  - generic [ref=e152]: "edit ID: 101"
                  - generic [ref=e153]:
                    - button [ref=e154] [cursor=pointer]: Maximize
                    - button [disabled]:
                      - generic: Close
              - generic [ref=e159]:
                - generic [ref=e161]:
                  - generic [ref=e162]: Aplication Category
                  - generic [ref=e163]:
                    - combobox [ref=e164]: category-a
                    - button [ref=e166] [cursor=pointer]
                - generic [ref=e169]:
                  - generic [ref=e170]: Tile Name
                  - textbox [ref=e172]:
                    - /placeholder: Type here
                    - text: STALE
                - generic [ref=e173]:
                  - generic [ref=e174]: Description
                  - textbox [ref=e176]:
                    - /placeholder: Type here
                    - text: Fixture tile
                - generic [ref=e178]:
                  - generic [ref=e179]: Image URL for Dark Theme
                  - generic [ref=e180]:
                    - combobox [ref=e181]: dark-a.png
                    - button [ref=e183] [cursor=pointer]
                - generic [ref=e187]:
                  - generic [ref=e188]: Image URL for Light Theme
                  - generic [ref=e189]:
                    - combobox [ref=e190]: light-a.png
                    - button [ref=e192] [cursor=pointer]
                - generic [ref=e196]:
                  - generic [ref=e197]: Container
                  - generic [ref=e198]:
                    - combobox [ref=e199]: container-a
                    - button [ref=e201] [cursor=pointer]
                - generic [ref=e204]:
                  - generic [ref=e205]: Module Path
                  - textbox [ref=e207]:
                    - /placeholder: Type here
                    - text: /fixture
                - generic [ref=e208]:
                  - generic [ref=e209]: Tile Path
                  - textbox [ref=e211]:
                    - /placeholder: Type here
                    - text: /case-089
                - generic [ref=e212]:
                  - generic [ref=e213]: Role Subject
                  - textbox [ref=e215]:
                    - /placeholder: Type here
                - generic [ref=e216]:
                  - generic [ref=e217]: Role Entities
                  - textbox [ref=e219]:
                    - /placeholder: Type here
                    - text: E-TRADE
                - generic [ref=e220]:
                  - generic [ref=e221]: Is Template?
                  - generic [ref=e222]:
                    - combobox [ref=e223] [cursor=pointer]: "false"
                    - textbox [aria-hidden]: "false"
                - generic [ref=e224]:
                  - generic [ref=e225]: Email Support
                  - textbox [ref=e227]:
                    - /placeholder: Type here
                    - text: support@example.test
                - generic [ref=e228]:
                  - generic [ref=e229]: Owner
                  - textbox [disabled] [ref=e231]:
                    - /placeholder: Type here
                    - text: FMO_ADMIN
                - generic [ref=e232]:
                  - generic [ref=e233]: Verified?
                  - textbox [disabled] [ref=e235]:
                    - /placeholder: Type here
                    - text: "false"
                - generic [ref=e236]:
                  - generic [ref=e237]: Created At
                  - textbox [disabled] [ref=e239]:
                    - /placeholder: Type here
                    - text: 2026-10-22T00:00:00.000+00:00
                - generic [ref=e240]:
                  - generic [ref=e241]: Created By
                  - textbox [disabled] [ref=e243]:
                    - /placeholder: Type here
                    - text: admin-a
                - generic [ref=e244]:
                  - generic [ref=e245]: Updated At
                  - textbox [disabled] [ref=e247]:
                    - /placeholder: Type here
                    - text: 2026-10-22T00:00:00.000+00:00
                - generic [ref=e248]:
                  - generic [ref=e249]: Updated By
                  - textbox [disabled] [ref=e251]:
                    - /placeholder: Type here
                    - text: admin-a
                - generic [ref=e252]:
                  - generic [ref=e253]: Record Id
                  - textbox [disabled] [ref=e255]:
                    - /placeholder: <<will be auto generated>>
                    - text: "101"
                - generic [ref=e256]:
                  - generic [ref=e257]: Aplication Category Record Id
                  - textbox [disabled] [ref=e259]:
                    - /placeholder: <<will be auto generated>>
                    - text: "101"
                - generic [ref=e260]:
                  - generic [ref=e261]: Container Record Id
                  - textbox [disabled] [ref=e263]:
                    - /placeholder: <<will be auto generated>>
                    - text: "201"
                - generic [ref=e264]:
                  - generic [ref=e265]: Order No
                  - spinbutton [ref=e267]: "7"
                - generic [ref=e268]:
                  - generic [ref=e269]: Filter Rule
                  - textbox [ref=e271]:
                    - /placeholder: Type here
                - generic [ref=e272]:
                  - generic [ref=e273]: Entry Name
                  - textbox [ref=e275]:
                    - /placeholder: Type here
                    - text: Global
              - generic [ref=e276]:
                - button [disabled]:
                  - progressbar
                  - text: Update
                - button [disabled]:
                  - progressbar
                  - text: Reset
                - button [disabled]:
                  - progressbar
                  - text: Close
              - button [ref=e277]
```

# Test source

```ts
  1   | import { expect, type Page } from '@playwright/test';
  2   | import { AdminApp, adminFields, type AdminKind } from './admin-app.js';
  3   | import { blockExternal, localPrefix, openLogin, workspace } from './local-app.js';
  4   | import type { AuditCapture, CanonicalStep } from './audit-fixture.js';
  5   | 
  6   | export const currentBff = 'http://127.0.0.1:8090/api/auth';
  7   | export const resourceFor = (kind: AdminKind) => kind === 'Category' ? 'category' : kind === 'Import Map' ? 'importmap' : 'tile';
  8   | export const keyFor = (kind: AdminKind) => kind === 'Category' ? 'applicationCategoryId' : kind === 'Import Map' ? 'importMapId' : 'applicationTileId';
  9   | const sqlTable = (kind: AdminKind) => kind === 'Category' ? 'application_category' : kind === 'Import Map' ? 'import_map' : 'application_tile';
  10  | const sqlKey = (kind: AdminKind) => keyFor(kind).replace(/[A-Z]/g, c => `_${c.toLowerCase()}`);
  11  | const quote = (value: unknown) => value === null ? 'NULL' : typeof value === 'number' || typeof value === 'boolean' ? String(value) : `'${String(value).replaceAll("'", "''")}'`;
  12  | export class BffAdminApp {
  13  |  readonly ui: AdminApp;
  14  |  readonly resource: string;
  15  |  readonly key: string;
  16  |  readonly requests: { resource: string; operation: string; body: any; status: number; response: any }[] = [];
  17  |  initialGrid: unknown;
  18  |  initialPersisted: any[] = [];
  19  |  expectedPersisted: any[] = [];
  20  |  lastSubmitted: Record<string, string> = {};
  21  |  access = '';
  22  |  entitlements = '';
  23  |  roles: string[] = [];
  24  |  baseline: Record<string,string> = {};
  25  |  initialCreateCount = 0;
  26  |  constructor(readonly page: Page, readonly kind: AdminKind, readonly id: string, readonly steps: readonly CanonicalStep[], readonly audit: AuditCapture) {
  27  |   this.ui = new AdminApp(page, kind, id); this.resource = resourceFor(kind); this.key = keyFor(kind);
  28  |  }
  29  |  async fixture(operation: string, body: unknown = {}): Promise<any> {
  30  |   const response = await this.page.request.post(`${currentBff}/local/fixture/${operation}`, { data: body });
  31  |   const text = await response.text(); expect(response.ok(), `Fixture ${operation}: ${text}`).toBe(true);
  32  |   return text ? JSON.parse(text) : {};
  33  |  }
  34  |  async sql(statements: string[]): Promise<any> { return this.fixture('sql', { statements }); }
  35  |  async snapshot(): Promise<any[]> {
  36  |   const result = await this.sql([`SELECT * FROM post_trade_portal_service.${sqlTable(this.kind)} ORDER BY ${sqlKey(this.kind)}`]);
  37  |   return result.results?.[0]?.rows ?? result[0]?.rows ?? result.rows ?? [];
  38  |  }
  39  |  async mutate(set: Record<string, unknown>, id = 101) {
  40  |   await this.sql([`UPDATE post_trade_portal_service.${sqlTable(this.kind)} SET ${Object.entries(set).map(([name,value])=>`${name}=${quote(value)}`).join(',')} WHERE ${sqlKey(this.kind)}=${id}`]);
  41  |   this.expectedPersisted=await this.snapshot();
  42  |  }
  43  |  async setup(): Promise<void> {
  44  |   const all = this.steps.map(step => step.text).join('\n');
  45  |   const subject = /uses subject "([^"]+)"/.exec(all)?.[1] ?? 'admin-a';
  46  |   const creating = all.includes('controlled creation clock');
  47  |   this.baseline = Object.fromEntries(this.steps.flatMap(step => {
  48  |    const match=/^the baseline fixture data defines "([^"]+)" as "(.*)"$/.exec(step.text);
  49  |    return match ? [[match[1],match[2]]] : [];
  50  |   }));
  51  |   const field = (name:string, fallback:string) => new RegExp(`baseline fixture data defines "${name}" as "([^"\\n]*)"`).exec(all)?.[1] ?? fallback;
  52  |   const common = { ems2Role:'FMO_ADMIN', active:false, createdAt:'2026-10-22T00:00:00Z', updatedAt:'2026-10-22T00:00:00Z', createdBy:'admin-a', updatedBy:all.includes('"ADMIN-A"')?'ADMIN-A':'admin-a', orderNo:7 };
  53  |   const category = { ...common, applicationCategoryId:101, label:this.kind==='Category'?field('Category Label','category-a'):'category-a', active:true };
  54  |   const map = { ...common, importMapId:this.kind==='Import Map'?(all.includes('grid has record "301"')?301:101):201, keyName:this.kind==='Import Map'?field('Module Name','container-a'):'container-a', path:field('Path','https://fixture.example/base.js'), active:true };
  55  |   if(this.kind==='Import Map' && creating)map.keyName=`existing-${this.id.toLowerCase()}`;
  56  |   const tile = { ...common, applicationTileId:all.includes('"301"') || this.id==='BFF-ADM-097'?301:101, title:field('Tile Name','tile-a'), subtitle:'Fixture tile', module:field('Module Path','/fixture'), tile:field('Tile Path','/tile-a'), ems2Entities:field('Role Entities','E-TRADE'), ems2Subject:'', entryName:'Global', filterRule:null, template:false, imageLightTheme:'light-a.png', imageDarkTheme:'dark-a.png', emailSupport:'support@example.test', applicationCategory:{applicationCategoryId:101}, importMap:{importMapId:map.importMapId} };
  57  |   if(this.kind==='Category') category.active=false;
  58  |   if(this.kind==='Import Map') map.active=false;
  59  |   if(all.includes('originally loaded')) { if(this.kind==='Category')category.label='OLD';else if(this.kind==='Import Map')map.keyName='OLD';else tile.title='OLD'; }
  60  |   if(all.includes('Category 101 is inactive')) category.active=false;
  61  |   if(all.includes('Import Map 201 is inactive')) map.active=false;
  62  |   const categories:any[]=[category], importMaps:any[]=[map], tiles:any[]=this.kind==='Tile'&&!creating?[tile]:[];
  63  |   let staleRow:any=null;
  64  |   if(all.includes('controlled stale grid exposes')) {
  65  |    staleRow={...(this.kind==='Category'?category:this.kind==='Import Map'?map:tile),[this.key]:901,ems2Role:'OTHER_ADMIN'};
  66  |    if(this.kind==='Category'){staleRow.label='PROTECTED-FOREIGN-CATEGORY';categories.push(staleRow);}
  67  |    else if(this.kind==='Import Map'){staleRow.keyName='PROTECTED-FOREIGN-MAP';importMaps.push(staleRow);}
  68  |    else {staleRow.title='PROTECTED-FOREIGN-TILE';tiles.push(staleRow);}
  69  |   }
  70  |   if(this.kind==='Category' && /existing Category record already|Category record "102" already/.test(all))categories.push({...common,applicationCategoryId:102,label:'shared-a'});
  71  |   if(this.kind==='Import Map' && /existing Import Map record already|Import Map record "102" already/.test(all))importMaps.push({...common,importMapId:102,keyName:all.includes('equal to "react"')?'react':'shared-a',path:'https://fixture.example/initial.js',active:true});
  72  |   if(all.includes('reference "102"'))categories.push({...common,applicationCategoryId:102,label:'foreign-category',ems2Role:'OTHER_ADMIN'});
  73  |   if(all.includes('reference "202"'))importMaps.push({...common,importMapId:202,keyName:'foreign-map',path:'https://fixture.example/foreign.js',ems2Role:'OTHER_ADMIN'});
  74  |   categories.push({...common,applicationCategoryId:9900,label:'Administration bootstrap',active:true});
  75  |   importMaps.push({...common,importMapId:9901,keyName:'base',path:'http://localhost:8122/base.js',active:true});
  76  |   tiles.push({...tile,applicationTileId:9902,title:this.kind,module:this.resource,tile:'',active:true,template:true,applicationCategory:{applicationCategoryId:9900},importMap:{importMapId:9901}});
  77  |   await this.fixture('reset'); await this.fixture('seed',{categories,importMaps,tiles,
  78  |    ...(staleRow?{[this.kind==='Category'?'categoryAudits':this.kind==='Import Map'?'importMapAudits':'tileAudits']:[{...staleRow,[this.kind==='Category'?'applicationCategoryAuditId':this.kind==='Import Map'?'importMapAuditId':'applicationTileAuditId']:5001,transactionMode:'maker'}]}:{})});
  79  |   await blockExternal(this.page);
  80  |   await this.page.route('**/api/auth/**',async route=>{
  81  |    const url=new URL(route.request().url());
  82  |    let body:any=route.request().method()==='POST'?route.request().postDataJSON():null;
  83  |    const parts=url.pathname.split('/'); const operation=parts.at(-1)!; const resource=parts.at(-2)!;
  84  |    const admin=url.pathname.includes('/v1/fmo/admin/');
  85  |    if(admin && ['create','update'].includes(operation)){
  86  |     if(all.includes('"applicationCategory.applicationCategoryId" as 102'))body.applicationCategory={applicationCategoryId:102};
  87  |     if(all.includes('"importMap.importMapId" as 202'))body.importMap={importMapId:202};
  88  |     if(all.includes('"importMap" as null'))body.importMap=null;
> 89  |     for(const [label,value] of Object.entries(this.lastSubmitted))expect(body[adminFields[label]],`Committed UI field ${label}`).toBe(value);
      |                                                                                                                                  ^ Error: Committed UI field Filter Rule
  90  |     if(all.includes('"applicationCategory.applicationCategoryId" as 102'))expect(body.applicationCategory.applicationCategoryId).toBe(102);
  91  |     if(all.includes('"importMap.importMapId" as 202'))expect(body.importMap.importMapId).toBe(202);
  92  |     if(all.includes('"importMap" as null'))expect(body.importMap).toBeNull();
  93  |     if(this.kind==='Tile'&&all.includes('clicks the option labeled "container-a"'))expect(body.importMap.importMapId).toBe(201);
  94  |    }
  95  |    const response=await route.fetch({url:`${currentBff}${url.pathname.replace('/api/auth','')}${url.search}`, ...(body?{postData:body}:{})});
  96  |    let payload:any;try{payload=await response.json();}catch{payload={raw:await response.text()};}
  97  |    if(staleRow && admin && operation==='data' && resource===this.resource) {
  98  |     payload.data=[...(payload.data??[]),staleRow];
  99  |     await route.fulfill({response,json:payload});
  100 |     this.requests.push({resource,operation,body:{entitlementsToken:'[SIGNED LOCAL TEST TOKEN]'},status:response.status(),response:payload});
  101 |     return;
  102 |    }
  103 |    if(operation==='login') {
  104 |     this.access=response.headers()['single-ui-authorization']??'';this.entitlements=payload.entitlementsToken??'';
  105 |     const accessClaims=JSON.parse(Buffer.from(this.access.replace(/^Bearer /,'').split('.')[1],'base64url').toString());
  106 |     const entitlementClaims=JSON.parse(Buffer.from(this.entitlements.split('.')[1],'base64url').toString());
  107 |     const roleMap=JSON.parse(entitlementClaims.entitlements);
  108 |     this.roles=Object.keys(roleMap).filter(key=>key.startsWith('FMO PORTAL ADMIN:')).map(key=>key.split(':')[1]);
  109 |     expect(accessClaims.sub).toBe(subject);expect(JSON.parse(payload.userInfo).sub).toBe(subject);
  110 |     expect(this.roles).toEqual([subject==='admin-s'?'SUPER_USER':'FMO_ADMIN']);
  111 |     await this.audit.record('actual-identity-projection',{subject:accessClaims.sub,issuer:accessClaims.iss,adminEntity:'FMO PORTAL ADMIN',roles:this.roles,signatureLimit:'Decoded projections do not independently verify signatures. Actual BFF calls retain authorization outcomes.'});
  112 |    }
  113 |    if(admin)this.requests.push({resource,operation,body:{...body,entitlementsToken:body?.entitlementsToken?'[SIGNED LOCAL TEST TOKEN]':undefined},status:response.status(),response:payload});
  114 |    await route.fulfill({response});
  115 |   });
  116 |   const initial={...workspace(this.kind),containers:[{id:'CURRENT-BFF-ADMIN',container:'@fm/base',module:`/${this.resource}`,tile:'/',title:this.kind,emailSupport:'support@example.test',panelId:'',tabId:'',parameters:{}}]};
  117 |   await this.page.addInitScript(value=>{if(!localStorage.getItem('SET_WORKSPACES'))localStorage.setItem('SET_WORKSPACES',JSON.stringify([value]));},initial);
  118 |   const login=await openLogin(this.page);await login.fillUsername(subject);await login.fillPassword('FixturePass1!');await login.clickSignInButton();await this.ui.portal.expectVisible();
  119 |   await expect(this.ui.grid).toBeVisible();if(this.kind==='Tile'&&subject!=='admin-s')await this.ui.selectCategory('category-a');
  120 |   await this.audit.record('baseline-inputs',{values:this.baseline,purpose:'Input defaults are separate from existing persisted records. Creation fixtures avoid accidental unique-key collisions.',storedFilterRule:tile.filterRule});
  121 |   await this.audit.record('bff-boundary',{origin:currentBff,scope:'Actual current controllers, services, signed tokens, JPA and disposable PostgreSQL. Controlled OUD/EMS2/bootstrap.',subject,role:subject==='admin-s'?'SUPER_USER':'FMO_ADMIN'});
  122 |  }
  123 |  async gridSnapshot(): Promise<unknown> {await this.ui.grid.locator('.MuiDataGrid-virtualScroller').evaluate(node=>{node.scrollLeft=0;});await expect(this.ui.grid.locator('[role="columnheader"][data-field="actions"]')).toBeVisible();await this.page.waitForTimeout(50);return this.ui.grid.locator('[data-id]').evaluateAll(rows=>rows.map(row=>({id:row.getAttribute('data-id'),values:Array.from(row.querySelectorAll('[data-field]')).filter(cell=>cell.getAttribute('data-field')!=='actions').map(cell=>[cell.getAttribute('data-field'),cell.textContent])})));}
  124 |  async remember(): Promise<void>{this.initialGrid=await this.gridSnapshot();this.initialPersisted=await this.snapshot();this.expectedPersisted=this.initialPersisted;await this.audit.record('initial-persisted-records',this.initialPersisted);}
  125 |  async fill(name:string,value:string):Promise<void>{this.lastSubmitted[name]=value;await this.ui.field(name).fill(value);await expect(this.ui.field(name)).toHaveValue(value);await this.page.waitForTimeout(350);}
  126 |  async clickFooter(name:string):Promise<void>{const count=this.requests.filter(request=>['create','update'].includes(request.operation)).length;await this.ui.footerButton(name).click();if(['Create','Update','Verified','Deactivate'].includes(name)){await expect.poll(()=>this.requests.filter(request=>['create','update'].includes(request.operation)).length).toBeGreaterThan(count);await this.audit.record('ui-origin-bff-requests',this.requests);await this.audit.record('persisted-after-submit',await this.snapshot());}}
  127 |  lastMutation(){return [...this.requests].reverse().find(x=>['create','update'].includes(x.operation));}
  128 |  async directUpdate(subject:string,mode:string,changes:Record<string,unknown>={},targetId=101):Promise<void>{
  129 |   const login=await this.page.request.post(`${currentBff}/v2/sso/login`,{data:{username:subject,password:'FixturePass1!',device:'LOCAL_UI_AUDIT'}});expect(login.ok()).toBe(true);const payload=await login.json();
  130 |   const rows:any[]=await this.snapshot(); const row=rows.find(row=>Number(row[sqlKey(this.kind)])===targetId)!;
  131 |   const base:any=Object.fromEntries(Object.entries(row).map(([name,value])=>[name.replace(/_([a-z])/g,(_,letter)=>letter.toUpperCase()),value]));
  132 |   base.active=base.isActive;delete base.isActive;
  133 |   if(this.kind==='Tile'){base.importMap={importMapId:base.importMapId};base.applicationCategory={applicationCategoryId:base.applicationCategoryId};}
  134 |   const response=await this.page.request.post(`${currentBff}/v1/fmo/admin/${this.resource}/update`,{headers:{'single-ui-authorization':login.headers()['single-ui-authorization']},data:{...base,...changes,mode,entitlementsToken:payload.entitlementsToken}});
  135 |   await this.audit.record(`concurrent-${subject}-${mode}`,{status:response.status(),response:await response.json()});expect(response.ok()).toBe(true);
  136 |  }
  137 |  async assertUnchanged():Promise<void>{expect(await this.snapshot()).toEqual(this.expectedPersisted);expect(await this.gridSnapshot()).toEqual(this.initialGrid);}
  138 |  async errorAlert(exact?:string):Promise<void>{const alert=this.page.locator('.MuiAlert-root').filter({has:this.page.locator('.MuiAlert-message')});await expect(alert).toBeVisible();await expect(alert).toHaveClass(/MuiAlert-standardError|MuiAlert-filledError|MuiAlert-outlinedError/);if(exact)await expect(alert.locator('.MuiAlert-message')).toHaveText(exact);else {const mutation=[...this.requests].reverse().find(request=>['create','update','audit'].includes(request.operation));expect(mutation?.status).toBeGreaterThanOrEqual(400);await expect(alert.locator('.MuiAlert-message')).not.toHaveText('');await this.audit.record('undefined-message-contract',{canonical:'Agreed message is unavailable. Only real error response and visible nonempty error are characterized.',actual:await alert.innerText()});}}
  139 |  async cell(name:string,id:string){return this.ui.reveal(adminFields[name]??name,id);}
  140 | }
  141 | 
```