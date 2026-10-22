# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: dialog-ux.spec.ts >> UX-033 actual dialog boundaries with step evidence
- Location: e2e/audit-specs/dialog-ux.spec.ts:14:3

# Error details

```
Error: expect(locator).toBeInViewport() failed

Locator:  locator('[role="dialog"]:visible').filter({ has: getByText('Fixture Dialog', { exact: true }) }).getByText('Fixture Dialog', { exact: true })
Expected: in viewport
Received: viewport ratio 0
Timeout:  5000ms

Call log:
  - Expect "toBeInViewport" locator('[role="dialog"]:visible').filter({ has: getByText('Fixture Dialog', { exact: true }) }).getByText('Fixture Dialog', { exact: true }) with timeout 5000ms
  - waiting for locator('[role="dialog"]:visible').filter({ has: getByText('Fixture Dialog', { exact: true }) }).getByText('Fixture Dialog', { exact: true })
    14 × locator resolved to <div class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-8 css-vok43g-MuiGrid-root">Fixture Dialog</div>
       - unexpected value "viewport ratio 0"

```

# Page snapshot

```yaml
- generic [ref=f1e4]:
  - generic [ref=f1e10]:
    - generic [ref=f1e11] [cursor=pointer]: New Tile
    - generic [ref=f1e19]:
      - text: dark
      - checkbox [ref=f1e22] [cursor=pointer]
    - group [ref=f1e26]:
      - generic [ref=f1e27]: 06:08 UTC
      - checkbox [checked] [ref=f1e30] [cursor=pointer]
    - button [ref=f1e34] [cursor=pointer]:
      - generic [ref=f1e35]: A
    - button [ref=f1e37] [cursor=pointer]
  - main [ref=f1e41]:
    - tablist [ref=f1e45]:
      - tab [selected] [ref=f1e47] [cursor=pointer]:
        - region [ref=f1e48]:
          - textbox [ref=f1e52]: Workspace 1
      - button [ref=f1e54] [cursor=pointer]
    - tabpanel [ref=f1e59]:
      - generic [ref=f1e61]:
        - paragraph [ref=f1e62]: /tile-global
        - dialog [ref=f1e65]:
          - heading [level=2] [ref=f1e66]:
            - generic [ref=f1e67]:
              - generic [ref=f1e68]: Fixture Dialog
              - generic [ref=f1e69]:
                - button [ref=f1e70] [cursor=pointer]: Maximize
                - button [ref=f1e73] [cursor=pointer]:
                  - generic [ref=f1e74]: Close
          - generic [ref=f1e77]:
            - generic [ref=f1e78]: Scrollable fixture content
            - paragraph [ref=f1e79]: CONTENT-END
          - button [ref=f1e80]
```

# Test source

