import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
const root = process.cwd();
const task = path.join(root, 'tasks/portal-background-session-20261019');
const out = path.join(task, 'evidence/runtime-log-html-20261031');
const {chromium} = await import(pathToFileURL(path.join(root, 'adapters/browser/node_modules/playwright/index.mjs')));
const browser = await chromium.launch({executablePath:'/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless:true});
const results = [];
try {
  for (const file of ['10-release-confidence.html', '10-release-confidence-details.html']) {
    for (const width of [1280, 390]) {
      const page = await browser.newPage({viewport:{width,height:900}});
      const errors = [];
      page.on('pageerror', error => errors.push(String(error)));
      await page.goto(pathToFileURL(path.join(task,file)).href);
      const panel = page.locator('#runtime-log-evidence');
      assert(await panel.isVisible());
      const text = await panel.innerText();
      assert(text.includes('Key release-confidence metric'));
      assert(text.includes('NOT_RUN') && text.includes('Metric: N/A'));
      assert(text.includes('5/6') && text.includes('83.3%'));
      assert(text.includes('3 cases passed') && text.includes('56 assertions passed') && text.includes('192/192'));
      assert.equal(await panel.locator('details').getAttribute('open'), null);
      await panel.locator('summary').click();
      assert(await panel.locator('table').isVisible());
      assert.equal(await panel.locator('tbody tr').count(), 6);
      const expanded = await panel.innerText();
      assert(expanded.includes('discard events lack request correlation'));
      assert(expanded.includes('historical 467-case assessment and its release hold'));
      const layout = await panel.evaluate(element => ({overflow:element.scrollWidth > element.clientWidth + 1,withinViewport:element.getBoundingClientRect().right <= innerWidth + 1}));
      assert(!layout.overflow && layout.withinViewport);
      assert.equal(errors.length, 0);
      const screenshot = file.replace('.html','') + '-' + width + '.png';
      await panel.screenshot({path:path.join(out,screenshot)});
      await panel.locator('summary').click();
      assert.equal(await panel.locator('details').getAttribute('open'), null);
      results.push({file,width,status:'PASSED',default_collapsed:true,disclosure_works:true,observations:6,layout,page_errors:errors,screenshot});
      await page.close();
    }
  }
} finally {
  await browser.close();
}
await fs.writeFile(path.join(out,'browser-checks.json'),JSON.stringify({browser:browser.version(),results},null,2)+'\n');
console.log(JSON.stringify({status:'PASSED',browser_checks:results.length}));
