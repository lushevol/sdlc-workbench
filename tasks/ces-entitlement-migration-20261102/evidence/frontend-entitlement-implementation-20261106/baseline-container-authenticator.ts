import { Hooks } from "../Root/import";
const { getHooks } = Hooks;

const X_RATANONE = "X_RATANONE";

export const getUser = () => {
  const hooks = getHooks();

  const entities = hooks.store?.entities;
  let entitlements = hooks.store?.user?.entitlements;
  let role =
    hooks.store?.user?.entitlement?.dataEntitlementRoles ||
    hooks.store?.user?.entitlement?.role;

  if (entities) {
    entitlements = {};
    entities.forEach((item) => {
      const entity = {};
      entitlements[item.name] = entity;
      item.subjects.forEach((subject) => {
        entity[subject.name] = subject.actions.map((action) => action.name);
      });
      if (item.name === X_RATANONE) {
        role = item.roleName;
      }
    });
  }

  return {
    id: hooks.store?.user?.id,
    name: hooks.store?.user?.fullName,
    role: role,
    actions: hooks.store?.user?.entitlement?.actions,
    entitlements: entitlements,
  };
};

export const hasPermission = (module: string) => {
  const user = getUser();

  if (user && user.actions && user.actions.includes(module)) {
    return true;
  }
  const moduleArr = module.split(":");
  const [subject, action] = moduleArr;
  const { entitlements } = user;

  /**
   * @author Tech
   * @description to cover login v2 logic
   */
  if (entitlements) {
    /**
     * @description To get X_RATANONE user permission
     *  */
    const userXratanonEntityName = Object.keys(entitlements).find(
      (value) => value.indexOf("X_RATANONE") > -1
    );

    if (userXratanonEntityName) {
      const ratanoneEntitlement = entitlements[userXratanonEntityName];
      const availavleActions: string[] = ratanoneEntitlement[subject] || [];
      const idx = availavleActions.findIndex((value) => value === action);
      /**
       * if actions set to role
       *  */
      if (idx != -1) {
        return true;
      }
      // X_RATAONE actions check end
      return false;
    }

    /**
     * @description if no X_RATANONE entity will try to get Legency Entity configs
     *  */
    const userEms2EntityNameOnEntity = Object.keys(entitlements).find(
      (value) => value.indexOf(subject) > -1
    );

    if (userEms2EntityNameOnEntity) {
      const entityOnly = entitlements[userEms2EntityNameOnEntity];
      /**
       * Subject Name can conervet to Entity Name
       * NSTP ruls subject and entity is different
       */
      let key: string | undefined;
      if (subject === "RATAN_SETTLEMENT_STP_RULE") {
        key = "RATAN Settlement NSTP Rule";
      } else {
        key = Object.keys(entityOnly).find(
          (v) => v.toLocaleUpperCase().replace(/\s/g, "_") === subject
        );
      }

      if (key) {
        const actions: string[] = entityOnly[key];
        if (action && actions.findIndex((v) => v === action) >= 0) {
          return true;
        }
      }
    }
  }

  return false;
};

/* 
  Auth: Tech
  Temporary remove dependency from ratanexception/config/dataGridConfig
  And will find solution to config keys 
*/
const EXCEPTIONS_TYPE = {
  MIDDLE_OFFICE_PROCESS: "MIDDLE_OFFICE_PROCESS",
  VALIDATION_INTERFACE: "VALIDATION_INTERFACE",
  VALIDATION_DATA_ENRICHMENT: "VALIDATION_DATA_ENRICHMENT",
  VALIDATION_CLIENT_DATA: "VALIDATION_CLIENT_DATA",
  VALIDATION_PROCESS: "VALIDATION_PROCESS",
  VALIDATION: "VALIDATION",
  SETTLEMENTS_INTERFACE: "SETTLEMENTS_INTERFACE",
  SETTLEMENTS_CLIENT_DATA: "SETTLEMENTS_CLIENT_DATA",
  SETTLEMENTS_PROCESS: "SETTLEMENTS_PROCESS",
  ISO_EXCEPTION: "ISO_PROCESS_EXCEPTION",
};

