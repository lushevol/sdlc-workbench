// API Document: https://confluence.global.standardchartered.com/display/DSP/RATAN+ONE+API+document
import { Service } from "../../Root/import";
import { getEnable } from "../componentEnabling";
const { service } = Service;

// High API Timeout For High Volume
// 6 min
const HIGH_TIMEOUT = 6 * 60 * 1000;

export const getWithParams = (url: string, data?: any) => {
  if (data) {
    return service.get(url, {
      params: data,
    });
  } else {
    return service.get(url);
  }
};

// Views Builder / Filter Builder
const VIEWS_BUILDER = (type) => {
  return getEnable("View_Builder_POC", type)
    ? "/api/ratan/v3/customview/views"
    : "/api/ratan/v2/customview/views";
};

const FILTERS_BUILDER = (type) => {
  return getEnable("Filter_Builder_POC", type)
    ? "/api/ratan/v3/customview/filters"
    : "/api/ratan/v2/customview/filters";
};
// Exception
const EXCEPTION: string = "/api/ratan/v1/exceptions";
const MANUAL_FIX: string = "/api/ratan/v1/cashflows/exception/manualFix";
// SSI
const LOOKUP_SSI: string = "/api/ratan/v1/slt/custom";
const OSCAR_VOSTRO: string = "/api/ratan/v1/oscar/vostros";
const MULTI_SSI: string = "/api/ratan/v1/slt/multi/";
const SSI_DETAIL: string = "/api/ratan/v1/slt/detail/";
const ADHOC_SSI_MAKER: string = "/api/ratan/v1/adhoc/ssis/maker";
const ADHOC_SSI_CHECKER: string = "/api/ratan/v1/adhoc/ssis/checker";
const ADHOC_SSI_REJECT: string = "/api/ratan/v1/adhoc/ssis/reject";
const ADHOC_SSI: string = "/api/ratan/v1/adhoc/ssis";
// Suppression Rules
const SUPPRESSION_RULE: string = "/api/ratan/v1/suppressions/rules";
const SUPPRESSION_RULE_HISTORY: string =
  "/api/ratan/v1/suppressions/rules/histories";
const SUPPRESSION_RULE_V2: string = "/api/ratan/v2/suppressions/rules";
// Currency Rules
const CURRENCY_RULE: string = "/api/ratan/rule/currency";
const CURRENCY_RULE_HISTORY: string = "/api/ratan/rule/currency/history";
// Netting Rules
const NETTING_RULE: string = "/api/ratan/v1/netting/rules";
const NETTING_RULE_HISTORY: string = "/api/ratan/v1/netting/rules/histories";
// New NSTP/Netting Rules
const newRuleBusinessType = "SETTLEMENT";
const NEW_NSTP_RULES_BASE = "/api/ratan/v1/nstpRule";
const NEW_NSTP_RULES_SPECIAL_CONFIG = `${NEW_NSTP_RULES_BASE}/SpecialConfig/${newRuleBusinessType}`;
const NEW_NSTP_RULES_ADD_SPECIAL_RULE = `${NEW_NSTP_RULES_BASE}/addSpecial`;
const NEW_RULES_BASE = "/api/ratan/v1/rule";
const NEW_RULES_LIST_RULES_BY_TYPE = `${NEW_RULES_BASE}/RULE_TYPE/listByType`;
const NEW_RULES_LIST_ALL_RULES = `${NEW_RULES_BASE}/${newRuleBusinessType}/listAll`;
const NEW_RULES_ADD_RULE = `${NEW_RULES_BASE}/add`;
const NEW_RULES_CANCEL_ADD_RULE = `${NEW_RULES_BASE}/RULE_ID/add/cancel`;
const NEW_RULES_CONFIRM_ADD_RULE = `${NEW_RULES_BASE}/RULE_ID/add/confirm`;
const NEW_RULES_DELETE_RULE = `${NEW_RULES_BASE}/RULE_ID/delete`;
const NEW_RULES_CANCEL_DELETE_RULE = `${NEW_RULES_BASE}/RULE_ID/delete/cancel`;
const NEW_RULES_CONFIRM_DELETE_RULE = `${NEW_RULES_BASE}/RULE_ID/delete/confirm`;
const NEW_RULES_HISTORIES = `${NEW_RULES_BASE}/histories`;
// Data Entitlement Rules
const ENTITLEMENT_RULE: string = "/api/ratan/v1/entitlement";
// Cashflow
const CASHFLOW_AFFIRMATION: string = "/api/ratan/v2/cashflows/affirm";
const CASHFLOW_NETTING: string =
  "/api/ratan/v1/cashSettlement/cashflows/netting";
