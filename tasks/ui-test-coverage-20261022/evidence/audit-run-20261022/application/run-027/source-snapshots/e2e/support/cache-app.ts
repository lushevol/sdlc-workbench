import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import { createHash } from 'node:crypto';
import { expect, type CDPSession, type Page } from '@playwright/test';
import { LoginPage } from '../pages/login.page.js';
import { PortalPage } from '../pages/portal.page.js';
import { fixtureCategory, fixtureEntity, fixtureTile } from './catalog-app.js';
import { localBase, localPrefix, workspace } from './local-app.js';

export type CacheVersion = 'V1' | 'V2';
type Versions = { base: CacheVersion; container: CacheVersion; tile: CacheVersion; lazy: CacheVersion; css: CacheVersion; image: CacheVersion };
const selected = (version: CacheVersion): Versions => ({ base: version, container: version, tile: version, lazy: version, css: version, image: version });
const hash = (bytes: string | Buffer) => createHash('sha256').update(bytes).digest('hex');

/** Real HTTP fixture transport. Playwright routing is deliberately absent because it disables HTTP cache. */
export class CacheApp {
  readonly server = createServer((request, response) => { void this.respond(request, response).catch(error => {
    this.events.push({ path: request.url, status: 500, error: String(error) });
    if (!response.headersSent) response.writeHead(500); response.end('Controlled cache fixture failure');
  }); });
  readonly portal: PortalPage;
  readonly events: Record<string, unknown>[] = [];
  readonly cacheHits: { url: string }[] = [];
  versions = selected('V1');
  removedV1Chunk = false;
  failTileEntry = false;
  origin = '';
  cdp!: CDPSession;
  private urls = new Map<string, string>();

  constructor(readonly page: Page) { this.portal = new PortalPage(page, localPrefix); }
  panel() { return this.page.getByRole('tabpanel').filter({ visible: true }); }
  drawer() { return this.page.getByTestId(`${localPrefix}_drawer`); }
  complete() { return this.panel().getByTestId('cache-complete'); }

  async start(): Promise<void> {
    await new Promise<void>(resolve => this.server.listen(0, '127.0.0.1', resolve));
    const address = this.server.address();
    if (!address || typeof address === 'string') throw new Error('Cache fixture HTTP port was not allocated.');
    this.origin = `http://127.0.0.1:${address.port}`;
    this.cdp = await this.page.context().newCDPSession(this.page);
    await this.cdp.send('Network.enable');
    await this.cdp.send('Network.setCacheDisabled', { cacheDisabled: false });
    await this.cdp.send('Network.setBlockedURLs', { urls: ['https://*'] });
    this.cdp.on('Network.requestWillBeSent', event => this.urls.set(event.requestId, event.request.url));
    this.cdp.on('Network.requestServedFromCache', event => this.cacheHits.push({ url: this.urls.get(event.requestId) ?? event.requestId }));
    await this.page.addInitScript(value => {
      if (!localStorage.getItem('CACHE_FIXTURE_INITIALIZED')) {
        localStorage.setItem('SET_WORKSPACES', JSON.stringify([value]));
        localStorage.setItem('CACHE_FIXTURE_INITIALIZED', 'true');
      }
    }, workspace());
    await this.page.goto(`${this.origin}/?show_normal_login=Y&survey=no`);
    const login = new LoginPage(this.page, localPrefix);
    await login.expectVisible(); await login.fillUsername('alice'); await login.fillPassword('FixturePass1!');
    await login.clickSignInButton(); await this.portal.expectVisible();
  }

  async openDrawer(): Promise<void> {
    await this.page.getByTestId(`${localPrefix}_new_tile`).click();
    await expect(this.drawer().getByText('Tile Options', { exact: true })).toBeVisible();
  }
  async openTile(): Promise<void> {
    await this.drawer().getByText('T-CACHE', { exact: true }).click();
  }
  async warm(version: CacheVersion): Promise<void> {
    this.versions = selected(version);
    await this.openDrawer(); await this.openTile();
    await expect(this.complete()).toBeVisible();
    await expect(this.panel().getByTestId('cache-tile-version')).toHaveText(version);
  }
  async saveBlankWorkspace(): Promise<void> {
    await this.page.evaluate(value => localStorage.setItem('SET_WORKSPACES', JSON.stringify([value])), workspace());
  }
  async reload(): Promise<void> { await this.page.reload(); await this.portal.expectVisible(); }
  async close(): Promise<void> {
    this.server.closeAllConnections();
    await new Promise<void>(resolve => this.server.close(() => resolve()));
  }
  observations() {
    return { origin: this.origin, versions: this.versions, serverEvents: this.events, cacheHits: this.cacheHits,
      cache: 'Real Chromium HTTP cache; CDP cache enabled; no Playwright route handlers.',
      limits: ['The actual MFE binary remains unchanged. The base V1/V2 marker identifies a controlled SystemJS entry wrapper.',
        'Container, tile, trade, lazy content, CSS, and image versions belong to controlled tenant fixtures.',
        'These observations do not establish a real deployment CDN policy or business tenant cache acceptance.'] };
  }

