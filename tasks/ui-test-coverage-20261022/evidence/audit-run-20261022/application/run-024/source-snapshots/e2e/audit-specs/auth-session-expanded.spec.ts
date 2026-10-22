import { test, expect } from '../support/audit-fixture.js';
import { at, equalsToken, observe, rotate, runSessionCase, sessionToken, tokenPayload, T, visibility,
  type Session, type SystemWindow } from '../support/auth-session.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES', serviceWorkers: 'block', hasTouch: true,
  auditFixture: 'Actual MFE; controlled API responses, clock, visibility and suspension adapters. Unsigned browser-only credentials. No natural lifecycle, real identity or service policy acceptance.' });
const mouse = async (s: Session) => { await s.portal.root.getByRole('tablist',{name:'workspaces',exact:true,includeHidden:true}).dispatchEvent('mousemove', { bubbles: true }); };
const hidden = async (page: Parameters<typeof visibility>[0]) => { await visibility(page, 'hidden'); };
const visible = async (page: Parameters<typeof visibility>[0]) => { await visibility(page, 'visible'); };
const refreshCount = async (s: Session, count: number) => { await expect.poll(() => s.count('refreshtoken')).toBe(count); };

for (const id of ['AUTH-045','AUTH-046','AUTH-047','AUTH-048','AUTH-049'] as const) {
  test(`${id} controlled visibility acquisition`, async ({ page, audit }) => {
    await runSessionCase(page, audit, id, {}, {
      4: async s => {
        await at(page, 60000);
        if (id === 'AUTH-045') return;
        if (id === 'AUTH-047') s.control.failAcquisition = true;
        if (id === 'AUTH-048' || id === 'AUTH-049') s.control.holdAcquisition = true;
        await hidden(page); await refreshCount(s, 1);
        if (id === 'AUTH-046') await expect.poll(async () => (await observe(page)).refreshPresent).toBe(true);
        if (id === 'AUTH-047') { await expect(page.getByTestId('MicroWebUI_base_snackbar').locator('.MuiSnackbarContent-root[role="alert"]')).toBeVisible(); s.control.failAcquisition = false; }
      },
      5: async s => { if (id === 'AUTH-045') await hidden(page); else s.requests.length = 0; },
      ...(id === 'AUTH-045' ? {
        7: async () => { await visible(page); },
      } : id === 'AUTH-046' ? {
        6: async () => { await at(page, 875000); }, 8: async () => { await visible(page); },
      } : id === 'AUTH-047' ? {
        6: async () => { await at(page, 120000); }, 7: async () => { await visible(page); }, 8: async () => { await at(page, 875000); },
      } : id === 'AUTH-048' ? {
        6: async () => { await hidden(page); }, 7: async () => { await hidden(page); }, 8: async () => { await hidden(page); },
        10: async s => { await s.acceptAcquisition(); }, 11: async () => { await visible(page); },
        13: async () => { await expect.poll(() => equalsToken(page, 'refreshToken', sessionToken(13524, 'R'))).toBe(true); },
      } : {
        6: async () => { await visible(page); }, 7: async () => { await hidden(page); },
        9: async () => { expect(await page.evaluate(async () => (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.signal.getRefreshToken?.signal.aborted)).toBe(false); },
        10: async s => { await s.acceptAcquisition(); }, 11: async () => { await visible(page); },
      }),
    });
  });
}
for (const [id, remaining] of [['AUTH-050',10800.001],['AUTH-051',10800],['AUTH-052',10799.999]] as const) {
  test(`${id} recovery reuse boundary`, async ({ page, audit }) => {
    await runSessionCase(page, audit, id, { accessExpires: 600, refreshExpires: remaining }, {
      4: async () => { expect((await observe(page)).now).toBe(T); },
      5: async () => { await hidden(page); }, 6: async () => { await visible(page); },
    });
  });
}
test('AUTH-053 refresh reuse uses current controlled time', async ({ page, audit }) => {
  await runSessionCase(page, audit, 'AUTH-053', { accessExpires: 600, refreshExpires: 10801 }, {
    4: async () => { await hidden(page); }, 5: async () => { await visible(page); },
    7: async () => { await page.clock.runFor(1000); }, 8: async () => { await hidden(page); }, 9: async () => { await visible(page); },
  });
});
const invalidRefresh: [string,string | undefined][] = [
  ['AUTH-054',undefined], ['AUTH-055','Bearer fixture.not-json.fixture'], ['AUTH-056',tokenPayload({ fixture: 'missing-exp' })],
  ['AUTH-057',tokenPayload({ exp: null })], ['AUTH-058',tokenPayload({ exp: '10800' })], ['AUTH-059',tokenPayload({ exp: 1e308 })],
];
for (const [id, refreshValue] of invalidRefresh) {
  test(`${id} replacement acquisition for unusable refresh`, async ({ page, audit }) => {
    const replacement = sessionToken(13524, 'replacement');
    await runSessionCase(page, audit, id, { accessExpires: 600 }, {
      3: async s => {
        if(refreshValue!==undefined){ await page.evaluate(async value => { (await(window as unknown as SystemWindow).System.import('@fm/base')).LoginUtil.setRefreshToken(value); },refreshValue); s.refreshR=refreshValue; }
        expect(await equalsToken(page,'refreshToken',refreshValue)).toBe(true);
      },
      4: async s => { s.control.holdAcquisition = true; await hidden(page); },
      6: async s => { await s.acceptAcquisition(replacement); },
      7: async () => { await visible(page); },
      9: async () => { await expect.poll(() => equalsToken(page, 'refreshToken', replacement)).toBe(true); },
    });
  });
}
test('AUTH-060 retry acquisition after network failure', async ({ page, audit }) => {
  await runSessionCase(page, audit, 'AUTH-060', {}, {
    4: async s => { s.control.acquisitionError = 'Network Error'; await hidden(page); await refreshCount(s, 1); await expect(page.getByTestId('MicroWebUI_base_snackbar').locator('.MuiSnackbarContent-root[role="alert"]')).toBeVisible(); s.control.acquisitionError = ''; s.control.holdAcquisition = true; },
    5: async s => { s.requests.length = 0; }, 6: async () => { await visible(page); }, 7: async () => { await hidden(page); },
    9: async s => { await s.acceptAcquisition(); }, 10: async () => { await visible(page); },
  });
});
test('AUTH-061 retry cancelled acquisition', async ({ page, audit }) => {
  await runSessionCase(page, audit, 'AUTH-061', {}, {
    4: async s => { s.control.holdAcquisition = true; await s.startAcquire(); await refreshCount(s,1);
      await page.evaluate(async () => { (await (window as unknown as SystemWindow).System.import('@fm/base')).Service.signal.getRefreshToken?.abort(); });
      await expect.poll(() => page.evaluate(async () => Boolean((await (window as unknown as SystemWindow).System.import('@fm/base')).Service.signal.getRefreshToken))).toBe(false);
      s.acquisition.length = 0;
    },
    5: async s => { s.requests.length = 0; }, 6: async () => { await hidden(page); },
    8: async s => { await s.acceptAcquisition(); }, 9: async () => { await visible(page); },
  });
});
for (const [id, remaining] of [['AUTH-064',1],['AUTH-065',24999]] as const) {
  test(`${id} last-moment hide preserves manual recovery`, async ({ page, audit }) => {
    await runSessionCase(page, audit, id, { accessExpires: remaining / 1000, refreshExpires: 600 }, {
      3: async s => { expect(await equalsToken(page, 'refreshToken', s.refreshR)).toBe(true); expect((await observe(page)).accessExpiryMs).toBe(T+remaining); },
      4: async () => { await hidden(page); }, 5: async () => { await page.clock.runFor(remaining); }, 6: async () => { await visible(page); },
    });
  });
}
test('AUTH-067 missed acquisition does not replay', async ({ page, audit }) => {
  await runSessionCase(page, audit, 'AUTH-067', {}, {
    4: async s => { s.control.failAcquisition = true; await at(page,60000); await hidden(page); await refreshCount(s,1); await expect(page.getByTestId('MicroWebUI_base_snackbar').locator('.MuiSnackbarContent-root[role="alert"]')).toBeVisible(); },
    5: async s => { s.requests.length = 0; }, 6: async () => { await at(page,890000); }, 7: async () => { await visible(page); },
    8: async () => { await at(page,900000); }, 9: async () => { await page.clock.runFor(1000); },
  });
});
test('AUTH-068 access rotation replaces obsolete timer', async ({ page, audit }) => {
  await runSessionCase(page, audit, 'AUTH-068', {}, {
    4: async () => { await rotate(page,sessionToken(1200,'B')); },
    5: async () => { expect((await observe(page)).visibility).toBe('visible'); },
    6: async () => { await at(page,875000); }, 10: async () => { await at(page,1175000); },
    12: async s => { expect(s.requests.filter(x=>x.endpoint==='refreshtoken').at(-1)?.accessMatchesB).toBe(true); },
  });
});
test('AUTH-069 paused mouse movement renews access', async ({ page, audit }) => {
  await runSessionCase(page,audit,'AUTH-069',{refreshExpires:13524},{4:async()=>{await at(page,60000);},5:mouse,6:async()=>{await at(page,65000);}});
});
test('AUTH-070 repeated mouse movements debounce', async ({ page, audit }) => {
  const ops: Partial<Record<number,(s:Session)=>Promise<unknown>>> = {4:async()=>{await at(page,60000);},17:async()=>{await at(page,70000);}};
  for (const [step,offset] of [[6,61000],[8,62000],[10,63000],[12,64000],[14,65000]]) ops[step]=async()=>{await at(page,offset);};
  for (const n of [5,7,9,11,13,15]) ops[n]=mouse;
  await runSessionCase(page,audit,'AUTH-070',{refreshExpires:13524},ops);
});
for (const [id, remaining] of [['AUTH-071',30000],['AUTH-072',29999]] as const) {
  test(`${id} mouse renewal lower boundary`, async ({page,audit})=>{
    await runSessionCase(page,audit,id,{accessExpires:remaining/1000,refreshExpires:13524},{4:mouse,5:async()=>{await page.clock.runFor(5000);}});
  });
}
test('AUTH-073 mouse does not revive expired access',async({page,audit})=>{
  await runSessionCase(page,audit,'AUTH-073',{refreshExpires:13524},{
    4:async()=>{await hidden(page);await page.clock.setSystemTime(new Date(T+1800000));},5:async()=>{await visible(page);},6:mouse,
    8:async()=>{await page.clock.runFor(5000);},
  });
});
for (const id of ['AUTH-074','AUTH-075'] as const) {
  test(`${id} proposed input activity renewal`,async({page,audit})=>{
    await runSessionCase(page,audit,id,{}, {
      3:async s=>{await at(page,60000);expect(await equalsToken(page,'token',s.accessA)).toBe(true); await page.evaluate(()=>{const w=window as unknown as {auditMouseMoves:number};w.auditMouseMoves=0;document.addEventListener('mousemove',()=>{w.auditMouseMoves++;});});},
      4:async s=>{
        if(id==='AUTH-074') await s.portal.workspace('WS-A').nameInput.fill('WS-A-KEYBOARD');
        else { await s.portal.addWorkspaceButton.tap({force:true}); expect(await page.evaluate(()=>(window as unknown as {auditMouseMoves:number}).auditMouseMoves)).toBe(0); }
      },
      5:async()=>{await page.clock.runFor(5000);},
      ...(id==='AUTH-074'?{6:async s=>{await expect(s.portal.workspaceList).toBeVisible();}}:{}),
    });
  });
}

test('AUTH-079 no silent recovery while expiry dialog is open',async({page,audit})=>{
  await runSessionCase(page,audit,'AUTH-079',{accessExpires:0,refreshExpires:600},{
    5:async()=>{await hidden(page);},6:async()=>{await visible(page);},
  });
});
for (const [id, duration] of [['AUTH-085',13524000],['AUTH-086',14400000],['AUTH-087',14400001],['AUTH-088',28800000],['AUTH-089',86400000]] as const) {
  test(`${id} controlled suspension expires session`,async({page,audit})=>{
    await runSessionCase(page,audit,id,{refreshExpires:13524},{
      4:async()=>{await hidden(page);expect((await observe(page)).now).toBe(T);},
      5:async()=>{await page.clock.setSystemTime(new Date(T+duration));expect((await observe(page)).now).toBe(T+duration);},
      6:async()=>{await visible(page);},7:async()=>{await page.clock.runFor(1000);},
    });
  });
}
test('AUTH-090 resume before expiry and renew through mouse',async({page,audit})=>{
  const B=sessionToken(1500,'B');
  await runSessionCase(page,audit,'AUTH-090',{refreshExpires:13524},{4:async()=>{await at(page,60000);await hidden(page);},
    5:async()=>{await at(page,120000);},6:async()=>{await visible(page);},7:mouse,8:async()=>{await at(page,125000);},
    11:async()=>{await expect.poll(()=>equalsToken(page,'token',B)).toBe(true);},
  });
});
test('AUTH-091 resume after expiry requires manual Extend',async({page,audit})=>{
  await runSessionCase(page,audit,'AUTH-091',{refreshExpires:13524},{
    4:async()=>{await hidden(page);await page.clock.setSystemTime(new Date(T+1800000));},5:async()=>{await visible(page);},
    8:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
    10:async s=>{expect(s.requests.find(x=>x.endpoint==='relogin')?.refreshMatchesR).toBe(true);},
  });
});
test('AUTH-092 background rotation preserves newer access',async({page,audit})=>{
  const B=sessionToken(1800,'B');
  await runSessionCase(page,audit,'AUTH-092',{refreshExpires:13524},{
    4:async()=>{await hidden(page);await rotate(page,B);},5:async()=>{await at(page,1000000);},6:async()=>{await visible(page);},9:async()=>{expect(await equalsToken(page,'token',B)).toBe(true);},
  });
});
for(const id of ['AUTH-095','AUTH-096'] as const){
  test(`${id} relogin failure UI`,async({page,audit})=>{
    await runSessionCase(page,audit,id,{accessExpires:0,refreshExpires:600},{
      5:async s=>{s.control.reloginError=id==='AUTH-095'?'TOKEN_INVALID_EXPIRED':'Network Error';},
      6:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});},
    });
  });
}
test('AUTH-100 forward clock jump reconciles expiry',async({page,audit})=>{
  await runSessionCase(page,audit,'AUTH-100',{refreshExpires:13524},{4:async()=>{await hidden(page);},
    5:async()=>{await page.clock.setSystemTime(new Date(T+13525000));},6:async()=>{await visible(page);},8:async()=>{await page.clock.runFor(1000);},
  });
});