```ts
  1  | import { test, expect } from '../support/audit-fixture.js';
  2  | import { loginCatalog, type CatalogApp } from '../support/catalog-app.js';
  3  | import { localPrefix } from '../support/local-app.js';
  4  | 
  5  | test.use({ auditScope: 'ACTUAL_APPLICATION_LOCAL_SERVICES',
  6  |   auditFixture: 'Actual portal Profile and exported Dialog components. A controlled SystemJS module supplies the declared isolated dialog or scrollable content. This run checks component behavior; the fixture content is not business output.' });
  7  | 
  8  | const moduleText = (dialog: boolean) => `System.register(['react','@fm/base'],function(exports){var React,base;return{setters:[function(v){React=v.default||v;},function(v){base=v;}],execute:function(){exports('default',function(props){var open=React.useState(true);return React.createElement('section',{'data-testid':'audit-controlled-container'},React.createElement('p',{'data-testid':'fixture-tile-route'},props.tile),${dialog
  9  |   ? "React.createElement(base.Dialog.default,{open:open[0],onClose:function(){open[1](false);},isDraggable:true,isResizeble:true,disablePortal:true,defaultWidth:700,defaultHeight:600,titleComponents:'Fixture Dialog'},React.createElement('div',{style:{height:'1600px'}},'Scrollable fixture content'),React.createElement('p',null,'CONTENT-END'))"
  10 |   : "React.createElement('div',{style:{height:'1800px'}},'Scrollable fixture content'),React.createElement('p',null,'CONTENT-END')"});});}};});`;
  11 | 
  12 | for (const number of [32, 33, 34, 35]) {
  13 |   const id = `UX-${String(number).padStart(3, '0')}`;
  14 |   test(`${id} actual dialog boundaries with step evidence`, async ({ page, audit }) => {
  15 |     const steps = await audit.defineCase(id);
  16 |     let app: CatalogApp;
  17 |     let scrollBefore = 0;
  18 |     const isolated = number === 33 || number === 34;
  19 |     const dialog = page.locator('[role="dialog"]:visible').filter({ has: page.getByText(isolated ? 'Fixture Dialog' : 'User Profile', { exact: true }) });
  20 |     const close = () => dialog.getByTestId(`${localPrefix}_Dialog-close`);
  21 |     const maximize = () => dialog.getByTestId(`${localPrefix}_Dialog-maximize`);
  22 |     const scrollArea = () => page.locator('[role="tabpanel"]:visible .tabmain');
  23 |     for (const step of steps) await audit.step(step.number, async () => {
  24 |       const text = step.text;
  25 |       if (step.number === 1) {
  26 |         await page.setViewportSize({ width: 1366, height: 768 });
  27 |         app = await loginCatalog(page, { occupied: true });
  28 |         if (number !== 32) {
  29 |           await page.route('**/audit-fixtures/test-container.js', route => route.fulfill({ status: 200, contentType: 'application/javascript', body: moduleText(isolated) }));
  30 |           await page.reload({ waitUntil: 'domcontentloaded' }); await app.portal.expectVisible();
  31 |           await expect(page.getByTestId('fixture-tile-route')).toBeVisible();
  32 |         }
  33 |         if (!isolated) { await app.portal.clickAvatarButton(); await app.openProfile(); }
  34 |         await expect(dialog).toBeVisible();
  35 |         if (number === 35) { scrollBefore = await scrollArea().evaluate(node => node.scrollTop); await audit.record('workspace-scroll-fixture', { fixtureId: 'WS-SCROLL', locator: '[role=tabpanel]:visible .tabmain', scrollBefore }); }
  36 |         return;
  37 |       }
  38 |       if (text.includes('changes the viewport')) { await page.setViewportSize({ width: 768, height: 600 }); return; }
  39 |       if (text.includes('visible title text')) { await expect(dialog.getByText('User Profile', { exact: true })).toBeVisible(); return; }
  40 |       if (text.includes('drags the text labelled')) {
  41 |         const header = dialog.getByTestId(`${localPrefix}_Dialog-header`);
  42 |         const box = await dialog.boundingBox(), title = await header.boundingBox(); expect(box).toBeTruthy(); expect(title).toBeTruthy();
  43 |         const x = title!.x + 60, y = title!.y + 12;
  44 |         await page.mouse.move(x, y); await page.mouse.down(); await page.mouse.move(x - box!.x, y - box!.y, { steps: 20 }); await page.mouse.up();
  45 |         await audit.record('dialog-drag', { before: box, after: await dialog.boundingBox(), targetTopLeft: { x: 0, y: 0 } }); return;
  46 |       }
  47 |       if (text.includes('drags the icon button')) {
  48 |         const target = dialog.getByTestId(`${localPrefix}_Dialog-resize`); const box = await target.boundingBox(); expect(box).toBeTruthy();
  49 |         const x = box!.x + box!.width / 2, y = box!.y + box!.height / 2;
  50 |         await page.mouse.move(x, y); await page.mouse.down(); await page.mouse.move(x - 800, y - 800, { steps: 20 }); await page.mouse.up();
  51 |         await audit.record('dialog-resize', { pointerStart: { x, y }, pointerEnd: { x: x - 800, y: y - 800 }, dialog: await dialog.boundingBox() }); return;
  52 |       }
  53 |       if (text.includes('CONTENT-END') && text.includes('reachable')) { const marker = dialog.getByText('CONTENT-END', { exact: true }); await marker.scrollIntoViewIfNeeded(); await expect(marker).toBeInViewport(); return; }
> 54 |       if (text.includes('Fixture Dialog') && text.includes('visible and reachable')) { await expect(dialog.getByText('Fixture Dialog', { exact: true })).toBeInViewport(); return; }
     |                                                                                                                                                          ^ Error: expect(locator).toBeInViewport() failed
  55 |       if (text.includes('Close') && (text.includes('visible and enabled') || text.includes('visible and reachable'))) {
  56 |         await close().scrollIntoViewIfNeeded(); await expect(close()).toBeInViewport(); await expect(close()).toBeEnabled(); return;
  57 |       }
  58 |       if (text.startsWith('USER-A clicks the button labelled "Maximize"')) {
  59 |         await audit.record('source-resolved-maximize-target', { canonicalName: 'Maximize', actualAccessibleName: 'resize', testId: `${localPrefix}_Dialog-maximize` });
  60 |         await maximize().click(); return;
  61 |       }
  62 |       if (text.includes('selected state equal to')) { await expect(maximize()).toHaveAttribute('aria-pressed', text.endsWith('true') ? 'true' : 'false'); return; }
  63 |       if (text.startsWith('USER-A clicks the chip labelled "Close"')) { await close().click(); return; }
  64 |       if (text.includes('User Profile') && text.endsWith('is hidden')) { await expect(dialog).toHaveCount(0); return; }
  65 |       if (text.startsWith('USER-A scrolls the tabpanel')) {
  66 |         const area = scrollArea(); await area.hover(); await page.mouse.wheel(0, 500); return;
  67 |       }
  68 |       if (text.startsWith('The workspace scroll offset')) { await expect.poll(() => scrollArea().evaluate(node => node.scrollTop)).toBeGreaterThan(scrollBefore); return; }
  69 |       throw new Error(`No dialog UX binding for ${id} step ${step.number}: ${text}`);
  70 |     });
  71 |   });
  72 | }
  73 | 
```