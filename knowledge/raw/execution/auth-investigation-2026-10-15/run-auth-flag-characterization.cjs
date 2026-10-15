const fs = require('node:fs');
const vm = require('node:vm');
const { stripTypeScriptTypes } = require('node:module');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
(async () => {
  const sourcePath = process.argv[2];
  const flagsPath = process.argv[3];
  const outputPath = process.argv[4];
  const source = fs.readFileSync(sourcePath, 'utf8');
  const flags = JSON.parse(fs.readFileSync(flagsPath, 'utf8'));
  let environment = 'local';
  const context = vm.createContext({ window: { location: { search: '' } }, URLSearchParams });
  const module = new vm.SourceTextModule(stripTypeScriptTypes(source, {mode: 'transform'}), {context, identifier: sourcePath});
  await module.link(async specifier => {
    if (specifier === './common') return new vm.SyntheticModule(['getEnv'], function () { this.setExport('getEnv', () => environment); }, {context});
    if (specifier === './feature-flags.json') return new vm.SyntheticModule(['default'], function () { this.setExport('default', flags); }, {context});
    throw new Error('Unexpected import: ' + specifier);
  });
  await module.evaluate();
  const results = [];
  const configured = { ENABLE_ENTRA_SSO: {local: false, dev: false, uat: false, 'pre-prod': false, prod: false} };
  const evaluate = module.namespace.featureScopedEnabledFactor(configured);
  for (const [value, expected] of [['true',true],['TRUE',true],['yes',true],['YeS',true],['1',true],['y',true],['false',false],['no',false],['0',false],['n',false],['unexpected',false],['',false]]) {
    context.window.location.search = '?ENABLE_ENTRA_SSO=' + value;
    const actual = evaluate('ENABLE_ENTRA_SSO');
    assert.equal(actual, expected);
    results.push({condition: 'declared flag query value', value, expected, actual, status:'PASSED'});
  }
  context.window.location.search = '';
  for (const value of ['local','dev','uat','pre-prod','prod']) {
    environment = value;
    const actual = module.namespace.featureScopedEnabled('ENABLE_ENTRA_SSO');
    assert.equal(actual, true);
    results.push({condition:'committed flag configuration', environment:value, expected:true, actual, status:'PASSED'});
  }
  environment = 'SIT';
  assert.equal(module.namespace.featureScopedEnabled('ENABLE_ENTRA_SSO'), false);
  results.push({condition:'environment outside declared flag environment set',environment:'SIT',expected:false,actual:false,status:'PASSED'});
  context.window.location.search = '?MISSING_FLAG=true';
  assert.equal(module.namespace.featureScopedEnabled('MISSING_FLAG'), false);
  results.push({condition:'undeclared flag query',expected:false,actual:false,status:'PASSED'});
  const report = {status:'PASSED',sourcePath,sourceSha256:crypto.createHash('sha256').update(source).digest('hex'),flagsPath,flagsSha256:crypto.createHash('sha256').update(fs.readFileSync(flagsPath)).digest('hex'),cases:results,limits:['This harness executes the actual parser after Node TypeScript transformation.','The getEnv import and browser location are controlled test inputs.','This is not Jest, an end-to-end login, or a deployed-browser observation.']};
  fs.writeFileSync(outputPath,JSON.stringify(report,null,2)+'\n');
  process.stdout.write(JSON.stringify({status:report.status,cases:results.length,output:outputPath})+'\n');
})().catch(error => { process.stderr.write(error.stack+'\n'); process.exitCode=1; });
