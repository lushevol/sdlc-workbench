# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-session-expanded.spec.ts >> AUTH-075 proposed input activity renewal
- Location: e2e/audit-specs/auth-session-expanded.spec.ts:138:3

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: 0
Received: 1
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
        - generic [ref=e27]: 00:01 UTC
        - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
      - button "User Profiles" [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button "Share Feedback" [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist "workspaces" [ref=e45]:
      - tab [ref=e47] [cursor=pointer]:
        - region "WS-A" [ref=e48]:
          - textbox "Workspace Name" [ref=e52]: WS-A
          - button "delete" [ref=e53]
      - tab [selected] [ref=e56] [cursor=pointer]:
        - region "Workspace 2" [ref=e57]:
          - textbox "Workspace Name" [ref=e61]: Workspace 2
          - button "delete" [ref=e62]
      - button "Add Workspace" [active] [ref=e66] [cursor=pointer]
    - tabpanel [ref=e71]
```

# Test source

```ts
  43  | for (const [id, remaining] of [['AUTH-050',10800.001],['AUTH-051',10800],['AUTH-052',10799.999]] as const) {
  44  |   test(`${id} recovery reuse boundary`, async ({ page, audit }) => {
  45  |     await runSessionCase(page, audit, id, { accessExpires: 600, refreshExpires: remaining }, {
  46  |       4: async () => { expect((await observe(page)).now).toBe(T); },
  47  |       5: async () => { await hidden(page); }, 6: async () => { await visible(page); },
  48  |     });
  49  |   });
  50  | }
  51  | test('AUTH-053 refresh reuse uses current controlled time', async ({ page, audit }) => {
  52  |   await runSessionCase(page, audit, 'AUTH-053', { accessExpires: 600, refreshExpires: 10801 }, {
  53  |     4: async () => { await hidden(page); }, 5: async () => { await visible(page); },
  54  |     7: async () => { await page.clock.runFor(1000); }, 8: async () => { await hidden(page); }, 9: async () => { await visible(page); },
  55  |   });
  56  | });
  57  | const invalidRefresh: [string,string | undefined][] = [
  58  |   ['AUTH-054',undefined], ['AUTH-055','Bearer fixture.not-json.fixture'], ['AUTH-056',tokenPayload({ fixture: 'missing-exp' })],
  59  |   ['AUTH-057',tokenPayload({ exp: null })], ['AUTH-058',tokenPayload({ exp: '10800' })], ['AUTH-059',tokenPayload({ exp: 1e308 })],
  60  | ];
  61  | for (const [id, refreshValue] of invalidRefresh) {
  62  |   test(`${id} replacement acquisition for unusable refresh`, async ({ page, audit }) => {
  63  |     const replacement = sessionToken(13524, 'replacement');
  64  |     await runSessionCase(page, audit, id, { accessExpires: 600 }, {
  65  |       3: async s => {
  66  |         if(refreshValue!==undefined){ await page.evaluate(async value => { (await(window as unknown as SystemWindow).System.import('@fm/base')).LoginUtil.setRefreshToken(value); },refreshValue); s.refreshR=refreshValue; }
  67  |         expect(await equalsToken(page,'refreshToken',refreshValue)).toBe(true);
  68  |       },
  69  |       4: async s => { s.control.holdAcquisition = true; await hidden(page); },
  70  |       6: async s => { await s.acceptAcquisition(replacement); },
  71  |       7: async () => { await visible(page); },
  72  |       9: async () => { await expect.poll(() => equalsToken(page, 'refreshToken', replacement)).toBe(true); },
  73  |     });
  74  |   });
  75  | }
  76  | test('AUTH-060 retry acquisition after network failure', async ({ page, audit }) => {
  77  |   await runSessionCase(page, audit, 'AUTH-060', {}, {
  78  |     4: async s => { s.control.acquisitionError = 'Network Error'; await hidden(page); await refreshCount(s, 1); await expect(page.getByTestId('MicroWebUI_base_snackbar').locator('.MuiSnackbarContent-root[role="alert"]')).toBeVisible(); s.control.acquisitionError = ''; s.control.holdAcquisition = true; },
  79  |     5: async s => { s.requests.length = 0; }, 6: async () => { await visible(page); }, 7: async () => { await hidden(page); },
  80  |     9: async s => { await s.acceptAcquisition(); }, 10: async () => { await visible(page); },
  81  |   });
  82  | });
  83  | test('AUTH-061 retry cancelled acquisition', async ({ page, audit }) => {
  84  |   await runSessionCase(page, audit, 'AUTH-061', {}, {
  85  |     4: async s => { s.control.holdAcquisition = true; await s.startAcquire(); await refreshCount(s,1);
  86  |       await page.evaluate(async () => { (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.signal.getRefreshToken?.abort(); });
  87  |       await expect.poll(() => page.evaluate(async () => Boolean((await (window as unknown as SystemWindow).System.import('@fm/base')).Service.signal.getRefreshToken))).toBe(false);
  88  |       s.acquisition.length = 0;
  89  |     },
  90  |     5: async s => { s.requests.length = 0; }, 6: async () => { await hidden(page); },
  91  |     8: async s => { await s.acceptAcquisition(); }, 9: async () => { await visible(page); },
  92  |   });
  93  | });
  94  | for (const [id, remaining] of [['AUTH-064',1],['AUTH-065',24999]] as const) {
  95  |   test(`${id} last-moment hide preserves manual recovery`, async ({ page, audit }) => {
  96  |     await runSessionCase(page, audit, id, { accessExpires: remaining / 1000, refreshExpires: 600 }, {
  97  |       3: async s => { expect(await equalsToken(page, 'refreshToken', s.refreshR)).toBe(true); expect((await observe(page)).accessExpiryMs).toBe(T+remaining); },
  98  |       4: async () => { await hidden(page); }, 5: async () => { await page.clock.runFor(remaining); }, 6: async () => { await visible(page); },
  99  |     });
  100 |   });
  101 | }
  102 | test('AUTH-067 missed acquisition does not replay', async ({ page, audit }) => {
  103 |   await runSessionCase(page, audit, 'AUTH-067', {}, {
  104 |     4: async s => { s.control.failAcquisition = true; await at(page,60000); await hidden(page); await refreshCount(s,1); await expect(page.getByTestId('MicroWebUI_base_snackbar').locator('.MuiSnackbarContent-root[role="alert"]')).toBeVisible(); },
  105 |     5: async s => { s.requests.length = 0; }, 6: async () => { await at(page,890000); }, 7: async () => { await visible(page); },
  106 |     8: async () => { await at(page,900000); }, 9: async () => { await page.clock.runFor(1000); },
  107 |   });
  108 | });
  109 | test('AUTH-068 access rotation replaces obsolete timer', async ({ page, audit }) => {
  110 |   await runSessionCase(page, audit, 'AUTH-068', {}, {
  111 |     4: async () => { await rotate(page,sessionToken(1200,'B')); },
  112 |     5: async () => { expect((await observe(page)).visibility).toBe('visible'); },
  113 |     6: async () => { await at(page,875000); }, 10: async () => { await at(page,1175000); },
  114 |     12: async s => { expect(s.requests.filter(x=>x.endpoint==='refreshtoken').at(-1)?.accessMatchesB).toBe(true); },
  115 |   });
  116 | });
  117 | test('AUTH-069 paused mouse movement renews access', async ({ page, audit }) => {
  118 |   await runSessionCase(page,audit,'AUTH-069',{refreshExpires:13524},{4:async()=>{await at(page,60000);},5:mouse,6:async()=>{await at(page,65000);}});
  119 | });
  120 | test('AUTH-070 repeated mouse movements debounce', async ({ page, audit }) => {
  121 |   const ops: Partial<Record<number,(s:Session)=>Promise<unknown>>> = {4:async()=>{await at(page,60000);},17:async()=>{await at(page,70000);}};
  122 |   for (const [step,offset] of [[6,61000],[8,62000],[10,63000],[12,64000],[14,65000]]) ops[step]=async()=>{await at(page,offset);};
  123 |   for (const n of [5,7,9,11,13,15]) ops[n]=mouse;
  124 |   await runSessionCase(page,audit,'AUTH-070',{refreshExpires:13524},ops);
  125 | });
  126 | for (const [id, remaining] of [['AUTH-071',30000],['AUTH-072',29999]] as const) {
  127 |   test(`${id} mouse renewal lower boundary`, async ({page,audit})=>{
  128 |     await runSessionCase(page,audit,id,{accessExpires:remaining/1000,refreshExpires:13524},{4:mouse,5:async()=>{await page.clock.runFor(5000);}});
  129 |   });
  130 | }
  131 | test('AUTH-073 mouse does not revive expired access',async({page,audit})=>{
  132 |   await runSessionCase(page,audit,'AUTH-073',{refreshExpires:13524},{
  133 |     4:async()=>{await hidden(page);await page.clock.setSystemTime(new Date(T+1800000));},5:async()=>{await visible(page);},6:mouse,
  134 |     8:async()=>{await page.clock.runFor(5000);},
  135 |   });
  136 | });
  137 | for (const id of ['AUTH-074','AUTH-075'] as const) {
  138 |   test(`${id} proposed input activity renewal`,async({page,audit})=>{
  139 |     await runSessionCase(page,audit,id,{}, {
  140 |       3:async s=>{await at(page,60000);expect(await equalsToken(page,'token',s.accessA)).toBe(true); await page.evaluate(()=>{const w=window as unknown as {auditMouseMoves:number};w.auditMouseMoves=0;document.addEventListener('mousemove',()=>{w.auditMouseMoves++;});});},
  141 |       4:async s=>{
  142 |         if(id==='AUTH-074') await s.portal.workspace('WS-A').nameInput.fill('WS-A-KEYBOARD');
> 143 |         else { await s.portal.addWorkspaceButton.tap({force:true}); expect(await page.evaluate(()=>(window as unknown as {auditMouseMoves:number}).auditMouseMoves)).toBe(0); }
      |                                                                                                                                                                      ^ Error: expect(received).toBe(expected) // Object.is equality
  144 |       },
  145 |       5:async()=>{await page.clock.runFor(5000);},
  146 |       ...(id==='AUTH-074'?{6:async s=>{await expect(s.portal.workspaceList).toBeVisible();}}:{}),
  147 |     });
  148 |   });
  149 | }
  150 | 
  151 | test('AUTH-079 no silent recovery while expiry dialog is open',async({page,audit})=>{
  152 |   await runSessionCase(page,audit,'AUTH-079',{accessExpires:0,refreshExpires:600},{
  153 |     5:async()=>{await hidden(page);},6:async()=>{await visible(page);},
  154 |   });
  155 | });
  156 | for (const [id, duration] of [['AUTH-085',13524000],['AUTH-086',14400000],['AUTH-087',14400001],['AUTH-088',28800000],['AUTH-089',86400000]] as const) {
  157 |   test(`${id} controlled suspension expires session`,async({page,audit})=>{
  158 |     await runSessionCase(page,audit,id,{refreshExpires:13524},{
  159 |       4:async()=>{await hidden(page);expect((await observe(page)).now).toBe(T);},
  160 |       5:async()=>{await page.clock.setSystemTime(new Date(T+duration));expect((await observe(page)).now).toBe(T+duration);},
  161 |       6:async()=>{await visible(page);},7:async()=>{await page.clock.runFor(1000);},
  162 |     });
  163 |   });
  164 | }
  165 | test('AUTH-090 resume before expiry and renew through mouse',async({page,audit})=>{
  166 |   const B=sessionToken(1500,'B');
  167 |   await runSessionCase(page,audit,'AUTH-090',{refreshExpires:13524},{4:async()=>{await at(page,60000);await hidden(page);},
  168 |     5:async()=>{await at(page,120000);},6:async()=>{await visible(page);},7:mouse,8:async()=>{await at(page,125000);},
  169 |     11:async()=>{await expect.poll(()=>equalsToken(page,'token',B)).toBe(true);},
  170 |   });
  171 | });
  172 | test('AUTH-091 resume after expiry requires manual Extend',async({page,audit})=>{
  173 |   await runSessionCase(page,audit,'AUTH-091',{refreshExpires:13524},{
  174 |     4:async()=>{await hidden(page);await page.clock.setSystemTime(new Date(T+1800000));},5:async()=>{await visible(page);},
  175 |     8:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
  176 |     10:async s=>{expect(s.requests.find(x=>x.endpoint==='relogin')?.refreshMatchesR).toBe(true);},
  177 |   });
  178 | });
  179 | test('AUTH-092 background rotation preserves newer access',async({page,audit})=>{
  180 |   const B=sessionToken(1800,'B');
  181 |   await runSessionCase(page,audit,'AUTH-092',{refreshExpires:13524},{
  182 |     4:async()=>{await hidden(page);await rotate(page,B);},5:async()=>{await at(page,1000000);},6:async()=>{await visible(page);},9:async()=>{expect(await equalsToken(page,'token',B)).toBe(true);},
  183 |   });
  184 | });
  185 | for(const id of ['AUTH-095','AUTH-096'] as const){
  186 |   test(`${id} relogin failure UI`,async({page,audit})=>{
  187 |     await runSessionCase(page,audit,id,{accessExpires:0,refreshExpires:600},{
  188 |       5:async s=>{s.control.reloginError=id==='AUTH-095'?'TOKEN_INVALID_EXPIRED':'Network Error';},
  189 |       6:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
  190 |     });
  191 |   });
  192 | }
  193 | test('AUTH-100 forward clock jump reconciles expiry',async({page,audit})=>{
  194 |   await runSessionCase(page,audit,'AUTH-100',{refreshExpires:13524},{4:async()=>{await hidden(page);},
  195 |     5:async()=>{await page.clock.setSystemTime(new Date(T+13525000));},6:async()=>{await visible(page);},8:async()=>{await page.clock.runFor(1000);},
  196 |   });
  197 | });
  198 | 
  199 | test('AUTH-082 access rotation does not postpone refresh expiry',async({page,audit})=>{
  200 |   await runSessionCase(page,audit,'AUTH-082',{refreshExpires:13524},{
  201 |     4:async()=>{await rotate(page,sessionToken(15000,'B'));},
  202 |     5:async()=>{await at(page,13524000,true);},7:async()=>{await page.clock.runFor(1000);},
  203 |   });
  204 | });
  205 | test('AUTH-094 late manual recovery retains refresh cutoff',async({page,audit})=>{
  206 |   const B=sessionToken(1500,'B');
  207 |   await runSessionCase(page,audit,'AUTH-094',{accessExpires:0,refreshExpires:600},{
  208 |     5:async s=>{expect(s.control.holdRelogin).toBe(true);},6:async()=>{await at(page,540000,true);},
  209 |     7:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});await expect.poll(()=>s.relogin.length).toBe(1);},
  210 |     9:async s=>{await s.acceptRelogin(B);await expect.poll(()=>equalsToken(page,'token',B)).toBe(true);},
  211 |     10:async()=>{expect(await equalsToken(page,'token',B)).toBe(true);},12:async()=>{await at(page,600000,true);},
  212 |     14:async()=>{await page.clock.runFor(1000);},
  213 |   });
  214 | });
  215 | test('AUTH-101 server expiry response after backward clock jump',async({page,audit})=>{
  216 |   let release!:()=>void;const held=new Promise<void>(resolve=>{release=resolve;});let pending=false;
  217 |   await runSessionCase(page,audit,'AUTH-101',{refreshExpires:13524},{
  218 |     4:async()=>{
  219 |       await page.route('**/api/auth/v2/sso/validate',async route=>{pending=true;await held;await route.fulfill({status:401,json:{message:'TOKEN_INVALID_EXPIRED'}});});
  220 |       await page.evaluate(async()=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');void m.Service.postService('/auth/v2/sso/validate',{singleUIAuthorization:m.Hooks.getHooks().store.token}).catch(()=>{});});
  221 |       await expect.poll(()=>pending).toBe(true);
  222 |     },
  223 |     5:async()=>{await page.clock.setSystemTime(new Date(T-3600000));},6:async()=>{release();},
  224 |     12:async()=>{expect((await observe(page)).accessPresent).toBe(false);},
  225 |   });
  226 | });
  227 | 
  228 | const leaveDialog=(page:Parameters<typeof visibility>[0])=>page.getByRole('dialog',{name:'Leave Now?',exact:true});
  229 | async function openLeave(s:Session){await s.portal.avatarButton.click({force:true});await s.portal.logoutMenuItem.click({force:true});await expect(leaveDialog(s.portal.page)).toBeVisible();}
  230 | const logoutButton=(page:Parameters<typeof visibility>[0])=>leaveDialog(page).getByRole('button',{name:'Logout',exact:true});
  231 | test('AUTH-102 cancelling logout preserves workspace state',async({page,audit})=>{
  232 |   let before='';
  233 |   await runSessionCase(page,audit,'AUTH-102',{}, {
  234 |     3:openLeave,
  235 |     4:async s=>{before=await page.getByTestId('workspaces-tab-WS-A').locator('input').inputValue();await audit.record('before-cancel',{name:before,accessPresent:(await observe(page)).accessPresent});},
  236 |     5:async()=>{await leaveDialog(page).getByRole('button',{name:'Cancel',exact:true}).click({force:true});},
  237 |     6:async()=>{await expect(leaveDialog(page)).toHaveCount(0);},
  238 |     8:async s=>{expect(await page.getByTestId('workspaces-tab-WS-A').locator('input').inputValue()).toBe(before);expect(await equalsToken(page,'token',s.accessA)).toBe(true);},
  239 |     9:async s=>{expect(s.count('logout')).toBe(0);},
  240 |   });
  241 | });
  242 | test('AUTH-103 profile logout clears session defaults',async({page,audit})=>{
  243 |   await runSessionCase(page,audit,'AUTH-103',{refreshExpires:13524},{
```