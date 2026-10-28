// https://github.com/apollographql/subscriptions-transport-ws

import {
  ApolloClient,
  InMemoryCache,
  gql,
  ApolloLink,
  HttpLink,
  from,
} from "@apollo/client";
import { WebSocketLink } from "@apollo/client/link/ws";
import { ErrorHandler, onError } from "@apollo/client/link/error";
import { ColDef, GridApi } from "ag-grid-community";

import {
  conversionDQSLRequest,
  conversionResult,
  conversionGraphqlErrorField,
  getDisplayFields,
} from "../conversion";
import {
  CASHFLOW_DEFAULT_FILTER,
  CASHFLOW_DEFAULT_FILTER_CN,
  CASHFLOW_SUB_STATUS,
  CASHFLOW_SUB_STATUS_BAU,
} from "../config/ratancashflow/fieldsConfig";
import {
  SIZE_CONFIG_INFINITE_SCROLL,
  INITIAL_COUNT_SCROLL,
} from "../config/ratantrades/UIconfig";
import { logger } from "../logger";
import { getBusinessFieldsFromCache } from "../init";
import {
  counterpartyQueryStr,
  counterpartyQueryStrForCN,
} from "../../ratandialog/components/CounterpartyDetails-v2/counterpartyDetailsConfig";
import { getEnable } from "../componentEnabling";
import {
  PAGE_NUMBER_FOR_CASHFLOW,
  PAGE_SIZE_FOR_CASHFLOW,
} from "../config/ratancashflow/UIconfig";
import {
  dynamicDefaultFilter,
  handleMultiFieldsQuery,
  setSearchFilter,
} from "../setDefaultFilter";
import { Hooks, CommonUtil, ExtendTokenService } from "../../Root/import";
import { SubscriptionClient } from "subscriptions-transport-ws";
import holidayDB from "../holidayDB";
export { gql };
const { getHooks } = Hooks;
const { showErrorMsg } = CommonUtil;

export const graphqlUrl = {
  QUERY_TRADES: "/api/ratan/bff/v1/trades",
  QUERY_EXCEPTIONS: "/api/ratan/bff/v1/exceptions",
  QUERY_COUNTERPARTY: "/api/ratan/bff/v1/counterparties",
  QUERY_CASHFLOW: "/api/ratan/bff/v1/cashflows",
  QUERY_CASHFLOW_SETTLEMENT: "/api/ratan/stmcn/v1/cashflows",
  QUERY_DATA: "/api/ratan/v1/da/graphql",
  SUBSCRIBE_TRADES:
    ratanConfig.REACT_APP_SOCKET_URL_TRADES +
    "/api/ratan/socket/trades/subscriptions",
  SUBSCRIBE_EXCEPTIONS:
    ratanConfig.REACT_APP_SOCKET_URL_EXCEPTIONS +
    "/api/ratan/socket/exceptions/subscriptions",
  SUBSCRIBE_CASHFLOW:
    ratanConfig.REACT_APP_SOCKET_URL_CASHFLOW +
    "/api/ratan/socket/cashflows/subscriptions",
  SUBSCRIBE_CASHFLOW_SUB_STATUS:
    ratanConfig.REACT_APP_SOCKET_URL_SUB_STATUS +
    "/api/ratan/socket/cashflows/subStatus/subscriptions",
  QUERY_DA_GRAPHQL: "/api/ratan/da/graphql",
};

export const handleError =
  (url: string): ErrorHandler =>
  ({ graphQLErrors, networkError }) => {
    if (graphQLErrors) {
      graphQLErrors.forEach((item) => {
        const errorMessage = `Message: ${item.message}, Location: ${item.locations}, Path: ${item.path}`;
        if (
          !(
            Array.isArray(item?.path) &&
            (item?.path.some(
              (e: any) => e === "Confirmation.Confirmation_Workflow_Status"
            ) ||
              item?.path?.[0] === "graphCashFlowDetails")
          )
        ) {
          showErrorMsg(errorMessage);
        }
        logger.error(errorMessage);
      });
    }
    if (networkError) {
      const { statusCode, response } = networkError as any;
      if (statusCode === 401) {
        const errorMessage = `Error happened, pls login or check with support team. ${url}: API request failed ${statusCode}`;
        showErrorMsg(errorMessage);
        console.info(statusCode);
      } else if (response) {
        const errorMessage = `Error happened, service is unavailable, pls check with support team. ${url}: API request failed ${statusCode}`;
        showErrorMsg(errorMessage);
        logger.error(errorMessage);
      } else {
        const errorMessage = `Error happened, service is unavailable, pls check with support team. ${url}: API request failed ${statusCode}`;

        showErrorMsg(errorMessage);
        logger.error(errorMessage);
      }
    }
  };

const errorLink = (url: string) => {
  return onError(handleError(url));
};

export const queryHandler = (setErrorField) => (res: any) => {
  if (setErrorField && res.errors) {
    conversionGraphqlErrorField(res);
  }
  return res.data;
};

export const queryGraphql = (
  url: string,
  query: any,
  setErrorField?: boolean,
  headers = {}
) => {
  const httpLink = new HttpLink({
    uri: url,
  });

  const authMiddleware = new ApolloLink((operation, forward) => {
    // add the token to the headers
    const hooks = getHooks();
    operation.setContext({
      headers: {
        "Single-UI-Authorization": hooks.store?.token,
        // "Frontend-Version": "mfe",
        ...headers,
      },
    });
    return forward(operation);
  });

  const queryClient = new ApolloClient({
    link: from([authMiddleware, errorLink(url), httpLink]),
    cache: new InMemoryCache({
      addTypename: false,
    }),
    defaultOptions: {
      query: {
        fetchPolicy: "no-cache",
        errorPolicy: "all",
      },
    },
  });

  return queryClient
    .query({ query })
    .then(queryHandler(setErrorField))
    .finally(() => {
      ExtendTokenService(url);
    });
};

