import { expect, type Locator, type Page } from '@playwright/test';
import { CashflowControlScope, cssValue, namedDialogRoot } from './control-scope.js';
import { CashflowDataGrid } from './data-grid.component.js';

const base = '/cashflow_blotter_cn/cashflow_cn';
const detail = `${base}/cashflow_detail`;
const exception = `${detail}/muti_exception`;
const nonempty = (value: string): string => {
  if (!value.trim()) throw new Error('A nonempty control identity is required.');
  return value;
};
const index = (value: number): number => {
  if (!Number.isInteger(value) || value < 0) throw new Error('A nonnegative row index is required.');
  return value;
};

/** These scopes support the inspected CN source. Runtime visibility depends on data, permissions, and feature flags. */
export class CashflowDialog extends CashflowControlScope {
  readonly closeButton: Locator;
  readonly maximizeButton: Locator;
  readonly restoreButton: Locator;
  readonly resizeHandle: Locator;
  readonly titleBar: Locator;

  constructor(page: Page, root: Locator) {
    super(page, root);
    this.closeButton = root.locator('[data-testid$="_Dialog-close"]');
    this.maximizeButton = root.locator('[data-testid$="_Dialog-maximize"]');
    this.restoreButton = this.maximizeButton.and(root.locator('[aria-pressed="true"]'));
    this.resizeHandle = root.locator('[data-testid$="_Dialog-resize"]');
    this.titleBar = root.locator('.MuiDialogTitle-root');
  }

  async close(): Promise<void> { await this.click(this.closeButton); }
  async expectClosed(): Promise<void> { await expect(this.root).toBeHidden(); }
}

export class CashflowAffirmationFields extends CashflowControlScope {
  readonly nameInput: Locator;
  readonly contactInput: Locator;
  readonly dateTimeInput: Locator;

  constructor(page: Page, root: Locator, kind: 'exception' | 'preview' = 'exception') {
    super(page, root);
    this.nameInput = kind === 'preview' ? this.field('affirmedName') : root.locator('[id="affirmationForm_affirmedBy"]');
    this.contactInput = kind === 'preview' ? this.field('affirmedEmail') : root.locator('[id="affirmationForm_phone_email"]');
    this.dateTimeInput = kind === 'preview' ? this.field('affirmedAt') : root.locator('[id="affirmationForm_affirmedAt"]');
  }
}

/** CustomForm items expose their configuration field as data-testid. Scope resolves duplicate labels and field IDs. */
export class CashflowSsiSection extends CashflowControlScope {
  constructor(page: Page, root: Locator, readonly kind: 'vostro' | 'nostro') { super(page, root); }

  formField(fieldName: string): Locator { return this.field(nonempty(fieldName)); }
  formCombobox(fieldName: string): Locator { return this.combobox(nonempty(fieldName)); }
  action(actionName: string): Locator {
    return this.testId(`${exception}/${this.kind}_form/${nonempty(actionName)}_btn`);
  }
  readonly resetButton = this.root.locator('button.custom-reset-btn');
  readonly previousButton = this.root.locator('button.custom-pre-btn');
  readonly nextButton = this.root.locator('button.custom-next-btn');

  /** Supply exact displayed cell values. Nostro SSI_Unique_Id is absent from rendered rows. */
  record(cells: readonly string[]): Locator {
    if (!cells.length) throw new Error('At least one exact SSI cell identity is required.');
    let row = this.root.getByRole('row');
    for (const cell of cells) row = row.filter({ has: this.page.getByRole('cell', { name: nonempty(cell), exact: true }) });
    return row;
  }
  pageButton(label: string): Locator { return this.root.locator('.ant-pagination').getByRole('button', { name: nonempty(label), exact: true }); }
}

