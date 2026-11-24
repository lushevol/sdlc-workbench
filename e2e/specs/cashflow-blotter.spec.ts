import { expect, test } from '@playwright/test';
import { CashflowControlScope } from '../components/cashflow/control-scope.js';
import { CashflowDataGrid } from '../components/cashflow/data-grid.component.js';
import { CashflowSearchBuilder, CashflowViewBuilder } from '../components/cashflow/builders.js';

// Canonical harness cases. These source-shaped fixtures verify POM mechanics only.
// They do not execute the React application or submit business transactions.
test('CF-POM-001: Given duplicate outer fields, When filling wrapped and native fields, Then only the scoped fields change', async ({ page }) => {
  await page.setContent(`<input data-testid="cashflowIDSearch" value="outside">
    <section id="cashflow"><div data-testid="cashflowIDSearch"><input></div>
    <input data-testid="amountStart"><textarea data-testid="comment"></textarea></section>`);
  const controls = new CashflowControlScope(page, page.locator('#cashflow'));
  await controls.fill(controls.field('cashflowIDSearch'), 'CF-101');
  await controls.fill(controls.field('amountStart'), '25.50');
  await controls.fill(controls.field('comment'), 'Synthetic comment');
  await expect(controls.field('cashflowIDSearch')).toHaveValue('CF-101');
  await expect(controls.field('amountStart')).toHaveValue('25.50');
  await expect(controls.field('comment')).toHaveValue('Synthetic comment');
  await expect(page.locator('body > input')).toHaveValue('outside');
});

test('CF-POM-002: Given two portalled lists, When selecting a quick filter, Then only its associated option is selected', async ({ page }) => {
  await page.setContent(`<section id="cashflow"><div data-testid="quickFilterCurrency">
    <input role="combobox" aria-controls="currency-options" aria-expanded="true"></div></section>
    <div id="unrelated" role="listbox"><div role="option" onclick="this.dataset.selected='true'">USD</div></div>
    <div id="currency-options" role="listbox"><div role="option" onclick="this.dataset.selected='true'">USD</div></div>`);
  const controls = new CashflowControlScope(page, page.locator('#cashflow'));
  await controls.selectOption(controls.combobox('quickFilterCurrency'), 'USD');
  await expect(page.locator('#currency-options [role=option]')).toHaveAttribute('data-selected', 'true');
  await expect(page.locator('#unrelated [role=option]')).not.toHaveAttribute('data-selected');
});

test('CF-POM-003: Given an unassociated popup, When selecting an option, Then selection requires an explicit popup scope', async ({ page }) => {
  await page.setContent(`<section id="cashflow"><input role="combobox"></section>
    <div id="options" role="listbox"><div role="option" onclick="this.dataset.selected='true'">CSV</div></div>`);
  const controls = new CashflowControlScope(page, page.locator('#cashflow'));
  const combo = controls.root.getByRole('combobox');
  await expect(controls.selectOption(combo, 'CSV')).rejects.toThrow('no associated popup');
  await expect(page.getByRole('option')).not.toHaveAttribute('data-selected');
  await controls.selectOption(combo, 'CSV', page.locator('#options'));
  await expect(page.getByRole('option')).toHaveAttribute('data-selected', 'true');
});

test('CF-POM-004: Given disabled or ambiguous controls, When clicking, Then no matching handler executes', async ({ page }) => {
  test.setTimeout(15_000);
  await page.setContent(`<section id="cashflow"><button disabled onclick="this.dataset.clicked='true'">Submit</button>
    <button onclick="this.dataset.clicked='true'">Close</button><button onclick="this.dataset.clicked='true'">Close</button></section>`);
  const controls = new CashflowControlScope(page, page.locator('#cashflow'));
  await expect(controls.click(controls.button('Submit'))).rejects.toThrow();
  await expect(controls.click(controls.button('Close'))).rejects.toThrow();
  await expect(controls.root.locator('[data-clicked]')).toHaveCount(0);
});

test('CF-POM-005: Given pinned row fragments, When selecting and reading a cashflow, Then stable row and column keys identify the controls', async ({ page }) => {
  await page.setContent(`<section id="grid"><div role="grid">
    <div role="columnheader" col-id="Cashflow.Amount" aria-sort="none" onclick="this.setAttribute('aria-sort','ascending')">Amount</div>
    <div class="ag-pinned-left-cols-container"><div role="row" row-id="CF-101"><input type="checkbox"></div></div>
    <div class="ag-center-cols-container"><div role="row" row-id="CF-101"><div role="gridcell" col-id="Cashflow.Amount">25.50</div></div>
    <div role="row" row-id="CF-102"><div role="gridcell" col-id="Cashflow.Amount">99.00</div></div></div></div></section>`);
  const grid = new CashflowDataGrid(page, page.locator('#grid'));
  await grid.selectRow('CF-101');
  await expect(grid.rowCheckbox('CF-101')).toBeChecked();
  await expect(grid.row('CF-101', 'left')).toHaveCount(1);
  await grid.expectCellText('CF-101', 'Cashflow.Amount', '25.50');
  await grid.sortColumn('Cashflow.Amount');
  await grid.expectSort('Cashflow.Amount', 'ascending');
  await expect(grid.row('missing-cashflow')).toHaveCount(0);
});

test('CF-POM-006: Given special identifier characters, When locating a cashflow cell, Then CSS characters remain literal', async ({ page }) => {
  await page.setContent('<section id="grid"><div role="row"><div role="gridcell">literal</div></div></section>');
  const id = 'CF-"\\[1]';
  await page.getByRole('row').evaluate((el, value) => el.setAttribute('row-id', value), id);
  await page.getByRole('gridcell').evaluate((el, value) => el.setAttribute('col-id', value), id);
  const grid = new CashflowDataGrid(page, page.locator('#grid'));
  await grid.expectCellText(id, id, 'literal');
});

