import { test, expect, type AuditCapture } from '../support/audit-fixture.js';
import type { Locator, Page } from '@playwright/test';
import { CatalogApp, fixtureCategory, fixtureContainer, fixtureTile, loginCatalog } from '../support/catalog-app.js';
import { localPrefix } from '../support/local-app.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual React shell. Controlled catalog, user identity, photo failures, and SystemJS tenant. Chromium only. Accessibility and layout outcomes are proposed probes; no approved conformance standard is inferred.' });
const profileRoot = (page: Page) => page.getByTestId(`${localPrefix}_Dialog`).filter({ has: page.getByText('User Profile', { exact: true }) });
const closeProfile = (page: Page) => profileRoot(page).getByTestId(`${localPrefix}_Dialog-close`);
async function profile(app: CatalogApp): Promise<void> { await app.portal.clickAvatarButton(); await app.openProfile(); }
async function focusWithin(root: Locator): Promise<boolean> { return root.evaluate(node => node.contains(document.activeElement)); }
async function traceFocus(page: Page, audit: AuditCapture, backwards = false, count = 12) {
  const trace: Record<string, unknown>[] = [];
  for (let index = 0; index < count; index++) {
    await page.keyboard.press(backwards ? 'Shift+Tab' : 'Tab');
    const item = await page.evaluate(() => {
      const node = document.activeElement as HTMLElement;
      const style = getComputedStyle(node);
      const parent = node.closest('.MuiSwitch-root,.MuiButtonBase-root') ?? node;
      const parentStyle = getComputedStyle(parent);
      return { tag: node.tagName, id: node.id, role: node.getAttribute('role'), aria: node.getAttribute('aria-label'),
        testId: node.getAttribute('data-testid'), text: node.textContent?.slice(0, 120),
        header: Boolean(node.closest('[data-testid="MicroWebUI_base_appBar"]')),
        profile: Boolean(node.closest('[data-testid="MicroWebUI_base_Dialog"]')),
        indicator: (style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) > 0)
          || style.boxShadow !== 'none' || parentStyle.boxShadow !== 'none'
          || Boolean(node.closest('.Mui-focusVisible')),
        outline: style.outline, boxShadow: style.boxShadow, parentBoxShadow: parentStyle.boxShadow };
    });
    trace.push(item);
    await audit.capture(`focus-${backwards ? 'reverse' : 'forward'}-${index + 1}`, 'Live keyboard focus checkpoint; computed CSS is retained separately.');
  }
  await audit.record(`focus-trace-${backwards ? 'reverse' : 'forward'}`, trace);
  return trace;
}

