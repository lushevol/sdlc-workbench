import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';
const out = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(out, '../../../..');
const task = path.join(root, 'tasks/portal-background-session-20261019');
const { chromium } = await import(pathToFileURL(path.join(root, 'adapters/browser/node_modules/playwright/index.mjs')).href);
const result = {status:'RUNNING', started_at:new Date().toISOString(), kind:'Local report artifact rendering', application_execution:false, cases:[], limits:['These browser checks verify report presentation. They add no application, UAT, deployment, or publication evidence.']};
const save = () => fs.writeFileSync(path.join(out, 'report-browser-checks.json'), JSON.stringify(result,null,2)+'\n');
save();
const browser = await chromium.launch({executablePath:'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless:true,args:['--disable-background-networking','--disable-component-update','--no-first-run','--no-default-browser-check']});
try {
  for (const file of ['10-release-confidence.html','10-release-confidence-details.html']) {
    for (const width of [1280,390]) {
      const context = await browser.newContext({viewport:{width,height:900},deviceScaleFactor:1});
      await context.route('**/*', route => /^(file:|data:)/.test(route.request().url()) ? route.continue() : route.abort());
      const page = await context.newPage();
      const pageErrors=[];
      page.on('pageerror', error=>pageErrors.push(error.message));
      await page.goto(pathToFileURL(path.join(task,file)).href,{waitUntil:'load'});
      const row = {file,width,status:'RUNNING',page_errors:pageErrors,screenshots:[]};
      result.cases.push(row);
      const details = page.locator('#knowledge-sync-details');
      row.default_collapsed = !(await details.evaluate(el=>el.open));
      row.runtime_default_collapsed = !(await page.locator('#runtime-log-details').evaluate(el=>el.open));
      const capture = async phase => {
        const name = `${file.replace('.html','')}-knowledge-${width}-${phase}.png`;
        const bytes = await page.locator('#knowledge-sync').screenshot({path:path.join(out,name)});
        row.screenshots.push({file:name,phase,captured_at:new Date().toISOString(),method:'Playwright element screenshot',sha256:crypto.createHash('sha256').update(bytes).digest('hex'),claim:`Knowledge supplement ${phase} at ${width}px`,limits:'Rendered report artifact; no business execution'});
      };
      await capture('collapsed');
      await details.locator('summary').click();
      row.disclosure_works = await details.evaluate(el=>el.open);
      row.knowledge_rows = await details.locator('tbody tr').count();
      row.rows_visible = await details.locator('tbody').isVisible();
      row.layout = await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,viewport_width:innerWidth,document_width:document.documentElement.scrollWidth}));
      row.section_within_viewport = await page.locator('#knowledge-sync').evaluate(el=>{const r=el.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth});
      await capture('expanded');
      row.status = row.default_collapsed && row.runtime_default_collapsed && row.disclosure_works && row.knowledge_rows===4 && row.rows_visible && !row.layout.overflow && row.section_within_viewport && pageErrors.length===0 ? 'PASSED':'FAILED';
      save();
      await context.close();
    }
  }
  result.status = result.cases.every(c=>c.status==='PASSED')?'PASSED':'FAILED';
  result.completed_at = new Date().toISOString();
  result.source_hashes = ['10-release-confidence.html','10-release-confidence-details.html'].map(file=>({file,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(task,file))).digest('hex')}));
  save();
  console.log(JSON.stringify({status:result.status,cases:result.cases.map(({file,width,status,knowledge_rows,layout})=>({file,width,status,knowledge_rows,layout}))},null,2));
} catch(error) {
  result.status='FAILED';result.error=String(error);save();throw error;
} finally {await browser.close();}
if(result.status!=='PASSED')process.exitCode=1;