const CASHFLOW_NETTING_BAU: string = "/api/ratan/v1/cashflows/netting";
const CASHFLOW_UN_NET: string = "/api/ratan/v1/cashSettlement/cashflows/unnet";
const CASHFLOW_UN_NET_BAU: string = "/api/ratan/v1/cashflows/unnet";
const CASHFLOW_NETTING_PREVIEW: string =
  "/api/ratan/v1/cashSettlement/cashflows/preview";
const REJECT_UN_NET: string = "/api/ratan/v1/cashflows/unnet/reject";
const VERIFY_UN_NET: string = "/api/ratan/v1/cashflows/unnet/verify";
const RELEASE_CASHFLOW: string = "/api/ratan/v1/cashflows/release/maker";
const REJECT_CASHFLOW: string = "/api/ratan/v1/cashflows/reject/checker";
const APPROVE_CASHFLOW: string = "/api/ratan/v1/cashflows/release/checker";
const CASHFLOW_ADD_COMMENT: string = "/api/ratan/v1/cashflows/comment/add";
const SUPPRESS_CASHFLOW: string = "/api/ratan/v1/cashflows/suppress/maker";
const REJECT_SUPPRESS_CASHFLOW: string =
  "/api/ratan/v1/cashflows/reject/suppress/checker";
const APPROVE_SUPPRESS_CASHFLOW: string =
  "/api/ratan/v1/cashflows/suppress/checker";
const UN_SUPPRESS_CASHFLOW: string = "/api/ratan/v1/cashflows/unsuppress";
const RELEASE_RECEIPT_CASHFLOW: string =
  "/api/ratan/v1/cashflows/release/receiptCashflow/maker";
const REJECT_RELEASE_RECEIPT_CASHFLOW: string =
  "/api/ratan/v1/cashflows/reject/release/receiptCashflow/checker";
const APPROVE_RELEASE_RECEIPT_CASHFLOW: string =
  "/api/ratan/v1/cashflows/release/receiptCashflow/checker";
const RELEASE_PAYMENT_CASHFLOW: string =
  "/api/ratan/v1/cashflows/release/paymentCashflow/maker";
const REJECT_RELEASE_PAYMENT_CASHFLOW: string =
  "/api/ratan/v1/cashflows/reject/release/paymentCashflow/checker";
const APPROVE_RELEASE_PAYMENT_CASHFLOW: string =
  "/api/ratan/v1/cashflows/release/paymentCashflow/checker";
const CASHFLOW_SUB_STATUS: string = "/api/ratan/v1/cashflows/substatus";
const SWIFT_MESSAGE: string = "/api/ratan/da/v1/swift/message";
const MAUNAL_FAIL_CASHFLOW: string = "/api/ratan/v1/cashflows/failed/manual";
// Trade
const TRADE_AFFIRMATION: string = "/api/ratan/v1/trade/affirmation";
const TRADE_AFFIRMATION_AUDIT: string = "/api/ratan/v1/trade/affirmation/audit";
const CURRENCY_PAIRS: string = "/api/ratan/currencyPairs/currencyPairsPop";
const BIZ_FIELDS: string = "/api/ratan/v1/static/fields";
const BIZ_FIELDS_RULE: string = "/api/ratan/rule/v1/fields";
const BIZ_FIELDS_VERSION: string = "/api/ratan/v1/static/fields/versions";
const BIZ_FIELDS_VERSION_RULE: string = "/api/ratan/rule/v1/fields/versions";
const REPLAY_TRADE: string = "/api/ratan/v1/trades";
// Nostro
const NOSTRO_DETAIL: string = "/api/ratan/v1/slt/nostros";
const NOSTRO: string = "/api/ratan/v1/slt/nostro";
const NOSTRO_LIST: string = "/api/ratan/v1/static/nostros";
// Validation rule
const VALIDATION_RULES: string =
  "/api/ratan/v1/static/validationRules/entities/";
