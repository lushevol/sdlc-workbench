# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: ux-shell.spec.ts >> UX-004 keyboard and accessibility probe
- Location: e2e/audit-specs/ux-shell.spec.ts:39:3

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator:  locator('#workspaces-tabpanel-1')
Expected: visible
Received: hidden
Timeout:  5000ms

Call log:
  - Expect "toBeVisible" locator('#workspaces-tabpanel-1') with timeout 5000ms
  - waiting for locator('#workspaces-tabpanel-1')
    14 × locator resolved to <div hidden="" tabid="W1" role="tabpanel" id="workspaces-tabpanel-1" data-testid="workspaces-tabpanel-1" class="MicroWebUI_base_home-tabpanel">…</div>
       - unexpected value "hidden"

```

```yaml
- img "Markets Operations One logo"
- img "new tile"
- text: New Tile
- img "dark"
- text: dark
- checkbox "Theme Switch"
- group:
  - text: 05:23 UTC
  - checkbox "Time Switch" [checked]
- button "User Profiles": A
- button "Share Feedback"
- main:
  - tablist "workspaces":
    - tab "Home":
      - region "Home":
        - textbox "Workspace Name": Home
        - button "delete"
    - tab "Cashflow" [selected]:
      - region "Cashflow":
        - textbox "Workspace Name": Cashflow
        - button "delete"
    - button "Add Workspace"
  - tabpanel:
    - paragraph: Start customizing your workspace
    - paragraph: find out what workspace preference options you have and how those options work.
    - button "Find tile"