const veryfyMOExceptionTypeFilter = (type: string) => {
  return (
    type === EXCEPTIONS_TYPE.VALIDATION_INTERFACE ||
    type === EXCEPTIONS_TYPE.VALIDATION_DATA_ENRICHMENT ||
    type === EXCEPTIONS_TYPE.VALIDATION_CLIENT_DATA ||
    type === EXCEPTIONS_TYPE.VALIDATION_PROCESS ||
    type === EXCEPTIONS_TYPE.VALIDATION
  );
};
const veryfySetllmentExceptionTypeFilter = (type: string) => {
  return (
    type === EXCEPTIONS_TYPE.SETTLEMENTS_INTERFACE ||
    type === EXCEPTIONS_TYPE.SETTLEMENTS_CLIENT_DATA ||
    type === EXCEPTIONS_TYPE.SETTLEMENTS_PROCESS
  );
};
const veryfyISOExceptionTypeFilter = (type: string) => {
  return type === EXCEPTIONS_TYPE.ISO_EXCEPTION;
};

export const hasPrivatePermission = (type: string = "") => {
  // middle office tabS
  if (type === EXCEPTIONS_TYPE.MIDDLE_OFFICE_PROCESS) {
    return hasPermission("RATAN_MO_EXCEPTION:F_Custom_View_Builder_Private");
  }
  // validation tab
  if (veryfyMOExceptionTypeFilter(type)) {
    return hasPermission(
      "RATAN_VALIDATION_EXCEPTION:F_Custom_View_Builder_Private"
    );
  }
  // settlement tab
  if (veryfySetllmentExceptionTypeFilter(type)) {
    return hasPermission(
      "RATAN_SETTLEMENT_EXCEPTION:F_Custom_View_Builder_Private"
    );
  }
  // trade blotter page
  if (type === "TRADE_VIEW_BUILDER") {
    return hasPermission("RATAN_TRADE_BLOTTER:F_Custom_View_Builder_Private");
  }
  // cashflow blotter page
  if (type === "CASHFLOW_VIEW_BUILDER" || type === "CASHFLOW_CN_VIEW_BUILDER") {
    return (
      hasPermission("RATAN_CASHFLOW_BLOTTER:F_Custom_View_Builder_Private") ||
      hasPermission(
        "RATAN_STRATEGIC_CASHFLOW_BLOTTER:F_Custom_View_Builder_Private"
      )
    );
  }
  // iso exception tab
  if (type === EXCEPTIONS_TYPE.ISO_EXCEPTION) {
    return hasPermission("RATAN_KR_EXCEPTION:F_Custom_View_Builder_Private");
  }
  return hasPermission(`${type}:F_Custom_View_Builder_Private`);
};

export const hasPublicPermission = (type: string = "") => {
  // middle office tab
  if (type === EXCEPTIONS_TYPE.MIDDLE_OFFICE_PROCESS) {
    return hasPermission("RATAN_MO_EXCEPTION:F_Custom_View_Builder_Public");
  }
  // validation tab
  if (veryfyMOExceptionTypeFilter(type)) {
    return hasPermission(
      "RATAN_VALIDATION_EXCEPTION:F_Custom_View_Builder_Public"
    );
  }
  // settlement tab
  if (veryfySetllmentExceptionTypeFilter(type)) {
    return hasPermission(
      "RATAN_SETTLEMENT_EXCEPTION:F_Custom_View_Builder_Public"
    );
  }
  // trade blotter page
  if (type === "TRADE_VIEW_BUILDER") {
    return hasPermission("RATAN_TRADE_BLOTTER:F_Custom_View_Builder_Public");
  }
  // cashflow blotter page
  if (type === "CASHFLOW_VIEW_BUILDER" || type === "CASHFLOW_CN_VIEW_BUILDER") {
    return (
      hasPermission("RATAN_CASHFLOW_BLOTTER:F_Custom_View_Builder_Public") ||
      hasPermission(
        "RATAN_STRATEGIC_CASHFLOW_BLOTTER:F_Custom_View_Builder_Public"
      )
    );
  }
  // iso exception tab
  if (type === EXCEPTIONS_TYPE.ISO_EXCEPTION) {
    return hasPermission("RATAN_KR_EXCEPTION:F_Custom_View_Builder_Public");
  }
  return hasPermission(`${type}:F_Custom_View_Builder_Public`);
};

