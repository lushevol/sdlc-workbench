// Actual React portal E2E with controlled login/validation responses and an unchanged permission-call consumer.
// Canonical definitions: ../06-test-cases.md#tc-fe-ces-010, #tc-fe-ces-011, #tc-fe-ces-012.
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import http from 'node:http';
import assert from 'node:assert/strict';

const directory = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(directory, '../../..');
process.env.PLAYWRIGHT_BROWSERS_PATH ??= path.join(root, 'adapters/browser/.browsers');
const { chromium, expect } = await import('@playwright/test');
const requireBase = createRequire(path.join(root, 'repos/ui/mfe-base/package.json'));
const output = path.resolve(process.env.CES_TEST_OUTPUT ?? path.join(directory, '../evidence/frontend-entitlement-implementation-20261106/portal-candidate'));
const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
await fs.mkdir(output, { recursive: true });
try { await fs.access(path.join(output, 'run.json')); throw new Error(`Refusing completed run overwrite: ${output}`); }
catch (error) { if (error.code !== 'ENOENT') throw error; }
const run = { startedAt: new Date().toISOString(), scope: 'ACTUAL_BASE_REACT_CONTROLLED_SERVICES', cases: [],
  substitutions: ['Login and validation APIs return synthetic fixtures; no real identity acceptance.',
    'Remote upper application is an isolated React consumer using the actual shared hasPermission API.',
    'Corporate toolkit custom elements are stubbed; native desktop startup and analytics are disabled.'],
  limits: ['No live CES, BFF controller, saved-view service, deployed import map, or native desktop execution.'] };