// Validation rule from rule servive
const VALIDATION_RULES_FROM_RULE_SERVICE =
  "/api/ratan/rule/v1/validationRules/entities/";
// Vostro
const VOSTRO_DETAIL: string = "/api/ratan/v1/slt/vostros";
// User Preference
const PREFERENCE: string = "/api/ratan/v1/preference";
// Reinstate
const REINSTATE: string = "/api/ratan/v1/cashflows/reinstate";

// Currency CutOff
const CURRENCY_CUTOFF: string = "/api/ratan/v1/cashflow/currency/cutoff";
// Query Holiday
const QUERY_HOLIDAY: string = "/api/ratan/v1/cashflow/currency/holiday";
// Hold
const HOLD = "/api/ratan/v1/ratan/lifecycle/hold";
// Unhold
const UNHOLD = "/api/ratan/v1/ratan/lifecycle/unhold";
// used in early materialization
const CASHFLOW_USER_STATUS_UPDATE =
  "/api/ratan/v1/ratan/cashflow/user/status/update";
const MANUAL_FAILED = "/api/ratan/v1/camunda/task/fail";
const SWIFT_SUPPRESS_MAKER = "/api/ratan/v1/ratan/lifecycle/suppress/maker";
const SWIFT_SUPPRESS_CHECKER = "/api/ratan/v1/ratan/lifecycle/suppress/checker";

export const CASHFLOW_NOTIFICATION_SUBSCRIPTIONS =
  "/api/ratan/notification/subscriptions";

export const QUERY_SCHEDULE = "/api/ratan/v1/da/payment/schedule";

export const NOSTRO_STATIC = "/api/ratan/v2/static/nostros";

export const TRADE_REVIEW = "/api/ratan/tradeservice/trade-review";

// Views Builder
export const getViewList = (data: any) =>
  getWithParams(VIEWS_BUILDER(data.type), data);
export const getViewDetails = (id: string, type) =>
  service.get(`${VIEWS_BUILDER(type)}/${id}`);
export const postSaveView = (data: any) =>
  service.post(VIEWS_BUILDER(data.type), data);
export const putUpdateView = (id: string, data: any) =>
  service.put(`${VIEWS_BUILDER(data.type)}/${id}`, data);
export const deleteView = (params, type) => {
  if (typeof params === "string") {
    return service.delete(`${VIEWS_BUILDER(type)}/${params}`);
  }
  return service.delete(
    `${VIEWS_BUILDER(type)}?rowKey=${params.rowKey}&creator=${
      params.creator
    }&moduleOwner=${params.moduleOwner}`
  );
};

// Filters Builder
export const getFilterList = (data: any) =>
  getWithParams(FILTERS_BUILDER(data.type), data);
export const getFilterDetails = (id: string, type) =>
  service.get(`${FILTERS_BUILDER(type)}/${id}`);
export const postSaveFilter = (data: any) =>
  service.post(FILTERS_BUILDER(data.type), data);
export const putUpdateFilter = (id: string, data: any) =>
  service.put(`${FILTERS_BUILDER(data.type)}/${id}`, data);