test('CF-POM-007: Given repeated query editors, When editing one explicit rule, Then adjacent rule values remain unchanged', async ({ page }) => {
  await page.setContent(`<div role="dialog" aria-label="Custom Search"><header class="MuiDialogTitle-root"><div class="MuiGrid-item">Custom Search</div></header><label>Filter Name<input></label>
    <button data-testid="new-filter-btn">+ New Filter</button>
    <div class="queryBuilder"><div class="ruleGroup"><div class="ruleGroup-header"><button class="ruleGroup-addRule">+ Rule</button></div>
    <div class="ruleGroup-body"><div class="rule"><input data-testid="text-input" value="first"></div>
    <div class="rule"><input data-testid="text-input" value="second"></div></div></div></div></div>`);
  const builder = new CashflowSearchBuilder(page);
  await builder.fill(builder.filterName, 'Synthetic filter');
  const rule = builder.query.ruleAt(1);
  await rule.fill(rule.textValue, 'CF-101');
  await expect(builder.query.ruleAt(0).textValue).toHaveValue('first');
  await expect(rule.textValue).toHaveValue('CF-101');
  expect(() => builder.query.ruleAt(-1)).toThrow('nonnegative integer');
});

test('CF-POM-008: Given identical view and query role selectors, When editing a view, Then controls stay within View Builder', async ({ page }) => {
  await page.setContent(`<div role="dialog" aria-label="Custom Search"><input data-testid="viewName" value="outside"></div>
    <div role="dialog" aria-label="View Builder"><header class="MuiDialogTitle-root"><div class="MuiGrid-item">View Builder</div></header><input data-testid="viewName">
    <label><input type="checkbox">Is Private</label><div class="result-data">
    <li data-rbd-draggable-id="Cashflow.Amount"><button title="Delete" onclick="this.parentElement.remove()"></button>Amount</li></div></div>`);
  const builder = new CashflowViewBuilder(page);
  await builder.fill(builder.viewName, 'Synthetic view');
  await builder.check(builder.privateCheckbox);
  await builder.click(builder.removeFieldButton('Cashflow.Amount'));
  await expect(builder.viewName).toHaveValue('Synthetic view');
  await expect(builder.displayedField('Cashflow.Amount')).toHaveCount(0);
  await expect(page.getByRole('dialog', { name: 'Custom Search' }).getByTestId('viewName')).toHaveValue('outside');
});

test('CF-POM-009: Given hidden upload input and export link, When transferring synthetic files, Then filenames and download bytes match', async ({ page }) => {
  await page.setContent(`<section id="cashflow"><input type="file" hidden>
    <a download="cashflows.csv" href="data:text/csv,id%0ACF-101">Download</a></section>`);
  const controls = new CashflowControlScope(page, page.locator('#cashflow'));
  const upload = controls.root.locator('input[type=file]');
  await controls.upload(upload, { name: 'cashflows.xlsx', mimeType: 'application/octet-stream', buffer: Buffer.from('synthetic') });
  expect(await upload.evaluate((el: HTMLInputElement) => el.files?.length)).toBe(1);
  expect(await upload.evaluate((el: HTMLInputElement) => el.files?.[0]?.name)).toBe('cashflows.xlsx');
  const download = await controls.download(controls.link('Download'));
  expect(download.suggestedFilename()).toBe('cashflows.csv');
  const stream = await download.createReadStream();
  if (!stream) throw new Error('Synthetic download has no readable stream.');
  const chunks: Buffer[] = [];
  for await (const chunk of stream) chunks.push(Buffer.from(chunk));
  expect(Buffer.concat(chunks).toString()).toBe('id\nCF-101');
});

test('CF-POM-014: Given virtual AntD options, When selecting a currency, Then the associated visible item receives the click', async ({ page }) => {
  await page.setContent(`<section id="cashflow"><input role="combobox" aria-controls="virtual-options"></section>
    <div class="ant-select-dropdown"><div id="virtual-options" role="listbox" style="height:0;width:0;overflow:hidden">
    <div role="option">USD</div></div><div class="ant-select-item-option" onclick="this.dataset.selected='true'">USD</div></div>
    <div class="ant-select-dropdown"><div class="ant-select-item-option" onclick="this.dataset.selected='true'">USD</div></div>`);
  const controls = new CashflowControlScope(page, page.locator('#cashflow'));
  await controls.selectOption(controls.root.getByRole('combobox'), 'USD');
  await expect(page.locator('.ant-select-item-option[data-selected]')).toHaveCount(1);
  await expect(page.locator('.ant-select-dropdown').filter({ has: page.locator('#virtual-options') })
    .locator('.ant-select-item-option')).toHaveAttribute('data-selected', 'true');
});

test('CF-POM-015: Given a switch already enabled, When setting it enabled twice, Then no toggle occurs', async ({ page }) => {
  await page.setContent(`<section id="cashflow"><button role="switch" aria-checked="true"
    onclick="this.setAttribute('aria-checked',this.getAttribute('aria-checked')==='true'?'false':'true');this.dataset.clicked='true'">Enabled</button></section>`);
  const controls = new CashflowControlScope(page, page.locator('#cashflow'));
  const toggle = controls.root.getByRole('switch');
  await controls.setSwitch(toggle, true);
  await controls.setSwitch(toggle, true);
  await expect(toggle).not.toHaveAttribute('data-clicked');
  await controls.setSwitch(toggle, false);
  await expect(toggle).toHaveAttribute('aria-checked', 'false');
});