export class CashflowDetailsDialog extends CashflowDialog {
  readonly tabs: Locator;
  readonly detailPanel: Locator;
  readonly historyPanel: Locator;
  readonly swiftPanel: Locator;
  readonly accountingPanel: Locator;
  readonly bookingEntityButton: Locator;
  readonly counterpartyButton: Locator;
  readonly openTradeDetailsButton: Locator;
  readonly childCashflowButton: Locator;
  readonly refreshButton: Locator;
  readonly submitExceptionsButton: Locator;
  readonly approveExceptionsButton: Locator;
  readonly rejectExceptionButton: Locator;
  readonly rejectExceptionsButton: Locator;
  readonly commentInput: Locator;
  readonly backValueDateInput: Locator;
  readonly affirmation: CashflowAffirmationFields;
  readonly vostro: CashflowSsiSection;
  readonly nostro: CashflowSsiSection;
  readonly swiftMenuButton: Locator;
  readonly copySwiftButton: Locator;
  readonly exportSwiftButton: Locator;
  readonly swiftMessageCount: Locator;
  readonly historyRestoreButton: Locator;

  constructor(page: Page, root: Locator) {
    super(page, root);
    this.tabs = root.getByTestId(`${detail}/cashflow_detail_tab`);
    this.detailPanel = root.locator('[id="simple-tabpanel-1"]');
    this.historyPanel = root.locator('[id="simple-tabpanel-3"]');
    this.swiftPanel = root.locator('[id="simple-tabpanel-4"]');
    this.accountingPanel = root.locator('[id="simple-tabpanel-6"]');
    this.bookingEntityButton = this.testId(`${detail}/booking_entity_btn`);
    // Source misspells data-testif. The explicit DOM ID is the usable identity.
    this.counterpartyButton = root.locator('[id="cashflow-counterparty-icon"]');
    this.openTradeDetailsButton = this.testId(`${detail}/open_trade_detail_btn`);
    this.childCashflowButton = this.testId('component-cashflow-display-btn');
    this.refreshButton = this.testId(`${detail}/notification_refresh_btn`);
    this.submitExceptionsButton = this.testId(`${exception}/submit_btn`);
    this.approveExceptionsButton = this.testId(`${exception}/approve_btn`);
    this.rejectExceptionButton = this.testId(`${exception}/reject_btn`);
    this.rejectExceptionsButton = this.testId(`${exception}/reject_multi_btn`);
    this.commentInput = root.locator('[id="commentForm_comment"]');
    this.backValueDateInput = root.locator('[id="back_valueForm_swiftPaymentDate"]');
    this.affirmation = new CashflowAffirmationFields(page, this.detailPanel);
    this.vostro = new CashflowSsiSection(page, root.locator('.MuiAccordion-root').filter({ has: page.locator('form[id="vostroForm"]').or(page.getByRole('columnheader', { name: 'SSI ID', exact: true })) }), 'vostro');
    this.nostro = new CashflowSsiSection(page, root.locator('.MuiAccordion-root').filter({ has: page.locator('form[id="nostroForm"]').or(page.getByRole('columnheader', { name: 'Nostro Account', exact: true })) }), 'nostro');
    this.swiftMenuButton = this.swiftPanel.getByTestId('menu-icon_btn');
    this.copySwiftButton = this.swiftPanel.getByTestId('copy-message');
    this.exportSwiftButton = this.swiftPanel.getByTestId('ExportMessageBtn');
    this.swiftMessageCount = this.swiftPanel.getByTestId('message-total-hits');
    this.historyRestoreButton = this.historyPanel.getByTestId('cashflow-history-resize-btn').getByRole('button', { name: 'Restore', exact: true });
  }

  detailTab(name: 'Cashflow Detail' | 'History' | 'Swift Message' | 'Accounting Detail'): Locator {
    return this.tabs.getByRole('tab', { name, exact: true });
  }
  swiftMessage(type: string): Locator { return this.page.locator('[id="menu-swift-message"]').getByTestId(`swift-menu-${nonempty(type)}`); }
  historyGrid(): CashflowDataGrid { return new CashflowDataGrid(this.page, this.historyPanel.getByRole('grid')); }
  accountingGrid(): CashflowDataGrid { return new CashflowDataGrid(this.page, this.accountingPanel.getByRole('grid')); }
  exceptionSection(title: string): CashflowControlScope {
    return new CashflowControlScope(this.page, this.detailPanel.locator('.MuiAccordion-root').filter({
      has: this.page.locator('.accordion-title').getByText(nonempty(title), { exact: true }),
    }));
  }
}

