import { chromium } from '../../../../adapters/browser/node_modules/playwright/index.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath,pathToFileURL } from 'node:url';
const folder=path.dirname(fileURLToPath(import.meta.url)),task=path.resolve(folder,'../..');
const browser=await chromium.launch({executablePath:'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless:true,
 args:['--disable-background-networking','--disable-component-update','--no-first-run']});
function check(value,message){if(!value)throw new Error(message);}
const captures=[];
try{
 for(const width of [390,715,1280]){
  const page=await browser.newPage({viewport:{width,height:1000}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.join(task,'10-release-confidence.html')).href);
  const state=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
   height:document.documentElement.scrollHeight,openDetails:document.querySelectorAll('details[open]').length,
   caseDetails:document.querySelectorAll('[id^="case-rn-"]').length,groupDetails:document.querySelectorAll('[id^="group-"]').length,
   adverseCriterionDetails:document.querySelectorAll('[id^="criterion-ac-"]').length,
   attentionDetails:document.querySelectorAll('[id^="attention-rn-"],[id^="attention-review-"]').length,
   conclusion:document.querySelector('.decision').innerText,metricCards:document.querySelectorAll('.metric').length}));
  check(state.scrollWidth<=width,'Main overflow at '+width);check(state.openDetails===0,'All details must start collapsed');
  check(state.caseDetails===285&&state.groupDetails===21,'Complete case explanations');
  check(state.adverseCriterionDetails===4&&state.attentionDetails===3,'AC and attention explanations');
  check(state.metricCards===4&&state.conclusion.includes('NO_GO'),'Compact summary retained');
  await page.click('#review-details>summary');
  check(await page.locator('#review-details [id^="review-review-"]').count()===18,'All review findings expandable');
  await page.click('#review-details>summary');
  await page.click('#unit-details>summary');
  check((await page.locator('#unit-details').innerText()).includes('No unit result is partial or blocked'),'Unit complete execution boundary');
  await page.click('#unit-details>summary');
  if(width===1280)await page.screenshot({path:path.join(folder,'collapsed-default.png'),fullPage:true});
  await page.click('#case-reasons>summary');
  for(const [id,count] of [['cases-failed',15],['cases-partially_executed',199],['cases-blocked',71]]){
   await page.locator('#'+id+'>summary').click();
   check(await page.locator('#'+id+' [id^="case-rn-"]').count()===count,'Status case count '+id);
   await page.locator('#'+id+'>summary').click();
  }
  await page.click('#cases-failed>summary');await page.click('#group-failed-logout>summary');await page.click('#case-rn-s002>summary');
  check((await page.locator('#case-rn-s002').innerText()).includes('Release hold for the assessed source'),'P1 impact details');
  check(await page.locator('#case-rn-s002 a').count()>=3,'Case evidence links');
  if(width===1280){await page.locator('#case-rn-s002').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(folder,'expanded-failure.png')});}
  await page.click('#sdlc-coverage>summary');
  await page.click('#criteria-failed>summary');await page.click('#criterion-ac-1>summary');
  check((await page.locator('#criterion-ac-1').innerText()).includes('Every movement restarts a five-second timer'),'AC failure reason');
  await page.click('#criteria-partial>summary');await page.click('#criterion-ac-4>summary');
  check((await page.locator('#criterion-ac-4').innerText()).includes('Actual identity-provider prompts'),'AC partial limit');
  await page.click('#criteria-blocked>summary');
  check((await page.locator('#criteria-blocked').innerText()).includes('No acceptance criterion has a blocked disposition'),'Zero blocked criteria explicit');
  if(width===1280){await page.locator('#criterion-ac-4').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(folder,'expanded-criterion.png')});}
  await page.click('#attention-rn-s002>summary');check((await page.locator('#attention-rn-s002').innerText()).includes('RSA-validating'),'Attention evidence expands');
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);check(!overflow,'Expanded overflow at '+width);
  check(errors.length===0,'Browser errors');
  captures.push({...state,interactions:'PASSED',expanded_overflow:false,browser_errors:errors});await page.close();
 }
 await fs.writeFile(path.join(folder,'html-qa.json'),JSON.stringify({status:'PASSED',method:'Local Edge at390px,715px,1280px; default collapsed state, case and AC expansion, links and overflow.',
  captures,visual_review:'PENDING',limits:['No application tests rerun. No actual mobile device or print check.']},null,2)+'\n');
}finally{await browser.close();}
