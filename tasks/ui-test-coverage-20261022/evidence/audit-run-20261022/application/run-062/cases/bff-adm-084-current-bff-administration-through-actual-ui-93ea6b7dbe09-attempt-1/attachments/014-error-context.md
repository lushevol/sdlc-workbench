# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: bff-admin.spec.ts >> BFF-ADM-084 current BFF administration through actual UI
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

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 06:06 UTC
  - checkbox "Time Switch" [checked]
- button "User Profiles": A
- button "Share Feedback"
- main:
  - tablist "workspaces":
    - tab "Category" [selected]:
      - region "Category":
        - textbox "Workspace Name": Category
        - button "refresh"
    - button "Add Workspace"
  - tabpanel:
    - button "Create New Category"
    - grid:
      - button "Export"
      - rowgroup:
        - row "Actions Category Label Owner Verified? Updated At Updated By Record Id Order No":
          - columnheader "Actions"
          - columnheader "Category Label"
          - columnheader "Owner"
          - columnheader "Verified?"
          - columnheader "Updated At"
          - columnheader "Updated By"
          - columnheader "Record Id"
          - columnheader "Order No"
      - rowgroup:
        - row "NEW FMO_ADMIN Oct 22, 2026, 6:06:47 AM admin-b 101 7":
          - cell:
            - menu:
              - menuitem "Edit"
              - menuitem "Verify" [disabled]
              - menuitem "Deactivate"
              - menuitem "Audit"
          - cell "NEW"
          - cell "FMO_ADMIN"
          - cell
          - cell "Oct 22, 2026, 6:06:47 AM"
          - cell "admin-b"
          - cell "101"
          - cell "7"
        - row "Administration bootstrap FMO_ADMIN Oct 22, 2026, 12:00:00 AM admin-a 9900 7":
          - cell:
            - menu:
              - menuitem "Edit"
              - menuitem "Verify" [disabled]
              - menuitem "Deactivate"
              - menuitem "Audit"
          - cell "Administration bootstrap"
          - cell "FMO_ADMIN"
          - cell
          - cell "Oct 22, 2026, 12:00:00 AM"
          - cell "admin-a"
          - cell "9900"
          - cell "7"
      - paragraph: "Rows per page:"
      - 'combobox "Rows per page: 20"': "20"
      - paragraph: 1–2 of 2
      - button "Go to previous page" [disabled]
      - button "Go to next page" [disabled]
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