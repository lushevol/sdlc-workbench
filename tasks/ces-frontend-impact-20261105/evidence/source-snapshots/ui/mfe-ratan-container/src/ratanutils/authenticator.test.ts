import * as authenticator from "./authenticator";

afterAll(() => {
  jest.clearAllMocks();
});

jest.mock("../Root/import", () => {
  const user = JSON.parse(
    `{"sub":"1243644","iss":"single-ui-bff","entitlement":{"role":"FMO_OPS_SUP","actions":["RATAN_TRADE_BLOTTER:F_Custom_Query_Builder","RATAN_TRADE_BLOTTER:F_Custom_View_Builder_Private","RATAN_TRADE_BLOTTER:F_Custom_View_Builder_Public","RATAN_TRADE_BLOTTER:F_Export_Data","RATAN_TRADE_BLOTTER:F_Retrigger_Confirmation_Dispatch","RATAN_TRADE_BLOTTER:F_Trade_Affirmation_Status_Change","RATAN_TRADE_BLOTTER:UI_Read_Access","RATAN_TRADE_BLOTTER:UI_View_Brokerage_Detail","RATAN_TRADE_BLOTTER:UI_View_Confirmation_Status","RATAN_TRADE_BLOTTER:UI_View_Counterparty_Data","RATAN_TRADE_BLOTTER:UI_View_Trade_Audit_History","RATAN_TRADE_BLOTTER:UI_View_Trade_Data","RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_Nostro_Initiate","RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_Nostro_Verify","RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_SSI_Initiate","RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_SSI_Verify","RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_Suppress","RATAN_CASHFLOW_BLOTTER:F_Add_Settlement_Comment","RATAN_CASHFLOW_BLOTTER:F_Cashflow_Affirmation_Status_Change","RATAN_CASHFLOW_BLOTTER:F_Cashflow_Status_Change_Release","RATAN_CASHFLOW_BLOTTER:F_Custom_Query_Builder","RATAN_CASHFLOW_BLOTTER:F_Custom_View_Builder_Private","RATAN_CASHFLOW_BLOTTER:F_Custom_View_Builder_Public","RATAN_CASHFLOW_BLOTTER:F_Export_Data","RATAN_CASHFLOW_BLOTTER:F_Perform_Ad_Hoc_Netting","RATAN_CASHFLOW_BLOTTER:F_Perform_Cashflow_Split","RATAN_CASHFLOW_BLOTTER:F_Perform_Un_Net_Initiate","RATAN_CASHFLOW_BLOTTER:F_Perform_Un_Net_Verify","RATAN_CASHFLOW_BLOTTER:F_Reinstate","RATAN_CASHFLOW_BLOTTER:UI_Read_Access","RATAN_CASHFLOW_BLOTTER:UI_View_Cashflow_Data","RATAN_CASHFLOW_BLOTTER:UI_View_Counterparty_Data","RATAN_MO_EXCEPTION:F_Custom_View_Builder_Private","RATAN_MO_EXCEPTION:UI_Read_Access","RATAN_VALIDATION_EXCEPTION:F_Custom_View_Builder_Private","RATAN_VALIDATION_EXCEPTION:F_Custom_View_Builder_Public","RATAN_VALIDATION_EXCEPTION:F_Manually_Close_Exception","RATAN_VALIDATION_EXCEPTION:F_Replay_Exception","RATAN_VALIDATION_EXCEPTION:F_Trade_Affirmation_Status_Change","RATAN_VALIDATION_EXCEPTION:UI_Read_Access","RATAN_SETTLEMENT_EXCEPTION:F_Custom_View_Builder_Private","RATAN_SETTLEMENT_EXCEPTION:F_Custom_View_Builder_Public","RATAN_SETTLEMENT_EXCEPTION:F_Input_Delete_Modify_SI_Initiate","RATAN_SETTLEMENT_EXCEPTION:F_Input_Delete_Modify_SI_Verify","RATAN_SETTLEMENT_EXCEPTION:F_Manual_Fix","RATAN_SETTLEMENT_EXCEPTION:F_Manually_Close_Exception","RATAN_SETTLEMENT_EXCEPTION:F_Replay_Exception","RATAN_SETTLEMENT_EXCEPTION:UI_Read_Access","RATAN_WORKFLOW:UI_Read_Access","RATAN_SUPPRESSION_RULE:F_Input_Delete_Modify_Initiate","RATAN_SUPPRESSION_RULE:F_Input_Delete_Modify_Verify","RATAN_SUPPRESSION_RULE:UI_View_Rule_Audit_History","RATAN_SUPPRESSION_RULE:UI_View_Suppression_Rule_Table","RATAN_SETTLEMENT_STP_RULE:F_Input_Delete_Modify_Initiate","RATAN_SETTLEMENT_STP_RULE:F_Input_Delete_Modify_Verify","RATAN_SETTLEMENT_STP_RULE:UI_View_Rule_Audit_History","RATAN_SETTLEMENT_STP_RULE:UI_View_STP_Rule_Table","RATAN_CURRENCY_NSTP_RULE:F_Input_Delete_Modify_Initiate","RATAN_CURRENCY_NSTP_RULE:F_Input_Delete_Modify_Verify","RATAN_CURRENCY_NSTP_RULE:UI_View_NSTP_Rule_Table","RATAN_CURRENCY_NSTP_RULE:UI_View_Rule_Audit_History","RATAN_ISO_CURRENCY_MAPPING:UI_View_Currency_Mapping_Table","RATAN_ISO_CURRENCY_MAPPING:UI_View_Rule_Audit_History","RATAN_NETTING_RULE:F_Input_Delete_Modify_Initiate","RATAN_NETTING_RULE:F_Input_Delete_Modify_Verify","RATAN_NETTING_RULE:UI_View_Netting_Rule_Table","RATAN_NETTING_RULE:UI_View_Rule_Audit_History","RATAN_CURRENCY_CUTOFF:F_Input_Delete_Modify_CUTOFF_Initiate","RATAN_CURRENCY_CUTOFF:F_Input_Delete_Modify_CUTOFF_Verify","RATAN_CURRENCY_CUTOFF:UI_Read_Access","PORTAL_CDU_ISLAMIC:UI_Read_Access"],"dataEntitlementRoles":""},"exp":1678957305,"iat":1678928505,"userLoginTime":"2023-03-16T01:01:45.948Z[GMT]","jti":"single-ui-bff-id","id":"1243644","fullName":"1243644","name":"1243644","userId":"1243644"}`
  );
  const entities =JSON.parse(`[{
    "id": "11274101",
    "name": "X_RATANONE",
    "applicationName": "RATAN",
    "roleId": "11274180",
    "roleName": "FMO_OPS_SUP",
    "subjects": [
        {
            "longName": "/RATAN_TRADE_BLOTTER",
            "name": "RATAN_TRADE_BLOTTER",
            "actions": [
                {"name": "F_Custom_Query_Builder"},
                {"name": "F_Custom_View_Builder_Private"},
                {"name": "ACCESS_FMO_POST_TRADE_PORTAL"},
                {"name": "F_Custom_View_Builder_Public"},
                {"name": "F_Export_Data"},
                {"name": "F_Retrigger_Confirmation_Dispatch"},
                {"name": "F_Trade_Affirmation_Status_Change"},
                {"name": "UI_View_Confirmation_Status"},
                {"name": "UI_View_Counterparty_Data"},
                {"name": "UI_View_Trade_Audit_History"}
            ]
        }
      ]
}]`);

const entities1 = [{
  "id": 11274101,
  "name": "X_RATANONE",
  "applicationName": "RATAN",
  "roleId": 11274180,
  "roleName": "FMO_OPS_SUP",
  "subjects": [
      {
          "longName": "/RATAN_AUTO_NETTING_RULE",
          "name": "RATAN_AUTO_NETTING_RULE",
          "actions": [
              {
                  "name": "ACCESS_FMO_POST_TRADE_PORTAL"
              }
          ]
      },
      {
          "longName": "/RATAN_ENTITLEMENT_RULE",
          "name": "RATAN_ENTITLEMENT_RULE",
          "actions": [
              {
                  "name": "ACCESS_FMO_POST_TRADE_PORTAL"
              }
          ]
      },
      {
          "longName": "/RATAN_CASHFLOW_BLOTTER",
          "name": "RATAN_CASHFLOW_BLOTTER",
          "actions": [
              {
                  "name": "F_Ad_Hoc_Nostro_Initiate"
              },
              {
                  "name": "F_Ad_Hoc_Nostro_Verify"
              },
              {
                  "name": "F_Ad_Hoc_SSI_Initiate"
              },
              {
                  "name": "F_Ad_Hoc_SSI_Verify"
              },
              {
                  "name": "F_Ad_Hoc_Suppress"
              },
              {
                  "name": "F_Add_Settlement_Comment"
              },
              {
                  "name": "F_Cashflow_Affirmation_Status_Change"
              },
              {
                  "name": "F_Cashflow_Status_Change_Release"
              },
              {
                  "name": "F_Custom_Query_Builder"
              },
              {
                  "name": "F_Custom_View_Builder_Private"
              },
              {
                  "name": "F_Custom_View_Builder_Public"
              },
              {
                  "name": "F_Export_Data"
              },
              {
                  "name": "F_Perform_Ad_Hoc_Netting"
              },
              {
                  "name": "F_Perform_Un_Net_Initiate"
              },
              {
                  "name": "F_Perform_Un_Net_Verify"
              },
              {
                  "name": "F_Reinstate"
              },
              {
                  "name": "ACCESS_FMO_POST_TRADE_PORTAL"
              }
          ]
      },
      {
          "longName": "/RATAN_MO_EXCEPTION",
          "name": "RATAN_MO_EXCEPTION",
          "id": 11274219,
          "actions": [
              {
                  "name": "F_Custom_View_Builder_Private",
                  "id": 11274958,
                  "entitlementId": 11274306
              },
              {
                  "name": "ACCESS_FMO_POST_TRADE_PORTAL",
                  "id": 11274984,
                  "entitlementId": 11275289
              }
          ]
      },
      {
          "longName": "/RATAN_NETTING_RULE",
          "name": "RATAN_NETTING_RULE",
          "id": 11274220,
          "actions": [
              {
                  "name": "ACCESS_FMO_POST_TRADE_PORTAL",
                  "id": 11274984,
                  "entitlementId": 11275353
              }
          ]
      },
      {
          "longName": "/RATAN_NOSTRO_BLOTTER",
          "name": "RATAN_NOSTRO_BLOTTER",
          "id": 11274221,
          "actions": [
              {
                  "name": "ACCESS_FMO_POST_TRADE_PORTAL",
                  "id": 11274984,
                  "entitlementId": 11275191
              }
          ]
      },
      {
          "longName": "/RATAN_SETTLEMENT_EXCEPTION",
          "name": "RATAN_SETTLEMENT_EXCEPTION",
          "id": 11274223,
          "actions": [
              {
                  "name": "F_Custom_View_Builder_Private",
                  "id": 11274958,
                  "entitlementId": 11275052
              },
              {
                  "name": "F_Custom_View_Builder_Public",
                  "id": 11274959,
                  "entitlementId": 11275070
              },
              {
                  "name": "F_Input_Delete_Modify_SI_Initiate",
                  "id": 11274964,
                  "entitlementId": 11275106
              },
              {
                  "name": "F_Input_Delete_Modify_SI_Verify",
                  "id": 11274965,
                  "entitlementId": 11275109
              },
              {
                  "name": "F_Manual_Fix",
                  "id": 11274967,
                  "entitlementId": 11275125
              },
              {
                  "name": "F_Manually_Close_Exception",
                  "id": 11274968,
                  "entitlementId": 11275129
              },
              {
                  "name": "F_Replay_Exception",
                  "id": 11274979,
                  "entitlementId": 11275180
              },
              {
                  "name": "ACCESS_FMO_POST_TRADE_PORTAL",
                  "id": 11274984,
                  "entitlementId": 11275298
              }
          ]
      },
      {
          "longName": "/RATAN_SETTLEMENT_STP_RULE",
          "name": "RATAN_SETTLEMENT_STP_RULE",
          "id": 11274224,
          "actions": [
              {
                  "name": "F_Input_Delete_Modify_Initiate",
                  "id": 11274963,
                  "entitlementId": 11275103
              },
              {
                  "name": "F_Input_Delete_Modify_Verify",
                  "id": 11274966,
                  "entitlementId": 11275111
              },
              {
                  "name": "ACCESS_FMO_POST_TRADE_PORTAL",
                  "id": 11274984,
                  "entitlementId": 11275340
              }
          ]
      },
      {
          "longName": "/RATAN_SUPPRESSION_RULE",
          "name": "RATAN_SUPPRESSION_RULE",
          "id": 11274225,
          "actions": [
              {
                  "name": "F_Input_Delete_Modify_Initiate",
                  "id": 11274963,
                  "entitlementId": 11274321
              },
              {
                  "name": "F_Input_Delete_Modify_Verify",
                  "id": 11274966,
                  "entitlementId": 11274322
              },
              {
                  "name": "ACCESS_FMO_POST_TRADE_PORTAL",
                  "id": 11274984,
                  "entitlementId": 11275315
              }
          ]
      },
      {
          "longName": "/RATAN_TRADE_BLOTTER",
          "name": "RATAN_TRADE_BLOTTER",
          "id": 11274226,
          "actions": [
              {
                  "name": "F_Custom_Query_Builder",
                  "id": 11274957,
                  "entitlementId": 11274366
              },
              {
                  "name": "F_Custom_View_Builder_Private",
                  "id": 11274958,
                  "entitlementId": 11274367
              },
              {
                  "name": "F_Custom_View_Builder_Public",
                  "id": 11274959,
                  "entitlementId": 11274368
              },
              {
                  "name": "F_Export_Data",
                  "id": 11274960,
                  "entitlementId": 11274369
              },
              {
                  "name": "F_Retrigger_Confirmation_Dispatch",
                  "id": 11274980,
                  "entitlementId": 11274371
              },
              {
                  "name": "F_Trade_Affirmation_Status_Change",
                  "id": 11274981,
                  "entitlementId": 11274372
              },
              {
                  "name": "ACCESS_FMO_POST_TRADE_PORTAL",
                  "id": 11274984,
                  "entitlementId": 11275267
              },
              {
                  "name": "UI_View_Trade_Audit_History",
                  "id": 11274993,
                  "entitlementId": 11274380
              }
          ]
      },
      {
          "longName": "/RATAN_VALIDATION_EXCEPTION",
          "name": "RATAN_VALIDATION_EXCEPTION",
          "id": 11274227,
          "actions": [
              {
                  "name": "F_Custom_View_Builder_Private",
                  "id": 11274958,
                  "entitlementId": 11274418
              },
              {
                  "name": "F_Custom_View_Builder_Public",
                  "id": 11274959,
                  "entitlementId": 11274419
              },
              {
                  "name": "F_Manually_Close_Exception",
                  "id": 11274968,
                  "entitlementId": 11274420
              },
              {
                  "name": "F_Replay_Exception",
                  "id": 11274979,
                  "entitlementId": 11274421
              },
              {
                  "name": "F_Trade_Affirmation_Status_Change",
                  "id": 11274981,
                  "entitlementId": 11274422
              },
              {
                  "name": "ACCESS_FMO_POST_TRADE_PORTAL",
                  "id": 11274984,
                  "entitlementId": 11275365
              }
          ]
      },
      {
          "longName": "/RATAN_MO_RULE",
          "name": "RATAN_MO_RULE",
          "id": 11932954,
          "actions": [
              {
                  "name": "ACCESS_FMO_POST_TRADE_PORTAL",
                  "id": 11274984,
                  "entitlementId": 12202644
              }
          ]
      },
      {
        "longName": "/RATAN_KR_EXCEPTION",
        "name": "RATAN_KR_EXCEPTION",
        "id": 11274467,
        "actions": [
          {
            "name": "F_Custom_View_Builder_Private",
            "id": 11274958,
            "entitlementId": 11275052
          },
          {
            "name": "F_Custom_View_Builder_Public",
            "id": 11274959,
            "entitlementId": 11275070
          },
          {
            "name": "F_Manually_Close_Exception",
            "id": 11274968,
            "entitlementId": 11275129
          },
          {
            "name": "F_Replay_Exception",
            "id": 11274979,
            "entitlementId": 11275180
          },
          {
            "name": "ACCESS_FMO_POST_TRADE_PORTAL",
            "id": 11274984,
            "entitlementId": 11275289
          }
        ]
    },
  ]
}];
  const hooks = {
    store: { user, entities:entities1 },
    setStore: function (store) {
      this.store = store;
    },
    baseDispatch: () => {},
    setBaseDispatch: function (dispatch) {
      this.baseDispatch = dispatch;
    },
  };
  const getHooks = () => hooks;
  const Hooks = { getHooks, hooks };
  return { Hooks };
});

