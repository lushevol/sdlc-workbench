import { chromium, type BrowserContext } from '@playwright/test';
import { mkdtemp, rm } from 'node:fs/promises';
import path from 'node:path';
import { test as auditTest, expect } from '../support/audit-fixture.js';
import { browserLaunchOptions } from '../browser-config.js';
import { CatalogApp, loginCatalog } from '../support/catalog-app.js';
import { localBase } from '../support/local-app.js';

const test = auditTest.extend({
 context: async ({},use)=>{
  const directory=await mkdtemp(path.resolve('.workbench/zoom-audit-'));
  const extension=path.resolve('e2e/fixtures/zoom-extension');
  const context=await chromium.launchPersistentContext(directory,{...browserLaunchOptions(),viewport:{width:1366,height:768},
   args:[`--disable-extensions-except=${extension}`,`--load-extension=${extension}`]});
  try{await use(context);}finally{await context.close();await rm(directory,{recursive:true,force:true});}
 },
});
async function applyZoom(context:BrowserContext,factor:number){
 const worker=context.serviceWorkers()[0]??await context.waitForEvent('serviceworker',{timeout:10000});
 return worker.evaluate(async({origin,factor})=>{
  const chrome=(globalThis as any).chrome;
  const tabs=await chrome.tabs.query({});const tab=tabs.find((tab:any)=>tab.url?.startsWith(origin));
  if(!tab)throw new Error('Local audit tab not found.');
  await chrome.tabs.setZoom(tab.id,factor);return await chrome.tabs.getZoom(tab.id);
 },{origin:localBase,factor});
}
for(const [id,factor] of [['UX-029',2],['UX-030',4]] as const){
 test(`${id} real Chromium tab zoom ${factor*100} percent`,async({page,context,audit})=>{
  await audit.defineCase(id);let app:CatalogApp;let before:{width:number;ratio:number};
  await audit.step(1,async()=>{app=await loginCatalog(page);before=await page.evaluate(()=>({width:innerWidth,ratio:devicePixelRatio}));expect(before.width).toBe(1366);});
  await audit.step(2,async()=>{
   expect(await applyZoom(context,factor)).toBeCloseTo(factor,8);
   await expect.poll(()=>page.evaluate(()=>devicePixelRatio)).toBeCloseTo(before.ratio*factor,8);
   await audit.record('browser-zoom-observation',{before,after:await page.evaluate(()=>({width:innerWidth,ratio:devicePixelRatio})),factor,method:'chrome.tabs.setZoom in an isolated local extension'});
  });
  await audit.step(3,async()=>{await app.portal.avatarButton.click({timeout:5000});});
  await audit.step(4,async()=>{await expect(app.portal.avatarMenu).toBeVisible();});
  await audit.step(5,async()=>{await app.portal.logoutMenuItem.scrollIntoViewIfNeeded();await expect(app.portal.logoutMenuItem).toBeVisible();await expect(app.portal.logoutMenuItem).toBeEnabled();await expect(app.portal.logoutMenuItem).toBeInViewport();});
 });
}
test.use({auditScope:'ACTUAL_APPLICATION_LOCAL_SERVICES',auditFixture:'Actual React shell in an isolated persistent Chromium context. Local extension calls real chrome.tabs.setZoom; no device scale or CSS zoom substitution. Controlled identity and catalog responses.'});
