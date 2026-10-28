import { defineConfig } from '@playwright/test';
import { browserLaunchOptions } from './browser-config.js';
import { rejectEnvironmentForFixtures } from './support/environment.js';

rejectEnvironmentForFixtures();
const launchOptions = browserLaunchOptions();

export default defineConfig({
  testDir: './specs',
  outputDir: './test-results',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['line'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
  ],
  use: {
    browserName: 'chromium',
    headless: launchOptions.headless,
    launchOptions,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
});