for (const n of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 19, 20]) {
  const id = `UX-${String(n).padStart(3, '0')}`;
  test(`${id} keyboard and accessibility probe`, async ({ page, audit }) => {
    const steps = await audit.defineCase(id);
    let app: CatalogApp;
    let forward: Record<string, unknown>[] = [], reverse: Record<string, unknown>[] = [];
    const tab = () => app.portal.workspace('W1');
    for (const step of steps) await audit.step(step.number, async () => {
      const text = step.text;
      if (step.number === 1) {
        app = await loginCatalog(page, [4,5,6,7].includes(n) ? { workspaces: [
          { id: 'W1', label: n === 4 || n === 6 ? 'Home' : 'Cashflow', isActive: true, containers: [fixtureContainer({registerRefresh:true})] },
          { id: n === 4 ? '1' : 'W2', label: 'Cashflow', isActive: n !== 4, containers: [] }] } : {});
        if ([4,5,6,7].includes(n)) {
          if (n === 4) { await tab().tab.focus(); await expect(tab().tab).toBeFocused(); }
        }
        if ([8,9,20].includes(n)) await app.portal.setThemeLight(n !== 8);
        if (n === 8) await app.portal.themeCheckbox.focus();
        if ([2,3].includes(n)) {
          await app.newTile.focus();
          await expect(app.newTile).toBeFocused();
          if (n === 3) { await page.keyboard.press('Enter'); await expect(app.drawer).toBeVisible(); }
        }
        if (n === 10) { await app.portal.avatarButton.focus(); await expect(app.portal.avatarButton).toBeFocused(); }
        if ([11,12,13].includes(n)) await profile(app);
        return;
      }
      if (text.includes('presses "Tab"') && !text.includes('Shift')) { forward = await traceFocus(page,audit,false,n === 11 ? 16 : 10); return; }
      if (text.includes('presses "Shift+Tab"')) { reverse = await traceFocus(page,audit,true,16); return; }
      if (text.includes('focus trace') || text.includes('Each traced control')) {
        if (n === 11) expect((text.startsWith('The reverse') ? reverse : forward).every(value => value.profile)).toBe(true);
        else if (text.includes('every enabled header control')) {
          const ids = forward.filter(value => value.header).map(value => [value.tag,value.id,value.aria,value.testId].join(':'));
          const required = await page.getByTestId(`${localPrefix}_appBar`).locator('button:enabled,input:enabled,[tabindex="0"]').count();
          expect(new Set(ids).size).toBeGreaterThanOrEqual(required);
        } else expect(forward.filter(value => value.header).every(value => value.indicator)).toBe(true);
        return;
      }
      if (text.includes('accessibility probe captures')) { await audit.record('accessibility-snapshot', await page.locator('body').ariaSnapshot()); return; }
      if (text.includes('presses "ArrowRight"')) { await page.keyboard.press('ArrowRight'); return; }
      if (text.includes('presses "Enter"') && text.includes('tab labelled')) { await page.keyboard.press('Enter'); return; }
      if (text.includes('presses "Enter"') && text.includes('New Tile')) { await page.keyboard.press('Enter'); return; }
      if (text.includes('presses "Escape"')) { await page.keyboard.press('Escape'); return; }
      if (text.includes('presses "Space"')) { await page.keyboard.press('Space'); return; }
      if (text.includes('presses "Enter"') && text.includes('avatar_IconButton')) { await page.keyboard.press('Enter'); return; }
      if (text.includes('focuses the menu item')) { await app.portal.profileMenuItem.focus(); await expect(app.portal.profileMenuItem).toBeFocused(); return; }
      if (text.includes('presses "Enter"') && text.includes('avatar_Profile')) { await page.keyboard.press('Enter'); return; }
      if (text.includes('types "Cashflow Review"')) { await tab().tab.dblclick(); await tab().fillName('Cashflow Review'); return; }
      if (text.includes('has value equal to "Cashflow Review"')) { await tab().expectName('Cashflow Review'); return; }
      if (text.includes('clicks the tab labelled "Cashflow"')) {
        const tabs = app.portal.workspaceList.getByRole('tab');
        for (const target of await tabs.all()) if (await target.getByRole('textbox').inputValue() === 'Cashflow') { await target.click(); break; }
        return;
      }
      if (text.includes('Cashflow') && text.includes('selected state')) { await expect(app.portal.workspaceList.getByRole('tab', { selected: true }).getByRole('textbox')).toHaveValue('Cashflow'); return; }
      if (text.includes('workspaces-tabpanel-1')) { await expect(page.locator('#workspaces-tabpanel-1')).toBeVisible(); return; }
      if (text.includes('accessible name equal to "refresh"')) { await expect(tab().refreshButton).toHaveAccessibleName('refresh'); return; }
      if (text.includes('accessible name equal to "delete"')) { await expect(tab().deleteButton).toHaveAccessibleName('delete'); return; }
      if (text.includes('Theme Switch') && text.includes('checked state')) { await app.portal.expectThemeLight(true); return; }
      if (text.includes('persisted theme value')) { expect(await page.evaluate(() => localStorage.getItem('SET_THEME'))).toBe('light'); return; }
      if (text.includes('Tile Options') && text.endsWith('is visible')) { await expect(app.drawer).toBeVisible(); return; }
      if (text.includes('Tile Options') && text.endsWith('is hidden')) { await expect(app.drawer).toBeHidden(); return; }
      if (text.includes('active element is inside the open Tile Options')) { expect(await focusWithin(app.drawer)).toBe(true); return; }
      if (text.includes('New Tile') && text.endsWith('is focused')) { await expect(app.newTile).toBeFocused(); return; }
      if (text.includes('chip labelled "Close"')) { await closeProfile(page).click(); return; }
      if (text.includes('avatar_IconButton') && text.endsWith('is focused')) { await expect(app.portal.avatarButton).toBeFocused(); return; }
      if (text.includes('dialog labelled "User Profile"') && text.endsWith('is visible')) { await expect(profileRoot(page)).toBeVisible(); return; }
      if (text.includes('dialog labelled "User Profile"') && text.endsWith('is hidden')) { await expect(profileRoot(page)).toBeHidden(); return; }
      if (text.includes('active element is inside the User Profile')) { expect(await focusWithin(profileRoot(page))).toBe(true); return; }
      if (text.includes('accessible name equal to "User Profile"')) { await expect(page.getByRole('dialog', { name:'User Profile', exact:true })).toBeVisible(); return; }
      throw new Error(`Unbound keyboard step ${id}: ${text}`);
    });
  });
}

