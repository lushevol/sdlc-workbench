import { test, expect } from '../support/audit-fixture.js';
import { at, equalsToken, observe, runSessionCase, sessionToken, T, type SystemWindow } from '../support/auth-session.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES', serviceWorkers: 'block',
  auditFixture: 'Actual MFE; Playwright clock; controlled API responses; unsigned browser-only credentials. No natural lifecycle or BFF expiry claim.' });

for (const [id, target] of [['AUTH-043', 875000], ['AUTH-044', 874999]] as const) {
  test(`${id} recovery acquisition timer boundary`, async ({ page, audit }) => {
    await runSessionCase(page, audit, id, {}, {
      4: async () => { expect((await observe(page)).visibility).toBe('visible'); },
      5: async () => { await at(page, target); },
      ...(id === 'AUTH-043' ? { 9: async () => { expect((await observe(page)).accessExpiryMs).toBe(T + 900000); } } : {}),
    });
  });
}
for (const [id, target] of [['AUTH-076', 900000], ['AUTH-077', 899999]] as const) {
  test(`${id} access expiry boundary`, async ({ page, audit }) => {
    await runSessionCase(page, audit, id, { refreshExpires: 13524 }, {
      4: async () => { await at(page, target); },
      ...(id === 'AUTH-076' ? { 6: async s => { await expect(s.portal.sessionTimeoutDialog.dialog).toHaveCount(1); } } : {}),
    });
  });
}
test('AUTH-080 Logout clears local access after delay', async ({ page, audit }) => {
  await runSessionCase(page, audit, 'AUTH-080', { accessExpires: 0, refreshExpires: 600 }, {
    5: async s => { await s.portal.sessionTimeoutDialog.logoutButton.click({ force: true }); },
    6: async () => { await page.clock.runFor(1000); },
    12: async () => { expect(await page.evaluate(() => [localStorage.getItem('SET_TOKEN'), sessionStorage.getItem('SET_TOKEN')])).toEqual([null, null]); },
  });
});
test('AUTH-081 expiry without refresh logs out', async ({ page, audit }) => {
  await runSessionCase(page, audit, 'AUTH-081', { acquisitionFails: true }, {
    3: async s => { await at(page, 875000); await expect.poll(() => s.count('refreshtoken')).toBe(1); expect((await observe(page)).refreshPresent).toBe(false); },
    4: async () => { await at(page, 900000); },
    5: async s => { await s.portal.sessionTimeoutDialog.expectVisible(); expect((await observe(page)).refreshPresent).toBe(false); },
    6: async () => { await page.clock.runFor(1000); },
  });
});
for (const [id, target] of [['AUTH-083', 598000], ['AUTH-084', 597999]] as const) {
  test(`${id} timeout refresh cutoff`, async ({ page, audit }) => {
    await runSessionCase(page, audit, id, { accessExpires: 0, refreshExpires: 600 }, {
      5: async () => { await at(page, target, true); },
      ...(id === 'AUTH-083' ? { 8: async () => { await at(page, 599000); } } : {}),
    });
  });
}
test('AUTH-078 manual Extend installs B and validates B', async ({ page, audit }) => {
  const B = sessionToken(900, 'B'); let validation = false;
  await runSessionCase(page, audit, 'AUTH-078', { accessExpires: 0, refreshExpires: 600 }, {
    5: async s => { expect(s.control.holdRelogin).toBe(true); },
    6: async s => { await s.portal.sessionTimeoutDialog.extendButton.click({ force: true }); await expect.poll(() => s.relogin.length).toBe(1); },
    9: async s => { expect(s.requests.find(x => x.endpoint === 'relogin')?.refreshMatchesR).toBe(true); },
    10: async s => { await s.acceptRelogin(B); await expect.poll(() => equalsToken(page, 'token', B)).toBe(true); },
    12: async () => { expect(await equalsToken(page, 'token', B)).toBe(true); },
    13: async () => {
      await page.route('**/api/auth/v2/sso/validate', async route => {
        validation = route.request().postDataJSON()?.singleUIAuthorization === B;
        await route.fulfill({ status: 200, json: { result: validation } });
      });
      const result = await page.evaluate(async () => {
        const m = await (window as unknown as SystemWindow).System.import('@fm/base');
        const r = await m.Service.postService('/auth/v2/sso/validate', { singleUIAuthorization: m.Hooks.getHooks().store.token });
        return (r.data as {result:boolean}).result;
      });
      expect(result).toBe(true);
    },
    14: async () => { expect(validation).toBe(true); },
  });
});
