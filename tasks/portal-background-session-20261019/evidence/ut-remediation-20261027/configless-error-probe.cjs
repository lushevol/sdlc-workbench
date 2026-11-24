const fs = require('fs');
const path = require('path');
const root = fs.realpathSync(process.argv[2]);
const dependencyRoot = '/tmp/mfe-ut-remediation-20261027-qposcs1f';
const babel = require(path.join(dependencyRoot, 'node_modules/@babel/core'));
const { JSDOM } = require(path.join(dependencyRoot, 'node_modules/jsdom'));
const dom = new JSDOM('', { url: 'http://localhost/' });
global.window = dom.window;
global.document = dom.window.document;
global.localStorage = dom.window.localStorage;
global.sessionStorage = dom.window.sessionStorage;
for (const extension of ['.ts', '.tsx']) {
  require.extensions[extension] = (module, filename) => {
    const code = babel.transformSync(fs.readFileSync(filename, 'utf8'), {
      filename, cwd: dependencyRoot, envName: 'test',
      plugins: [require(path.join(dependencyRoot, 'node_modules/@babel/plugin-transform-modules-commonjs'))]
    }).code;
    module._compile(code, filename);
  };
}
const hooks = require(path.join(root, 'src/hooks/HooksBase.ts')).getHooksBase();
const reducer0 = require(path.join(root, 'src/hooks/reducer/root0.reducers.ts')).default;
const reducer = require(path.join(root, 'src/hooks/reducer/root.reducers.ts')).default;
const service = require(path.join(root, 'src/hooks/service/config.ts')).default;
hooks.setStore({ token: 'session-a', workspaces: [] });
hooks.setBaseDispatch(action => hooks.setStore(reducer(reducer0(hooks.store, action), action)));
let adapterCalls = 0;
service.defaults.adapter = async config => {
  adapterCalls += 1;
  return { config, data: '{}', headers: {}, status: 200, statusText: 'OK' };
};
(async () => {
  const events = [];
  const originalDispatch = hooks.baseDispatch;
  hooks.setBaseDispatch(action => {
    events.push({type: action.type, loading: action.data?.isLoading});
    originalDispatch(action);
  });
  let rejection;
  try {
    await service.get('/api/portfolio/positions', {
      transformResponse: [() => { throw new Error('Invalid positions payload'); }]
    });
  } catch (error) {
    rejection = { message: error.message ?? null, code: error.code ?? null, configPresent: !!error.config };
  }
  const afterError = hooks.store.isLoading;
  await service.get('/api/portfolio/positions?request=next');
  const afterNextRequest = hooks.store.isLoading;
  process.stdout.write(JSON.stringify({root, adapterCalls, rejection, afterError, afterNextRequest, events}, null, 2) + '\n');
})().catch(error => { process.stderr.write(error.stack); process.exitCode = 1; });
