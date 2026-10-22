import { expect, type Page } from '@playwright/test';
import { AdminApp, adminFields, type AdminKind } from './admin-app.js';
import { blockExternal, localPrefix, openLogin, workspace } from './local-app.js';
import type { AuditCapture, CanonicalStep } from './audit-fixture.js';

export const currentBff = 'http://127.0.0.1:8090/api/auth';
export const resourceFor = (kind: AdminKind) => kind === 'Category' ? 'category' : kind === 'Import Map' ? 'importmap' : 'tile';
export const keyFor = (kind: AdminKind) => kind === 'Category' ? 'applicationCategoryId' : kind === 'Import Map' ? 'importMapId' : 'applicationTileId';
const sqlTable = (kind: AdminKind) => kind === 'Category' ? 'application_category' : kind === 'Import Map' ? 'import_map' : 'application_tile';
const sqlKey = (kind: AdminKind) => keyFor(kind).replace(/[A-Z]/g, c => `_${c.toLowerCase()}`);
const quote = (value: unknown) => value === null ? 'NULL' : typeof value === 'number' || typeof value === 'boolean' ? String(value) : `'${String(value).replaceAll("'", "''")}'`;
export class BffAdminApp {
 readonly ui: AdminApp;
 readonly resource: string;
 readonly key: string;
 readonly requests: { resource: string; operation: string; body: any; status: number; response: any }[] = [];
 initialGrid: unknown;
 initialPersisted: any[] = [];
 lastSubmitted: Record<string, string> = {};
 access = '';
 entitlements = '';
 initialCreateCount = 0;
 constructor(readonly page: Page, readonly kind: AdminKind, readonly id: string, readonly steps: readonly CanonicalStep[], readonly audit: AuditCapture) {
  this.ui = new AdminApp(page, kind, id); this.resource = resourceFor(kind); this.key = keyFor(kind);
 }
 async fixture(operation: string, body: unknown = {}): Promise<any> {
  const response = await this.page.request.post(`${currentBff}/local/fixture/${operation}`, { data: body });
  const text = await response.text(); expect(response.ok(), `Fixture ${operation}: ${text}`).toBe(true);
  return text ? JSON.parse(text) : {};
 }
 async sql(statements: string[]): Promise<any> { return this.fixture('sql', { statements }); }
 async snapshot(): Promise<any[]> {
  const result = await this.sql([`SELECT * FROM post_trade_portal_service.${sqlTable(this.kind)} ORDER BY ${sqlKey(this.kind)}`]);
  return result.results?.[0]?.rows ?? result[0]?.rows ?? result.rows ?? [];
 }
 async mutate(set: Record<string, unknown>, id = 101) {
  await this.sql([`UPDATE post_trade_portal_service.${sqlTable(this.kind)} SET ${Object.entries(set).map(([name,value])=>`${name}=${quote(value)}`).join(',')} WHERE ${sqlKey(this.kind)}=${id}`]);
 }
 async setup(): Promise<void> {
  const all = this.steps.map(step => step.text).join('\n');
  const subject = /uses subject "([^"]+)"/.exec(all)?.[1] ?? 'admin-a';
  const field = (name:string, fallback:string) => new RegExp(`baseline fixture data defines "${name}" as "([^"\\n]*)"`).exec(all)?.[1] ?? fallback;
  const common = { ems2Role:'FMO_ADMIN', active:false, createdAt:'2026-10-22T00:00:00Z', updatedAt:'2026-10-22T00:00:00Z', createdBy:'admin-a', updatedBy:all.includes('"ADMIN-A"')?'ADMIN-A':'admin-a', orderNo:7 };
  const category = { ...common, applicationCategoryId:101, label:this.kind==='Category'?field('Category Label','category-a'):'category-a', active:true };
  const map = { ...common, importMapId:this.kind==='Import Map'?101:201, keyName:this.kind==='Import Map'?field('Module Name','container-a'):'container-a', path:field('Path','https://fixture.example/base.js'), active:true };
  const tile = { ...common, applicationTileId:all.includes('"301"') || this.id==='BFF-ADM-097'?301:101, title:field('Tile Name','tile-a'), subtitle:'Fixture tile', module:'/fixture', tile:'/tile-a', ems2Entities:'E-TRADE', ems2Subject:'', entryName:'Global', filterRule:'', template:false, imageLightTheme:'light-a.png', imageDarkTheme:'dark-a.png', emailSupport:'support@example.test', applicationCategory:{applicationCategoryId:101}, importMap:{importMapId:map.importMapId} };
  if(this.kind==='Category') category.active=false;
  if(this.kind==='Import Map') map.active=false;
  if(all.includes('originally loaded')) { if(this.kind==='Category')category.label='OLD';else if(this.kind==='Import Map')map.keyName='OLD';else tile.title='OLD'; }
  if(all.includes('Category 101 is inactive')) category.active=false;
  if(all.includes('Import Map 201 is inactive')) map.active=false;
  const categories:any[]=[category], importMaps:any[]=[map], tiles:any[]=this.kind==='Tile'?[tile]:[];
  if(this.kind==='Category' && /existing Category record already|Category record "102" already/.test(all))categories.push({...common,applicationCategoryId:102,label:'shared-a'});
  if(this.kind==='Import Map' && /existing Import Map record already|Import Map record "102" already/.test(all))importMaps.push({...common,importMapId:102,keyName:all.includes('equal to "react"')?'react':'shared-a',path:'https://fixture.example/initial.js',active:true});
  if(all.includes('reference "102"'))categories.push({...common,applicationCategoryId:102,label:'foreign-category',ems2Role:'OTHER_ADMIN'});
  if(all.includes('reference "202"'))importMaps.push({...common,importMapId:202,keyName:'foreign-map',path:'https://fixture.example/foreign.js',ems2Role:'OTHER_ADMIN'});
  await this.fixture('reset'); await this.fixture('seed',{categories,importMaps,tiles});
  await blockExternal(this.page);
  await this.page.route('**/api/auth/**',async route=>{
   const url=new URL(route.request().url());
   let body:any=route.request().method()==='POST'?route.request().postDataJSON():null;
   const parts=url.pathname.split('/'); const operation=parts.at(-1)!; const resource=parts.at(-2)!;
   const admin=url.pathname.includes('/v1/fmo/admin/');
   if(admin && ['create','update'].includes(operation)){
    if(all.includes('"applicationCategory.applicationCategoryId" as 102'))body.applicationCategory={applicationCategoryId:102};
    if(all.includes('"importMap.importMapId" as 202'))body.importMap={importMapId:202};
    if(all.includes('"importMap" as null'))body.importMap=null;
   }
   const response=await route.fetch({url:`${currentBff}${url.pathname.replace('/api/auth','')}${url.search}`, ...(body?{postData:body}:{})});
   let payload:any;try{payload=await response.json();}catch{payload={raw:await response.text()};}
   if(operation==='login') {this.access=response.headers()['single-ui-authorization']??'';this.entitlements=payload.entitlementsToken??'';}
   if(admin)this.requests.push({resource,operation,body:{...body,entitlementsToken:body?.entitlementsToken?'[SIGNED LOCAL TEST TOKEN]':undefined},status:response.status(),response:payload});
   await route.fulfill({response});
  });
  const initial={...workspace(this.kind),containers:[{id:'CURRENT-BFF-ADMIN',container:'@fm/base',module:`/${this.resource}`,tile:'',title:this.kind,emailSupport:'support@example.test',panelId:'',tabId:'',parameters:{}}]};
  await this.page.addInitScript(value=>{if(!localStorage.getItem('SET_WORKSPACES'))localStorage.setItem('SET_WORKSPACES',JSON.stringify([value]));},initial);
  const login=await openLogin(this.page);await login.fillUsername(subject);await login.fillPassword('FixturePass1!');await login.clickSignInButton();await this.ui.portal.expectVisible();
  await expect(this.ui.grid).toBeVisible();if(this.kind==='Tile')await this.ui.selectCategory('category-a');
  await expect(this.ui.row(String(this.kind==='Tile'?tile.applicationTileId:101))).toBeVisible();
  await this.audit.record('bff-boundary',{origin:currentBff,scope:'Actual current controllers, services, signed tokens, JPA and disposable PostgreSQL. Controlled OUD/EMS2/bootstrap.',subject,role:subject==='admin-s'?'SUPER_USER':'FMO_ADMIN'});
 }
 async gridSnapshot(): Promise<unknown> {return this.ui.grid.locator('[data-id]').evaluateAll(rows=>rows.map(row=>({id:row.getAttribute('data-id'),values:Array.from(row.querySelectorAll('[data-field]')).filter(cell=>cell.getAttribute('data-field')!=='actions').map(cell=>[cell.getAttribute('data-field'),cell.textContent])})));}
 async remember(): Promise<void>{this.initialGrid=await this.gridSnapshot();this.initialPersisted=await this.snapshot();await this.audit.record('initial-persisted-records',this.initialPersisted);}
 async fill(name:string,value:string):Promise<void>{this.lastSubmitted[name]=value;await this.ui.field(name).fill(value);}
 async clickFooter(name:string):Promise<void>{const count=this.requests.length;await this.ui.footerButton(name).click();if(['Create','Update','Verified','Deactivate'].includes(name)){await expect.poll(()=>this.requests.length).toBeGreaterThan(count);await this.audit.record('ui-origin-bff-requests',this.requests);await this.audit.record('persisted-after-submit',await this.snapshot());}}
 lastMutation(){return [...this.requests].reverse().find(x=>['create','update'].includes(x.operation));}
 async directUpdate(subject:string,mode:string,changes:Record<string,unknown>={}):Promise<void>{
  const login=await this.page.request.post(`${currentBff}/v2/sso/login`,{data:{username:subject,password:'FixturePass1!',device:'LOCAL_UI_AUDIT'}});expect(login.ok()).toBe(true);const payload=await login.json();
  const rows:any[]=await this.snapshot(); const row=rows.find(row=>Number(row[sqlKey(this.kind)])===101)!;
  const base:any=Object.fromEntries(Object.entries(row).map(([name,value])=>[name.replace(/_([a-z])/g,(_,letter)=>letter.toUpperCase()),value]));
  base.active=base.isActive;delete base.isActive;
  if(this.kind==='Tile'){base.importMap={importMapId:base.importMapId};base.applicationCategory={applicationCategoryId:base.applicationCategoryId};}
  const response=await this.page.request.post(`${currentBff}/v1/fmo/admin/${this.resource}/update`,{headers:{'single-ui-authorization':login.headers()['single-ui-authorization']},data:{...base,...changes,mode,entitlementsToken:payload.entitlementsToken}});
  await this.audit.record(`concurrent-${subject}-${mode}`,{status:response.status(),response:await response.json()});expect(response.ok()).toBe(true);
 }
 async assertUnchanged():Promise<void>{expect(await this.snapshot()).toEqual(this.initialPersisted);expect(await this.gridSnapshot()).toEqual(this.initialGrid);}
 async errorAlert(exact?:string):Promise<void>{const alert=this.page.getByRole('alert').filter({has:this.page.locator('.MuiAlert-message')});await expect(alert).toBeVisible();await expect(alert).toHaveClass(/MuiAlert-standardError|MuiAlert-filledError|MuiAlert-outlinedError/);if(exact)await expect(alert.locator('.MuiAlert-message')).toHaveText(exact);else {const mutation=this.lastMutation();expect(mutation?.status).toBeGreaterThanOrEqual(400);await expect(alert.locator('.MuiAlert-message')).not.toHaveText('');await this.audit.record('undefined-message-contract',{canonical:'Agreed message is unavailable. Only real error response and visible nonempty error are characterized.',actual:await alert.innerText()});}}
 async cell(name:string,id:string){return this.ui.reveal(adminFields[name]??name,id);}
}