export const reconnectionAttempts = new Map<
  string,
  { num: number; updateTime: number }
>();
export const timeout = (url, query, next, error, complete, num) => () => {
  reconnectionAttempts.set(url, { num: num + 1, updateTime: 0 });
  subscribeGraphqlNotification(url, query, next, error, complete);
};
export const onDisconnected = (url, query, next, error, complete) => () => {
  const { num, updateTime } = reconnectionAttempts.get(url) || {
    num: 0,
    updateTime: 0,
  };
  console.info("onDisconnected", url, num, updateTime);
  if (num < 5 && new Date().getTime() - updateTime > 5000) {
    setTimeout(timeout(url, query, next, error, complete, num), num * 1000);
  } else if (num <= 5) {
    reconnectionAttempts.set(url, { num: 6, updateTime: 0 });
    logger.error(`Subscription error, url: ${url}`);
  }
};
export const onConnected = (url) => () => {
  const { num } = reconnectionAttempts.get(url) || { num: 0, updateTime: 0 };
  if (num <= 5) {
    reconnectionAttempts.set(url, {
      num: 0,
      updateTime: new Date().getTime(),
    });
  }
};
export const connectionParams = () => ({
  "Single-UI-Authorization": `${getHooks().store?.token}`,
});
export const nextWrap = (next) => (res: any) => {
  const data = res.data
    ? res.data.onExceptionEvent.payload
    : res.onExceptionEvent.payload;
  logger.info(
    `Receive exception notification: exceptionId: ${data.exceptionId}, exceptionCode: ${data.exceptionCode}`
  );
  next(res);
};
const subscribeGraphqlNotification = (
  url: string,
  query: any,
  next: (value: any) => void,
  error?: (error: any) => void,
  complete?: () => void
) => {
  const wsClient = new SubscriptionClient(`${url}`, {
    timeout: 60000,
    connectionParams,
  });
  const wsLink = new WebSocketLink(wsClient);
  // @ts-ignore
  wsLink.subscriptionClient.onDisconnected(
    onDisconnected(url, query, next, error, complete)
  );
  // @ts-ignore
  wsLink.subscriptionClient.onConnected(onConnected(url));

  const subscriptionClient = new ApolloClient({
    link: from([errorLink(url), wsLink]),
    cache: new InMemoryCache({
      addTypename: false,
    }),
  });

  subscriptionClient
    .subscribe({ fetchPolicy: "no-cache", query })
    .subscribe(nextWrap(next), error, complete);
};

interface GraphqlFilterProps {
  field: string;
  operator: string;
  values: string | string[];
}

interface QueryTradesProps {
  filters: GraphqlFilterProps[];
  quickFilterName: string;
  page?: number;
  api?: GridApi;
  instrumentConfig?: any;
  filtersString?: string;
}
export const queryTrades = async ({
  filters,
  quickFilterName,
  page = INITIAL_COUNT_SCROLL,
  api,
  instrumentConfig,
  filtersString,
}: QueryTradesProps) => {
  const newParams = [...filters];
  const { newFilters, onlyDefaultFilter } = dynamicDefaultFilter(newParams);
  let searchFilter = setSearchFilter(newFilters, onlyDefaultFilter);

  if (filtersString) {
    searchFilter = searchFilter.replace(
      'searchFilter: "',
      `searchFilter: "${filtersString} and `
    );
  }

  let res;
  if (api) {
    const columns = api.getAllDisplayedColumns();
    res = getDisplayFields(columns, ratanConfig.trades.tradeMandatoryFields);
  } else {
    const businessFields = await getBusinessFieldsFromCache("trade");
    res = conversionDQSLRequest({
      businessFields: businessFields?.tradeFields,
      isAllFields: true,
      instrumentConfig,
    });
  }

  const query = gql`
    query {
      trades(filter:[], ${searchFilter}, page: ${page}, size: ${SIZE_CONFIG_INFINITE_SCROLL}) {
        pageInfo {
          totalHits
          pageNo
          pageSize
          lastPage
        }
        results {
          ${res}
        }  
      }
    }
  `;

  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query, true);
};

interface QueryCustomTradeDataProps {
  filters: GraphqlFilterProps[];
  results: string;
  headers?: any;
}
export const queryCustomTradeData = ({
  filters,
  results,
  headers,
}: QueryCustomTradeDataProps) => {
  const { newFilters, onlyDefaultFilter } = dynamicDefaultFilter(filters);
  const searchFilter = setSearchFilter(newFilters, onlyDefaultFilter);

  const filter = newFilters.map((item) => {
    return `{field: "${item.field}", operator: ${
      item.operator
    }, values: ${JSON.stringify(item.values)}}`;
  });

  const query = gql`
    query {
      trades(filter: [${filter}], ${searchFilter}, page: 0, size: 50) {
        pageInfo {
          totalHits
          pageNo
          pageSize
          lastPage
        }
        results {
          ${results}
        }  
      }
    }
  `;

  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query, true, headers);
};

interface QueryTradeDetialsHeaderProps {
  filters: GraphqlFilterProps[];
  results: string;
}
export const queryTradeDetialsHeader = ({
  filters,
  results,
}: QueryTradeDetialsHeaderProps) => {
  const { newFilters, onlyDefaultFilter } = dynamicDefaultFilter(filters);
  const searchFilter = setSearchFilter(newFilters, onlyDefaultFilter);
  const query = gql`
    query {
      tradeHeaders(${searchFilter}) {
        pageInfo {
          totalHits
          pageNo
          pageSize
          lastPage
        }
        results {
          ${results}
        }
      }
    }
  `;

  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query, true);
};

