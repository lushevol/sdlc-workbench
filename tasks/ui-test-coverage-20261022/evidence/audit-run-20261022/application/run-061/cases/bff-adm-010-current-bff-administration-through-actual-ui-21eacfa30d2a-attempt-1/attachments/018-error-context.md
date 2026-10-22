# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: bff-admin.spec.ts >> BFF-ADM-010 current BFF administration through actual UI
- Location: e2e/audit-specs/bff-admin.spec.ts:10:2

# Error details

```
TimeoutError: locator.click: Timeout 8000ms exceeded.
Call log:
  - waiting for getByRole('option', { name: 'container-a', exact: true, includeHidden: true })

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
      - generic [ref=e27]: 05:52 UTC
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
                    - cell [ref=e130]: tile-010
                    - cell [ref=e131]: Fixture tile
                    - cell [ref=e132]: dark-a.png
                    - cell [ref=e133]: light-a.png
                    - cell [ref=e134]: container-a
                    - cell [ref=e135]: /fixture
                    - cell [ref=e136]: /case-010
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
                  - generic [ref=e152]: "new ID: 1700000000000"
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
                - generic [ref=e173]:
                  - generic [ref=e174]: Description
                  - textbox [ref=e176]:
                    - /placeholder: Type here
                - generic [ref=e178]:
                  - generic [ref=e179]: Image URL for Dark Theme
                  - generic [ref=e180]:
                    - combobox [ref=e181]
                    - button [ref=e183] [cursor=pointer]
                - generic [ref=e187]:
                  - generic [ref=e188]: Image URL for Light Theme
                  - generic [ref=e189]:
                    - combobox [ref=e190]
                    - button [ref=e192] [cursor=pointer]
                - generic [ref=e195]:
                  - generic [ref=e196]:
                    - generic [ref=e197]: Container
                    - generic [ref=e198]:
                      - combobox [expanded] [active] [ref=e199]
                      - button [ref=e201] [cursor=pointer]
                  - listbox "Container" [ref=e204]:
                    - option "container-a" [ref=e205] [cursor=pointer]
                    - option "base" [ref=e206] [cursor=pointer]
                - generic [ref=e207]:
                  - generic [ref=e208]: Module Path
                  - textbox [ref=e210]:
                    - /placeholder: Type here
                - generic [ref=e211]:
                  - generic [ref=e212]: Tile Path
                  - textbox [ref=e214]:
                    - /placeholder: Type here
                - generic [ref=e215]:
                  - generic [ref=e216]: Role Subject
                  - textbox [ref=e218]:
                    - /placeholder: Type here
                - generic [ref=e219]:
                  - generic [ref=e220]: Role Entities
                  - textbox [ref=e222]:
                    - /placeholder: Type here
                - generic [ref=e223]:
                  - generic: Is Template?
                  - generic [ref=e224]:
                    - combobox [ref=e225] [cursor=pointer]
                    - textbox [aria-hidden]
                - generic [ref=e226]:
                  - generic [ref=e227]: Email Support
                  - textbox [ref=e229]:
                    - /placeholder: Type here
                - generic [ref=e230]:
                  - generic [ref=e231]: Owner
                  - textbox [disabled] [ref=e233]:
                    - /placeholder: Type here
                    - text: FMO_ADMIN
                - generic [ref=e234]:
                  - generic [ref=e235]: Verified?
                  - textbox [disabled] [ref=e237]:
                    - /placeholder: Type here
                    - text: "false"
                - generic [ref=e238]:
                  - generic [ref=e239]: Created At
                  - textbox [disabled] [ref=e241]:
                    - /placeholder: Type here
                    - text: 2023-11-14T22:13:20.000Z
                - generic [ref=e242]:
                  - generic [ref=e243]: Created By
                  - textbox [disabled] [ref=e245]:
                    - /placeholder: Type here
                    - text: admin-a
                - generic [ref=e246]:
                  - generic [ref=e247]: Updated At
                  - textbox [disabled] [ref=e249]:
                    - /placeholder: Type here
                    - text: 2023-11-14T22:13:20.000Z
                - generic [ref=e250]:
                  - generic [ref=e251]: Updated By
                  - textbox [disabled] [ref=e253]:
                    - /placeholder: Type here
                    - text: admin-a
                - generic [ref=e254]:
                  - generic [ref=e255]: Record Id
                  - textbox [disabled] [ref=e257]:
                    - /placeholder: <<will be auto generated>>
                - generic [ref=e258]:
                  - generic [ref=e259]: Aplication Category Record Id
                  - textbox [disabled] [ref=e261]:
                    - /placeholder: <<will be auto generated>>
                    - text: "101"
                - generic [ref=e262]:
                  - generic [ref=e263]: Container Record Id
                  - textbox [disabled] [ref=e265]:
                    - /placeholder: <<will be auto generated>>
                - generic [ref=e266]:
                  - generic [ref=e267]: Order No
                  - spinbutton [ref=e269]
                - generic [ref=e270]:
                  - generic [ref=e271]: Filter Rule
                  - textbox [ref=e273]:
                    - /placeholder: Type here
                - generic [ref=e274]:
                  - generic [ref=e275]: Entry Name
                  - textbox [ref=e277]:
                    - /placeholder: Type here
              - generic [ref=e278]:
                - button [ref=e279] [cursor=pointer]: Create
                - button [ref=e280] [cursor=pointer]: Reset
                - button [ref=e281] [cursor=pointer]: Close
              - button [ref=e282]
```

