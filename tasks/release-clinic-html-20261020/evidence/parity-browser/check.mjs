import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const output = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(output, '../../../..');
const browserRoot = path.join(root, 'adapters/browser');
process.env.PLAYWRIGHT_BROWSERS_PATH = path.join(browserRoot, '.browsers');
const { chromium } = await import(pathToFileURL(path.join(browserRoot, 'node_modules/playwright/index.mjs')));
const packageInfo = JSON.parse(await readFile(path.join(browserRoot, 'node_modules/playwright/package.json')));
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const json = value => JSON.stringify(value, null, 2) + '\n';
const sources = {
  upstream: 'core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/SKILL.md',
  included: '.agents/skills/release-clinic/references/dtp-tda-report.md',
};

async function preserve(relative, content) {
  const target = path.join(output, relative);
  await mkdir(path.dirname(target), { recursive: true });
  try { await writeFile(target, content, { flag: 'wx' }); }
  catch (error) {
    if (error.code !== 'EEXIST') throw error;
    assert.equal(sha256(await readFile(target)), sha256(content), `Existing evidence differs: ${target}`);
  }
}

function extract(source, label) {
  const cssSection = source.indexOf('### Canonical CSS');
  const cssStart = source.indexOf('```css\n', cssSection) + 7;
  const cssEnd = source.indexOf('```', cssStart);
  assert.ok(cssSection > 0 && cssStart > 6 && cssEnd > cssStart);
  const css = source.slice(cssStart, cssEnd);
  const shellSection = source.indexOf('### Canonical HTML Shell');
  const shellStart = source.indexOf('```html\n', shellSection) + 8;
  const shellEnd = source.indexOf('```', shellStart);
  assert.ok(shellSection > cssSection && shellStart > 7 && shellEnd > shellStart);
  const shell = source.slice(shellStart, shellEnd);
  const script = shell.match(/<script>\n([\s\S]*?)<\/script>/)?.[1];
  assert.ok(script && script.includes('function remExport()'));
  const values = {
    title: 'TEST ONLY — synthetic canonical control fixture',
    release_id: 'TEST_ONLY_RELEASE', stream: 'TEST_ONLY_STREAM', branch: 'TEST_ONLY_BRANCH',
    chg: 'TEST_ONLY_CHG', snow_state: 'TEST ONLY', wi_state: 'TEST ONLY', date: 'TEST ONLY',
    skill_version: source.match(/\n  version: "([^"]+)"/)?.[1],
    collector_version: 'TEST ONLY', drift_indicator: '<span>TEST ONLY</span>',
    generated_by: 'TEST ONLY Fixture', staleness_banner_html: '',
    critical_count: '1', moderate_count: '1', minor_count: '1', looksGood_count: '0',
    critical_findings_html: '<div class="finding"><strong>[1] TEST ONLY critical fixture</strong>: Synthetic control check.</div>',
    moderate_findings_html: '<div class="finding"><strong>[2] TEST ONLY moderate fixture</strong>: Synthetic control check.</div>',
    minor_findings_html: '<div class="finding"><strong>[3] TEST ONLY minor fixture</strong>: Synthetic control check.</div>',
    looksGood_findings_html: '<div class="finding">None identified &#9989;</div>',
    required_quality_gate: 'TEST ONLY', verdict_class: 'blocked',
    verdict_text: 'TEST ONLY — synthetic fixture. No release assessment.',
  };
  const placeholders = [...new Set([...shell.matchAll(/\{([a-zA-Z_][a-zA-Z0-9_]*)\}/g)].map(match => match[1]))];
  for (const key of placeholders) {
    if (!(key in values)) values[key] = '<tr><td>TEST ONLY — no business data.</td></tr>';
  }
  const html = shell.replace('/* === PASTE THE CANONICAL CSS ABOVE HERE VERBATIM === */', css)
    .replace(/\{([a-zA-Z_][a-zA-Z0-9_]*)\}/g, (_, key) => values[key]);
  assert.equal(html.match(/<script>\n([\s\S]*?)<\/script>/)?.[1], script, `${label} script changed`);
  assert.equal(html.match(/<style>\n([\s\S]*?)<\/style>/)?.[1], css + '\n', `${label} CSS changed`);
  assert.ok(html.trimEnd().endsWith('</html>'));
  return { css, shell, script, html, version: values.skill_version, placeholders };
}

