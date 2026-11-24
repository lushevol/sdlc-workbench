const path = require('path');
const webpack = require("/var/folders/3q/zc3tlwsj1p1_pskzk1j9r5100000gn/T/comprehensive-renewal-9jgsnhhq/source/node_modules/webpack");
const sourceConfig = require("/var/folders/3q/zc3tlwsj1p1_pskzk1j9r5100000gn/T/comprehensive-renewal-9jgsnhhq/source/webpack.config.js");

module.exports = (env, argv) => {
  const config = sourceConfig(env, argv);
  config.context = "/var/folders/3q/zc3tlwsj1p1_pskzk1j9r5100000gn/T/comprehensive-renewal-9jgsnhhq/source";
  config.resolve = { ...config.resolve, alias: { ...config.resolve?.alias, '@sctoolkit/webkit': "/Users/lushevol/code/github/ratan-release-impact/workbench/.workbench/portal-session-real-20261019/local-mfe/toolkit-mock" } };
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
    port: 8242,
    allowedHosts: ['localhost', '127.0.0.1'],
    hot: false,
    liveReload: false,
    client: false,
    open: false,
  };
  return config;
};
