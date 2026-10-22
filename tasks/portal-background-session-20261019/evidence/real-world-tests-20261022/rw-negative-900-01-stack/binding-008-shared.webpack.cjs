const path = require('path');
const root = path.resolve(__dirname, '../..');
const cached = path.join(root, '.workbench/portal-session-real-20261019/local-mfe/node_modules');
const installed = path.join(__dirname, 'dependencies/node_modules');
const webpack = require(path.join(cached, 'webpack'));
module.exports = function build({repo, name, port}) {
  const source = path.join(root, 'repos/ui', repo, 'src');
  return {
    mode: 'development',
    devtool: 'source-map',
    entry: path.join(source, 'root.tsx'),
    output: {
      path: path.join(__dirname, 'build', name),
      filename: name + '.js',
      chunkFilename: '[contenthash].[name].' + name + '.js',
      publicPath: 'http://127.0.0.1:' + port + '/',
      library: {type: 'system'},
      uniqueName: name,
    },
    resolve: {
      extensions: ['.tsx', '.ts', '.jsx', '.js', '.json'],
      modules: [installed, cached, 'node_modules'],
      alias: {src: source, Import: path.join(source, 'Root/import'), '@Test': path.join(source, 'test')},
      fallback: {net: false},
    },
    resolveLoader: {modules: [cached]},
    externalsType: 'system',
    externals: [({request}, callback) => {
      if (request === 'react' || request === 'react-dom' || request.startsWith('@fm/')) return callback(null, request);
      callback();
    }],
    module: {rules: [
      {test: /\.[jt]sx?$/, exclude: /node_modules/, use: {loader: 'babel-loader', options: {
        babelrc: false, configFile: false,
        presets: [
          [require.resolve(path.join(cached, '@babel/preset-env')), {targets: {chrome: '120'}, modules: false}],
          [require.resolve(path.join(cached, '@babel/preset-react')), {runtime: 'automatic'}],
          require.resolve(path.join(cached, '@babel/preset-typescript')),
        ],
      }}},
      {test: /\.css$/, use: ['style-loader', 'css-loader']},
      {test: /\.less$/, use: ['style-loader', 'css-loader', {loader: 'less-loader', options: {lessOptions: {javascriptEnabled: true}}}]},
      {test: /\.(png|jpe?g|gif|svg|ico|woff2?|eot|ttf|otf|xlsx|pdf)$/, type: 'asset/resource'},
    ]},
    plugins: [new webpack.DefinePlugin({
      'process.env.MFE_APP_PREFIX_STYLE': JSON.stringify('ratan'),
      'process.env.orgName': JSON.stringify('fm'),
    })],
    optimization: {minimize: false},
    devServer: {
      host: '127.0.0.1', port, allowedHosts: 'all', hot: false, liveReload: false, client: false,
      headers: {'Access-Control-Allow-Origin': '*'},
      devMiddleware: {writeToDisk: false}, static: false,
    },
    stats: {preset: 'errors-warnings', errorDetails: true},
  };
};
