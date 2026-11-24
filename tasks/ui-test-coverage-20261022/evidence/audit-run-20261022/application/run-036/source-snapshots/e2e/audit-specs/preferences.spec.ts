import { readFileSync } from 'node:fs';
import { test, expect } from '../support/audit-fixture.js';
import { acceptedLogin, blockExternal, loginToWorkspace } from '../support/local-app.js';
import { type PortalPage } from '../pages/portal.page.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES', timezoneId: 'Asia/Singapore',
  auditFixture: 'Actual current React with controlled login/validation/activity renewal and seeded empty workspace. Preference storage is real browser storage. Clock cases use Playwright clock.' });

for (const id of ['UI-PREF-001', 'UI-PREF-002'] as const) {
  test(`${id} theme selection and persistence`, async ({ page, audit }) => {
    await audit.defineCase(id);
    let portal: PortalPage;
    await audit.step(1, async () => {
      await blockExternal(page);
      await page.route('**/api/auth/v2/sso/validate', acceptedLogin);
      portal = await loginToWorkspace(page);
    });
    await audit.step(2, async () => {
      await portal.expectThemeLight(false);
      if (id === 'UI-PREF-002') {
        await portal.setThemeLight(true); await portal.expectThemeLight(true);
        expect(await page.evaluate(() => localStorage.getItem('SET_THEME'))).toBe('light');
      }
    });
    await audit.step(3, async () => {
      if (id === 'UI-PREF-001') await portal.themeCheckbox.click();
      else { await page.reload(); await portal.expectVisible(); }
    });
    await audit.step(4, async () => { await portal.expectThemeLight(true); });
    await audit.step(5, async () => { await expect(page.getByTestId('MicroWebUI_base_switch').getByText('light', { exact: true })).toBeVisible(); });
    if (id === 'UI-PREF-001') await audit.step(6, async () => {
      const logo = page.getByRole('img', { name: 'Markets Operations One logo', exact: true });
      const src = await logo.getAttribute('src');
      expect(src).toBeTruthy();
      const actual = src!.startsWith('data:')
        ? Buffer.from(src!.split(',')[1], src!.includes(';base64,') ? 'base64' : 'utf8')
        : await (await page.request.get(new URL(src!, page.url()).href)).body();
      const expected = readFileSync('repos/ui/mfe-base/src/components/AppBar/mo1_logo_light.svg');
      expect(actual.equals(expected)).toBe(true);
    });
  });
}

for (const id of ['UI-PREF-003', 'UI-PREF-004', 'UI-PREF-005'] as const) {
  test(`${id} time display uses the selected clock mode`, async ({ page, audit }) => {
    await audit.defineCase(id);
    const control = page.getByRole('checkbox', { name: 'Time Switch', exact: true });
    await audit.step(1, async () => {
      await blockExternal(page);
      await page.clock.install({ time: new Date('2026-10-22T00:05:00Z') });
      await loginToWorkspace(page);
    });
    await audit.step(2, async () => {
      await page.clock.pauseAt(new Date('2026-10-22T00:05:01Z'));
      await expect(control).toBeChecked();
      await expect(page.getByText('00:05 UTC', { exact: true })).toBeVisible();
      if (id === 'UI-PREF-004') {
        await control.click(); await expect(control).not.toBeChecked();
        await expect(page.getByText('08:05 Local', { exact: true })).toBeVisible();
      }
    });
    await audit.step(3, async () => {
      if (id === 'UI-PREF-005') await page.clock.runFor(60000);
      else await control.click();
    });
    const expectedText = id === 'UI-PREF-003' ? '08:05 Local' : id === 'UI-PREF-004' ? '00:05 UTC' : '00:06 UTC';
    await audit.step(4, async () => { await expect(page.getByText(expectedText, { exact: true })).toBeVisible(); });
    await audit.step(5, async () => { await expect(control).toBeChecked({ checked: id !== 'UI-PREF-003' }); });
    await audit.record('clock-assertions', { timezone: 'Asia/Singapore', expectedText,
      initialTime: '2026-10-22T00:05:00Z', controlledAdvanceSeconds: id === 'UI-PREF-005' ? 60 : 0,
      timer: 'PLAYWRIGHT_CONTROLLED', naturalElapsedTime: 'NOT_CLAIMED' });
  });
}
