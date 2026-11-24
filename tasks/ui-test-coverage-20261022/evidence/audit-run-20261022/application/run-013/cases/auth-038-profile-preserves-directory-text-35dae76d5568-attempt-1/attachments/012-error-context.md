# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: callback-profile.spec.ts >> AUTH-038 profile preserves directory text
- Location: e2e/audit-specs/callback-profile.spec.ts:103:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByTestId('entitlement-profile-label-box').getByText('user-a', { exact: true })
Expected: visible
Error: strict mode violation: getByTestId('entitlement-profile-label-box').getByText('user-a', { exact: true }) resolved to 2 elements:
    1) <div class="MuiTypography-root MuiTypography-h5 css-1mfwip3-MuiTypography-root">user-a</div> aka getByText('user-a').nth(1)
    2) <span class="MuiTypography-root MuiTypography-subtitle1 css-j9kgcn-MuiTypography-root">user-a</span> aka locator('span').filter({ hasText: 'user-a' })

Call log:
  - Expect "toBeVisible" getByTestId('entitlement-profile-label-box').getByText('user-a', { exact: true }) with timeout 5000ms
  - waiting for getByTestId('entitlement-profile-label-box').getByText('user-a', { exact: true })

```

# Page snapshot

```yaml
- generic [ref=e1]:
  - generic [ref=e4]:
    - generic [ref=e10]:
      - generic [ref=e11] [cursor=pointer]: New Tile
      - generic [ref=e19]:
        - text: dark
        - checkbox [ref=e22] [cursor=pointer]
      - group [ref=e26]:
        - generic [ref=e27]: 05:19 UTC
        - checkbox [checked] [ref=e30] [cursor=pointer]
      - button [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button [ref=e37] [cursor=pointer]
    - main [ref=e41]:
      - tablist [ref=e45]:
        - tab [selected] [ref=e47] [cursor=pointer]:
          - region [ref=e48]:
            - textbox [ref=e52]: WS-A
        - button [ref=e54] [cursor=pointer]
      - tabpanel [ref=e59]:
        - generic [ref=e63]:
          - paragraph [ref=e65]: Start customizing your workspace
          - paragraph [ref=e66]: find out what workspace preference options you have and how those options work.
          - button [ref=e67] [cursor=pointer]: Find tile
  - dialog [ref=e73]:
    - heading "User Profile resize Close" [level=2] [ref=e74]:
      - generic [ref=e75]:
        - generic [ref=e76]: User Profile
        - generic [ref=e77]:
          - button "resize" [ref=e78] [cursor=pointer]: Maximize
          - button "Close" [ref=e81] [cursor=pointer]
    - generic [ref=e86]:
      - generic [ref=e87]:
        - generic [ref=e89]:
          - generic [ref=e90]: user-a
          - generic [ref=e91]:
            - generic [ref=e92]: user-a
            - separator [ref=e93]
            - separator [ref=e94]
            - separator [ref=e95]
          - generic [ref=e96]:
            - generic [ref=e97]: "Login time:"
            - generic [ref=e98]: Oct 22, 2026, 5:19:16 AM Coordinated Universal Time
          - generic [ref=e99]:
            - generic [ref=e100]: "Session Expired time:"
            - generic [ref=e101]: Oct 22, 2026, 6:19:16 AM Coordinated Universal Time
        - img "Live from space album cover" [ref=e102]
      - generic [ref=e103]: Functional User Profile
    - button "resize" [ref=e105]
```

# Test source

```ts
  28  |       await page.route(/\/api\/auth\/v[23]\/sso\/login$/, async route => {
  29  |         requests.push({ pathname: new URL(route.request().url()).pathname, body: route.request().postDataJSON() });
  30  |         await route.fulfill({ status: 200, headers: { 'single-ui-authorization': fixtureAccess() }, json: response() });
  31  |       });
  32  |     });
  33  |     await audit.step(4, async () => { await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]); });
  34  |     await audit.step(5, async () => { await page.goto(callback); await portal.expectVisible(); });
  35  |     await audit.step(6, async () => { await portal.expectWorkspaceTabVisible('WS-A'); });
  36  |     await audit.step(7, async () => {
  37  |       expect(requests).toHaveLength(1); expect(requests[0].pathname).toBe(`/api/auth/${version}/sso/login`);
  38  |       expect(requests[0].body).toMatchObject(Object.fromEntries(new URLSearchParams(query)));
  39  |       await audit.record('callback-requests', requests);
  40  |     });
  41  |   });
  42  | }
  43  | 
  44  | test('AUTH-035 accepted callback removes query after entitlement validation', async ({ page, audit }) => {
  45  |   await audit.defineCase('AUTH-035');
  46  |   const portal = new PortalPage(page, localPrefix);
  47  |   let release!: () => void;
  48  |   const held = new Promise<void>(resolve => { release = resolve; });
  49  |   await audit.step(1, async () => {
  50  |     await blockExternal(page); await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
  51  |     await page.route('**/api/auth/v3/sso/login', async route => { await held;
  52  |       await route.fulfill({ status: 200, headers: { 'single-ui-authorization': fixtureAccess() }, json: response() }); });
  53  |     await page.goto(`${localBase}/?code=ENTRA-CODE-A`);
  54  |   });
  55  |   await audit.step(2, async () => { expect(workspace('WS-A', 'WS-A').label).toBe('WS-A'); });
  56  |   await audit.step(3, async () => { expect(new URL(page.url()).searchParams.get('code')).toBe('ENTRA-CODE-A'); await audit.record('callback-fixture', { entity: 'ENTITY-A', drawer: 'DRAWER-A' }); });
  57  |   await audit.step(4, async () => { release(); await portal.expectVisible(); });
  58  |   await audit.step(5, async () => { await expect.poll(() => new URL(page.url()).pathname + new URL(page.url()).search).toBe('/'); });
  59  |   await audit.step(6, async () => { await portal.expectWorkspaceTabVisible('WS-A'); });
  60  | });
  61  | 
  62  | for (const id of ['AUTH-034', 'AUTH-036'] as const) {
  63  |   test(`${id} rejected callback remains anonymous`, async ({ page, audit }) => {
  64  |     await audit.defineCase(id);
  65  |     let release!: () => void;
  66  |     const held = new Promise<void>(resolve => { release = resolve; });
  67  |     let count = 0;
  68  |     const login = new LoginPage(page, localPrefix);
  69  |     const alert = page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]');
  70  |     const tablist = page.getByRole('tablist', { name: 'workspaces', exact: true });
  71  |     await audit.step(1, async () => { await blockExternal(page); await openLogin(page); await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]); });
  72  |     const configure = async () => {
  73  |       await page.route('**/api/auth/v3/sso/login', async route => {
  74  |         count++; await held;
  75  |         if (id === 'AUTH-034') await route.fulfill({ status: 401, json: { message: 'AuthenticationException' } });
  76  |         else await route.fulfill({ status: 200, headers: { 'single-ui-authorization': fixtureAccess() },
  77  |           json: { userInfo: JSON.stringify({ sub: 'user-a' }), drawers, entities: [{ name: 'ENTITY-X', subjects: [] }] } });
  78  |       });
  79  |     };
  80  |     if (id === 'AUTH-034') {
  81  |       await audit.step(2, async () => { await audit.record('callback-url', { url: `${localBase}/?code=USED-CODE-A` }); });
  82  |       await audit.step(3, configure);
  83  |       await audit.step(4, async () => { await page.goto(`${localBase}/?code=USED-CODE-A`); await expect.poll(() => count).toBe(1); release(); await login.expectVisible(); });
  84  |       await audit.step(5, async () => { await expect(login.usernameInput).toBeVisible(); });
  85  |       await audit.step(6, async () => { await expect(login.passwordInput).toBeVisible(); });
  86  |       await audit.step(7, async () => { await expect(login.signInButton).toBeVisible(); });
  87  |       await audit.step(8, async () => { await expect(alert).toHaveText('Invalid username and password combination or SSO service is unavailable.'); });
  88  |       await audit.step(9, async () => { await expect(tablist).toHaveCount(0); });
  89  |     } else {
  90  |       await audit.step(2, async () => { await configure(); await page.goto(`${localBase}/?code=ENTRA-CODE-A`); await expect.poll(() => count).toBe(1); });
  91  |       await audit.step(3, async () => { release(); await login.expectVisible(); });
  92  |       await audit.step(4, async () => { await expect(login.usernameInput).toBeVisible(); });
  93  |       await audit.step(5, async () => { await expect(login.passwordInput).toBeVisible(); });
  94  |       await audit.step(6, async () => { await expect(login.signInButton).toBeVisible(); });
  95  |       await audit.step(7, async () => { await expect(tablist).toHaveCount(0); });
  96  |       await audit.step(8, async () => { await expect(alert).toHaveText('No entitlements found.'); });
  97  |     }
  98  |   });
  99  | }
  100 | 
  101 | for (const [id, fullName] of [['AUTH-037', 'Alex Example'], ['AUTH-038', 'user-a'], ['AUTH-039', 'Álex 王'],
  102 |   ['AUTH-040', '<img src=x onerror=alert(1)>']] as const) {
  103 |   test(`${id} profile preserves directory text`, async ({ page, audit }) => {
  104 |     await audit.defineCase(id);
  105 |     const login = new LoginPage(page, localPrefix);
  106 |     const portal = new PortalPage(page, localPrefix);
  107 |     const details = page.getByTestId('entitlement-profile-label-box');
  108 |     let alerts = 0;
  109 |     await audit.step(1, async () => {
  110 |       await blockExternal(page); await seedWorkspaces(page, [workspace('WS-A', 'WS-A')]);
  111 |       page.on('dialog', async dialog => { alerts++; await dialog.dismiss(); }); await openLogin(page);
  112 |     });
  113 |     await audit.step(2, async () => {
  114 |       await page.route('**/api/auth/v2/sso/login', route => route.fulfill({ status: 200,
  115 |         headers: { 'single-ui-authorization': fixtureAccess() },
  116 |         json: { userInfo: JSON.stringify({ sub: 'user-a', auth_time: Math.floor(Date.now() / 1000),
  117 |           oud: JSON.stringify({ fullName, userId: 'user-a' }) }), entities: [], drawers: [] } }));
  118 |       await audit.record('directory-response-fixture', { fullName, fallback: id === 'AUTH-038' ? 'BFF fallback substituted by response fixture' : null });
  119 |       await login.expectVisible();
  120 |     });
  121 |     await audit.step(3, async () => { await login.fillUsername(credentials.username); });
  122 |     await audit.step(4, async () => { await login.fillPassword(credentials.password); });
  123 |     await audit.step(5, async () => { await login.clickSignInButton(); await portal.expectVisible(); });
  124 |     let n = 6;
  125 |     if (id !== 'AUTH-040') { await audit.step(n++, async () => { await portal.expectWorkspaceTabVisible('WS-A'); }); }
  126 |     await audit.step(n++, async () => { await portal.clickAvatarButton(); });
  127 |     await audit.step(n++, async () => { await expect(portal.profileMenuItem.getByText(fullName, { exact: true })).toBeVisible(); await portal.clickProfileMenuItem(); });
> 128 |     await audit.step(n++, async () => { await expect(page.getByText('User Profile', { exact: true })).toBeVisible(); await expect(details.getByText(fullName, { exact: true })).toBeVisible(); });
      |                                                                                                                                                                                 ^ Error: expect(locator).toBeVisible() failed
  129 |     if (id === 'AUTH-039') await audit.step(n++, async () => { expect(await details.textContent()).not.toContain('�'); });
  130 |     if (id === 'AUTH-040') {
  131 |       await audit.step(n++, async () => { expect(alerts).toBe(0); });
  132 |       await audit.step(n++, async () => { await expect(details.locator('img')).toHaveCount(0); });
  133 |     }
  134 |     await audit.record('profile-assertions', { fullName, alertCount: alerts, BffFallback: 'NOT_VERIFIED', providerAcceptance: 'CONTROLLED_FIXTURE' });
  135 |   });
  136 | }
  137 | 
```