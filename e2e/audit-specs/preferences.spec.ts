import { readFileSync } from 'node:fs';
import { test, expect } from '../support/audit-fixture.js';
import { acceptedLogin, blockExternal, loginToWorkspace } from '../support/local-app.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES', timezoneId: 'Asia/Singapore',
  auditFixture: 'Actual current React with controlled login/validation and seeded empty workspace. Preference storage is real browser storage. Clock cases use Playwright clock.' });

for (const id of ['UI-PREF-001', 'UI-PREF-002'] as const) {
  test(`${id} theme selection and persistence`, async ({ page, audit }) => {
    await blockExternal(page);
    await page.route('**/api/auth/v2/sso/validate', acceptedLogin);
    const portal = await loginToWorkspace(page);
    await portal.expectThemeLight(false);
    await audit.capture('dark-theme', 'The shell starts with its unchecked dark theme control.', `${id} Given`);
    await portal.setThemeLight(true);
    await portal.expectThemeLight(true);
    if (id === 'UI-PREF-002') {
      await audit.capture('saved-light-theme', 'Light theme is selected before browser reload.', `${id} Given`);
      await page.reload();
      await portal.expectVisible();
      await portal.expectThemeLight(true);
    }
    await expect(page.getByTestId('MicroWebUI_base_switch').getByText('light', { exact: true })).toBeVisible();
    expect(await page.evaluate(() => localStorage.getItem('SET_THEME'))).toBe('light');
    if (id === 'UI-PREF-001') {
      const logo = page.getByRole('img', { name: 'Markets Operations One logo', exact: true });
      const src = await logo.getAttribute('src');
      expect(src).toBeTruthy();
      const actual = src!.startsWith('data:')
        ? Buffer.from(src!.split(',')[1], src!.includes(';base64,') ? 'base64' : 'utf8')
        : await (await page.request.get(new URL(src!, page.url()).href)).body();
      const expected = readFileSync('repos/ui/mfe-base/src/components/AppBar/mo1_logo_light.svg');
      expect(actual.equals(expected)).toBe(true);
    }
    await audit.capture('light-theme-result', 'Light theme is checked and the light label is visible.', `${id} Then`);
  });
}

for (const id of ['UI-PREF-003', 'UI-PREF-004', 'UI-PREF-005'] as const) {
  test(`${id} time display uses the selected clock mode`, async ({ page, audit }) => {
    await blockExternal(page);
    await page.clock.install({ time: new Date('2026-10-22T00:05:00Z') });
    await loginToWorkspace(page);
    await page.clock.pauseAt(new Date('2026-10-22T00:05:01Z'));
    const control = page.getByRole('checkbox', { name: 'Time Switch', exact: true });
    await expect(control).toBeChecked();
    await expect(page.getByText('00:05 UTC', { exact: true })).toBeVisible();
    if (id === 'UI-PREF-004') {
      await control.click();
      await expect(control).not.toBeChecked();
      await expect(page.getByText('08:05 Local', { exact: true })).toBeVisible();
    }
    await audit.capture('clock-start', 'The clock shows the canonical initial mode and controlled minute.', `${id} Given`);
    if (id === 'UI-PREF-005') await page.clock.runFor(60000);
    else await control.click();
    const expectedText = id === 'UI-PREF-003' ? '08:05 Local' : id === 'UI-PREF-004' ? '00:05 UTC' : '00:06 UTC';
    await expect(page.getByText(expectedText, { exact: true })).toBeVisible();
    await expect(control).toBeChecked({ checked: id !== 'UI-PREF-003' });
    await audit.record('clock-assertions', { timezone: 'Asia/Singapore', expectedText,
      initialTime: '2026-10-22T00:05:00Z', controlledAdvanceSeconds: id === 'UI-PREF-005' ? 60 : 0,
      timer: 'PLAYWRIGHT_CONTROLLED', naturalElapsedTime: 'NOT_CLAIMED' });
    await audit.capture('clock-result', `The clock displays ${expectedText}.`, `${id} Then`);
  });
}