for (const [n,width,height] of [[23,320,568],[24,375,812],[25,768,1024],[26,1024,768],[27,1366,768],[28,1920,1080]]) {
  test(`UX-${n.toString().padStart(3,'0')} responsive shell ${width}x${height}`, async ({ page, audit }) => {
    await audit.defineCase(`UX-${n.toString().padStart(3,'0')}`); let app: CatalogApp;
    await audit.step(1,async()=>{await page.setViewportSize({width,height});app=await loginCatalog(page);});
    await audit.step(2,async()=>{await app.newTile.click({timeout:5000});});
    await audit.step(3,async()=>{await expect(app.drawer).toBeInViewport();});
    await audit.step(4,async()=>{await page.keyboard.press('Escape');});
    await audit.step(5,async()=>{await expect(app.drawer).toBeHidden();});
    await audit.step(6,async()=>{await app.portal.avatarButton.click({timeout:5000});});
    await audit.step(7,async()=>{
      await expect(app.portal.profileMenuItem).toBeVisible();
      const first=await app.portal.profileMenuItem.boundingBox(), second=await app.portal.logoutMenuItem.boundingBox();
      expect(first).not.toBeNull();expect(second).not.toBeNull();
      expect(first!.y+first!.height<=second!.y || second!.y+second!.height<=first!.y).toBe(true);
    });
    await audit.step(8,async()=>{await expect(app.portal.logoutMenuItem).toBeEnabled();await expect(app.portal.logoutMenuItem).toBeInViewport();});
  });
}

for (const n of [37,44,46]) {
  const id=`UX-${String(n).padStart(3,'0')}`;
  test(`${id} workspace text boundary`,async({page,audit})=>{
    const steps=await audit.defineCase(id);let app:CatalogApp;const alerts:string[]=[];
    const value=n===37?'<img src=x onerror=alert(1)>':n===46?'A'.repeat(512):'Cashflow 東京 😀';
    for(const step of steps) await audit.step(step.number,async()=>{
      const text=step.text;
      if(step.number===1){page.on('dialog',async dialog=>{alerts.push(dialog.type());await dialog.dismiss();});app=await loginCatalog(page,{workspaces:[{id:'W1',label:'Cashflow',isActive:true,containers:[fixtureContainer({registerRefresh:true})]},{id:'W2',label:'Second',isActive:true,containers:[]}]});await app.portal.workspace('W1').tab.dblclick();await app.portal.workspace('W1').fillName(n===46?value:'Cashflow');return;}
      if(text.includes('types ')){await app.portal.workspace('W1').fillName(value);return;}
      if(text.includes('hovers over')){await app.portal.workspace('W1').tab.hover();return;}
      if(text.includes('input value equals')||text.includes('textbox')&&text.includes('value equal')){await app.portal.workspace('W1').expectName(value);return;}
      if(text.includes('zero alert events')){expect(alerts).toEqual([]);await audit.record('script-dialog-events',alerts);return;}
      if(text.includes('tooltip') || text.includes('Tooltip')){await expect(page.getByRole('tooltip')).toHaveText(value);return;}
      if(text.includes('named "delete"')){await expect(app.portal.workspace('W1').deleteButton).toBeVisible();await expect(app.portal.workspace('W1').deleteButton).toBeEnabled();return;}
      if(text.includes('named "refresh"')){await expect(app.portal.workspace('W1').refreshButton).toBeVisible();await expect(app.portal.workspace('W1').refreshButton).toBeEnabled();return;}
      throw new Error(`Unbound workspace text step: ${text}`);
    });
  });
}

