import { test, expect } from '../support/audit-fixture.js';
import { CacheApp, type CacheVersion } from '../support/cache-app.js';
import { LoginPage } from '../pages/login.page.js';
import { localPrefix } from '../support/local-app.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual current React shell and real Chromium HTTP cache. Local HTTP fixture server supplies synthetic Alice, permissions, base entry wrapper, container, tile, trade, lazy content, CSS and images. V1/V2 markers identify controlled fixture assets. No browser routing, production CDN, real business tenant, or changed base binary acceptance.' });

const allVersions = (version: CacheVersion) => ({ base: version, container: version, tile: version, lazy: version, css: version, image: version });
const ids = ['KNOW-041', 'KNOW-042', 'KNOW-043', 'KNOW-044', 'KNOW-045', 'KNOW-046',
  'KNOW-047', 'KNOW-048', 'KNOW-049', 'KNOW-050', 'KNOW-051', 'KNOW-052'] as const;

for (const id of ids) {
  test(`${id} real HTTP cache and controlled tenant lifecycle`, async ({ page, audit }) => {
    test.setTimeout(60000);
    await audit.defineCase(id);
    const app = new CacheApp(page);
    const login = new LoginPage(page, localPrefix);
    const tileVersion = () => app.panel().getByTestId('cache-tile-version');
    const drawerVisible = () => expect(app.drawer().getByText('Tile Options', { exact: true })).toBeVisible();
    const noChunkError = async () => {
      await expect(app.complete()).toBeVisible();
      await expect(app.panel().getByTestId('FallbackError__page-id')).toHaveCount(0);
      expect(app.events.filter(event => String(event.path).includes('/cache/tile-') && Number(event.status) >= 400)).toEqual([]);
    };
    const expectMarkers = async (version: CacheVersion) => {
      await expect(app.complete()).toBeVisible();
      for (const kind of ['base', 'container', 'tile'])
        await expect(app.panel().getByTestId(`cache-${kind}-version`)).toHaveText(version);
    };
    const noActiveVersion = (version: CacheVersion) => expect(tileVersion().filter({ hasText: new RegExp(`^${version}$`) })).toHaveCount(0);
    try {
      await audit.step(1, async () => {
        if (id === 'KNOW-052') app.versions = allVersions('V2');
        await app.start();
        await audit.record('cache-fixture-scope', app.observations());
      });
      await audit.step(2, async () => {
        await app.portal.expectVisible();
        await audit.record('catalog-permission', { actor: 'alice', exactTileTitle: 'T-CACHE',
          source: 'Controlled local HTTP login/validate responses', container: '@fm/cache-container', tile: '/cache' });
      });

      if (id === 'KNOW-041') {
        await audit.step(3, async () => {
          await app.cdp.send('Network.clearBrowserCache');
          expect(app.events.some(event => event.path === '/cache/tile-entry.js')).toBe(false);
          await audit.record('empty-tenant-cache', { method: 'CDP Network.clearBrowserCache', tileEntryPreviouslyRequested: false });
        });
        await audit.step(4, async () => { app.versions = allVersions('V1'); });
        await audit.step(5, () => app.openDrawer());
        await audit.step(6, drawerVisible);
        await audit.step(7, () => app.openTile());
        await audit.step(8, () => expectMarkers('V1'));
        await audit.step(9, noChunkError);
      } else if (id === 'KNOW-045') {
        await audit.step(3, async () => { await expect(page.getByTestId('cache-base-entry-version')).toHaveText('Portal fixture base V1'); });
        await audit.step(4, async () => { app.versions.base = 'V2'; await app.saveBlankWorkspace(); });
        await audit.step(5, () => app.reload());
        await audit.step(6, async () => { await expect(page.getByTestId('cache-base-entry-version')).toHaveText('Portal fixture base V2'); });
        await audit.step(7, () => app.openDrawer());
        await audit.step(8, drawerVisible);
      } else if (id === 'KNOW-046') {
        await audit.step(3, () => app.warm('V1'));
        await audit.step(4, async () => { app.versions = allVersions('V2'); });
        await audit.step(5, async () => { expect(new URL(page.url()).searchParams.get('show_normal_login')).toBe('Y'); });
        await audit.step(6, () => app.portal.clickAvatarButton());
        await audit.step(7, () => app.portal.clickLogoutMenuItem());
        await audit.step(8, async () => {
          await page.getByRole('dialog', { name: 'Leave Now?', exact: true }).getByRole('button', { name: 'Logout', exact: true }).click();
          await login.expectVisible();
        });
        await audit.step(9, () => login.fillUsername('alice'));
        await audit.step(10, () => login.fillPassword('FixturePass1!'));
        await audit.step(11, async () => { await login.clickSignInButton(); await app.portal.expectVisible(); });
        await audit.step(12, () => app.openDrawer());
        await audit.step(13, drawerVisible);
        await audit.step(14, () => app.openTile());
        await audit.step(15, async () => { await expect(tileVersion()).toHaveText('V2'); });
        await audit.step(16, () => noActiveVersion('V1'));
      } else if (id === 'KNOW-047') {
        await audit.step(3, async () => {
          const entry = await page.evaluate(async origin => {
            const response = await fetch(`${origin}/cache/tile-entry.js`);
            return { status: response.status, body: await response.text(), cacheControl: response.headers.get('cache-control') };
          }, app.origin);
          expect(entry.status).toBe(200); expect(entry.body).toContain('tile-V1.js');
          await audit.record('held-v1-entry', entry);
        });
        await audit.step(4, async () => { app.removedV1Chunk = true; });
        await audit.step(5, () => app.openDrawer());
        await audit.step(6, drawerVisible);
        await audit.step(7, () => app.openTile());
        await audit.step(8, async () => {
          await expect(app.panel().getByTestId('FallbackError__page-id')).toBeVisible();
          await expect(app.complete()).toHaveCount(0);
          expect(app.events.some(event => event.path === '/cache/tile-V1.js' && event.status === 404)).toBe(true);
        });
        await audit.step(9, () => app.openDrawer());
        await audit.step(10, drawerVisible);
      } else if (id === 'KNOW-048') {
        await audit.step(3, async () => { await app.warm('V1'); await expect(app.panel().getByTestId('cache-trade-id')).toHaveText('TR-1001'); });
        await audit.step(4, async () => { app.failTileEntry = true; await app.saveBlankWorkspace(); });
        await audit.step(5, async () => {
          app.versions = allVersions('V2');
          await audit.record('versioned-trade-fixtures', { V1: { identifier: 'TR-1001', amount: '100' }, V2: { identifier: 'TR-1002', amount: '200' },
            loadFailureState: 'Actual MFE FallbackError__page-id: There is a problem in this Tile.',
            limit: 'This source-defined failure state is used for characterization. Business agreement remains unverified.' });
        });
        await audit.step(6, () => app.reload());
        await audit.step(7, () => app.openDrawer());
        await audit.step(8, drawerVisible);
        await audit.step(9, () => app.openTile());
        await audit.step(10, async () => {
          await expect(app.panel().getByTestId('FallbackError__page-id')).toBeVisible();
          await expect(app.panel().getByTestId('cache-trade-id')).toHaveCount(0);
          await expect(app.panel().getByTestId('cache-trade-amount')).toHaveCount(0);
          expect(app.events.some(event => event.path === '/cache/tile-entry.js' && event.status === 503)).toBe(true);
        });
        await audit.step(11, async () => { await expect(app.panel().getByText('There is a problem in this Tile.', { exact: true })).toBeVisible(); });
      } else {
        await audit.step(3, async () => {
          await app.warm(id === 'KNOW-052' ? 'V2' : 'V1');
          if (id === 'KNOW-049') {
            await app.panel().getByRole('button', { name: 'Open lazy search', exact: true }).click();
            await expect(app.panel().getByTestId('cache-lazy-version')).toHaveText('V1');
          }
          if (id === 'KNOW-051') await expect.poll(() => app.panel().getByTestId('cache-image').evaluate((image: HTMLImageElement) => image.naturalWidth)).toBeGreaterThan(0);
        });
        await audit.step(4, async () => {
          if (id === 'KNOW-042') app.versions.tile = 'V2';
          if (id === 'KNOW-044') app.versions.container = 'V2';
          if (id === 'KNOW-049') { app.versions.tile = 'V2'; app.versions.lazy = 'V2'; }
          if (id === 'KNOW-050') { app.versions.tile = 'V2'; app.versions.css = 'V2'; }
          if (id === 'KNOW-051') { app.versions.tile = 'V2'; app.versions.image = 'V2'; }
          if (id === 'KNOW-052') app.versions = allVersions('V1');
          await app.saveBlankWorkspace();
        });
        await audit.step(5, () => app.reload());
        await audit.step(6, () => app.openDrawer());
        await audit.step(7, drawerVisible);
        await audit.step(8, () => app.openTile());
        if (id === 'KNOW-042') {
          await audit.step(9, async () => { await expect(tileVersion()).toHaveText('V2'); });
          await audit.step(10, () => noActiveVersion('V1'));
        } else if (id === 'KNOW-043') {
          await audit.step(9, () => expectMarkers('V1'));
          await audit.step(10, async () => {
            await noChunkError();
            expect(app.events.some(event => event.path === '/cache/tile-entry.js' && event.status === 304)).toBe(true);
          });
        } else if (id === 'KNOW-044') {
          await audit.step(9, async () => {
            await expect(app.panel().getByTestId('cache-container-version')).toHaveText('V2');
            await expect(tileVersion()).toHaveText('V1');
          });
        } else if (id === 'KNOW-049') {
          await audit.step(9, async () => { await app.panel().getByRole('button', { name: 'Open lazy search', exact: true }).click(); });
          await audit.step(10, async () => { await expect(app.panel().getByTestId('cache-lazy-version')).toHaveText('V2'); });
          await audit.step(11, async () => { await expect(app.panel().getByTestId('cache-lazy-version').filter({ hasText: /^V1$/ })).toHaveCount(0); });
        } else if (id === 'KNOW-050') {
          await audit.step(9, async () => {
            await expect(app.panel().getByTestId('cache-appearance')).toHaveText('Appearance V2');
            await expect(app.complete()).toHaveCSS('background-color', 'rgb(204, 238, 255)');
          });
          await audit.step(10, async () => {
            await expect(app.panel().getByRole('heading', { name: 'T-CACHE controlled tenant', exact: true })).toBeVisible();
            await expect(app.panel().getByRole('button', { name: 'Open lazy search', exact: true })).toBeVisible();
            await expect(app.panel().getByTestId('cache-trade-id')).toBeVisible();
          });
        } else if (id === 'KNOW-051') {
          await audit.step(9, async () => { await expect(app.panel().getByTestId('cache-image')).toHaveAttribute('src', `${app.origin}/cache/image-V2.svg`); });
          await audit.step(10, async () => { await expect.poll(() => app.panel().getByTestId('cache-image').evaluate((image: HTMLImageElement) => image.naturalWidth)).toBeGreaterThan(0); });
        } else if (id === 'KNOW-052') {
          await audit.step(9, () => expectMarkers('V1'));
          await audit.step(10, async () => {
            await expect(app.panel().getByTestId('cache-trade-id')).toHaveText('TR-1001');
            await expect(app.panel().getByTestId('cache-trade-amount')).toHaveText('100');
          });
        }
      }
    } finally {
      await audit.record('http-cache-observations', app.observations());
      await app.close();
    }
  });
}