export const queryTradeAllFields = async (
  filters: Filter[],
  instrumentConfig?: any
) => {
  const enableHeader = !!filters.find((item) => item.field === "Trade_Id");
  const headers = enableHeader
    ? {
        "DA-Header-With-Array": "true",
      }
    : {};
  const businessFields = await getBusinessFieldsFromCache("trade");
  const res = conversionDQSLRequest({
    businessFields: businessFields?.tradeFields,
    isAllFields: true,
    instrumentConfig,
  });

  const { newFilters, onlyDefaultFilter } = dynamicDefaultFilter(filters);
  const searchFilter = setSearchFilter(newFilters, onlyDefaultFilter);

  const filter = newFilters.map((item) => {
    return `{field: "${item.field}", operator: ${
      item.operator
    }, values: ${JSON.stringify(item.values)}}`;
  });

  const query = gql`
    query {
      trades(filter:[${filter}], ${searchFilter}, page: 0, size: 10) {
        pageInfo {
          totalHits
          pageNo
          pageSize
          lastPage
        }
        results {
          ${res}
        }  
      }
    }
  `;
  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query, undefined, headers);
};

// For version comparison and cashflow schedule
export const queryTradeVersionsData = async (
  filters: Filter[],
  instrumentConfig?: any,
  result?: string[]
) => {
  const businessFields = await getBusinessFieldsFromCache("trade");
  const { newFilters, onlyDefaultFilter } = dynamicDefaultFilter(filters);
  let res = "";
  if (result) {
    res = conversionResult(result);
  } else {
    res = conversionDQSLRequest({
      businessFields: businessFields?.tradeFields,
      isAllFields: true,
      instrumentConfig,
    });
  }
  const searchFilter = setSearchFilter(newFilters, onlyDefaultFilter);

  const query = gql`
    query {
      tradeVersions(${searchFilter}) {
        pageInfo {
          totalHits
          pageNo
          pageSize
          lastPage
        }
        results {
          ${res}
        }
      }
    }
  `;

  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query);
};

export const queryTradeAuditTrail = (tradeId: string) => {
  const query = gql`
    query {
      tradeAuditTrail(tradeId: "${tradeId}") {
        Trade_Id
        Tracking_Version
        Trade_Version
        Trade_Lake_Trade_Major_Version
        Trade_Lake_Trade_Minor_Version
        Action_Date_Time
        Action_Type
        User_PSID
        Source_System
        Source_System_Physical_Status
        Source_System_Validation_Status
        Trade_Status_Change {
          Status_Name
          Old_Status
          New_Status
        }
        Value_Change {
          Field_Name
          Old_Value
          New_Value
        }
      }
    }
  `;
  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query);
};

export const querySearch = async (
  params: string,
  from = INITIAL_COUNT_SCROLL,
  api?: GridApi
) => {
  let res;
  if (api) {
    const columns = api.getAllDisplayedColumns();
    res = getDisplayFields(columns, ratanConfig.trades.tradeMandatoryFields);
  } else {
    const businessFields = await getBusinessFieldsFromCache("trade");
    res = conversionDQSLRequest({
      businessFields: businessFields?.tradeFields,
      isAllFields: true,
    });
  }

  const query = gql`
    query {
      search(term: "${params}", entity: ALL, from: ${from}, size: ${SIZE_CONFIG_INFINITE_SCROLL}) {
        pageInfo {
          totalHits
          pageNo
          pageSize
          lastPage
        }
        trades {
          ${res}
        }
      }
    }
  `;
  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query, true);
};

export const queryFetchPortfolio = (searchTerm: string) => {
  const query = gql`
    query {
      fetchPortfolio (searchTerm: "${searchTerm}", size: 50) {
        Name
      }
    }
  `;
  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query);
};

export const queryCounterpartyDynamicList = (
  searchField: string,
  searchTerm: string
) => {
  const query = gql`
    query {
      referenceData(searchField: ${searchField}, searchTerm: "${searchTerm}", size: 50) {
        ${searchField}
      }
    }
  `;
  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query);
};

export const subscribeTrades = async (
  filters: GraphqlFilterProps[],
  quickFilterName: string,
  api: GridApi,
  next: (value: any) => void,
  error?: (error: any) => void,
  complete?: () => void
) => {
  const newParams = [...filters];
  const filter = newParams.map((item) => {
    return `{field: "${item.field}", operator: ${
      item.operator
    }, values: ${JSON.stringify(item.values)}}`;
  });

  const columns = api.getAllDisplayedColumns();
  const res = getDisplayFields(
    columns,
    ratanConfig.trades.tradeMandatoryFields
  );

  const query = gql`
    subscription {
      onTradeEvent(filter: [${filter}]) {
        payload {
          ${res}
        }
      }
    }
  `;
  const subUrl = graphqlUrl.SUBSCRIBE_TRADES;
  subscribeGraphqlNotification(subUrl, query, next, error, complete);
};

export const queryExceptionListV2 = (exceptionCodeList: string[]) => {
  const exceptionCode = exceptionCodeList.join(",");
  const query = gql`
    query {
      exceptionsV2(statusNotIn: "DISCARDED,REPLAYED,REPAIRED,AUTO_REPLAYED,AUTO_FIXED,IMS_FIXED,IMS_RECORDED", exceptionCode: "${exceptionCode}") {
        currentPage
        page
        size
        totalPages
        totalSizes
        data {
          exceptionId
          exceptionType
          exceptionCode
          eventRowKey
          createTimestamp
          lastModifyTimestamp
          exceptionStatus
          maker
          referenceId
          description
          exceptionOptions {
            optionId
            exceptionId
            exceptionOptionType
            optionDetails
          }
        }
      }
    }
  `;
  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query);
};