export const deleteFilter = (params, type) => {
  if (typeof params === "string") {
    return service.delete(`${FILTERS_BUILDER(type)}/${params}`);
  }
  return service.delete(
    `${FILTERS_BUILDER(type)}?rowKey=${params.rowKey}&creator=${
      params.creator
    }&moduleOwner=${params.moduleOwner}`
  );
};

// exceptions
export const putReplay = (id: string) =>
  service.put(`${EXCEPTION}/${id}/replay`);
export const postManualFix = (data: any) => service.post(`${MANUAL_FIX}`, data);
export const putCloseException = (id: string) =>
  service.put(`${EXCEPTION}/${id}/close`);
export const postMakerRepair = (id: string, data: any) =>
  service.post(`${EXCEPTION}/${id}/repair`, data);
export const postCheckerRepair = (id: string, data: any) =>
  service.post(`${EXCEPTION}/${id}/accept`, data);
export const putCheckerReject = (id: string, data: any) =>
  service.put(`${EXCEPTION}/${id}/reject`, data);

// SSI
export const getLookupSSI = (data: any) =>
  service.post(LOOKUP_SSI, data, { timeout: 2 * 60 * 1000 });
export const fetchVostroForOscarStamping = (data: any) =>
  service.post(OSCAR_VOSTRO, data, { timeout: 2 * 60 * 1000 });
export const getQueryMultiSSI = (id: string) =>
  service.get(`${MULTI_SSI}${id}`);
export const getQuerySSIDetail = (id: string) =>
  service.get(`${SSI_DETAIL}${id}`); // Not used. Because the above two APIs already contain detailed data.
export const postAdhocSSIMaker = (data: any) =>
  service.post(ADHOC_SSI_MAKER, data);
export const postAdhocSSIChecker = (data: any) =>
  service.post(ADHOC_SSI_CHECKER, data);
export const postAdhocSSIReject = (data: any) =>
  service.post(ADHOC_SSI_REJECT, data);
export const getAdhocSSI = ({ cashflowId, cashflowVersion }: any) =>
  service.post(
    `${ADHOC_SSI}?cashflowId=${cashflowId}&cashflowVersion=${cashflowVersion}`
  );

// Suppression Rules
export const getSuppressionRuleList = () => service.get(SUPPRESSION_RULE);
export const createSuppressionRule = (data: any) =>
  service.post(SUPPRESSION_RULE, data);
export const changeSuppressionRuleStatus = (data: any) =>
  service.put(`${SUPPRESSION_RULE}/${data.id}/status`, {
    status: data.status,
  });
export const approveSuppressionRuleStatus = (data: any) =>
  service.put(`${SUPPRESSION_RULE_V2}/${data.id}/approve`, {
    status: data.status,
  });
export const getSuppressionRuleHistoryList = (data: any) =>
  getWithParams(SUPPRESSION_RULE_HISTORY, data);

// Settlement Rules
export const getSettlementRuleList = () =>
  service.get(`${SUPPRESSION_RULE}/nstp`);
export const createSettlementRule = (data: any) =>
  service.post(SUPPRESSION_RULE, { ...data, ruleType: "nstp" });
export const changeSettlementRuleStatus = (data: any) =>
  service.put(`${SUPPRESSION_RULE}/${data.id}/status`, {
    status: data.status,
    ruleType: "nstp",
  });
export const approveSettlementRuleStatus = (data: any) =>
  service.put(`${SUPPRESSION_RULE_V2}/${data.id}/approve`, {
    status: data.status,
    ruleType: "nstp",
  });
export const getSettlementRuleHistoryList = (data: any) =>
  getWithParams(SUPPRESSION_RULE_HISTORY, {
    ...data,
    ruleType: "nstp",
  });

// Netting Rules
export const getNettingRuleList = () => service.get(NETTING_RULE);
export const createNettingRule = (data: any) =>
  service.post(NETTING_RULE, data);
export const changeNettingRuleStatus = (data: any) =>
  service.put(`${NETTING_RULE}/${data.id}/status`, {
    status: data.status,
  });
