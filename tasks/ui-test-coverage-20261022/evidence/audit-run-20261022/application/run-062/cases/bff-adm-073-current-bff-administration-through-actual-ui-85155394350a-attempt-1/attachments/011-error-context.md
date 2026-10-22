# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: bff-admin.spec.ts >> BFF-ADM-073 current BFF administration through actual UI
- Location: e2e/audit-specs/bff-admin.spec.ts:10:2

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('.MuiAlert-root').filter({ has: locator('.MuiAlert-message') })
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" locator('.MuiAlert-root').filter({ has: locator('.MuiAlert-message') }) with timeout 5000ms
  - waiting for locator('.MuiAlert-root').filter({ has: locator('.MuiAlert-message') })

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
      - generic [ref=e27]: 06:04 UTC
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
                  - cell [ref=e130]: tile-a
                  - cell [ref=e131]: Fixture tile
                  - cell [ref=e132]: dark-a.png
                  - cell [ref=e133]: light-a.png
                  - cell [ref=e134]: container-a
                  - cell [ref=e135]: /fixture
                  - cell [ref=e136]: /tile-a
                  - cell [ref=e137]
                  - cell [ref=e138]: E-TRADE
                - row [ref=e139]:
                  - cell [ref=e140]:
                    - menu [ref=e141]:
                      - menuitem [ref=e142] [cursor=pointer]
                      - menuitem [ref=e145] [cursor=pointer]
                      - menuitem [disabled]
                      - menuitem [ref=e148] [cursor=pointer]
                  - cell [ref=e151]: PROTECTED-FOREIGN-TILE
                  - cell [ref=e152]: Fixture tile
                  - cell [ref=e153]: dark-a.png
                  - cell [ref=e154]: light-a.png
                  - cell [ref=e155]
                  - cell [ref=e156]: /fixture
                  - cell [ref=e157]: /tile-a
                  - cell [ref=e158]
                  - cell [ref=e159]: E-TRADE
            - generic [ref=e162]:
              - paragraph [ref=e163]: "Rows per page:"
              - generic [ref=e164]:
                - combobox [ref=e165] [cursor=pointer]: "20"
                - textbox [aria-hidden]: "20"
              - paragraph [ref=e166]: 1–2 of 2
              - generic [ref=e167]:
                - button [disabled]
                - button [disabled]
          - dialog [ref=e170]:
            - heading [level=2] [ref=e171]:
              - generic [ref=e172]:
                - generic [ref=e173]: Audit
                - generic [ref=e174]:
                  - button [ref=e175] [cursor=pointer]: Maximize
                  - button [ref=e178] [cursor=pointer]:
                    - generic [ref=e179]: Close
            - grid [ref=e183]:
              - generic [ref=e184]:
                - rowgroup [ref=e185]:
                  - row [ref=e186]:
                    - columnheader [ref=e187] [cursor=pointer]:
                      - generic [ref=e188]: Audit ID
                    - columnheader [ref=e190] [cursor=pointer]:
                      - generic [ref=e191]: Transaction Mode
                    - columnheader [ref=e193] [cursor=pointer]:
                      - generic [ref=e194]: Tile ID
                    - columnheader [ref=e196] [cursor=pointer]:
                      - generic [ref=e197]: Aplication Category
                    - columnheader [ref=e199] [cursor=pointer]:
                      - generic [ref=e200]: Tile Name
                    - columnheader [ref=e202] [cursor=pointer]:
                      - generic [ref=e203]: Description
                    - columnheader [ref=e205] [cursor=pointer]:
                      - generic [ref=e206]: Image URL for Dark Theme
                    - columnheader [ref=e208] [cursor=pointer]:
                      - generic [ref=e209]: Image URL for Light Theme
                    - columnheader [ref=e211] [cursor=pointer]:
                      - generic [ref=e212]: Container
                    - columnheader [ref=e214] [cursor=pointer]:
                      - generic [ref=e215]: Module Path
                    - columnheader [ref=e217] [cursor=pointer]:
                      - generic [ref=e218]: Tile Path
                - rowgroup [ref=e220]:
                  - row [ref=e221]:
                    - cell [ref=e222]: "1000"
                    - cell [ref=e223]: maker
                    - cell [ref=e224]: "901"
                    - cell [ref=e225]: category-a
                    - cell [ref=e226]: PROTECTED-FOREIGN-TILE
                    - cell [ref=e227]: Fixture tile
                    - cell [ref=e228]: dark-a.png
                    - cell [ref=e229]: light-a.png
                    - cell [ref=e230]: container-a
                    - cell [ref=e231]: /fixture
                    - cell [ref=e232]: /tile-a
              - generic [ref=e235]:
                - paragraph [ref=e236]: "Rows per page:"
                - generic [ref=e237]:
                  - combobox [ref=e238] [cursor=pointer]: "20"
                  - textbox [aria-hidden]: "20"
                - paragraph [ref=e239]: 1–1 of 1
                - generic [ref=e240]:
                  - button [disabled]
                  - button [disabled]
            - button [ref=e241]
