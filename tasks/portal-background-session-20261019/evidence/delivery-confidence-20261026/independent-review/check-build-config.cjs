const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const repo = path.resolve(__dirname, '../../../../..', 'repos/ui/mfe-base');
const resolve = (name) => require.resolve(name, { paths: [repo] });
const { getEnvFileVars } = require(resolve('env-cmd/dist/parse-env-file'));

(async () => {
  const records = [];
  for (const file of ['.env.server', '.env.cloud', '.env.local', '.env.mfe']) {
    const filename = path.join(repo, file);
    const bytes = fs.readFileSync(filename);
    const vars = await getEnvFileVars(filename);
    const record = {
      file,
      sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
      keys: Object.keys(vars),
      hasSessionLifetimeKey: Object.keys(vars).some((key) => /token.*(life|expir)|refresh.*(life|expir)|session.*(life|expir)/i.test(key)),
    };
    if (file === '.env.server') {
      Object.assign(process.env, vars);
      const config = require(path.join(repo, 'webpack.config.js'))({}, { mode: 'production' });
      const publicPath = new URL(config.output.publicPath);
      record.effectiveWebpack = {
        mode: config.mode,
        devtool: config.devtool,
        publicPathIsLoopback: publicPath.hostname === 'localhost',
        publicPathUsesHttp: publicPath.protocol === 'http:',
        portMatchesServerFile: publicPath.port === vars.port,
        remoteConfigured: typeof vars.cduplatform === 'string',
        remotePointsAtDevelopmentHost: /-dev\./.test(vars.cduplatform),
      };
    }
    if (Object.hasOwn(vars, 'FILE_LIMIT')) {
      const parser = require(resolve('bytes'));
      record.bodyLimit = {
        effectiveBytes: parser.parse(vars.FILE_LIMIT),
        sourceFallbackBytes: parser.parse('1mb'),
      };
    }
    if (file === '.env.cloud') {
      record.runtimeServer = {
        portMatchesContainerPort8080: vars.PORT === '8080',
        timeoutMatchesSourceFallback30000: vars.DEFAULT_TIMEOUT === '30000',
        webpackOnlyKeysNotReadByServer: ['orgName', 'mode', 'devtool', 'cduplatform'].filter((key) => Object.hasOwn(vars, key)),
      };
    }
    records.push(record);
  }
  const result = {
    status: 'COMPLETED_CONFIG_EVALUATION',
    records,
    limits: [
      'Evaluated repository configuration and installed parser behavior; no build, deployment, or external network request occurred.',
      'The source-only pipeline extends an external nodejs-mfe.yml template. Its configuration rewriting and artifact selection remain unavailable.',
      'Main has no tracked environment files, so its actual CI environment values remain unknown.',
      'The selected remote is declared by webpack. No cduplatform import was found in the application source.',
      'The Express server exposes static assets and health GET routes. No supported JSON-body business route was found.',
      'Parser behavior uses locally installed bytes; the immutable container dependency version is unbound.',
    ],
  };
  fs.writeFileSync(path.join(__dirname, 'build-config-effects.json'), JSON.stringify(result, null, 2) + '\n');
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
})().catch((error) => { process.stderr.write(error.stack + '\n'); process.exitCode = 1; });