export class CashflowCommentDialog extends CashflowDialog {
  readonly commentInput: Locator;
  readonly submitButton: Locator;
  readonly rejectButton: Locator;
  readonly selectedIdsButton: Locator;
  readonly affirmation: CashflowAffirmationFields;

  constructor(page: Page, root: Locator, readonly actionTestId: string, actionLabel: string) {
    super(page, root);
    this.commentInput = this.field('addCommentText');
    this.submitButton = this.testId(`${base}/blotter_menu_action/${actionTestId}/submit_btn`);
    this.rejectButton = this.testId(`${base}/blotter_menu_action/${actionTestId}/reject_btn`);
    this.selectedIdsButton = this.testId(`${base}/blotter_menu_action/${flattenAction(actionLabel)}/all_cashflow_ids_btn`);
    this.affirmation = new CashflowAffirmationFields(page, root);
  }
}

export class CashflowNettingDialog extends CashflowDialog {
  readonly submitButton: Locator;
  readonly footerCloseButtons: Locator;
  readonly previewGrids: Locator;
  constructor(page: Page, root: Locator) {
    super(page, root);
    this.submitButton = this.testId(`${base}/netting_cashflow_dialog/net_with_affirm_btn`);
    // The ERROR state renders the same Close ID twice. Callers must choose the containing section.
    this.footerCloseButtons = this.testId(`${base}/netting_cashflow_dialog/close_btn`);
    this.previewGrids = root.getByRole('grid');
  }
  gridIn(section: Locator): CashflowDataGrid { return new CashflowDataGrid(this.page, section.getByRole('grid')); }
  resultantGrid(): CashflowDataGrid { return this.titledGrid('Netting Resultant Cashflow (Preview)'); }
  componentGrid(): CashflowDataGrid { return this.titledGrid('Netting Component Cashflows'); }
  private titledGrid(title: string): CashflowDataGrid {
    return new CashflowDataGrid(this.page, this.root.getByText(title, { exact: true }).locator('..').getByRole('grid'));
  }
}

export class CashflowPreviewAffirmationDialog extends CashflowDialog {
  readonly affirmation: CashflowAffirmationFields;
  readonly submitButton: Locator;
  constructor(page: Page, root: Locator, kind: 'netting' | 'splitting') {
    super(page, root);
    this.affirmation = new CashflowAffirmationFields(page, root, 'preview');
    this.submitButton = this.testId(kind === 'netting'
      ? `${base}/netting_cashflow_dialog/net_submit_btn`
      // The splitting source uses this literal rather than the similarly named exported constant.
      : 'CASHFLOW_BLOTTER_SPLITTING_DIALOG_NET_SUBMIT_BTN');
  }
}

export class CashflowSplittingDialog extends CashflowDialog {
  readonly openAffirmationButton: Locator;
  readonly confirmButton: Locator;
  readonly grids: Locator;
  constructor(page: Page, root: Locator) {
    super(page, root);
    this.openAffirmationButton = this.testId('open-affirmation-btn');
    this.confirmButton = this.testId('confirm-amendment-btn');
    this.grids = root.getByRole('grid');
  }
  amountInput(rowIndex: number): Locator { return this.field(`splittingAmount_Input_${index(rowIndex)}`); }
  deleteRowButton(rowIndex: number): Locator { return this.testId(`splittingDeleteButton_${index(rowIndex)}`); }
  lookupSsiButton(rowIndex: number): Locator { return this.testId(`lookUpSSIBtn_${index(rowIndex)}`); }
  parentGrid(): CashflowDataGrid { return this.gridUnder('Parent Cashflow'); }
  childGrid(): CashflowDataGrid { return this.gridUnder('Child Cashflows (Preview)'); }
  private gridUnder(title: string): CashflowDataGrid {
    // Locate the closest structural section; parent/child grids have no separate test IDs.
    const grid = this.root.getByText(title, { exact: title === 'Parent Cashflow' }).locator('..').getByRole('grid');
    return new CashflowDataGrid(this.page, grid);
  }
}

