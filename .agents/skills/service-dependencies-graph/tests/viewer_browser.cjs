'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(path.join(process.cwd(), 'node_modules/@playwright/test'));

(async () => {
  const input = path.resolve(process.argv[2]), output = path.resolve(process.argv[3]);
  fs.mkdirSync(output, {recursive:true});
  const browser = await chromium.launch({headless:true,
    ...(process.env.WORKBENCH_GRAPH_BROWSER ? {executablePath:process.env.WORKBENCH_GRAPH_BROWSER} : {})});
  const page = await browser.newPage({viewport:{width:1366,height:768}});
  const errors = [], requests = [];
  page.on('pageerror', error=>errors.push(error.message));
  page.on('request', request=>requests.push(request.url()));
  const start = performance.now();
  await page.goto(pathToFileURL(input).href);
  await page.waitForSelector('g.node');
  const initialMs = performance.now()-start;
  assert.equal(requests.filter(url=>url.endsWith('.js')).length,0,'Startup must load only the summary HTML');
  const roots = await page.evaluate(()=>[...rootIds]);
  assert.equal(await page.locator('g.node').count(),roots.length);
  assert.equal(await page.locator('#overview').evaluate(element=>element.open),false);
  assert.equal(await page.locator('#legend').evaluate(element=>element.open),false);
  const layouts=[];
  for(const [width,height] of [[1366,768],[1440,900],[1024,768]]){
    await page.setViewportSize({width,height});
    const layout=await page.evaluate(()=>({width:innerWidth,height:innerHeight,scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight}));
    assert(layout.scrollWidth<=width&&layout.scrollHeight<=height,JSON.stringify(layout));
    layouts.push(layout);
  }
  await page.setViewportSize({width:1366,height:768});
  await page.screenshot({path:path.join(output,'overview.png')});
  const root = roots.find(id=>id.includes('single-ui-bff'))||roots.find(id=>id.includes('service:'))||roots[0];
  const rootSelector='g.node[data-node='+JSON.stringify(root)+']';
  await page.locator(rootSelector).click();
  await page.waitForFunction(id=>branches.has(id),root);
  const groups=await page.evaluate(id=>[...nodes.values()].filter(node=>node.parent===id&&node.type==='DEPENDENCY_GROUP').map(node=>({id:node.id,pages:node.pages,family:node.family})),root);
  assert(groups.length>0);
  await page.screenshot({path:path.join(output,'repository-expanded.png')});
  const group=groups.find(row=>row.family==='api')||groups.find(row=>row.family==='shared')||groups[0];
  await page.locator('g.node[data-node='+JSON.stringify(group.id)+']').click();
  await page.waitForFunction(id=>branches.has(id),group.id);
  if(group.pages>1){
    await page.locator('[data-more='+JSON.stringify(group.id)+']').click();
    await page.waitForFunction(id=>branches.get(id).pages===2,group.id);
  }
  const rootRetention=await page.evaluate(ids=>ids.every(id=>projection().nodes.some(node=>node.id===id)),roots);
  assert(rootRetention);
  const duplicates=await page.locator('g.node').evaluateAll(items=>items.length-new Set(items.map(item=>item.dataset.node)).size);
  assert.equal(duplicates,0);
  const canonical=await page.evaluate(id=>[...branches.get(id).edges].find(key=>!edges.get(key).navigation),group.id);
  if(canonical){
    await page.evaluate(id=>selectItem('edge',id),canonical);
    await page.locator('#source-details > summary').click();
    await page.waitForFunction(()=>document.getElementById('record-content').textContent.includes('Source evidence'));
    await page.screenshot({path:path.join(output,'dependency-evidence.png')});
  }
  await page.locator('#collapse').click();
  assert.equal(await page.locator('g.node').count(),roots.length);
  await page.locator('#overview > summary').click();
  assert.equal(await page.locator('.repo-chip').count(),roots.length);
  await page.locator('#overview > summary').click();
  assert.equal(await page.locator('#error').isVisible(),false);
  assert.deepEqual(errors,[]);
  const receipt={status:'PASSED',browser:await browser.version(),initial_ms:initialMs,repositories:roots.length,
    startup_data_requests:0,layouts,progressive_expansion:true,load_more:group.pages>1,
    unique_nodes:true,roots_retained:true,evidence_inspected:Boolean(canonical),collapse_restores_overview:true,errors};
  fs.writeFileSync(path.join(output,'browser-result.json'),JSON.stringify(receipt,null,2)+'\n');
  console.log(JSON.stringify(receipt));
  await browser.close();
})().catch(error=>{console.error(error);process.exit(1);});
