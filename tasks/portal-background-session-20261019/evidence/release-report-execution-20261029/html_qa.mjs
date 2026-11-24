import { chromium } from '../../../../adapters/browser/node_modules/playwright/index.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const folder=path.dirname(fileURLToPath(import.meta.url));
const task=path.resolve(folder,'../..');
const browser=await chromium.launch({executablePath:'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  headless:true,args:['--disable-background-networking','--disable-component-update','--no-first-run']});
const captures=[];
try{
 for(const width of [715,1280]){
  const page=await browser.newPage({viewport:{width,height:1000}});
  await page.goto(pathToFileURL(path.join(task,'10-release-confidence.html')).href);
  const state=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
   conclusion:document.querySelector('.decision').innerText,metrics:[...document.querySelectorAll('.metric')].map(x=>x.innerText),
   riskRows:document.querySelectorAll('tbody tr').length,links:document.querySelectorAll('a').length}));
  if(state.scrollWidth>state.width)throw new Error('Horizontal content clipping at '+width);
  if(!state.conclusion.includes('NO_GO'))throw new Error('Conclusion missing');
  if(state.metrics.length!==4)throw new Error('Metric card missing');
  const filename='html-'+width+'.png';await page.screenshot({path:path.join(folder,filename),fullPage:true});
  captures.push({screenshot:filename,...state});await page.close();
 }
 await fs.writeFile(path.join(folder,'html-qa.json'),JSON.stringify({status:'PASSED',
  method:'Headless Edge rendering at715px and1280px; DOM overflow and required-content checks. Images receive separate visual review.',
  captures,visual_review:'PENDING',limits:['No actual mobile device or print rendering. Report rendering does not verify application behavior.']},null,2)+'\n');
}finally{await browser.close();}