export const approveNettingRuleStatus = (data: any) =>
  service.put(`${NETTING_RULE}/${data.id}/approve`, {
    status: data.status,
  });
export const getNettingRuleHistoryList = (data: any) =>
  getWithParams(NETTING_RULE_HISTORY, data);

// Currency Rules
export const getCurrencyRuleList = () => service.get(CURRENCY_RULE);
export const getCurrencyRuleHistoryList = () =>
  service.get(CURRENCY_RULE_HISTORY);
export const createCurrencyRule = (data: any) =>
  service.post(CURRENCY_RULE, data);
export const changeCurrencyRuleStatus = (data: any) =>
  service.patch(CURRENCY_RULE, data);

// New NSTP Rules
export const getSpecialRuleConfig_NewNSTPRules = () =>
  service.get(NEW_NSTP_RULES_SPECIAL_CONFIG);

export const addRule_NewRules = (payload) =>
  service.post(NEW_RULES_ADD_RULE, payload);

export const listAllRule_NewRules = () => service.get(NEW_RULES_LIST_ALL_RULES);

export const listRuleByType_NewRules = (ruleType: string) =>
  service.get(NEW_RULES_LIST_RULES_BY_TYPE.replace(/RULE_TYPE/, ruleType));

export const addSpecialRule_NewNSTPRules = (payload) =>
  service.post(NEW_NSTP_RULES_ADD_SPECIAL_RULE, payload);

export const cancelAddedRule_NewRules = ({ ruleId }) =>
  service.put(NEW_RULES_CANCEL_ADD_RULE.replace(/RULE_ID/, ruleId));

export const confirmAddedRule_NewRules = ({ ruleId }) =>
  service.put(NEW_RULES_CONFIRM_ADD_RULE.replace(/RULE_ID/, ruleId));

export const deleteRule_NewRules = ({ ruleId }) =>
  service.put(NEW_RULES_DELETE_RULE.replace(/RULE_ID/, ruleId));

export const cancelDeleteRule_NewRules = ({ ruleId }) =>
  service.put(NEW_RULES_CANCEL_DELETE_RULE.replace(/RULE_ID/, ruleId));

export const confirmDeleteRule_NewRules = ({ ruleId }) =>
  service.put(NEW_RULES_CONFIRM_DELETE_RULE.replace(/RULE_ID/, ruleId));

export const ruleHistories_NewRules = (payload) =>
  service.post(NEW_RULES_HISTORIES, payload);

// Data Entitlement Rules
export const getEntitlementRuleList = () => service.get(ENTITLEMENT_RULE);
export const createEntitlementRule = (data: any) =>
  service.post(ENTITLEMENT_RULE, data);
export const updateEntitlementRule = (data: any) =>
  service.put(ENTITLEMENT_RULE, data);
export const delEntitlementRule = (data: any) =>
  service.delete(`${ENTITLEMENT_RULE}/${data.role}/${data.entity}`, data);
export const getMyEntitlementRuleList = () =>
  service.get(`${ENTITLEMENT_RULE}/user`);
export const getEntitlementRoles = () =>
  service.get(`${ENTITLEMENT_RULE}/roles`);

// Trade
export const postTradeAffirmation = (data: any) =>
  service.post(TRADE_AFFIRMATION, data, { timeout: 2 * 60 * 1000 });
export const getTradeAffirmation = (tradeId: string) =>
  service.get(`${TRADE_AFFIRMATION_AUDIT}/${tradeId}`);
export const getCurrencyPairsData = () => service.get(CURRENCY_PAIRS);
export const replayTrade = (data: any) =>
  service.put(`${REPLAY_TRADE}/${data.tradeId}/replay?version=${data.version}`);

// Cashflow
export const postCashAffirmation = (data: any) =>
  service.post(CASHFLOW_AFFIRMATION, data);
export const cashflowNetting = (data: any) =>
  service.post<any>(CASHFLOW_NETTING, data);
