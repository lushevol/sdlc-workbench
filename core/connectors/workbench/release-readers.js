import axios from 'axios';
import { createHash } from 'node:crypto';
import { createWriteStream, existsSync, lstatSync, readFileSync, realpathSync, unlinkSync } from 'node:fs';
import http from 'node:http';
import https from 'node:https';
import { checkServerIdentity, rootCertificates } from 'node:tls';
import { basename, dirname, isAbsolute, relative, resolve, sep } from 'node:path';
import { pipeline } from 'node:stream/promises';
import { Transform } from 'node:stream';
import { HttpsProxyAgent } from 'https-proxy-agent';
import { z } from 'zod';
import { detectProxyFor } from '../packages/core/src/proxy.js';

const text = z.string().min(1).max(8192);
const identifier = z.number().int().positive();
const page = z.number().int().min(0).max(10000000).optional();
const selectors = { branch: text.optional(), pullRequest: text.optional() };
const project = { project: text };
const build = { ...project, buildId: identifier };
const repo = { ...project, repository: text };
const enc = value => encodeURIComponent(String(value));
const qp = (path, values) => {
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(values)) {
    if (value !== undefined && value !== null && value !== '') query.set(key, String(value));
  }
  return `${path}?${query}`;
};
const ado = (path, values = {}) => qp(path, { ...values, 'api-version': '7.1' });
const repoPath = a => `${enc(a.project)}/_apis/git/repositories/${enc(a.repository)}`;
const buildPath = a => `${enc(a.project)}/_apis/build/builds/${a.buildId}`;
const sonarSelectors = a => ({ branch: a.branch, pullRequest: a.pullRequest });
const transientNetworkErrors = new Set([
  'ECONNRESET', 'ECONNREFUSED', 'EPIPE', 'ETIMEDOUT', 'ECONNABORTED',
  'ERR_NETWORK', 'ERR_CANCELED', 'EAI_AGAIN',
]);

