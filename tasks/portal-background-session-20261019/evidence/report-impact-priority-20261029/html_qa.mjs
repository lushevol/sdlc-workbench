import { chromium } from '../../../../adapters/browser/node_modules/playwright/index.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath,pathToFileURL } from 'node:url';
const folder=path.dirname(fileURLToPath(import.meta.url)),task=path.resolve(folder,'../..');
const browser=await chromium.launch({executablePath:'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless:true,
 args:['--disable-background-networking','--disable-component-update','--no-first-run']});
const captures=[];
function check(value,message){if(!value)throw new Error(message);}
try{
 for(const width of [390,715,1280]){
  const page=await browser.newPage({viewport:{width,height:1000}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.join(task,'10-release-confidence.html')).href);
  const state=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
   height:document.documentElement.scrollHeight,conclusion:document.querySelector('.decision').innerText,
   cards:document.querySelectorAll('.metric').length,attentionRows:document.querySelectorAll('#attention tbody tr').length,
   disclosures:document.querySelectorAll('.disclosure').length,openDisclosures:document.querySelectorAll('.disclosure[open]').length,
   caseRows:document.querySelectorAll('.case-row').length}));
  check(state.scrollWidth<=width,'Main horizontal overflow at '+width);
  check(state.conclusion.includes('NO_GO'),'Conclusion');
  check(state.cards===4&&state.attentionRows===3,'Essential summary inventory');
  check(state.disclosures===2&&state.openDisclosures===0,'Details closed by default');
  check(state.caseRows===0,'Detailed case list leaked onto landing page');
  await page.screenshot({path:path.join(folder,'main-'+width+'.png'),fullPage:true});
  await page.click('#case-reasons summary');check(await page.locator('#case-reasons').getAttribute('open')!==null,'Reasons expand');
  check((await page.locator('#case-reasons').innerText()).includes('273 P3'),'Current priority summary');
  await page.click('#sdlc-coverage summary');check(await page.locator('#sdlc-coverage tbody tr').count()===7,'Seven criterion explanations');
  check((await page.locator('#sdlc-coverage').innerText()).includes('Four simulated hours passed'),'Four-hour limit');
  await page.locator('#sdlc-coverage').scrollIntoViewIfNeeded();
  if(width===1280)await page.screenshot({path:path.join(folder,'expanded-coverage.png')});
  const detailsUrl=await page.locator('a[href="10-release-confidence-details.html#case-explorer"]').getAttribute('href');
  await page.goto(new URL(detailsUrl,pathToFileURL(path.join(task,'10-release-confidence.html'))).href);
  check(await page.locator('.case-row').count()===285,'All nonpass cases retained');
  check(await page.locator('.case-row:visible').count()===15,'Default failed filter');
  await page.fill('#case-search','RN-S035');
  check((await page.locator('.case-row:visible').innerText()).includes('Current priority: P3.'),'Exposure priority');
  await page.selectOption('#status-filter','PARTIALLY_EXECUTED');await page.fill('#case-search','RN-L004');
  check((await page.locator('.case-row:visible').innerText()).includes('Current priority: P3.'),'Listener priority');
  await page.fill('#case-search','');check((await page.locator('#case-count').innerText()).includes('of 199'),'Partial inventory');
  await page.selectOption('#status-filter','BLOCKED');check((await page.locator('#case-count').innerText()).includes('of 71'),'Blocked inventory');
  await page.click('#reset-filter');check((await page.locator('#case-count').innerText()).includes('of 285'),'All inventory');
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);check(!overflow,'Details overflow');
  if(width===1280){await page.locator('#priority-register').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(folder,'issue-priorities.png')});}
  check(errors.length===0,'Browser errors');captures.push({...state,browser_errors:errors,main_screenshot:'main-'+width+'.png',
    details_checks:'285 case rows, priority labels, search, status filters, and overflow passed'});await page.close();
 }
 await fs.writeFile(path.join(folder,'html-qa.json'),JSON.stringify({status:'PASSED',method:'Local Edge at390px,715px,1280px. Compact main report and linked detail view.',
  captures,visual_review:'PENDING',limits:['No application behavior was rerun. No actual mobile device or print check.']},null,2)+'\n');
}finally{await browser.close();}
