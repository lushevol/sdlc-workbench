# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: bff-admin.spec.ts >> BFF-ADM-097 current BFF administration through actual UI
- Location: e2e/audit-specs/bff-admin.spec.ts:10:2

# Error details

```
Error: locator.getAttribute: Error: strict mode violation: locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText('Audit', { exact: true }) }).getByRole('button', { name: 'resize', exact: true, includeHidden: true }) resolved to 2 elements:
    1) <button tabindex="0" type="button" value="check" aria-label="resize" aria-pressed="false" data-testid="MicroWebUI_base_Dialog-maximize" class="MuiButtonBase-root MuiToggleButton-root MuiToggleButton-sizeSmall MuiToggleButton-primary css-2t00w2-MuiButtonBase-root-MuiToggleButton-root">…</button> aka getByTestId('MicroWebUI_base_Dialog-maximize')
    2) <button tabindex="0" type="button" aria-label="resize" data-testid="MicroWebUI_base_Dialog-resize" class="MuiButtonBase-root MuiIconButton-root MuiIconButton-sizeLarge MicroWebUI_base_Dialog-root css-4w3i5g-MuiButtonBase-root-MuiIconButton-root">…</button> aka getByTestId('MicroWebUI_base_Dialog-resize')

Call log:
  - waiting for locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText('Audit', { exact: true }) }).getByRole('button', { name: 'resize', exact: true, includeHidden: true })

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
      - generic [ref=e27]: 06:15 UTC
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
                - generic [ref=e152]: Audit
                - generic [ref=e153]:
                  - button [ref=e154] [cursor=pointer]: Maximize
                  - button [ref=e157] [cursor=pointer]:
                    - generic [ref=e158]: Close
            - grid [ref=e162]:
              - generic [ref=e163]:
                - rowgroup [ref=e164]:
                  - row [ref=e165]:
                    - columnheader [ref=e166] [cursor=pointer]:
                      - generic [ref=e167]: Audit ID
                    - columnheader [ref=e169] [cursor=pointer]:
                      - generic [ref=e170]: Transaction Mode
                    - columnheader [ref=e172] [cursor=pointer]:
                      - generic [ref=e173]: Tile ID
                    - columnheader [ref=e175] [cursor=pointer]:
                      - generic [ref=e176]: Aplication Category
                    - columnheader [ref=e178] [cursor=pointer]:
                      - generic [ref=e179]: Tile Name
                    - columnheader [ref=e181] [cursor=pointer]:
                      - generic [ref=e182]: Description
                    - columnheader [ref=e184] [cursor=pointer]:
                      - generic [ref=e185]: Image URL for Dark Theme
                    - columnheader [ref=e187] [cursor=pointer]:
                      - generic [ref=e188]: Image URL for Light Theme
                    - columnheader [ref=e190] [cursor=pointer]:
                      - generic [ref=e191]: Container
                    - columnheader [ref=e193] [cursor=pointer]:
                      - generic [ref=e194]: Module Path
                    - columnheader [ref=e196] [cursor=pointer]:
                      - generic [ref=e197]: Tile Path
                - rowgroup [ref=e199]:
                  - row [ref=e200]:
                    - cell [ref=e201]: "5001"
                    - cell [ref=e202]: maker
                    - cell [ref=e203]: "301"
                    - cell [ref=e204]: category-a
                    - cell [ref=e205]: tile-a
                    - cell [ref=e206]: Fixture tile
                    - cell [ref=e207]: light-a.png
                    - cell [ref=e208]: dark-a.png
                    - cell [ref=e209]: container-a
                    - cell [ref=e210]: /fixture
                    - cell [ref=e211]: /tile-a
              - generic [ref=e214]:
                - paragraph [ref=e215]: "Rows per page:"
                - generic [ref=e216]:
                  - combobox [ref=e217] [cursor=pointer]: "20"
                  - textbox [aria-hidden]: "20"
                - paragraph [ref=e218]: 1–1 of 1
                - generic [ref=e219]:
                  - button [disabled]
                  - button [disabled]
            - button [ref=e220]
```

# Test source

