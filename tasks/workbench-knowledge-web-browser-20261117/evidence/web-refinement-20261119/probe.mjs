// Run from the source checkout: node PATH/probe.mjs BASE_URL NEW_OUTPUT_DIRECTORY
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { chromium } from '../../../../adapters/browser/node_modules/playwright/index.mjs';

const [base, output] = process.argv.slice(2);
assert(base && output, 'Supply the local service URL and a new output directory.');
await mkdir(output, { recursive: false });
const root = process.cwd();
const result = { started_at: new Date().toISOString(), base, cases: [], source_hashes: {},
  environment: { node: process.version, platform: process.platform, browser: 'Installed Chromium, headless, disposable profile' },
  limits: ['Local macOS browser checks only.', 'The format and unsafe-content case substitutes one synthetic API document.'] };
for (const file of ['core/knowledge_web/server.py', 'core/knowledge_web/static/app.js',
  'core/knowledge_web/static/index.html', 'core/knowledge_web/static/styles.css', 'core/knowledge_web/static/marked.umd.js']) {
  result.source_hashes[file] = createHash('sha256').update(await readFile(file)).digest('hex');
}
const save = async () => writeFile(path.join(output, 'results.json'), JSON.stringify(result, null, 2) + '\n');
const browser = await chromium.launch({ headless: true, chromiumSandbox: true,
  executablePath: path.join(root, 'adapters/browser/.browsers/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing') });