export class CashflowLookupSsiDialog extends CashflowDialog {
  readonly submitButton: Locator;
  readonly resetButton: Locator;
  readonly vostro: CashflowSsiSection;
  readonly nostro: CashflowSsiSection;
  constructor(page: Page, root: Locator) {
    super(page, root);
    this.submitButton = this.button('Submit');
    this.resetButton = this.testId('look-up-ssi-reset-button');
    this.vostro = new CashflowSsiSection(page, root.locator('.split-lookup-vostro-section'), 'vostro');
    this.nostro = new CashflowSsiSection(page, root.locator('.split-lookup-nostro-section'), 'nostro');
  }
}

export class CashflowBulkExceptionsDialog extends CashflowDialog {
  readonly submitButton: Locator;
  readonly approveButton: Locator;
  readonly rejectButton: Locator;
  readonly commentInput: Locator;
  readonly extraForm: Locator;
  readonly affirmation: CashflowAffirmationFields;
  readonly backValueDateInput: Locator;
  readonly insufficientExpander: Locator;
  constructor(page: Page, root: Locator) {
    super(page, root);
    this.submitButton = this.testId(`${base}/bulk_fix_exceptions/submit_btn`);
    this.approveButton = this.testId(`${base}/bulk_fix_exceptions/approve_btn`);
    this.rejectButton = this.testId(`${base}/bulk_fix_exceptions/reject_btn`);
    this.extraForm = this.testId('extra-form');
    this.commentInput = this.extraForm.getByPlaceholder('Please type in comment.', { exact: true });
    this.affirmation = new CashflowAffirmationFields(page, this.extraForm);
    this.backValueDateInput = this.extraForm.locator('[id="back_valueForm_swiftPaymentDate"]');
    this.insufficientExpander = root.getByRole('button', { name: /cashflows insufficient for bulk operation/ });
  }
  eligibleTable(): CashflowControlScope {
    // Only the eligible table has row selection checkboxes.
    return new CashflowControlScope(this.page, this.testId('cashflow-display-table').filter({ has: this.page.getByRole('checkbox') }));
  }
  cashflowRow(cashflowId: string): Locator {
    return this.eligibleTable().root.locator(`[data-row-key=${cssValue(nonempty(cashflowId))}]`);
  }
  selectedCashflow(cashflowId: string): Locator { return this.cashflowRow(cashflowId).getByRole('checkbox'); }
  selectAllCheckbox(): Locator { return this.eligibleTable().root.locator('thead').getByRole('checkbox'); }
}

export class CashflowSettlementMethodDialog extends CashflowDialog {
  readonly submitButton: Locator;
  readonly commentInput: Locator;
  readonly tables: Locator;
  readonly insufficientExpander: Locator;
  readonly tradeIdsButton: Locator;
  constructor(page: Page, root: Locator) {
    super(page, root);
    this.submitButton = this.testId(`${base}/settlement_method_update/submit_btn`);
    this.commentInput = this.testId('extra-form').getByPlaceholder('Please type in comment.', { exact: true });
    this.tables = this.testId('cashflow-table');
    this.insufficientExpander = root.getByRole('button', { name: /cashflows insufficient for Settlement Method Update/ });
    // The title's information button shares the header with the maximize ToggleButton.
    this.tradeIdsButton = this.titleBar.locator('.MuiGrid-item').filter({ hasText: /^Settlement Method Update/ }).locator('button');
  }
  tableIn(section: Locator): CashflowDataGrid { return new CashflowDataGrid(this.page, section.getByRole('grid')); }
}