// @Comment: Because only the permission to create, delete and modify is restricted, this function is no longer needed.
export const hasViewSelectorUIPermission = (type: string = "") => {
  // middle office tab
  if (type === EXCEPTIONS_TYPE.MIDDLE_OFFICE_PROCESS) {
    return (
      hasPermission("RATAN_MO_EXCEPTION:F_Custom_View_Builder_Private") ||
      hasPermission("RATAN_MO_EXCEPTION:F_Custom_View_Builder_Public")
    );
  }
  // validation tab
  if (veryfyMOExceptionTypeFilter(type)) {
    return (
      hasPermission(
        "RATAN_VALIDATION_EXCEPTION:F_Custom_View_Builder_Private"
      ) ||
      hasPermission("RATAN_VALIDATION_EXCEPTION:F_Custom_View_Builder_Public")
    );
  }
  // settlement tab
  if (veryfySetllmentExceptionTypeFilter(type)) {
    return (
      hasPermission(
        "RATAN_SETTLEMENT_EXCEPTION:F_Custom_View_Builder_Private"
      ) ||
      hasPermission("RATAN_SETTLEMENT_EXCEPTION:F_Custom_View_Builder_Public")
    );
  }
  // trade blotter page
  if (type === "TRADE_VIEW_BUILDER") {
    return (
      hasPermission("RATAN_TRADE_BLOTTER:F_Custom_View_Builder_Private") ||
      hasPermission("RATAN_TRADE_BLOTTER:F_Custom_View_Builder_Public")
    );
  }
  // cashflow blotter page
  if (type === "CASHFLOW_VIEW_BUILDER") {
    return (
      hasPermission("RATAN_CASHFLOW_BLOTTER:F_Custom_View_Builder_Private") ||
      hasPermission("RATAN_CASHFLOW_BLOTTER:F_Custom_View_Builder_Public") ||
      hasPermission(
        "RATAN_STRATEGIC_CASHFLOW_BLOTTER:F_Custom_View_Builder_Private"
      ) ||
      hasPermission(
        "RATAN_STRATEGIC_CASHFLOW_BLOTTER:F_Custom_View_Builder_Public"
      )
    );
  }
  return false;
};

export const hasCloseExceptionPermission = (type: string = "") => {
  // middle office tab
  if (type === EXCEPTIONS_TYPE.MIDDLE_OFFICE_PROCESS) {
    return hasPermission("RATAN_MO_EXCEPTION:F_Manually_Close_Exception");
  }
  // validation tab
  if (veryfyMOExceptionTypeFilter(type)) {
    return hasPermission(
      "RATAN_VALIDATION_EXCEPTION:F_Manually_Close_Exception"
    );
  }
  // settlement tab
  if (veryfySetllmentExceptionTypeFilter(type)) {
    if (type === EXCEPTIONS_TYPE.SETTLEMENTS_CLIENT_DATA) {
      const user = getUser();
      return (
        user.role !== "PSS_RO" &&
        hasPermission("RATAN_SETTLEMENT_EXCEPTION:F_Manually_Close_Exception")
      );
    }
    return hasPermission(
      "RATAN_SETTLEMENT_EXCEPTION:F_Manually_Close_Exception"
    );
  }
  //iso exception tab
  if (veryfyISOExceptionTypeFilter(type)) {
    return hasPermission("RATAN_KR_EXCEPTION:F_Manually_Close_Exception");
  }

  return false;
};

export const hasManualFixExceptionPermission = (type: string = "") => {
  // @Comment: Only added permission code for the settlement exception
  // middle office tab
  // if (type === EXCEPTIONS_TYPE.MIDDLE_OFFICE_PROCESS) {
  //   return hasPermission('RATAN_MO_EXCEPTION:F_Manual_Fix');
  // }
  // validation tab
  // if (type === types[1] || type === types[2] || type === types[3] || type === types[4] || type === types[5]) {
  //   return hasPermission('RATAN_VALIDATION_EXCEPTION:F_Manual_Fix');
  // }
  // settlement tab
  if (veryfySetllmentExceptionTypeFilter(type)) {
    return hasPermission("RATAN_SETTLEMENT_EXCEPTION:F_Manual_Fix");
  }
  return false;
};