  private send(request: IncomingMessage, response: ServerResponse, body: string | Buffer,
    type: string, cache = 'no-store', status = 200): void {
    const etag = `"${hash(body)}"`;
    const revalidated = status === 200 && cache === 'no-cache' && request.headers['if-none-match'] === etag;
    const code = revalidated ? 304 : status;
    this.events.push({ path: request.url, method: request.method, status: code, etag,
      ifNoneMatch: request.headers['if-none-match'] ?? null, cacheControl: cache, sha256: hash(body) });
    response.writeHead(code, { 'content-type': type, 'cache-control': cache, etag });
    response.end(revalidated ? undefined : body);
  }

  private async respond(request: IncomingMessage, response: ServerResponse): Promise<void> {
    const url = new URL(request.url ?? '/', this.origin);
    if (url.pathname.startsWith('/api/')) {
      let body: Record<string, unknown> = { result: true };
      const now = Math.floor(Date.now() / 1000);
      const encode = (value: unknown) => Buffer.from(JSON.stringify(value)).toString('base64url');
      const token = `${encode({ alg: 'none' })}.${encode({ sub: 'alice', iat: now, exp: now + 3600 })}.fixture`;
      response.setHeader('single-ui-authorization', `Bearer ${token}`);
      if (url.pathname.endsWith('/refreshtoken')) response.setHeader('single-ui-refresh', `Bearer ${token}`);
      if (/\/(?:login|validate|extend)$/.test(url.pathname)) {
        body = { result: true, userInfo: JSON.stringify({ sub: 'alice', fullName: 'Alice', auth_time: now,
          entitlements: { 'TEST_ENTITY:Viewer': { TEST_SUBJECT: ['READ'] } } }), entities: [fixtureEntity()],
        drawers: [fixtureCategory([fixtureTile({ title: 'T-CACHE', subtitle: undefined, container: '@fm/cache-container',
          module: '/cache', tile: '/cache', imageDarkTheme: 'cache/drawer.svg', imageLightTheme: 'cache/drawer.svg' })])] };
      }
      this.send(request, response, JSON.stringify(body), 'application/json'); return;
    }
    if (url.pathname.includes('importmap') && url.pathname.endsWith('.json')) {
      const upstream = await fetch(`${localBase}${url.pathname}`); const map = await upstream.json() as { imports: Record<string, string> };
      map.imports['@audit/actual-base'] = 'http://127.0.0.1:8122/base.js';
      map.imports['@fm/base'] = `${this.origin}/cache/base-entry.js`;
      map.imports['@fm/cache-container'] = `${this.origin}/cache/container-entry.js`;
      map.imports['@fm/cache-tile'] = `${this.origin}/cache/tile-entry.js`;
      this.send(request, response, JSON.stringify(map), 'application/json'); return;
    }
    const v = this.versions;
    if (url.pathname === '/cache/base-entry.js') {
      const body = `System.register(['@audit/actual-base'],function(exports){return{setters:[function(base){Object.keys(base).forEach(function(key){exports(key,base[key]);});}],execute:function(){window.__cacheBaseVersion='${v.base}';var marker=document.createElement('aside');marker.setAttribute('data-testid','cache-base-entry-version');marker.textContent='Portal fixture base ${v.base}';marker.style.cssText='position:fixed;right:8px;bottom:8px;background:#fff3b0;color:#111;padding:6px;z-index:1500';document.body.appendChild(marker);}};});`;
      this.send(request, response, body, 'application/javascript', 'no-cache'); return;
    }
    if (url.pathname === '/cache/container-entry.js') {
      const body = `System.register(['react'],function(exports){var React;return{setters:[function(value){React=value.default||value;}],execute:function(){var Tile=React.lazy(function(){return System.import('@fm/cache-tile');});exports('default',function(props){return React.createElement(React.Suspense,{fallback:React.createElement('p',null,'Controlled tenant loading')},React.createElement(Tile,Object.assign({},props,{containerVersion:'${v.container}'})));});}};});`;
      this.send(request, response, body, 'application/javascript', 'no-cache'); return;
    }
    if (url.pathname === '/cache/tile-entry.js') {
      if (this.failTileEntry) { this.send(request, response, 'Controlled entry unavailable', 'text/plain', 'no-store', 503); return; }
      const body = `System.register(['react'],function(exports){var React;return{setters:[function(value){React=value.default||value;}],execute:function(){var Tile=React.lazy(function(){return System.import('${this.origin}/cache/tile-${v.tile}.js');});exports('default',Tile);}};});`;
      this.send(request, response, body, 'application/javascript', 'no-cache'); return;
    }
    const tileMatch = /^\/cache\/tile-(V[12])\.js$/.exec(url.pathname);
    if (tileMatch) {
      const version = tileMatch[1] as CacheVersion;
      if (version === 'V1' && this.removedV1Chunk) { this.send(request, response, 'Controlled removed chunk', 'text/plain', 'no-store', 404); return; }
      const trade = version === 'V1' ? 'TR-1001' : 'TR-1002'; const amount = version === 'V1' ? '100' : '200';
      const body = `System.register(['react'],function(exports){var React;return{setters:[function(value){React=value.default||value;}],execute:function(){var style=document.createElement('link');style.rel='stylesheet';style.href='${this.origin}/cache/tile-${v.css}.css';document.head.appendChild(style);exports('default',function(props){var lazy=React.useState(null);var e=React.createElement;return e('section',{'data-testid':'cache-complete',className:'controlled-cache-tile'},e('h2',null,'T-CACHE controlled tenant'),e('p',{'data-testid':'cache-base-version'},window.__cacheBaseVersion),e('p',{'data-testid':'cache-container-version'},props.containerVersion),e('p',{'data-testid':'cache-tile-version'},'${version}'),e('p',{'data-testid':'cache-appearance'},'Appearance ${v.css}'),e('p',{'data-testid':'cache-trade-id'},'${trade}'),e('p',{'data-testid':'cache-trade-amount'},'${amount}'),e('img',{'data-testid':'cache-image',src:'${this.origin}/cache/image-${v.image}.svg',alt:'Fixture image ${v.image}'}),e('button',{onClick:function(){System.import('${this.origin}/cache/lazy-${v.lazy}.js').then(function(mod){lazy[1](function(){return mod.default;});});}},'Open lazy search'),lazy[0]?e(lazy[0]):null);});}};});`;
      this.send(request, response, body, 'application/javascript', 'public, max-age=31536000, immutable'); return;
    }
    const lazyMatch = /^\/cache\/lazy-(V[12])\.js$/.exec(url.pathname);
    if (lazyMatch) {
      const body = `System.register(['react'],function(exports){var React;return{setters:[function(value){React=value.default||value;}],execute:function(){exports('default',function(){return React.createElement('section',{'data-testid':'cache-lazy-panel'},React.createElement('h3',null,'Lazy search'),React.createElement('p',{'data-testid':'cache-lazy-version'},'${lazyMatch[1]}'));});}};});`;
      this.send(request, response, body, 'application/javascript', 'public, max-age=31536000, immutable'); return;
    }
    if (/^\/cache\/tile-V[12]\.css$/.test(url.pathname)) {
      this.send(request, response, `.controlled-cache-tile{padding:20px;background:${url.pathname.includes('V2') ? '#cceeff' : '#f0f0f0'};color:#111}.controlled-cache-tile img{width:240px;height:90px}`, 'text/css', 'public, max-age=31536000, immutable'); return;
    }
    if (url.pathname.startsWith('/cache/') && url.pathname.endsWith('.svg')) {
      const version = url.pathname.includes('V2') ? 'V2' : 'V1';
      this.send(request, response, `<svg xmlns="http://www.w3.org/2000/svg" width="240" height="90"><rect width="240" height="90" fill="${version === 'V2' ? '#3b9' : '#369'}"/><text x="20" y="50" fill="white">Controlled image ${version}</text></svg>`, 'image/svg+xml', 'public, max-age=31536000, immutable'); return;
    }
    const upstream = await fetch(`${localBase}${url.pathname}${url.search}`);
    let bytes = Buffer.from(await upstream.arrayBuffer());
    const contentType = upstream.headers.get('content-type') ?? 'application/octet-stream';
    if (contentType.includes('text/html')) bytes = Buffer.from(bytes.toString('utf8').replace(/<link[^>]+href="https:\/\/fonts[^>]+>/g, ''));
    this.send(request, response, bytes, contentType, 'no-store', upstream.status);
  }
}