/** Shared raw readers. The report collector and native MCP use the same definitions. */
export const REPORT_READERS = Object.freeze({
  report_work_items: {
    connector: 'ado', description: 'Read at most 200 complete work items with expanded relations.',
    shape: { ids: z.array(identifier).min(1).max(200), project: text.optional(), asOf: text.optional() },
    request: a => ({ method: 'POST', path: ado(`${a.project ? `${enc(a.project)}/` : ''}_apis/wit/workitemsbatch`),
      data: { ids: a.ids, $expand: 'All', ...(a.asOf ? { asOf: a.asOf } : {}) } }),
  },
  report_builds: {
    connector: 'ado', description: 'Read identified builds without projecting raw fields.',
    shape: { ...project, ids: z.array(identifier).min(1).max(200) },
    request: a => ({ path: ado(`${enc(a.project)}/_apis/build/builds`, { buildIds: a.ids.join(','), $top: a.ids.length }) }),
  },
  report_build_timeline: {
    connector: 'ado', description: 'Read the complete timeline for an identified build.', shape: build,
    request: a => ({ path: ado(`${buildPath(a)}/timeline`) }),
  },
  report_build_artifacts: {
    connector: 'ado', description: 'Read build artifact metadata and original links.', shape: build,
    request: a => ({ path: ado(`${buildPath(a)}/artifacts`) }),
  },
  report_build_logs: {
    connector: 'ado', description: 'Read log metadata without downloading every log.', shape: build,
    request: a => ({ path: ado(`${buildPath(a)}/logs`) }),
  },
  report_build_properties: {
    connector: 'ado', description: 'Read build properties, including published analysis identities.', shape: build,
    request: a => ({ path: ado(`${buildPath(a)}/properties`) }),
  },
  report_attachment: {
    connector: 'ado', description: 'Read a named build timeline attachment.',
    shape: { ...build, timelineId: text, recordId: text, type: text, name: text },
    request: a => ({ path: ado(`${buildPath(a)}/${enc(a.timelineId)}/${enc(a.recordId)}/attachments/${enc(a.type)}/${enc(a.name)}`) }),
  },
  report_coverage: {
    connector: 'ado', description: 'Read code coverage for an identified build.', shape: build,
    request: a => ({ path: ado(`${enc(a.project)}/_apis/test/codecoverage`, { buildId: a.buildId, flags: 7 }) }),
  },
  report_deployments: {
    connector: 'ado', description: 'Read pipeline run stage evidence through the supplied source contribution query.',
    shape: { ...project, pipelineId: identifier, keyword: text.optional(), continuationToken: text.optional() },
    request: a => ({ method: 'POST', path: qp(`_apis/Contribution/HierarchyQuery/project/${enc(a.project)}`, { 'api-version': '5.0-preview.1' }),
      data: { contributionIds: ['ms.vss-build-web.runs-data-provider'], dataProviderContext: { properties: {
        definitionId: String(a.pipelineId), ...(a.keyword ? { keywordFilter: a.keyword } : {}),
        ...(a.continuationToken ? { continuationToken: a.continuationToken } : {}),
        sourcePage: { routeId: 'ms.vss-build-web.pipeline-details-route', routeValues: {
          project: a.project, viewname: 'details', controller: 'ContributedPage', action: 'Execute',
        } },
      } } } }),
  },
  report_branches: {
    connector: 'ado', description: 'Read branch refs in one identified repository.',
    shape: { ...repo, filter: text.optional(), continuationToken: text.optional() },
    request: a => ({ path: ado(`${repoPath(a)}/refs`, { filter: a.filter ? `heads/${a.filter.replace(/^refs\/heads\//, '')}` : 'heads/',
      continuationToken: a.continuationToken, $top: 1000 }) }),
  },
  report_compare: {
    connector: 'ado', description: 'Compare exact commits with explicit base and target identities.',
    shape: { ...repo, base: text, target: text, common: z.boolean().optional(), skip: page, top: z.number().int().min(1).max(1000).optional() },
    request: a => ({ path: ado(`${repoPath(a)}/diffs/commits`, { baseVersion: a.base, baseVersionType: 'commit',
      targetVersion: a.target, targetVersionType: 'commit', diffCommonCommit: a.common || false, $skip: a.skip || 0, $top: a.top || 100 }) }),
  },
  report_commits: {
    connector: 'ado', description: 'Read commits between exact versions with linked work item identities.',
    shape: { ...repo, base: text, target: text, skip: page, top: z.number().int().min(1).max(1000).optional() },
    request: a => ({ path: ado(`${repoPath(a)}/commits`, {
      'searchCriteria.itemVersion.version': a.base, 'searchCriteria.itemVersion.versionType': 'commit',
      'searchCriteria.compareVersion.version': a.target, 'searchCriteria.compareVersion.versionType': 'commit',
      'searchCriteria.includeWorkItems': true, '$skip': a.skip || 0, '$top': a.top || 100,
    }) }),
  },
  report_commit_changes: {
    connector: 'ado', description: 'Read changed file metadata for an exact commit.',
    shape: { ...repo, commit: text, skip: page, top: z.number().int().min(1).max(1000).optional() },
    request: a => ({ path: ado(`${repoPath(a)}/commits/${enc(a.commit)}/changes`, { skip: a.skip || 0, top: a.top || 100 }) }),
  },
  report_file: {
    connector: 'ado', description: 'Read exact commit file content with source identity.',
    shape: { ...repo, path: text, commit: text },
    request: a => ({ path: ado(`${repoPath(a)}/items`, { path: a.path,
      'versionDescriptor.version': a.commit, 'versionDescriptor.versionType': 'commit', includeContent: true }) }),
  },
  report_sonar_measures: {
    connector: 'sonar', description: 'Read raw Sonar measures for an explicit component and selector.',
    shape: { component: text, ...selectors, metricKeys: text.optional() },
    request: a => ({ path: qp('api/measures/component', { component: a.component, ...sonarSelectors(a),
      metricKeys: a.metricKeys || 'coverage,line_coverage,branch_coverage,new_coverage,bugs,vulnerabilities,code_smells,duplicated_lines_density,ncloc,alert_status' }) }),
  },
  report_sonar_gate: {
    connector: 'sonar', description: 'Read raw Sonar quality gate data without a release verdict.',
    shape: { component: text, ...selectors },
    request: a => ({ path: qp('api/qualitygates/project_status', { projectKey: a.component, ...sonarSelectors(a) }) }),
  },
  report_sonar_issues: {
    connector: 'sonar', description: 'Read a complete unprojected issue page with explicit paging.',
    shape: { component: text, ...selectors, page: z.number().int().min(1).optional(), pageSize: z.number().int().min(1).max(500).optional() },
    request: a => ({ path: qp('api/issues/search', { componentKeys: a.component, ...sonarSelectors(a), p: a.page || 1, ps: a.pageSize || 100 }) }),
  },
  report_sonar_hotspots: {
    connector: 'sonar', description: 'Read a complete unprojected hotspot page with explicit paging.',
    shape: { component: text, ...selectors, page: z.number().int().min(1).optional(), pageSize: z.number().int().min(1).max(500).optional() },
    request: a => ({ path: qp('api/hotspots/search', { projectKey: a.component, ...sonarSelectors(a), p: a.page || 1, ps: a.pageSize || 100 }) }),
  },
  report_sonar_analyses: {
    connector: 'sonar', description: 'Read Sonar analysis identity and revision pages.',
    shape: { component: text, branch: text.optional(), page: z.number().int().min(1).optional(), pageSize: z.number().int().min(1).max(500).optional() },
    request: a => ({ path: qp('api/project_analyses/search', { project: a.component, branch: a.branch, p: a.page || 1, ps: a.pageSize || 100 }) }),
  },
});

