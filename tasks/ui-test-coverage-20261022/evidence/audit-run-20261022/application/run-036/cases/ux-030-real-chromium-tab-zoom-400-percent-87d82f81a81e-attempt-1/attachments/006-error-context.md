# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: browser-zoom.spec.ts >> UX-030 real Chromium tab zoom 400 percent
- Location: e2e/audit-specs/browser-zoom.spec.ts:28:2

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: 4
Received: 3.9999999999999996
```

# Test source

```ts
  1  | import { chromium, type BrowserContext } from '@playwright/test';
  2  | import { mkdtemp, rm } from 'node:fs/promises';
  3  | import path from 'node:path';
  4  | import { test as auditTest, expect } from '../support/audit-fixture.js';
  5  | import { browserLaunchOptions } from '../browser-config.js';
  6  | import { CatalogApp, loginCatalog } from '../support/catalog-app.js';
  7  | import { localBase } from '../support/local-app.js';
  8  | 
  9  | const test = auditTest.extend({
  10 |  context: async ({},use)=>{
  11 |   const directory=await mkdtemp(path.resolve('.workbench/zoom-audit-'));
  12 |   const extension=path.resolve('e2e/fixtures/zoom-extension');
  13 |   const context=await chromium.launchPersistentContext(directory,{...browserLaunchOptions(),viewport:{width:1366,height:768},
  14 |    args:[`--disable-extensions-except=${extension}`,`--load-extension=${extension}`]});
  15 |   try{await use(context);}finally{await context.close();await rm(directory,{recursive:true,force:true});}
  16 |  },
  17 | });
  18 | async function applyZoom(context:BrowserContext,factor:number){
  19 |  const worker=context.serviceWorkers()[0]??await context.waitForEvent('serviceworker',{timeout:10000});
  20 |  return worker.evaluate(async({origin,factor})=>{
  21 |   const chrome=(globalThis as any).chrome;
  22 |   const tabs=await chrome.tabs.query({});const tab=tabs.find((tab:any)=>tab.url?.startsWith(origin));
  23 |   if(!tab)throw new Error('Local audit tab not found.');
  24 |   await chrome.tabs.setZoom(tab.id,factor);return await chrome.tabs.getZoom(tab.id);
  25 |  },{origin:localBase,factor});
  26 | }
  27 | for(const [id,factor] of [['UX-029',2],['UX-030',4]] as const){
  28 |  test(`${id} real Chromium tab zoom ${factor*100} percent`,async({page,context,audit})=>{
  29 |   await audit.defineCase(id);let app:CatalogApp;let before:{width:number;ratio:number};
  30 |   await audit.step(1,async()=>{app=await loginCatalog(page);before=await page.evaluate(()=>({width:innerWidth,ratio:devicePixelRatio}));expect(before.width).toBe(1366);});
  31 |   await audit.step(2,async()=>{
> 32 |    expect(await applyZoom(context,factor)).toBe(factor);
     |                                            ^ Error: expect(received).toBe(expected) // Object.is equality
  33 |    await expect.poll(()=>page.evaluate(()=>devicePixelRatio)).toBe(before.ratio*factor);
  34 |    await audit.record('browser-zoom-observation',{before,after:await page.evaluate(()=>({width:innerWidth,ratio:devicePixelRatio})),factor,method:'chrome.tabs.setZoom in an isolated local extension'});
  35 |   });
  36 |   await audit.step(3,async()=>{await app.portal.avatarButton.click({timeout:5000});});
  37 |   await audit.step(4,async()=>{await expect(app.portal.avatarMenu).toBeVisible();});
  38 |   await audit.step(5,async()=>{await app.portal.logoutMenuItem.scrollIntoViewIfNeeded();await expect(app.portal.logoutMenuItem).toBeVisible();await expect(app.portal.logoutMenuItem).toBeEnabled();await expect(app.portal.logoutMenuItem).toBeInViewport();});
  39 |  });
  40 | }
  41 | test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',auditFixture:'Actual React shell in an isolated persistent Chromium context. Local extension calls real chrome.tabs.setZoom; no device scale or CSS zoom substitution. Controlled identity and catalog responses.'});
  42 | 
```