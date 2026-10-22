import type { LaunchOptions } from '@playwright/test';
import { fileURLToPath } from 'node:url';

// The browser adapter and this harness pin the same Playwright version.
// Package installation and browser provisioning remain explicit operations.
process.env.PLAYWRIGHT_BROWSERS_PATH ??= fileURLToPath(new URL('../adapters/browser/.browsers', import.meta.url));

export function browserLaunchOptions(): LaunchOptions {
  const browser = process.env.E2E_BROWSER ?? 'chromium';
  if (!['chromium', 'msedge'].includes(browser)) {
    throw new Error('E2E_BROWSER must be chromium or msedge.');
  }
  return {
    channel: browser,
    headless: process.env.E2E_HEADED !== '1',
    chromiumSandbox: true,
  };
}
