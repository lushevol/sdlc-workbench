import { chromium, expect } from '@playwright/test';
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import { pathToFileURL, fileURLToPath } from 'node:url';
import path from 'node:path';

const directory = path.dirname(fileURLToPath(import.meta.url));
const report = path.resolve(directory, '../audit-run-20261022/report-006');
const browser = await chromium.launch({ channel: 'chromium', chromiumSandbox: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
const evidence = [];
try {
  await page.goto(pathToFileURL(path.join(report, 'cases/AUTH-084.html')).href);
  const latest = page.locator('.latest-attempt');
  const boundary = latest.locator('li[data-step="5"]');
  await boundary.scrollIntoViewIfNeeded();
  await expect(boundary.locator('.capture-context')).toContainText('T+597.999s (597999 ms); cutoff remaining 1 ms; Extend enabled; dialog visible');
  await expect(boundary.locator('img')).toBeVisible();
  await expect(latest.locator('li[data-step="1"] .capture-context').first()).toContainText('Extend absent; dialog absent');
  await expect(latest.locator('li[data-step="7"]')).toContainText('Image bytes match frame');
  await expect(page.locator('.attempt-history[open]')).toHaveCount(0);
  const screenshot = path.join(directory, 'gallery-auth084-boundary.png');
  await boundary.screenshot({ path: screenshot });
  evidence.push({ caseId: 'AUTH-084', screenshot, sha256: createHash('sha256').update(await readFile(screenshot)).digest('hex'),
    checked: ['Exact boundary context visible', 'Real screenshot visible', 'Preparatory Home frame separate', 'Unchanged image explained', 'Earlier attempts collapsed'] });

  await page.goto(pathToFileURL(path.join(report, 'cases/AUTH-116.html')).href);
  const contextStep = page.locator('.latest-attempt li[data-step="8"]');
  await contextStep.scrollIntoViewIfNeeded();
  await expect(contextStep).toContainText('Captured page: CTX-B');
  await expect(contextStep.locator('img')).toBeVisible();
  const contextScreenshot = path.join(directory, 'gallery-auth116-context-b.png');
  await contextStep.screenshot({ path: contextScreenshot });
  evidence.push({ caseId: 'AUTH-116', screenshot: contextScreenshot,
    sha256: createHash('sha256').update(await readFile(contextScreenshot)).digest('hex'),
    checked: ['CTX-B identity visible beside correct bound frame'] });

  await page.goto(pathToFileURL(path.join(report, 'index.html')).href);
  await page.locator('#search').fill('AUTH-084');
  await expect(page.locator('tbody tr:visible')).toHaveCount(1);
  await expect(page.locator('tbody tr:visible')).toContainText('CONTEXT_RECORDED');
  await writeFile(path.join(directory, 'gallery-ui-check.json'), JSON.stringify({ status: 'PASSED',
    checkedAt: new Date().toISOString(), report, browserVersion: browser.version(), evidence,
    limits: ['Presentation checks cover two corrected case pages and the index filter. They do not visually review every frame.'] }, null, 2) + '\n');
} finally { await browser.close(); }