```ts
  1   | import { test, expect } from '../support/audit-fixture.js';
  2   | import { BffAdminApp, currentBff, resourceFor, keyFor } from '../support/bff-admin-app.js';
  3   | import type { AdminKind } from '../support/admin-app.js';
  4   | 
  5   | // These cases share only this disposable database. Run this file with one worker.
  6   | test.describe.configure({mode:'default'});
  7   | test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',auditFixture:'Actual current React and exact-current BFF admin controllers/services/JPA with actual migration DDL in disposable PostgreSQL. Controlled OUD/EMS2 identities and local Spring bootstrap. Fixture SQL seeds/mutates isolated records; service errors are actual database errors. Undefined agreed messages remain unresolved acceptance.'});
  8   | for(let n=1;n<=97;n++){
  9   |  const id=`BFF-ADM-${String(n).padStart(3,'0')}`;
  10  |  test(`${id} current BFF administration through actual UI`,async({page,audit},testInfo)=>{
  11  |   test.setTimeout(90000);
  12  |   const steps=await audit.defineCase(id);const all=steps.map(s=>s.text).join('\n');
  13  |   const kind:AdminKind=/controlled (Category|Import Map|Tile) fixture/.exec(all)?.[1] as AdminKind ?? 'Category';
  14  |   const app=new BffAdminApp(page,kind,id,steps,audit);let match:RegExpExecArray|null;let creationClock=false;
  15  |   const field=(name:string)=>name==='Record Id'?keyFor(kind):name==='Category Label'?'label':name==='Module Name'?'keyName':name==='Tile Name'?'title':name==='Path'?'path':name==='Module Path'?'module':name==='Tile Path'?'tile':name==='Entry Name'?'entryName':'ems2Entities';
  16  |   if(all.includes('agreed'))testInfo.annotations.push({type:'audit-limit',description:'Undefined agreed error-message or policy contract. Execution is a proposed probe, not approved business acceptance.'});
  17  |   for(const step of steps)await audit.step(step.number,async()=>{
  18  |    const text=step.text;
  19  |    if(step.number===1){await app.setup();return;}
  20  |    if(/controlled (Category|Import Map|Tile) fixture records/.test(text)){await app.remember();return;}
  21  |    if(text.includes('controlled creation clock')){creationClock=true;await audit.record('creation-clock',{milliseconds:1700000000000,scope:'Only the Create New event uses the fixed date. Authentication and session clocks remain native.'});return;}
  22  |    if((match=/^the baseline fixture data defines "([^"]+)" as "(.*)"$/.exec(text))){
  23  |     expect(app.baseline[match[1]]).toBe(match[2]);
  24  |     if(!all.includes('controlled creation clock')){
  25  |      const row=(await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===Number(/grid has record "(\d+)"/.exec(all)?.[1]??101));
  26  |      if(row){const property=match[1]==='Filter Rule'?'filter_rule':field(match[1]).replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`);const expected=all.includes(`originally loaded "${match[1]}"`)?'OLD':match[2];expect(row[property]).toBe(property==='filter_rule'&&expected===''?null:expected);}
  27  |     }
  28  |     await audit.record(`fixture-step-${step.number}`,{definition:text,inputDefault:app.baseline[match[1]],persisted:await app.snapshot(),limit:'Baseline input defaults are distinct from pre-existing records. Empty Filter Rule input and normalized SQL null remain separate representations.'});return;
  29  |    }
  30  |    if(text.startsWith('the baseline Tile references')){const rows=await app.snapshot();const tile=rows.find(row=>Number(row.application_tile_id)!==9902);if(tile){expect(tile.application_category_id).toBe(101);expect(tile.import_map_id).toBe(201);}await audit.record(`fixture-step-${step.number}`,{definition:text,expectedCategoryId:101,expectedImportMapId:201,existingTile:tile??null});return;}
  31  |    if(text.startsWith('Category 101 has label')||text.startsWith('both references belong')){
  32  |     const snapshot=await app.sql(['SELECT application_category_id,label,ems2_role FROM post_trade_portal_service.application_category WHERE application_category_id=101','SELECT import_map_id,key_name,ems2_role FROM post_trade_portal_service.import_map WHERE import_map_id=201']);
  33  |     expect(snapshot.results[0].rows).toEqual([{application_category_id:101,label:'category-a',ems2_role:'FMO_ADMIN'}]);
  34  |     expect(snapshot.results[1].rows).toEqual([{import_map_id:201,key_name:'container-a',ems2_role:'FMO_ADMIN'}]);
  35  |     if(text.startsWith('both references belong'))await expect(app.ui.category).toHaveValue('category-a');
  36  |     await audit.record(`reference-snapshot-${step.number}`,snapshot);return;
  37  |    }
  38  |    if(/prepared database uses the inspected migration DDL/.test(text)){const schema=await app.sql(["SELECT table_name,column_name,data_type,character_maximum_length FROM information_schema.columns WHERE table_schema='post_trade_portal_service' ORDER BY table_name,ordinal_position"]);await audit.record('actual-migration-schema',schema);return;}
  39  |    if(text.startsWith('the controlled BFF configuration')){await app.fixture('seed',{creationEnabled:false});return;}
  40  |    if(text.startsWith('the next BFF repository save')){await app.fixture('seed',{failure:`${app.resource}-save`});return;}
  41  |    if((match=/^Admin [ABCS] clicks the button labeled "([^"]+)"/.exec(text))){if(match[1].startsWith('Create New')){const nativeNow=Date.now();if(creationClock)await page.clock.setFixedTime(new Date(1700000000000));await app.ui.panel.getByRole('button',{name:match[1],exact:true}).click();if(creationClock)await page.clock.setFixedTime(new Date(nativeNow));}else {const row= /row with "Record Id" "(\d+)"/.exec(text)?.[1];if(row){await app.ui.reveal('actions',row);await app.ui.action(match[1],row).click();}else await app.clickFooter(match[1]);}return;}
  42  |    if((match=/^the dialog titled "([^"]+)" (is visible|remains visible)/.exec(text))){await expect(app.ui.dialog()).toBeVisible();await expect(app.ui.dialog()).toContainText(match[1]);return;}
  43  |    if((match=/^Admin [ABCS] fills the (?:textbox|textarea) labeled "([^"]+)" with exactly (\d+) ASCII "a" characters/.exec(text))){await app.fill(match[1],'a'.repeat(Number(match[2])));return;}
  44  |    if((match=/^Admin [ABCS] fills the (?:textbox|textarea) labeled "([^"]+)" with "(.*)" in dialog/.exec(text))){await app.fill(match[1],match[2].replaceAll('\\"','"').replaceAll('\\t','\t'));return;}
  45  |    if((match=/^Admin [ABCS] clicks the combobox labeled "([^"]+)"/.exec(text))){await app.ui.field(match[1],'combobox').click();return;}
  46  |    if((match=/^Admin [ABCS] clicks the option labeled "([^"]+)"/.exec(text))){await page.getByRole('option',{includeHidden:true}).filter({hasText:new RegExp(`^${match[1].replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}$`)}).click();await expect(app.ui.field('Container','combobox')).toHaveValue(match[1]);await page.waitForTimeout(350);return;}
  47  |    if((match=/^the alert with severity "error".*contains the exact text "(.*)"$/.exec(text))){await app.errorAlert(match[1]);return;}
  48  |    if(text.startsWith('the alert with severity "error"')){const response=app.lastMutation();await audit.record('rejection-or-policy-observation',response);await app.errorAlert(text.includes('captured rejection')?response?.response.errorMessage:undefined);return;}
  49  |    if(/row identifiers and loaded field values equal/.test(text)){await app.assertUnchanged();return;}
  50  |    if((match=/contains exactly one existing row with value "([^"]+)"/.exec(text))){const key=field(kind==='Category'?'Category Label':'Module Name');await expect(app.ui.grid.locator(`[data-field="${key}"]`).filter({hasText:new RegExp(`^${match[1]}$`)})).toHaveCount(1);expect((await app.snapshot()).filter(row=>row[key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]===match![1])).toHaveLength(1);return;}
  51  |    if(text.includes('contains exactly one row with the create response Record Id')){const response=app.lastMutation();expect(response?.status).toBe(200);const row=String(response?.response.data[app.key]);await expect(app.ui.row(row)).toHaveCount(1);return;}
  52  |    if((match=/its "([^"]+)" cell equals the submitted value without truncation/.exec(text))){const row=String(app.lastMutation()?.response.data[app.key]);await expect(await app.cell(match[1],row)).toHaveText(app.lastSubmitted[match[1]]);return;}
  53  |    if((match=/independent persisted-record readback contains exactly (\d+) ASCII "a" characters in "([^"]+)"/.exec(text))){const rows=await app.snapshot();const row=rows.find(row=>String(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===String(app.lastMutation()?.response.data[app.key]));expect(row[field(match[2]).replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]).toBe('a'.repeat(Number(match[1])));return;}
  54  |    if(/grid has record/.test(text)){const id=/record "(\d+)"/.exec(text)![1];const row=(await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===Number(id));expect(row?.ems2_role).toBe('FMO_ADMIN');await expect(app.ui.row(id)).toBeVisible();return;}
  55  |    if(/record "\d+" is inactive/.test(text)){expect((await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===Number(/record "(\d+)"/.exec(text)?.[1]))?.is_active).toBe(false);return;}
  56  |    if((match=/^its stored "updatedBy" value is "([^"]+)"/.exec(text))){expect((await app.snapshot())[0].updated_by).toBe(match[1]);return;}
  57  |    if(/originally loaded/.test(text)){expect((await app.snapshot())[0][kind==='Category'?'label':kind==='Import Map'?'key_name':'title']).toBe('OLD');return;}
  58  |    if(/^an existing|record "102" already/.test(text)){const rows=await app.snapshot();const expected=text.includes('"react"')?'react':'shared-a';const property=kind==='Category'?'label':'key_name';const matches=rows.filter(row=>row[property]===expected);expect(matches).toHaveLength(1);expect(matches[0][app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]).toBe(102);expect(matches[0].ems2_role).toBe('FMO_ADMIN');await audit.record('existing-duplicate-fixture',rows);return;}
  59  |    if(text.startsWith('the controlled database event changes')){await app.mutate({ems2_role:'OTHER_ADMIN'});return;}
  60  |    if(text.startsWith('the controlled stale grid exposes')){await expect(app.ui.row('901')).toBeVisible();await audit.record('stale-grid-contract',{definition:text,limit:'Only the declared stale grid data response includes the actual seeded foreign record. The audit request executes the actual BFF authorization.'});return;}
  61  |    if(text.startsWith('no cell in dialog "Audit"')){await expect(app.ui.auditDialog()).not.toContainText('PROTECTED-FOREIGN');return;}
  62  |    if((match=/^the controlled database event removes (Category|Import Map) (\d+)/.exec(text))){await app.sql([`DELETE FROM post_trade_portal_service.${match[1]==='Category'?'application_category':'import_map'} WHERE ${match[1]==='Category'?'application_category_id':'import_map_id'}=${match[2]}`]);return;}
  63  |    if((match=/Admin B completes a controlled concurrent update setting "([^"]+)" to "NEW"/.exec(text))){await app.directUpdate('admin-b','maker',{[field(match[1])]:'NEW'});return;}
  64  |    if(text.startsWith('Admin A completes a controlled maker update')){await app.directUpdate('admin-a','maker',{[field(kind==='Category'?'Category Label':kind==='Import Map'?'Module Name':'Tile Name')]:'NEW'});return;}
  65  |    if(text.startsWith('Admin B completes a controlled verification')){await app.directUpdate('admin-b','checker');return;}
  66  |    if(text.includes('persisted-record readback')&&text.includes('"active" equal to false')){const rows=await app.snapshot();expect(rows[0].is_active).toBe(false);return;}
  67  |    if(text.includes('status tooltip "Unverified or Deactivated"')){const row=/record "(\d+)"/.exec(text)?.[1]??'101';const cell=await app.ui.reveal('active',row);await expect(cell.getByTestId('DangerousIcon')).toBeVisible();await cell.hover();await expect(page.getByRole('tooltip',{name:'Unverified or Deactivated',exact:true})).toBeVisible();return;}
  68  |    if(text.includes('independent persisted-record readback retains the concurrent result')){const rows=await app.snapshot();if(text.endsWith('"active"'))expect(rows[0].is_active).toBe(true);else expect(rows[0][kind==='Category'?'label':kind==='Import Map'?'key_name':'title']).toBe('NEW');return;}
  69  |    if(text.startsWith('a subsequent')){const response=await page.request.post(`${currentBff}/v1/fmo/admin/${app.resource}/data`,{headers:{'single-ui-authorization':app.access},data:{entitlementsToken:app.entitlements}});expect(response.ok()).toBe(true);const payload=await response.json();await audit.record('independent-data-response',payload);const persisted=(await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===101);const record=payload.data.find((row:any)=>Number(row[app.key])===101);const changed=kind==='Category'?'label':kind==='Import Map'?'keyName':'title';expect(record[changed]).toBe(persisted[changed.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]);expect(new Date(record.updatedAt).getTime()).toBe(new Date(persisted.updated_at).getTime());return;}
  70  |    if(text.endsWith('entitlement')){expect(app.roles).not.toContain('OTHER_ADMIN');await audit.record(`fixture-step-${step.number}`,{definition:text,actualRoles:app.roles});return;}
  71  |    if(text.startsWith('reference "')){const id=Number(/reference "(\d+)"/.exec(text)![1]);const table=id===102?'application_category':'import_map';const key=id===102?'application_category_id':'import_map_id';const rows=await app.sql([`SELECT ${key},ems2_role FROM post_trade_portal_service.${table} WHERE ${key} IN (${id},${id===102?101:201}) ORDER BY ${key}`]);expect(rows.results[0].rows).toEqual([{[key]:id===102?101:201,ems2_role:'FMO_ADMIN'},{[key]:id,ems2_role:'OTHER_ADMIN'}]);await audit.record(`fixture-step-${step.number}`,{definition:text,actual:rows});return;}
  72  |    if(text.startsWith('the installed request interceptor')){await audit.record(`fixture-step-${step.number}`,{definition:text,limit:'The declared substitution is checked on the actual UI-originated request before forwarding.'});return;}
  73  |    if(text.startsWith('the active-import-map response')){const response=await page.request.get(`${currentBff}/v1/fmo/admin/importmap/active`);const result=await response.json();await audit.record('active-import-map-response',result);if(text.includes('unsafe Path'))expect(Object.values(result.imports)).not.toContain(app.lastSubmitted.Path);else expect(result.imports.react).toBe('https://fixture.example/initial.js');return;}
  74  |    if(text.startsWith('the persisted Tile record equals')){expect(await app.snapshot()).toEqual(app.initialPersisted);return;}
  75  |    if(text.includes('grid row "301" retains')){await expect(await app.cell('Aplication Category Record Id','301')).toHaveText('101');await expect(await app.cell('Container Record Id','301')).toHaveText('201');return;}
  76  |    if(text.includes('primary save persists record 101')){
  77  |     await app.fixture('seed',{failure:`${app.resource}-audit`});
  78  |     // The canonical setup specifies an already completed write. Execute its actual UI request before the reload action.
  79  |     await app.ui.action('Edit','101').click();
  80  |     for(const [name,value] of Object.entries(kind==='Category'?{'Category Label':'persisted-after-audit-failure'}:kind==='Import Map'?{'Module Name':'persisted-after-audit-failure','Path':'https://fixture.example/failed-audit.js'}:{'Tile Name':'persisted-after-audit-failure','Module Path':'/fixture','Tile Path':'/failed-audit','Role Entities':'E-TRADE'}))await app.fill(name,value);
  81  |     await app.clickFooter('Update');app.initialCreateCount=app.requests.filter(x=>x.operation==='create').length;expect(app.lastMutation()?.status).toBeGreaterThanOrEqual(400);const after=await app.snapshot();expect(after).toHaveLength(app.initialPersisted.length);const saved=after.find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===101);expect(saved[kind==='Category'?'label':kind==='Import Map'?'key_name':'title']).toBe('persisted-after-audit-failure');await audit.record('partial-save-readback',after);return;
  82  |    }
  83  |    if(text.includes('has received the error response')){expect(app.lastMutation()?.status).toBeGreaterThanOrEqual(400);return;}
  84  |    if(text.startsWith('Admin A reloads')){await page.reload();await expect(app.ui.grid).toBeVisible();if(kind==='Tile')await app.ui.selectCategory('category-a');return;}
  85  |    if(text.includes('contains exactly one row with "Record Id" equal to "101"')){await expect(app.ui.row('101')).toHaveCount(1);return;}
  86  |    if(text.includes('that row displays the values returned by the persisted-record readback')){const row=(await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===101);await expect(await app.cell(kind==='Category'?'Category Label':kind==='Import Map'?'Module Name':'Tile Name','101')).toHaveText(row[kind==='Category'?'label':kind==='Import Map'?'key_name':'title']);return;}
  87  |    if(text.includes('no additional create request after the reload')){expect(app.requests.filter(x=>x.operation==='create')).toHaveLength(app.initialCreateCount);return;}
  88  |    if(text.startsWith('Category 101 is inactive')||text.startsWith('Import Map 201 is inactive')){const category=text.startsWith('Category');const rows=await app.sql([`SELECT is_active FROM post_trade_portal_service.${category?'application_category':'import_map'} WHERE ${category?'application_category_id=101':'import_map_id=201'}`]);expect(rows.results[0].rows).toEqual([{is_active:false}]);await audit.record('inactive-reference',rows);return;}
  89  |    if(text.startsWith('Tile 301 has')){const row=(await app.snapshot()).find(row=>row.application_tile_id===301);expect(row.image_light_theme).toBe('light-a.png');expect(row.image_dark_theme).toBe('dark-a.png');return;}
  90  |    if(text.startsWith('its completed maker update creates audit row')){await app.sql(['ALTER SEQUENCE post_trade_portal_service.application_tile_audit_seq RESTART WITH 5001']);await app.directUpdate('admin-a','maker',{},301);const rows=await app.sql(['SELECT * FROM post_trade_portal_service.application_tile_audit WHERE application_tile_audit_id=5001']);await audit.record('actual-generated-tile-audit',rows);expect(rows.results[0].rows).toHaveLength(1);return;}
  91  |    if((match=/^the cell under "Image URL for (Light|Dark) Theme" equals "([^"]+)" in audit row "(\d+)"/.exec(text))){
  92  |     const dialog=app.ui.auditDialog();const maximize=dialog.getByRole('button',{name:'resize',exact:true,includeHidden:true});
