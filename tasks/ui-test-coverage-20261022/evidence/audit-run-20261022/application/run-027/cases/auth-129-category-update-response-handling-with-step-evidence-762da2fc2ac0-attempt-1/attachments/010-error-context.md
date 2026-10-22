# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-auth.spec.ts >> AUTH-129 Category update response handling with step evidence
- Location: e2e/audit-specs/admin-auth.spec.ts:10:3

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator: getByTestId('MicroWebUI_base_snackbar').locator('.MuiSnackbarContent-root[role="alert"]')
Expected: "Error happened, service is unavailable, pls check with support team: /api/auth/v1/fmo/admin/category/update: API request failed"
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toHaveText" getByTestId('MicroWebUI_base_snackbar').locator('.MuiSnackbarContent-root[role="alert"]') with timeout 5000ms
  - waiting for getByTestId('MicroWebUI_base_snackbar').locator('.MuiSnackbarContent-root[role="alert"]')

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 05:36 UTC
  - checkbox "Time Switch" [checked]
- button "User Profiles": A
- button "Share Feedback"
- main:
  - tablist "workspaces":
    - tab "WS-A" [selected]:
      - region "WS-A":
        - textbox "Workspace Name": WS-A
        - button "refresh"
    - button "Add Workspace"
  - tabpanel:
    - button "Create New Category"
    - grid:
      - button "Export"
      - rowgroup:
        - row "Actions Category Label Owner Verified? Updated At Updated By Record Id Order No":
          - columnheader "Actions"
          - columnheader "Category Label"
          - columnheader "Owner"
          - columnheader "Verified?"
          - columnheader "Updated At"
          - columnheader "Updated By"
          - columnheader "Record Id"
          - columnheader "Order No"
      - rowgroup:
        - row "Fixture Category TEST_OWNER Oct 22, 2026, 12:05:00 AM UI-ADMIN-01 101 7":
          - cell:
            - menu:
              - menuitem "Edit"
              - menuitem "Verify"
              - menuitem "Deactivate" [disabled]
              - menuitem "Audit"
          - cell "Fixture Category"
          - cell "TEST_OWNER"
          - cell
          - cell "Oct 22, 2026, 12:05:00 AM"
          - cell "UI-ADMIN-01"
          - cell "101"
          - cell "7"
      - paragraph: "Rows per page:"
      - 'combobox "Rows per page: 20"': "20"
      - paragraph: 1–1 of 1
      - button "Go to previous page" [disabled]
      - button "Go to next page" [disabled]
```

# Test source

```ts
  1  | import { test, expect } from '../support/audit-fixture.js';
  2  | import { AdminApp } from '../support/admin-app.js';
  3  | import { equalsToken, observe, type SystemWindow } from '../support/auth-session.js';
  4  | import { localPrefix } from '../support/local-app.js';
  5  | 
  6  | test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  7  |   auditFixture: 'Actual Category editor and Axios response handler. Controlled login supplies user-a with TEST_OWNER. Controlled update responses establish frontend error handling only. BFF authorization and storage are not verified.' });
  8  | 
  9  | for (const id of ['AUTH-128', 'AUTH-129', 'AUTH-131']) {
  10 |   test(`${id} Category update response handling with step evidence`, async ({ page, audit }) => {
  11 |     const steps = await audit.defineCase(id);
  12 |     const app = new AdminApp(page, 'Category', id);
  13 |     app.principal = 'user-a'; app.workspaceLabel = 'WS-A';
  14 |     let installed: string | undefined;
  15 |     let response: { status: number; body: string } | undefined;
  16 |     const alert = page.getByTestId(`${localPrefix}_snackbar`).locator('.MuiSnackbarContent-root[role="alert"]');
  17 |     for (const step of steps) await audit.step(step.number, async () => {
  18 |       const text = step.text;
  19 |       if (step.number === 1) {
  20 |         await app.setup();
  21 |         installed = await page.evaluate(async () => (await (window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store.token);
  22 |         expect(installed).toBeTruthy(); return;
  23 |       }
  24 |       if (text.includes('selected fixture tab') || text.startsWith('the tab labelled')) { await app.portal.expectWorkspaceTabVisible('WS-A'); return; }
  25 |       if (text.startsWith('User A has entity')) {
  26 |         const entities = await page.evaluate(async () => (await (window as unknown as SystemWindow).System.import('@fm/base')).Hooks.getHooks().store.entities);
  27 |         expect(entities).toEqual(expect.arrayContaining([expect.objectContaining({ name: 'FMO PORTAL ADMIN', roleName: 'TEST_OWNER' })])); return;
  28 |       }
  29 |       if (text.startsWith('the Category editor')) { await app.open(); await app.action('Edit').click(); await expect(app.dialog()).toContainText('edit ID: 101'); return; }
  30 |       if (text.startsWith('the Category update POST returns')) {
  31 |         response = id === 'AUTH-128' ? { status: 403, body: JSON.stringify({ message: 'Access denied' }) }
  32 |           : id === 'AUTH-129' ? { status: 401, body: '' } : { status: 503, body: 'Fixture service unavailable' };
  33 |         await page.route('**/api/auth/v1/fmo/admin/category/update', route => route.fulfill({ status: response!.status,
  34 |           contentType: id === 'AUTH-128' ? 'application/json' : 'text/plain', body: response!.body }));
  35 |         await audit.record('declared-controlled-update-response', { ...response, serverAuthorization: 'NOT_VERIFIED' }); return;
  36 |       }
  37 |       if (text.startsWith('User A clicks')) {
  38 |         const received = page.waitForResponse(value => new URL(value.url()).pathname === '/api/auth/v1/fmo/admin/category/update');
  39 |         await app.footerButton('Update').click();
  40 |         const actual = await received; response = { status: actual.status(), body: await actual.text() };
  41 |         await audit.record('received-update-response', response); return;
  42 |       }
  43 |       const message = /^the alert .* displays exactly "(.*)"$/.exec(text);
> 44 |       if (message) { await expect(alert).toHaveText(message[1]); return; }
     |                                          ^ Error: expect(locator).toHaveText(expected) failed
  45 |       if (text.startsWith('the POST to')) { expect(response?.status).toBe(403); expect(JSON.parse(response!.body)).not.toHaveProperty('data'); return; }
  46 |       if (text.startsWith('the visible Category record')) { await expect(app.row()).toHaveText(app.beforeValues); return; }
  47 |       if (text.startsWith('the installed access credential')) { expect(await equalsToken(page, 'token', installed)).toBe(true); return; }
  48 |       if (text.startsWith('the application global isLoading')) { await expect.poll(async () => (await observe(page)).isLoading).toBe(false); return; }
  49 |       throw new Error(`No Category auth binding for ${id} step ${step.number}: ${text}`);
  50 |     });
  51 |   });
  52 | }
  53 | 
```