```

# Test source

```ts
  16  |  readonly requests: { resource: string; operation: string; body: any; status: number; response: any }[] = [];
  17  |  initialGrid: unknown;
  18  |  initialPersisted: any[] = [];
  19  |  expectedPersisted: any[] = [];
  20  |  lastSubmitted: Record<string, string> = {};
  21  |  access = '';
  22  |  entitlements = '';
  23  |  initialCreateCount = 0;
  24  |  constructor(readonly page: Page, readonly kind: AdminKind, readonly id: string, readonly steps: readonly CanonicalStep[], readonly audit: AuditCapture) {
  25  |   this.ui = new AdminApp(page, kind, id); this.resource = resourceFor(kind); this.key = keyFor(kind);
  26  |  }
  27  |  async fixture(operation: string, body: unknown = {}): Promise<any> {
  28  |   const response = await this.page.request.post(`${currentBff}/local/fixture/${operation}`, { data: body });
  29  |   const text = await response.text(); expect(response.ok(), `Fixture ${operation}: ${text}`).toBe(true);
  30  |   return text ? JSON.parse(text) : {};
  31  |  }
  32  |  async sql(statements: string[]): Promise<any> { return this.fixture('sql', { statements }); }
  33  |  async snapshot(): Promise<any[]> {
  34  |   const result = await this.sql([`SELECT * FROM post_trade_portal_service.${sqlTable(this.kind)} ORDER BY ${sqlKey(this.kind)}`]);
  35  |   return result.results?.[0]?.rows ?? result[0]?.rows ?? result.rows ?? [];
  36  |  }
  37  |  async mutate(set: Record<string, unknown>, id = 101) {
  38  |   await this.sql([`UPDATE post_trade_portal_service.${sqlTable(this.kind)} SET ${Object.entries(set).map(([name,value])=>`${name}=${quote(value)}`).join(',')} WHERE ${sqlKey(this.kind)}=${id}`]);
  39  |   this.expectedPersisted=await this.snapshot();
  40  |  }
  41  |  async setup(): Promise<void> {
  42  |   const all = this.steps.map(step => step.text).join('\n');
  43  |   const subject = /uses subject "([^"]+)"/.exec(all)?.[1] ?? 'admin-a';
  44  |   const field = (name:string, fallback:string) => new RegExp(`baseline fixture data defines "${name}" as "([^"\\n]*)"`).exec(all)?.[1] ?? fallback;
  45  |   const common = { ems2Role:'FMO_ADMIN', active:false, createdAt:'2026-10-22T00:00:00Z', updatedAt:'2026-10-22T00:00:00Z', createdBy:'admin-a', updatedBy:all.includes('"ADMIN-A"')?'ADMIN-A':'admin-a', orderNo:7 };
  46  |   const category = { ...common, applicationCategoryId:101, label:this.kind==='Category'?field('Category Label','category-a'):'category-a', active:true };
  47  |   const map = { ...common, importMapId:this.kind==='Import Map'?(all.includes('grid has record "301"')?301:101):201, keyName:this.kind==='Import Map'?field('Module Name','container-a'):'container-a', path:field('Path','https://fixture.example/base.js'), active:true };
  48  |   const tile = { ...common, applicationTileId:all.includes('"301"') || this.id==='BFF-ADM-097'?301:101, title:field('Tile Name','tile-a'), subtitle:'Fixture tile', module:field('Module Path','/fixture'), tile:field('Tile Path','/tile-a'), ems2Entities:field('Role Entities','E-TRADE'), ems2Subject:'', entryName:'Global', filterRule:null, template:false, imageLightTheme:'light-a.png', imageDarkTheme:'dark-a.png', emailSupport:'support@example.test', applicationCategory:{applicationCategoryId:101}, importMap:{importMapId:map.importMapId} };
  49  |   if(this.kind==='Category') category.active=false;
  50  |   if(this.kind==='Import Map') map.active=false;
  51  |   if(all.includes('originally loaded')) { if(this.kind==='Category')category.label='OLD';else if(this.kind==='Import Map')map.keyName='OLD';else tile.title='OLD'; }
  52  |   if(all.includes('Category 101 is inactive')) category.active=false;
  53  |   if(all.includes('Import Map 201 is inactive')) map.active=false;
  54  |   const categories:any[]=[category], importMaps:any[]=[map], tiles:any[]=this.kind==='Tile'?[tile]:[];
  55  |   let staleRow:any=null;
  56  |   if(all.includes('controlled stale grid exposes')) {
  57  |    staleRow={...(this.kind==='Category'?category:this.kind==='Import Map'?map:tile),[this.key]:901,ems2Role:'OTHER_ADMIN'};
  58  |    if(this.kind==='Category'){staleRow.label='PROTECTED-FOREIGN-CATEGORY';categories.push(staleRow);}
  59  |    else if(this.kind==='Import Map'){staleRow.keyName='PROTECTED-FOREIGN-MAP';importMaps.push(staleRow);}
  60  |    else {staleRow.title='PROTECTED-FOREIGN-TILE';tiles.push(staleRow);}
  61  |   }
  62  |   if(this.kind==='Category' && /existing Category record already|Category record "102" already/.test(all))categories.push({...common,applicationCategoryId:102,label:'shared-a'});
  63  |   if(this.kind==='Import Map' && /existing Import Map record already|Import Map record "102" already/.test(all))importMaps.push({...common,importMapId:102,keyName:all.includes('equal to "react"')?'react':'shared-a',path:'https://fixture.example/initial.js',active:true});
  64  |   if(all.includes('reference "102"'))categories.push({...common,applicationCategoryId:102,label:'foreign-category',ems2Role:'OTHER_ADMIN'});
  65  |   if(all.includes('reference "202"'))importMaps.push({...common,importMapId:202,keyName:'foreign-map',path:'https://fixture.example/foreign.js',ems2Role:'OTHER_ADMIN'});
  66  |   categories.push({...common,applicationCategoryId:9900,label:'Administration bootstrap',active:true});
  67  |   importMaps.push({...common,importMapId:9901,keyName:'base',path:'http://localhost:8122/MicroWebUI_base.js',active:true});
  68  |   tiles.push({...tile,applicationTileId:9902,title:this.kind,module:this.resource,tile:'',active:true,template:true,applicationCategory:{applicationCategoryId:9900},importMap:{importMapId:9901}});
  69  |   await this.fixture('reset'); await this.fixture('seed',{categories,importMaps,tiles,
  70  |    ...(staleRow?{[this.kind==='Category'?'categoryAudits':this.kind==='Import Map'?'importMapAudits':'tileAudits']:[{...staleRow,[this.kind==='Category'?'applicationCategoryAuditId':this.kind==='Import Map'?'importMapAuditId':'applicationTileAuditId']:5001,transactionMode:'maker'}]}:{})});
  71  |   await blockExternal(this.page);
  72  |   await this.page.route('**/api/auth/**',async route=>{
  73  |    const url=new URL(route.request().url());
  74  |    let body:any=route.request().method()==='POST'?route.request().postDataJSON():null;
  75  |    const parts=url.pathname.split('/'); const operation=parts.at(-1)!; const resource=parts.at(-2)!;
  76  |    const admin=url.pathname.includes('/v1/fmo/admin/');
  77  |    if(admin && ['create','update'].includes(operation)){
  78  |     if(all.includes('"applicationCategory.applicationCategoryId" as 102'))body.applicationCategory={applicationCategoryId:102};
  79  |     if(all.includes('"importMap.importMapId" as 202'))body.importMap={importMapId:202};
  80  |     if(all.includes('"importMap" as null'))body.importMap=null;
  81  |    }
  82  |    const response=await route.fetch({url:`${currentBff}${url.pathname.replace('/api/auth','')}${url.search}`, ...(body?{postData:body}:{})});
  83  |    let payload:any;try{payload=await response.json();}catch{payload={raw:await response.text()};}
  84  |    if(staleRow && admin && operation==='data' && resource===this.resource) {
  85  |     payload.data=[...(payload.data??[]),staleRow];
  86  |     await route.fulfill({response,json:payload});
  87  |     this.requests.push({resource,operation,body:{entitlementsToken:'[SIGNED LOCAL TEST TOKEN]'},status:response.status(),response:payload});
  88  |     return;
  89  |    }
  90  |    if(operation==='login') {this.access=response.headers()['single-ui-authorization']??'';this.entitlements=payload.entitlementsToken??'';}
  91  |    if(admin)this.requests.push({resource,operation,body:{...body,entitlementsToken:body?.entitlementsToken?'[SIGNED LOCAL TEST TOKEN]':undefined},status:response.status(),response:payload});
  92  |    await route.fulfill({response});
  93  |   });
  94  |   const initial={...workspace(this.kind),containers:[{id:'CURRENT-BFF-ADMIN',container:'@fm/base',module:`/${this.resource}`,tile:'/',title:this.kind,emailSupport:'support@example.test',panelId:'',tabId:'',parameters:{}}]};
  95  |   await this.page.addInitScript(value=>{if(!localStorage.getItem('SET_WORKSPACES'))localStorage.setItem('SET_WORKSPACES',JSON.stringify([value]));},initial);
  96  |   const login=await openLogin(this.page);await login.fillUsername(subject);await login.fillPassword('FixturePass1!');await login.clickSignInButton();await this.ui.portal.expectVisible();
  97  |   await expect(this.ui.grid).toBeVisible();if(this.kind==='Tile')await this.ui.selectCategory('category-a');
  98  |   await expect(this.ui.row(String(this.kind==='Tile'?tile.applicationTileId:this.kind==='Import Map'?map.importMapId:101))).toBeVisible();
  99  |   await this.audit.record('bff-boundary',{origin:currentBff,scope:'Actual current controllers, services, signed tokens, JPA and disposable PostgreSQL. Controlled OUD/EMS2/bootstrap.',subject,role:subject==='admin-s'?'SUPER_USER':'FMO_ADMIN'});
  100 |  }
  101 |  async gridSnapshot(): Promise<unknown> {await this.ui.grid.locator('.MuiDataGrid-virtualScroller').evaluate(node=>{node.scrollLeft=0;});await expect(this.ui.grid.locator('[role="columnheader"][data-field="actions"]')).toBeVisible();await this.page.waitForTimeout(50);return this.ui.grid.locator('[data-id]').evaluateAll(rows=>rows.map(row=>({id:row.getAttribute('data-id'),values:Array.from(row.querySelectorAll('[data-field]')).filter(cell=>cell.getAttribute('data-field')!=='actions').map(cell=>[cell.getAttribute('data-field'),cell.textContent])})));}
  102 |  async remember(): Promise<void>{this.initialGrid=await this.gridSnapshot();this.initialPersisted=await this.snapshot();this.expectedPersisted=this.initialPersisted;await this.audit.record('initial-persisted-records',this.initialPersisted);}
  103 |  async fill(name:string,value:string):Promise<void>{this.lastSubmitted[name]=value;await this.ui.field(name).fill(value);await this.page.waitForTimeout(300);}
  104 |  async clickFooter(name:string):Promise<void>{const count=this.requests.filter(request=>['create','update'].includes(request.operation)).length;await this.ui.footerButton(name).click();if(['Create','Update','Verified','Deactivate'].includes(name)){await expect.poll(()=>this.requests.filter(request=>['create','update'].includes(request.operation)).length).toBeGreaterThan(count);await this.audit.record('ui-origin-bff-requests',this.requests);await this.audit.record('persisted-after-submit',await this.snapshot());}}
  105 |  lastMutation(){return [...this.requests].reverse().find(x=>['create','update'].includes(x.operation));}
  106 |  async directUpdate(subject:string,mode:string,changes:Record<string,unknown>={},targetId=101):Promise<void>{
  107 |   const login=await this.page.request.post(`${currentBff}/v2/sso/login`,{data:{username:subject,password:'FixturePass1!',device:'LOCAL_UI_AUDIT'}});expect(login.ok()).toBe(true);const payload=await login.json();
  108 |   const rows:any[]=await this.snapshot(); const row=rows.find(row=>Number(row[sqlKey(this.kind)])===targetId)!;
  109 |   const base:any=Object.fromEntries(Object.entries(row).map(([name,value])=>[name.replace(/_([a-z])/g,(_,letter)=>letter.toUpperCase()),value]));
  110 |   base.active=base.isActive;delete base.isActive;
  111 |   if(this.kind==='Tile'){base.importMap={importMapId:base.importMapId};base.applicationCategory={applicationCategoryId:base.applicationCategoryId};}
  112 |   const response=await this.page.request.post(`${currentBff}/v1/fmo/admin/${this.resource}/update`,{headers:{'single-ui-authorization':login.headers()['single-ui-authorization']},data:{...base,...changes,mode,entitlementsToken:payload.entitlementsToken}});
  113 |   await this.audit.record(`concurrent-${subject}-${mode}`,{status:response.status(),response:await response.json()});expect(response.ok()).toBe(true);
  114 |  }
  115 |  async assertUnchanged():Promise<void>{expect(await this.snapshot()).toEqual(this.expectedPersisted);expect(await this.gridSnapshot()).toEqual(this.initialGrid);}
> 116 |  async errorAlert(exact?:string):Promise<void>{const alert=this.page.locator('.MuiAlert-root').filter({has:this.page.locator('.MuiAlert-message')});await expect(alert).toBeVisible();await expect(alert).toHaveClass(/MuiAlert-standardError|MuiAlert-filledError|MuiAlert-outlinedError/);if(exact)await expect(alert.locator('.MuiAlert-message')).toHaveText(exact);else {const mutation=[...this.requests].reverse().find(request=>['create','update','audit'].includes(request.operation));expect(mutation?.status).toBeGreaterThanOrEqual(400);await expect(alert.locator('.MuiAlert-message')).not.toHaveText('');await this.audit.record('undefined-message-contract',{canonical:'Agreed message is unavailable. Only real error response and visible nonempty error are characterized.',actual:await alert.innerText()});}}
      |                                                                                                                                                                         ^ Error: expect(locator).toBeVisible() failed
  117 |  async cell(name:string,id:string){return this.ui.reveal(adminFields[name]??name,id);}
  118 | }
  119 | 
```