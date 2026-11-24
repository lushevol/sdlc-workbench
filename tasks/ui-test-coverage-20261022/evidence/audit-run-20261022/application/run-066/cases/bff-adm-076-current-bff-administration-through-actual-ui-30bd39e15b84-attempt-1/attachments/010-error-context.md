# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: bff-admin.spec.ts >> BFF-ADM-076 current BFF administration through actual UI
- Location: e2e/audit-specs/bff-admin.spec.ts:11:2

# Error details

```
Error: expect(received).toEqual(expected) // deep equality

- Expected  - 4
+ Received  + 0

  Array [
    Object {
-     "ems2_role": "FMO_ADMIN",
-     "import_map_id": 201,
-   },
-   Object {
      "ems2_role": "OTHER_ADMIN",
      "import_map_id": 202,
    },
  ]
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
        - generic [ref=e27]: 06:26 UTC
        - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
      - button "User Profiles" [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button "Share Feedback" [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist "workspaces" [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region "Import Map" [ref=e48]:
          - textbox "Workspace Name" [ref=e52]: Import Map
          - button "refresh" [ref=e53]
      - button "Add Workspace" [ref=e57] [cursor=pointer]
    - tabpanel [ref=e62]:
      - generic [ref=e65]:
        - button "Create New Import Map" [ref=e66] [cursor=pointer]
        - grid [ref=e68]:
          - button "Export" [ref=e70] [cursor=pointer]
          - generic [ref=e74]:
            - rowgroup [ref=e75]:
              - row [ref=e76]:
                - columnheader "Actions" [ref=e77]
                - columnheader "Module Name" [ref=e80] [cursor=pointer]
                - columnheader "Path" [ref=e83] [cursor=pointer]
                - columnheader "Owner" [ref=e86] [cursor=pointer]
                - columnheader "Verified?" [ref=e89] [cursor=pointer]
                - columnheader "Updated At" [ref=e92] [cursor=pointer]
                - columnheader "Updated By" [ref=e95] [cursor=pointer]
                - columnheader "Record Id" [ref=e98] [cursor=pointer]
            - rowgroup [ref=e101]:
              - row [ref=e102]:
                - cell [ref=e103]:
                  - menu [ref=e104]:
                    - menuitem "Edit" [ref=e105] [cursor=pointer]
                    - menuitem "Verify" [ref=e108] [cursor=pointer]
                    - menuitem "Deactivate" [disabled]
                    - menuitem "Audit" [ref=e111] [cursor=pointer]
                - cell "container-076" [ref=e114]
                - cell "https://fixture.example/case-076.js" [ref=e115]
                - cell "FMO_ADMIN" [ref=e116]
                - cell [ref=e117]
                - cell "Oct 22, 2026, 12:00:00 AM" [ref=e120]
                - cell "admin-a" [ref=e122]
                - cell "301" [ref=e123]
              - row [ref=e124]:
                - cell [ref=e125]:
                  - menu [ref=e126]:
                    - menuitem "Edit" [ref=e127] [cursor=pointer]
                    - menuitem "Verify" [disabled]
                    - menuitem "Deactivate" [ref=e130] [cursor=pointer]
                    - menuitem "Audit" [ref=e133] [cursor=pointer]
                - cell "base" [ref=e136]
                - cell "http://localhost:8122/base.js" [ref=e137]
                - cell "FMO_ADMIN" [ref=e138]
                - cell [ref=e139]
                - cell "Oct 22, 2026, 12:00:00 AM" [ref=e142]
                - cell "admin-a" [ref=e144]
                - cell "9901" [ref=e145]
          - generic [ref=e148]:
            - paragraph [ref=e149]: "Rows per page:"
            - generic [ref=e150]:
              - 'combobox "Rows per page: 20" [ref=e151] [cursor=pointer]': "20"
              - textbox [aria-hidden]: "20"
            - paragraph [ref=e152]: 1–2 of 2
            - generic [ref=e153]:
              - button "Go to previous page" [disabled]
              - button "Go to next page" [disabled]
```

# Test source

