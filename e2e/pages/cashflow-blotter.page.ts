import { expect, type Locator, type Page } from '@playwright/test';
import { CashflowControlScope } from '../components/cashflow/control-scope.js';
import { CashflowDataGrid } from '../components/cashflow/data-grid.component.js';
import { CashflowDialogs } from '../components/cashflow/dialogs.js';
import { CashflowSearchBuilder, CashflowViewBuilder } from '../components/cashflow/builders.js';
import { requireIdentifier } from '../catalog/ui-contracts.js';

/** Source identities: e2e/traceability/cashflow-main-inventory.json. */
export const cashflowTestIdPrefix = '/cashflow_blotter_cn/cashflow_cn';

export const cashflowQuickSearchFields = {
  'Cashflow ID': 'cashflowIDSearch',
  'Trade ID': 'tradeIDSearch',
  'Original Trade ID': 'originalTradeIDSearch',
  'Value Date Range': 'valueDateRangeSearch',
  Currency: 'currencyAutoComplete',
  'Product Taxonomy': 'productTaxonomySearch',
  'Counterparty FMCODE': 'counterpartyFMCODESearch',
  'Counterparty FMID': 'counterpartyFMIDSearch',
  'SCB Booking Entity': 'sCBBookingEntitySearch',
  'SCB Booking Entity FMID': 'sCBBookingEntityFMIDSearch',
  'Beneficiary Name': 'beneficiaryNameSearch',
  'Beneficiary Account BIC Code': 'beneficiaryAccountBICCodeSearch',
  'Cashflow State': 'cashflowStateSearch',
  'Cashflow Sub State': 'cashflowSubStateSearch',
} as const;
export type CashflowQuickSearchField = keyof typeof cashflowQuickSearchFields;

export const cashflowQuickFilterIds = {
  'Value Date Horizon': 'quickFilterDays',
  'Product Taxonomy': 'quickFilterTaxonomy',
  'NSTP Exception': 'quickFilterNstpException',
  'Booking Entity': 'quickFilterBookingEntity',
  'Cashflow State': 'quickFilterCashflowStatus',
  'Cashflow Sub State': 'quickFilterSubStatus',
  'Cashflow Sub State Type': 'quickFilterSubStatusType',
  'Settlement Method': 'quickFilterSettlementMethod',
  'Bic Net Flag': 'quickFilterBicNet',
} as const;
export type CashflowQuickFilter = keyof typeof cashflowQuickFilterIds;

export const cashflowAmountModes = {
  is: 'Amount Range (Is)',
  between: 'Amount Range (Between)',
  greaterThan: 'Amount Range (Greater Than)',
  lessThan: 'Amount Range (Less Than)',
} as const;

const dynamicFieldVariants = {
  trade: ['Trade ID', 'Original Trade ID'],
  counterparty: ['Counterparty FMCODE', 'Counterparty FMID'],
  bookingEntity: ['SCB Booking Entity', 'SCB Booking Entity FMID'],
  amount: Object.values(cashflowAmountModes),
} as const;

const exactText = (text: string) => new RegExp(`^${text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`);

export class CashflowQuickSearch extends CashflowControlScope {
  readonly searchButton: Locator;
  readonly clearButton: Locator;
  readonly amount: Readonly<Record<'is' | 'comparison' | 'minimum' | 'maximum', Locator>>;

  constructor(page: Page, root: Locator) {
    super(page, root);
    this.searchButton = root.getByTestId(`${cashflowTestIdPrefix}/quick_search/search_btn`);
    this.clearButton = root.getByTestId(`${cashflowTestIdPrefix}/quick_search/clear_btn`);
    this.amount = {
      is: this.field('amountValueEQ'),
      comparison: this.field('amountValueLaterOrBefore'),
      minimum: this.field('amountStart'),
      maximum: this.field('amountEnd'),
    };
  }

  control(name: CashflowQuickSearchField): Locator {
    return this.root.getByTestId(cashflowQuickSearchFields[name]);
  }

  input(name: CashflowQuickSearchField): Locator {
    return this.field(cashflowQuickSearchFields[name]);
  }

  /** Many-in-one fields render only their active variant. */
  variantSelector(group: keyof typeof dynamicFieldVariants): Locator {
    const names = dynamicFieldVariants[group];
    const label = this.page.locator('label').filter({
      hasText: new RegExp(`^(?:${names.map(name => exactText(name).source.slice(1, -1)).join('|')})$`),
    });
    return this.root.getByTestId('dynamickLabel').filter({ has: label }).locator('label');
  }

  async chooseVariant(group: keyof typeof dynamicFieldVariants, label: string): Promise<void> {
    if (!(dynamicFieldVariants[group] as readonly string[]).includes(label)) {
      throw new Error(`Unknown ${group} field variant: ${label}`);
    }
    const selector = this.variantSelector(group);
    await expect(this.root).toHaveCount(1);
    await expect(this.root).toBeVisible();
    await expect(selector).toHaveCount(1);
    await expect(selector).toBeVisible();
    if ((await selector.innerText()).trim() === label) return;
    // Ant Design renders this menu in a portal outside the quick-search root.
    await selector.hover();
    const option = this.page.getByRole('menuitem', { name: label, exact: true }).filter({ visible: true });
    await expect(option).toHaveCount(1);
    await expect(option).toBeVisible();
    await expect(option).toBeEnabled();
    await expect(option).not.toHaveAttribute('aria-disabled', 'true');
    await option.click();
  }

