# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: callback-profile.spec.ts >> AUTH-036 rejected callback remains anonymous
- Location: e2e/audit-specs/callback-profile.spec.ts:50:3

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator: getByRole('alert')
Expected: "No entitlements found."
Error: strict mode violation: getByRole('alert') resolved to 2 elements:
    1) <div role="alert" direction="up" class="MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation6 MuiAlert-root MuiAlert-colorError MuiAlert-standardError MuiAlert-standard css-rgg0t8-MuiPaper-root-MuiAlert-root">…</div> aka getByRole('alert').first()
    2) <div role="alert" class="MuiPaper-root MuiPaper-elevation MuiPaper-elevation6 MuiSnackbarContent-root css-11hfw37-MuiPaper-root-MuiSnackbarContent-root">…</div> aka getByRole('alert').nth(1)

Call log:
  - Expect "toHaveText" getByRole('alert') with timeout 5000ms
  - waiting for getByRole('alert')

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
          - textbox "Enter Username" [ref=e17]
        - generic [ref=e18]:
          - generic [ref=e19]: Password
          - textbox "Enter Password" [ref=e25]
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
      - generic [ref=e48]: No entitlements found.
    - button "Close" [ref=e50] [cursor=pointer]
```

# Test source

```ts
  1   | import { test, expect } from '../support/audit-fixture.js';
  2   | import { blockExternal, credentials, fixtureAccess, localBase, localPrefix, openLogin, seedWorkspaces, workspace } from '../support/local-app.js';
  3   | import { LoginPage } from '../pages/login.page.js';
  4   | import { PortalPage } from '../pages/portal.page.js';
  5   | 
  6   | test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  7   |   auditFixture: 'Current actual React; controlled SSO/login HTTP responses; unsigned fixture access token; seeded empty WS-A; external requests blocked. Provider acceptance and BFF fallback are not verified.' });
  8   | 
  9   | const drawers = [{ id: 'DRAWER-A', label: 'Audit catalog', tiles: [{ title: 'Audit tile', entity: ['ENTITY-A'],
  10  |   container: '@fm/audit-unused', module: '/unused', tile: '/unused', subject: 'AUDIT', isTemplate: true }] }];
  11  | 
  12  | for (const [id, query, version] of [
  13  |   ['AUTH-030', 'code=ENTRA-CODE-A', 'v3'],
  14  |   ['AUTH-031', 'code=MFA-CODE-A&iss=ISSUER-A&client_id=CLIENT-A', 'v2'],
  15  |   ['AUTH-032', 'code=MFA-CODE-A&iss=ISSUER-A', 'v2'],
  16  |   ['AUTH-033', 'code=MFA-CODE-A&client_id=CLIENT-A', 'v2'],
  17  |   ['AUTH-035', 'code=ENTRA-CODE-A', 'v3'],
  18  | ] as const) {
  19  |   test(`${id} callback route and restored workspace`, async ({ page, audit }) => {
  20  |     await blockExternal(page);
  21  |     await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
  22  |     const requests: { pathname: string; body: unknown }[] = [];
  23  |     let release!: () => void;
  24  |     const held = new Promise<void>(resolve => { release = resolve; });
  25  |     await page.route(/\/api\/auth\/v[23]\/sso\/login$/, async route => {
  26  |       requests.push({ pathname: new URL(route.request().url()).pathname, body: route.request().postDataJSON() });
  27  |       await held;
  28  |       await route.fulfill({ status: 200, headers: { 'single-ui-authorization': fixtureAccess() },
  29  |         json: { userInfo: JSON.stringify({ sub: 'user-a', fullName: 'Audit User A' }), drawers,
  30  |           entities: [{ name: 'ENTITY-A', subjects: [] }] } });
  31  |     });
  32  |     await page.goto(`${localBase}/?${query}`);
  33  |     await expect.poll(() => requests.length).toBe(1);
  34  |     await audit.capture('callback-pending', 'The callback URL is loaded and its controlled exchange is pending.', `${id} When`);
  35  |     release();
  36  |     const portal = new PortalPage(page, localPrefix);
  37  |     await portal.expectVisible();
  38  |     await portal.expectWorkspaceTabVisible('WS-A');
  39  |     expect(requests).toHaveLength(1);
  40  |     expect(requests[0].pathname).toBe(`/api/auth/${version}/sso/login`);
  41  |     const expected = Object.fromEntries(new URLSearchParams(query));
  42  |     expect(requests[0].body).toMatchObject(expected);
  43  |     await expect.poll(() => new URL(page.url()).pathname + new URL(page.url()).search).toBe('/');
  44  |     await audit.record('callback-assertions', { requests, resultingPath: '/', providerAcceptance: 'CONTROLLED_FIXTURE' });
  45  |     await audit.capture('callback-home', 'WS-A is visible and the callback query has been removed.', `${id} Then`);
  46  |   });
  47  | }
  48  | 
  49  | for (const id of ['AUTH-034', 'AUTH-036'] as const) {
  50  |   test(`${id} rejected callback remains anonymous`, async ({ page, audit }) => {
  51  |     await blockExternal(page);
  52  |     await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
  53  |     let release!: () => void;
  54  |     const held = new Promise<void>(resolve => { release = resolve; });
  55  |     let count = 0;
  56  |     await page.route('**/api/auth/v3/sso/login', async route => {
  57  |       count++;
  58  |       await held;
  59  |       if (id === 'AUTH-034') await route.fulfill({ status: 401, json: { message: 'AuthenticationException' } });
  60  |       else await route.fulfill({ status: 200, headers: { 'single-ui-authorization': fixtureAccess() },
  61  |         json: { userInfo: JSON.stringify({ sub: 'user-a' }), drawers,
  62  |           entities: [{ name: 'ENTITY-X', subjects: [] }] } });
  63  |     });
  64  |     await page.goto(`${localBase}/?code=${id === 'AUTH-034' ? 'USED-CODE-A' : 'ENTRA-CODE-A'}`);
  65  |     await expect.poll(() => count).toBe(1);
  66  |     await audit.capture('callback-pending', 'The callback exchange is held before its rejected result.', `${id} Given`);
  67  |     release();
  68  |     const login = new LoginPage(page, localPrefix);
  69  |     await login.expectVisible();
  70  |     await expect(login.usernameInput).toBeVisible();
  71  |     await expect(login.passwordInput).toBeVisible();
  72  |     await expect(login.signInButton).toBeVisible();
  73  |     await expect(page.getByRole('tablist', { name: 'workspaces', exact: true })).toHaveCount(0);
> 74  |     await expect(page.getByRole('alert')).toHaveText(id === 'AUTH-034'
      |                                           ^ Error: expect(locator).toHaveText(expected) failed
  75  |       ? 'Invalid username and password combination or SSO service is unavailable.' : 'No entitlements found.');
  76  |     await audit.capture('callback-rejected', 'The exact rejection alert appears with login controls and no workspace tablist.', `${id} Then`);
  77  |   });
  78  | }
  79  | 
  80  | for (const [id, fullName] of [['AUTH-037', 'Alex Example'], ['AUTH-039', 'Álex 王'],
  81  |   ['AUTH-040', '<img src=x onerror=alert(1)>']] as const) {
  82  |   test(`${id} profile display preserves directory text`, async ({ page, audit }) => {
  83  |     await blockExternal(page);
  84  |     await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
  85  |     let alerts = 0;
  86  |     page.on('dialog', async dialog => { alerts++; await dialog.dismiss(); });
  87  |     await page.route('**/api/auth/v2/sso/login', route => route.fulfill({ status: 200,
  88  |       headers: { 'single-ui-authorization': fixtureAccess() },
  89  |       json: { userInfo: JSON.stringify({ sub: 'user-a', auth_time: Math.floor(Date.now() / 1000),
  90  |         oud: JSON.stringify({ fullName, userId: 'user-a' }) }), entities: [], drawers: [] } }));
  91  |     const login = await openLogin(page);
  92  |     await audit.capture('start-login', 'The login form is visible before the directory fixture is returned.', `${id} Given`);
  93  |     await login.fillUsername(credentials.username);
  94  |     await login.fillPassword(credentials.password);
  95  |     await login.clickSignInButton();
  96  |     const portal = new PortalPage(page, localPrefix);
  97  |     await portal.expectWorkspaceTabVisible('WS-A');
  98  |     await portal.clickAvatarButton();
  99  |     await expect(portal.profileMenuItem.getByText(fullName, { exact: true })).toBeVisible();
  100 |     await audit.capture('profile-menu', 'The avatar menu displays the fixture directory name.', `${id} When`);
  101 |     await portal.clickProfileMenuItem();
  102 |     // The source Modal uses a title node without an accessible dialog role.
  103 |     const profile = page.locator('[class*="profile"]').filter({ has: page.getByText('User Profile', { exact: true }) });
  104 |     await expect(page.getByText('User Profile', { exact: true })).toBeVisible();
  105 |     const details = page.getByTestId('entitlement-profile-label-box');
  106 |     await expect(details.getByText(fullName, { exact: true })).toBeVisible();
  107 |     expect(await details.textContent()).not.toContain('�');
  108 |     expect(alerts).toBe(0);
  109 |     if (id === 'AUTH-040') await expect(details.locator('img')).toHaveCount(0);
  110 |     await audit.record('profile-assertions', { fullName, alertCount: alerts,
  111 |       directoryMarkupImagesInNameRegion: 0, policyApproval: id === 'AUTH-037' ? 'IMPLEMENTATION_CHARACTERIZATION' : 'PROPOSED_EXPECTATION_ONLY' });
  112 |     await audit.capture('profile-details', 'User Profile displays the exact directory name as text.', `${id} Then`);
  113 |   });
  114 | }
  115 | 
```