# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: additional-boundaries.spec.ts >> UX-036 thirty workspace tabs remain operable
- Location: e2e/audit-specs/additional-boundaries.spec.ts:12:1

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByTestId('MicroWebUI_base_home').getByRole('tablist', { name: 'workspaces', exact: true }).getByRole('tab', { name: 'Workspace 30', exact: true }).getByRole('button', { name: 'refresh', exact: true })
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" getByTestId('MicroWebUI_base_home').getByRole('tablist', { name: 'workspaces', exact: true }).getByRole('tab', { name: 'Workspace 30', exact: true }).getByRole('button', { name: 'refresh', exact: true }) with timeout 5000ms
  - waiting for getByTestId('MicroWebUI_base_home').getByRole('tablist', { name: 'workspaces', exact: true }).getByRole('tab', { name: 'Workspace 30', exact: true }).getByRole('button', { name: 'refresh', exact: true })

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 05:48 UTC
  - checkbox "Time Switch" [checked]
- button "User Profiles": A
- button "Share Feedback"
- main:
  - tablist "workspaces":
    - tab "Workspace 1":
      - region "Workspace 1":
        - textbox "Workspace Name": Workspace 1
        - button "delete"
    - tab "Workspace 2":
      - region "Workspace 2":
        - textbox "Workspace Name": Workspace 2
        - button "delete"
    - tab "Workspace 3":
      - region "Workspace 3":
        - textbox "Workspace Name": Workspace 3
        - button "delete"
    - tab "Workspace 4":
      - region "Workspace 4":
        - textbox "Workspace Name": Workspace 4
        - button "delete"
    - tab "Workspace 5":
      - region "Workspace 5":
        - textbox "Workspace Name": Workspace 5
        - button "delete"
    - tab "Workspace 6":
      - region "Workspace 6":
        - textbox "Workspace Name": Workspace 6
        - button "delete"
    - tab "Workspace 7":
      - region "Workspace 7":
        - textbox "Workspace Name": Workspace 7
        - button "delete"
    - tab "Workspace 8":
      - region "Workspace 8":
        - textbox "Workspace Name": Workspace 8
        - button "delete"
    - tab "Workspace 9":
      - region "Workspace 9":
        - textbox "Workspace Name": Workspace 9
        - button "delete"
    - tab "Workspace 10":
      - region "Workspace 10":
        - textbox "Workspace Name": Workspace 10
        - button "delete"
    - tab "Workspace 11":
      - region "Workspace 11":
        - textbox "Workspace Name": Workspace 11
        - button "delete"
    - tab "Workspace 12":
      - region "Workspace 12":
        - textbox "Workspace Name": Workspace 12
        - button "delete"
    - tab "Workspace 13":
      - region "Workspace 13":
        - textbox "Workspace Name": Workspace 13
        - button "delete"
    - tab "Workspace 14":
      - region "Workspace 14":
        - textbox "Workspace Name": Workspace 14
        - button "delete"
    - tab "Workspace 15":
      - region "Workspace 15":
        - textbox "Workspace Name": Workspace 15
        - button "delete"
    - tab "Workspace 16":
      - region "Workspace 16":
        - textbox "Workspace Name": Workspace 16
        - button "delete"
    - tab "Workspace 17":
      - region "Workspace 17":
        - textbox "Workspace Name": Workspace 17
        - button "delete"
    - tab "Workspace 18":
      - region "Workspace 18":
        - textbox "Workspace Name": Workspace 18
        - button "delete"
    - tab "Workspace 19":
      - region "Workspace 19":
        - textbox "Workspace Name": Workspace 19
        - button "delete"
    - tab "Workspace 20":
      - region "Workspace 20":
        - textbox "Workspace Name": Workspace 20
        - button "delete"
    - tab "Workspace 21":
      - region "Workspace 21":
        - textbox "Workspace Name": Workspace 21
        - button "delete"
    - tab "Workspace 22":
      - region "Workspace 22":
        - textbox "Workspace Name": Workspace 22
        - button "delete"
    - tab "Workspace 23":
      - region "Workspace 23":
        - textbox "Workspace Name": Workspace 23
        - button "delete"
    - tab "Workspace 24":
      - region "Workspace 24":
        - textbox "Workspace Name": Workspace 24
        - button "delete"
    - tab "Workspace 25":
      - region "Workspace 25":
        - textbox "Workspace Name": Workspace 25
        - button "delete"
    - tab "Workspace 26":
      - region "Workspace 26":
        - textbox "Workspace Name": Workspace 26
        - button "delete"
    - tab "Workspace 27":
      - region "Workspace 27":
        - textbox "Workspace Name": Workspace 27
        - button "delete"
    - tab "Workspace 28":
      - region "Workspace 28":
        - textbox "Workspace Name": Workspace 28
        - button "delete"
    - tab "Workspace 29":
      - region "Workspace 29":
        - textbox "Workspace Name": Workspace 29
        - button "delete"
    - tab "Workspace 30" [selected]:
      - region "Workspace 30":
        - textbox "Workspace Name": Workspace 30
        - button "delete"
    - button "Add Workspace"
  - tabpanel:
    - paragraph: Start customizing your workspace
    - paragraph: find out what workspace preference options you have and how those options work.
    - button "Find tile"
