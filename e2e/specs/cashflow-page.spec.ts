import { expect, test } from '@playwright/test';
import { CashflowBlotterPage } from '../pages/cashflow-blotter.page.js';

// Synthetic DOM mechanics. These cases do not execute the React application.
// Literal source identities intentionally remain independent from POM constants.
const tile = (content: string, prefix = 'fixture') =>
  `<section data-testid="${prefix}_Cashflow"><div class="kp--ratan_cashflow_blotter">${content}</div></section>`;
const idPrefix = '/cashflow_blotter_cn/cashflow_cn';

test('CF-PAGE-001: Given separate blotter tiles, When using page controls, Then only the selected tile changes', async ({ page }) => {
  const controls = `<div class="kp--quick_search"><div data-testid="cashflowIDSearch"><input></div>
      <button data-testid="${idPrefix}/quick_search/search_btn" onclick="this.dataset.clicked='true'">Search</button>
      <button data-testid="${idPrefix}/quick_search/clear_btn" onclick="this.dataset.clicked='true'">Clear Filters</button></div>
    <button data-testid="${idPrefix}/hide_search_bar_btn" onclick="this.dataset.clicked='true'">Hide Search Bar</button>
    <button data-testid="${idPrefix}/show_search_bar_btn" onclick="this.dataset.clicked='true'">Show Search Bar</button>
    <button data-testid="/advanced_search/entry_selector/setting_btn" onclick="this.dataset.clicked='true'">Create or Modify</button>
    <button data-testid="customView-create-modify-btn" onclick="this.dataset.clicked='true'">Create or Modify</button>
    <div data-testid="cashflow-export-file">
      <button data-testid="${idPrefix}/blotter/resize_btn" onclick="this.dataset.clicked='true'">Resize</button>
      <button data-testid="${idPrefix}/blotter/export_file_btn" onclick="this.dataset.clicked='true'">Export File</button></div>
    <div class="main-blotter-data-grid"><div class="ag-center-cols-container">
      <div role="row" row-id="CF-101"><div role="gridcell" col-id="Cashflow.Cashflow_Id">CF-101</div></div>
    </div></div>`;
  await page.setContent(tile(controls) + tile(controls, 'other'));
  const blotter = new CashflowBlotterPage(page, 'fixture');
  await blotter.expectVisible();
  await blotter.quickSearch.fillText('Cashflow ID', 'CF-101');
  await blotter.quickSearch.search();
  await blotter.quickSearch.clear();
  await blotter.hideSearchBar();
  await blotter.showSearchBar();
  await blotter.openCustomSearch();
  await blotter.openViewBuilder();
  await blotter.resizeColumns();
  await blotter.openExport();
  await expect(blotter.quickSearch.input('Cashflow ID')).toHaveValue('CF-101');
  await expect(blotter.root.locator('[data-clicked="true"]')).toHaveCount(8);
  await expect(page.getByTestId('other_Cashflow').locator('[data-clicked]')).toHaveCount(0);
  await expect(page.getByTestId('other_Cashflow').locator('input')).toHaveValue('');
  await blotter.grid.expectCellText('CF-101', 'Cashflow.Cashflow_Id', 'CF-101');
});

