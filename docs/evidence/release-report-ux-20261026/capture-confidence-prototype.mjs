import {pathToFileURL} from 'node:url';
process.env.PLAYWRIGHT_BROWSERS_PATH=`${process.cwd()}/adapters/browser/.browsers`;
const {chromium}=await import(`${process.cwd()}/node_modules/@playwright/test/index.mjs`);
const browser=await chromium.launch({channel:'chromium',headless:true,chromiumSandbox:true});
try{
 for(const [width,theme] of [[1024,'light'],[1024,'dark'],[390,'light']]){
  const page=await browser.newPage({viewport:{width,height:1200},colorScheme:theme});
  await page.route(/^https?:/,r=>r.abort());
  await page.goto(pathToFileURL('/private/tmp/release-report-ux-20261026/confidence-preview.html').href);
  const f=page.frames().find(f=>f.parentFrame());
  await f.locator('#rc-tab-decision').waitFor();
  const h=await f.locator('#release-confidence-prototype').evaluate(el=>Math.ceil(el.getBoundingClientRect().height)+48);
  await page.setViewportSize({width,height:h});
  await page.locator('iframe').evaluate((el,h)=>{el.style.height=h+'px';},h);
  await f.evaluate(()=>{window.scrollTo(0,0);document.scrollingElement.scrollTop=0;});
  await page.evaluate(()=>window.scrollTo(0,0));
  await page.waitForTimeout(300);
  await page.screenshot({path:`${process.cwd()}/docs/evidence/release-report-ux-20261026/confidence-decision-${width}-${theme}.png`,fullPage:true,animations:'disabled'});
  console.log(JSON.stringify({width,theme,height:h,root_count:await f.locator('#release-confidence-prototype').count(),root_height:await f.locator('#release-confidence-prototype').evaluate(el=>el.getBoundingClientRect().height)}));
  await page.close();
 }
}finally{await browser.close();}
