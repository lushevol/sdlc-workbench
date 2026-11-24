export interface ContainerProps {
  children?: React.ReactNode;
  module: string;
  tile: string;
}

export enum CONTAINER_MENU {
  TRADE_BLOTTER = "/trade_blotter",
  CASHFLOW_BLOTTER = "/cashflow_blotter",
  EXCEPTIONS_BLOTTER = "/exceptions_blotter",
  RULES_BLOTTER = "/rules_blotter",
  AUTHORIZATION_LIMITS_CONTAINER = "/authorization_limits_container",
  NOSTRO_STATIC = "/nostro_static",
}

export enum TILE_MENU {
  TRADE = "/trade",
  CASHFLOW_CN = "/cashflow_cn",
  CASHFLOW_BAU = "/cashflow_bau",
  SETTLEMENT_EXCEPTIONS = "/settlement",
  VALIDATION_EXCEPTIONS = "/validation",
  ISO_EXCEPTIONS = "/iso_exception",
  NEW_NSTP_RULES = "/new_nstp_rules",
  NEW_NETTING_RULES = "/new_netting_rules",
  SETTLEMENT_NSTP_RULES = "/settlement_nstp_rules",
  SUPPRESSION_RULES = "/suppression_rules",
  NETTING_RULES = "/netting_rules",
  AUTHORIZATION_LIMITS = "/authorization_limits",
  NOSTRO_STATIC = "/nostro_static",
}

export enum APPLICATION_MENU {
  TRADE_BLOTTER = "/trade_blotter/*",
  CASHFLOW_BLOTTER = "/cashflow_blotter/*",
  CASHFLOW_BLOTTER_CN = "/cashflow_blotter_cn/*",
  EXCEPTIONS_BLOTTER = "/exceptions_blotter/*",
  RULES_BLOTTER = "/rules_blotter/*",
  AUTHORIZATION_LIMITS_CONTAINER = "/authorization_limits_container/*",
  NOSTRO_STATIC_CONTAINER = "/nostro_static_container/*",
}