```

# Test source

```ts
  1   | import { test, expect } from '../support/audit-fixture.js';
  2   | import { AdminApp, categoryRecord } from '../support/admin-app.js';
  3   | import { loginCatalog, type CatalogApp } from '../support/catalog-app.js';
  4   | import { equalsToken, type SystemWindow } from '../support/auth-session.js';
  5   | import { localPrefix, workspace } from '../support/local-app.js';
  6   | import { LoginPage } from '../pages/login.page.js';
  7   | import type { Page, Route } from '@playwright/test';
  8   | 
  9   | test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  10  |   auditFixture: 'Actual React shell, Category grid, and response handler. Controlled browser identity and service responses. Cross-tab rejection does not establish BFF global revocation. Spreadsheet formula execution requires a separate viewer.' });
  11  | 
  12  | test('UX-036 thirty workspace tabs remain operable', async ({ page, audit }) => {
  13  |   const steps = await audit.defineCase('UX-036');
  14  |   let app: CatalogApp;
  15  |   const last = () => app.portal.workspaceList.getByRole('tab', { name: 'Workspace 30', exact: true });
  16  |   for (const step of steps) await audit.step(step.number, async () => {
  17  |     if (step.number === 1) {
  18  |       app = await loginCatalog(page, { workspaces: Array.from({ length: 30 }, (_, i) => ({ ...workspace(`Workspace ${i + 1}`, `W${i + 1}`), isActive: i === 0 })) });
  19  |       await expect(app.allWorkspaceTabs()).toHaveCount(30); return;
  20  |     }
  21  |     if (step.number === 2) { await last().scrollIntoViewIfNeeded(); await last().click(); return; }
  22  |     if (step.number === 3) { await expect(last()).toHaveAttribute('aria-selected', 'true'); await expect(last()).toBeInViewport(); return; }
  23  |     const name = step.number === 4 ? 'refresh' : 'delete';
> 24  |     await last().hover(); await expect(last().getByRole('button', { name, exact: true })).toBeVisible();
      |                                                                                           ^ Error: expect(locator).toBeVisible() failed
  25  |     await expect(last().getByRole('button', { name, exact: true })).toBeEnabled();
  26  |   });
  27  | });
  28  | 
  29  | test('UX-043 captured CSV retains a spreadsheet-viewer prerequisite', async ({ page, audit }) => {
  30  |   const steps = await audit.defineCase('UX-043');
  31  |   const app = new AdminApp(page, 'Category', 'UX-043');
  32  |   for (const step of steps) {
  33  |     if (step.number === 3) {
  34  |       await audit.record('execution-blocker', { code: 'FORMULA_ENABLED_SPREADSHEET_VIEWER_UNAVAILABLE',
  35  |         blockedStep: step.number, owner: 'Unknown', nextAction: 'Provide a formula-enabled spreadsheet viewer for captured CSV imports.',
  36  |         consequence: 'Export and screenshot evidence exist. Formula execution and cell data types remain unverified.' });
  37  |       test.skip(true, 'FORMULA_ENABLED_SPREADSHEET_VIEWER_UNAVAILABLE: export completed; viewer steps cannot execute.');
  38  |     }
  39  |     await audit.step(step.number, async () => {
  40  |       if (step.number === 1) {
  41  |         app.rows = ['=1+1', '+1+1', '-1+1', '@SUM(1)'].map((label, i) => categoryRecord(101 + i, label));
  42  |         await app.setup(); await app.open();
  43  |         await expect(app.grid.locator('[data-id] [data-field="label"]')).toHaveText(['=1+1', '+1+1', '-1+1', '@SUM(1)']); return;
  44  |       }
  45  |       if (step.number === 2) {
  46  |         const waiting = page.waitForEvent('download'); await app.grid.getByRole('button', { name: 'Export', exact: true }).click();
  47  |         await page.getByRole('menuitem', { name: 'Download as CSV', exact: true }).click();
  48  |         const download = await waiting; const stream = await download.createReadStream(); const chunks: Buffer[] = [];
  49  |         for await (const chunk of stream!) chunks.push(Buffer.from(chunk));
  50  |         const bytes = Buffer.concat(chunks); await audit.record('formula-label-csv-artifact', { filename: download.suggestedFilename(), csv: bytes.toString('utf8'),
  51  |           limit: 'Raw CSV bytes do not establish spreadsheet data types or formula nonexecution.' });
  52  |         await test.info().attach('formula-label-export.csv', { body: bytes, contentType: 'text/csv' }); return;
  53  |       }
  54  |       throw new Error('Spreadsheet viewer prerequisite was not handled.');
  55  |     });
  56  |   }
  57  | });
  58  | 
  59  | test('AUTH-115 shared-session rejection across two live pages', async ({ page, context, audit }) => {
  60  |   const steps = await audit.defineCase('AUTH-115');
  61  |   const appA = new AdminApp(page, 'Category', 'AUTH-115'); appA.principal = 'user-a';
  62  |   let tabB: Page; let appB: AdminApp;
  63  |   let installed: string | undefined;
  64  |   let held: Route | undefined; let release!: () => void;
  65  |   const pending = new Promise<void>(resolve => { release = resolve; });
  66  |   const rejected = { message: 'TOKEN_INVALID_EXPIRED' };
  67  |   const logout = page.getByRole('dialog', { name: 'Leave Now?', exact: true });
  68  |   for (const step of steps) await audit.step(step.number, async () => {
  69  |     if (step.number === 1) {
  70  |       await appA.setup();
  71  |       installed = await page.evaluate(async () => (await (window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store.token);
  72  |       expect(installed).toBeTruthy();
  73  |       tabB = await context.newPage(); appB = new AdminApp(tabB, 'Category', 'AUTH-115'); appB.principal = 'user-a'; appB.access = installed!;
  74  |       await appB.setup(true); expect(await equalsToken(tabB, 'token', installed)).toBe(true);
  75  |       expect(new URL(page.url()).origin).toBe(new URL(tabB.url()).origin);
  76  |       await audit.record('shared-session-fixture', { session: 'SESSION-A', principal: 'user-a', sameContext: page.context() === tabB.context(), sameAccess: true,
  77  |         limit: 'Controlled credentials and rejection. Actual BFF revocation is not executed.' });
  78  |       await audit.capture('tab-b-initial', 'TAB-B authenticated under the shared SESSION-A fixture.', 'AUTH-115 step 1', tabB); return;
  79  |     }
  80  |     if (step.number === 2) {
  81  |       await appA.portal.clickAvatarButton(); await appA.portal.clickLogoutMenuItem(); await expect(logout).toBeVisible();
  82  |       const now = new Date(); await page.clock.install({ time: now }); await page.clock.pauseAt(new Date(now.getTime() + 60_000));
  83  |       await page.route('**/api/auth/v2/sso/logout', route => route.fulfill({ status: 200, json: {} }));
  84  |       await page.route('**/api/ssiplus/imeta/logout', route => route.fulfill({ status: 200, json: {} })); return;
  85  |     }
  86  |     if (step.number === 3) {
  87  |       await appB.open(); await appB.action('Edit').click(); await expect(appB.dialog()).toContainText('edit ID: 101');
  88  |       await tabB.route('**/api/auth/v1/fmo/admin/category/update', async route => { held = route; await pending;
  89  |         await route.fulfill({ status: 401, json: rejected }); });
  90  |     } else if (step.number === 4) { await logout.getByRole('button', { name: 'Logout', exact: true }).click(); return; }
  91  |     else if (step.number === 5) { await page.clock.runFor(1000); await new LoginPage(page, localPrefix).expectVisible(); return; }
  92  |     else if (step.number === 6) { await appB.footerButton('Update').click(); await expect.poll(() => Boolean(held)).toBe(true); }
  93  |     else if (step.number === 7) {
  94  |       const response = tabB.waitForResponse(value => new URL(value.url()).pathname === '/api/auth/v1/fmo/admin/category/update'); release();
  95  |       const actual = await response; expect(actual.status()).toBe(401); expect(await actual.json()).toEqual(rejected);
  96  |       await audit.record('rejected-category-response', { status: actual.status(), body: await actual.json() });
  97  |     } else if (step.number === 8) await expect(new LoginPage(tabB, localPrefix).usernameInput).toBeVisible();
  98  |     else if (step.number === 9) await expect(new LoginPage(tabB, localPrefix).passwordInput).toBeVisible();
  99  |     else if (step.number === 10) await expect(new LoginPage(tabB, localPrefix).signInButton).toBeVisible();
  100 |     else if (step.number === 11) await expect(tabB.getByRole('tablist', { name: 'workspaces', exact: true })).toHaveCount(0);
  101 |     else if (step.number === 12) await expect(tabB.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]')).toHaveText('Expired Session, please login again.');
  102 |     else if (step.number === 13) expect(rejected).not.toHaveProperty('data');
  103 |     else throw new Error(`No shared-session binding for step ${step.number}.`);
  104 |     await audit.capture(`tab-b-step-${step.number}`, `TAB-B state for canonical step ${step.number}: ${step.text}`, 'AUTH-115', tabB);
  105 |   });
  106 | });
  107 | 
```