test('CF-PAGE-002: Given conditional search fields, When switching each variant, Then only the active field accepts input', async ({ page }) => {
  await page.setContent(tile(`<div class="kp--quick_search">
    <div data-testid="dynamickLabel" id="trade"><label onmouseenter="document.querySelector('#trade-menu').hidden=false">Trade ID</label><input data-testid="tradeIDSearch"></div>
    <div data-testid="dynamickLabel" id="counterparty"><label onmouseenter="document.querySelector('#counterparty-menu').hidden=false">Counterparty FMCODE</label><input data-testid="counterpartyFMCODESearch"></div>
    <div data-testid="dynamickLabel" id="entity"><label onmouseenter="document.querySelector('#entity-menu').hidden=false">SCB Booking Entity</label><input data-testid="sCBBookingEntitySearch"></div>
    </div>`) + `
    <div id="trade-menu" role="menu" hidden><div role="menuitem" onclick="swap('trade','Original Trade ID','originalTradeIDSearch');this.parentElement.hidden=true">Original Trade ID</div></div>
    <div id="counterparty-menu" role="menu" hidden><div role="menuitem" onclick="swap('counterparty','Counterparty FMID','counterpartyFMIDSearch');this.parentElement.hidden=true">Counterparty FMID</div></div>
    <div id="entity-menu" role="menu" hidden><div role="menuitem" onclick="swap('entity','SCB Booking Entity FMID','sCBBookingEntityFMIDSearch');this.parentElement.hidden=true">SCB Booking Entity FMID</div></div>
    <script>function swap(id,label,testId){const root=document.getElementById(id);root.querySelector('label').textContent=label;root.querySelector('input').setAttribute('data-testid',testId);}</script>`);
  const blotter = new CashflowBlotterPage(page, 'fixture');
  await blotter.quickSearch.fillText('Trade ID', 'TR-101');
  await blotter.quickSearch.chooseVariant('trade', 'Original Trade ID');
  await blotter.quickSearch.fillText('Original Trade ID', 'ORIG-101');
  await blotter.quickSearch.chooseVariant('counterparty', 'Counterparty FMID');
  await blotter.quickSearch.fillText('Counterparty FMID', 'CP-101');
  await blotter.quickSearch.chooseVariant('bookingEntity', 'SCB Booking Entity FMID');
  await blotter.quickSearch.fillText('SCB Booking Entity FMID', 'BE-101');
  await expect(blotter.quickSearch.control('Trade ID')).toHaveCount(0);
  await expect(blotter.quickSearch.input('Original Trade ID')).toHaveValue('ORIG-101');
  await expect(blotter.quickSearch.input('Counterparty FMID')).toHaveValue('CP-101');
  await expect(blotter.quickSearch.input('SCB Booking Entity FMID')).toHaveValue('BE-101');
  await expect(blotter.quickSearch.chooseVariant('trade', 'Unknown')).rejects.toThrow('Unknown trade field variant');
});

test('CF-PAGE-003: Given conditional amount inputs, When choosing each operator, Then the matching amount fields hold the values', async ({ page }) => {
  await page.setContent(tile(`<div class="kp--quick_search"><div data-testid="dynamickLabel" id="amount">
    <label onmouseenter="document.querySelector('#amount-menu').hidden=false">Amount Range (Is)</label><span id="amount-inputs"><input data-testid="amountValueEQ"></span>
    </div></div>`) + `<div id="amount-menu" role="menu" hidden>
    <div role="menuitem" onclick="amount('Is')">Amount Range (Is)</div>
    <div role="menuitem" onclick="amount('Between')">Amount Range (Between)</div>
    <div role="menuitem" onclick="amount('Greater Than')">Amount Range (Greater Than)</div>
    <div role="menuitem" onclick="amount('Less Than')">Amount Range (Less Than)</div></div>
    <script>function amount(mode){document.querySelector('#amount label').textContent='Amount Range ('+mode+')';document.getElementById('amount-inputs').innerHTML=mode==='Between'?'<input data-testid="amountStart"><input data-testid="amountEnd">':'<input data-testid="'+(mode==='Is'?'amountValueEQ':'amountValueLaterOrBefore')+'">';document.getElementById('amount-menu').hidden=true;}</script>`);
  const search = new CashflowBlotterPage(page, 'fixture').quickSearch;
  await search.setAmount('is', '20');
  await expect(search.amount.is).toHaveValue('20');
  await search.setAmount('between', '10', '30');
  await expect(search.amount.minimum).toHaveValue('10');
  await expect(search.amount.maximum).toHaveValue('30');
  await expect(search.setAmount('between', '5')).rejects.toThrow('requires minimum and maximum');
  await expect(search.amount.minimum).toHaveValue('10');
  await search.setAmount('greaterThan', '40');
  await expect(search.amount.comparison).toHaveValue('40');
  await expect(search.amount.minimum).toHaveCount(0);
  await search.setAmount('lessThan', '50');
  await expect(search.amount.comparison).toHaveValue('50');
  await search.setAmount('is', '60');
  await expect(search.amount.is).toHaveValue('60');
});