export const refreshExceptions = (exceptionIds: string[]) => {
  const exceptionIdsString = exceptionIds.join(",");
  const query = gql`
    query {
      exceptionsV2(exceptionId: "${exceptionIdsString}") {
        data {
          exceptionId
          exceptionType
          exceptionCode
          eventRowKey
          createTimestamp
          lastModifyTimestamp
          exceptionStatus
          maker
          referenceId
          description
          exceptionOptions {
            optionId
            exceptionId
            exceptionOptionType
            optionDetails
          }
        }
      }
    }
  `;

  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query);
};

export const subscribeException = (
  exceptionCodeList: string[],
  next: (value: any) => void,
  error?: (error: any) => void,
  complete?: () => void
) => {
  const query = gql`
    subscription {
      onExceptionEvent(filter: [{ field: "exceptionType", operator: IN, values: ["BUSINESS", "VISIBLE"]}, {field: "exceptionCode", operator: IN, values: ${JSON.stringify(
        exceptionCodeList
      )}}]) {
        payload {
          exceptionId
          exceptionType
          exceptionCode
          eventRowKey
          createTimestamp
          lastModifyTimestamp
          exceptionStatus
          maker
          referenceId
          description
          exceptionOptions {
            optionId
            exceptionId
            exceptionOptionType
            optionDetails
          }
        }
      }
    }
  `;
  const subUrl = graphqlUrl.SUBSCRIBE_EXCEPTIONS;
  subscribeGraphqlNotification(subUrl, query, next, error, complete);
};

// isOld means not use Counterparty Details V2 api
export const queryCounterPartyDetails = (fmId: any, isOld?: boolean) => {
  let query: any = "";
  if (getEnable("Counterparty_Detail_V2") && !isOld) {
    // const str1 = `legalEntity(leId: ${leId}){`;
    const str2 = `fmEntity(fmId: ${fmId}){`;
    const str = counterpartyQueryStr.replace("fmEntity{", str2);
    query = gql`query {
          ${str}
        }`;
  } else {
    query = gql`query {
        counterPartyDetails(fm_profile_sys_gen_id: "${fmId}") {
          fm_profile_sys_gen_id
          fpi_le_id
          fla_address_line_1
          fla_address_line_2
          fla_state
          fla_city
          fla_post_code
          lmp_long_name
          lmp_inc_cntry_iso_code
          lsp_dmcl_cntry_iso_code
          lri_reg_field_text
        }
      }`;
  }

  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query);
};

export const queryCounterPartyDetails_CN = (fmId: string) => {
  fmId = Number.isNaN(Number(fmId)) ? `"${fmId}"` : fmId;
  const str2 = `fmEntity(fmId: ${fmId}){`;
  const str = counterpartyQueryStrForCN.replace("fmEntity{", str2);
  const query = gql`query {
        ${str}
      }`;

  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query);
};

const disabledDefaultFilter = [
  "Cashflow.Cashflow_State",
  "Cashflow.Cashflow_Id",
];
export const judgeDefaultFilter = (
  disabledDefault: boolean | undefined,
  filters: GraphqlFilterProps[]
) => {
  if (disabledDefault) {
    return true;
  } else if (disabledDefault === false) {
    return false;
  } else if (
    filters.some((item) => disabledDefaultFilter.includes(item.field))
  ) {
    return true;
  }
  return false;
};

interface QueryCashflowEvent {
  filters: GraphqlFilterProps[];
  page?: number;
  columnDefs?: ColDef[];
  api?: GridApi;
  disabledDefault?: boolean;
  isCashflowSettlementCN?: boolean;
}
export const queryCashflow = async ({
  filters,
  page = PAGE_NUMBER_FOR_CASHFLOW,
  columnDefs,
  api,
  disabledDefault,
  isCashflowSettlementCN,
}: QueryCashflowEvent) => {
  holidayDB?.clear();

  const newFilters = handleMultiFieldsQuery(filters);
  const df = isCashflowSettlementCN
    ? CASHFLOW_DEFAULT_FILTER_CN
    : CASHFLOW_DEFAULT_FILTER;
  const newParams = judgeDefaultFilter(disabledDefault, newFilters)
    ? newFilters
    : [...df, ...newFilters];

  const filter = newParams.map((item) => {
    return `{field: "${item.field}", operator: ${
      item.operator
    }, values: ${JSON.stringify(item.values)}}`;
  });

  let res;
  if (columnDefs) {
    res = getDisplayFields(
      columnDefs,
      isCashflowSettlementCN
        ? ratanConfig.cashflow.cashflowSettlementMandatoryFields
        : ratanConfig.cashflow.cashflowMandatoryFields
    );
  } else if (api) {
    const columns = api.getAllDisplayedColumns();
    res = getDisplayFields(
      columns,
      isCashflowSettlementCN
        ? ratanConfig.cashflow.cashflowSettlementMandatoryFields
        : ratanConfig.cashflow.cashflowMandatoryFields
    );
  } else {
    const businessFields = await getBusinessFieldsFromCache(
      isCashflowSettlementCN ? "cashflowCN" : "cashflow"
    );
    res = conversionDQSLRequest({
      businessFields: businessFields?.cashflowFields,
      isAllFields: true,
    });
  }

  const searchFilter = isCashflowSettlementCN
    ? ""
    : setSearchFilter(newParams, "", true);
  const pendingCount = !isCashflowSettlementCN ? "pendingCount" : "";

  const query = gql`
    query {
      cashflows${
        isCashflowSettlementCN ? "New" : ""
      }(filter: [${filter}], ${searchFilter}, page: ${page}, size: ${PAGE_SIZE_FOR_CASHFLOW}) {
        pageInfo {
          totalHits
          pageNo
          pageSize
          lastPage
          ${pendingCount}
        }
        results {
          ${res}
        }
      }
    }
  `;

  const queryUrl = isCashflowSettlementCN
    ? graphqlUrl.QUERY_CASHFLOW_SETTLEMENT
    : graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query, true);
};

