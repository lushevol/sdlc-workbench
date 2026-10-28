import { defineConfig } from '@playwright/test';
import path from 'node:path';
import { browserLaunchOptions } from './browser-config.js';
import { loadTarget, targetSummary, TargetConfigurationError } from './support/environment.js';

const target = loadTarget();
if (!target) throw new TargetConfigurationError('Select E2E_ENVIRONMENT for deployed application tests.');
process.env.E2E_AUDIT_OUTPUT ??= path.resolve('.workbench/e2e-remote', target.name,
  new Date().toISOString().replace(/[:.]/g, '-'));
process.env.E2E_AUDIT_SCOPE = 'CONFIGURED_APPLICATION';
process.env.E2E_AUDIT_FIXTURE = 'Configured application and real responses; no test response replacement or storage seed.';
const output = path.resolve(process.env.E2E_AUDIT_OUTPUT);

export default defineConfig({
  testDir: './remote-specs',
  outputDir: path.join(output, 'playwright-artifacts'),
  timeout: 30_000,
  expect: { timeout: 8_000 },
  forbidOnly: true,
  fullyParallel: false,
  retries: 0,
  workers: 1,
  metadata: { executionTarget: targetSummary(target) },
  reporter: [
    ['line'],
    ['./audit.reporter.ts', { output, excludedSources: [
      path.resolve(process.env.E2E_ENVIRONMENTS_FILE ?? '.workbench/e2e-environments.json'),
      ...(target.storageState ? [target.storageState] : []),
    ] }],
    ['html', { outputFolder: path.join(output, 'html-report'), open: 'never' }],
  ],
  use: {
    browserName: 'chromium',
    launchOptions: browserLaunchOptions(),
    storageState: target.storageState,
    serviceWorkers: 'block',
    trace: 'off', screenshot: 'off', video: 'off',
  },
});