export function validateReportArguments(connector, tool, args) {
  const definition = REPORT_READERS[tool];
  if (!definition || definition.connector !== connector) throw Object.assign(new Error('Unsupported report tool.'), { code: 'UNKNOWN_TOOL' });
  const values = z.object(definition.shape).strict().parse(args || {});
  if (values.branch && values.pullRequest) throw Object.assign(new Error('Choose one selector.'), { code: 'INVALID_ARGUMENT' });
  return { definition, values };
}

function inside(root, path) {
  const diff = relative(root, path);
  return diff !== '' && diff !== '..' && !diff.startsWith(`..${sep}`) && !isAbsolute(diff);
}

export function confinedEvidencePath(runDir, path) {
  if (!isAbsolute(path)) throw Object.assign(new Error('Invalid evidence destination.'), { code: 'INVALID_PATH' });
  const destination = resolve(realpathSync(dirname(path)), basename(path));
  if (!inside(runDir, destination)) throw Object.assign(new Error('Invalid evidence destination.'), { code: 'INVALID_PATH' });
  if (existsSync(destination) || (() => { try { return lstatSync(destination).isSymbolicLink(); } catch { return false; } })()) {
    throw Object.assign(new Error('The evidence destination already exists.'), { code: 'INVALID_PATH' });
  }
  return destination;
}

function retryDelay(value) {
  if (!value) return 0;
  const numeric = Number(value);
  return Number.isFinite(numeric) ? Math.max(0, numeric * 1000) : Math.max(0, Date.parse(value) - Date.now() || 0);
}

class ConfiguredProxyAgent extends HttpsProxyAgent {
  constructor(proxy, trust) {
    super(proxy, { keepAlive: true, ...trust });
    this.trust = trust;
  }

  connect(request, options) {
    return super.connect(request, { ...options, ...this.trust,
      ...(options.secureEndpoint ? {
        checkServerIdentity: (_hostname, certificate) => checkServerIdentity(options.host, certificate),
      } : {}) });
  }
}