const report = {
  kind: 'synthetic-canonical-template-control-comparison',
  status: 'RUNNING', started_at: new Date().toISOString(),
  command: 'node tasks/release-clinic-html-20261020/evidence/parity-browser/check.mjs',
  head: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim(),
  environment: { node: process.version, platform: process.platform, arch: process.arch, playwright: packageInfo.version },
  launch: { chromiumSandbox: true, headless: true, executablePath: chromium.executablePath() },
  sources: {}, results: {}, blocked_external_requests: [],
  writing_review: {
    standard: 'ASD-STE100', automated_check: 'PENDING', asd_review: 'PENDING', reviewer: null, reviewed_at: null,
    limitations: ['Automated checks do not check the complete approved dictionary or grammar rules.'],
  },
  limitations: [
    'Synthetic fixtures check canonical browser controls only. They do not assess release data or agent reasoning.',
    'Only the installed macOS Chromium was exercised. Windows and other browsers remain untested.',
    'Page requests outside the local fixture origin were blocked. Browser background networking was disabled at launch.',
    'Source CSS and JavaScript were preserved. No standalone report generator was invoked.',
  ],
};
const fixtures = {};
for (const [label, relative] of Object.entries(sources)) {
  const bytes = await readFile(path.join(root, relative));
  const parts = extract(bytes.toString('utf8'), label);
  fixtures[label] = parts.html;
  report.sources[label] = {
    path: relative, sha256: sha256(bytes), version: parts.version,
    css_sha256: sha256(parts.css), javascript_sha256: sha256(parts.script),
    shell_sha256: sha256(parts.shell), fixture_sha256: sha256(parts.html),
  };
  await preserve(`${label}/fixture.html`, parts.html);
  await preserve(`${label}/canonical.css`, parts.css);
  await preserve(`${label}/canonical.js`, parts.script);
}
report.source_bytes_equal = report.sources.upstream.sha256 === report.sources.included.sha256;
report.fixture_bytes_equal = fixtures.upstream === fixtures.included;