  async fillText(name: CashflowQuickSearchField, value: string): Promise<void> {
    await this.fill(this.input(name), value);
  }

  async chooseValue(name: CashflowQuickSearchField, value: string, popup?: Locator): Promise<void> {
    await this.selectOption(this.combobox(cashflowQuickSearchFields[name]), value, popup);
  }

  async setAmount(mode: keyof typeof cashflowAmountModes, value: string, maximum?: string): Promise<void> {
    if (mode === 'between' && maximum === undefined) throw new Error('Between requires minimum and maximum amounts.');
    await this.chooseVariant('amount', cashflowAmountModes[mode]);
    if (mode === 'between') {
      await this.fill(this.amount.minimum, value);
      await this.fill(this.amount.maximum, maximum!);
    } else {
      await this.fill(mode === 'is' ? this.amount.is : this.amount.comparison, value);
    }
  }

  async setDateRange(start: string, end: string): Promise<void> {
    const picker = this.control('Value Date Range');
    const inputs = picker.locator('input');
    await expect(picker).toHaveCount(1);
    await expect(inputs).toHaveCount(2);
    await this.fill(inputs.nth(0), start);
    await this.press(inputs.nth(0), 'Enter');
    await this.fill(inputs.nth(1), end);
    await this.press(inputs.nth(1), 'Enter');
  }

  async search(): Promise<void> { await this.click(this.searchButton); }
  async clear(): Promise<void> { await this.click(this.clearButton); }
}

/** Composes the CN blotter. Conditional controls remain explicit locators. */
export class CashflowBlotterPage {
  readonly root: Locator;
  readonly controls: CashflowControlScope;
  readonly quickSearch: CashflowQuickSearch;
  readonly quickFilters: CashflowControlScope;
  readonly footer: CashflowControlScope;
  readonly grid: CashflowDataGrid;
  readonly dialogs: CashflowDialogs;
  readonly searchBuilder: CashflowSearchBuilder;
  readonly viewBuilder: CashflowViewBuilder;
  readonly hideSearchBarButton: Locator;
  readonly showSearchBarButton: Locator;
  readonly loadNextButton: Locator;
  readonly loadNextSettings: Locator;
  readonly resizeButton: Locator;
  readonly exportButton: Locator;
  readonly uploadButton: Locator;
  readonly clearGridFiltersButton: Locator;
  readonly clearQuickFiltersButton: Locator;
  readonly resultsAlert: Locator;
  readonly savedFilter: Locator;
  readonly clearSavedFilterButton: Locator;
  readonly createOrModifyFilterButton: Locator;
  readonly savedView: Locator;
  readonly clearSavedViewButton: Locator;
  readonly createOrModifyViewButton: Locator;
  readonly notificationReconnectButton: Locator;

  /** Supply an instance root when several tiles share the same build prefix. */
  constructor(readonly page: Page, prefix: string, instanceRoot?: Locator) {
    requireIdentifier(prefix, 'MFE_APP_PREFIX_STYLE');
    this.root = (instanceRoot ?? page.getByTestId(`${prefix}_Cashflow`))
      .locator('.kp--ratan_cashflow_blotter');
    this.controls = new CashflowControlScope(page, this.root);
    this.quickSearch = new CashflowQuickSearch(page, this.root.locator('.kp--quick_search'));
    this.quickFilters = this.controls;
    this.footer = new CashflowControlScope(page, this.root.getByTestId('cashflow-export-file'));
    this.grid = new CashflowDataGrid(page, this.root.locator('.main-blotter-data-grid'));
    this.dialogs = new CashflowDialogs(page);
    this.searchBuilder = new CashflowSearchBuilder(page);
    this.viewBuilder = new CashflowViewBuilder(page);
    const target = (suffix: string) => this.root.getByTestId(`${cashflowTestIdPrefix}/${suffix}`);
    this.hideSearchBarButton = target('hide_search_bar_btn');
    this.showSearchBarButton = target('show_search_bar_btn');
    this.loadNextButton = target('blotter/auto_load_next_btn');
    this.loadNextSettings = this.footer.root.locator('.load-next-settings');
    this.resizeButton = target('blotter/resize_btn');
    this.exportButton = target('blotter/export_file_btn');
    this.uploadButton = target('blotter/upload_btn');
    this.clearGridFiltersButton = target('blotter/clear_all_aggrid_filter_btn');
    this.clearQuickFiltersButton = target('quick_filter/clear_all_btn');
    this.resultsAlert = this.footer.root.getByRole('alert');
    this.savedFilter = this.root.getByTestId('select-fliter');
    this.clearSavedFilterButton = this.root.getByTestId('/advanced_search/entry_selector/clear_btn');
    this.createOrModifyFilterButton = this.root.getByTestId('/advanced_search/entry_selector/setting_btn');
    this.savedView = this.root.getByTestId('selectView');
    this.clearSavedViewButton = this.root.getByTestId('customView-clear-btn');
    this.createOrModifyViewButton = this.root.getByTestId('customView-create-modify-btn');
    // Ant Design renders notifications outside the owning blotter tile.
    this.notificationReconnectButton = page.getByTestId(`${cashflowTestIdPrefix}/notification_reconnect_btn`);
  }

