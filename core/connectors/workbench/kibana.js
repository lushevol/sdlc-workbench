import axios from 'axios';
import { HttpsProxyAgent } from 'https-proxy-agent';
import { z } from 'zod';
import { detectProxyFor } from '../packages/core/src/proxy.js';

const indexName = z.string().min(1).max(255).regex(/^[a-z0-9][a-z0-9._*-]*$/);
const fieldName = z.string().min(1).max(255).regex(/^[A-Za-z_@][A-Za-z0-9_.@-]*$/);
const explainedField = z.object({
  field: fieldName,
  explanation: z.string().trim().min(1).max(1000),
}).strict();
const semanticMapping = z.object({
  timestamp: explainedField,
  message: explainedField,
  level: explainedField.optional(),
  service: explainedField.optional(),
  correlationId: explainedField.optional(),
}).strict();
const mappingShape = { index: indexName };
const searchShape = {
  index: indexName,
  kql: z.string().trim().min(1).max(8192),
  start: z.string().datetime({ offset: true }),
  end: z.string().datetime({ offset: true }),
  fieldMapping: semanticMapping,
  fields: z.array(explainedField).max(50).optional(),
  size: z.number().int().min(1).max(500).default(100),
};
const numericTypes = new Set(['byte', 'short', 'integer', 'long', 'unsigned_long', 'half_float', 'float', 'double', 'scaled_float']);
const exactTypes = new Set(['keyword', 'constant_keyword', 'wildcard', 'ip', 'version']);
const dateTypes = new Set(['date', 'date_nanos']);
const supportedTypes = new Set([...numericTypes, ...exactTypes, ...dateTypes, 'boolean', 'text', 'match_only_text']);
const fail = (message, code = 'KIBANA_INVALID_QUERY') => { throw Object.assign(new Error(message), { code }); };

export function validateKibanaConfig(config) {
  const selected = config.kibanaConfig;
  if (!selected || typeof selected.baseUrl !== 'string') fail('Kibana configuration is missing.');
  const url = new URL(selected.baseUrl);
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash) {
    fail('Use a Kibana base URL without credentials, query, or fragment.');
  }
  const apiKey = typeof selected.apiKey === 'string' && selected.apiKey.trim();
  const basic = typeof selected.username === 'string' && selected.username.trim() &&
    typeof selected.password === 'string' && selected.password.length;
  if (Boolean(apiKey) === Boolean(basic)) fail('Configure one Kibana authentication method.');
  if (!Array.isArray(selected.indices) || !selected.indices.length ||
      selected.indices.some(index => !indexName.safeParse(index).success)) {
    fail('Configure an explicit Kibana index allowlist.');
  }
  if (!Number.isFinite(selected.maxRangeHours ?? 24) || (selected.maxRangeHours ?? 24) < 1 ||
      (selected.maxRangeHours ?? 24) > 168) fail('Kibana maximum range must be between 1 and 168 hours.');
}

function mappingFields(mapping) {
  if (!mapping || typeof mapping !== 'object' || Array.isArray(mapping) || !Object.keys(mapping).length) {
    fail('The Console mapping response has no index mappings.');
  }
  const all = new Map();
  const walk = (properties, prefix = '', nested = false) => {
    for (const [name, definition] of Object.entries(properties || {})) {
      const field = prefix ? `${prefix}.${name}` : name;
      const type = definition.type || (definition.properties ? 'object' : 'unknown');
      const blocked = nested || type === 'nested';
      if (all.has(field)) {
        const previous = all.get(field);
        if (previous.type !== type || previous.nested !== blocked) previous.conflict = true;
      } else all.set(field, { type, nested: blocked, conflict: false });
      walk(definition.properties, field, blocked);
      walk(definition.fields, field, blocked);
    }
  };
  for (const index of Object.values(mapping)) {
    if (!index?.mappings || typeof index.mappings !== 'object') fail('Unsupported Console mapping response.');
    walk(index.mappings.properties);
    // Runtime fields can shadow indexed fields. Exclude them even when properties exist.
    for (const field of Object.keys(index.mappings.runtime || {})) {
      all.set(field, { type: 'runtime', nested: false, conflict: true });
    }
    // Alias fields retain their unsupported type and cannot become executable queries.
  }
  return all;
}