for(const n of [48,49,50,63,64,71,72]){
  const id=`UX-${String(n).padStart(3,'0')}`;
  test(`${id} profile or catalog resilience`,async({page,audit})=>{
    const steps=await audit.defineCase(id);let app:CatalogApp;
    for(const step of steps) await audit.step(step.number,async()=>{
      const text=step.text;
      if(step.number===1){
        if(n===50)await page.route('**/tsp-profile/**',route=>route.fulfill({status:404,body:''}));
        if(n===63)await page.route('**/*analytics*',route=>route.fulfill({status:503,body:''}));
        app=await loginCatalog(page,{user:{fullName:n===49?'A'.repeat(200):'User A',oud:JSON.stringify({userId:'USER-A',fullName:n===49?'A'.repeat(200):'User A'})},
          drawers:n===71?[fixtureCategory([fixtureTile({entryName:'Mars'})])]:n===72?[fixtureCategory([fixtureTile({entryName:'Indonesia',tile:'/fixture/one'}),fixtureTile({entryName:'Indonesia',tile:'/fixture/two'})])]:undefined});return;
      }
      if(text.includes('clicks the icon button')){await app.portal.clickAvatarButton();return;}
      if(text.includes('clicks the menu item')){await app.openProfile();return;}
      if(text.includes('clicks the section labelled "New Tile"')){await app.openDrawer();return;}
      if(text.includes('dialog labelled "User Profile"')&&text.endsWith('is visible')){await expect(profileRoot(page)).toBeVisible();return;}
      if(text.includes('neither literal')){await expect(app.profileIdentity).not.toContainText(/undefined|null/);return;}
      if(text.includes('profile name text equals')){await expect(app.profileIdentity.locator('.MuiTypography-h5')).toHaveText('A'.repeat(200));return;}
      if(text.includes('complete profile name is visible')){await expect(app.profileIdentity.locator('.MuiTypography-h5')).toBeVisible();return;}
      if(text.includes('chip labelled "Close"')&&text.includes('clicks')){await closeProfile(page).click();return;}
      if(text.includes('chip labelled "Close"')){await expect(closeProfile(page)).toBeVisible();await expect(closeProfile(page)).toBeEnabled();return;}
      if(text.includes('dialog labelled "User Profile"')&&text.endsWith('is hidden')){await expect(profileRoot(page)).toBeHidden();return;}
      if(text.includes('profile identity text')){await expect(app.profileIdentity).toContainText('USER-A');if(n===50)await expect(app.profileIdentity).toContainText('User A');return;}
      if(text.includes('tile error panel is absent')){await expect(profileRoot(page).getByTestId('FallbackError__page-id')).toHaveCount(0);return;}
      if(text.includes('Markets Operations One logo')){await expect(page.getByRole('img',{name:'Markets Operations One logo',exact:true})).toBeVisible();return;}
      if(text.includes('avatar_Profile')&&text.includes('contains')){await expect(app.portal.profileMenuItem).toContainText(/USER-A|User A/);return;}
      if(text.includes('button labelled "Mars"')&&text.endsWith('is visible')){await expect(app.entry('Mars')).toBeVisible();return;}
      if(text.includes('contains no Indonesia flag')){await expect(app.entry('Mars').getByRole('img',{name:'Indonesia icon',exact:true})).toHaveCount(0);return;}
      if(text.includes('expose distinct route or record identifiers')){
        const buttons=app.card().getByRole('button').filter({hasText:/^Indonesia$/});await expect(buttons).toHaveCount(2);
        const identifiers=await buttons.evaluateAll(nodes=>nodes.map(node=>node.getAttribute('data-route')||node.getAttribute('data-record-id')||node.getAttribute('id')||node.getAttribute('aria-label')));
        await audit.record('duplicate-entry-identifiers',identifiers);expect(identifiers.every(Boolean)&&new Set(identifiers).size===2).toBe(true);return;
      }
      throw new Error(`Unbound resilience step ${id}: ${text}`);
    });
  });
}
