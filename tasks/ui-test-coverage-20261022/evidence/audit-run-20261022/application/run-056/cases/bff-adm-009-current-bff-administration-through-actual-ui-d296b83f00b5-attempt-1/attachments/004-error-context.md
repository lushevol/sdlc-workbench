# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: bff-admin.spec.ts >> BFF-ADM-009 current BFF administration through actual UI
- Location: e2e/audit-specs/bff-admin.spec.ts:10:2

# Error details

```
Error: Fixture seed: {"timestamp":"2026-10-22T05:41:19.497+00:00","status":500,"error":"Internal Server Error","path":"/api/auth/local/fixture/seed"}

expect(received).toBe(expected) // Object.is equality

Expected: true
Received: false
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
  19  |  lastSubmitted: Record<string, string> = {};
  20  |  access = '';
  21  |  entitlements = '';
  22  |  initialCreateCount = 0;
  23  |  constructor(readonly page: Page, readonly kind: AdminKind, readonly id: string, readonly steps: readonly CanonicalStep[], readonly audit: AuditCapture) {
  24  |   this.ui = new AdminApp(page, kind, id); this.resource = resourceFor(kind); this.key = keyFor(kind);
  25  |  }
  26  |  async fixture(operation: string, body: unknown = {}): Promise<any> {
  27  |   const response = await this.page.request.post(`${currentBff}/local/fixture/${operation}`, { data: body });
> 28  |   const text = await response.text(); expect(response.ok(), `Fixture ${operation}: ${text}`).toBe(true);
      |                                                                                              ^ Error: Fixture seed: {"timestamp":"2026-10-22T05:41:19.497+00:00","status":500,"error":"Internal Server Error","path":"/api/auth/local/fixture/seed"}
  29  |   return text ? JSON.parse(text) : {};
  30  |  }
  31  |  async sql(statements: string[]): Promise<any> { return this.fixture('sql', { statements }); }
  32  |  async snapshot(): Promise<any[]> {
  33  |   const result = await this.sql([`SELECT * FROM post_trade_portal_service.${sqlTable(this.kind)} ORDER BY ${sqlKey(this.kind)}`]);
  34  |   return result.results?.[0]?.rows ?? result[0]?.rows ?? result.rows ?? [];
  35  |  }
  36  |  async mutate(set: Record<string, unknown>, id = 101) {
  37  |   await this.sql([`UPDATE post_trade_portal_service.${sqlTable(this.kind)} SET ${Object.entries(set).map(([name,value])=>`${name}=${quote(value)}`).join(',')} WHERE ${sqlKey(this.kind)}=${id}`]);
  38  |  }
  39  |  async setup(): Promise<void> {
  40  |   const all = this.steps.map(step => step.text).join('\n');
  41  |   const subject = /uses subject "([^"]+)"/.exec(all)?.[1] ?? 'admin-a';
  42  |   const field = (name:string, fallback:string) => new RegExp(`baseline fixture data defines "${name}" as "([^"\\n]*)"`).exec(all)?.[1] ?? fallback;
  43  |   const common = { ems2Role:'FMO_ADMIN', active:false, createdAt:'2026-10-22T00:00:00Z', updatedAt:'2026-10-22T00:00:00Z', createdBy:'admin-a', updatedBy:all.includes('"ADMIN-A"')?'ADMIN-A':'admin-a', orderNo:7 };
  44  |   const category = { ...common, applicationCategoryId:101, label:this.kind==='Category'?field('Category Label','category-a'):'category-a', active:true };
  45  |   const map = { ...common, importMapId:this.kind==='Import Map'?101:201, keyName:this.kind==='Import Map'?field('Module Name','container-a'):'container-a', path:field('Path','https://fixture.example/base.js'), active:true };
  46  |   const tile = { ...common, applicationTileId:all.includes('"301"') || this.id==='BFF-ADM-097'?301:101, title:field('Tile Name','tile-a'), subtitle:'Fixture tile', module:'/fixture', tile:'/tile-a', ems2Entities:'E-TRADE', ems2Subject:'', entryName:'Global', filterRule:'', template:false, imageLightTheme:'light-a.png', imageDarkTheme:'dark-a.png', emailSupport:'support@example.test', applicationCategory:{applicationCategoryId:101}, importMap:{importMapId:map.importMapId} };
  47  |   if(this.kind==='Category') category.active=false;
  48  |   if(this.kind==='Import Map') map.active=false;
  49  |   if(all.includes('originally loaded')) { if(this.kind==='Category')category.label='OLD';else if(this.kind==='Import Map')map.keyName='OLD';else tile.title='OLD'; }
  50  |   if(all.includes('Category 101 is inactive')) category.active=false;
  51  |   if(all.includes('Import Map 201 is inactive')) map.active=false;
  52  |   const categories:any[]=[category], importMaps:any[]=[map], tiles:any[]=this.kind==='Tile'?[tile]:[];
  53  |   if(this.kind==='Category' && /existing Category record already|Category record "102" already/.test(all))categories.push({...common,applicationCategoryId:102,label:'shared-a'});
  54  |   if(this.kind==='Import Map' && /existing Import Map record already|Import Map record "102" already/.test(all))importMaps.push({...common,importMapId:102,keyName:all.includes('equal to "react"')?'react':'shared-a',path:'https://fixture.example/initial.js',active:true});
  55  |   if(all.includes('reference "102"'))categories.push({...common,applicationCategoryId:102,label:'foreign-category',ems2Role:'OTHER_ADMIN'});
  56  |   if(all.includes('reference "202"'))importMaps.push({...common,importMapId:202,keyName:'foreign-map',path:'https://fixture.example/foreign.js',ems2Role:'OTHER_ADMIN'});
  57  |   await this.fixture('reset'); await this.fixture('seed',{categories,importMaps,tiles});
  58  |   await blockExternal(this.page);
  59  |   await this.page.route('**/api/auth/**',async route=>{
  60  |    const url=new URL(route.request().url());
  61  |    let body:any=route.request().method()==='POST'?route.request().postDataJSON():null;
  62  |    const parts=url.pathname.split('/'); const operation=parts.at(-1)!; const resource=parts.at(-2)!;
  63  |    const admin=url.pathname.includes('/v1/fmo/admin/');
  64  |    if(admin && ['create','update'].includes(operation)){
  65  |     if(all.includes('"applicationCategory.applicationCategoryId" as 102'))body.applicationCategory={applicationCategoryId:102};
  66  |     if(all.includes('"importMap.importMapId" as 202'))body.importMap={importMapId:202};
  67  |     if(all.includes('"importMap" as null'))body.importMap=null;
  68  |    }
  69  |    const response=await route.fetch({url:`${currentBff}${url.pathname.replace('/api/auth','')}${url.search}`, ...(body?{postData:body}:{})});
  70  |    let payload:any;try{payload=await response.json();}catch{payload={raw:await response.text()};}
  71  |    if(operation==='login') {this.access=response.headers()['single-ui-authorization']??'';this.entitlements=payload.entitlementsToken??'';}
  72  |    if(admin)this.requests.push({resource,operation,body:{...body,entitlementsToken:body?.entitlementsToken?'[SIGNED LOCAL TEST TOKEN]':undefined},status:response.status(),response:payload});
  73  |    await route.fulfill({response});
  74  |   });
  75  |   const initial={...workspace(this.kind),containers:[{id:'CURRENT-BFF-ADMIN',container:'@fm/base',module:`/${this.resource}`,tile:'',title:this.kind,emailSupport:'support@example.test',panelId:'',tabId:'',parameters:{}}]};
  76  |   await this.page.addInitScript(value=>{if(!localStorage.getItem('SET_WORKSPACES'))localStorage.setItem('SET_WORKSPACES',JSON.stringify([value]));},initial);
  77  |   const login=await openLogin(this.page);await login.fillUsername(subject);await login.fillPassword('FixturePass1!');await login.clickSignInButton();await this.ui.portal.expectVisible();
  78  |   await expect(this.ui.grid).toBeVisible();if(this.kind==='Tile')await this.ui.selectCategory('category-a');
  79  |   await expect(this.ui.row(String(this.kind==='Tile'?tile.applicationTileId:101))).toBeVisible();
  80  |   await this.audit.record('bff-boundary',{origin:currentBff,scope:'Actual current controllers, services, signed tokens, JPA and disposable PostgreSQL. Controlled OUD/EMS2/bootstrap.',subject,role:subject==='admin-s'?'SUPER_USER':'FMO_ADMIN'});
  81  |  }
  82  |  async gridSnapshot(): Promise<unknown> {return this.ui.grid.locator('[data-id]').evaluateAll(rows=>rows.map(row=>({id:row.getAttribute('data-id'),values:Array.from(row.querySelectorAll('[data-field]')).filter(cell=>cell.getAttribute('data-field')!=='actions').map(cell=>[cell.getAttribute('data-field'),cell.textContent])})));}
  83  |  async remember(): Promise<void>{this.initialGrid=await this.gridSnapshot();this.initialPersisted=await this.snapshot();await this.audit.record('initial-persisted-records',this.initialPersisted);}
  84  |  async fill(name:string,value:string):Promise<void>{this.lastSubmitted[name]=value;await this.ui.field(name).fill(value);}
  85  |  async clickFooter(name:string):Promise<void>{const count=this.requests.length;await this.ui.footerButton(name).click();if(['Create','Update','Verified','Deactivate'].includes(name)){await expect.poll(()=>this.requests.length).toBeGreaterThan(count);await this.audit.record('ui-origin-bff-requests',this.requests);await this.audit.record('persisted-after-submit',await this.snapshot());}}
  86  |  lastMutation(){return [...this.requests].reverse().find(x=>['create','update'].includes(x.operation));}
  87  |  async directUpdate(subject:string,mode:string,changes:Record<string,unknown>={}):Promise<void>{
  88  |   const login=await this.page.request.post(`${currentBff}/v2/sso/login`,{data:{username:subject,password:'FixturePass1!',device:'LOCAL_UI_AUDIT'}});expect(login.ok()).toBe(true);const payload=await login.json();
  89  |   const rows:any[]=await this.snapshot(); const row=rows.find(row=>Number(row[sqlKey(this.kind)])===101)!;
  90  |   const base:any=Object.fromEntries(Object.entries(row).map(([name,value])=>[name.replace(/_([a-z])/g,(_,letter)=>letter.toUpperCase()),value]));
  91  |   base.active=base.isActive;delete base.isActive;
  92  |   if(this.kind==='Tile'){base.importMap={importMapId:base.importMapId};base.applicationCategory={applicationCategoryId:base.applicationCategoryId};}
  93  |   const response=await this.page.request.post(`${currentBff}/v1/fmo/admin/${this.resource}/update`,{headers:{'single-ui-authorization':login.headers()['single-ui-authorization']},data:{...base,...changes,mode,entitlementsToken:payload.entitlementsToken}});
  94  |   await this.audit.record(`concurrent-${subject}-${mode}`,{status:response.status(),response:await response.json()});expect(response.ok()).toBe(true);
  95  |  }
  96  |  async assertUnchanged():Promise<void>{expect(await this.snapshot()).toEqual(this.initialPersisted);expect(await this.gridSnapshot()).toEqual(this.initialGrid);}
  97  |  async errorAlert(exact?:string):Promise<void>{const alert=this.page.getByRole('alert').filter({has:this.page.locator('.MuiAlert-message')});await expect(alert).toBeVisible();await expect(alert).toHaveClass(/MuiAlert-standardError|MuiAlert-filledError|MuiAlert-outlinedError/);if(exact)await expect(alert.locator('.MuiAlert-message')).toHaveText(exact);else {const mutation=this.lastMutation();expect(mutation?.status).toBeGreaterThanOrEqual(400);await expect(alert.locator('.MuiAlert-message')).not.toHaveText('');await this.audit.record('undefined-message-contract',{canonical:'Agreed message is unavailable. Only real error response and visible nonempty error are characterized.',actual:await alert.innerText()});}}
  98  |  async cell(name:string,id:string){return this.ui.reveal(adminFields[name]??name,id);}
  99  | }
  100 | 
```