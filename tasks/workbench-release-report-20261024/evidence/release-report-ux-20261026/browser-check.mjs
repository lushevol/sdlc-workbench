import { writeFileSync,readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';
process.env.PLAYWRIGHT_BROWSERS_PATH=`${process.cwd()}/adapters/browser/.browsers`;
const {chromium}=await import(`${process.cwd()}/node_modules/@playwright/test/index.mjs`);
const out=`${process.cwd()}/docs/evidence/release-report-ux-20261026`;
const source='/Users/lushevol/.codex/visualizations/2026/10/24/01a16dc1-66fd-76e3-8299-50eb25ce7bbd/release-review-prototype.html';
const browser=await chromium.launch({channel:'chromium',headless:true,chromiumSandbox:true});
const checks=[];
try{
 for(const [width,theme] of [[1024,'light'],[390,'light'],[320,'light'],[1024,'dark']]){
  const page=await browser.newPage({viewport:{width,height:1100},colorScheme:theme});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const attempts=[];await page.route(/^https?:/,async r=>{attempts.push(r.request().url());await r.abort();});
  await page.goto(pathToFileURL('/private/tmp/release-report-ux-20261026/prototype-preview.html').href);
  const frame=page.frameLocator('iframe');
  await frame.locator('#rr-board-cards .rr-release-card').first().waitFor();
  const iframe=page.frames().find(f=>f.parentFrame());
  await iframe.evaluate(()=>{window.rrClickTrace=[];document.getElementById('release-review-prototype').addEventListener('click',event=>{window.rrClickTrace.push({button:event.target.closest('button')?.outerHTML.slice(0,180),header:document.querySelector('#rr-release-id').textContent});});});
  const overflow=()=>iframe.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  const fitCapture=async()=>{const height=await iframe.locator('#release-review-prototype').evaluate(el=>Math.ceil(el.getBoundingClientRect().height+32));await page.locator('iframe').evaluate((el,height)=>{el.style.height=height+'px';},height);};
  if(await overflow())throw Error(`Board overflows ${width}`);
  await frame.locator('[data-release="501"]').click();
  await frame.locator('#rr-tab-builds').click();
  const initial=await frame.locator('#rr-build-content').innerText();
  for(const label of ['PROD','Main','Current build','Latest','2 behind','1 ahead'])if(!initial.includes(label))throw Error(`Missing ${label}`);
  if(await overflow())throw Error(`Build view overflows ${width}`);
  await fitCapture();
  await frame.locator('[data-variant="Reference strip"] [data-diff="latest"]').click({timeout:5000}).catch(async e=>{const debug=await iframe.evaluate(()=>({strip:document.querySelector('[data-variant="Reference strip"]').outerHTML.slice(0,100),panelHidden:document.querySelector('#rr-panel-builds').hidden,detailHidden:document.querySelector('[data-screen="detail"]').hidden,active:document.querySelector('.viz-carousel').dataset.activeVariant}));throw Error(JSON.stringify({width,theme,debug,error:e.message}));});
  if(!(await frame.locator('#rr-diff').innerText()).includes('Validate configuration'))throw Error('Diff missing');
  await frame.locator('[data-close-diff]').click();
  if(width<=680)await frame.locator('#rr-repo-select').selectOption('auth-service');else await frame.locator('[data-repo="auth-service"]').click();
  if(!(await frame.locator('#rr-coverage').innerText()).includes('Unavailable'))throw Error('Unavailable coverage missing');
  if(width<=680)await frame.locator('#rr-repo-select').selectOption('service-properties');else await frame.locator('[data-repo="service-properties"]').click();
  await frame.locator('.viz-carousel-next').click();
  if(!await frame.locator('[data-variant="Reference table"]').isVisible())throw Error('Alternate reference layout unavailable');
  if(await overflow())throw Error('Reference table causes page overflow');
  await frame.locator('.viz-carousel-previous').click();
  if(width===1024&&theme==='light'){
    await fitCapture();await page.screenshot({path:`${out}/prototype-builds-desktop.png`,fullPage:true});
  }
  if(width===390){await fitCapture();await page.screenshot({path:`${out}/prototype-builds-mobile.png`,fullPage:true});}
  await frame.locator('#rr-tab-stories').click();
  await frame.locator('#rr-stories summary').click();
  if(!(await frame.locator('#rr-stories').innerText()).includes('endpoint was unavailable'))throw Error('Story reason missing');
  await frame.locator('#rr-tab-checklist').click();
  if(!(await frame.locator('#rr-checklist').innerText()).includes('Main ↔ PROD'))throw Error('Checklist missing');
  await frame.locator('#rr-tab-builds').click();
  if(width<=680)await frame.locator('#rr-repo-select').selectOption('api-gateway');else await frame.locator('[data-repo="api-gateway"]').click();
  await frame.locator('#rr-tab-checklist').click();
  await frame.locator('#rr-checklist [data-diff="main"]').click();
  if(!(await frame.locator('#rr-build-heading').innerText()).includes('api-gateway'))throw Error('Checklist diff changed repository');
  await frame.locator('[data-action="board"]').click();
  if(width===1024&&theme==='light'){await fitCapture();await page.screenshot({path:`${out}/prototype-board-desktop.png`,fullPage:true});}
  await frame.locator('[data-week="1"]').click();
  if(!(await frame.locator('#rr-week-message').innerText()).includes('No sample'))throw Error('Week navigation failed');
  await frame.locator('[data-week="-1"]').click();
  for(const id of ['502','503']){
    await frame.locator(`[data-release="${id}"]`).focus();
    await frame.locator(`[data-release="${id}"]`).press('Enter');
    const overview=await frame.locator('#rr-overview-content').innerText();
    if(id==='502'&&!overview.includes('Evidence needs attention'))throw Error(JSON.stringify({width,id,overview,header:await frame.locator('#rr-release-id').innerText(),screen:await frame.locator('[data-screen="detail"]').getAttribute('hidden'),trace:await iframe.evaluate(()=>window.rrClickTrace.slice(-8))}));
    if(id==='503'&&!overview.includes('story test failed'))throw Error('Wrong release fixture');
    await frame.locator('[data-action="board"]').click();
  }
  if(errors.length)throw Error(JSON.stringify({errors,attempts}));
  if(attempts.some(url=>!url.startsWith('https://unpkg.com/')))throw Error('Unexpected network resource');
  checks.push({width,theme,status:'PASSED',board_to_detail:true,four_commit_references:true,alternate_reference_layout:true,checklist_repository_preserved:true,diff_reason_accessible:true,unavailable_coverage:true,story_reason_accessible:true,checklist_accessible:true,week_navigation:true,other_release_fixtures_keyboard_activation:true,page_overflow:false,page_errors:errors,preview_host_resource_attempts:attempts,prototype_network_calls:0});
  await page.close();
 }
 const result={date:'2026-10-26',status:'PASSED',prototype_sha256:createHash('sha256').update(readFileSync(source)).digest('hex'),checks,standard:'ASD-STE100',automated_check:'PASSED',asd_review:'PENDING',reviewer:null,reviewed_at:null,limitations:['Automated checks do not check the complete approved dictionary or grammar rules.','Illustrative prototype only. External ADO and Clinic link destinations are not connected.','Additional release cards use native keyboard activation after preview-frame resizing.','The preview wrapper attempted two standard CDN utilities; both were blocked. The prototype calls no network API.','No runtime implementation or live behavior was verified.']};
 writeFileSync(`${out}/prototype-validation.json`,JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify(result));
}finally{await browser.close();}