export class CashflowExportDialog extends CashflowDialog {
  readonly fileNameInput: Locator;
  readonly formatCombobox: Locator;
  readonly exportButton: Locator;
  constructor(page: Page, root: Locator) {
    super(page, root);
    this.fileNameInput = this.field('exportFileName');
    this.formatCombobox = this.combobox('exportFileFormat');
    this.exportButton = this.testId(`${base}/blotter/export_file_confirm_btn`);
  }
  async selectFormat(format: 'CSV' | 'XLSX'): Promise<void> {
    await this.selectOption(this.formatCombobox, format);
  }
}

const flattenAction = (value: string): string => value.toLowerCase().replace(/\W/g, '_');
export type CashflowCommentAction = 'Hold' | 'UnHold' | 'Send to WAITING' | 'Manual Fail' | 'Confirm Manual Fail'
  | 'Manual Settle' | 'Verify Settle' | 'Early Materialization' | 'ReInstate' | 'Settle As Gross'
  | 'Status Write Back' | 'Resend To Razor' | 'Early Release' | 'Update Affirmation' | 'Comment' | 'Regenerate Swift'
  | 'Swift Suppression' | 'Verify Swift Suppression' | 'Undo Swift Suppression' | 'Verify Undo Swift Suppression'
  | 'Suppress Cashflow' | 'Confirm Suppression' | 'Un-Suppress Cashflow' | 'Confirm Un-Suppression';

/** Dialogs use portals. Their roots must be selected from the page rather than the blotter DOM subtree. */
export class CashflowDialogs {
  constructor(readonly page: Page) {}

  named(title: string | RegExp): CashflowDialog { return new CashflowDialog(this.page, this.namedRoot(title)); }
  private namedRoot(title: string | RegExp): Locator {
    return namedDialogRoot(this.page, title);
  }
  details(): CashflowDetailsDialog {
    return new CashflowDetailsDialog(this.page, this.page.getByRole('dialog').filter({ has: this.page.getByTestId(`${detail}/cashflow_detail_tab`) }));
  }
  comment(action: CashflowCommentAction): CashflowCommentDialog {
    const testId = ['Hold', 'UnHold', 'Send to WAITING'].includes(action) ? action.replaceAll(' ', '_')
      : ['Manual Fail', 'Confirm Manual Fail'].includes(action) ? 'manual_fail'
      : ['Manual Settle', 'Verify Settle'].includes(action) ? 'manual_settle' : flattenAction(action);
    return new CashflowCommentDialog(this.page, this.namedRoot(action), testId, action);
  }
  netting(): CashflowNettingDialog { return new CashflowNettingDialog(this.page, this.namedRoot('Cashflow Netting Preview')); }
  previewAffirmation(kind: 'netting' | 'splitting'): CashflowPreviewAffirmationDialog {
    return new CashflowPreviewAffirmationDialog(this.page, this.namedRoot('Update Affirmation').filter({ has: this.page.getByTestId('affirmedName') }), kind);
  }
  splitting(mode: 'split' | 'amend' | 'unsplit' | 'children' = 'split'): CashflowSplittingDialog {
    const titles = { split: 'Split Cashflow Preview', amend: 'Amend Split Amount', unsplit: 'Un-Split Cashflow Preview', children: 'View Child Cashflow' };
    return new CashflowSplittingDialog(this.page, this.namedRoot(titles[mode]));
  }
  lookupSsi(): CashflowLookupSsiDialog { return new CashflowLookupSsiDialog(this.page, this.namedRoot('Look Up SSI')); }
  bulkExceptions(role: 'maker' | 'checker'): CashflowBulkExceptionsDialog {
    return new CashflowBulkExceptionsDialog(this.page, this.namedRoot(role === 'maker' ? 'Bulk Fix Exceptions' : 'Bulk Verify Exceptions'));
  }
  settlementMethod(): CashflowSettlementMethodDialog { return new CashflowSettlementMethodDialog(this.page, this.namedRoot(/^Settlement Method Update/)); }
  counterparty(): CashflowDialog { return this.named('Counterparty Detail'); }
  exportFile(): CashflowExportDialog { return new CashflowExportDialog(this.page, this.namedRoot('Export File')); }
  historyChange(kind: 'Value Change'): CashflowDialog { return this.named(kind); }
  /** Explicit supplied root handles remote trade/unnnet controls whose source is absent from this checkout. */
  external(observedRoot: Locator): CashflowControlScope { return new CashflowControlScope(this.page, observedRoot); }
  rejectExceptionsPopup(): CashflowControlScope {
    return new CashflowControlScope(this.page, this.page.locator('.ant-popconfirm').filter({ hasText: 'Reject Exceptions' }));
  }
  confirmation(title: string): CashflowControlScope {
    return new CashflowControlScope(this.page, this.page.getByRole('dialog').filter({ hasText: nonempty(title) }));
  }
}

