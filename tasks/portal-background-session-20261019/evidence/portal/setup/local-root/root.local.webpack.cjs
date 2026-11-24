const path = require('path');
const repo = path.resolve(__dirname, '../../../repos/ui/mfe-root-config');
const sourceConfig = require(path.join(repo, 'webpack.config.js'));

module.exports = (env, argv) => {
  const config = sourceConfig(env, argv);
  config.output.path = path.join(__dirname, 'build');
  config.devServer = {
    ...config.devServer,
    host: '127.0.0.1',
    port: 8001,
    allowedHosts: ['localhost', '127.0.0.1'],
    open: false,
    hot: false,
    liveReload: false,
    client: false,
    static: { directory: path.join(repo, 'public') },
    proxy: [{ context: ['/api/'], target: 'http://127.0.0.1:8088', changeOrigin: true }],
    setupMiddlewares(middlewares, server) {
      server.app.get('/background-control.html', (_req, res) => {
        res.type('html').send('<!doctype html><html><head><title>Local background control</title></head><body><h1>Local background control</h1><p>This separate Edge tab is for the portal session observation.</p><p>This page has no scripts, timers, or network requests.</p></body></html>');
      });
      return middlewares;
    },
  };
  return config;
};