function describedFields(values, available) {
  const described = new Map();
  for (const [role, definition] of Object.entries(values.fieldMapping)) {
    described.set(definition.field, { ...definition, roles: [...(described.get(definition.field)?.roles || []), role] });
  }
  for (const definition of values.fields || []) {
    described.set(definition.field, { ...definition, roles: described.get(definition.field)?.roles || [] });
  }
  for (const [field, definition] of described) {
    const actual = available.get(field);
    if (!actual || actual.nested || actual.conflict || !supportedTypes.has(actual.type)) {
      fail(`Field ${field} is missing, conflicting, nested, or unsupported. Inspect the field mapping.`, 'KIBANA_INVALID_FIELD_MAPPING');
    }
    definition.type = actual.type;
  }
  if (!dateTypes.has(described.get(values.fieldMapping.timestamp.field)?.type)) fail('The timestamp mapping requires a date field.', 'KIBANA_INVALID_FIELD_MAPPING');
  return described;
}

// A bounded KQL grammar. Unknown syntax is rejected instead of sent as query_string.
function tokenize(source) {
  const tokens = [];
  let i = 0;
  while (i < source.length) {
    if (/\s/.test(source[i])) { i++; continue; }
    const char = source[i];
    if ('():'.includes(char)) { tokens.push({ kind: char }); i++; continue; }
    if ('<>'.includes(char)) {
      let value = source[i++];
      if (source[i] === '=') value += source[i++];
      tokens.push({ kind: 'range', value }); continue;
    }
    if (char === '"') {
      i++;
      let value = '';
      let closed = false;
      while (i < source.length) {
        if (source[i] === '"') { i++; closed = true; break; }
        if (source[i] === '\\') {
          i++;
          if (!['"', '\\'].includes(source[i])) fail('Only quote and backslash escapes are supported inside quoted KQL values.');
        }
        value += source[i++];
      }
      if (!closed) fail('The KQL quoted value is incomplete.');
      tokens.push({ kind: 'value', value, quoted: true }); continue;
    }
    let value = '';
    while (i < source.length && !/[\s():<>"\\]/.test(source[i])) value += source[i++];
    if (!value || /[{}?]/.test(value)) fail('This KQL syntax is unsupported. Use explicit field comparisons and Boolean operators.');
    tokens.push({ kind: 'value', value, quoted: false });
  }
  if (tokens.length > 1024) fail('The KQL expression is too complex.');
  return tokens;
}

export function compileKql(source, fields) {
  const tokens = tokenize(source);
  let offset = 0;
  let depth = 0;
  const peek = () => tokens[offset];
  const take = () => tokens[offset++];
  const operator = name => peek()?.kind === 'value' && !peek().quoted && peek().value.toUpperCase() === name;
  const clause = () => {
    const fieldToken = take();
    if (!fieldToken || fieldToken.kind !== 'value' || fieldToken.quoted) fail('KQL requires an explicit field name.');
    if (fieldToken.value === '*' && offset === tokens.length && tokens.length === 1) return { match_all: {} };
    const field = fieldToken.value;
    const definition = fields.get(field);
    if (!definition) fail(`KQL field ${field} requires a field mapping and explanation.`);
    const comparison = take();
    if (!comparison || ![':', 'range'].includes(comparison.kind)) fail('KQL requires a field comparison.');
    const value = take();
    if (!value || value.kind !== 'value' || (!value.quoted && ['AND', 'OR', 'NOT'].includes(value.value.toUpperCase()))) {
      fail('KQL requires one value per field comparison.');
    }
    if (comparison.kind === ':' && value.value === '*' && !value.quoted) return { exists: { field } };
    const type = definition.type;
    let typed = value.value;
    if (numericTypes.has(type)) {
      if (!/^-?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$/.test(typed) || !Number.isFinite(Number(typed))) {
        fail(`KQL field ${field} requires a numeric value.`);
      }
      // Preserve large integer bytes; Elasticsearch accepts numeric strings.
    } else if (type === 'boolean') {
      if (!['true', 'false'].includes(typed)) fail(`KQL field ${field} requires true or false.`);
      typed = typed === 'true';
    } else if (dateTypes.has(type)) {
      if (!z.string().datetime({ offset: true }).safeParse(typed).success) fail(`KQL field ${field} requires an absolute ISO timestamp.`);
    }
    if (comparison.kind === 'range') {
      if (!numericTypes.has(type) && !dateTypes.has(type)) fail('KQL ranges support numeric and date fields only.');
      const names = { '>': 'gt', '>=': 'gte', '<': 'lt', '<=': 'lte' };
      return { range: { [field]: { [names[comparison.value]]: typed } } };
    }
    if (!value.quoted && typed.includes?.('*')) {
      if (!['keyword', 'constant_keyword', 'wildcard'].includes(type) || !/^[^*]+\*$/.test(typed)) {
        fail('KQL supports one trailing wildcard on a keyword field only.');
      }
      return { wildcard: { [field]: { value: typed } } };
    }
    if (type === 'text' || type === 'match_only_text') {
      return value.quoted ? { match_phrase: { [field]: typed } } : { match: { [field]: { query: typed, operator: 'and' } } };
    }
    return { term: { [field]: typed } };
  };
  const unary = () => {
    if (++depth > 50) fail('The KQL nesting limit is 50.');
    let result;
    if (operator('NOT')) { take(); result = { bool: { must_not: [unary()] } }; }
    else if (peek()?.kind === '(') {
      take(); result = or();
      if (take()?.kind !== ')') fail('KQL parentheses are incomplete.');
    } else result = clause();
    depth--;
    return result;
  };
  const and = () => {
    const clauses = [unary()];
    while (operator('AND')) { take(); clauses.push(unary()); }
    return clauses.length === 1 ? clauses[0] : { bool: { filter: clauses } };
  };
  const or = () => {
    const clauses = [and()];
    while (operator('OR')) { take(); clauses.push(and()); }
    return clauses.length === 1 ? clauses[0] : { bool: { should: clauses, minimum_should_match: 1 } };
  };
  const output = or();
  if (offset !== tokens.length) fail('This KQL syntax is unsupported. Use explicit comparisons, AND, OR, NOT, and parentheses.');
  return output;
}

export class KibanaReader {
  constructor(config) {
    validateKibanaConfig(config);
    this.config = config;
    this.selected = config.kibanaConfig;
  }

  allowed(index) {
    indexName.parse(index);
    if (!this.selected.indices.includes(index)) fail('The requested index selector is not in KIBANA_ALLOWED_INDICES.', 'KIBANA_INDEX_DENIED');
  }

  async consoleRead(index, operation, body) {
    this.allowed(index);
    if (!['_mapping', '_search'].includes(operation)) fail('The Console operation is not read-only.');
    const proxy = await detectProxyFor(this.selected.baseUrl, this.config.HTTPS_PROXY);
    const agent = proxy ? new HttpsProxyAgent(proxy) : undefined;
    const headers = {
      Authorization: this.selected.apiKey ? `ApiKey ${this.selected.apiKey}` :
        `Basic ${Buffer.from(`${this.selected.username}:${this.selected.password}`).toString('base64')}`,
      'kbn-xsrf': 'workbench-read-only', Accept: 'application/json',
    };
    try {
      const url = `${this.selected.baseUrl.replace(/\/+$/, '')}/api/console/proxy`;
      const response = await axios.request({
        method: 'POST', url,
        params: { path: `${index}/${operation}`, method: operation === '_mapping' ? 'GET' : 'POST' },
        headers, data: body, proxy: false, httpAgent: agent, httpsAgent: agent,
        maxRedirects: 0, timeout: 30000, maxContentLength: 2 * 1024 * 1024, maxBodyLength: 128 * 1024,
      });
      if (!response.data || typeof response.data !== 'object' || Array.isArray(response.data)) fail('The Console response is not JSON data.');
      return response.data;
    } catch {
      fail('The Kibana Console read failed. Check the endpoint, read-only role, authentication, and Console compatibility.');
    } finally {
      agent?.destroy();
    }
  }

  async fieldMapping(args) {
    const { index } = z.object(mappingShape).strict().parse(args);
    const mapping = await this.consoleRead(index, '_mapping');
    const fields = mappingFields(mapping);
    return {
      index, mapping,
      fields: Object.fromEntries(fields),
      explanation: 'The mapping supplies technical types. Supply project-owned explanations for timestamp, message, and every queried field.',
      limits: 'Nested, runtime, alias, conflicting, and unsupported field types cannot be used by the log search tool.',
    };
  }

  async searchLogs(args) {
    const values = z.object(searchShape).strict().parse(args);
    this.allowed(values.index);
    const rangeMs = Date.parse(values.end) - Date.parse(values.start);
    if (rangeMs <= 0 || rangeMs > (this.selected.maxRangeHours ?? 24) * 3600000) {
      fail('The log time range must be positive and within the configured maximum.', 'KIBANA_INVALID_TIME_RANGE');
    }
    const available = mappingFields(await this.consoleRead(values.index, '_mapping'));
    const described = describedFields(values, available);
    const filter = compileKql(values.kql, described);
    const query = {
      size: values.size, _source: false, fields: [...described.keys()], track_total_hits: true,
      timeout: '20s', sort: [{ [values.fieldMapping.timestamp.field]: { order: 'desc' } }],
      query: { bool: { filter: [
        { range: { [values.fieldMapping.timestamp.field]: { gte: values.start, lt: values.end } } }, filter,
      ] } },
    };
    const data = await this.consoleRead(values.index, '_search', query);
    if (!data.hits || !Array.isArray(data.hits.hits)) fail('The Console search response is unsupported.');
    const total = data.hits.total;
    const totalCount = typeof total === 'number' ? total : total?.value;
    const failedShards = data._shards?.failed ?? null;
    return {
      index: values.index, kql: values.kql, fieldMapping: values.fieldMapping,
      fieldExplanations: [...described.values()], query, data,
      explanation: `Search ${values.index} through Kibana Console. Use ${values.fieldMapping.timestamp.field} for the inclusive start and exclusive end. Return at most ${values.size} newest logs.`,
      completeness: {
        returned: data.hits.hits.length, total: totalCount ?? null, totalRelation: total?.relation || null,
        truncated: typeof totalCount !== 'number' ? null : totalCount > data.hits.hits.length ? true :
          (total?.relation === 'gte' ? null : false),
        timedOut: data.timed_out ?? null, failedShards,
        partial: data.timed_out === true || (typeof failedShards === 'number' && failedShards > 0) ? true :
          (data.timed_out === false && typeof failedShards === 'number' ? false : null),
      },
      limits: 'Supported KQL: explicit field comparisons, Boolean AND/OR/NOT, parentheses, quoted phrases, existence, numeric/date ranges, and one trailing keyword wildcard. Nested, runtime, field wildcards, value lists, free text, and other syntax are rejected. Results describe this bounded search only.',
    };
  }
}

export function configureKibanaTools(server, config) {
  const register = (name, description, shape, action) => server.tool(name, description, shape, async args => {
    try {
      const reader = new KibanaReader(config);
      return { content: [{ type: 'text', text: JSON.stringify(await reader[action](args)) }] };
    } catch (error) {
      return { content: [{ type: 'text', text: error.message }], structuredContent: { code: error.code || 'KIBANA_INVALID_QUERY' }, isError: true };
    }
  });
  register('kibana_get_field_mapping',
    'Read Elasticsearch field mappings through Kibana Console. Use technical types with project-owned semantic explanations before log analysis.',
    mappingShape, 'fieldMapping');
  register('kibana_search_logs',
    'Read logs through Kibana Console with mandatory explained field mapping and bounded absolute time range. Supported KQL: explicit comparisons, AND/OR/NOT, parentheses, phrases, existence, numeric/date ranges, trailing keyword wildcard. Unsupported syntax is rejected. No arbitrary Console requests or DSL.',
    searchShape, 'searchLogs');
}