interface QueryComponentCashflowProps {
  filters: GraphqlFilterProps[];
  page?: number;
  columnDefs?: ColDef[];
  api?: GridApi;
  isCashflowSettlementCN?: boolean;
}
// copied from query cashflow, used in CN to search against netted/component cashflows.
export const queryComponentCashflows = async ({
  filters,
  page = PAGE_NUMBER_FOR_CASHFLOW,
  columnDefs,
  api,
  isCashflowSettlementCN,
}: QueryComponentCashflowProps) => {
  const newFilters = handleMultiFieldsQuery(filters);
  const df = isCashflowSettlementCN
    ? CASHFLOW_DEFAULT_FILTER_CN
    : CASHFLOW_DEFAULT_FILTER;
  const newParams = judgeDefaultFilter(true, newFilters)
    ? newFilters
    : [...df, ...newFilters];

  const filter = newParams.map((item) => {
    return `{field: "${item.field}", operator: ${
      item.operator
    }, values: ${JSON.stringify(item.values)}}`;
  });

  let res;
  if (columnDefs) {
    res = getDisplayFields(
      columnDefs,
      ratanConfig.cashflow.cashflowSettlementMandatoryFields
    );
  } else if (api) {
    const columns = api.getAllDisplayedColumns();
    res = getDisplayFields(
      columns,
      ratanConfig.cashflow.cashflowSettlementMandatoryFields
    );
  } else {
    const businessFields = await getBusinessFieldsFromCache("cashflowCN");
    res = conversionDQSLRequest({
      businessFields: businessFields?.cashflowFields,
      isAllFields: true,
    });
  }

  const query = gql`
    query {
      componentCashflow(filter: [${filter}], page: ${page}, size: ${PAGE_SIZE_FOR_CASHFLOW}) {
        pageInfo {
          totalHits
          pageNo
          pageSize
          lastPage
        }
        results {
          ${res}
        }
      }
    }
  `;

  const queryUrl = graphqlUrl.QUERY_CASHFLOW_SETTLEMENT;
  return queryGraphql(queryUrl, query, true);
};

export const queryCashflowCount = (
  filters: FilterItem[],
  isCashflowSettlementCN?: boolean
) => {
  const filter = filters.map((item) => {
    return `{field: "${item.field}", operator: ${
      item.operator
    }, values: ${JSON.stringify(item.values)}}`;
  });

  const query = gql`
    query {
      cashflows${
        isCashflowSettlementCN ? "New" : ""
      }(filter: [${filter}], page: ${PAGE_NUMBER_FOR_CASHFLOW}, size: ${PAGE_SIZE_FOR_CASHFLOW}) {
        pageInfo {
          totalHits
          pageNo
          pageSize
          lastPage
        }
        results {
          Cashflow{
            Cashflow_Id
          }
        }
      }
    }
  `;

  const queryUrl = isCashflowSettlementCN
    ? graphqlUrl.QUERY_CASHFLOW_SETTLEMENT
    : graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query, true);
};

export const queryCashflowPendingManualAmount = (
  isCashflowSettlementCN?: boolean
) => {
  const newParams = isCashflowSettlementCN
    ? [...CASHFLOW_DEFAULT_FILTER, ...CASHFLOW_SUB_STATUS]
    : [...CASHFLOW_DEFAULT_FILTER, ...CASHFLOW_SUB_STATUS_BAU];

  const filter = newParams.map((item) => {
    return `{field: "${item.field}", operator: ${
      item.operator
    }, values: ${JSON.stringify(item.values)}}`;
  });

  const query = gql`
    query {
      cashflows${
        isCashflowSettlementCN ? "New" : ""
      }(filter: [${filter}], page: ${PAGE_NUMBER_FOR_CASHFLOW}, size: ${PAGE_SIZE_FOR_CASHFLOW}) {
        pageInfo {
          totalHits
          pageNo
          pageSize
          lastPage
        }
        results {
          Cashflow{
            Cashflow_Id
          }
        }
      }
    }
  `;

  const queryUrl = isCashflowSettlementCN
    ? graphqlUrl.QUERY_CASHFLOW_SETTLEMENT
    : graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query, true);
};

export const subscribeCashflow = async (
  filters: GraphqlFilterProps[],
  api: GridApi,
  next: (value: any) => void,
  error?: (error: any) => void,
  complete?: () => void,
  isCashflowSettlementCN?: boolean
) => {
  const newParams = [...CASHFLOW_DEFAULT_FILTER, ...filters];

  const filter = newParams.map((item) => {
    return `{field: "${item.field}", operator: ${
      item.operator
    }, values: ${JSON.stringify(item.values)}}`;
  });

  const columns = api.getAllDisplayedColumns();
  const res = getDisplayFields(
    columns,
    isCashflowSettlementCN
      ? ratanConfig.cashflow.cashflowSettlementMandatoryFields
      : ratanConfig.cashflow.cashflowMandatoryFields
  );

  const query = gql`
    subscription {
      onCashflowEvent(filter: [${filter}]) {
        payload {
          ${res}
        }
      }
    }
  `;
  const subUrl = graphqlUrl.SUBSCRIBE_CASHFLOW;
  subscribeGraphqlNotification(subUrl, query, next, error, complete);
};