export const hasReplayExceptionPermission = (type: string = "") => {
  // middle office tab
  if (type === EXCEPTIONS_TYPE.MIDDLE_OFFICE_PROCESS) {
    return false;
  }
  // validation tab
  if (veryfyMOExceptionTypeFilter(type)) {
    return hasPermission("RATAN_VALIDATION_EXCEPTION:F_Replay_Exception");
  }
  // settlement tab
  if (veryfySetllmentExceptionTypeFilter(type)) {
    if (type === EXCEPTIONS_TYPE.SETTLEMENTS_CLIENT_DATA) {
      const user = getUser();
      return (
        user.role !== "PSS_RO" &&
        hasPermission("RATAN_SETTLEMENT_EXCEPTION:F_Replay_Exception")
      );
    }
    return hasPermission("RATAN_SETTLEMENT_EXCEPTION:F_Replay_Exception");
  }
  //iso exception tab
  if (veryfyISOExceptionTypeFilter(type)) {
    return hasPermission("RATAN_KR_EXCEPTION:F_Replay_Exception");
  }

  return false;
};

export const hasInitPermission = (type: string = "") => {
  if (["suppression", "SUPPRESSION", "SWIFT_SUPPRESSION"].includes(type)) {
    return hasPermission(
      "RATAN_SUPPRESSION_RULE:F_Input_Delete_Modify_Initiate"
    );
  }
  if (["settlementStp", "NSTP"].includes(type)) {
    return hasPermission(
      "RATAN_SETTLEMENT_STP_RULE:F_Input_Delete_Modify_Initiate"
    );
  }
  if (type === "currencyNstp") {
    return hasPermission(
      "RATAN_CURRENCY_NSTP_RULE:F_Input_Delete_Modify_Initiate"
    );
  }
  if (["netting", "NETTING"].includes(type)) {
    return hasPermission("RATAN_NETTING_RULE:F_Input_Delete_Modify_Initiate");
  }
  if (type === "currencyCutOff") {
    return hasPermission(
      "RATAN_CURRENCY_CUTOFF:F_Input_Delete_Modify_CUTOFF_Initiate"
    );
  }
  if (type === "nostroList") {
    return (
      hasPermission("RATAN_SUPPRESSION_RULE:F_Input_Delete_Modify_Initiate") ||
      hasPermission("RATAN_NOSTRO_BLOTTER:F_Input_Delete_Modify_Initiate")
    );
  }

  return false;
};

export const hasVerifyPermission = (type: string = "") => {
  if (
    ["suppression", "SUPPRESSION", "SWIFT_SUPPRESSION", "nostroList"].includes(
      type
    )
  ) {
    return (
      hasPermission("RATAN_SUPPRESSION_RULE:F_Input_Delete_Modify_Verify") ||
      hasPermission("RATAN_NOSTRO_BLOTTER:F_Input_Delete_Modify_Verify")
    );
  }
  if (["settlementStp", "NSTP"].includes(type)) {
    return hasPermission(
      "RATAN_SETTLEMENT_STP_RULE:F_Input_Delete_Modify_Verify"
    );
  }
  if (type === "currencyNstp") {
    return hasPermission(
      "RATAN_CURRENCY_NSTP_RULE:F_Input_Delete_Modify_Verify"
    );
  }
  if (["netting", "NETTING"].includes(type)) {
    return hasPermission("RATAN_NETTING_RULE:F_Input_Delete_Modify_Verify");
  }
  if (type === "currencyCutOff") {
    return hasPermission(
      "RATAN_CURRENCY_CUTOFF:F_Input_Delete_Modify_CUTOFF_Verify"
    );
  }
  return false;
};

export const hasExceptionPagePermission = () => {
  return (
    hasPermission("RATAN_MO_EXCEPTION:UI_Read_Access") ||
    hasPermission("RATAN_VALIDATION_EXCEPTION:UI_Read_Access") ||
    hasPermission("RATAN_SETTLEMENT_EXCEPTION:UI_Read_Access") ||
    hasPermission("RATAN_MO_EXCEPTION:ACCESS_FMO_POST_TRADE_PORTAL") ||
    hasPermission("RATAN_VALIDATION_EXCEPTION:ACCESS_FMO_POST_TRADE_PORTAL") ||
    hasPermission("RATAN_SETTLEMENT_EXCEPTION:ACCESS_FMO_POST_TRADE_PORTAL")
  );
};

export const getTheShellListWithPermission = (list: any[]) => {
  return list.filter((item: any) => hasPermission(item.entitlementCode));
};