/** Source-defined fields. Rules can hide or disable them for the selected payment and role. */
export const cashflowSsiFields = {
  "vostro": [
    "accountWithInstitutionAccount",
    "accountWithInstitutionAddress",
    "accountWithInstitutionAddress1",
    "accountWithInstitutionAddress2",
    "accountWithInstitutionBic",
    "accountWithInstitutionCity",
    "accountWithInstitutionCityName",
    "accountWithInstitutionCountryIsoCode",
    "accountWithInstitutionName",
    "accountWithInstitutionPostCode",
    "beneficiaryAccount",
    "beneficiaryAddress",
    "beneficiaryAddress1",
    "beneficiaryAddress2",
    "beneficiaryBic",
    "beneficiaryCity",
    "beneficiaryCityName",
    "beneficiaryCountryIsoCode",
    "beneficiaryName",
    "beneficiaryName2",
    "beneficiaryPostCode",
    "charges",
    "coveredPayment",
    "entity",
    "intermediaryAccount",
    "intermediaryAddress",
    "intermediaryAddress1",
    "intermediaryAddress2",
    "intermediaryBic",
    "intermediaryCity",
    "intermediaryCityName",
    "intermediaryCountryIsoCode",
    "intermediaryName",
    "intermediaryPostcode",
    "isThirdPartyPayment",
    "orderCustomerAccount",
    "orderCustomerAddress",
    "orderCustomerAddress1",
    "orderCustomerAddress2",
    "orderCustomerBic",
    "orderCustomerCity",
    "orderCustomerCityName",
    "orderCustomerCountryIsoCode",
    "orderCustomerName",
    "orderCustomerPostCode",
    "popDubai",
    "receiversCorrespondentAccount",
    "receiversCorrespondentAddress",
    "receiversCorrespondentAddress1",
    "receiversCorrespondentAddress2",
    "receiversCorrespondentBic",
    "receiversCorrespondentCity",
    "receiversCorrespondentCityName",
    "receiversCorrespondentCountryIsoCode",
    "receiversCorrespondentName",
    "receiversCorrespondentPostCode",
    "remittanceInformation1",
    "remittanceInformation2",
    "remittanceInformation3",
    "remittanceInformation4",
    "senderToReceiver1",
    "senderToReceiver2",
    "senderToReceiver3",
    "senderToReceiver4",
    "senderToReceiver5",
    "senderToReceiver6",
    "settlementAccount",
    "settlementMeans",
    "ssiType",
    "swiftType",
    "tradingCurrency"
  ],
  "nostro": [
    "dedicatedPortfolio",
    "ebbsNostroAccount",
    "nostroType",
    "noticeToReceive",
    "sendersCorrespondent53Account",
    "sendersCorrespondent53Address",
    "sendersCorrespondent53City",
    "sendersCorrespondent53Fullname",
    "sendersCorrespondent53Swift",
    "settlementAccount",
    "settlementMeans"
  ]
} as const;