export const queryCashFlowAuditTrail = (
  cashflowId: string,
  isCashflowSettlementCN?: boolean
) => {
  const query = gql`
    query {
      cashflowAuditTrail${
        isCashflowSettlementCN ? "New" : ""
      }(cashflowId: "${cashflowId}") {
        Action_Date_Time
        User_PSID
        ${
          isCashflowSettlementCN
            ? `
          Cashflow {
            Cashflow_Id
            Cashflow_State
            Cashflow_Sub_State_Type
            Cashflow_Sub_State
            Cashflow_Business_Version
            Cashflow_Version
            Cashflow_Minor_Version
            Cashflow_Event_Type
            Exception_Reason
            NSTP_Reason
          }
          FMO_Comments {
            FMO_Comment
            FMO_Comment_Timestamp
            FMO_Comment_Updater
          }`
            : `
            Version
            Cashflow_Id
            Cashflow_Status
            Cashflow_Sub_Status_Type
            Cashflow_Sub_Status
            Cashflow_Business_Version
            Cashflow_Version
            Cashflow_Ratan_Version
            Cashflow_Event_Type
            Exception_Code
            NSTP_Code`
        }
        Action
        Action_Time
        Exception_Type
        Value_Change {
          Field_Name
          Old_Value
          New_Value
        }
        Comments_Change {
          Field_Name
          Old_Value {
            FMO_Comment
            FMO_Comment_Updater
            FMO_Comment_Timestamp
          }
          New_Value {
            FMO_Comment
            FMO_Comment_Updater
            FMO_Comment_Timestamp
          }
        }  
      }
    }
  `;

  const queryUrl = isCashflowSettlementCN
    ? graphqlUrl.QUERY_CASHFLOW_SETTLEMENT
    : graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query);
};