export const cashflowNettingBAU = (data: any) =>
  service.post<any>(CASHFLOW_NETTING_BAU, data);
export const cashflowNettingPreview = (data: any) =>
  service.post<any>(CASHFLOW_NETTING_PREVIEW, data);
export const releaseCashflow = (data: any) =>
  service.post(RELEASE_CASHFLOW, data);
export const rejectCashflow = (data: any) =>
  service.post(REJECT_CASHFLOW, data);
export const approveCashflow = (data: any) =>
  service.post(APPROVE_CASHFLOW, data);
export const cashflowUnNet = (data: any) =>
  service.post(CASHFLOW_UN_NET, data, { timeout: HIGH_TIMEOUT });
export const cashflowUnNetBAU = (data: any) =>
  service.post(CASHFLOW_UN_NET_BAU, data);
export const verifyCashflowUnNet = (data: any) =>
  service.post(VERIFY_UN_NET, data);
export const rejectCashflowUnNet = (data: any) =>
  service.post(REJECT_UN_NET, data);
export const cashflowAddComment = (data: any) =>
  service.post(CASHFLOW_ADD_COMMENT, data);
export const suppressCashflow = (data: any) =>
  service.post(SUPPRESS_CASHFLOW, data);
export const rejectSuppressCashflow = (data: any) =>
  service.post(REJECT_SUPPRESS_CASHFLOW, data);
export const approveSuppressCashflow = (data: any) =>
  service.post(APPROVE_SUPPRESS_CASHFLOW, data);
export const requestUnSuppressCashflow = (data: any) =>
  service.post(UN_SUPPRESS_CASHFLOW, data);
export const releaseReceiptCashflow = (data: any) =>
  service.post(RELEASE_RECEIPT_CASHFLOW, data);
export const rejectReleaseReceiptCashflow = (data: any) =>
  service.post(REJECT_RELEASE_RECEIPT_CASHFLOW, data);
export const approveReleaseReceiptCashflow = (data: any) =>
  service.post(APPROVE_RELEASE_RECEIPT_CASHFLOW, data);
export const releasePaymentCashflow = (data: any) =>
  service.post(RELEASE_PAYMENT_CASHFLOW, data);
export const rejectReleasePaymentCashflow = (data: any) =>
  service.post(REJECT_RELEASE_PAYMENT_CASHFLOW, data);
export const approveReleasePaymentCashflow = (data: any) =>
  service.post(APPROVE_RELEASE_PAYMENT_CASHFLOW, data);
export const getCashflowSubStatusList = () => service.get(CASHFLOW_SUB_STATUS);
export const swiftMessageDetails = (data: any) =>
  service.post(SWIFT_MESSAGE, data);
export const postReinstate = (data: any) => service.post(REINSTATE, data);

export const cashflowHold = (data: any) => service.post(HOLD, data);
export const cashflowUnhold = (data: any) => service.post(UNHOLD, data);

export const cashflowManualFailed = (data: any) =>
  service.post(MANUAL_FAILED, data);
export const cashflowSwiftSuppressionMakerAction = (data: any) =>
  service.post(SWIFT_SUPPRESS_MAKER, data);
export const cashflowSwiftSuppressionCheckerAction = (data: any) =>
  service.post(SWIFT_SUPPRESS_CHECKER, data);

export const manualFailCashflow = (data: any) =>
  service.post(MAUNAL_FAIL_CASHFLOW, data);

// used in early materialization
export const cashflowUserStatusUpdate = (data: any) =>
  service.post(CASHFLOW_USER_STATUS_UPDATE, data);

// Nostro
export const getNostroDetail = (data: any) =>
  getWithParams(NOSTRO_DETAIL, data);
export const getNostroList = (params: any) =>
  service.get(
    `${NOSTRO_LIST}?legalEntityFmid=${params.legalEntityFmid}&currency=${params.currency}`
  );