export class ReportReader {
  constructor(connector, config, options = {}) {
    this.connector = connector;
    this.config = config;
    this.limit = options.concurrency || (connector === 'ado' ? 6 : 2);
    this.timeoutMs = (options.request_timeout_seconds || 30) * 1000;
    this.end = performance.now() + (options.deadline_seconds || 300) * 1000;
    this.queue = [];
    this.active = 0;
    this.pauseUntil = 0;
    this.controllers = new Set();
    this.closed = false;
    this.timer = undefined;
    this.metrics = { requests: 0, retries: 0, peak_concurrency: 0, bytes: 0, sessions: 1,
      client_creations: 1, throttle_wait_ms: 0, concurrency_reductions: 0, calls: 0 };
    this.base = (connector === 'ado' ? config.AZURE_DEVOPS_ORG_URL : config.sonarConfig.baseUrl).replace(/\/+$/, '');
    const parsed = new URL(this.base);
    if (!['http:', 'https:'].includes(parsed.protocol) || parsed.username || parsed.password || parsed.search || parsed.hash) throw new Error('Invalid endpoint.');
    const token = connector === 'ado' ? config.AZURE_DEVOPS_PAT : config.sonarConfig.token;
    if (!token) throw new Error('Missing connector token.');
    this.httpAgent = new http.Agent({ keepAlive: true, maxSockets: this.limit });
    const extraCertificate = config.env?.NODE_EXTRA_CA_CERTS;
    const trust = extraCertificate ? { ca: [...rootCertificates, readFileSync(extraCertificate, 'utf8')] } : {};
    this.httpsAgent = new https.Agent({ keepAlive: true, maxSockets: this.limit,
      ...trust });
    this.client = axios.create({ headers: { Authorization: connector === 'ado' ?
      `Basic ${Buffer.from(`:${token}`).toString('base64')}` : `Bearer ${token}`, Accept: 'application/json' },
      httpAgent: this.httpAgent, httpsAgent: this.httpsAgent, proxy: false, maxRedirects: 0,
      validateStatus: () => true, responseType: 'stream' });
    this.proxyReady = detectProxyFor(this.base, config.HTTPS_PROXY).then(proxy => {
      if (proxy) {
        this.proxyAgent = new ConfiguredProxyAgent(proxy, trust);
        this.client.defaults.httpAgent = this.proxyAgent;
        this.client.defaults.httpsAgent = this.proxyAgent;
      }
    });
  }

  _pump() {
    clearTimeout(this.timer);
    if (this.closed) {
      for (const item of this.queue.splice(0)) item.reject(Object.assign(new Error('Session closed.'), { code: 'CANCELLED' }));
      return;
    }
    const remaining = this.end - performance.now();
    if (remaining <= 0) {
      for (const item of this.queue.splice(0)) item.reject(Object.assign(new Error('Collection deadline expired.'), { code: 'DEADLINE_EXCEEDED' }));
      return;
    }
    const pause = this.pauseUntil - performance.now();
    if (pause > 0) {
      this.timer = setTimeout(() => this._pump(), Math.min(pause, remaining));
      return;
    }
    while (this.active < this.limit && this.queue.length) {
      const item = this.queue.shift();
      this.active++;
      this.metrics.peak_concurrency = Math.max(this.metrics.peak_concurrency, this.active);
      item.resolve(() => { this.active--; this._pump(); });
    }
  }

  _acquire() {
    return new Promise((resolveSlot, reject) => { this.queue.push({ resolve: resolveSlot, reject }); this._pump(); });
  }

