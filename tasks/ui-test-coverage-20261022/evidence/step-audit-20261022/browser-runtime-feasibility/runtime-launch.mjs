import {mkdir,readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const packagePath=path.resolve(process.env.E2E_RUNTIME_PACKAGE??'node_modules/playwright/index.mjs');
const output=path.resolve(process.env.E2E_RUNTIME_OUTPUT??'tasks/ui-test-coverage-20261022/evidence/step-audit-20261022/browser-runtime-feasibility/connected-launch');
const playwright=await import(pathToFileURL(packagePath).href);
await mkdir(output,{recursive:true});
const results=[];
for(const engine of ['firefox','webkit']){
 const result={engine,packagePath,browserPath:process.env.PLAYWRIGHT_BROWSERS_PATH,startedAt:new Date().toISOString(),scope:'SYNTHETIC_RUNTIME_PROVISIONING_ONLY'};
 let browser;
 try{
  const executable=playwright[engine].executablePath();
  result.executablePath=executable;result.executableSha256=createHash('sha256').update(await readFile(executable)).digest('hex');
  browser=await playwright[engine].launch({headless:true});
  result.browserVersion=browser.version();
  const page=await browser.newPage({viewport:{width:1000,height:700}});
  await page.setContent('<!doctype html><html><body><h1>Local browser runtime check</h1><p>This page is a synthetic provisioning fixture.</p><button onclick="document.querySelector(\'output\').textContent=\'1\'">Count</button><output>0</output></body></html>');
  await page.getByRole('button',{name:'Count',exact:true}).click();
  const actual=await page.locator('output').innerText();
  if(actual!=='1')throw new Error(`Expected counter1,received${actual}`);
  result.counter=actual;
  const screenshot=path.join(output,`${engine}.png`);await page.screenshot({path:screenshot,fullPage:true});
  result.screenshot=screenshot;result.screenshotSha256=createHash('sha256').update(await readFile(screenshot)).digest('hex');
  result.status='PASSED';
 }catch(error){result.status='FAILED';result.error=String(error?.stack??error);}
 finally{await browser?.close();result.finishedAt=new Date().toISOString();results.push(result);await writeFile(path.join(output,'result.json'),`${JSON.stringify({results,limitations:['Synthetic launch and counter checks establish runtime provisioning only.','No business application, Safari browser, provider, or business acceptance is measured.']},null,2)}\n`);}
}
process.stdout.write(`${JSON.stringify(results,null,2)}\n`);
if(results.some(result=>result.status!=='PASSED'))process.exitCode=1;