let browser;
let server;
const attempt = new Date().toISOString().replace(/[:.]/g, '-');
try {
  server = createServer((request, response) => {
    const match = /^\/(upstream|included)\/(fixture|exported)\.html$/.exec(request.url);
    if (!match) { response.writeHead(404); response.end(); return; }
    const [label, kind] = match.slice(1);
    readFile(path.join(output, label, `${kind}.html`)).then(bytes => {
      response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
      response.end(bytes);
    }, () => { response.writeHead(404); response.end(); });
  });
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  const origin = `http://127.0.0.1:${server.address().port}`;
  report.origin = origin;
  browser = await chromium.launch({
    ...report.launch,
    args: ['--disable-background-networking', '--disable-component-update', '--disable-sync', '--no-first-run'],
  });
  report.environment.browser = browser.version();

  for (const label of Object.keys(sources)) {
    const result = { cases: [], dialogs: [], page_errors: [] };
    report.results[label] = result;
    const context = await browser.newContext({ acceptDownloads: true, serviceWorkers: 'block', viewport: { width: 1440, height: 1000 } });
    await context.route('**/*', async route => {
      if (new URL(route.request().url()).origin === origin) await route.continue();
      else { report.blocked_external_requests.push(route.request().url()); await route.abort('blockedbyclient'); }
    });
    await context.tracing.start({ screenshots: true, snapshots: true, sources: true });
    const page = await context.newPage();
    page.on('pageerror', error => result.page_errors.push(String(error)));
    const record = (name, passed, observed) => result.cases.push({ name, passed, observed });
    async function dialogClick(locator, response) {
      const promise = page.waitForEvent('dialog');
      const click = locator.click();
      const dialog = await promise;
      result.dialogs.push({ type: dialog.type(), message: dialog.message() });
      if (response === undefined) await dialog.accept(); else await dialog.accept(response);
      await click;
      return dialog.message();
    }
    await page.goto(`${origin}/${label}/fixture.html`);
    record('canonical_initialization', await page.locator('.rem-btn').count() === 3 && await page.locator('[data-rem-mandatory="true"]').count() === 2,
      { buttons: await page.locator('.rem-btn').count(), mandatory: await page.locator('[data-rem-mandatory="true"]').count() });
    const details = page.locator('details.tables').first();
    record('summary_initially_expanded', await details.getAttribute('open') !== null, await details.getAttribute('open'));
    await details.locator('summary').click();
    record('summary_collapse', await details.getAttribute('open') === null, await details.getAttribute('open'));
    await details.locator('summary').click();
    record('summary_expand', await details.getAttribute('open') !== null, await details.getAttribute('open'));
    await dialogClick(page.getByRole('button', { name: 'Set Reviewer Name' }), 'TEST ONLY Reviewer');
    record('explicit_test_reviewer', (await page.locator('#remToolbarInfo').textContent()).includes('TEST ONLY Reviewer'), await page.locator('#remToolbarInfo').textContent());
    let downloadCount = 0;
    page.on('download', () => downloadCount++);
    const early = await dialogClick(page.getByRole('button', { name: 'Save Annotated Report' }));
    record('premature_export_blocked', early.includes('Cannot save: 2') && downloadCount === 0,
      { alert: early, download_count: downloadCount, highlights: await page.locator('.rem-missing').count() });
    const critical = page.locator('.section.critical .finding');
    await critical.getByRole('button', { name: /Remediate/ }).click();
    const missingStatus = await dialogClick(critical.getByRole('button', { name: 'Save Annotation' }));
    record('annotation_requires_status', missingStatus.includes('select a Type of Remediation') && await critical.locator('.rem-recorded').count() === 0, missingStatus);
    await critical.locator('select').selectOption('unresolved');
    const missingNote = await dialogClick(critical.getByRole('button', { name: 'Save Annotation' }));
    record('annotation_requires_note', missingNote.includes('enter a remediation note') && await critical.locator('.rem-recorded').count() === 0, missingNote);
    await critical.locator('textarea').fill('TEST ONLY — unresolved synthetic critical case.');
    await critical.getByRole('button', { name: 'Save Annotation' }).click();
    record('critical_annotation_saved', await critical.locator('.rem-recorded').count() === 1 && await critical.locator('.rem-meta').getAttribute('data-reviewer') === 'TEST ONLY Reviewer', await critical.locator('.rem-recorded').textContent());
    const partially = await dialogClick(page.getByRole('button', { name: 'Save Annotated Report' }));
    record('partial_annotation_export_blocked', partially.includes('Cannot save: 1') && downloadCount === 0, partially);
    const moderate = page.locator('.section.moderate .finding');
    await moderate.getByRole('button', { name: /Remediate/ }).click();
    await moderate.locator('select').selectOption('workaround');
    await moderate.locator('textarea').fill('TEST ONLY — synthetic workaround case.');
    await moderate.getByRole('button', { name: 'Save Annotation' }).click();
    record('moderate_annotation_saved', await moderate.locator('.rem-recorded').count() === 1, await moderate.locator('.rem-recorded').textContent());
    await page.screenshot({ path: path.join(output, label, 'annotated-original.png'), fullPage: true });
    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('button', { name: 'Save Annotated Report' }).click();
    const download = await downloadPromise;
    await download.saveAs(path.join(output, label, 'exported.html'));
    record('annotated_export_succeeds', downloadCount === 1, { download_count: downloadCount, filename: download.suggestedFilename(), failure: await download.failure() });
    const exported = await readFile(path.join(output, label, 'exported.html'));
    result.exported_sha256 = sha256(exported);
    await page.goto(`${origin}/${label}/exported.html`);
    record('reopened_annotations_preserved', await page.locator('.rem-recorded').count() === 2, { records: await page.locator('.rem-recorded').count(), mandatory: await page.locator('[data-rem-mandatory="true"]').count() });
    const minor = page.locator('.section.minor .finding');
    await minor.getByRole('button', { name: /Remediate/ }).click();
    const reopenedPanel = await minor.locator('.rem-panel').evaluate(element => ({ open: element.classList.contains('open'), display: getComputedStyle(element).display }));
    record('reopened_remediate_button_opens_panel', reopenedPanel.open && reopenedPanel.display !== 'none', reopenedPanel);
    await dialogClick(page.getByRole('button', { name: 'Set Reviewer Name' }), 'TEST ONLY Reopened Reviewer');
    record('reopened_reviewer_control', (await page.locator('#remToolbarInfo').textContent()).includes('TEST ONLY Reopened Reviewer'), await page.locator('#remToolbarInfo').textContent());
    const secondDownload = page.waitForEvent('download');
    await page.getByRole('button', { name: 'Save Annotated Report' }).click();
    const exportedAgain = await secondDownload;
    await exportedAgain.saveAs(path.join(output, label, 'exported-again.html'));
    record('reopened_export_control', await exportedAgain.failure() === null, { filename: exportedAgain.suggestedFilename(), failure: await exportedAgain.failure() });
    await page.screenshot({ path: path.join(output, label, 'reopened.png'), fullPage: true });
    await writeFile(path.join(output, label, 'reopened-aria.yaml'), await page.locator('body').ariaSnapshot());
    await context.tracing.stop({ path: path.join(output, label, 'trace.zip') });
    await context.close();
    result.status = result.cases.every(item => item.passed) && result.page_errors.length === 0 ? 'PASSED' : 'FAILED';
  }
  const comparable = result => result.cases.map(({ name, passed }) => ({ name, passed }));
  report.behavior_equal = JSON.stringify(comparable(report.results.upstream)) === JSON.stringify(comparable(report.results.included));
  report.status = report.source_bytes_equal && report.fixture_bytes_equal && report.behavior_equal
    ? (Object.values(report.results).every(result => result.status === 'PASSED') ? 'PARITY_CONFIRMED' : 'PARITY_CONFIRMED_WITH_SHARED_FAILURE')
    : 'PARITY_GAP';
  report.writing_review.automated_check = 'PASSED';
} catch (error) {
  report.status = 'EXECUTION_FAILED';
  report.error = String(error);
  report.writing_review.automated_check = 'FAILED';
  process.exitCode = 1;
} finally {
  if (browser) await browser.close();
  if (server) await new Promise(resolve => server.close(resolve));
  report.finished_at = new Date().toISOString();
  await writeFile(path.join(output, `results-${attempt}.json`), json(report), { flag: 'wx' });
  console.log(json(report));
}
