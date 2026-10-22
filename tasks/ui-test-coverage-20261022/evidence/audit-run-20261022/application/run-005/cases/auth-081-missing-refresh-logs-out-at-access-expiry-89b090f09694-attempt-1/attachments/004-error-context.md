# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: session-timing.spec.ts >> AUTH-081 missing refresh logs out at access expiry
- Location: e2e/audit-specs/session-timing.spec.ts:209:1

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator: getByRole('alert')
Expected: "/api/auth/v2/sso/refreshtoken : Request failed with status code 503"
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
          - generic [ref=e27]: 00:14 UTC
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
      - generic [ref=e77]: "/api/auth/v2/sso/refreshtoken : Request failed with status code 503"
    - button "Close" [ref=e79] [cursor=pointer]
```

# Test source

```ts
  113 |   if (refreshR) {
  114 |     // The fixture invokes the actual exported acquisition service to establish the canonical refresh setup.
  115 |     await page.evaluate(async () => {
  116 |       const module = await (window as unknown as BrowserWithSystem).System.import('@fm/base');
  117 |       await module.Service.getRefreshToken();
  118 |     });
  119 |     await expect.poll(async () => (await storeObservation(page, accessA, refreshR)).refreshEqualsR).toBe(true);
  120 |   }
  121 |   await page.clock.pauseAt(new Date(T));
  122 |   const initial = await storeObservation(page, accessA, refreshR);
  123 |   expect(initial.documentVisibility).toBe('visible');
  124 |   expect(initial.accessEqualsA).toBe(true);
  125 |   expect(initial.refreshEqualsR).toBe(true);
  126 |   await audit.record('controlled-setup', { ...initial, accessExpiryOffsetSeconds: options.accessExpires ?? 900,
  127 |     refreshExpiryOffsetSeconds: options.refreshExpires ?? null,
  128 |     refreshSetup: refreshR ? 'Fixture called actual exported acquisition service before T; counters reset afterward.' : 'No refresh credential at T.',
  129 |     noMouseActivityAfterSetup: true, credentials: 'Unsigned fixture values; equality booleans only in observation records.' });
  130 |   requests.length = 0;
  131 |   await audit.capture('controlled-session-start', 'WS-A is present at controlled time T before the named timer action.', ref(id));
  132 |   return { portal, accessA, refreshR, requests, pending };
  133 | }
  134 | 
  135 | test('AUTH-043 acquire recovery at T+875 without moving access expiry', async ({ page, audit }) => {
  136 |   const { portal, accessA, requests } = await setup(page, audit, 'AUTH-043');
  137 |   await runTo(page, 875000);
  138 |   await expect.poll(() => requests.filter(request => request.endpoint === 'refreshtoken').length).toBe(1);
  139 |   await portal.expectWorkspaceTabVisible('WS-A');
  140 |   await portal.sessionTimeoutDialog.expectAbsent();
  141 |   const observation = await storeObservation(page, accessA);
  142 |   expect(observation.accessExpiryMs).toBe(T + 900000);
  143 |   expect(observation.accessEqualsA).toBe(true);
  144 |   await audit.record('deadline-assertions', { requests, observation,
  145 |     expectedRefreshPostCount: 1, expectedAccessExpiryMs: T + 900000 });
  146 |   await audit.capture('recovery-acquired-before-expiry', 'WS-A remains visible without the expiry dialog at T+875 seconds.', ref('AUTH-043'));
  147 | });
  148 | 
  149 | test('AUTH-044 do not acquire recovery at T+874.999', async ({ page, audit }) => {
  150 |   const { portal, accessA, requests } = await setup(page, audit, 'AUTH-044');
  151 |   await runTo(page, 874999);
  152 |   expect(requests.filter(request => request.endpoint === 'refreshtoken')).toHaveLength(0);
  153 |   await portal.expectWorkspaceTabVisible('WS-A');
  154 |   await portal.sessionTimeoutDialog.expectAbsent();
  155 |   await audit.record('deadline-assertions', { requests, observation: await storeObservation(page, accessA),
  156 |     expectedRefreshPostCount: 0 });
  157 |   await audit.capture('before-acquisition-deadline', 'WS-A remains visible without the expiry dialog immediately before acquisition.', ref('AUTH-044'));
  158 | });
  159 | 
  160 | for (const [id, target] of [['AUTH-076', 900000], ['AUTH-077', 899999]] as const) {
  161 |   test(`${id} access expiry boundary at T+${target}ms`, async ({ page, audit }) => {
  162 |     const { portal, accessA, refreshR, requests } = await setup(page, audit, id, { refreshExpires: 13524 });
  163 |     await runTo(page, target);
  164 |     if (id === 'AUTH-076') {
  165 |       await portal.sessionTimeoutDialog.expectVisible();
  166 |       await expect(portal.sessionTimeoutDialog.dialog).toHaveCount(1);
  167 |       await expect(portal.sessionTimeoutDialog.extendButton).toBeVisible();
  168 |       await expect(portal.sessionTimeoutDialog.logoutButton).toBeVisible();
  169 |       expect(requests.filter(request => request.endpoint === 'relogin')).toHaveLength(0);
  170 |     } else {
  171 |       await portal.sessionTimeoutDialog.expectAbsent();
  172 |       await portal.expectWorkspaceTabVisible('WS-A');
  173 |     }
  174 |     await audit.record('expiry-boundary-assertions', { requests, observation: await storeObservation(page, accessA, refreshR),
  175 |       targetOffsetMs: target, expiryDialogExpected: id === 'AUTH-076' });
  176 |     await audit.capture('access-expiry-boundary', id === 'AUTH-076'
  177 |       ? 'Exactly one expiry dialog presents Extend and Logout at T+900 seconds.'
  178 |       : 'WS-A is visible without the expiry dialog at T+899.999 seconds.', ref(id));
  179 |   });
  180 | }
  181 | 
  182 | async function expectSignedOut(page: Page, portal: PortalPage): Promise<void> {
  183 |   const login = new LoginPage(page, localPrefix);
  184 |   await login.expectVisible();
  185 |   await expect(login.usernameInput).toBeVisible();
  186 |   await expect(login.passwordInput).toBeVisible();
  187 |   await expect(login.signInButton).toBeVisible();
  188 |   await expect(portal.workspaceList).toHaveCount(0);
  189 | }
  190 | 
  191 | test('AUTH-080 Logout clears local access after the 1000ms delay', async ({ page, audit }) => {
  192 |   const { portal, accessA, refreshR, requests } = await setup(page, audit, 'AUTH-080', { accessExpires: 0, refreshExpires: 600 });
  193 |   await portal.sessionTimeoutDialog.expectVisible();
  194 |   await audit.capture('expiry-decision', 'The expired-access dialog presents Logout and Extend.', ref('AUTH-080'));
  195 |   await expect(portal.sessionTimeoutDialog.logoutButton).toBeEnabled();
  196 |   // Forced pointer dispatch avoids Playwright stability frames while requestAnimationFrame is paused.
  197 |   await portal.sessionTimeoutDialog.logoutButton.click({ force: true });
  198 |   await audit.capture('logout-delay-pending', 'Logout has started while the 1000-millisecond application delay is pending.', ref('AUTH-080'));
  199 |   await page.clock.runFor(1000);
  200 |   await expectSignedOut(page, portal);
  201 |   await portal.sessionTimeoutDialog.expectAbsent();
  202 |   const storage = await page.evaluate(() => ({ localAccessPresent: Boolean(localStorage.getItem('SET_TOKEN')),
  203 |     sessionAccessPresent: Boolean(sessionStorage.getItem('SET_TOKEN')) }));
  204 |   expect(storage).toEqual({ localAccessPresent: false, sessionAccessPresent: false });
  205 |   await audit.record('logout-assertions', { requests, storage, observation: await storeObservation(page, accessA, refreshR) });
  206 |   await audit.capture('signed-out-after-delay', 'Login controls are visible without the workspace tablist or expiry dialog.', ref('AUTH-080'));
  207 | });
  208 | 
  209 | test('AUTH-081 missing refresh logs out at access expiry', async ({ page, audit }) => {
  210 |   const { portal, accessA, requests } = await setup(page, audit, 'AUTH-081', { acquisitionFails: true });
  211 |   await runTo(page, 875000);
  212 |   await expect.poll(() => requests.filter(request => request.endpoint === 'refreshtoken').length).toBe(1);
> 213 |   await expect(page.getByRole('alert')).toHaveText('/api/auth/v2/sso/refreshtoken : Request failed with status code 503');
      |                                         ^ Error: expect(locator).toHaveText(expected) failed
  214 |   const beforeExpiry = await storeObservation(page, accessA);
  215 |   expect(beforeExpiry.refreshPresent).toBe(false);
  216 |   await audit.capture('recovery-acquisition-failed', 'WS-A remains visible after the controlled acquisition failure.', ref('AUTH-081'));
  217 |   await runTo(page, 900000);
  218 |   await portal.sessionTimeoutDialog.expectVisible();
  219 |   await audit.capture('expiry-without-refresh', 'The expiry component mounted without a refresh credential.', ref('AUTH-081'));
  220 |   await page.clock.runFor(1000);
  221 |   await expectSignedOut(page, portal);
  222 |   expect(requests.filter(request => request.endpoint === 'relogin')).toHaveLength(0);
  223 |   await audit.record('missing-refresh-assertions', { requests, observation: await storeObservation(page, accessA),
  224 |     recoveryCredentialAbsentBeforeExpiry: true, expectedReloginPosts: 0 });
  225 |   await audit.capture('signed-out-without-recovery', 'Login controls replace Home after the logout delay.', ref('AUTH-081'));
  226 | });
  227 | 
  228 | for (const [id, target] of [['AUTH-083', 598000], ['AUTH-084', 597999]] as const) {
  229 |   test(`${id} open-dialog refresh cutoff at T+${target}ms`, async ({ page, audit }) => {
  230 |     const { portal, accessA, refreshR, requests } = await setup(page, audit, id, { accessExpires: 0, refreshExpires: 600 });
  231 |     await portal.sessionTimeoutDialog.expectVisible();
  232 |     await audit.capture('expiry-decision', 'The expired-access dialog is visible before its refresh cutoff.', ref(id));
  233 |     await runTo(page, target);
  234 |     if (id === 'AUTH-084') {
  235 |       await expect(portal.sessionTimeoutDialog.extendButton).toBeEnabled();
  236 |       await portal.sessionTimeoutDialog.expectVisible();
  237 |     } else {
  238 |       await expect(portal.sessionTimeoutDialog.extendButton).toBeDisabled();
  239 |       const state = await storeObservation(page, accessA, refreshR);
  240 |       expect(state.isOnLogout).toBe(true);
  241 |       await audit.record('cutoff-state', state);
  242 |       await audit.capture('cutoff-starts-logout', 'Extend is disabled at the two-second refresh cutoff.', ref(id));
  243 |       await runTo(page, 599000);
  244 |       await expectSignedOut(page, portal);
  245 |     }
  246 |     await audit.record('cutoff-assertions', { requests, observation: await storeObservation(page, accessA, refreshR), targetOffsetMs: target });
  247 |     await audit.capture('refresh-cutoff-result', id === 'AUTH-084'
  248 |       ? 'Extend is available at T+597.999 seconds.' : 'Login controls replace Home at T+599 seconds.', ref(id));
  249 |   });
  250 | }
  251 | 
  252 | test('AUTH-078 manual Extend installs response B and sends controlled validation with B', async ({ page, audit }) => {
  253 |   const { portal, accessA, refreshR, requests, pending } = await setup(page, audit, 'AUTH-078', { accessExpires: 0, refreshExpires: 600 });
  254 |   await portal.sessionTimeoutDialog.expectVisible();
  255 |   await audit.capture('expiry-decision', 'The expiration dialog is visible with a valid browser refresh fixture.', ref('AUTH-078'));
  256 |   await expect(portal.sessionTimeoutDialog.extendButton).toBeEnabled();
  257 |   await portal.sessionTimeoutDialog.extendButton.click({ force: true });
  258 |   await expect.poll(() => pending.length).toBe(1);
  259 |   await portal.sessionTimeoutDialog.expectAbsent();
  260 |   const recoveryRequests = requests.filter(request => request.endpoint === 'relogin');
  261 |   expect(recoveryRequests).toHaveLength(1);
  262 |   expect(recoveryRequests[0].refreshMatchesR).toBe(true);
  263 |   await audit.capture('recovery-pending', 'The dialog is absent while the controlled relogin response remains pending.', ref('AUTH-078'));
  264 |   const accessB = token(900, 'B');
  265 |   await pending[0].fulfill({ status: 200, headers: { 'single-ui-authorization': accessB },
  266 |     json: { result: true, entities: [], userInfo: JSON.stringify({ sub: 'user-a', fullName: 'Audit User A' }) } });
  267 |   await portal.expectWorkspaceTabVisible('WS-A');
  268 |   await expect.poll(async () => page.evaluate(async expected => {
  269 |     const module = await (window as unknown as BrowserWithSystem).System.import('@fm/base');
  270 |     return module.Hooks.getHooks().store.token === expected;
  271 |   }, accessB)).toBe(true);
  272 |   // This is an independent application HTTP operation after response installation.
  273 |   let validationMatchesB = false;
  274 |   await page.route('**/api/auth/v2/sso/validate', async route => {
  275 |     validationMatchesB = route.request().postDataJSON()?.singleUIAuthorization === accessB;
  276 |     await route.fulfill({ status: 200, json: { result: validationMatchesB } });
  277 |   });
  278 |   const validation = await page.evaluate(async expected => {
  279 |     const module = await (window as unknown as BrowserWithSystem).System.import('@fm/base');
  280 |     const installed = module.Hooks.getHooks().store.token;
  281 |     const response = await module.Service.postService('/auth/v2/sso/validate', { singleUIAuthorization: installed },
  282 |       { headers: { 'show-loading': 'false' } });
  283 |     return { installedMatchesB: installed === expected, result: response.data.result === true };
  284 |   }, accessB);
  285 |   expect(validation).toEqual({ installedMatchesB: true, result: true });
  286 |   expect(validationMatchesB).toBe(true);
  287 |   await audit.record('recovery-independent-assertions', { reloginPosts: recoveryRequests.length,
  288 |     refreshHeaderEqualsR: recoveryRequests[0].refreshMatchesR, installedAccessEqualsB: validation.installedMatchesB,
  289 |     controlledValidationBodyEqualsB: validationMatchesB, controlledValidationResult: validation.result,
  290 |     responseAcceptance: 'CONTROLLED_FIXTURE', realAuthenticationAcceptance: 'NOT_VERIFIED',
  291 |     observation: await storeObservation(page, accessA, refreshR) });
  292 |   await audit.capture('recovered-and-validated', 'WS-A is visible after installing B and the controlled validation operation.', ref('AUTH-078'));
  293 | });
  294 | 
```