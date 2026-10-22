# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-session-expanded.spec.ts >> AUTH-060 retry acquisition after network failure
- Location: e2e/audit-specs/auth-session-expanded.spec.ts:72:1

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByRole('alert')
Expected: visible
Error: strict mode violation: getByRole('alert') resolved to 2 elements:
    1) <div role="alert" direction="up" class="MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation6 MuiAlert-root MuiAlert-colorError MuiAlert-standardError MuiAlert-standard css-rgg0t8-MuiPaper-root-MuiAlert-root">…</div> aka getByRole('alert').first()
    2) <div role="alert" class="MuiPaper-root MuiPaper-elevation MuiPaper-elevation6 MuiSnackbarContent-root css-11hfw37-MuiPaper-root-MuiSnackbarContent-root">…</div> aka getByRole('alert').nth(1)

Call log:
  - Expect "toBeVisible" getByRole('alert') with timeout 5000ms
  - waiting for getByRole('alert')

```

# Page snapshot

```yaml
- generic [ref=e3]:
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
          - generic [ref=e27]: 00:00 UTC
          - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
        - button "User Profiles" [ref=e34] [cursor=pointer]:
          - generic [ref=e35]: A
        - button "Share Feedback" [ref=e37] [cursor=pointer]
    - main [ref=e41]:
      - tablist "workspaces" [ref=e45]:
        - tab [selected] [ref=e47] [cursor=pointer]:
          - region "WS-A" [ref=e48]:
            - textbox "Workspace Name" [ref=e52]: WS-A
        - button "Add Workspace" [ref=e54] [cursor=pointer]
      - tabpanel [ref=e59]:
        - generic [ref=e63]:
          - paragraph [ref=e65]: Start customizing your workspace
          - paragraph [ref=e66]: find out what workspace preference options you have and how those options work.
          - button [ref=e67] [cursor=pointer]
  - alert [ref=e71]:
    - alert [ref=e76]:
      - generic [ref=e77]: "Error happened, service is unavailable, pls check with support team: /api/auth/v2/sso/refreshtoken: API request failed"
    - button "Close" [ref=e79] [cursor=pointer]