test('AUTH-082 access rotation does not postpone refresh expiry',async({page,audit})=>{
  await runSessionCase(page,audit,'AUTH-082',{refreshExpires:13524},{
    4:async()=>{await rotate(page,sessionToken(15000,'B'));},
    5:async()=>{await at(page,13524000,true);},7:async()=>{await page.clock.runFor(1000);},
  });
});
test('AUTH-094 late manual recovery retains refresh cutoff',async({page,audit})=>{
  const B=sessionToken(1500,'B');
  await runSessionCase(page,audit,'AUTH-094',{accessExpires:0,refreshExpires:600},{
    5:async s=>{expect(s.control.holdRelogin).toBe(true);},6:async()=>{await at(page,540000,true);},
    7:async s=>{await s.portal.sessionTimeoutDialog.extendButton.click({force:true});await expect.poll(()=>s.relogin.length).toBe(1);},
    9:async s=>{await s.acceptRelogin(B);await expect.poll(()=>equalsToken(page,'token',B)).toBe(true);},
    10:async()=>{expect(await equalsToken(page,'token',B)).toBe(true);},12:async()=>{await at(page,600000,true);},
    14:async()=>{await page.clock.runFor(1000);},
  });
});
test('AUTH-101 server expiry response after backward clock jump',async({page,audit})=>{
  let release!:()=>void;const held=new Promise<void>(resolve=>{release=resolve;});let pending=false;
  await runSessionCase(page,audit,'AUTH-101',{refreshExpires:13524},{
    4:async()=>{
      await page.route('**/api/auth/v2/sso/validate',async route=>{pending=true;await held;await route.fulfill({status:401,json:{message:'TOKEN_INVALID_EXPIRED'}});});
      await page.evaluate(async()=>{const m=await(window as unknown as SystemWindow).System.import('@fm/base');void m.Service.postService('/auth/v2/sso/validate',{singleUIAuthorization:m.Hooks.getHooks().store.token}).catch(()=>{});});
      await expect.poll(()=>pending).toBe(true);
    },
    5:async()=>{await page.clock.setSystemTime(new Date(T-3600000));},6:async()=>{release();},
    12:async()=>{expect((await observe(page)).accessPresent).toBe(false);},
  });
});

