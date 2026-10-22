# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: bff-admin.spec.ts >> BFF-ADM-081 current BFF administration through actual UI
- Location: e2e/audit-specs/bff-admin.spec.ts:11:2

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
  - text: 06:47 UTC
  - checkbox "Time Switch" [checked]
- button "User Profiles": A
- button "Share Feedback"
- main:
  - tablist "workspaces":
    - tab "Tile" [selected]:
      - region "Tile":
        - textbox "Workspace Name": Tile
    - button "Add Workspace"
  - tabpanel:
    - text: Application Category
    - combobox "Application Category": category-a
    - button "Open"
    - button "refresh"
    - button "Create New Tile"
    - grid:
      - button "Export"
      - rowgroup:
        - row "Actions Tile Name Description Image URL for Dark Theme Image URL for Light Theme Container Module Path Tile Path Role Subject Role Entities":
          - columnheader "Actions"
          - columnheader "Tile Name"
          - columnheader "Description"
          - columnheader "Image URL for Dark Theme"
          - columnheader "Image URL for Light Theme"
          - columnheader "Container"
          - columnheader "Module Path"
          - columnheader "Tile Path"
          - columnheader "Role Subject"
          - columnheader "Role Entities"
      - rowgroup:
        - row "tile-081 Fixture tile dark-a.png light-a.png container-a /fixture /case-081 E-TRADE":
          - cell:
            - menu:
              - menuitem "Edit"
              - menuitem "Verify" [disabled]
              - menuitem "Deactivate"
              - menuitem "Audit"
          - cell "tile-081"
          - cell "Fixture tile"
          - cell "dark-a.png"
          - cell "light-a.png"
          - cell "container-a"
          - cell "/fixture"
          - cell "/case-081"
          - cell
          - cell "E-TRADE"
      - paragraph: "Rows per page:"
      - 'combobox "Rows per page: 20"': "20"
      - paragraph: 1–1 of 1
      - button "Go to previous page" [disabled]
      - button "Go to next page" [disabled]