  async read(tool, args, evidencePath) {
    const { definition, values } = validateReportArguments(this.connector, tool, args);
    const spec = definition.request(values);
    await this.proxyReady;
    this.metrics.calls++;
    for (let attempt = 0; attempt < 4; attempt++) {
      const release = await this._acquire();
      const controller = new AbortController();
      this.controllers.add(controller);
      const remaining = this.end - performance.now();
      const timer = setTimeout(() => controller.abort(), Math.max(1, Math.min(this.timeoutMs, remaining)));
      this.metrics.requests++;
      let response;
      let createdEvidence = false;
      try {
        response = await this.client.request({ method: spec.method || 'GET', url: `${this.base}/${spec.path}`, data: spec.data,
          signal: controller.signal, timeout: Math.max(1, Math.min(this.timeoutMs, remaining)) });
        const wait = retryDelay(response.headers['retry-after']);
        if (wait) {
          this.pauseUntil = Math.max(this.pauseUntil, performance.now() + wait);
          this.metrics.throttle_wait_ms += wait;
        }
        if ((wait || response.status === 429) && this.limit > 1) {
          this.limit = Math.max(1, Math.floor(this.limit / 2));
          this.metrics.concurrency_reductions++;
        }
        if ([408, 429, 502, 503, 504].includes(response.status) && attempt < 3) {
          response.data.destroy();
          this.metrics.retries++;
          const backoff = wait || Math.min(5000, 200 * (2 ** attempt)) + Math.random() * 100;
          this.pauseUntil = Math.max(this.pauseUntil, performance.now() + backoff);
          continue;
        }
        const hash = createHash('sha256');
        let bytes = 0;
        let inline = [];
        const counter = new Transform({ transform(chunk, encoding, callback) {
          bytes += chunk.length;
          hash.update(chunk);
          callback(null, chunk);
        } });
        if (evidencePath) {
          const output = createWriteStream(evidencePath, { flags: 'wx', mode: 0o600 });
          output.on('open', () => { createdEvidence = true; });
          await pipeline(response.data, counter, output);
        } else {
          for await (const chunk of response.data) {
            bytes += chunk.length;
            if (bytes > 4 * 1024 * 1024) throw Object.assign(new Error('Response exceeds inline limit.'), { code: 'RESPONSE_TOO_LARGE' });
            hash.update(chunk);inline.push(chunk);
          }
        }
        this.metrics.bytes += bytes;
        const headers = {};
        for (const name of ['x-ms-continuationtoken', 'x-ms-continuation-token', 'retry-after', 'content-type', 'etag', 'last-modified']) {
          if (response.headers[name]) headers[name] = String(response.headers[name]);
        }
        const output = { status: response.status >= 200 && response.status < 300 ? 'SUCCEEDED' : 'ERROR', http_status: response.status, headers,
          metrics: { ...this.metrics } };
        if (output.status === 'ERROR') { output.code = `HTTP_${response.status}`;output.message = 'The remote read failed.'; }
        if (evidencePath) output.artifact = { path: evidencePath, sha256: hash.digest('hex'), bytes,
          content_type: response.headers['content-type'] || 'application/octet-stream' };
        else {
          const raw = Buffer.concat(inline).toString('utf8');
          try { output.data = JSON.parse(raw); } catch { output.data = raw; }
        }
        return output;
      } catch (error) {
        response?.data?.destroy();
        if (createdEvidence && evidencePath && existsSync(evidencePath)) { try { unlinkSync(evidencePath); } catch {} }
        if (performance.now() >= this.end) throw Object.assign(new Error('Collection deadline expired.'), { code: 'DEADLINE_EXCEEDED' });
        if (this.closed) throw Object.assign(new Error('Session closed.'), { code: 'CANCELLED' });
        if (attempt < 3 && transientNetworkErrors.has(error.code)) {
          this.metrics.retries++;
          this.pauseUntil = Math.max(this.pauseUntil, performance.now() + Math.min(5000, 200 * (2 ** attempt)) + Math.random() * 100);
          continue;
        }
        throw Object.assign(new Error('The connector read failed.'), { code: error.code === 'RESPONSE_TOO_LARGE' ? error.code : 'REQUEST_FAILED' });
      } finally {
        clearTimeout(timer);this.controllers.delete(controller);release();
      }
    }
  }

  close() {
    this.closed = true;clearTimeout(this.timer);
    for (const controller of this.controllers) controller.abort();
    this._pump();this.httpAgent.destroy();this.httpsAgent.destroy();this.proxyAgent?.destroy();
  }
}

/** Existing discovery and exact-grant calls can use these same raw read definitions. */
export function configureReportReadTools(server, connector, config) {
  for (const [name, definition] of Object.entries(REPORT_READERS)) {
    if (definition.connector !== connector) continue;
    server.tool(name, definition.description, definition.shape, async args => {
      let reader;
      try {
        reader = new ReportReader(connector, config);
        const result = await reader.read(name, args);
        if (result.status !== 'SUCCEEDED') return { isError: true, content: [{ type: 'text', text: result.message }] };
        const payload = { structuredContent: { data: result.data, headers: result.headers, http_status: result.http_status },
          content: [{ type: 'text', text: JSON.stringify(result.data) }] };
        // MCP serializes both copies. Leave room for its envelope and transport metadata.
        if (Buffer.byteLength(JSON.stringify(payload)) > 4 * 1024 * 1024 - 4096) {
          return { isError: true, content: [{ type: 'text', text: 'The report response exceeds the inline limit. Use release report collection evidence.' }] };
        }
        return payload;
      } catch { return { isError: true, content: [{ type: 'text', text: 'The report source read failed.' }] }; }
      finally { reader?.close(); }
    });
  }
}