```

# Test source

```ts
  1   | import { test, expect, type AuditCapture } from '../support/audit-fixture.js';
  2   | import type { Locator, Page } from '@playwright/test';
  3   | import { CatalogApp, fixtureCategory, fixtureContainer, fixtureTile, loginCatalog } from '../support/catalog-app.js';
  4   | import { localPrefix } from '../support/local-app.js';
  5   | 
  6   | test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  7   |   auditFixture: 'Actual React shell. Controlled catalog, user identity, photo failures, and SystemJS tenant. Chromium only. Accessibility and layout outcomes are proposed probes; no approved conformance standard is inferred.' });
  8   | const profileRoot = (page: Page) => page.getByTestId(`${localPrefix}_Dialog`).filter({ has: page.getByText('User Profile', { exact: true }) });
  9   | const closeProfile = (page: Page) => profileRoot(page).getByTestId(`${localPrefix}_Dialog-close`);
  10  | async function profile(app: CatalogApp): Promise<void> { await app.portal.clickAvatarButton(); await app.openProfile(); }
  11  | async function focusWithin(root: Locator): Promise<boolean> { return root.evaluate(node => node.contains(document.activeElement)); }
  12  | async function traceFocus(page: Page, audit: AuditCapture, backwards = false, count = 12) {
  13  |   const trace: Record<string, unknown>[] = [];
  14  |   for (let index = 0; index < count; index++) {
  15  |     await page.keyboard.press(backwards ? 'Shift+Tab' : 'Tab');
  16  |     const item = await page.evaluate(() => {
  17  |       const node = document.activeElement as HTMLElement;
  18  |       const style = getComputedStyle(node);
  19  |       const parent = node.closest('.MuiSwitch-root,.MuiButtonBase-root') ?? node;
  20  |       const parentStyle = getComputedStyle(parent);
  21  |       return { tag: node.tagName, id: node.id, role: node.getAttribute('role'), aria: node.getAttribute('aria-label'),
  22  |         testId: node.getAttribute('data-testid'), text: node.textContent?.slice(0, 120),
  23  |         header: Boolean(node.closest('[data-testid="MicroWebUI_base_appBar"]')),
  24  |         profile: Boolean(node.closest('[data-testid="MicroWebUI_base_Dialog"]')),
  25  |         indicator: (style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) > 0)
  26  |           || style.boxShadow !== 'none' || parentStyle.boxShadow !== 'none'
  27  |           || Boolean(node.closest('.Mui-focusVisible')),
  28  |         outline: style.outline, boxShadow: style.boxShadow, parentBoxShadow: parentStyle.boxShadow };
  29  |     });
  30  |     trace.push(item);
  31  |     await audit.capture(`focus-${backwards ? 'reverse' : 'forward'}-${index + 1}`, 'Live keyboard focus checkpoint; computed CSS is retained separately.');
  32  |   }
  33  |   await audit.record(`focus-trace-${backwards ? 'reverse' : 'forward'}`, trace);
  34  |   return trace;
  35  | }
  36  | 
  37  | for (const n of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 19, 20]) {
  38  |   const id = `UX-${String(n).padStart(3, '0')}`;
  39  |   test(`${id} keyboard and accessibility probe`, async ({ page, audit }) => {
  40  |     const steps = await audit.defineCase(id);
  41  |     let app: CatalogApp;
  42  |     let forward: Record<string, unknown>[] = [], reverse: Record<string, unknown>[] = [];
  43  |     const tab = () => app.portal.workspace('W1');
  44  |     for (const step of steps) await audit.step(step.number, async () => {
  45  |       const text = step.text;
  46  |       if (step.number === 1) {
  47  |         app = await loginCatalog(page, [4,5,6,7].includes(n) ? { workspaces: [
  48  |           { id: 'W1', label: n === 4 || n === 6 ? 'Home' : 'Cashflow', isActive: true, containers: [fixtureContainer({registerRefresh:true})] },
  49  |           { id: 'W2', label: 'Cashflow', isActive: true, containers: [] }] } : {});
  50  |         if ([4,5,6,7].includes(n)) {
  51  |           if (n === 4) { await tab().tab.focus(); await expect(tab().tab).toBeFocused(); }
  52  |         }
  53  |         if ([8,9,20].includes(n)) await app.portal.setThemeLight(n !== 8);
  54  |         if (n === 8) await app.portal.themeCheckbox.focus();
  55  |         if ([2,3].includes(n)) {
  56  |           await app.newTile.focus();
  57  |           await expect(app.newTile).toBeFocused();
  58  |           if (n === 3) { await page.keyboard.press('Enter'); await expect(app.drawer).toBeVisible(); }
  59  |         }
  60  |         if (n === 10) { await app.portal.avatarButton.focus(); await expect(app.portal.avatarButton).toBeFocused(); }
  61  |         if ([11,12,13].includes(n)) await profile(app);
  62  |         return;
  63  |       }
  64  |       if (text.includes('presses "Tab"') && !text.includes('Shift')) { forward = await traceFocus(page,audit,false,n === 11 ? 16 : 10); return; }
  65  |       if (text.includes('presses "Shift+Tab"')) { reverse = await traceFocus(page,audit,true,16); return; }
  66  |       if (text.includes('focus trace') || text.includes('Each traced control')) {
  67  |         if (n === 11) expect((text.startsWith('The reverse') ? reverse : forward).every(value => value.profile)).toBe(true);
  68  |         else if (text.includes('every enabled header control')) {
  69  |           const ids = forward.filter(value => value.header).map(value => [value.tag,value.id,value.aria,value.testId].join(':'));
  70  |           const required = await page.getByTestId(`${localPrefix}_appBar`).locator('button:enabled,input:enabled,[tabindex="0"]').count();
  71  |           expect(new Set(ids).size).toBeGreaterThanOrEqual(required);
  72  |         } else expect(forward.filter(value => value.header).every(value => value.indicator)).toBe(true);
  73  |         return;
  74  |       }
  75  |       if (text.includes('accessibility probe captures')) { await audit.record('accessibility-snapshot', await page.locator('body').ariaSnapshot()); return; }
  76  |       if (text.includes('presses "ArrowRight"')) { await page.keyboard.press('ArrowRight'); return; }
  77  |       if (text.includes('presses "Enter"') && text.includes('tab labelled')) { await page.keyboard.press('Enter'); return; }
  78  |       if (text.includes('presses "Enter"') && text.includes('New Tile')) { await page.keyboard.press('Enter'); return; }
  79  |       if (text.includes('presses "Escape"')) { await page.keyboard.press('Escape'); return; }
  80  |       if (text.includes('presses "Space"')) { await page.keyboard.press('Space'); return; }
  81  |       if (text.includes('presses "Enter"') && text.includes('avatar_IconButton')) { await page.keyboard.press('Enter'); return; }
  82  |       if (text.includes('focuses the menu item')) { await app.portal.profileMenuItem.focus(); await expect(app.portal.profileMenuItem).toBeFocused(); return; }
  83  |       if (text.includes('presses "Enter"') && text.includes('avatar_Profile')) { await page.keyboard.press('Enter'); return; }
  84  |       if (text.includes('types "Cashflow Review"')) { await tab().tab.dblclick(); await tab().fillName('Cashflow Review'); return; }
  85  |       if (text.includes('has value equal to "Cashflow Review"')) { await tab().expectName('Cashflow Review'); return; }
  86  |       if (text.includes('clicks the tab labelled "Cashflow"')) {
  87  |         const tabs = app.portal.workspaceList.getByRole('tab');
  88  |         for (const target of await tabs.all()) if (await target.getByRole('textbox').inputValue() === 'Cashflow') { await target.click(); break; }
  89  |         return;
  90  |       }
  91  |       if (text.includes('Cashflow') && text.includes('selected state')) { await expect(app.portal.workspaceList.getByRole('tab', { selected: true }).getByRole('textbox')).toHaveValue('Cashflow'); return; }
> 92  |       if (text.includes('workspaces-tabpanel-1')) { await expect(page.locator('#workspaces-tabpanel-1')).toBeVisible(); return; }
      |                                                                                                          ^ Error: expect(locator).toBeVisible() failed
  93  |       if (text.includes('accessible name equal to "refresh"')) { await expect(tab().refreshButton).toHaveAccessibleName('refresh'); return; }
  94  |       if (text.includes('accessible name equal to "delete"')) { await expect(tab().deleteButton).toHaveAccessibleName('delete'); return; }
  95  |       if (text.includes('Theme Switch') && text.includes('checked state')) { await app.portal.expectThemeLight(true); return; }
  96  |       if (text.includes('persisted theme value')) { expect(await page.evaluate(() => localStorage.getItem('SET_THEME'))).toBe('light'); return; }
  97  |       if (text.includes('Tile Options') && text.endsWith('is visible')) { await expect(app.drawer).toBeVisible(); return; }
  98  |       if (text.includes('Tile Options') && text.endsWith('is hidden')) { await expect(app.drawer).toBeHidden(); return; }
  99  |       if (text.includes('active element is inside the open Tile Options')) { expect(await focusWithin(app.drawer)).toBe(true); return; }
  100 |       if (text.includes('New Tile') && text.endsWith('is focused')) { await expect(app.newTile).toBeFocused(); return; }
  101 |       if (text.includes('chip labelled "Close"')) { await closeProfile(page).click(); return; }
  102 |       if (text.includes('avatar_IconButton') && text.endsWith('is focused')) { await expect(app.portal.avatarButton).toBeFocused(); return; }
  103 |       if (text.includes('dialog labelled "User Profile"') && text.endsWith('is visible')) { await expect(profileRoot(page)).toBeVisible(); return; }
  104 |       if (text.includes('dialog labelled "User Profile"') && text.endsWith('is hidden')) { await expect(profileRoot(page)).toBeHidden(); return; }
  105 |       if (text.includes('active element is inside the User Profile')) { expect(await focusWithin(profileRoot(page))).toBe(true); return; }
  106 |       if (text.includes('accessible name equal to "User Profile"')) { await expect(page.getByRole('dialog', { name:'User Profile', exact:true })).toBeVisible(); return; }
  107 |       throw new Error(`Unbound keyboard step ${id}: ${text}`);
  108 |     });
  109 |   });
  110 | }
  111 | 
  112 | for (const [n,width,height] of [[23,320,568],[24,375,812],[25,768,1024],[26,1024,768],[27,1366,768],[28,1920,1080]]) {
  113 |   test(`UX-${n.toString().padStart(3,'0')} responsive shell ${width}x${height}`, async ({ page, audit }) => {
  114 |     await audit.defineCase(`UX-${n.toString().padStart(3,'0')}`); let app: CatalogApp;
  115 |     await audit.step(1,async()=>{await page.setViewportSize({width,height});app=await loginCatalog(page);});
  116 |     await audit.step(2,async()=>{await app.openDrawer();});
  117 |     await audit.step(3,async()=>{await expect(app.drawer).toBeInViewport();});
  118 |     await audit.step(4,async()=>{await page.keyboard.press('Escape');});
  119 |     await audit.step(5,async()=>{await expect(app.drawer).toBeHidden();});
  120 |     await audit.step(6,async()=>{await app.portal.clickAvatarButton();});
  121 |     await audit.step(7,async()=>{
  122 |       await expect(app.portal.profileMenuItem).toBeVisible();
  123 |       const first=await app.portal.profileMenuItem.boundingBox(), second=await app.portal.logoutMenuItem.boundingBox();
  124 |       expect(first).not.toBeNull();expect(second).not.toBeNull();
  125 |       expect(first!.y+first!.height<=second!.y || second!.y+second!.height<=first!.y).toBe(true);
  126 |     });
  127 |     await audit.step(8,async()=>{await expect(app.portal.logoutMenuItem).toBeEnabled();await expect(app.portal.logoutMenuItem).toBeInViewport();});
  128 |   });
  129 | }
  130 | 
  131 | for (const n of [37,44,46]) {
  132 |   const id=`UX-${String(n).padStart(3,'0')}`;
  133 |   test(`${id} workspace text boundary`,async({page,audit})=>{
  134 |     const steps=await audit.defineCase(id);let app:CatalogApp;const alerts:string[]=[];
  135 |     const value=n===37?'<img src=x onerror=alert(1)>':n===46?'A'.repeat(512):'Cashflow 東京 😀';
  136 |     for(const step of steps) await audit.step(step.number,async()=>{
  137 |       const text=step.text;
  138 |       if(step.number===1){page.on('dialog',async dialog=>{alerts.push(dialog.type());await dialog.dismiss();});app=await loginCatalog(page,{workspaces:[{id:'W1',label:'Cashflow',isActive:true,containers:[fixtureContainer({registerRefresh:true})]},{id:'W2',label:'Second',isActive:true,containers:[]}]});await app.portal.workspace('W1').tab.dblclick();await app.portal.workspace('W1').fillName(n===46?value:'Cashflow');return;}
  139 |       if(text.includes('types ')){await app.portal.workspace('W1').fillName(value);return;}
  140 |       if(text.includes('hovers over')){await app.portal.workspace('W1').tab.hover();return;}
  141 |       if(text.includes('input value equals')||text.includes('textbox')&&text.includes('value equal')){await app.portal.workspace('W1').expectName(value);return;}
  142 |       if(text.includes('zero alert events')){expect(alerts).toEqual([]);await audit.record('script-dialog-events',alerts);return;}
  143 |       if(text.includes('tooltip') || text.includes('Tooltip')){await expect(page.getByRole('tooltip')).toHaveText(value);return;}
  144 |       if(text.includes('named "delete"')){await expect(app.portal.workspace('W1').deleteButton).toBeVisible();await expect(app.portal.workspace('W1').deleteButton).toBeEnabled();return;}
  145 |       if(text.includes('named "refresh"')){await expect(app.portal.workspace('W1').refreshButton).toBeVisible();await expect(app.portal.workspace('W1').refreshButton).toBeEnabled();return;}
  146 |       throw new Error(`Unbound workspace text step: ${text}`);
  147 |     });
  148 |   });
  149 | }
  150 | 
  151 | for(const n of [48,49,50,63,64,71,72]){
  152 |   const id=`UX-${String(n).padStart(3,'0')}`;
  153 |   test(`${id} profile or catalog resilience`,async({page,audit})=>{
  154 |     const steps=await audit.defineCase(id);let app:CatalogApp;
  155 |     for(const step of steps) await audit.step(step.number,async()=>{
  156 |       const text=step.text;
  157 |       if(step.number===1){
  158 |         if(n===50)await page.route('**/tsp-profile/**',route=>route.fulfill({status:404,body:''}));
  159 |         if(n===63)await page.route('**/*analytics*',route=>route.fulfill({status:503,body:''}));
  160 |         app=await loginCatalog(page,{user:{fullName:n===49?'A'.repeat(200):'User A',oud:JSON.stringify({userId:'USER-A'})},
  161 |           drawers:n===71?[fixtureCategory([fixtureTile({entryName:'Mars'})])]:n===72?[fixtureCategory([fixtureTile({entryName:'Indonesia',tile:'/fixture/one'}),fixtureTile({entryName:'Indonesia',tile:'/fixture/two'})])]:undefined});return;
  162 |       }
  163 |       if(text.includes('clicks the icon button')){await app.portal.clickAvatarButton();return;}
  164 |       if(text.includes('clicks the menu item')){await app.openProfile();return;}
  165 |       if(text.includes('clicks the section labelled "New Tile"')){await app.openDrawer();return;}
  166 |       if(text.includes('dialog labelled "User Profile"')&&text.endsWith('is visible')){await expect(profileRoot(page)).toBeVisible();return;}
  167 |       if(text.includes('neither literal')){await expect(app.profileIdentity).not.toContainText(/undefined|null/);return;}
  168 |       if(text.includes('profile name text equals')){await expect(app.profileIdentity.locator('.MuiTypography-h5')).toHaveText('A'.repeat(200));return;}
  169 |       if(text.includes('complete profile name is visible')){await expect(app.profileIdentity.locator('.MuiTypography-h5')).toBeVisible();return;}
  170 |       if(text.includes('chip labelled "Close"')&&text.includes('clicks')){await closeProfile(page).click();return;}
  171 |       if(text.includes('chip labelled "Close"')){await expect(closeProfile(page)).toBeVisible();await expect(closeProfile(page)).toBeEnabled();return;}
  172 |       if(text.includes('dialog labelled "User Profile"')&&text.endsWith('is hidden')){await expect(profileRoot(page)).toBeHidden();return;}
  173 |       if(text.includes('profile identity text')){await expect(app.profileIdentity).toContainText('USER-A');if(n===50)await expect(app.profileIdentity).toContainText('User A');return;}
  174 |       if(text.includes('tile error panel is absent')){await expect(profileRoot(page).getByTestId('FallbackError__page-id')).toHaveCount(0);return;}
  175 |       if(text.includes('Markets Operations One logo')){await expect(page.getByRole('img',{name:'Markets Operations One logo',exact:true})).toBeVisible();return;}
  176 |       if(text.includes('avatar_Profile')&&text.includes('contains')){await expect(app.portal.profileMenuItem).toContainText(/USER-A|User A/);return;}
  177 |       if(text.includes('button labelled "Mars"')&&text.endsWith('is visible')){await expect(app.entry('Mars')).toBeVisible();return;}
  178 |       if(text.includes('contains no Indonesia flag')){await expect(app.entry('Mars').getByRole('img',{name:'Indonesia icon',exact:true})).toHaveCount(0);return;}
  179 |       if(text.includes('expose distinct route or record identifiers')){
  180 |         const buttons=app.card().getByRole('button').filter({hasText:/^Indonesia$/});await expect(buttons).toHaveCount(2);
  181 |         const identifiers=await buttons.evaluateAll(nodes=>nodes.map(node=>node.getAttribute('data-route')||node.getAttribute('data-record-id')||node.getAttribute('id')||node.getAttribute('aria-label')));
  182 |         await audit.record('duplicate-entry-identifiers',identifiers);expect(identifiers.every(Boolean)&&new Set(identifiers).size===2).toBe(true);return;
  183 |       }
  184 |       throw new Error(`Unbound resilience step ${id}: ${text}`);
  185 |     });
  186 |   });
  187 | }
  188 | 
```