test("getUser", () => {
  const user = authenticator.getUser();
  expect(
    user.role).toEqual("FMO_OPS_SUP");
});


test("hasPermission", () => {
  expect(
    authenticator.hasPermission("RATAN_TRADE_BLOTTER:UI_Read_Access")
  ).toEqual(true);
  expect(authenticator.hasPermission("OTHER")).toEqual(false);
});
test("hasPrivatePermission", () => {
  expect(authenticator.hasPrivatePermission("MIDDLE_OFFICE_PROCESS")).toEqual(
    true
  );
  expect(authenticator.hasPrivatePermission("VALIDATION_INTERFACE")).toEqual(
    true
  );
  expect(
    authenticator.hasPrivatePermission("VALIDATION_DATA_ENRICHMENT")
  ).toEqual(true);
  expect(authenticator.hasPrivatePermission("VALIDATION_CLIENT_DATA")).toEqual(
    true
  );
  expect(authenticator.hasPrivatePermission("VALIDATION_PROCESS")).toEqual(
    true
  );
  expect(authenticator.hasPrivatePermission("VALIDATION")).toEqual(true);
  expect(authenticator.hasPrivatePermission("SETTLEMENTS_INTERFACE")).toEqual(
    true
  );
  expect(authenticator.hasPrivatePermission("SETTLEMENTS_CLIENT_DATA")).toEqual(
    true
  );
  expect(authenticator.hasPrivatePermission("SETTLEMENTS_PROCESS")).toEqual(
    true
  );
  expect(authenticator.hasPrivatePermission("TRADE_VIEW_BUILDER")).toEqual(
    true
  );
  expect(authenticator.hasPrivatePermission("CASHFLOW_VIEW_BUILDER")).toEqual(
    true
  );
  expect(authenticator.hasPrivatePermission("OTHER")).toEqual(false);
  expect(authenticator.hasPrivatePermission()).toEqual(false);
});
test("hasPublicPermission", () => {
  expect(authenticator.hasPublicPermission("MIDDLE_OFFICE_PROCESS")).toEqual(
    false
  );
  expect(authenticator.hasPublicPermission("VALIDATION_INTERFACE")).toEqual(
    true
  );
  expect(
    authenticator.hasPublicPermission("VALIDATION_DATA_ENRICHMENT")
  ).toEqual(true);
  expect(authenticator.hasPublicPermission("VALIDATION_CLIENT_DATA")).toEqual(
    true
  );
  expect(authenticator.hasPublicPermission("VALIDATION_PROCESS")).toEqual(true);
  expect(authenticator.hasPublicPermission("VALIDATION")).toEqual(true);
  expect(authenticator.hasPublicPermission("SETTLEMENTS_INTERFACE")).toEqual(
    true
  );
  expect(authenticator.hasPublicPermission("SETTLEMENTS_CLIENT_DATA")).toEqual(
    true
  );
  expect(authenticator.hasPublicPermission("SETTLEMENTS_PROCESS")).toEqual(
    true
  );
  expect(authenticator.hasPublicPermission("TRADE_VIEW_BUILDER")).toEqual(true);
  expect(authenticator.hasPublicPermission("CASHFLOW_VIEW_BUILDER")).toEqual(
    true
  );
  expect(authenticator.hasPublicPermission("OTHER")).toEqual(false);
  expect(authenticator.hasPublicPermission()).toEqual(false);
  expect(authenticator.hasPublicPermission("ISO_PROCESS_EXCEPTION")).toEqual(true);
});
test("hasViewSelectorUIPermission", () => {
  expect(
    authenticator.hasViewSelectorUIPermission("MIDDLE_OFFICE_PROCESS")
  ).toEqual(true);
  expect(
    authenticator.hasViewSelectorUIPermission("VALIDATION_INTERFACE")
  ).toEqual(true);
  expect(
    authenticator.hasViewSelectorUIPermission("VALIDATION_DATA_ENRICHMENT")
  ).toEqual(true);
  expect(
    authenticator.hasViewSelectorUIPermission("VALIDATION_CLIENT_DATA")
  ).toEqual(true);
  expect(
    authenticator.hasViewSelectorUIPermission("VALIDATION_PROCESS")
  ).toEqual(true);
  expect(authenticator.hasViewSelectorUIPermission("VALIDATION")).toEqual(true);
  expect(
    authenticator.hasViewSelectorUIPermission("SETTLEMENTS_INTERFACE")
  ).toEqual(true);
  expect(
    authenticator.hasViewSelectorUIPermission("SETTLEMENTS_CLIENT_DATA")
  ).toEqual(true);
  expect(
    authenticator.hasViewSelectorUIPermission("SETTLEMENTS_PROCESS")
  ).toEqual(true);
  expect(
    authenticator.hasViewSelectorUIPermission("TRADE_VIEW_BUILDER")
  ).toEqual(true);
  expect(
    authenticator.hasViewSelectorUIPermission("CASHFLOW_VIEW_BUILDER")
  ).toEqual(true);
  expect(authenticator.hasViewSelectorUIPermission("OTHER")).toEqual(false);
  expect(authenticator.hasViewSelectorUIPermission()).toEqual(false);
  expect(authenticator.hasPrivatePermission("ISO_PROCESS_EXCEPTION")).toEqual(true);
});
test("hasCloseExceptionPermission", () => {
  expect(
    authenticator.hasCloseExceptionPermission("MIDDLE_OFFICE_PROCESS")
  ).toEqual(false);
  expect(
    authenticator.hasCloseExceptionPermission("VALIDATION_INTERFACE")
  ).toEqual(true);
  expect(
    authenticator.hasCloseExceptionPermission("VALIDATION_DATA_ENRICHMENT")
  ).toEqual(true);
  expect(
    authenticator.hasCloseExceptionPermission("VALIDATION_CLIENT_DATA")
  ).toEqual(true);
  expect(
    authenticator.hasCloseExceptionPermission("VALIDATION_PROCESS")
  ).toEqual(true);
  expect(authenticator.hasCloseExceptionPermission("VALIDATION")).toEqual(true);
  expect(
    authenticator.hasCloseExceptionPermission("SETTLEMENTS_INTERFACE")
  ).toEqual(true);
  expect(
    authenticator.hasCloseExceptionPermission("SETTLEMENTS_CLIENT_DATA")
  ).toEqual(true);
  expect(
    authenticator.hasCloseExceptionPermission("SETTLEMENTS_PROCESS")
  ).toEqual(true);
  expect(authenticator.hasCloseExceptionPermission("OTHER")).toEqual(false);
  expect(authenticator.hasCloseExceptionPermission()).toEqual(false);
  expect(authenticator.hasCloseExceptionPermission("ISO_PROCESS_EXCEPTION")).toBe(true)
});
test("hasReplayExceptionPermission", () => {
  expect(
    authenticator.hasReplayExceptionPermission("MIDDLE_OFFICE_PROCESS")
  ).toEqual(false);
  expect(
    authenticator.hasReplayExceptionPermission("VALIDATION_INTERFACE")
  ).toEqual(true);
  expect(
    authenticator.hasReplayExceptionPermission("VALIDATION_DATA_ENRICHMENT")
  ).toEqual(true);
  expect(
    authenticator.hasReplayExceptionPermission("VALIDATION_CLIENT_DATA")
  ).toEqual(true);
  expect(
    authenticator.hasReplayExceptionPermission("VALIDATION_PROCESS")
  ).toEqual(true);
  expect(authenticator.hasReplayExceptionPermission("VALIDATION")).toEqual(
    true
  );
  expect(
    authenticator.hasReplayExceptionPermission("SETTLEMENTS_INTERFACE")
  ).toEqual(true);
  expect(
    authenticator.hasReplayExceptionPermission("SETTLEMENTS_CLIENT_DATA")
  ).toEqual(true);
  expect(
    authenticator.hasReplayExceptionPermission("SETTLEMENTS_PROCESS")
  ).toEqual(true);
  expect(authenticator.hasReplayExceptionPermission("OTHER")).toEqual(false);
  expect(authenticator.hasReplayExceptionPermission()).toEqual(false);
  expect(authenticator.hasReplayExceptionPermission("ISO_PROCESS_EXCEPTION")).toBe(true);
});
test("hasInitPermission", () => {
  expect(authenticator.hasInitPermission("suppression")).toEqual(true);
  expect(authenticator.hasInitPermission("settlementStp")).toEqual(true);
  expect(authenticator.hasInitPermission("currencyNstp")).toEqual(true);
  expect(authenticator.hasInitPermission("netting")).toEqual(true);
  expect(authenticator.hasInitPermission("currencyCutOff")).toEqual(true);
  expect(authenticator.hasInitPermission("OTHER")).toEqual(false);
  expect(authenticator.hasInitPermission()).toEqual(false);
  expect(authenticator.hasInitPermission("nostroList")).toBe(true);
});
test("hasVerifyPermission", () => {
  expect(authenticator.hasVerifyPermission("suppression")).toEqual(true);
  expect(authenticator.hasVerifyPermission("settlementStp")).toEqual(true);
  expect(authenticator.hasVerifyPermission("currencyNstp")).toEqual(true);
  expect(authenticator.hasVerifyPermission("netting")).toEqual(true);
  expect(authenticator.hasVerifyPermission("currencyCutOff")).toEqual(true);
  expect(authenticator.hasVerifyPermission("OTHER")).toEqual(false);
  expect(authenticator.hasVerifyPermission()).toEqual(false);
});
test("hasExceptionPagePermission", () => {
  expect(authenticator.hasExceptionPagePermission()).toEqual(true);
});
test("getTheShellListWithPermission", () => {
  expect(
    authenticator.getTheShellListWithPermission([
      { entitlementCode: "RATAN_CASHFLOW_BLOTTER:UI_Read_Access" },
    ])
  ).toEqual([{ entitlementCode: "RATAN_CASHFLOW_BLOTTER:UI_Read_Access" }]);
});
test("hasManualFixExceptionPermission", () => {
  expect(
    authenticator.hasManualFixExceptionPermission("SETTLEMENTS_INTERFACE")
  ).toEqual(true);
  expect(
    authenticator.hasManualFixExceptionPermission("SETTLEMENTS_CLIENT_DATA")
  ).toEqual(true);
  expect(
    authenticator.hasManualFixExceptionPermission("SETTLEMENTS_PROCESS")
  ).toEqual(true);
  expect(authenticator.hasManualFixExceptionPermission("OTHER")).toEqual(false);
  expect(authenticator.hasManualFixExceptionPermission()).toEqual(false);
});
