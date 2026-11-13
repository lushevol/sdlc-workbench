import {pathToFileURL} from 'node:url';
process.env.PLAYWRIGHT_BROWSERS_PATH=`${process.cwd()}/adapters/browser/.browsers`;
const {chromium}=await import(`${process.cwd()}/node_modules/@playwright/test/index.mjs`);
const browser=await chromium.launch({channel:'chromium',headless:true,chromiumSandbox:true});
try{
 for(const [name,width] of [['desktop',1024],['mobile',390]]){
  const page=await browser.newPage({viewport:{width,height:1000}});
  await page.route(/^https?:/,route=>route.abort());
  await page.goto(pathToFileURL('/private/tmp/release-report-ux-20261026/prototype-preview.html').href);
  const frame=page.frameLocator('iframe');const content=page.frames().find(f=>f.parentFrame());
  await frame.locator('[data-release="501"]').press('Enter');
  await frame.locator('#rr-tab-builds').press('Enter');
  const height=await frame.locator('#release-review-prototype').evaluate(e=>Math.ceil(e.getBoundingClientRect().height)+40);
  await page.locator('iframe').evaluate((el,h)=>{el.style.height=h+'px';},height);
  await content.evaluate(()=>{window.scrollTo(0,0);document.scrollingElement.scrollTop=0;});
  await page.evaluate(()=>window.scrollTo(0,0));
  await page.screenshot({path:`${process.cwd()}/docs/evidence/release-report-ux-20261026/prototype-builds-${name}.png`,fullPage:true});
  await page.close();
 }
}finally{await browser.close();}
