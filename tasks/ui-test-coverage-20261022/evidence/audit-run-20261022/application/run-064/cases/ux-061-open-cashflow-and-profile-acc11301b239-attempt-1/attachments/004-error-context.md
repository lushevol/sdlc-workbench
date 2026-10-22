# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: browser-compatibility.spec.ts >> UX-061 firefox >> UX-061 open Cashflow and profile
- Location: e2e/audit-specs/browser-compatibility.spec.ts:21:3

# Error details

```
Error: page.goto: NS_ERROR_NET_ERROR_RESPONSE
Call log:
  - navigating to "http://localhost:8128/?show_normal_login=Y", waiting until "load"

```

# Page snapshot

```yaml
- article [ref=e3]:
  - generic [ref=e6]:
    - heading "Looks like there’s a problem with this site" [level=1] [ref=e7]
    - paragraph [ref=e8]:
      - text: The server at
      - strong [ref=e9]: localhost:8128
      - text: "sent back an error: 503 Service Unavailable"
    - generic [ref=e10]:
      - heading "What can you do about it?" [level=3] [ref=e11]
      - list [ref=e12]:
        - listitem [ref=e13]: Check to make sure you’ve typed the website address correctly.
        - listitem [ref=e14]: The site could be temporarily unavailable or too busy. Try again in a few moments.
    - button "Try Again" [ref=e17]
```

# Test source

```ts
  1  | import { type Page, type Route } from '@playwright/test';
  2  | import { LoginPage } from '../pages/login.page.js';
  3  | import { PortalPage } from '../pages/portal.page.js';
  4  | 
  5  | export const localBase = 'http://localhost:8128';
  6  | export const localPrefix = 'MicroWebUI_base';
  7  | export const credentials = { username: 'user-a', password: 'FixturePass1!' };
  8  | export const workspace = (label = 'Workspace 1', id = 'W1') => ({ id, label, isActive: true, containers: [] });
  9  | 
  10 | // This deliberately unsigned token is a browser fixture. No service accepts it as proof of identity.
  11 | export function fixtureAccess(): string {
  12 |   const now = Math.floor(Date.now() / 1000);
  13 |   const encode = (value: unknown) => Buffer.from(JSON.stringify(value)).toString('base64url');
  14 |   return `Bearer ${encode({ alg: 'none', typ: 'JWT' })}.${encode({ sub: 'UI-USER-01', iat: now, exp: now + 3600 })}.fixture`;
  15 | }
  16 | 
  17 | export async function blockExternal(page: Page): Promise<string[]> {
  18 |   const blocked: string[] = [];
  19 |   await page.context().route('**/*', async route => {
  20 |     const url = new URL(route.request().url());
  21 |     if (['localhost', '127.0.0.1', '[::1]'].includes(url.hostname)) await route.continue();
  22 |     else { blocked.push(`${url.origin}${url.pathname}`); await route.abort('blockedbyclient'); }
  23 |   });
  24 |   return blocked;
  25 | }
  26 | 
  27 | export async function seedWorkspaces(page: Page, values: ReturnType<typeof workspace>[]): Promise<void> {
  28 |   await page.addInitScript(values => {
  29 |     localStorage.setItem('SET_WORKSPACES', JSON.stringify(values));
  30 |   }, values);
  31 | }
  32 | 
  33 | export async function acceptedLogin(route: Route): Promise<void> {
  34 |   await route.fulfill({ status: 200, headers: { 'content-type': 'application/json',
  35 |     'single-ui-authorization': fixtureAccess() },
  36 |     body: JSON.stringify({ userInfo: JSON.stringify({ sub: 'UI-USER-01', fullName: 'Audit User A' }),
  37 |       entities: [], drawers: [], result: true }) });
  38 | }
  39 | 
  40 | export async function openLogin(page: Page): Promise<LoginPage> {
> 41 |   await page.goto(`${localBase}/?show_normal_login=Y`);
     |              ^ Error: page.goto: NS_ERROR_NET_ERROR_RESPONSE
  42 |   const login = new LoginPage(page, localPrefix);
  43 |   await login.expectVisible();
  44 |   return login;
  45 | }
  46 | 
  47 | export async function loginToWorkspace(page: Page, label = 'Workspace 1', id = 'W1'): Promise<PortalPage> {
  48 |   await seedWorkspaces(page, [workspace(label, id)]);
  49 |   await page.route('**/api/auth/v2/sso/login', acceptedLogin);
  50 |   await page.route('**/api/auth/v2/sso/extend', acceptedLogin);
  51 |   const login = await openLogin(page);
  52 |   await login.fillUsername(credentials.username);
  53 |   await login.fillPassword(credentials.password);
  54 |   await login.clickSignInButton();
  55 |   const portal = new PortalPage(page, localPrefix);
  56 |   await portal.expectVisible();
  57 |   await portal.expectWorkspaceTabVisible(label);
  58 |   return portal;
  59 | }
  60 | 
```