# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: bff-admin.spec.ts >> BFF-ADM-005 current BFF administration through actual UI
- Location: e2e/audit-specs/bff-admin.spec.ts:10:2

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  getByTestId('MicroWebUI_base_home')
Expected: 1
Received: 0
Timeout:  5000ms

Call log:
  - Expect "toHaveCount" getByTestId('MicroWebUI_base_home') with timeout 5000ms
  - waiting for getByTestId('MicroWebUI_base_home')
    14 × locator resolved to 0 elements
       - unexpected value "0"

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - generic [ref=e5]:
    - main [ref=e7]:
      - heading "Sign In" [level=3] [ref=e8]
      - generic [ref=e9]:
        - generic [ref=e10]:
          - generic [ref=e11]: Username
          - textbox "Enter Username" [ref=e17]: admin-a
        - generic [ref=e18]:
          - generic [ref=e19]: Password
          - textbox "Enter Password" [ref=e25]: FixturePass1!
        - button "Sign In" [ref=e26] [cursor=pointer]
        - separator [ref=e27]
      - link "Sign In With SSO" [ref=e29] [cursor=pointer]:
        - /url: https://login.microsoftonline.com/cd823f6b-31c5-4241-b504-3707cbc03fb7/oauth2/v2.0/authorize?client_id=80c8b904-1b64-443b-a651-7548764d534d&response_type=code&redirect_uri=http://localhost:8128/mfa/callback&response_mode=query&scope=openid+profile+offline_access+email
    - main [ref=e31]:
      - tabpanel [ref=e32]:
        - generic [ref=e33]:
          - heading "Markets Operations One" [level=2] [ref=e34]
          - paragraph [ref=e35]: Markets Operations One Portal (MO1) is a single, evolving workspace for Operations processing, integrating post-trade applications, and progressively delivering a more connected, intelligent, and efficient processing.
      - tablist "login tabs" [ref=e39]:
        - tab "login-tabpanel" [selected] [ref=e40] [cursor=pointer]
  - alert [ref=e42]:
    - alert [ref=e47]:
      - generic [ref=e48]: Invalid username and password combination or SSO service is unavailable.
    - button "Close" [ref=e50] [cursor=pointer]
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