result.environment.browser_version = browser.version();
const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
const pageErrors = [], remoteRequests = [];
page.on('pageerror', error => pageErrors.push(error.message));
page.on('request', request => { if (!request.url().startsWith(base) && /^https?:/.test(request.url())) remoteRequests.push(request.url()); });
const caseRun = async (id, run) => {
  const entry = { id, started_at: new Date().toISOString() };
  try { await run(entry); entry.status = 'PASSED'; }
  catch (error) { entry.status = 'FAILED'; entry.error = error.stack; throw error; }
  finally { entry.finished_at = new Date().toISOString(); result.cases.push(entry); await save(); }
};
const open = async (key) => {
  await page.goto(`${base}/?key=${encodeURIComponent(key)}`);
  await page.locator('#article-body').waitFor();
};
try {
  await caseRun('knowledge-scope-and-authored-navigation', async entry => {
    const navigation = await (await page.request.get(`${base}/api/navigation`)).json();
    const documents = navigation.collections.flatMap(collection => collection.documents);
    assert(documents.every(doc => doc.path.startsWith('knowledge/')));
    assert(!documents.some(doc => /\/(audit|processing|incoming|\.openkb)\/|\/log\.md$|\.log$/.test(doc.path)));
    assert(!navigation.collections.some(collection => collection.id === 'docs'));
    entry.collections = navigation.health.collections;
    await open('records:knowledge/records/candidates/index.md');
    await page.locator('#article-body table').first().waitFor();
    assert(await page.getByText('Canonical record', { exact: true }).isVisible());
    await page.screenshot({ path: path.join(output, 'canonical.png') });
    await page.locator('#article a[data-target="../../llm-wiki/wiki/index.md"]').click();
    await page.waitForURL(/wiki%3Aknowledge/);
    await page.locator('.authority-note').waitFor();
    entry.assertions = ['Every catalog path stays inside knowledge/.', 'Audit and runtime files are absent.', 'Canonical index tables render.', 'Authored canonical-to-wiki link opens the native wiki index.'];
  });
  await caseRun('wiki-native-links-and-canonical-aliases', async entry => {
    await open('wiki:knowledge/llm-wiki/wiki/summaries/KT-authentication-and-sessions.md');
    await page.locator('#article a[data-target="wiki:entities/portal-team"]').first().click();
    await page.waitForURL(/entities%2Fportal-team/);
    await open('wiki:knowledge/llm-wiki/wiki/summaries/KT-authentication-and-sessions.md');
    await page.locator('.inline-metadata summary').click();
    await page.locator('.inline-metadata a[data-target="sources/KT-authentication-and-sessions.md"]').click();
    await page.waitForURL(/records%3Aknowledge/);
    await page.getByText('Canonical record', { exact: true }).waitFor();
    entry.assertions = ['Native wikilinks open the correct entity.', 'Wiki full_text alias opens its one canonical source.', 'Canonical and derived authority labels stay distinct.'];
  });
  await caseRun('standard-markdown-and-unsafe-content-fixture', async entry => {
    const key = 'records:knowledge/records/candidates/index.md';
    const original = await (await page.request.get(`${base}/api/document?key=${encodeURIComponent(key)}`)).json();
    const content = '# Format fixture\n\n- Outer\n  - Inner\n\n| A | B |\n| --- | --- |\n| Last | Row |\n\n## 重复\n\n## 重复\n\n<a id="authored-anchor"></a>\n\n[Anchor](#authored-anchor)\n\n[Unsafe](javascript:alert(1))\n\n<img src=x onerror="window.__executed=true">\n\n![Missing](https://example.invalid/image.png)\n\n[Outside](../../../../docs/README.md)\n';
    await page.route('**/api/document?*', async route => {
      const url = new URL(route.request().url());
      if (url.searchParams.get('key') === key) await route.fulfill({ json: { ...original, content, metadata: { type: 'KnowledgeTopic', status: 'draft', governance_state: 'candidate' } } });
      else await route.continue();
    });
    await open(key);
    assert.equal(await page.locator('#article-body ul ul li').textContent(), 'Inner');
    assert.equal(await page.locator('#article-body tbody tr').count(), 1);
    assert.equal(await page.locator('#article-body #重复-1').count(), 1);
    assert.equal(await page.locator('#article-body #authored-anchor').count(), 1);
    assert.equal(await page.locator('#article-body script, #article-body img, #article-body a[href^="javascript:"]').count(), 0);
    assert.equal(await page.evaluate(() => window.__executed), undefined);
    await page.locator('a[data-target="#authored-anchor"]').click();
    await page.waitForURL(/#authored-anchor$/);
    await page.locator('a[data-target="../../../../docs/README.md"]').click();
    await page.getByRole('status').filter({ hasText: 'unavailable in the knowledge folder' }).waitFor();
    await page.unroute('**/api/document?*');
    entry.assertions = ['Nested lists and final table rows render.', 'Unicode duplicate headings receive unique anchors.', 'Authored anchors work.', 'Raw HTML and unsafe links remain inert.', 'Remote images make no request.', 'Outside links report the scope boundary.'];
  });
  await caseRun('original-wiki-graph-and-sandbox', async entry => {
    await page.locator('#graph-button').click();
    const frame = page.frameLocator('iframe[title="Wiki relationship graph"]');
    await frame.locator('#ncount').waitFor();
    assert.equal(await page.locator('iframe').getAttribute('sandbox'), 'allow-scripts');
    entry.nodes = await frame.locator('#ncount').textContent();
    entry.edges = await frame.locator('#ecount').textContent();
    assert(Number.parseInt(entry.nodes, 10) > 0);
    await frame.locator('#search').fill('session');
    await page.screenshot({ path: path.join(output, 'wiki-graph.png') });
    assert.equal(await frame.locator('body').evaluate(() => { try { return parent.document.title; } catch (error) { return error.name; } }), 'SecurityError');
    entry.assertions = ['Original graph executes with nonzero nodes.', 'Graph search accepts interaction.', 'Opaque sandbox blocks access to the reader document.'];
  });
  await caseRun('mobile-browse-and-search', async entry => {
    await page.setViewportSize({ width: 390, height: 844 });
    const brand = await page.locator('.brand strong').boundingBox();
    const browse = await page.locator('#browse-toggle').boundingBox();
    assert(brand.x + brand.width <= browse.x, 'The mobile header title must not overlap Browse.');
    await page.locator('#browse-toggle').click();
    await page.locator('#collections-panel').waitFor({ state: 'visible' });
    await page.locator('[data-key="records:knowledge/records/candidates/index.md"]').click();
    await page.waitForURL(/records%3Aknowledge/);
    assert.equal(await page.locator('#browse-toggle').getAttribute('aria-expanded'), 'false');
    await page.locator('#search').fill('session');
    await page.locator('.search-result').first().waitFor();
    const searchResult = page.locator('.search-result').filter({ hasNotText: 'Portal knowledge map' }).first();
    const resultKey = await searchResult.getAttribute('data-key');
    await searchResult.click();
    await page.waitForURL(url => url.searchParams.get('key') === resultKey);
    await page.locator('#article-body').waitFor();
    await page.locator('#search-panel').waitFor({ state: 'hidden' });
    await page.screenshot({ path: path.join(output, 'mobile.png') });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    entry.assertions = ['Header title and Browse do not overlap.', 'Narrow-screen browse opens and closes.', 'Search opens its selected result.', 'No horizontal page overflow at 390 pixels.'];
  });
  assert.deepEqual(pageErrors, []);
  assert.deepEqual(remoteRequests, []);
  result.status = 'PASSED';
} catch (error) { result.status = 'FAILED'; result.error = error.stack; process.exitCode = 1; }
finally {
  result.page_errors = pageErrors; result.remote_requests = remoteRequests; result.finished_at = new Date().toISOString();
  for (const file of ['canonical.png', 'wiki-graph.png', 'mobile.png']) {
    try { result.source_hashes[file] = createHash('sha256').update(await readFile(path.join(output, file))).digest('hex'); } catch {}
  }
  await save(); await browser.close(); console.log(JSON.stringify({ status: result.status, cases: result.cases.map(({ id, status }) => ({ id, status })), output }));
}