> 93  |     if(await maximize.getAttribute('aria-pressed')==='false')await maximize.click();
      |                       ^ Error: locator.getAttribute: Error: strict mode violation: locator('[role="tabpanel"]:visible').locator('[role="dialog"]').filter({ has: getByText('Audit', { exact: true }) }).getByRole('button', { name: 'resize', exact: true, includeHidden: true }) resolved to 2 elements:
  94  |     const grid=dialog.getByRole('grid',{includeHidden:true});const scroller=grid.locator('.MuiDataGrid-virtualScroller');
  95  |     await scroller.evaluate(node=>{node.scrollLeft=0;});await expect(grid.locator(`[data-id="${match[3]}"] [data-field="id"]`)).toHaveText(match[3]);
  96  |     await audit.capture('audit-row-identity',`Actual audit row ${match[3]} before scrolling to the theme column.`,text);
  97  |     const property=`image${match[1]}Theme`;const target=grid.locator(`[data-id="${match[3]}"] [data-field="${property}"]`);
  98  |     for(let i=0;i<20 && !await target.count();i++){await scroller.evaluate(node=>{node.scrollLeft+=400;});await page.waitForTimeout(30);}
  99  |     await target.scrollIntoViewIfNeeded();await expect(target).toBeVisible();
  100 |     const header=grid.locator(`[role="columnheader"][data-field="${property}"]`);await header.hover();
  101 |     await expect(page.getByRole('tooltip',{includeHidden:true})).toHaveText(`Image URL for ${match[1]} Theme`);
  102 |     await expect(target).toHaveText(match[2]);return;
  103 |    }
  104 |    throw new Error(`Missing exact BFF UI binding at ${id} step${step.number}: ${text}`);
  105 |   });
  106 |  });
  107 | }
  108 | 
```