  quickFilter(name: CashflowQuickFilter): Locator {
    return this.controls.combobox(cashflowQuickFilterIds[name]);
  }

  preset(period: 'today' | 'nextBusinessDay', status: 'operator' | 'verification'): Locator {
    const day = period === 'today' ? 'today' : 'tmr';
    return this.root.getByTestId(`${cashflowTestIdPrefix}/preset_query_count/value_${day}_pending_${status}`);
  }

  localFilterTag(columnLabel: string): Locator {
    requireIdentifier(columnLabel, 'columnLabel');
    return this.footer.root.locator('[title="Local Filter"]').filter({ hasText: exactText(columnLabel) });
  }

  customFilterTag(name: string): Locator {
    requireIdentifier(name, 'filter name');
    return this.footer.root.locator('[title="Custom Search"]').filter({ hasText: exactText(name) });
  }

  async expectVisible(): Promise<void> {
    await expect(this.root).toHaveCount(1);
    await expect(this.root).toBeVisible();
  }

  async hideSearchBar(): Promise<void> { await this.controls.click(this.hideSearchBarButton); }
  async showSearchBar(): Promise<void> { await this.controls.click(this.showSearchBarButton); }
  async loadNext(): Promise<void> { await this.footer.click(this.loadNextButton); }
  async resizeColumns(): Promise<void> { await this.footer.click(this.resizeButton); }
  async clearGridFilters(): Promise<void> { await this.footer.click(this.clearGridFiltersButton); }
  async clearQuickFilters(): Promise<void> { await this.controls.click(this.clearQuickFiltersButton); }
  async openExport(): Promise<void> { await this.footer.click(this.exportButton); }
  async openCustomSearch(): Promise<void> { await this.controls.click(this.createOrModifyFilterButton); }
  async openViewBuilder(): Promise<void> { await this.controls.click(this.createOrModifyViewButton); }
  async clearSavedFilter(): Promise<void> { await this.controls.click(this.clearSavedFilterButton); }
  async clearSavedView(): Promise<void> { await this.controls.click(this.clearSavedViewButton); }
  async reconnectNotifications(): Promise<void> { await this.controls.click(this.notificationReconnectButton); }

  async chooseQuickFilter(name: CashflowQuickFilter, value: string, popup?: Locator): Promise<void> {
    await this.controls.selectOption(this.quickFilter(name), value, popup);
  }

  async chooseSavedFilter(name: string, popup?: Locator): Promise<void> {
    await this.controls.selectOption(this.controls.combobox('select-fliter'), name, popup);
  }

  async chooseSavedView(name: string, popup?: Locator): Promise<void> {
    await this.controls.selectOption(this.controls.combobox('selectView'), name, popup);
  }

  async setLoadSize(size: 1000 | 5000): Promise<void> {
    await this.expectVisible();
    await expect(this.loadNextButton).toHaveCount(1);
    if ((await this.loadNextButton.innerText()).trim() === `Load next ${size}`) return;
    await expect(this.loadNextSettings).toHaveCount(1);
    await expect(this.loadNextSettings).toBeVisible();
    await this.loadNextSettings.hover();
    const item = this.page.getByRole('menuitem', { name: `set size to ${size}`, exact: true })
      .filter({ visible: true });
    await expect(item).toHaveCount(1);
    await expect(item).toBeEnabled();
    await expect(item).not.toHaveAttribute('aria-disabled', 'true');
    await item.click();
  }

  async dismissResultsAlert(): Promise<void> {
    await this.footer.click(this.resultsAlert.getByRole('button', { name: 'Close', exact: true }));
  }

  async removeLocalFilter(columnLabel: string): Promise<void> {
    await this.footer.click(this.localFilterTag(columnLabel).locator('.ant-tag-close-icon'));
  }

  async removeCustomFilter(name: string): Promise<void> {
    await this.footer.click(this.customFilterTag(name).locator('.ant-tag-close-icon'));
  }

  async uploadConfirmation(files: Parameters<Locator['setInputFiles']>[0]): Promise<void> {
    await this.expectVisible();
    await expect(this.uploadButton).toHaveCount(1);
    await expect(this.uploadButton).toBeVisible();
    await expect(this.uploadButton).toBeEnabled();
    const upload = this.footer.root.locator('.ant-upload').filter({ has: this.uploadButton });
    const fileInput = upload.locator('input[type="file"]');
    await expect(fileInput).toHaveCount(1);
    // Native upload inputs are intentionally hidden by Ant Design.
    await fileInput.setInputFiles(files);
  }
}
