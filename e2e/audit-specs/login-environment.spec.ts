import { test } from '../support/audit-fixture.js';
import { runLoginCase } from '../support/login-audit.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual MFE React; controlled login API responses; hostname proxy preserves source environment decisions. No real identity or deployment acceptance.',
  serviceWorkers: 'block' });
for (const n of [...Array.from({ length: 15 }, (_, i) => i + 1), ...Array.from({ length: 8 }, (_, i) => i + 21)]) {
  const id = `AUTH-${String(n).padStart(3, '0')}`;
  test(`${id} actual React canonical steps`, async ({ page, audit }) => {
    test.setTimeout(n === 27 ? 100000 : 60000);
    await runLoginCase(id, page, audit);
  });
}
