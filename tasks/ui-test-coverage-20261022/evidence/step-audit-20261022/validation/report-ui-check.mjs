import { chromium, expect } from '@playwright/test';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';
import crypto from 'node:crypto';

const output=path.resolve('tasks/ui-test-coverage-20261022/evidence/step-audit-20261022/validation');
const report=path.resolve('tasks/ui-test-coverage-20261022/evidence/audit-run-20261022/report-002');
const {browserLaunchOptions}=await import(pathToFileURL(path.resolve('e2e/browser-config.ts')).href);
const browser=await chromium.launch(browserLaunchOptions());
const page=await browser.newPage({viewport:{width:1440,height:1100}});
const checks=[];
const screenshots=[];
async function capture(name){
 const file=path.join(output,name+'.png');
 await page.screenshot({path:file,animations:'disabled'});
 const bytes=await fs.readFile(file);
 screenshots.push({path:path.relative(process.cwd(),file),sha256:crypto.createHash('sha256').update(bytes).digest('hex')});
}
try{
 await page.goto(pathToFileURL(path.join(report,'index.html')).href);
 await expect(page.locator('tbody tr')).toHaveCount(521);
 await page.locator('#status').selectOption('FAIL');
 await expect(page.locator('tbody tr:visible')).toHaveCount(72);
 checks.push('All 521 case rows exist. The FAIL filter shows 72 rows.');
 await page.locator('#status').selectOption('');
 await page.locator('#search').fill('AUTH-084:');
 await expect(page.locator('tbody tr:visible')).toHaveCount(1);
 await capture('report-index-filter');
 await page.goto(pathToFileURL(path.join(report,'cases/AUTH-084.html')).href);
 await expect(page.locator('h2').first()).toContainText('Latest local result: PASS');
 await expect(page.locator('.attempt-history')).not.toHaveAttribute('open','');
 const executed=page.locator('.latest-attempt .step-timeline > li').filter({hasText:/Execution: (PASSED|FAILED)/});
 for(const step of await executed.all())expect(await step.locator('img').count()).toBeGreaterThan(0);
 checks.push('AUTH-084 shows latest PASS first. Earlier attempts remain collapsed. Each executed latest step has an image.');
 await capture('report-auth084-latest');
 await page.goto(pathToFileURL(path.join(report,'cases/UX-043.html')).href);
 await expect(page.locator('h2').first()).toContainText('BLOCKED_NOT_EXECUTED');
 const pending=page.locator('.latest-attempt .step-timeline > li').filter({hasText:'Execution: NOT_EXECUTED'});
 await expect(pending).toHaveCount(3);
 for(const step of await pending.all())await expect(step.locator('img')).toHaveCount(0);
 checks.push('UX-043 shows its active blocker and three unexecuted steps without invented images.');
 await capture('report-ux043-blocker');
 await fs.writeFile(path.join(output,'report-ui-check.json'),JSON.stringify({checkedAt:new Date().toISOString(),status:'PASSED',browserVersion:browser.version(),checks,screenshots,limit:'These checks inspect report presentation. They do not execute business cases.'},null,2)+'\n');
}finally{await browser.close();}