export const queryCashFlowDetails = (
  cashflowId: string
): Promise<{ graphCashFlowDetails: GraphqlCashflowDetails }> => {
  const query = gql`
    query {
      graphCashFlowDetails(cashflowId: "${cashflowId}") {
        cashflow {
          BCS_Parent_Trade_Id
          BCS_Trade_Id
          Delivery_Method
          Parent_Trade_Id
          Position_Id
          Settlement_Method
          Trade_Id
          Trade_State
          Trade_Version
          Cashflow {
            Cashflow_Id
            Cashflow_Business_Version
            Cashflow_Version
            Cashflow_State
            Cashflow_Affirmation_Status
            Cashflow_Event_Type
            Cashflow_Minor_Version
            Payment_Currency
            Payment_Date
            Payment_Type
            Payment_Cutoff_Time
            Pay_Receive_Indicator
            Payment_Amount
            Netting_Id
            Netting_Cuttoff_Date
            Payment_Receiver_Party_Reference
            Payment_Payer_Party_Reference
            Cashflow_Sub_State
            Cashflow_Sub_State_Type
            Cashflow_Sub_State_Updater
            Status_Event_Type
            Event_Date
            Cashflow_Event_Reason
            Booking_System_Event
          }
          FMO_Comments {
            FMO_Comment
            FMO_Comment_Timestamp
            FMO_Comment_Updater
          }
          Confirmation {
            Confirmation_Status
          }
          Entity {
            Booking_Entity_SCI_FMCODE
            Booking_Entity_SCI_FMID
            Counterparty_SCI_FMID
            Counterparty_SCI_FMCODE
            Counterparty_CIF_Code
            Counterparty_Source_System_Entity_Id
            General_Ledger_Business_Unit_Name
            Booking_Entity_General_Ledger_Business_Unit_Id
          }
          Instrument_Common {
            CFI_Code
            ISDA_Taxonomy
            Source_System_Instrument_Sub_Type
          }
          Settlement_Instruction {
            Account {
              SCB_Nostro_Account_Number
              SCB_Nostro_Account_Type
              Beneficiary_BIC_code
              Beneficiary_Account_Name
              Beneficiary_Account_Name_2
              Beneficiary_Street_Address
              Beneficiary_City
              Beneficiary_Account_Number
              Intermediary_BIC_code
              Intermediary_Account_Name
              Intermediary_Street_Address
              Intermediary_City
              Intermediary_Account_Number
              Beneficiary_Bank_BIC_code
              Beneficiary_Bank_Account_Name
              Beneficiary_Bank_Street_Address
              Beneficiary_Bank_City
              Beneficiary_Bank_Account_Number
              Beneficiary_Correspondent_BIC_code
              Beneficiary_Correspondent_Account_Name
              Beneficiary_Correspondent_Street_Address
              Beneficiary_Correspondent_City
              Beneficiary_Correspondent_Account_Number
              Ordering_Customer_BIC_Code
              Ordering_Customer_Account_Name
              Ordering_Customer_Street_Address
              Ordering_Customer_City
              Ordering_Customer_Account_Number
              Counterparty_CMS_Account_Number
              EBBS_Bridge_Account_Number
              EBBS_Account_Number
              Booking_Entity_Correspondent_BIC_code
              Booking_Entity_Correspondent_Account_Name
              Booking_Entity_Correspondent_Street_Address
              Booking_Entity_Correspondent_City
              Booking_Entity_Correspondent_Account_Number
            }
            SSI_Id
            SSI_Unique_Id
            SSI_Source
            SSI_Priority
            Settlement_Code
            Swift_Message_Type
            CFI_Code
            Payment_Currency
            Counterparty_SCI_FMID
            SCB_Entity_SCI_FMID
            Remittance_Information_1
            Remittance_Information_2
            Remittance_Information_3
            Remittance_Information_4
            Sender_To_Receiver_Information_1
            Sender_To_Receiver_Information_2
            Sender_To_Receiver_Information_3
            Sender_To_Receiver_Information_4
            Sender_To_Receiver_Information_5
            Sender_To_Receiver_Information_6
            Is_Third_Party_Payment
            Swift_Payment_Method
            Swift_Payment_Date
            Charge_Bearer
            Nostro_Swift_Message_Type
          }
          Portfolio {
            Booking_Entity_Trade_Portfolio_Name
          }
          Data_Flow {
            Data_Source_System
          }
        }
        cashflowAuditTrail {
          Action_Date_Time
          User_PSID
          Cashflow {
            Cashflow_Id
            Cashflow_State
            Cashflow_Sub_State_Type
            Cashflow_Sub_State
            Cashflow_Business_Version
            Cashflow_Version
            Cashflow_Minor_Version
            Cashflow_Event_Type
            Exception_Reason
            NSTP_Reason
          }
          FMO_Comments {
            FMO_Comment
            FMO_Comment_Timestamp
            FMO_Comment_Updater
          }
          Action
          Action_Time
          Exception_Type
          Value_Change {
            Field_Name
            Old_Value
            New_Value
          }
          Comments_Change {
            Field_Name
            Old_Value {
              FMO_Comment
              FMO_Comment_Updater
              FMO_Comment_Timestamp
            }
            New_Value {
              FMO_Comment
              FMO_Comment_Updater
              FMO_Comment_Timestamp
            }
          }
        }
        ratanException {
          Id
          Original_Exception_Id
          Exception_Code
          Exception_Category
          Exception_Type
          Description
          Status
          Actions {
            Api_Url
            Api_Method
            Action_Name
            Action_Type
            Component_Url
            Component_Name
          }
          Stashing {
            Request_Body
            Maker_Id
          }
        }
                
        ratanVostroCandidates {
          Account {
            SCB_Nostro_Account_Number
            SCB_Nostro_Account_Type
            Beneficiary_BIC_code
            Beneficiary_Account_Name
            Beneficiary_Account_Name_2
            Beneficiary_Street_Address
            Beneficiary_City
            Beneficiary_Account_Number
            Intermediary_BIC_code
            Intermediary_Account_Name
            Intermediary_Street_Address
            Intermediary_City
            Intermediary_Account_Number
            Beneficiary_Bank_BIC_code
            Beneficiary_Bank_Account_Name
            Beneficiary_Bank_Street_Address
            Beneficiary_Bank_City
            Beneficiary_Bank_Account_Number
            Beneficiary_Correspondent_BIC_code
            Beneficiary_Correspondent_Account_Name
            Beneficiary_Correspondent_Street_Address
            Beneficiary_Correspondent_City
            Beneficiary_Correspondent_Account_Number
            Ordering_Customer_BIC_Code
            Ordering_Customer_Account_Name
            Ordering_Customer_Street_Address
            Ordering_Customer_City
            Ordering_Customer_Account_Number
            Counterparty_CMS_Account_Number
            EBBS_Bridge_Account_Number
            EBBS_Account_Number
            Booking_Entity_Correspondent_BIC_code
            Booking_Entity_Correspondent_Account_Name
            Booking_Entity_Correspondent_Street_Address
            Booking_Entity_Correspondent_City
            Booking_Entity_Correspondent_Account_Number
          }
          SSI_Id
          SSI_Unique_Id
          SSI_Source
          SSI_Priority
          Settlement_Code
          Swift_Message_Type
          CFI_Code
          Payment_Currency
          Counterparty_SCI_FMID
          SCB_Entity_SCI_FMID
          Remittance_Information_1
          Remittance_Information_2
          Remittance_Information_3
          Remittance_Information_4
          Sender_To_Receiver_Information_1
          Sender_To_Receiver_Information_2
          Sender_To_Receiver_Information_3
          Sender_To_Receiver_Information_4
          Sender_To_Receiver_Information_5
          Sender_To_Receiver_Information_6
          Is_Third_Party_Payment
          Swift_Payment_Method
          Swift_Payment_Date
          Charge_Bearer
          Nostro_Swift_Message_Type
          BranchId_Murex3Id
        }
        ratanNostroCandidates {
          Account {
            SCB_Nostro_Account_Number
            SCB_Nostro_Account_Type
            Beneficiary_BIC_code
            Beneficiary_Account_Name
            Beneficiary_Account_Name_2
            Beneficiary_Street_Address
            Beneficiary_City
            Beneficiary_Account_Number
            Intermediary_BIC_code
            Intermediary_Account_Name
            Intermediary_Street_Address
            Intermediary_City
            Intermediary_Account_Number
            Beneficiary_Bank_BIC_code
            Beneficiary_Bank_Account_Name
            Beneficiary_Bank_Street_Address
            Beneficiary_Bank_City
            Beneficiary_Bank_Account_Number
            Beneficiary_Correspondent_BIC_code
            Beneficiary_Correspondent_Account_Name
            Beneficiary_Correspondent_Street_Address
            Beneficiary_Correspondent_City
            Beneficiary_Correspondent_Account_Number
            Ordering_Customer_BIC_Code
            Ordering_Customer_Account_Name
            Ordering_Customer_Street_Address
            Ordering_Customer_City
            Ordering_Customer_Account_Number
            Counterparty_CMS_Account_Number
            EBBS_Bridge_Account_Number
            EBBS_Account_Number
            Booking_Entity_Correspondent_BIC_code
            Booking_Entity_Correspondent_Account_Name
            Booking_Entity_Correspondent_Street_Address
            Booking_Entity_Correspondent_City
            Booking_Entity_Correspondent_Account_Number
          }
          SSI_Id
          SSI_Unique_Id
          SSI_Source
          SSI_Priority
          Swift_Message_Type
          CFI_Code
          Payment_Currency
          Counterparty_SCI_FMID
          SCB_Entity_SCI_FMID
          Remittance_Information_1
          Remittance_Information_2
          Remittance_Information_3
          Remittance_Information_4
          Sender_To_Receiver_Information_1
          Sender_To_Receiver_Information_2
          Sender_To_Receiver_Information_3
          Sender_To_Receiver_Information_4
          Sender_To_Receiver_Information_5
          Sender_To_Receiver_Information_6
          Is_Third_Party_Payment
          Swift_Payment_Method
          Swift_Payment_Date
          Charge_Bearer
          Nostro_Swift_Message_Type
        }
        ratanAffirmation {
          Affirmed_By
          Phone_Email
          Affirmed_At
        }    
      }
    }
  `;

  const queryUrl = graphqlUrl.QUERY_CASHFLOW_SETTLEMENT;
  return queryGraphql(queryUrl, query);
};

