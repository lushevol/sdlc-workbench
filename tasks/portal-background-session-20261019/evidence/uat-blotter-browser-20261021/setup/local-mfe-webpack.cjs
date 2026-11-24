const path = require('path');
const webpack = require('webpack');
const sourceConfig = require("/Users/lushevol/code/github/ratan-release-impact/workbench/.workbench/session-minor-rerun-20261020/mfe/source/webpack.config.js");

module.exports = (env, argv) => {
  const config = sourceConfig(env, argv);
  config.context = "/Users/lushevol/code/github/ratan-release-impact/workbench/.workbench/session-minor-rerun-20261020/mfe/source";
  config.output.path = path.join(__dirname, 'build');
  config.plugins = config.plugins.filter((plugin) =>
    !['ModuleFederationPlugin', 'Dotenv', 'ForkTsCheckerWebpackPlugin'].includes(plugin.constructor.name));
  config.plugins.push(new webpack.container.ModuleFederationPlugin({
    name: 'baseContainer',
    remotes: {},
    shared: { react: { singleton: true }, 'react-dom': { singleton: true } },
  }));
  config.plugins.push(new webpack.DefinePlugin({
    'process.env.MFE_APP_PREFIX_STYLE': JSON.stringify('MicroWebUI_base'),
    'process.env.orgName': JSON.stringify('fm'),
  }));
  config.devServer = {
    ...config.devServer,
    host: '127.0.0.1',
    port: 8122,
    allowedHosts: ['localhost', '127.0.0.1'],
    hot: false,
    liveReload: false,
    client: false,
    open: false,
  };
  return config;
};
