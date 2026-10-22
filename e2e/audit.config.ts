import { defineConfig } from '@playwright/test';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { browserLaunchOptions } from './browser-config.js';

const workspace = fileURLToPath(new URL('../', import.meta.url));
process.env.E2E_AUDIT_OUTPUT ??= path.join(workspace,
  'tasks/ui-test-coverage-20261022/evidence/audit-run-20261022/harness',
  new Date().toISOString().replace(/[:.]/g, '-'));
const output = path.resolve(process.env.E2E_AUDIT_OUTPUT);

export default defineConfig({
  testDir: process.env.E2E_AUDIT_TEST_DIR ?? './specs',
  outputDir: path.join(output, 'playwright-artifacts'),
  timeout: 30000,
  expect: { timeout: 5000 },
  fullyParallel: true,
  forbidOnly: true,
  retries: 0,
  workers: 2,
  reporter: [
    ['line'],
    ['./audit.reporter.ts', { output }],
    ['json', { outputFile: path.join(output, 'playwright-report.json') }],
    ['html', { outputFolder: path.join(output, 'html-report'), open: 'never' }],
  ],
  use: {
    browserName: 'chromium',
    viewport: { width: 1440, height: 1000 },
    deviceScaleFactor: 1,
    actionTimeout: 8000,
    navigationTimeout: 10000,
    launchOptions: browserLaunchOptions(),
    trace: 'on',
    screenshot: 'on',
    video: 'off',
  },
});