```ts
  1   | import { test, expect } from '../support/audit-fixture.js';
  2   | import { BffAdminApp, currentBff, resourceFor, keyFor } from '../support/bff-admin-app.js';
  3   | import type { AdminKind } from '../support/admin-app.js';
  4   | import { localPrefix } from '../support/local-app.js';
  5   | 
  6   | // These cases share only this disposable database. Run this file with one worker.
  7   | test.describe.configure({mode:'default'});
  8   | test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',auditFixture:'Actual current React and exact-current BFF admin controllers/services/JPA with actual migration DDL in disposable PostgreSQL. Controlled OUD/EMS2 identities and local Spring bootstrap. Fixture SQL seeds/mutates isolated records; service errors are actual database errors. Undefined agreed messages remain unresolved acceptance.'});
  9   | for(let n=1;n<=97;n++){
  10  |  const id=`BFF-ADM-${String(n).padStart(3,'0')}`;
  11  |  test(`${id} current BFF administration through actual UI`,async({page,audit},testInfo)=>{
  12  |   test.setTimeout(90000);
  13  |   const steps=await audit.defineCase(id);const all=steps.map(s=>s.text).join('\n');
  14  |   const kind:AdminKind=/controlled (Category|Import Map|Tile) fixture/.exec(all)?.[1] as AdminKind ?? 'Category';
  15  |   const app=new BffAdminApp(page,kind,id,steps,audit);let match:RegExpExecArray|null;let creationClock=false;
  16  |   const field=(name:string)=>name==='Record Id'?keyFor(kind):name==='Category Label'?'label':name==='Module Name'?'keyName':name==='Tile Name'?'title':name==='Path'?'path':name==='Module Path'?'module':name==='Tile Path'?'tile':name==='Entry Name'?'entryName':'ems2Entities';
  17  |   if(all.includes('agreed'))testInfo.annotations.push({type:'audit-limit',description:'Undefined agreed error-message or policy contract. Execution is a proposed probe, not approved business acceptance.'});
  18  |   for(const step of steps)await audit.step(step.number,async()=>{
  19  |    const text=step.text;
  20  |    if(step.number===1){await app.setup();return;}
  21  |    if(/controlled (Category|Import Map|Tile) fixture records/.test(text)){await app.remember();return;}
  22  |    if(text.includes('controlled creation clock')){creationClock=true;await audit.record('creation-clock',{milliseconds:1700000000000,scope:'Only the Create New event uses the fixed date. Authentication and session clocks remain native.'});return;}
  23  |    if((match=/^the baseline fixture data defines "([^"]+)" as "(.*)"$/.exec(text))){
  24  |     expect(app.baseline[match[1]]).toBe(match[2]);
  25  |     if(!all.includes('controlled creation clock')){
  26  |      const row=(await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===Number(/grid has record "(\d+)"/.exec(all)?.[1]??101));
  27  |      if(row){const property=match[1]==='Filter Rule'?'filter_rule':field(match[1]).replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`);const expected=all.includes(`originally loaded "${match[1]}"`)?'OLD':match[2];expect(row[property]).toBe(property==='filter_rule'&&expected===''?null:expected);}
  28  |     }
  29  |     await audit.record(`fixture-step-${step.number}`,{definition:text,inputDefault:app.baseline[match[1]],persisted:await app.snapshot(),limit:'Baseline input defaults are distinct from pre-existing records. Empty Filter Rule input and normalized SQL null remain separate representations.'});return;
  30  |    }
  31  |    if(text.startsWith('the baseline Tile references')){const rows=await app.snapshot();const tile=rows.find(row=>Number(row.application_tile_id)!==9902);if(tile){expect(tile.application_category_id).toBe(101);expect(tile.import_map_id).toBe(201);}await audit.record(`fixture-step-${step.number}`,{definition:text,expectedCategoryId:101,expectedImportMapId:201,existingTile:tile??null});return;}
  32  |    if(text.startsWith('Category 101 has label')||text.startsWith('both references belong')){
  33  |     const snapshot=await app.sql(['SELECT application_category_id,label,ems2_role FROM post_trade_portal_service.application_category WHERE application_category_id=101','SELECT import_map_id,key_name,ems2_role FROM post_trade_portal_service.import_map WHERE import_map_id=201']);
  34  |     expect(snapshot.results[0].rows).toEqual([{application_category_id:101,label:'category-a',ems2_role:'FMO_ADMIN'}]);
  35  |     expect(snapshot.results[1].rows).toEqual([{import_map_id:201,key_name:'container-a',ems2_role:'FMO_ADMIN'}]);
  36  |     if(text.startsWith('both references belong'))await expect(app.ui.category).toHaveValue('category-a');
  37  |     await audit.record(`reference-snapshot-${step.number}`,snapshot);return;
  38  |    }
  39  |    if(/prepared database uses the inspected migration DDL/.test(text)){const schema=await app.sql(["SELECT table_name,column_name,data_type,character_maximum_length FROM information_schema.columns WHERE table_schema='post_trade_portal_service' ORDER BY table_name,ordinal_position"]);await audit.record('actual-migration-schema',schema);return;}
  40  |    if(text.startsWith('the controlled BFF configuration')){await app.fixture('seed',{creationEnabled:false});return;}
  41  |    if(text.startsWith('the next BFF repository save')){await app.fixture('seed',{failure:`${app.resource}-save`});return;}
  42  |    if((match=/^Admin [ABCS] clicks the button labeled "([^"]+)"/.exec(text))){if(match[1].startsWith('Create New')){const nativeNow=Date.now();if(creationClock)await page.clock.setFixedTime(new Date(1700000000000));await app.ui.panel.getByRole('button',{name:match[1],exact:true}).click();if(creationClock)await page.clock.setFixedTime(new Date(nativeNow));}else {const row= /row with "Record Id" "(\d+)"/.exec(text)?.[1];if(row){await app.ui.reveal('actions',row);await app.ui.action(match[1],row).click();}else await app.clickFooter(match[1]);}return;}
  43  |    if((match=/^the dialog titled "([^"]+)" (is visible|remains visible)/.exec(text))){await expect(app.ui.dialog()).toBeVisible();await expect(app.ui.dialog()).toContainText(match[1]);return;}
  44  |    if((match=/^Admin [ABCS] fills the (?:textbox|textarea) labeled "([^"]+)" with exactly (\d+) ASCII "a" characters/.exec(text))){await app.fill(match[1],'a'.repeat(Number(match[2])));return;}
  45  |    if((match=/^Admin [ABCS] fills the (?:textbox|textarea) labeled "([^"]+)" with "(.*)" in dialog/.exec(text))){await app.fill(match[1],match[2].replaceAll('\\"','"').replaceAll('\\t','\t'));return;}
  46  |    if((match=/^Admin [ABCS] clicks the combobox labeled "([^"]+)"/.exec(text))){await app.ui.field(match[1],'combobox').click();return;}
  47  |    if((match=/^Admin [ABCS] clicks the option labeled "([^"]+)"/.exec(text))){await page.getByRole('option',{includeHidden:true}).filter({hasText:new RegExp(`^${match[1].replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}$`)}).click();await expect(app.ui.field('Container','combobox')).toHaveValue(match[1]);await page.waitForTimeout(350);return;}
  48  |    if((match=/^the alert with severity "error".*contains the exact text "(.*)"$/.exec(text))){await app.errorAlert(match[1]);return;}
  49  |    if(text.startsWith('the alert with severity "error"')){const response=app.lastMutation();await audit.record('rejection-or-policy-observation',response);await app.errorAlert(text.includes('captured rejection')?response?.response.errorMessage:undefined);return;}
  50  |    if(/row identifiers and loaded field values equal/.test(text)){await app.assertUnchanged();return;}
  51  |    if((match=/contains exactly one existing row with value "([^"]+)"/.exec(text))){const key=field(kind==='Category'?'Category Label':'Module Name');await expect(app.ui.grid.locator(`[data-field="${key}"]`).filter({hasText:new RegExp(`^${match[1]}$`)})).toHaveCount(1);expect((await app.snapshot()).filter(row=>row[key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]===match![1])).toHaveLength(1);return;}
  52  |    if(text.includes('contains exactly one row with the create response Record Id')){const response=app.lastMutation();expect(response?.status).toBe(200);const row=String(response?.response.data[app.key]);await expect(app.ui.row(row)).toHaveCount(1);return;}
  53  |    if((match=/its "([^"]+)" cell equals the submitted value without truncation/.exec(text))){const row=String(app.lastMutation()?.response.data[app.key]);await expect(await app.cell(match[1],row)).toHaveText(app.lastSubmitted[match[1]]);return;}
  54  |    if((match=/independent persisted-record readback contains exactly (\d+) ASCII "a" characters in "([^"]+)"/.exec(text))){const rows=await app.snapshot();const row=rows.find(row=>String(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===String(app.lastMutation()?.response.data[app.key]));expect(row[field(match[2]).replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]).toBe('a'.repeat(Number(match[1])));return;}
  55  |    if(/grid has record/.test(text)){const id=/record "(\d+)"/.exec(text)![1];const row=(await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===Number(id));expect(row?.ems2_role).toBe('FMO_ADMIN');await expect(app.ui.row(id)).toBeVisible();return;}
  56  |    if(/record "\d+" is inactive/.test(text)){expect((await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===Number(/record "(\d+)"/.exec(text)?.[1]))?.is_active).toBe(false);return;}
  57  |    if((match=/^its stored "updatedBy" value is "([^"]+)"/.exec(text))){expect((await app.snapshot())[0].updated_by).toBe(match[1]);return;}
  58  |    if(/originally loaded/.test(text)){expect((await app.snapshot())[0][kind==='Category'?'label':kind==='Import Map'?'key_name':'title']).toBe('OLD');return;}
  59  |    if(/^an existing|record "102" already/.test(text)){const rows=await app.snapshot();const expected=text.includes('"react"')?'react':'shared-a';const property=kind==='Category'?'label':'key_name';const matches=rows.filter(row=>row[property]===expected);expect(matches).toHaveLength(1);expect(matches[0][app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]).toBe(102);expect(matches[0].ems2_role).toBe('FMO_ADMIN');await audit.record('existing-duplicate-fixture',rows);return;}
  60  |    if(text.startsWith('the controlled database event changes')){await app.mutate({ems2_role:'OTHER_ADMIN'});return;}
  61  |    if(text.startsWith('the controlled stale grid exposes')){await expect(app.ui.row('901')).toBeVisible();await audit.record('stale-grid-contract',{definition:text,limit:'Only the declared stale grid data response includes the actual seeded foreign record. The audit request executes the actual BFF authorization.'});return;}
  62  |    if(text.startsWith('no cell in dialog "Audit"')){await expect(app.ui.auditDialog()).not.toContainText('PROTECTED-FOREIGN');return;}
  63  |    if((match=/^the controlled database event removes (Category|Import Map) (\d+)/.exec(text))){await app.sql([`DELETE FROM post_trade_portal_service.${match[1]==='Category'?'application_category':'import_map'} WHERE ${match[1]==='Category'?'application_category_id':'import_map_id'}=${match[2]}`]);return;}
  64  |    if((match=/Admin B completes a controlled concurrent update setting "([^"]+)" to "NEW"/.exec(text))){await app.directUpdate('admin-b','maker',{[field(match[1])]:'NEW'});return;}
  65  |    if(text.startsWith('Admin A completes a controlled maker update')){await app.directUpdate('admin-a','maker',{[field(kind==='Category'?'Category Label':kind==='Import Map'?'Module Name':'Tile Name')]:'NEW'});return;}
  66  |    if(text.startsWith('Admin B completes a controlled verification')){await app.directUpdate('admin-b','checker');return;}
  67  |    if(text.includes('persisted-record readback')&&text.includes('"active" equal to false')){const rows=await app.snapshot();expect(rows[0].is_active).toBe(false);return;}
  68  |    if(text.includes('status tooltip "Unverified or Deactivated"')){const row=/record "(\d+)"/.exec(text)?.[1]??'101';const cell=await app.ui.reveal('active',row);await expect(cell.getByTestId('DangerousIcon')).toBeVisible();await cell.hover();await expect(page.getByRole('tooltip',{name:'Unverified or Deactivated',exact:true})).toBeVisible();return;}
  69  |    if(text.includes('independent persisted-record readback retains the concurrent result')){const rows=await app.snapshot();if(text.endsWith('"active"'))expect(rows[0].is_active).toBe(true);else expect(rows[0][kind==='Category'?'label':kind==='Import Map'?'key_name':'title']).toBe('NEW');return;}
  70  |    if(text.startsWith('a subsequent')){const response=await page.request.post(`${currentBff}/v1/fmo/admin/${app.resource}/data`,{headers:{'single-ui-authorization':app.access},data:{entitlementsToken:app.entitlements}});expect(response.ok()).toBe(true);const payload=await response.json();await audit.record('independent-data-response',payload);const persisted=(await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===101);const record=payload.data.find((row:any)=>Number(row[app.key])===101);const changed=kind==='Category'?'label':kind==='Import Map'?'keyName':'title';expect(record[changed]).toBe(persisted[changed.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]);expect(new Date(record.updatedAt).getTime()).toBe(new Date(persisted.updated_at).getTime());return;}
  71  |    if(text.endsWith('entitlement')){expect(app.roles).not.toContain('OTHER_ADMIN');await audit.record(`fixture-step-${step.number}`,{definition:text,actualRoles:app.roles});return;}