const leaveDialog=(page:Parameters<typeof visibility>[0])=>page.getByRole('dialog',{name:'Leave Now?',exact:true});
async function openLeave(s:Session){await s.portal.avatarButton.click({force:true});await s.portal.logoutMenuItem.click({force:true});await expect(leaveDialog(s.portal.page)).toBeVisible();}
const logoutButton=(page:Parameters<typeof visibility>[0])=>leaveDialog(page).getByRole('button',{name:'Logout',exact:true});
test('AUTH-102 cancelling logout preserves workspace state',async({page,audit})=>{
  let before='';
  await runSessionCase(page,audit,'AUTH-102',{}, {
    3:openLeave,
    4:async s=>{before=await page.getByTestId('workspaces-tab-WS-A').locator('input').inputValue();await audit.record('before-cancel',{name:before,accessPresent:(await observe(page)).accessPresent});},
    5:async()=>{await leaveDialog(page).getByRole('button',{name:'Cancel',exact:true}).click({force:true});},
    6:async()=>{await expect(leaveDialog(page)).toHaveCount(0);},
    8:async s=>{expect(await page.getByTestId('workspaces-tab-WS-A').locator('input').inputValue()).toBe(before);expect(await equalsToken(page,'token',s.accessA)).toBe(true);},
    9:async s=>{expect(s.count('logout')).toBe(0);},
  });
});
test('AUTH-103 profile logout clears session defaults',async({page,audit})=>{
  await runSessionCase(page,audit,'AUTH-103',{refreshExpires:13524},{
    3:openLeave,4:async()=>{await logoutButton(page).click({force:true});},5:async()=>{await page.clock.runFor(1000);},
    10:async()=>{
      const state=await page.evaluate(async()=>{const s=(await(window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store as Record<string,unknown>;
        return {token:s.token??null,refreshToken:s.refreshToken??null,user:s.user??null,expiredIn:s.expiredIn,userLoginTime:s.userLoginTime??null};});
      expect(state).toEqual({token:null,refreshToken:null,user:null,expiredIn:undefined,userLoginTime:null});await audit.record('cleared-session-defaults',state);
    },
  });
});
for(const id of ['AUTH-107','AUTH-108','AUTH-109','AUTH-110'] as const){
  test(`${id} logout transport failure keeps local logout`,async({page,audit})=>{
    await runSessionCase(page,audit,id,{}, {
      3:openLeave,
      4:async()=>{
        if(id!=='AUTH-108') await page.route('**/api/auth/v2/sso/logout',async route=>{if(id==='AUTH-110')return;await route.fulfill({status:503,json:{message:'Fixture logout unavailable'}});});
        if(id!=='AUTH-107') await page.route('**/api/ssiplus/imeta/logout',async route=>{if(id==='AUTH-110')return;await route.fulfill({status:503,json:{message:'Fixture logout unavailable'}});});
      },
      5:async()=>{await logoutButton(page).click({force:true});},6:async()=>{await page.clock.runFor(1000);},
      12:async()=>{await expect(page.getByRole('alert')).toHaveCount(0);},
    });
  });
}
for(const id of ['AUTH-113','AUTH-114'] as const){
  test(`${id} browser navigation cannot restore logged out access`,async({page,audit})=>{
    const steps=await audit.defineCase(id);let s!:Session;
    for(const step of steps)await audit.step(step.number,async()=>{
      if(step.number===1){s=await import('../support/auth-session.js').then(m=>m.sessionSetup(page,audit,{}));await openLeave(s);await logoutButton(page).click({force:true});await page.clock.runFor(1000);await s.login.expectVisible();return;}
      if(step.number===2){if(id==='AUTH-113')await page.goBack();else await page.reload();return;}
      if(step.number===7){expect(await page.evaluate(()=>Boolean(localStorage.getItem('SET_TOKEN')||sessionStorage.getItem('SET_TOKEN')))).toBe(false);return;}
      const handled=await import('../support/auth-session.js').then(m=>m.commonAssertion(page,s,step.text));if(!handled)throw new Error(`Missing ${id} step ${step.number}`);
    });
  });
}
