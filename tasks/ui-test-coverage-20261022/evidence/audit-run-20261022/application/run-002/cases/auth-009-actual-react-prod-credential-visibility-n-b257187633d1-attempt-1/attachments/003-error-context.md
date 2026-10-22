# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: login-environment.spec.ts >> AUTH-009 actual React PROD credential visibility N
- Location: e2e/audit-specs/login-environment.spec.ts:108:3

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  getByTestId('MicroWebUI_base_login')
Expected: 1
Received: 0
Timeout:  5000ms

Call log:
  - Expect "toHaveCount" getByTestId('MicroWebUI_base_login') with timeout 5000ms
  - waiting for getByTestId('MicroWebUI_base_login')
    14 × locator resolved to 0 elements
       - unexpected value "0"

```

# Test source

```ts
  1  | import { expect, type Locator } from '@playwright/test';
  2  | import type { UiTarget } from '../catalog/ui-contracts.js';
  3  | 
  4  | export interface TargetInspection {
  5  |   readonly contract: UiTarget['contract'];
  6  |   readonly count: number;
  7  |   readonly visible: boolean | null;
  8  |   readonly enabled: boolean | null;
  9  |   readonly available: boolean;
  10 |   readonly reason: 'ready' | 'not-found' | 'ambiguous' | 'hidden' | 'disabled';
  11 | }
  12 | 
  13 | export async function inspectTarget(target: UiTarget): Promise<TargetInspection> {
  14 |   const count = await target.locator.count();
  15 |   if (count !== 1) {
  16 |     return { contract: target.contract, count, visible: null, enabled: null,
  17 |       available: false, reason: count === 0 ? 'not-found' : 'ambiguous' };
  18 |   }
  19 |   const visible = await target.locator.isVisible();
  20 |   const enabled = await target.locator.isEnabled();
  21 |   return { contract: target.contract, count, visible, enabled, available: visible && enabled,
  22 |     reason: !visible ? 'hidden' : !enabled ? 'disabled' : 'ready' };
  23 | }
  24 | 
  25 | export async function expectUniqueVisible(locator: Locator): Promise<void> {
> 26 |   await expect(locator).toHaveCount(1);
     |                         ^ Error: expect(locator).toHaveCount(expected) failed
  27 |   await expect(locator).toBeVisible();
  28 | }
  29 | 
  30 | export async function expectActionable(target: UiTarget, scope?: Locator): Promise<void> {
  31 |   if (scope) await expectUniqueVisible(scope);
  32 |   await expectUniqueVisible(target.locator);
  33 |   await expect(target.locator).toBeEnabled();
  34 | }
  35 | 
  36 | export const assertUniqueVisibleEnabled = expectActionable;
  37 | 
```