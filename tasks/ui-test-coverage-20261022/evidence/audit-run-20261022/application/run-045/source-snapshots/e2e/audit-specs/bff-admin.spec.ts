import { test, expect } from '../support/audit-fixture.js';
import { BffAdminApp, currentBff, resourceFor, keyFor } from '../support/bff-admin-app.js';
import type { AdminKind } from '../support/admin-app.js';

// These cases share only this disposable database. Run this file with one worker.
test.describe.configure({mode:'default'});
test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',auditFixture:'Actual current React and exact-current BFF admin controllers/services/JPA with actual migration DDL in disposable PostgreSQL. Controlled OUD/EMS2 identities and local Spring bootstrap. Fixture SQL seeds/mutates isolated records; service errors are actual database errors. Undefined agreed messages remain unresolved acceptance.'});
for(let n=1;n<=97;n++){
 const id=`BFF-ADM-${String(n).padStart(3,'0')}`;
 test(`${id} current BFF administration through actual UI`,async({page,audit},testInfo)=>{
  test.setTimeout(90000);
  const steps=await audit.defineCase(id);const all=steps.map(s=>s.text).join('\n');
  const kind:AdminKind=/controlled (Category|Import Map|Tile) fixture/.exec(all)?.[1] as AdminKind ?? 'Category';
  const app=new BffAdminApp(page,kind,id,steps,audit);let match:RegExpExecArray|null;let creationClock=false;
  const field=(name:string)=>name==='Record Id'?keyFor(kind):name==='Category Label'?'label':name==='Module Name'?'keyName':name==='Tile Name'?'title':name==='Path'?'path':name==='Module Path'?'module':name==='Tile Path'?'tile':name==='Entry Name'?'entryName':'ems2Entities';
  if(all.includes('agreed'))testInfo.annotations.push({type:'audit-limit',description:'Undefined agreed error-message or policy contract. Execution is a proposed probe, not approved business acceptance.'});
  for(const step of steps)await audit.step(step.number,async()=>{
   const text=step.text;
   if(step.number===1){await app.setup();return;}
   if(/controlled (Category|Import Map|Tile) fixture records/.test(text)){await app.remember();return;}
   if(text.includes('controlled creation clock')){creationClock=true;await audit.record('creation-clock',{milliseconds:1700000000000,scope:'Only the Create New event uses the fixed date. Authentication and session clocks remain native.'});return;}
   if(/^the baseline fixture data defines|^the baseline Tile references|^both references belong/.test(text)){await audit.record(`fixture-step-${step.number}`,{definition:text,actual:await app.snapshot()});return;}
   if(text.startsWith('Category 101 has label')){const snapshot=await app.sql(['SELECT label FROM post_trade_portal_service.application_category WHERE application_category_id=101']);await audit.record('reference-snapshot',snapshot);return;}
   if(/prepared database uses the inspected migration DDL/.test(text)){const schema=await app.sql(["SELECT table_name,column_name,data_type,character_maximum_length FROM information_schema.columns WHERE table_schema='post_trade_portal_service' ORDER BY table_name,ordinal_position"]);await audit.record('actual-migration-schema',schema);return;}
   if(text.startsWith('the controlled BFF configuration')){await app.fixture('seed',{creationEnabled:false});return;}
   if(text.startsWith('the next BFF repository save')){await app.fixture('seed',{failure:`${app.resource}-save`});return;}
   if((match=/^Admin [ABCS] clicks the button labeled "([^"]+)"/.exec(text))){if(match[1].startsWith('Create New')){const nativeNow=Date.now();if(creationClock)await page.clock.setFixedTime(new Date(1700000000000));await app.ui.panel.getByRole('button',{name:match[1],exact:true}).click();if(creationClock)await page.clock.setFixedTime(new Date(nativeNow));}else {const row= /row with "Record Id" "(\d+)"/.exec(text)?.[1];if(row){await app.ui.reveal('actions',row);await app.ui.action(match[1],row).click();}else await app.clickFooter(match[1]);}return;}
   if((match=/^the dialog titled "([^"]+)" (is visible|remains visible)/.exec(text))){await expect(app.ui.dialog()).toBeVisible();await expect(app.ui.dialog()).toContainText(match[1]);return;}
   if((match=/^Admin [ABCS] fills the (?:textbox|textarea) labeled "([^"]+)" with exactly (\d+) ASCII "a" characters/.exec(text))){await app.fill(match[1],'a'.repeat(Number(match[2])));return;}
   if((match=/^Admin [ABCS] fills the (?:textbox|textarea) labeled "([^"]+)" with "(.*)" in dialog/.exec(text))){await app.fill(match[1],match[2].replaceAll('\\"','"').replaceAll('\\t','\t'));return;}
   if((match=/^Admin [ABCS] clicks the combobox labeled "([^"]+)"/.exec(text))){await app.ui.field(match[1],'combobox').click();return;}
   if((match=/^Admin [ABCS] clicks the option labeled "([^"]+)"/.exec(text))){await page.getByRole('option',{includeHidden:true}).filter({hasText:new RegExp(`^${match[1].replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}$`)}).click();return;}
   if((match=/^the alert with severity "error".*contains the exact text "(.*)"$/.exec(text))){await app.errorAlert(match[1]);return;}
   if(text.startsWith('the alert with severity "error"')){const response=app.lastMutation();await audit.record('rejection-or-policy-observation',response);await app.errorAlert(text.includes('captured rejection')?response?.response.errorMessage:undefined);return;}
   if(/row identifiers and loaded field values equal/.test(text)){await app.assertUnchanged();return;}
   if((match=/contains exactly one existing row with value "([^"]+)"/.exec(text))){const key=field(kind==='Category'?'Category Label':'Module Name');await expect(app.ui.grid.locator(`[data-field="${key}"]`).filter({hasText:new RegExp(`^${match[1]}$`)})).toHaveCount(1);expect((await app.snapshot()).filter(row=>row[key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]===match![1])).toHaveLength(1);return;}
   if(text.includes('contains exactly one row with the create response Record Id')){const response=app.lastMutation();expect(response?.status).toBe(200);const row=String(response?.response.data[app.key]);await expect(app.ui.row(row)).toHaveCount(1);return;}
   if((match=/its "([^"]+)" cell equals the submitted value without truncation/.exec(text))){const row=String(app.lastMutation()?.response.data[app.key]);await expect(await app.cell(match[1],row)).toHaveText(app.lastSubmitted[match[1]]);return;}
   if((match=/independent persisted-record readback contains exactly (\d+) ASCII "a" characters in "([^"]+)"/.exec(text))){const rows=await app.snapshot();const row=rows.find(row=>String(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===String(app.lastMutation()?.response.data[app.key]));expect(row[field(match[2]).replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]).toBe('a'.repeat(Number(match[1])));return;}
   if(/grid has record/.test(text)){const row=/record "(\d+)"/.exec(text)?.[1];await expect(app.ui.row(row)).toBeVisible();return;}
   if(/record "\d+" is inactive/.test(text)){expect((await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===Number(/record "(\d+)"/.exec(text)?.[1]))?.is_active).toBe(false);return;}
   if((match=/^its stored "updatedBy" value is "([^"]+)"/.exec(text))){expect((await app.snapshot())[0].updated_by).toBe(match[1]);return;}
   if(/originally loaded/.test(text)){expect((await app.snapshot())[0][kind==='Category'?'label':kind==='Import Map'?'key_name':'title']).toBe('OLD');return;}
   if(/^an existing|record "102" already/.test(text)){await audit.record('existing-duplicate-fixture',await app.snapshot());return;}
   if(text.startsWith('the controlled database event changes')){await app.mutate({ems2_role:'OTHER_ADMIN'});return;}
   if(text.startsWith('the controlled stale grid exposes')){await expect(app.ui.row('901')).toBeVisible();await audit.record('stale-grid-contract',{definition:text,limit:'Only the declared stale grid data response includes the actual seeded foreign record. The audit request executes the actual BFF authorization.'});return;}
   if(text.startsWith('no cell in dialog "Audit"')){await expect(app.ui.auditDialog()).not.toContainText('PROTECTED-FOREIGN');return;}
   if((match=/^the controlled database event removes (Category|Import Map) (\d+)/.exec(text))){await app.sql([`DELETE FROM post_trade_portal_service.${match[1]==='Category'?'application_category':'import_map'} WHERE ${match[1]==='Category'?'application_category_id':'import_map_id'}=${match[2]}`]);return;}
   if((match=/Admin B completes a controlled concurrent update setting "([^"]+)" to "NEW"/.exec(text))){await app.directUpdate('admin-b','maker',{[field(match[1])]:'NEW'});return;}
   if(text.startsWith('Admin A completes a controlled maker update')){await app.directUpdate('admin-a','maker',{[field(kind==='Category'?'Category Label':kind==='Import Map'?'Module Name':'Tile Name')]:'NEW'});return;}
   if(text.startsWith('Admin B completes a controlled verification')){await app.directUpdate('admin-b','checker');return;}
   if(text.includes('persisted-record readback')&&text.includes('"active" equal to false')){const rows=await app.snapshot();expect(rows[0].is_active).toBe(false);return;}
   if(text.includes('status tooltip "Unverified or Deactivated"')){const row=/record "(\d+)"/.exec(text)?.[1]??'101';const cell=await app.ui.reveal('active',row);await expect(cell.getByTestId('DangerousIcon')).toBeVisible();await cell.hover();await expect(page.getByRole('tooltip',{name:'Unverified or Deactivated',exact:true})).toBeVisible();return;}
   if(text.includes('independent persisted-record readback retains the concurrent result')){const rows=await app.snapshot();if(text.endsWith('"active"'))expect(rows[0].is_active).toBe(true);else expect(rows[0][kind==='Category'?'label':kind==='Import Map'?'key_name':'title']).toBe('NEW');return;}
   if(text.startsWith('a subsequent')){const response=await page.request.post(`${currentBff}/v1/fmo/admin/${app.resource}/data`,{headers:{'single-ui-authorization':app.access},data:{entitlementsToken:app.entitlements}});expect(response.ok()).toBe(true);const payload=await response.json();await audit.record('independent-data-response',payload);const persisted=(await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===101);const record=payload.data.find((row:any)=>Number(row[app.key])===101);const changed=kind==='Category'?'label':kind==='Import Map'?'keyName':'title';expect(record[changed]).toBe(persisted[changed.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]);expect(new Date(record.updatedAt).getTime()).toBe(new Date(persisted.updated_at).getTime());return;}
   if(text.startsWith('the installed request interceptor')||text.startsWith('reference "')||text.endsWith('entitlement')){await audit.record(`fixture-step-${step.number}`,{definition:text});return;}
   if(text.startsWith('the active-import-map response')){const response=await page.request.get(`${currentBff}/v1/fmo/admin/importmap/active`);const result=await response.json();await audit.record('active-import-map-response',result);if(text.includes('unsafe Path'))expect(Object.values(result.imports)).not.toContain(app.lastSubmitted.Path);else expect(result.imports.react).toBe('https://fixture.example/initial.js');return;}
   if(text.startsWith('the persisted Tile record equals')){expect(await app.snapshot()).toEqual(app.initialPersisted);return;}
   if(text.includes('grid row "301" retains')){await expect(await app.cell('Aplication Category Record Id','301')).toHaveText('101');await expect(await app.cell('Container Record Id','301')).toHaveText('201');return;}
   if(text.includes('primary save persists record 101')){
    await app.fixture('seed',{failure:`${app.resource}-audit`});
    // The canonical setup specifies an already completed write. Execute its actual UI request before the reload action.
    await app.ui.action('Edit','101').click();
    for(const [name,value] of Object.entries(kind==='Category'?{'Category Label':'persisted-after-audit-failure'}:kind==='Import Map'?{'Module Name':'persisted-after-audit-failure','Path':'https://fixture.example/failed-audit.js'}:{'Tile Name':'persisted-after-audit-failure','Module Path':'/fixture','Tile Path':'/failed-audit','Role Entities':'E-TRADE'}))await app.fill(name,value);
    await app.clickFooter('Update');app.initialCreateCount=app.requests.filter(x=>x.operation==='create').length;expect(app.lastMutation()?.status).toBeGreaterThanOrEqual(400);const after=await app.snapshot();expect(after).toHaveLength(app.initialPersisted.length);const saved=after.find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===101);expect(saved[kind==='Category'?'label':kind==='Import Map'?'key_name':'title']).toBe('persisted-after-audit-failure');await audit.record('partial-save-readback',after);return;
   }
   if(text.includes('has received the error response')){expect(app.lastMutation()?.status).toBeGreaterThanOrEqual(400);return;}
   if(text.startsWith('Admin A reloads')){await page.reload();await expect(app.ui.grid).toBeVisible();if(kind==='Tile')await app.ui.selectCategory('category-a');return;}
   if(text.includes('contains exactly one row with "Record Id" equal to "101"')){await expect(app.ui.row('101')).toHaveCount(1);return;}
   if(text.includes('that row displays the values returned by the persisted-record readback')){const row=(await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===101);await expect(await app.cell(kind==='Category'?'Category Label':kind==='Import Map'?'Module Name':'Tile Name','101')).toHaveText(row[kind==='Category'?'label':kind==='Import Map'?'key_name':'title']);return;}
   if(text.includes('no additional create request after the reload')){expect(app.requests.filter(x=>x.operation==='create')).toHaveLength(app.initialCreateCount);return;}
   if(text.startsWith('Category 101 is inactive')||text.startsWith('Import Map 201 is inactive')){await audit.record('inactive-reference',await app.sql([`SELECT * FROM post_trade_portal_service.${text.startsWith('Category')?'application_category':'import_map'}`]));return;}
   if(text.startsWith('Tile 301 has')){const row=(await app.snapshot()).find(row=>row.application_tile_id===301);expect(row.image_light_theme).toBe('light-a.png');expect(row.image_dark_theme).toBe('dark-a.png');return;}
   if(text.startsWith('its completed maker update creates audit row')){await app.sql(['ALTER SEQUENCE post_trade_portal_service.application_tile_audit_seq RESTART WITH 5001']);await app.directUpdate('admin-a','maker',{},301);const rows=await app.sql(['SELECT * FROM post_trade_portal_service.application_tile_audit WHERE application_tile_audit_id=5001']);await audit.record('actual-generated-tile-audit',rows);expect(rows.results[0].rows).toHaveLength(1);return;}
   if((match=/^the cell under "Image URL for (Light|Dark) Theme" equals "([^"]+)" in audit row "(\d+)"/.exec(text))){const grid=app.ui.auditDialog().getByRole('grid',{includeHidden:true});const target=grid.locator(`[data-id="${match[3]}"] [data-field="image${match[1]}Theme"]`);const scroller=grid.locator('.MuiDataGrid-virtualScroller');for(let i=0;i<20 && !await target.count();i++){await scroller.evaluate(node=>{node.scrollLeft+=400;});await page.waitForTimeout(30);}await target.scrollIntoViewIfNeeded();await expect(target).toBeVisible();await expect(target).toHaveText(match[2]);return;}
   throw new Error(`Missing exact BFF UI binding at ${id} step${step.number}: ${text}`);
  });
 });
}
