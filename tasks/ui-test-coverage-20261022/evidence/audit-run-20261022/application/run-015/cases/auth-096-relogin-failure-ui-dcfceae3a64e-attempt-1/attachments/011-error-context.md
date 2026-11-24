# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-session-expanded.spec.ts >> AUTH-096 relogin failure UI
- Location: e2e/audit-specs/auth-session-expanded.spec.ts:182:3

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  getByRole('dialog', { name: 'Your session has been expired', exact: true })
Expected: 1
Received: 0
Timeout:  5000ms

Call log:
  - Expect "toHaveCount" getByRole('dialog', { name: 'Your session has been expired', exact: true }) with timeout 5000ms
  - waiting for getByRole('dialog', { name: 'Your session has been expired', exact: true })
    14 × locator resolved to 0 elements
       - unexpected value "0"

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - generic [ref=e4]:
    - generic [ref=e7]:
      - img "Markets Operations One logo" [ref=e9]
      - generic [ref=e10]:
        - generic [ref=e11] [cursor=pointer]:
          - img "new tile" [ref=e13]
          - generic [ref=e14]: New Tile
        - generic [ref=e15]:
          - img "dark" [ref=e17]
          - generic [ref=e19]:
            - text: dark
            - checkbox "Theme Switch" [ref=e22] [cursor=pointer]
        - group [ref=e26]:
          - generic [ref=e27]: 00:00 UTC
          - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
        - button "User Profiles" [ref=e34] [cursor=pointer]:
          - generic [ref=e35]: A
        - button "Share Feedback" [ref=e37] [cursor=pointer]
    - main [ref=e41]:
      - tablist "workspaces" [ref=e45]:
        - tab [selected] [ref=e47] [cursor=pointer]:
          - region "WS-A" [ref=e48]:
            - textbox "Workspace Name" [ref=e52]: WS-A
        - button "Add Workspace" [ref=e54] [cursor=pointer]
      - tabpanel [ref=e59]:
        - generic [ref=e63]:
          - paragraph [ref=e65]: Start customizing your workspace
          - paragraph [ref=e66]: find out what workspace preference options you have and how those options work.
          - button [ref=e67] [cursor=pointer]
  - alert [ref=e71]:
    - alert [ref=e76]:
      - generic [ref=e77]: "Error happened, service is unavailable, pls check with support team: /api/auth/v2/sso/relogin: API request failed"
    - button "Close" [ref=e79] [cursor=pointer]
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