let browser, server;
try {
  const built = await requireBase('esbuild').build({ entryPoints: [path.join(directory, 'portal-entry.tsx')],
    bundle: true, write: false, format: 'iife', platform: 'browser', metafile: true,
    nodePaths: [path.join(root, 'repos/ui/mfe-base/node_modules')],
    loader: { '.svg': 'dataurl', '.png': 'dataurl', '.jpg': 'dataurl', '.gif': 'dataurl', '.css': 'empty', '.woff': 'dataurl', '.woff2': 'dataurl' },
    define: { 'process.env.NODE_ENV': '"development"', 'process.env.MFE_APP_PREFIX_STYLE': '"MicroWebUI_base"', 'process.env.orgName': '"fm"' },
    plugins: [{ name: 'declared-local-boundaries', setup(build) {
      build.onResolve({ filter: /\/Root\/import$/ }, args => args.importer.includes('mfe-ratan-container') ? { path: 'container-hooks', namespace: 'fixture' } : undefined);
      build.onResolve({ filter: /^@sctoolkit\/webkit/ }, () => ({ path: 'toolkit', namespace: 'fixture' }));
      build.onLoad({ filter: /.*/, namespace: 'fixture' }, args => ({ contents: args.path === 'container-hooks'
        ? 'export const Hooks = {getHooks: () => window.__base.Hooks.getHooks()};' : '', loader: 'js' }));
    } }],
  });
  run.sourceBindings = await Promise.all(Object.keys(built.metafile.inputs).filter(file => file.startsWith('repos/') && !file.includes('/node_modules/')).map(async file => ({path:file,sha256:digest(await fs.readFile(path.join(root,file)))})));
  run.scriptBindings = await Promise.all(['run-portal.mjs', 'portal-entry.tsx'].map(async file => ({ path: path.relative(root,path.join(directory,file)), sha256:digest(await fs.readFile(path.join(directory,file))) })));
  await fs.writeFile(path.join(output,'run-binding.json'), JSON.stringify(run,null,2));
  server = http.createServer((req,res) => {
    res.setHeader('content-type',req.url === '/app.js' ? 'application/javascript' : 'text/html');
    res.end(req.url === '/app.js' ? built.outputFiles[0].text : '<!doctype html><title>Local CES portal</title><div id="root"></div><script>window.fin=undefined;</script><script src="/app.js"></script>');
  });
  await new Promise((resolve,reject) => { server.once('error',reject);server.listen(0,'127.0.0.1',resolve); });
  browser = await chromium.launch({ channel:'chromium', headless:true, chromiumSandbox:true });
  run.browserVersion = browser.version();
  const url = `http://127.0.0.1:${server.address().port}`;
  const entities = [{name:'RATAN_ENTITLEMENT_RULE',applicationName:'RATAN',applicationId:'51358',roleName:null,id:null,roleId:null,roleList:['Role A','Role B'],subjects:[{id:null,name:'feature-a',entitlementSource:'EMS3',actions:[{id:null,name:'action-a'}]}]},
    {name:'X_RATANONE',applicationName:'RATAN',roleName:'PSS',id:2,roleId:2,subjects:[{id:2,name:'feature-b',actions:[{id:2,name:'action-a'}]}]}];
  const tiles = [1,2].map(id=>({id,title:id===1?'CES fixture':'EMS2 fixture',entryName:String(id),container:'@fixture/consumer',module:'fixture',tile:id===1?'/ces-fixture':'/legacy-fixture',imageDarkTheme:'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"/>',imageLightTheme:'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"/>',entity:[id===1?'RATAN_ENTITLEMENT_RULE':'X_RATANONE'],subject:`feature-${id===1?'a':'b'}`,entitlementSource:id===1?'EMS3':'EMS2',emailSupport:'fixture@example.test',parameters:{label:id===1?'CES fixture':'EMS2 fixture',permissionCode:`feature-${id===1?'a':'b'}:action-a`}}));
  tiles[0].subject = '';
  const routing=tiles.map(tile=>({tileId:String(tile.id),source:tile.entitlementSource,entityNames:tile.entity,features:[tile.id===1?'feature-a':tile.subject],...(tile.id===1?{applicationId:'51358'}:{})}));
  const payload={result:true,userInfo:JSON.stringify({sub:'1481696',fullName:'CES Fixture User',auth_time:Math.floor(Date.now()/1000),oud:JSON.stringify({userId:'1481696',fullName:'CES Fixture User'})}),entities,drawers:[{id:1,label:'Migration fixtures',tiles}],entitlementRouting:routing};
  const encode=value=>Buffer.from(JSON.stringify(value)).toString('base64url');
  const now=Math.floor(Date.now()/1000),token=`Bearer ${encode({alg:'none'})}.${encode({sub:'1481696',iat:now,exp:now+3600})}.fixture`;
  const context=await browser.newContext();
  const page=await context.newPage();
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  await context.route('**/*',async route=>{
    const target=new URL(route.request().url());
    if(target.origin!==url){await route.abort('blockedbyclient');return;}
    if(target.pathname.includes('/api/')){
      await route.fulfill({status:200,contentType:'application/json',headers:{'single-ui-authorization':token},body:JSON.stringify(payload)});return;
    }
    await route.continue();
  });
  await page.routeWebSocket('**/*',socket=>socket.close());
  await page.addInitScript(()=>{localStorage.setItem('SET_WORKSPACES',JSON.stringify([{id:'fixture-workspace',label:'Workspace 1',isActive:true,containers:[]}]))});
  async function check(id,name,operation){
    const record={id,name,startedAt:new Date().toISOString(),status:'RUNNING'};
    try{record.observations=await operation();record.status='PASSED';}
    catch(error){record.status='FAILED';record.error=error.stack;record.pageErrors=[...errors];}
    finally{
      record.endedAt=new Date().toISOString();
      const screenshot=`${id}-${name}.png`;
      try{await page.screenshot({path:path.join(output,screenshot),fullPage:true});record.screenshot={path:screenshot,sha256:digest(await fs.readFile(path.join(output,screenshot)))};}catch(error){record.captureError=error.message;}
      const filename=`${id}-${name}.json`;await fs.writeFile(path.join(output,filename),JSON.stringify(record,null,2));
      run.cases.push({id,name,status:record.status,path:filename});await fs.writeFile(path.join(output,'progress.json'),JSON.stringify(run.cases,null,2));
    }
  }
  await check('TC-FE-CES-013','login-routing',async()=>{
    await page.goto(`${url}/?show_normal_login=Y`);
    await page.getByPlaceholder('Enter Username').fill('1481696');
    await page.getByPlaceholder('Enter Password').fill('FixtureOnly1!');
    await page.getByRole('button',{name:'Sign In',exact:true}).click();
    await expect(page.getByRole('tab',{name:'Workspace 1',exact:true})).toBeVisible();
    const state=await page.evaluate(()=>window.__base.Hooks.getHooks().store);
    assert.deepEqual(state.entitlementRouting,routing);assert.deepEqual(state.user.entities,entities);
    return {routeCount:state.entitlementRouting.length,userId:state.user.id};
  });
  await check('TC-FE-CES-013','profile-structured-actions',async()=>{
    await page.getByTestId('MicroWebUI_base_avatar_IconButton').click();
    await page.getByTestId('MicroWebUI_base_avatar_Profile').click();
    await page.getByRole('button',{name:'RATAN :: RATAN_ENTITLEMENT_RULE :: Role A, Role B',exact:true}).click();
    await page.getByRole('button',{name:'feature-a',exact:true}).click();
    await expect(page.getByText('action-a',{exact:true})).toBeVisible();
    assert.equal(errors.length,0);return {profileLabel:'RATAN :: RATAN_ENTITLEMENT_RULE :: Role A, Role B',actions:['action-a']};
  });
  await check('TC-FE-CES-013','ordinary-launch',async()=>{
    await page.keyboard.press('Escape');
    await page.getByText('New Tile',{exact:true}).click();
    await page.getByText('CES fixture',{exact:true}).click();
    await expect(page.getByTestId('consumer-CES fixture').getByRole('button',{name:'Export fixture data'})).toBeEnabled();
    const state=await page.evaluate(()=>window.__base.Hooks.getHooks().store);
    const opened=state.workspaces.flatMap(item=>item.containers).find(item=>item.parameters?.label==='CES fixture');
    assert.equal(String(opened.applicationTileId),'1');assert.notEqual(opened.id,'1');
    await expect(page.getByTestId('consumer-CES fixture').getByTestId('scope')).toHaveText('1');
    await page.evaluate(()=>window.__dispatcher.dispatchOpenTile({label:'EMS2 fixture',permissionCode:'feature-b:action-a'},'legacy-fixture'));
    await expect(page.getByTestId('consumer-EMS2 fixture').getByRole('button',{name:'Export fixture data'})).toBeEnabled();
    await expect(page.getByTestId('consumer-EMS2 fixture').getByTestId('scope')).toHaveText('2');
    return {applicationTileId:opened.applicationTileId,scopeForwarded:true,ordinaryDispatcherArguments:2};
  });
  await check('TC-FE-CES-013','refresh-withdraws-access',async()=>{
    await page.evaluate(()=>{
      const response={data:{entities:[],entitlementRouting:[],drawers:[]}};
      window.__base.LoginUtil.handleEntities(response);
      window.__base.LoginUtil.handleDrawers(response);
    });
    await expect(page.locator('[data-testid^="consumer-"]')).toHaveCount(0);
    const decisions=await page.evaluate(()=>[window.__auth.hasPermission('feature-a:action-a'),window.__auth.hasPermission('feature-b:action-a')]);
    assert.deepEqual(decisions,[false,false]);return {mountedConsumers:0,permissionResults:decisions};
  });
  await context.close();
} catch(error){run.setupError=error.stack;}
finally{
  await browser?.close();if(server?.listening)await new Promise(resolve=>server.close(resolve));
  run.endedAt=new Date().toISOString();run.status=run.setupError||!run.cases.length||run.cases.some(item=>item.status==='FAILED')?'FAILED':'PASSED';
  await fs.writeFile(path.join(output,'run.json'),JSON.stringify(run,null,2));
}
console.log(JSON.stringify({status:run.status,cases:run.cases,setupError:run.setupError,output},null,2));
if(run.status!=='PASSED')process.exitCode=1;