test('CF-PAGE-004: Given repeated quick-filter options, When choosing a filter, Then its associated popup receives the selection', async ({ page }) => {
  const fields = [
    ['Value Date Horizon', 'quickFilterDays'], ['Product Taxonomy', 'quickFilterTaxonomy'],
    ['NSTP Exception', 'quickFilterNstpException'], ['Booking Entity', 'quickFilterBookingEntity'],
    ['Cashflow State', 'quickFilterCashflowStatus'], ['Cashflow Sub State', 'quickFilterSubStatus'],
    ['Cashflow Sub State Type', 'quickFilterSubStatusType'], ['Settlement Method', 'quickFilterSettlementMethod'],
    ['Bic Net Flag', 'quickFilterBicNet'],
  ] as const;
  await page.setContent(tile(fields.map(([, id], i) =>
    `<div data-testid="${id}"><input role="combobox" aria-controls="options-${i}"></div>`).join('')) +
    fields.map(([,], i) => `<div id="options-${i}" role="listbox"><div role="option" onclick="this.dataset.selected='true'">Synthetic option</div></div>`).join(''));
  const blotter = new CashflowBlotterPage(page, 'fixture');
  for (const [name] of fields) await expect(blotter.quickFilter(name)).toHaveCount(1);
  await blotter.chooseQuickFilter('Cashflow State', 'Synthetic option');
  await expect(page.locator('#options-4 [role="option"]')).toHaveAttribute('data-selected', 'true');
  await expect(page.locator('[role="option"][data-selected]')).toHaveCount(1);
});

test('CF-PAGE-005: Given load-size settings, When selecting a new size, Then the footer uses that size and skips a repeated selection', async ({ page }) => {
  await page.setContent(tile(`<div data-testid="cashflow-export-file">
      <button id="load-next" data-testid="${idPrefix}/blotter/auto_load_next_btn" onclick="this.dataset.clicked='true'">Load next 1000</button>
      <div class="load-next-settings" onmouseenter="document.querySelector('#load-menu').hidden=false"><span role="img" aria-label="setting">Settings</span></div>
    </div>`) + `<div id="load-menu" role="menu" hidden><div role="menuitem" onclick="document.getElementById('load-next').textContent='Load next 5000';this.parentElement.remove()">set size to 5000</div></div>`);
  const blotter = new CashflowBlotterPage(page, 'fixture');
  await blotter.setLoadSize(5000);
  await expect(blotter.loadNextButton).toHaveText('Load next 5000');
  await expect(page.locator('#load-menu')).toHaveCount(0);
  await blotter.setLoadSize(5000);
  await blotter.loadNext();
  await expect(blotter.loadNextButton).toHaveAttribute('data-clicked', 'true');
});

test('CF-PAGE-006: Given preset counters and a portalled notification, When activating them, Then their exact identities select the intended controls', async ({ page }) => {
  const presetIds = ['value_today_pending_operator','value_today_pending_verification','value_tmr_pending_operator','value_tmr_pending_verification'];
  await page.setContent(tile(presetIds.map(id => `<button data-testid="${idPrefix}/preset_query_count/${id}" onclick="this.dataset.clicked='true'">Pending</button>`).join('')) +
    `<div role="alert"><button data-testid="${idPrefix}/notification_reconnect_btn" onclick="this.dataset.clicked='true'">Reconnect</button></div>`);
  const blotter = new CashflowBlotterPage(page, 'fixture');
  await blotter.controls.click(blotter.preset('today', 'operator'));
  await blotter.controls.click(blotter.preset('nextBusinessDay', 'verification'));
  await expect(blotter.preset('today', 'operator')).toHaveAttribute('data-clicked', 'true');
  await expect(blotter.preset('nextBusinessDay', 'verification')).toHaveAttribute('data-clicked', 'true');
  await expect(blotter.preset('today', 'verification')).not.toHaveAttribute('data-clicked');
  await expect(blotter.preset('nextBusinessDay', 'operator')).not.toHaveAttribute('data-clicked');
  await blotter.reconnectNotifications();
  await expect(blotter.notificationReconnectButton).toHaveAttribute('data-clicked', 'true');
});
