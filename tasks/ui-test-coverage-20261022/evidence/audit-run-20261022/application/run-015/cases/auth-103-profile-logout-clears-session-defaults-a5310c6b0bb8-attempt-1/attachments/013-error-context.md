# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-session-expanded.spec.ts >> AUTH-103 profile logout clears session defaults
- Location: e2e/audit-specs/auth-session-expanded.spec.ts:238:1

# Error details

```
Error: expect(received).toEqual(expected) // deep equality

- Expected  - 1
+ Received  + 1

  Object {
-   "expiredIn": 0,
+   "expiredIn": undefined,
    "refreshToken": null,
    "token": null,
    "user": null,
    "userLoginTime": null,
  }
```

# Page snapshot

```yaml
- generic [ref=e5]:
  - main [ref=e7]:
    - heading "Sign In" [level=3] [ref=e8]
    - generic [ref=e9]:
      - generic [ref=e10]:
        - generic [ref=e11]: Username
        - textbox "Enter Username" [ref=e17]
      - generic [ref=e18]:
        - generic [ref=e19]: Password
        - textbox "Enter Password" [ref=e25]
      - button "Sign In" [ref=e26] [cursor=pointer]
      - separator [ref=e27]
    - link "Sign In With SSO" [ref=e29] [cursor=pointer]:
      - /url: https://login.microsoftonline.com/cd823f6b-31c5-4241-b504-3707cbc03fb7/oauth2/v2.0/authorize?client_id=80c8b904-1b64-443b-a651-7548764d534d&response_type=code&redirect_uri=http://localhost:8128/mfa/callback&response_mode=query&scope=openid+profile+offline_access+email
  - main [ref=e31]:
    - tabpanel [ref=e32]:
      - generic [ref=e33]:
        - heading "Markets Operations One" [level=2] [ref=e34]
        - paragraph [ref=e35]: Markets Operations One Portal (MO1) is a single, evolving workspace for Operations processing, integrating post-trade applications, and progressively delivering a more connected, intelligent, and efficient processing.
    - tablist "login tabs" [ref=e39]:
      - tab "login-tabpanel" [selected] [ref=e40] [cursor=pointer]
```

# Test source