export const getNostroForOscar = (query: any) => {
  let queryStr = "";
  const l = Object.keys(query).length;
  Object.keys(query)?.forEach((element, index) => {
    const suffix = l - 1 === index ? "" : "&";
    queryStr += `${element}=${query[element]}${suffix}`;
  });
  return service.get(`${NOSTRO_LIST}?${queryStr}`);
};
export const postMakerNostro = (data: any) =>
  service.post(`${NOSTRO}/maker`, data);
export const postCheckerNostro = (data: any) =>
  service.post(`${NOSTRO}/checker`, data);
export const postRejectNostro = (data: any) =>
  service.post(`${NOSTRO}/reject`, data);
// Vostro
export const getVostroDetail = (data: any) =>
  getWithParams(VOSTRO_DETAIL, data);

// Validation rules
export const getValidationRules = (entity: any) =>
  service.get(`${VALIDATION_RULES}${entity}`);

export const getValidationRulesFromRuleService = (entity: string) =>
  service.get(`${VALIDATION_RULES_FROM_RULE_SERVICE}${entity}`);
// User Preference
export const getPreference = () => service.get(PREFERENCE);
export const putPreference = (data: any) => service.put(PREFERENCE, data);

// Fields
export const getBusinessFieldsVersion = () => service.get(BIZ_FIELDS_VERSION);
export const getBusinessFieldsVersionFromRuleService = () =>
  service.get(BIZ_FIELDS_VERSION_RULE);
export const getBusinessFieldsTrade = (contexts: string) =>
  service.get(`${BIZ_FIELDS}?contexts=${contexts}`);
export const getBusinessFieldsCashflow = (contexts: string) =>
  service.get(`${BIZ_FIELDS}?contexts=${contexts}`);
export const getBusinessFieldsCashflowFromRuleService = (contexts: string) =>
  service.get(`${BIZ_FIELDS_RULE}?contexts=${contexts}`);

//Currency CutOff
export const getCurrencyList = () => service.get(CURRENCY_CUTOFF);
export const createCurrency = (data: any) =>
  service.post(CURRENCY_CUTOFF, data);
export const deleteCurrency = (data: any) =>
  service.delete(`${CURRENCY_CUTOFF}/${data.id}`);
export const checkerApproveCurrency = (data: any) =>
  service.post(`${CURRENCY_CUTOFF}/${data.ticketId}/confirm`);
export const checkerRejectCurrency = (data: any) =>
  service.post(`${CURRENCY_CUTOFF}/${data.ticketId}/reject`);

// Query Holiday
export const queryHolidy = (params: any) => service.post(QUERY_HOLIDAY, params);

// Query Schedule
export const querySchedule = (params: any) =>
  service.get(
    `${QUERY_SCHEDULE}?tradeId=${params.tradeId}&trackingVersion=${params.trackingVersion}`
  );

// Nostro Static
export const getNostroStaticList = () =>
  service.get(`${NOSTRO_STATIC}?page=0&size=1000`);
export const makerAddNostroStatic = (data) => service.post(NOSTRO_STATIC, data);
export const checkerConfirmActionNostroStatic = (id: any) =>
  service.post(`${NOSTRO_STATIC}/${id}/confirm`);
export const checkerCancelActionNostroStatic = (id: any) =>
  service.post(`${NOSTRO_STATIC}/${id}/cancel`);
export const makerDeleteNostroStatic = (id: any) =>
  service.delete(`${NOSTRO_STATIC}/${id}`);
export const getNostroAudit = () =>
  service.get(`${NOSTRO_STATIC}/audit?page=0&size=5000`);
export const getNostroAuditDetails = (id: any) =>
  service.get(`${NOSTRO_STATIC}/audit/${id}`);

// Trade Review Comment and Validation Status
export const setValidationStatusAndComment = (data: any) =>
  service.post(`${TRADE_REVIEW}/validate`, data);
export const getValidationAudit = (id: any) =>
  service.get(`${TRADE_REVIEW}/${id}/validation/history`);
