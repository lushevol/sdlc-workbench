import { test, expect } from '../support/audit-fixture.js';
import { loginCatalog, type CatalogApp } from '../support/catalog-app.js';
import { localPrefix } from '../support/local-app.js';

test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  auditFixture: 'Actual portal Profile and exported Dialog components. A controlled SystemJS module supplies the declared isolated dialog or scrollable content. This run checks component behavior; the fixture content is not business output.' });

const moduleText = (dialog: boolean) => `System.register(['react','@fm/base'],function(exports){var React,base;return{setters:[function(v){React=v.default||v;},function(v){base=v;}],execute:function(){exports('default',function(props){var open=React.useState(true);return React.createElement('section',{'data-testid':'audit-controlled-container'},React.createElement('p',{'data-testid':'fixture-tile-route'},props.tile),${dialog
  ? "React.createElement(base.Dialog.default,{open:open[0],onClose:function(){open[1](false);},isDraggable:true,isResizeble:true,disablePortal:true,defaultWidth:700,defaultHeight:600,titleComponents:'Fixture Dialog'},React.createElement('div',{style:{height:'1600px'}},'Scrollable fixture content'),React.createElement('p',null,'CONTENT-END'))"
  : "React.createElement('div',{style:{height:'1800px'}},'Scrollable fixture content'),React.createElement('p',null,'CONTENT-END')"});});}};});`;

for (const number of [32, 33, 34, 35]) {
  const id = `UX-${String(number).padStart(3, '0')}`;
  test(`${id} actual dialog boundaries with step evidence`, async ({ page, audit }) => {
    const steps = await audit.defineCase(id);
    let app: CatalogApp;
    let scrollBefore = 0;
    const isolated = number === 33 || number === 34;
    const dialog = page.locator('[role="dialog"]:visible').filter({ has: page.getByText(isolated ? 'Fixture Dialog' : 'User Profile', { exact: true }) });
    const close = () => dialog.getByTestId(`${localPrefix}_Dialog-close`);
    const maximize = () => dialog.getByTestId(`${localPrefix}_Dialog-maximize`);
    const scrollArea = () => page.locator('[role="tabpanel"]:visible .tabmain');
    for (const step of steps) await audit.step(step.number, async () => {
      const text = step.text;
      if (step.number === 1) {
        await page.setViewportSize({ width: 1366, height: 768 });
        app = await loginCatalog(page, { occupied: true });
        if (number !== 32) {
          await page.route('**/audit-fixtures/test-container.js', route => route.fulfill({ status: 200, contentType: 'application/javascript', body: moduleText(isolated) }));
          await page.reload({ waitUntil: 'domcontentloaded' }); await app.portal.expectVisible();
          await expect(page.getByTestId('fixture-tile-route')).toBeVisible();
        }
        if (!isolated) { await app.portal.clickAvatarButton(); await app.openProfile(); }
        await expect(dialog).toBeVisible();
        if (number === 35) { scrollBefore = await scrollArea().evaluate(node => node.scrollTop); await audit.record('workspace-scroll-fixture', { fixtureId: 'WS-SCROLL', locator: '[role=tabpanel]:visible .tabmain', scrollBefore }); }
        return;
      }
      if (text.includes('changes the viewport')) { await page.setViewportSize({ width: 768, height: 600 }); return; }
      if (text.includes('visible title text')) { await expect(dialog.getByText('User Profile', { exact: true })).toBeVisible(); return; }
      if (text.includes('drags the text labelled')) {
        const header = dialog.getByTestId(`${localPrefix}_Dialog-header`);
        const box = await dialog.boundingBox(), title = await header.boundingBox(); expect(box).toBeTruthy(); expect(title).toBeTruthy();
        const x = title!.x + 60, y = title!.y + 12;
        await page.mouse.move(x, y); await page.mouse.down(); await page.mouse.move(x - box!.x, y - box!.y, { steps: 20 }); await page.mouse.up();
        await audit.record('dialog-drag', { before: box, after: await dialog.boundingBox(), targetTopLeft: { x: 0, y: 0 } }); return;
      }
      if (text.includes('drags the icon button')) {
        const target = dialog.getByTestId(`${localPrefix}_Dialog-resize`); const box = await target.boundingBox(); expect(box).toBeTruthy();
        const x = box!.x + box!.width / 2, y = box!.y + box!.height / 2;
        await page.mouse.move(x, y); await page.mouse.down(); await page.mouse.move(x - 800, y - 800, { steps: 20 }); await page.mouse.up();
        await audit.record('dialog-resize', { pointerStart: { x, y }, pointerEnd: { x: x - 800, y: y - 800 }, dialog: await dialog.boundingBox() }); return;
      }
      if (text.includes('CONTENT-END') && text.includes('reachable')) { const marker = dialog.getByText('CONTENT-END', { exact: true }); await marker.scrollIntoViewIfNeeded(); await expect(marker).toBeInViewport(); return; }
      if (text.includes('Fixture Dialog') && text.includes('visible and reachable')) { await expect(dialog.getByText('Fixture Dialog', { exact: true })).toBeInViewport(); return; }
      if (text.includes('Close') && (text.includes('visible and enabled') || text.includes('visible and reachable'))) {
        await close().scrollIntoViewIfNeeded(); await expect(close()).toBeInViewport(); await expect(close()).toBeEnabled(); return;
      }
      if (text.startsWith('USER-A clicks the button labelled "Maximize"')) {
        await audit.record('source-resolved-maximize-target', { canonicalName: 'Maximize', actualAccessibleName: 'resize', testId: `${localPrefix}_Dialog-maximize` });
        await maximize().click(); return;
      }
      if (text.includes('selected state equal to')) { await expect(maximize()).toHaveAttribute('aria-pressed', text.endsWith('true') ? 'true' : 'false'); return; }
      if (text.startsWith('USER-A clicks the chip labelled "Close"')) { await close().click(); return; }
      if (text.includes('User Profile') && text.endsWith('is hidden')) { await expect(dialog).toHaveCount(0); return; }
      if (text.startsWith('USER-A scrolls the tabpanel')) {
        const area = scrollArea(); await area.hover(); await page.mouse.wheel(0, 500); return;
      }
      if (text.startsWith('The workspace scroll offset')) { await expect.poll(() => scrollArea().evaluate(node => node.scrollTop)).toBeGreaterThan(scrollBefore); return; }
      throw new Error(`No dialog UX binding for ${id} step ${step.number}: ${text}`);
    });
  });
}