interface QueryGroupMessagesProps {
  filter: { [k: string]: string | number | boolean };
  pagination: {
    pageNo: number;
    pageSize: number;
  };
}
export const queryGroupMessages: (
  p: QueryGroupMessagesProps
) => Promise<any> = ({ filter, pagination: { pageNo, pageSize } }) => {
  const filterCriterias = Object.keys(filter)
    .map((k) => (filter[k] ? `${k}: ${JSON.stringify(filter[k])}` : ""))
    .filter(Boolean)
    .join(", ");
  const filterStr = filterCriterias ? `, filter:{ ${filterCriterias} }` : "";
  const query = gql`
    query {
      groupMessages(page:${pageNo},size:${pageSize}${filterStr}){
        pageInfo{
          pageNo
          pageSize
          lastPage
          totalHits
        }
        results{
          Id
          Group_Id
          Trade_Id
          Cashflow_Id
          Group_Event
          Group_Status
          Booking_System_Event
          Status
          Cashflow_Count
          Cashflow_Sequence
          Cashflow_Event_Reason
          Create_At
          Update_At
          Is_Group_Locked
          Major_Version
          ratanException{
            Description
          }
        }
      }
    }
  `;

  const queryUrl = graphqlUrl.QUERY_CASHFLOW_SETTLEMENT;
  return queryGraphql(queryUrl, query);
};

export const queryFmidOrCounterpartyList = (searchTerm: string) => {
  const query = gql`
    query {
      searchCounterParty(searchTerm: "${searchTerm}") {
        fm_profile_sys_gen_id
        lmp_long_name
      }
    }
  `;
  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query);
};

export const subscribeSubStatusCashflow = async (
  filters: GraphqlFilterProps[],
  next: (value: any) => void,
  error?: (error: any) => void,
  complete?: () => void
) => {
  const componentCashflowFilter = [
    {
      field: "cashflowId",
      operator: "NE",
      values: ["000000"],
    },
  ];
  const newParams = [...componentCashflowFilter, ...filters];

  const filter = newParams.map((item) => {
    return `{field: "${item.field}", operator: ${
      item.operator
    }, values: ${JSON.stringify(item.values)}}`;
  });

  const query = gql`
    subscription {
      onSubStatusEvent(filter: [${filter}]) {
        payload {
          cashflowId
          businessVersion
          updater
          requestSource
          action
          nstpFlag
          nstpReason
        }
      }
    }
  `;
  const subUrl = graphqlUrl.SUBSCRIBE_CASHFLOW_SUB_STATUS;
  subscribeGraphqlNotification(subUrl, query, next, error, complete);
};

export const queryCashflowDialogTradeDetail = async (
  filters: GraphqlFilterProps[],
  fields = ratanConfig.cashflow.tradeDetailsResultInCashflow
) => {
  const newParams = [...filters];

  const filter = newParams.map((item) => {
    return `{field: "${item.field}", operator: ${
      item.operator
    }, values: ${JSON.stringify(item.values)}}`;
  });

  const query = gql`
    query {
      trades(filter: [${filter}], page: 0, size: 10) {
        pageInfo {
          totalHits
          pageNo
          pageSize
          lastPage
        }
        results {
          ${conversionResult(fields)}
        }  
      }
    }
  `;
  const queryUrl = graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query);
};

export const queryCashflowDialogCashflowDetail = (
  filters: GraphqlFilterProps[],
  isCashflowSettlementCN?: boolean
) => {
  const searchFilter =
    isCashflowSettlementCN || setSearchFilter(filters, "", true);
  const filter = filters.map((item) => {
    return `{field: "${item.field}", operator: ${
      item.operator
    }, values: ${JSON.stringify(item.values)}}`;
  });
  const query = gql`
    query {
      cashflows(filter: [${filter}], ${searchFilter}, page: 0, size: 1) {
        pageInfo {
          totalHits
          pageNo
          pageSize
          lastPage
        }
        results {
          ${conversionResult(
            isCashflowSettlementCN
              ? ratanConfig.cashflow.cashflowSettlementDetailsResultInCashflow
              : ratanConfig.cashflow.cashflowDetailsResultInCashflow
          )}
        }
      }
    }
  `;

  const queryUrl = isCashflowSettlementCN
    ? graphqlUrl.QUERY_CASHFLOW_SETTLEMENT
    : graphqlUrl.QUERY_DA_GRAPHQL;
  return queryGraphql(queryUrl, query, true);
};
