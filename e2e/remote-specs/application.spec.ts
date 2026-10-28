import { test, expect } from '@playwright/test';
import { writeFile } from 'node:fs/promises';
import { createPom } from '../catalog/actions.js';
import { loadTarget, targetSummary } from '../support/environment.js';

test('REMOTE-UI-001: Given a selected environment, When opening its URL, Then its expected UI area is visible', async ({ page }, testInfo) => {
  const target = loadTarget()!;
  testInfo.annotations.push({ type: 'audit-scope', description: 'CONFIGURED_APPLICATION' });
  const summary = { ...targetSummary(target),
    assertions: ['HTTP response is successful', 'The final origin matches the selected target', `${target.area} POM assertions pass`],
    limits: ['UI visibility does not establish token lifetime, business authorization, or full canonical case coverage.'] };
  const evidence = testInfo.outputPath('target.json');
  await writeFile(evidence, `${JSON.stringify(summary, null, 2)}\n`, { mode: 0o600 });
  await testInfo.attach('Selected environment and assertion scope', { path: evidence, contentType: 'application/json' });
  const response = await page.goto(target.targetUrl);
  expect(response?.ok(), 'The selected application URL must return a successful response.').toBe(true);
  expect(new URL(page.url()).origin).toBe(new URL(target.targetUrl).origin);
  const pom = createPom(page, target.prefix);
  await pom[target.area].expectVisible();
  if (target.area === 'portal' && target.workspaceName) await pom.portal.expectWorkspaceTabVisible(target.workspaceName);
  if (target.area === 'category') await pom.category.expectCoreColumnHeaders();
  expect(new URL(page.url()).origin, 'The asserted UI must belong to the selected target origin.').toBe(new URL(target.targetUrl).origin);
});