```ts
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
  175 | test('AUTH-092 background rotation preserves newer access',async({page,audit})=>{
  176 |   const B=sessionToken(1800,'B');
  177 |   await runSessionCase(page,audit,'AUTH-092',{refreshExpires:13524},{
  178 |     4:async()=>{await hidden(page);await rotate(page,B);},5:async()=>{await at(page,1000000);},6:async()=>{await visible(page);},9:async()=>{expect(await equalsToken(page,'token',B)).toBe(true);},
  179 |   });
  180 | });
  181 | for(const id of ['AUTH-095','AUTH-096'] as const){
  182 |   test(`${id} relogin failure UI`,async({page,audit})=>{
  183 |     await runSessionCase(page,audit,id,{accessExpires:0,refreshExpires:600},{
  184 |       5:async s=>{s.control.reloginError=id==='AUTH-095'?'TOKEN_INVALID_EXPIRED':'Network Error';},
  185 |       6:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
  186 |     });
  187 |   });
  188 | }
  189 | test('AUTH-100 forward clock jump reconciles expiry',async({page,audit})=>{
  190 |   await runSessionCase(page,audit,'AUTH-100',{refreshExpires:13524},{4:async()=>{await hidden(page);},
  191 |     5:async()=>{await page.clock.setSystemTime(new Date(T+13525000));},6:async()=>{await visible(page);},8:async()=>{await page.clock.runFor(1000);},
  192 |   });
  193 | });
  194 | 
  195 | test('AUTH-082 access rotation does not postpone refresh expiry',async({page,audit})=>{
  196 |   await runSessionCase(page,audit,'AUTH-082',{refreshExpires:13524},{
  197 |     4:async()=>{await rotate(page,sessionToken(15000,'B'));},
  198 |     5:async()=>{await at(page,13524000,true);},7:async()=>{await page.clock.runFor(1000);},
  199 |   });
  200 | });
  201 | test('AUTH-094 late manual recovery retains refresh cutoff',async({page,audit})=>{
  202 |   const B=sessionToken(1500,'B');
  203 |   await runSessionCase(page,audit,'AUTH-094',{accessExpires:0,refreshExpires:600},{
  204 |     5:async s=>{expect(s.control.holdRelogin).toBe(true);},6:async()=>{await at(page,540000,true);},
  205 |     7:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});await expect.poll(()=>s.relogin.length).toBe(1);},
  206 |     9:async s=>{await s.acceptRelogin(B);await expect.poll(()=>equalsToken(page,'token',B)).toBe(true);},
  207 |     10:async()=>{expect(await equalsToken(page,'token',B)).toBe(true);},12:async()=>{await at(page,600000,true);},
  208 |     14:async()=>{await page.clock.runFor(1000);},
  209 |   });
  210 | });
  211 | test('AUTH-101 server expiry response after backward clock jump',async({page,audit})=>{
  212 |   let release!:()=>void;const held=new Promise<void>(resolve=>{release=resolve;});let pending=false;
  213 |   await runSessionCase(page,audit,'AUTH-101',{refreshExpires:13524},{
  214 |     4:async()=>{
  215 |       await page.route('**/api/auth/v2/sso/validate',async route=>{pending=true;await held;await route.fulfill({status:401,json:{message:'TOKEN_INVALID_EXPIRED'}});});
  216 |       await page.evaluate(async()=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');void m.Service.postService('/auth/v2/sso/validate',{singleUIAuthorization:m.Hooks.getHooks().store.token}).catch(()=>{});});
  217 |       await expect.poll(()=>pending).toBe(true);
  218 |     },
  219 |     5:async()=>{await page.clock.setSystemTime(new Date(T-3600000));},6:async()=>{release();},
  220 |     12:async()=>{expect((await observe(page)).accessPresent).toBe(false);},
  221 |   });
  222 | });
  223 | 
  224 | const leaveDialog=(page:Parameters<typeof visibility>[0])=>page.getByRole('dialog',{name:'Leave Now?',exact:true});
  225 | async function openLeave(s:Session){await s.portal.avatarButton.click({force:true});await s.portal.logoutMenuItem.click({force:true});await expect(leaveDialog(s.portal.page)).toBeVisible();}
  226 | const logoutButton=(page:Parameters<typeof visibility>[0])=>leaveDialog(page).getByRole('button',{name:'Logout',exact:true});
  227 | test('AUTH-102 cancelling logout preserves workspace state',async({page,audit})=>{
  228 |   let before='';
  229 |   await runSessionCase(page,audit,'AUTH-102',{}, {
  230 |     3:openLeave,
  231 |     4:async s=>{before=await s.portal.workspace('WS-A').nameInput.inputValue();await audit.record('before-cancel',{name:before,accessPresent:(await observe(page)).accessPresent});},
  232 |     5:async()=>{await leaveDialog(page).getByRole('button',{name:'Cancel',exact:true}).click({force:true});},
  233 |     6:async()=>{await expect(leaveDialog(page)).toHaveCount(0);},
  234 |     8:async s=>{expect(await s.portal.workspace('WS-A').nameInput.inputValue()).toBe(before);expect(await equalsToken(page,'token',s.accessA)).toBe(true);},
  235 |     9:async s=>{expect(s.count('logout')).toBe(0);},
  236 |   });
  237 | });
  238 | test('AUTH-103 profile logout clears session defaults',async({page,audit})=>{
  239 |   await runSessionCase(page,audit,'AUTH-103',{refreshExpires:13524},{
  240 |     3:openLeave,4:async()=>{await logoutButton(page).click({force:true});},5:async()=>{await page.clock.runFor(1000);},
  241 |     10:async()=>{
  242 |       const state=await page.evaluate(async()=>{const s=(await(window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store as Record<string,unknown>;
  243 |         return {token:s.token??null,refreshToken:s.refreshToken??null,user:s.user??null,expiredIn:s.expiredIn,userLoginTime:s.userLoginTime??null};});
> 244 |       expect(state).toEqual({token:null,refreshToken:null,user:null,expiredIn:0,userLoginTime:null});await audit.record('cleared-session-defaults',state);
      |                     ^ Error: expect(received).toEqual(expected) // deep equality
  245 |     },
  246 |   });
  247 | });
  248 | for(const id of ['AUTH-107','AUTH-108','AUTH-109','AUTH-110'] as const){
  249 |   test(`${id} logout transport failure keeps local logout`,async({page,audit})=>{
  250 |     await runSessionCase(page,audit,id,{}, {
  251 |       3:openLeave,
  252 |       4:async()=>{
  253 |         if(id!=='AUTH-108') await page.route('**/api/auth/v2/sso/logout',async route=>{if(id==='AUTH-110')return;await route.fulfill({status:503,json:{message:'Fixture logout unavailable'}});});
  254 |         if(id!=='AUTH-107') await page.route('**/api/ssiplus/imeta/logout',async route=>{if(id==='AUTH-110')return;await route.fulfill({status:503,json:{message:'Fixture logout unavailable'}});});
  255 |       },
  256 |       5:async()=>{await logoutButton(page).click({force:true});},6:async()=>{await page.clock.runFor(1000);},
  257 |       12:async()=>{await expect(page.getByRole('alert')).toHaveCount(0);},
  258 |     });
  259 |   });
  260 | }
  261 | for(const id of ['AUTH-113','AUTH-114'] as const){
  262 |   test(`${id} browser navigation cannot restore logged out access`,async({page,audit})=>{
  263 |     const steps=await audit.defineCase(id);let s!:Session;
  264 |     for(const step of steps)await audit.step(step.number,async()=>{
  265 |       if(step.number===1){s=await import('../support/auth-session.js').then(m=>m.sessionSetup(page,audit,{}));await openLeave(s);await logoutButton(page).click({force:true});await page.clock.runFor(1000);await s.login.expectVisible();return;}
  266 |       if(step.number===2){if(id==='AUTH-113')await page.goBack();else await page.reload();return;}
  267 |       if(step.number===7){expect(await page.evaluate(()=>Boolean(localStorage.getItem('SET_TOKEN')||sessionStorage.getItem('SET_TOKEN')))).toBe(false);return;}
  268 |       const handled=await import('../support/auth-session.js').then(m=>m.commonAssertion(page,s,step.text));if(!handled)throw new Error(`Missing ${id} step ${step.number}`);
  269 |     });
  270 |   });
  271 | }
  272 | 
```