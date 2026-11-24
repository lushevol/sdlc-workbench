import { test } from '../support/audit-fixture.js';
import { runLoginCase } from '../support/login-audit.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual MFE React; intercepted accepted credential response; unsigned fixture JWT; WS-A seeded before navigation. No real identity acceptance.',
  serviceWorkers: 'block' });
for (const n of [16, 17, 18, 19, 20]) {
  const id = `AUTH-${String(n).padStart(3, '0')}`;
  test(`${id} actual React canonical steps`, async ({ page, audit }) => {
    await runLoginCase(id, page, audit);
  });
}