> 72  |    if(text.startsWith('reference "')){const id=Number(/reference "(\d+)"/.exec(text)![1]);const table=id===102?'application_category':'import_map';const key=id===102?'application_category_id':'import_map_id';const rows=await app.sql([`SELECT ${key},ems2_role FROM post_trade_portal_service.${table} WHERE ${key} IN (${id},${id===102?101:201}) ORDER BY ${key}`]);expect(rows.results[0].rows).toEqual([{[key]:id===102?101:201,ems2_role:'FMO_ADMIN'},{[key]:id,ems2_role:'OTHER_ADMIN'}]);await audit.record(`fixture-step-${step.number}`,{definition:text,actual:rows});return;}
      |                                                                                                                                                                                                                                                                                                                                                                                                        ^ Error: expect(received).toEqual(expected) // deep equality
  73  |    if(text.startsWith('the installed request interceptor')){await audit.record(`fixture-step-${step.number}`,{definition:text,limit:'The declared substitution is checked on the actual UI-originated request before forwarding.'});return;}
  74  |    if(text.startsWith('the active-import-map response')){const response=await page.request.get(`${currentBff}/v1/fmo/admin/importmap/active`);const result=await response.json();await audit.record('active-import-map-response',result);if(text.includes('unsafe Path'))expect(Object.values(result.imports)).not.toContain(app.lastSubmitted.Path);else expect(result.imports.react).toBe('https://fixture.example/initial.js');return;}
  75  |    if(text.startsWith('the persisted Tile record equals')){expect(await app.snapshot()).toEqual(app.initialPersisted);return;}
  76  |    if(text.includes('grid row "301" retains')){await expect(await app.cell('Aplication Category Record Id','301')).toHaveText('101');await expect(await app.cell('Container Record Id','301')).toHaveText('201');return;}
  77  |    if(text.includes('primary save persists record 101')){
  78  |     await app.fixture('seed',{failure:`${app.resource}-audit`});
  79  |     // The canonical setup specifies an already completed write. Execute its actual UI request before the reload action.
  80  |     await app.ui.action('Edit','101').click();
  81  |     for(const [name,value] of Object.entries(kind==='Category'?{'Category Label':'persisted-after-audit-failure'}:kind==='Import Map'?{'Module Name':'persisted-after-audit-failure','Path':'https://fixture.example/failed-audit.js'}:{'Tile Name':'persisted-after-audit-failure','Module Path':'/fixture','Tile Path':'/failed-audit','Role Entities':'E-TRADE'}))await app.fill(name,value);
  82  |     await app.clickFooter('Update');app.initialCreateCount=app.requests.filter(x=>x.operation==='create').length;expect(app.lastMutation()?.status).toBeGreaterThanOrEqual(400);const after=await app.snapshot();expect(after).toHaveLength(app.initialPersisted.length);const saved=after.find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===101);expect(saved[kind==='Category'?'label':kind==='Import Map'?'key_name':'title']).toBe('persisted-after-audit-failure');await audit.record('partial-save-readback',after);return;
  83  |    }
  84  |    if(text.includes('has received the error response')){expect(app.lastMutation()?.status).toBeGreaterThanOrEqual(400);return;}
  85  |    if(text.startsWith('Admin A reloads')){await page.reload();await expect(app.ui.grid).toBeVisible();if(kind==='Tile')await app.ui.selectCategory('category-a');return;}
  86  |    if(text.includes('contains exactly one row with "Record Id" equal to "101"')){await expect(app.ui.row('101')).toHaveCount(1);return;}
  87  |    if(text.includes('that row displays the values returned by the persisted-record readback')){const row=(await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===101);await expect(await app.cell(kind==='Category'?'Category Label':kind==='Import Map'?'Module Name':'Tile Name','101')).toHaveText(row[kind==='Category'?'label':kind==='Import Map'?'key_name':'title']);return;}
  88  |    if(text.includes('no additional create request after the reload')){expect(app.requests.filter(x=>x.operation==='create')).toHaveLength(app.initialCreateCount);return;}
  89  |    if(text.startsWith('Category 101 is inactive')||text.startsWith('Import Map 201 is inactive')){const category=text.startsWith('Category');const rows=await app.sql([`SELECT is_active FROM post_trade_portal_service.${category?'application_category':'import_map'} WHERE ${category?'application_category_id=101':'import_map_id=201'}`]);expect(rows.results[0].rows).toEqual([{is_active:false}]);await audit.record('inactive-reference',rows);return;}
  90  |    if(text.startsWith('Tile 301 has')){const row=(await app.snapshot()).find(row=>row.application_tile_id===301);expect(row.image_light_theme).toBe('light-a.png');expect(row.image_dark_theme).toBe('dark-a.png');return;}
  91  |    if(text.startsWith('its completed maker update creates audit row')){await app.sql(['ALTER SEQUENCE post_trade_portal_service.application_tile_audit_seq RESTART WITH 5001']);await app.directUpdate('admin-a','maker',{},301);const rows=await app.sql(['SELECT * FROM post_trade_portal_service.application_tile_audit WHERE application_tile_audit_id=5001']);await audit.record('actual-generated-tile-audit',rows);expect(rows.results[0].rows).toHaveLength(1);return;}
  92  |    if((match=/^the cell under "Image URL for (Light|Dark) Theme" equals "([^"]+)" in audit row "(\d+)"/.exec(text))){
  93  |     const dialog=app.ui.auditDialog();const maximize=dialog.getByTestId(`${localPrefix}_Dialog-maximize`);
  94  |     if(await maximize.getAttribute('aria-pressed')==='false')await maximize.click();
  95  |     const grid=dialog.getByRole('grid',{includeHidden:true});const scroller=grid.locator('.MuiDataGrid-virtualScroller');
  96  |     await scroller.evaluate(node=>{node.scrollLeft=0;});await expect(grid.locator(`[data-id="${match[3]}"] [data-field="id"]`)).toHaveText(match[3]);
  97  |     await audit.capture('audit-row-identity',`Actual audit row ${match[3]} before scrolling to the theme column.`,text);
  98  |     const property=`image${match[1]}Theme`;const target=grid.locator(`[data-id="${match[3]}"] [data-field="${property}"]`);
  99  |     for(let i=0;i<20 && !await target.count();i++){await scroller.evaluate(node=>{node.scrollLeft+=400;});await page.waitForTimeout(30);}
  100 |     await target.scrollIntoViewIfNeeded();await expect(target).toBeVisible();
  101 |     const header=grid.locator(`[role="columnheader"][data-field="${property}"]`);await header.scrollIntoViewIfNeeded();
  102 |     await header.locator('.MuiDataGrid-columnHeaderTitle').hover();
  103 |     await expect(page.getByRole('tooltip',{includeHidden:true})).toHaveText(`Image URL for ${match[1]} Theme`);
  104 |     await expect(target).toHaveText(match[2]);return;
  105 |    }
  106 |    throw new Error(`Missing exact BFF UI binding at ${id} step${step.number}: ${text}`);
  107 |   });
  108 |  });
  109 | }
  110 | 
```