```

# Test source

```ts
  66  |    staleRow={...(this.kind==='Category'?category:this.kind==='Import Map'?map:tile),[this.key]:901,ems2Role:'OTHER_ADMIN'};
  67  |    if(this.kind==='Category'){staleRow.label='PROTECTED-FOREIGN-CATEGORY';categories.push(staleRow);}
  68  |    else if(this.kind==='Import Map'){staleRow.keyName='PROTECTED-FOREIGN-MAP';importMaps.push(staleRow);}
  69  |    else {staleRow.title='PROTECTED-FOREIGN-TILE';tiles.push(staleRow);}
  70  |   }
  71  |   if(this.kind==='Category' && /existing Category record already|Category record "102" already/.test(all))categories.push({...common,applicationCategoryId:102,label:'shared-a'});
  72  |   if(this.kind==='Import Map' && /existing Import Map record already|Import Map record "102" already/.test(all))importMaps.push({...common,importMapId:102,keyName:all.includes('equal to "react"')?'react':'shared-a',path:'https://fixture.example/initial.js',active:true});
  73  |   if(all.includes('reference "102"'))categories.push({...common,applicationCategoryId:102,label:'foreign-category',ems2Role:'OTHER_ADMIN'});
  74  |   if(all.includes('reference "202"'))importMaps.push({...common,importMapId:202,keyName:'foreign-map',path:'https://fixture.example/foreign.js',ems2Role:'OTHER_ADMIN'});
  75  |   categories.push({...common,applicationCategoryId:9900,label:'Administration bootstrap',active:true});
  76  |   importMaps.push({...common,importMapId:9901,keyName:'base',path:'http://localhost:8122/base.js',active:true});
  77  |   tiles.push({...tile,applicationTileId:9902,title:this.kind,module:this.resource,tile:'',active:true,template:true,applicationCategory:{applicationCategoryId:9900},importMap:{importMapId:9901}});
  78  |   await this.fixture('reset'); await this.fixture('seed',{categories,importMaps,tiles,
  79  |    ...(staleRow?{[this.kind==='Category'?'categoryAudits':this.kind==='Import Map'?'importMapAudits':'tileAudits']:[{...staleRow,[this.kind==='Category'?'applicationCategoryAuditId':this.kind==='Import Map'?'importMapAuditId':'applicationTileAuditId']:5001,transactionMode:'maker'}]}:{})});
  80  |   await blockExternal(this.page);
  81  |   await this.page.route('**/api/auth/**',async route=>{
  82  |    const url=new URL(route.request().url());
  83  |    let body:any=route.request().method()==='POST'?route.request().postDataJSON():null;
  84  |    const parts=url.pathname.split('/'); const operation=parts.at(-1)!; const resource=parts.at(-2)!;
  85  |    const admin=url.pathname.includes('/v1/fmo/admin/');
  86  |    if(admin && ['create','update'].includes(operation)){
  87  |     if(all.includes('"applicationCategory.applicationCategoryId" as 102'))body.applicationCategory={applicationCategoryId:102};
  88  |     if(all.includes('"importMap.importMapId" as 202'))body.importMap={importMapId:202};
  89  |     if(all.includes('"importMap" as null'))body.importMap=null;
  90  |     for(const [label,value] of Object.entries(this.lastSubmitted)){
  91  |      const outbound=body[adminFields[label]];
  92  |      if(label==='Filter Rule'&&value===''){
  93  |       this.submissionChecks.push({label:'Empty Filter Rule representation',actual:outbound,allowed:[null,'']});
  94  |       await this.audit.record('empty-filter-rule-representation',{visibleInput:value,outbound,limit:'An unchanged empty input can retain its initial null. The UI string and outbound representation are recorded separately.'});
  95  |      }else this.submissionChecks.push({label:`Committed UI field ${label}`,actual:outbound,allowed:[value]});
  96  |     }
  97  |     if(all.includes('"applicationCategory.applicationCategoryId" as 102'))this.submissionChecks.push({label:'Declared category substitution',actual:body.applicationCategory?.applicationCategoryId,allowed:[102]});
  98  |     if(all.includes('"importMap.importMapId" as 202'))this.submissionChecks.push({label:'Declared import map substitution',actual:body.importMap?.importMapId,allowed:[202]});
  99  |     if(all.includes('"importMap" as null'))this.submissionChecks.push({label:'Declared null import map substitution',actual:body.importMap,allowed:[null]});
  100 |     if(this.kind==='Tile'&&all.includes('clicks the option labeled "container-a"'))this.submissionChecks.push({label:'Selected Container identifier',actual:body.importMap?.importMapId,allowed:[201]});
  101 |    }
  102 |    const response=await route.fetch({url:`${currentBff}${url.pathname.replace('/api/auth','')}${url.search}`, ...(body?{postData:body}:{})});
  103 |    let payload:any;try{payload=await response.json();}catch{payload={raw:await response.text()};}
  104 |    if(subject==='admin-s'&&admin&&operation==='data'){
  105 |     const dataKey=resource==='category'?'applicationCategoryId':resource==='importmap'?'importMapId':'applicationTileId';
  106 |     const fixtureRows=resource==='category'?categories.filter(row=>row.applicationCategoryId===101):resource==='importmap'?importMaps.filter(row=>row.importMapId===(this.kind==='Tile'?201:101)):tiles.filter(row=>row.applicationTileId===101);
  107 |     const originalData=payload.data??[];
  108 |     payload.data=[...originalData,...fixtureRows.filter(row=>!originalData.some((existing:any)=>existing[dataKey]===row[dataKey]))];
  109 |     await this.audit.record(`super-user-stale-read-${resource}`,{originalData,visibleFixtureRows:fixtureRows,scope:'The canonical Setup declares a controlled stale fixture. Only READ data exposes the actual persisted records. Signed SUPER_USER entitlements, owners, mutations and mutation responses remain actual.',limit:'This does not establish normal SUPER_USER discovery or read access.'});
  110 |     await route.fulfill({response,json:payload});
  111 |     this.requests.push({resource,operation,body:{entitlementsToken:'[SIGNED LOCAL TEST TOKEN]'},status:response.status(),response:payload});return;
  112 |    }
  113 |    if(staleRow && admin && operation==='data' && resource===this.resource) {
  114 |     payload.data=[...(payload.data??[]),staleRow];
  115 |     await route.fulfill({response,json:payload});
  116 |     this.requests.push({resource,operation,body:{entitlementsToken:'[SIGNED LOCAL TEST TOKEN]'},status:response.status(),response:payload});
  117 |     return;
  118 |    }
  119 |    if(operation==='login') {
  120 |     this.access=response.headers()['single-ui-authorization']??'';this.entitlements=payload.entitlementsToken??'';
  121 |     const accessClaims=JSON.parse(Buffer.from(this.access.replace(/^Bearer /,'').split('.')[1],'base64url').toString());
  122 |     const entitlementClaims=JSON.parse(Buffer.from(this.entitlements.split('.')[1],'base64url').toString());
  123 |     const roleMap=JSON.parse(entitlementClaims.entitlements);
  124 |     this.roles=Object.keys(roleMap).filter(key=>key.startsWith('FMO PORTAL ADMIN:')).map(key=>key.split(':')[1]);
  125 |     expect(accessClaims.sub).toBe(subject);expect(JSON.parse(payload.userInfo).sub).toBe(subject);
  126 |     expect(this.roles).toEqual([subject==='admin-s'?'SUPER_USER':'FMO_ADMIN']);
  127 |     await this.audit.record('actual-identity-projection',{subject:accessClaims.sub,issuer:accessClaims.iss,adminEntity:'FMO PORTAL ADMIN',roles:this.roles,signatureLimit:'Decoded projections do not independently verify signatures. Actual BFF calls retain authorization outcomes.'});
  128 |    }
  129 |    if(admin)this.requests.push({resource,operation,body:{...body,entitlementsToken:body?.entitlementsToken?'[SIGNED LOCAL TEST TOKEN]':undefined},status:response.status(),response:payload});
  130 |    await route.fulfill({response});
  131 |   });
  132 |   const initial={...workspace(this.kind),containers:[{id:'CURRENT-BFF-ADMIN',container:'@fm/base',module:`/${this.resource}`,tile:'/',title:this.kind,emailSupport:'support@example.test',panelId:'',tabId:'',parameters:{}}]};
  133 |   await this.page.addInitScript(value=>{if(!localStorage.getItem('SET_WORKSPACES'))localStorage.setItem('SET_WORKSPACES',JSON.stringify([value]));},initial);
  134 |   const login=await openLogin(this.page);await login.fillUsername(subject);await login.fillPassword('FixturePass1!');await login.clickSignInButton();await this.ui.portal.expectVisible();
  135 |   await expect(this.ui.grid).toBeVisible();if(this.kind==='Tile')await this.ui.selectCategory('category-a');
  136 |   await this.audit.record('baseline-inputs',{values:this.baseline,purpose:'Input defaults are separate from existing persisted records. Creation fixtures avoid accidental unique-key collisions.',storedFilterRule:tile.filterRule});
  137 |   await this.audit.record('bff-boundary',{origin:currentBff,scope:'Actual current controllers, services, signed tokens, JPA and disposable PostgreSQL. Controlled OUD/EMS2/bootstrap.',subject,role:subject==='admin-s'?'SUPER_USER':'FMO_ADMIN'});
  138 |  }
  139 |  async gridSnapshot(): Promise<unknown> {await this.ui.grid.locator('.MuiDataGrid-virtualScroller').evaluate(node=>{node.scrollLeft=0;});await expect(this.ui.grid.locator('[role="columnheader"][data-field="actions"]')).toBeVisible();await this.page.waitForTimeout(50);return this.ui.grid.locator('[data-id]').evaluateAll(rows=>rows.map(row=>({id:row.getAttribute('data-id'),values:Array.from(row.querySelectorAll('[data-field]')).filter(cell=>cell.getAttribute('data-field')!=='actions').map(cell=>[cell.getAttribute('data-field'),cell.textContent])})));}
  140 |  async remember(): Promise<void>{this.initialGrid=await this.gridSnapshot();this.initialPersisted=await this.snapshot();this.expectedPersisted=this.initialPersisted;await this.audit.record('initial-persisted-records',this.initialPersisted);}
  141 |  async fill(name:string,value:string):Promise<void>{this.lastSubmitted[name]=value;await this.ui.field(name).fill(value);await expect(this.ui.field(name)).toHaveValue(value);await this.page.waitForTimeout(350);}
  142 |  async clickFooter(name:string):Promise<void>{
  143 |   const count=this.requests.filter(request=>['create','update'].includes(request.operation)).length;
  144 |   const checkCount=this.submissionChecks.length;
  145 |   await this.ui.footerButton(name).click();
  146 |   if(['Create','Update','Verified','Deactivate'].includes(name)){
  147 |    await expect.poll(()=>this.requests.filter(request=>['create','update'].includes(request.operation)).length).toBeGreaterThan(count);
  148 |    await this.audit.record('ui-origin-bff-requests',this.requests);
  149 |    await this.audit.record('persisted-after-submit',await this.snapshot());
  150 |    const checks=this.submissionChecks.slice(checkCount);
  151 |    await this.audit.record('committed-ui-submission-comparisons',checks);
  152 |    for(const check of checks)expect(check.allowed,check.label).toContainEqual(check.actual);
  153 |   }
  154 |  }
  155 |  lastMutation(){return [...this.requests].reverse().find(x=>['create','update'].includes(x.operation));}
  156 |  async directUpdate(subject:string,mode:string,changes:Record<string,unknown>={},targetId=101):Promise<void>{
  157 |   const login=await this.page.request.post(`${currentBff}/v2/sso/login`,{data:{username:subject,password:'FixturePass1!',device:'LOCAL_UI_AUDIT'}});expect(login.ok()).toBe(true);const payload=await login.json();
  158 |   const rows:any[]=await this.snapshot(); const row=rows.find(row=>Number(row[sqlKey(this.kind)])===targetId)!;
  159 |   const base:any=Object.fromEntries(Object.entries(row).map(([name,value])=>[name.replace(/_([a-z])/g,(_,letter)=>letter.toUpperCase()),value]));
  160 |   base.active=base.isActive;delete base.isActive;
  161 |   if(this.kind==='Tile'){base.importMap={importMapId:base.importMapId};base.applicationCategory={applicationCategoryId:base.applicationCategoryId};}
  162 |   const response=await this.page.request.post(`${currentBff}/v1/fmo/admin/${this.resource}/update`,{headers:{'single-ui-authorization':login.headers()['single-ui-authorization']},data:{...base,...changes,mode,entitlementsToken:payload.entitlementsToken}});
  163 |   await this.audit.record(`concurrent-${subject}-${mode}`,{status:response.status(),response:await response.json()});expect(response.ok()).toBe(true);
  164 |  }
  165 |  async assertUnchanged():Promise<void>{expect(await this.snapshot()).toEqual(this.expectedPersisted);expect(await this.gridSnapshot()).toEqual(this.initialGrid);}
> 166 |  async errorAlert(exact?:string):Promise<void>{const alert=this.page.locator('.MuiAlert-root').filter({has:this.page.locator('.MuiAlert-message')});await expect(alert).toBeVisible();await expect(alert).toHaveClass(/MuiAlert-standardError|MuiAlert-filledError|MuiAlert-outlinedError/);if(exact)await expect(alert.locator('.MuiAlert-message')).toHaveText(exact);else {const mutation=[...this.requests].reverse().find(request=>['create','update','audit'].includes(request.operation));expect(mutation?.status).toBeGreaterThanOrEqual(400);await expect(alert.locator('.MuiAlert-message')).not.toHaveText('');await this.audit.record('undefined-message-contract',{canonical:'Agreed message is unavailable. Only real error response and visible nonempty error are characterized.',actual:await alert.innerText()});}}
      |                                                                                                                                                                         ^ Error: expect(locator).toBeVisible() failed
  167 |  async cell(name:string,id:string){return this.ui.reveal(adminFields[name]??name,id);}
  168 | }
  169 | 
```