```

# Test source

```ts
  1   | import { test, expect } from '../support/audit-fixture.js';
  2   | import { at, equalsToken, observe, rotate, runSessionCase, sessionToken, tokenPayload, T, visibility,
  3   |   type Session, type SystemWindow } from '../support/auth-session.js';
  4   | 
  5   | test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES', serviceWorkers: 'block', hasTouch: true,
  6   |   auditFixture: 'Actual MFE; controlled API responses, clock, visibility and suspension adapters. Unsigned browser-only credentials. No natural lifecycle, real identity or service policy acceptance.' });
  7   | const mouse = async (s: Session) => { await s.portal.workspaceList.dispatchEvent('mousemove', { bubbles: true }); };
  8   | const hidden = async (page: Parameters<typeof visibility>[0]) => { await visibility(page, 'hidden'); };
  9   | const visible = async (page: Parameters<typeof visibility>[0]) => { await visibility(page, 'visible'); };
  10  | const refreshCount = async (s: Session, count: number) => { await expect.poll(() => s.count('refreshtoken')).toBe(count); };
  11  | 
  12  | for (const id of ['AUTH-045','AUTH-046','AUTH-047','AUTH-048','AUTH-049'] as const) {
  13  |   test(`${id} controlled visibility acquisition`, async ({ page, audit }) => {
  14  |     await runSessionCase(page, audit, id, {}, {
  15  |       4: async s => {
  16  |         await at(page, 60000);
  17  |         if (id === 'AUTH-045') return;
  18  |         if (id === 'AUTH-047') s.control.failAcquisition = true;
  19  |         if (id === 'AUTH-048' || id === 'AUTH-049') s.control.holdAcquisition = true;
  20  |         await hidden(page); await refreshCount(s, 1);
  21  |         if (id === 'AUTH-046') await expect.poll(async () => (await observe(page)).refreshPresent).toBe(true);
  22  |         if (id === 'AUTH-047') { await expect(page.getByRole('alert')).toBeVisible(); s.control.failAcquisition = false; }
  23  |       },
  24  |       5: async s => { if (id === 'AUTH-045') await hidden(page); else s.requests.length = 0; },
  25  |       ...(id === 'AUTH-045' ? {
  26  |         7: async () => { await visible(page); },
  27  |       } : id === 'AUTH-046' ? {
  28  |         6: async () => { await at(page, 875000); }, 8: async () => { await visible(page); },
  29  |       } : id === 'AUTH-047' ? {
  30  |         6: async () => { await at(page, 120000); }, 7: async () => { await visible(page); }, 8: async () => { await at(page, 875000); },
  31  |       } : id === 'AUTH-048' ? {
  32  |         6: async () => { await hidden(page); }, 7: async () => { await hidden(page); }, 8: async () => { await hidden(page); },
  33  |         10: async s => { await s.acceptAcquisition(); }, 11: async () => { await visible(page); },
  34  |         13: async () => { await expect.poll(() => equalsToken(page, 'refreshToken', sessionToken(13524, 'R'))).toBe(true); },
  35  |       } : {
  36  |         6: async () => { await visible(page); }, 7: async () => { await hidden(page); },
  37  |         9: async () => { expect(await page.evaluate(async () => (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.signal.getRefreshToken?.signal.aborted)).toBe(false); },
  38  |         10: async s => { await s.acceptAcquisition(); }, 11: async () => { await visible(page); },
  39  |       }),
  40  |     });
  41  |   });
  42  | }
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
  64  |     await runSessionCase(page, audit, id, { accessExpires: 600, refreshValue }, {
  65  |       4: async s => { s.control.holdAcquisition = true; await hidden(page); },
  66  |       6: async s => { await s.acceptAcquisition(replacement); },
  67  |       7: async () => { await visible(page); },
  68  |       9: async () => { await expect.poll(() => equalsToken(page, 'refreshToken', replacement)).toBe(true); },
  69  |     });
  70  |   });
  71  | }
  72  | test('AUTH-060 retry acquisition after network failure', async ({ page, audit }) => {
  73  |   await runSessionCase(page, audit, 'AUTH-060', {}, {
> 74  |     4: async s => { s.control.acquisitionError = 'Network Error'; await hidden(page); await refreshCount(s, 1); await expect(page.getByRole('alert')).toBeVisible(); s.control.acquisitionError = ''; s.control.holdAcquisition = true; },
      |                                                                                                                                                       ^ Error: expect(locator).toBeVisible() failed
  75  |     5: async s => { s.requests.length = 0; }, 6: async () => { await visible(page); }, 7: async () => { await hidden(page); },
  76  |     9: async s => { await s.acceptAcquisition(); }, 10: async () => { await visible(page); },
  77  |   });
  78  | });
  79  | test('AUTH-061 retry cancelled acquisition', async ({ page, audit }) => {
  80  |   await runSessionCase(page, audit, 'AUTH-061', {}, {
  81  |     4: async s => { s.control.holdAcquisition = true; await s.startAcquire(); await refreshCount(s,1);
  82  |       await page.evaluate(async () => { (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.signal.getRefreshToken?.abort(); });
  83  |       await expect.poll(() => page.evaluate(async () => Boolean((await (window as unknown as SystemWindow).System.import('@fm/base')).Service.signal.getRefreshToken))).toBe(false);
  84  |       s.acquisition.length = 0;
  85  |     },
  86  |     5: async s => { s.requests.length = 0; }, 6: async () => { await hidden(page); },
  87  |     8: async s => { await s.acceptAcquisition(); }, 9: async () => { await visible(page); },
  88  |   });
  89  | });
  90  | for (const [id, remaining] of [['AUTH-064',1],['AUTH-065',24999]] as const) {
  91  |   test(`${id} last-moment hide preserves manual recovery`, async ({ page, audit }) => {
  92  |     await runSessionCase(page, audit, id, { accessExpires: remaining / 1000, refreshExpires: 600 }, {
  93  |       3: async s => { expect(await equalsToken(page, 'refreshToken', s.refreshR)).toBe(true); expect((await observe(page)).accessExpiryMs).toBe(T+remaining); },
  94  |       4: async () => { await hidden(page); }, 5: async () => { await page.clock.runFor(remaining); }, 6: async () => { await visible(page); },
  95  |     });
  96  |   });
  97  | }
  98  | test('AUTH-067 missed acquisition does not replay', async ({ page, audit }) => {
  99  |   await runSessionCase(page, audit, 'AUTH-067', {}, {
  100 |     4: async s => { s.control.failAcquisition = true; await at(page,60000); await hidden(page); await refreshCount(s,1); await expect(page.getByRole('alert')).toBeVisible(); },
  101 |     5: async s => { s.requests.length = 0; }, 6: async () => { await at(page,890000); }, 7: async () => { await visible(page); },
  102 |     8: async () => { await at(page,900000); }, 9: async () => { await page.clock.runFor(1000); },
  103 |   });
  104 | });
  105 | test('AUTH-068 access rotation replaces obsolete timer', async ({ page, audit }) => {
  106 |   await runSessionCase(page, audit, 'AUTH-068', {}, {
  107 |     4: async () => { await rotate(page,sessionToken(1200,'B')); },
  108 |     5: async () => { expect((await observe(page)).visibility).toBe('visible'); },
  109 |     6: async () => { await at(page,875000); }, 10: async () => { await at(page,1175000); },
  110 |     12: async s => { expect(s.requests.filter(x=>x.endpoint==='refreshtoken').at(-1)?.accessMatchesB).toBe(true); },
  111 |   });
  112 | });
  113 | test('AUTH-069 paused mouse movement renews access', async ({ page, audit }) => {
  114 |   await runSessionCase(page,audit,'AUTH-069',{refreshExpires:13524},{4:async()=>{await at(page,60000);},5:mouse,6:async()=>{await at(page,65000);}});
  115 | });
  116 | test('AUTH-070 repeated mouse movements debounce', async ({ page, audit }) => {
  117 |   const ops: Partial<Record<number,(s:Session)=>Promise<unknown>>> = {4:async()=>{await at(page,60000);},17:async()=>{await at(page,70000);}};
  118 |   for (const [step,offset] of [[6,61000],[8,62000],[10,63000],[12,64000],[14,65000]]) ops[step]=async()=>{await at(page,offset);};
  119 |   for (const n of [5,7,9,11,13,15]) ops[n]=mouse;
  120 |   await runSessionCase(page,audit,'AUTH-070',{refreshExpires:13524},ops);
  121 | });
  122 | for (const [id, remaining] of [['AUTH-071',30000],['AUTH-072',29999]] as const) {
  123 |   test(`${id} mouse renewal lower boundary`, async ({page,audit})=>{
  124 |     await runSessionCase(page,audit,id,{accessExpires:remaining/1000,refreshExpires:13524},{4:mouse,5:async()=>{await page.clock.runFor(5000);}});
  125 |   });
  126 | }
  127 | test('AUTH-073 mouse does not revive expired access',async({page,audit})=>{
  128 |   await runSessionCase(page,audit,'AUTH-073',{refreshExpires:13524},{
  129 |     4:async()=>{await hidden(page);await page.clock.setSystemTime(new Date(T+1800000));},5:async()=>{await visible(page);},6:mouse,
  130 |     8:async()=>{await page.clock.runFor(5000);},
  131 |   });
  132 | });
  133 | for (const id of ['AUTH-074','AUTH-075'] as const) {
  134 |   test(`${id} proposed input activity renewal`,async({page,audit})=>{
  135 |     await runSessionCase(page,audit,id,{}, {
  136 |       3:async s=>{await at(page,60000);expect(await equalsToken(page,'token',s.accessA)).toBe(true);},
  137 |       4:async s=>{
  138 |         if(id==='AUTH-074') await s.portal.workspace('WS-A').nameInput.fill('WS-A-KEYBOARD');
  139 |         else await s.portal.addWorkspaceButton.tap({force:true});
  140 |       },
  141 |       5:async()=>{await page.clock.runFor(5000);},
  142 |       ...(id==='AUTH-074'?{6:async s=>{await expect(s.portal.workspaceList).toBeVisible();}}:{}),
  143 |     });
  144 |   });
  145 | }
  146 | 
  147 | test('AUTH-079 no silent recovery while expiry dialog is open',async({page,audit})=>{
  148 |   await runSessionCase(page,audit,'AUTH-079',{accessExpires:0,refreshExpires:600},{
  149 |     5:async()=>{await hidden(page);},6:async()=>{await visible(page);},
  150 |   });
  151 | });
  152 | for (const [id, duration] of [['AUTH-085',13524000],['AUTH-086',14400000],['AUTH-087',14400001],['AUTH-088',28800000],['AUTH-089',86400000]] as const) {
  153 |   test(`${id} controlled suspension expires session`,async({page,audit})=>{
  154 |     await runSessionCase(page,audit,id,{refreshExpires:13524},{
  155 |       4:async()=>{await hidden(page);expect((await observe(page)).now).toBe(T);},
  156 |       5:async()=>{await page.clock.setSystemTime(new Date(T+duration));expect((await observe(page)).now).toBe(T+duration);},
  157 |       6:async()=>{await visible(page);},7:async()=>{await page.clock.runFor(1000);},
  158 |     });
  159 |   });
  160 | }
  161 | test('AUTH-090 resume before expiry and renew through mouse',async({page,audit})=>{
  162 |   const B=sessionToken(1500,'B');
  163 |   await runSessionCase(page,audit,'AUTH-090',{refreshExpires:13524},{4:async()=>{await at(page,60000);await hidden(page);},
  164 |     5:async()=>{await at(page,120000);},6:async()=>{await visible(page);},7:mouse,8:async()=>{await at(page,125000);},
  165 |     11:async()=>{await expect.poll(()=>equalsToken(page,'token',B)).toBe(true);},
  166 |   });
  167 | });
  168 | test('AUTH-091 resume after expiry requires manual Extend',async({page,audit})=>{
  169 |   await runSessionCase(page,audit,'AUTH-091',{refreshExpires:13524},{
  170 |     4:async()=>{await hidden(page);await page.clock.setSystemTime(new Date(T+1800000));},5:async()=>{await visible(page);},
  171 |     8:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
  172 |     10:async s=>{expect(s.requests.find(x=>x.endpoint==='relogin')?.refreshMatchesR).toBe(true);},
  173 |   });
  174 | });
```