# Test source

```ts
  1  | import { test, expect } from '../support/audit-fixture.js';
  2  | import { BffAdminApp, currentBff, resourceFor, keyFor } from '../support/bff-admin-app.js';
  3  | import type { AdminKind } from '../support/admin-app.js';
  4  | 
  5  | // These cases share only this disposable database. Run this file with one worker.
  6  | test.describe.configure({mode:'default'});
  7  | test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',auditFixture:'Actual current React and exact-current BFF admin controllers/services/JPA with actual migration DDL in disposable PostgreSQL. Controlled OUD/EMS2 identities and local Spring bootstrap. Fixture SQL seeds/mutates isolated records; service errors are actual database errors. Undefined agreed messages remain unresolved acceptance.'});
  8  | for(let n=1;n<=97;n++){
  9  |  const id=`BFF-ADM-${String(n).padStart(3,'0')}`;
  10 |  test(`${id} current BFF administration through actual UI`,async({page,audit},testInfo)=>{
  11 |   test.setTimeout(90000);
  12 |   const steps=await audit.defineCase(id);const all=steps.map(s=>s.text).join('\n');
  13 |   const kind:AdminKind=/controlled (Category|Import Map|Tile) fixture/.exec(all)?.[1] as AdminKind ?? 'Category';
  14 |   const app=new BffAdminApp(page,kind,id,steps,audit);let match:RegExpExecArray|null;let creationClock=false;
  15 |   const field=(name:string)=>name==='Record Id'?keyFor(kind):name==='Category Label'?'label':name==='Module Name'?'keyName':name==='Tile Name'?'title':name==='Path'?'path':name==='Module Path'?'module':name==='Tile Path'?'tile':name==='Entry Name'?'entryName':'ems2Entities';
  16 |   if(all.includes('agreed'))testInfo.annotations.push({type:'audit-limit',description:'Undefined agreed error-message or policy contract. Execution is a proposed probe, not approved business acceptance.'});
  17 |   for(const step of steps)await audit.step(step.number,async()=>{
  18 |    const text=step.text;
  19 |    if(step.number===1){await app.setup();return;}
  20 |    if(/controlled (Category|Import Map|Tile) fixture records/.test(text)){await app.remember();return;}
  21 |    if(text.includes('controlled creation clock')){creationClock=true;await audit.record('creation-clock',{milliseconds:1700000000000,scope:'Only the Create New event uses the fixed date. Authentication and session clocks remain native.'});return;}
  22 |    if(/^the baseline fixture data defines|^the baseline Tile references|^both references belong/.test(text)){await audit.record(`fixture-step-${step.number}`,{definition:text,actual:await app.snapshot()});return;}
  23 |    if(text.startsWith('Category 101 has label')){const snapshot=await app.sql(['SELECT label FROM post_trade_portal_service.application_category WHERE application_category_id=101']);await audit.record('reference-snapshot',snapshot);return;}
  24 |    if(/prepared database uses the inspected migration DDL/.test(text)){const schema=await app.sql(["SELECT table_name,column_name,data_type,character_maximum_length FROM information_schema.columns WHERE table_schema='post_trade_portal_service' ORDER BY table_name,ordinal_position"]);await audit.record('actual-migration-schema',schema);return;}
  25 |    if(text.startsWith('the controlled BFF configuration')){await app.fixture('seed',{creationEnabled:false});return;}
  26 |    if(text.startsWith('the next BFF repository save')){await app.fixture('seed',{failure:`${app.resource}-save`});return;}
  27 |    if((match=/^Admin [ABCS] clicks the button labeled "([^"]+)"/.exec(text))){if(match[1].startsWith('Create New')){const nativeNow=Date.now();if(creationClock)await page.clock.setFixedTime(new Date(1700000000000));await app.ui.panel.getByRole('button',{name:match[1],exact:true}).click();if(creationClock)await page.clock.setFixedTime(new Date(nativeNow));}else {const row= /row with "Record Id" "(\d+)"/.exec(text)?.[1];if(row){await app.ui.reveal('actions',row);await app.ui.action(match[1],row).click();}else await app.clickFooter(match[1]);}return;}
  28 |    if((match=/^the dialog titled "([^"]+)" (is visible|remains visible)/.exec(text))){await expect(app.ui.dialog()).toBeVisible();await expect(app.ui.dialog()).toContainText(match[1]);return;}
  29 |    if((match=/^Admin [ABCS] fills the (?:textbox|textarea) labeled "([^"]+)" with exactly (\d+) ASCII "a" characters/.exec(text))){await app.fill(match[1],'a'.repeat(Number(match[2])));return;}
  30 |    if((match=/^Admin [ABCS] fills the (?:textbox|textarea) labeled "([^"]+)" with "(.*)" in dialog/.exec(text))){await app.fill(match[1],match[2].replaceAll('\\"','"').replaceAll('\\t','\t'));return;}
  31 |    if((match=/^Admin [ABCS] clicks the combobox labeled "([^"]+)"/.exec(text))){await app.ui.field(match[1],'combobox').click();return;}
> 32 |    if((match=/^Admin [ABCS] clicks the option labeled "([^"]+)"/.exec(text))){await page.getByRole('option',{name:match[1],exact:true,includeHidden:true}).click();return;}
     |                                                                                                                                                            ^ TimeoutError: locator.click: Timeout 8000ms exceeded.
  33 |    if((match=/^the alert with severity "error".*contains the exact text "(.*)"$/.exec(text))){await app.errorAlert(match[1]);return;}
  34 |    if(text.startsWith('the alert with severity "error"')){const response=app.lastMutation();await audit.record('rejection-or-policy-observation',response);await app.errorAlert(text.includes('captured rejection')?response?.response.errorMessage:undefined);return;}
  35 |    if(/row identifiers and loaded field values equal/.test(text)){await app.assertUnchanged();return;}
  36 |    if((match=/contains exactly one existing row with value "([^"]+)"/.exec(text))){const key=field(kind==='Category'?'Category Label':'Module Name');await expect(app.ui.grid.locator(`[data-field="${key}"]`).filter({hasText:new RegExp(`^${match[1]}$`)})).toHaveCount(1);expect((await app.snapshot()).filter(row=>row[key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]===match![1])).toHaveLength(1);return;}
  37 |    if(text.includes('contains exactly one row with the create response Record Id')){const response=app.lastMutation();expect(response?.status).toBe(200);const row=String(response?.response.data[app.key]);await expect(app.ui.row(row)).toHaveCount(1);return;}
  38 |    if((match=/its "([^"]+)" cell equals the submitted value without truncation/.exec(text))){const row=String(app.lastMutation()?.response.data[app.key]);await expect(await app.cell(match[1],row)).toHaveText(app.lastSubmitted[match[1]]);return;}
  39 |    if((match=/independent persisted-record readback contains exactly (\d+) ASCII "a" characters in "([^"]+)"/.exec(text))){const rows=await app.snapshot();const row=rows.find(row=>String(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===String(app.lastMutation()?.response.data[app.key]));expect(row[field(match[2]).replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)]).toBe('a'.repeat(Number(match[1])));return;}
  40 |    if(/grid has record/.test(text)){const row=/record "(\d+)"/.exec(text)?.[1];await expect(app.ui.row(row)).toBeVisible();return;}
  41 |    if(/record "\d+" is inactive/.test(text)){expect((await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===Number(/record "(\d+)"/.exec(text)?.[1]))?.is_active).toBe(false);return;}
  42 |    if((match=/^its stored "updatedBy" value is "([^"]+)"/.exec(text))){expect((await app.snapshot())[0].updated_by).toBe(match[1]);return;}
  43 |    if(/originally loaded/.test(text)){expect((await app.snapshot())[0][kind==='Category'?'label':kind==='Import Map'?'key_name':'title']).toBe('OLD');return;}
  44 |    if(/^an existing|record "102" already/.test(text)){await audit.record('existing-duplicate-fixture',await app.snapshot());return;}
  45 |    if(text.startsWith('the controlled database event changes')){await app.mutate({ems2_role:'OTHER_ADMIN'});return;}
  46 |    if(text.startsWith('the controlled stale grid exposes')){await expect(app.ui.row('901')).toBeVisible();await audit.record('stale-grid-contract',{definition:text,limit:'Only the declared stale grid data response includes the actual seeded foreign record. The audit request executes the actual BFF authorization.'});return;}
  47 |    if(text.startsWith('no cell in dialog "Audit"')){await expect(app.ui.auditDialog()).not.toContainText('PROTECTED-FOREIGN');return;}
  48 |    if((match=/^the controlled database event removes (Category|Import Map) (\d+)/.exec(text))){await app.sql([`DELETE FROM post_trade_portal_service.${match[1]==='Category'?'application_category':'import_map'} WHERE ${match[1]==='Category'?'application_category_id':'import_map_id'}=${match[2]}`]);return;}
  49 |    if((match=/Admin B completes a controlled concurrent update setting "([^"]+)" to "NEW"/.exec(text))){await app.directUpdate('admin-b','maker',{[field(match[1])]:'NEW'});return;}
  50 |    if(text.startsWith('Admin A completes a controlled maker update')){await app.directUpdate('admin-a','maker',{[field(kind==='Category'?'Category Label':kind==='Import Map'?'Module Name':'Tile Name')]:'NEW'});return;}
  51 |    if(text.startsWith('Admin B completes a controlled verification')){await app.directUpdate('admin-b','checker');return;}
  52 |    if(text.includes('persisted-record readback')&&text.includes('"active" equal to false')){const rows=await app.snapshot();expect(rows[0].is_active).toBe(false);return;}
  53 |    if(text.includes('status tooltip "Unverified or Deactivated"')){const row=/record "(\d+)"/.exec(text)?.[1]??'101';const cell=await app.ui.reveal('active',row);await expect(cell.getByTestId('DangerousIcon')).toBeVisible();await cell.hover();await expect(page.getByRole('tooltip',{name:'Unverified or Deactivated',exact:true})).toBeVisible();return;}
  54 |    if(text.includes('independent persisted-record readback retains the concurrent result')){const rows=await app.snapshot();if(text.endsWith('"active"'))expect(rows[0].is_active).toBe(true);else expect(rows[0][kind==='Category'?'label':kind==='Import Map'?'key_name':'title']).toBe('NEW');return;}
  55 |    if(text.startsWith('a subsequent')){const response=await page.request.post(`${currentBff}/v1/fmo/admin/${app.resource}/data`,{headers:{'single-ui-authorization':app.access},data:{entitlementsToken:app.entitlements}});expect(response.ok()).toBe(true);await audit.record('independent-data-response',await response.json());return;}
  56 |    if(text.startsWith('the installed request interceptor')||text.startsWith('reference "')||text.endsWith('entitlement')){await audit.record(`fixture-step-${step.number}`,{definition:text});return;}
  57 |    if(text.startsWith('the active-import-map response')){const response=await page.request.get(`${currentBff}/v1/fmo/admin/importmap/active`);const result=await response.json();await audit.record('active-import-map-response',result);if(text.includes('unsafe Path'))expect(Object.values(result.imports)).not.toContain(app.lastSubmitted.Path);else expect(result.imports.react).toBe('https://fixture.example/initial.js');return;}
  58 |    if(text.startsWith('the persisted Tile record equals')){expect(await app.snapshot()).toEqual(app.initialPersisted);return;}
  59 |    if(text.includes('grid row "301" retains')){await expect(await app.cell('Aplication Category Record Id','301')).toHaveText('101');await expect(await app.cell('Container Record Id','301')).toHaveText('201');return;}
  60 |    if(text.includes('primary save persists record 101')){
  61 |     await app.fixture('seed',{failure:`${app.resource}-audit`});
  62 |     // The canonical setup specifies an already completed write. Execute its actual UI request before the reload action.
  63 |     await app.ui.action('Edit','101').click();
  64 |     for(const [name,value] of Object.entries(kind==='Category'?{'Category Label':'persisted-after-audit-failure'}:kind==='Import Map'?{'Module Name':'persisted-after-audit-failure','Path':'https://fixture.example/failed-audit.js'}:{'Tile Name':'persisted-after-audit-failure','Module Path':'/fixture','Tile Path':'/failed-audit','Role Entities':'E-TRADE'}))await app.fill(name,value);
  65 |     await app.clickFooter('Update');app.initialCreateCount=app.requests.filter(x=>x.operation==='create').length;expect(app.lastMutation()?.status).toBeGreaterThanOrEqual(400);await audit.record('partial-save-readback',await app.snapshot());return;
  66 |    }
  67 |    if(text.includes('has received the error response')){expect(app.lastMutation()?.status).toBeGreaterThanOrEqual(400);return;}
  68 |    if(text.startsWith('Admin A reloads')){await page.reload();await expect(app.ui.grid).toBeVisible();if(kind==='Tile')await app.ui.selectCategory('category-a');return;}
  69 |    if(text.includes('contains exactly one row with "Record Id" equal to "101"')){await expect(app.ui.row('101')).toHaveCount(1);return;}
  70 |    if(text.includes('that row displays the values returned by the persisted-record readback')){const row=(await app.snapshot()).find(row=>Number(row[app.key.replace(/[A-Z]/g,c=>`_${c.toLowerCase()}`)])===101);await expect(await app.cell(kind==='Category'?'Category Label':kind==='Import Map'?'Module Name':'Tile Name','101')).toHaveText(row[kind==='Category'?'label':kind==='Import Map'?'key_name':'title']);return;}
  71 |    if(text.includes('no additional create request after the reload')){expect(app.requests.filter(x=>x.operation==='create')).toHaveLength(app.initialCreateCount);return;}
  72 |    if(text.startsWith('Category 101 is inactive')||text.startsWith('Import Map 201 is inactive')){await audit.record('inactive-reference',await app.sql([`SELECT * FROM post_trade_portal_service.${text.startsWith('Category')?'application_category':'import_map'}`]));return;}
  73 |    if(text.startsWith('Tile 301 has')){const row=(await app.snapshot()).find(row=>row.application_tile_id===301);expect(row.image_light_theme).toBe('light-a.png');expect(row.image_dark_theme).toBe('dark-a.png');return;}
  74 |    if(text.startsWith('its completed maker update creates audit row')){await app.sql(['ALTER SEQUENCE post_trade_portal_service.application_tile_audit_seq RESTART WITH 5001']);await app.directUpdate('admin-a','maker',{},301);const rows=await app.sql(['SELECT * FROM post_trade_portal_service.application_tile_audit WHERE application_tile_audit_id=5001']);await audit.record('actual-generated-tile-audit',rows);expect(rows.results[0].rows).toHaveLength(1);return;}
  75 |    if((match=/^the cell under "Image URL for (Light|Dark) Theme" equals "([^"]+)" in audit row "(\d+)"/.exec(text))){const grid=app.ui.auditDialog().getByRole('grid',{includeHidden:true});const target=grid.locator(`[data-id="${match[3]}"] [data-field="image${match[1]}Theme"]`);const scroller=grid.locator('.MuiDataGrid-virtualScroller');for(let i=0;i<20 && !await target.count();i++){await scroller.evaluate(node=>{node.scrollLeft+=400;});await page.waitForTimeout(30);}await expect(target).toHaveText(match[2]);return;}
  76 |    throw new Error(`Missing exact BFF UI binding at ${id} step${step.number}: ${text}`);
  77 |   });
  78 |  });
  79 | }
  80 | 
```