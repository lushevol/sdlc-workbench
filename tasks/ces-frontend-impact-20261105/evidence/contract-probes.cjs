const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const cp = require('node:child_process');
const root = path.resolve(__dirname, '../../..');
const ts = require(path.join(root, 'repos/ui/mfe-base/node_modules/typescript/lib/typescript.js'));
const hash = text => crypto.createHash('sha256').update(text).digest('hex');
const paths = {
  common: 'repos/ui/mfe-base/src/utils/common.ts',
  drawer: 'repos/ui/mfe-base/src/utils/drawer.ts',
  launch: 'repos/ui/mfe-base/src/pages/Home/common/util.ts',
  permissions: 'repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts',
};
const texts = Object.fromEntries(Object.entries(paths).map(([key, file]) => [key, fs.readFileSync(path.join(root,file),'utf8')]));
function extract(text, names) {
  const source = ts.createSourceFile('actual.ts', text, ts.ScriptTarget.Latest, true);
  return source.statements.filter(statement => ts.isVariableStatement(statement) && statement.declarationList.declarations.some(d => names.includes(d.name.getText(source)))).map(statement => statement.getText(source)).join('\n');
}
function evaluate(source, globals = {}) {
  const exports = {};
  const context = {exports, ...globals};
  vm.runInNewContext(ts.transpileModule(source, {compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2020}}).outputText, context);
  return exports;
}
const baseSource = extract(texts.drawer,['findTile','findTileConfig']) + '\n' + extract(texts.common,['validateTile','validateWorkspace']) + '\n' + extract(texts.launch,['openTileUtil']);
const base = evaluate(baseSource, {firstWorkspace: () => ({id:'blank-fixture',containers:[]})});
let store;
const container = evaluate(extract(texts.permissions,['X_RATANONE','getUser','hasPermission']), {getHooks:()=>({store})});
const feature = 'RATAN_TRADE_BLOTTER';
const action = 'F_Custom_View_Builder_Private';
const entity = (name, source, actions, subjectName=feature) => ({name,roleName:source === 'EMS2' ? 'PSS_USER' : null,subjects:[{name:subjectName,longName:subjectName,entitlementSource:source,actions:actions.map(name=>({name}))}]});
const results = [];
function save(id, fixture, actual, asserted, limit) {
  if (!asserted) throw new Error('Unexpected probe observation: ' + id);
  const result = {id,captured_at:new Date().toISOString(),fixture,actual,observation_assertion:'PASSED',business_verification:'NOT_ESTABLISHED',limits:limit};
  const resultPath = path.join(__dirname, id+'.json');
  if (fs.existsSync(resultPath)) {
    const prior = JSON.parse(fs.readFileSync(resultPath, 'utf8'));
    if (JSON.stringify(prior.actual) !== JSON.stringify(actual)) throw new Error('Existing result differs: '+id);
    results.push(prior);
  } else {
    fs.writeFileSync(resultPath,JSON.stringify(result,null,2)+'\n');
    results.push(result);
  }
}
const legacyTile = {id:42,container:'@fm/ratan_container',module:'/ratan',tile:'/trade',title:'Trade',entity:['X_RATANONE'],subject:'Legacy Trade Tile',entitlementSource:'EMS2'};
const cesTile = {...legacyTile,entity:['RATAN_ENTITLEMENT_RULE'],entitlementSource:'EMS3'};
const workspace = {id:'saved-trade',containers:[{container:legacyTile.container,module:legacyTile.module,tile:legacyTile.tile}]};
const oldEntities = [entity('X_RATANONE','EMS2',[action],'Legacy Trade Tile')];
const newEntities = [entity('RATAN_ENTITLEMENT_RULE','EMS3',[action])];
const oldValid = base.validateTile(oldEntities,legacyTile.entity,legacyTile.subject);
const newValid = base.validateTile(newEntities,cesTile.entity,cesTile.subject);
const oldRestored = JSON.parse(JSON.stringify(base.validateWorkspace([workspace],oldEntities,[{tiles:[legacyTile]}])));
const newRestored = JSON.parse(JSON.stringify(base.validateWorkspace([workspace],newEntities,[{tiles:[cesTile]}])));
let opened = 0;
base.openTileUtil(false,newValid,()=>opened++,cesTile,'{}');
save('PROBE-01',{oldEntities,newEntities,legacyTile,cesTile,workspace},{oldValid,newValid,oldRestored,newRestored,newDeepLinkOpenCount:opened},oldValid===true && newValid===false && oldRestored[0].id==='saved-trade' && newRestored[0].id==='blank-fixture' && opened===0,['Actual frontend function bodies; synthetic BFF-shaped payloads.','BFF Java, network, React lifecycle, storage and browser were not executed.','firstWorkspace is a deterministic blank fixture; removal is tested, real blank workspace fields are not.']);
store={user:{id:'fixture-user'},entities:[entity('X_RATANONE','EMS2',[action])]};
const oldPermission = container.hasPermission(feature+':'+action);
store={user:{id:'fixture-user'},entities:newEntities};
const cesPermission = container.hasPermission(feature+':'+action);
save('PROBE-02',{feature,action,oldEntity:'X_RATANONE',newEntity:'RATAN_ENTITLEMENT_RULE'},{oldPermission,cesPermission},oldPermission===true && cesPermission===false,['Synthetic equivalent grants; actual container helpers executed.','No live CES mapping or deployed app was tested.']);
store={user:{id:'fixture-user'},entities:[entity('X_RATANONE','EMS2',['DifferentAction']),...newEntities]};
const mixedPermission = container.hasPermission(feature+':'+action);
save('PROBE-03',{feature,action,entities:store.entities},{mixedPermission},mixedPermission===false,['Synthetic mixed response demonstrates legacy early-return masking.','Which provider should authorize each business action requires application scope and reviewed migration policy.']);
store={user:{id:'fixture-user'},entities:[entity('RATAN_ENTITLEMENT_RULE','EMS3',[action]),entity('RATAN_ENTITLEMENT_RULE','EMS2',['DifferentAction'])]};
const flattened = container.getUser();
save('PROBE-04',{feature,action,entities:store.entities},{flattened},!flattened.entitlements.RATAN_ENTITLEMENT_RULE[feature].includes(action),['Synthetic duplicate application name demonstrates last-write overwrite.','Safe resolution must retain provider and application scope; arbitrary union is not validated.']);
const mainCommon = cp.execFileSync('git',['-C',path.join(root,'repos/ui/mfe-base'),'show','main:src/utils/common.ts'],{encoding:'utf8'});
const sameValidationAsMain = extract(mainCommon,['validateTile','validateWorkspace']) === extract(texts.common,['validateTile','validateWorkspace']);
const summary = {started_from:'Read-only current frontend sources',runtime:process.version,typescript:ts.version,source_hashes:Object.fromEntries(Object.entries(paths).map(([key,file])=>[file,hash(texts[key])])),base_functions_same_as_main:sameValidationAsMain,source_comparison:'BFF main 834b4155232222347220e47139a502ee43a9cbdf -> 267081800cc28b6af0f8e080fa67c2d5f14d3a26; payload shapes reconstructed from source, not executed Java',results:results.map(r=>({id:r.id,observation_assertion:r.observation_assertion,business_verification:r.business_verification}))};
fs.writeFileSync(path.join(__dirname,'contract-probe-summary.json'),JSON.stringify(summary,null,2)+'\n');
console.log(JSON.stringify(summary,null,2));
