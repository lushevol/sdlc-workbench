const path = require('path');
const baseline = require('../local-mfe/mfe.local.webpack.cjs');
module.exports = (env, argv) => {
  const config = baseline(env, argv);
  config.output.path = path.join(__dirname, 'build');
  config.entry = [path.join(__dirname, 'evidence-runtime.js'), config.entry];
  config.module.rules.unshift({
    test: /\.[tj]sx?$/,
    include: path.resolve(__dirname, '../local-mfe/source/src'),
    enforce: 'pre',
    loader: path.join(__dirname, 'evidence-loader.cjs'),
  });
  return config;
};
