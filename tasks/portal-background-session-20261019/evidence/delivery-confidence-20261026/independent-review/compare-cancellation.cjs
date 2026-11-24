const fs = require('fs');
const cp = require('child_process');
const path = require('path');
const crypto = require('crypto');
const vm = require('vm');

const repo = path.resolve(__dirname, '../../../../..', 'repos/ui/mfe-base');
const babel = require(require.resolve('@babel/core', { paths: [repo] }));
const sourcePath = 'src/hooks/service/util/error.response.handler.ts';
const refs = ['f025513f696476a9cc8162681410cbd21e029bcb', 'c42e7609c4e14eb53de32702e4bd3424a223988a'];

(async () => {
  const results = [];
  for (const ref of refs) {
    const source = cp.execFileSync('git', ['show', `${ref}:${sourcePath}`], { cwd: repo });
    const state = { isLoading: true, errorMsg: undefined };
    const dispatches = [];
    const exports = {};
    const code = babel.transformSync(source.toString(), {
      filename: sourcePath,
      babelrc: false,
      configFile: false,
      presets: [require.resolve('@babel/preset-typescript', { paths: [repo] })],
      plugins: [require.resolve('@babel/plugin-transform-modules-commonjs', { paths: [repo] })],
    }).code;
    const getHooksBase = () => ({ baseDispatch: (action) => {
      dispatches.push(action);
      Object.assign(state, action.data);
    }});
    const dependency = (id) => {
      if (id.endsWith('/HooksBase')) return { getHooksBase };
      if (id.endsWith('/ActionType')) return { ActionType: { SET_ERRORMSG: 'SET_ERRORMSG', SET_IS_LOADING: 'SET_IS_LOADING' }};
      if (id.endsWith('/common')) return { clearStorageWhenLogout() { throw new Error('Unexpected logout'); }};
      if (id.endsWith('/sessionEpoch')) return { isStaleSessionRequest: () => false };
      throw new Error(`Unexpected dependency: ${id}`);
    };
    vm.runInNewContext(code, { exports, require: dependency, console, Promise });
    const controller = new AbortController();
    controller.abort();
    let rejected;
    try {
      await exports.errorHandler({ code: 'ERR_CANCELED', message: 'canceled', config: { url: '/api/auth/v1/fmo/admin/category/data', signal: controller.signal, sessionEpoch: 1 } });
    } catch (error) { rejected = error.code; }
    results.push({ ref, sourcePath, sourceSha256: crypto.createHash('sha256').update(source).digest('hex'), fixture: 'Current-session final cancellation; no replacement or later response.', expected: { isLoading: false, errorMsg: undefined, rejectionCode: 'ERR_CANCELED' }, actual: { ...state, rejectionCode: rejected }, dispatches, status: state.isLoading === false && rejected === 'ERR_CANCELED' ? 'PASSED' : 'FAILED' });
    fs.writeFileSync(path.join(__dirname, `cancellation-${ref.slice(0,7)}.json`), JSON.stringify(results.at(-1), null, 2) + '\n');
  }
  fs.writeFileSync(path.join(__dirname, 'cancellation-comparison.json'), JSON.stringify({ caseId: 'DEL-14', boundaries: 'Exact handler source transpiled with Babel; HooksBase dispatcher, enum, logout, and session-current check stubbed. No browser or Axios transport execution.', results }, null, 2) + '\n');
  process.stdout.write(JSON.stringify(results.map(({ref,status,actual}) => ({ref,status,actual}))) + '\n');
})().catch((error) => { process.stderr.write(error.stack + '\n'); process.exitCode = 1; });
