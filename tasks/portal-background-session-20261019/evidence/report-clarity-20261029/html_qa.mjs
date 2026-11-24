import { chromium } from '../../../../adapters/browser/node_modules/playwright/index.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const folder=path.dirname(fileURLToPath(import.meta.url));
const task=path.resolve(folder,'../..');
const browser=await chromium.launch({executablePath:'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  headless:true,args:['--disable-background-networking','--disable-component-update','--no-first-run']});
const captures=[];
function check(value,message){if(!value)throw new Error(message);}
try{
 for(const width of [390,715,1280]){
  const page=await browser.newPage({viewport:{width,height:1000}});
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  await page.goto(pathToFileURL(path.join(task,'10-release-confidence.html')).href);
  const state=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
   conclusion:document.querySelector('.decision').innerText,metrics:[...document.querySelectorAll('.stat')].map(x=>x.innerText),
   caseRows:document.querySelectorAll('.case-row').length,criterionRows:document.querySelectorAll('.ac-table tbody tr').length,
   reasonGroups:document.querySelectorAll('.reason-card').length,links:document.querySelectorAll('a').length}));
  check(state.scrollWidth<=state.width,'Horizontal overflow at '+width);
  check(state.conclusion.includes('NO_GO'),'Conclusion missing');
  check(state.metrics.length===4,'Four result cards required');
  check(state.caseRows===285&&state.criterionRows===7&&state.reasonGroups===21,'Explanation inventory mismatch');
  const count=()=>page.locator('#case-count').innerText();
  check((await count()).includes('of 15'),'Default failure count');
  check(await page.locator('.case-row:visible').count()===15,'Default failure rows');
  await page.selectOption('#status-filter','PARTIALLY_EXECUTED');
  check((await count()).includes('of 199'),'Partial count');
  await page.click('#next-page');check((await count()).startsWith('Showing 21–40'),'Pagination forward');
  await page.click('#previous-page');check((await count()).startsWith('Showing 1–20'),'Pagination backward');
  await page.fill('#case-search','RN-L011');
  check((await count()).includes('of 1 cases'),'Exact case search');
  check((await page.locator('.case-row:visible').innerText()).includes('RSA protected endpoint'),'Four-hour missing proof visible');
  await page.locator('.case-row:visible summary').click();
  check((await page.locator('.case-row:visible').innerText()).includes('Four controlled hours'),'What ran expands');
  await page.fill('#case-search','');await page.selectOption('#status-filter','BLOCKED');
  check((await count()).includes('of 71'),'Blocked count');
  await page.click('#reset-filter');check((await count()).includes('of 285'),'Clear filters');
  await page.locator('.group-button[data-group="failed-logout"]').click();
  check((await count()).includes('of 1 cases'),'Reason group filter');
  check((await page.locator('.case-row:visible').innerText()).includes('RN-S002'),'Correct group member');
  await page.click('#reset-filter');await page.fill('#case-search','no-such-case-xyz');
  check(await count()==='0 cases','Empty search');check(await page.locator('#no-results').isVisible(),'Empty message');
  await page.click('#reset-filter');await page.selectOption('#status-filter','FAILED');
  await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
  const filename=width===1280?'html-1280.png':'top-'+width+'.png';
  if(width===1280)await page.screenshot({path:path.join(folder,filename),fullPage:true});
  await page.screenshot({path:path.join(folder,'top-'+width+'.png')});
  await page.locator('#acceptance-criteria').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(folder,'criteria-'+width+'.png')});
  await page.locator('#case-explorer').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(folder,'cases-'+width+'.png')});
  check(errors.length===0,'Browser errors: '+errors.join(';'));
  captures.push({screenshot:filename,...state,interactive_checks:'PASSED',browser_errors:errors});await page.close();
 }
 await fs.writeFile(path.join(folder,'html-qa.json'),JSON.stringify({status:'PASSED',
  method:'Headless Edge at 390px, 715px, and 1280px. Inventory, overflow, filters, search, grouping, pagination, and browser errors checked.',
  captures,visual_review:'PENDING',limits:['No actual mobile device or print rendering. Report rendering does not verify application behavior.']},null,2)+'\n');
}finally{await browser.close();}
