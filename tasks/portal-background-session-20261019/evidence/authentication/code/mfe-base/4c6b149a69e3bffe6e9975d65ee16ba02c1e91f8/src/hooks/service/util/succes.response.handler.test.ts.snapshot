import { AxiosResponse, InternalAxiosRequestConfig } from "axios";
import { config } from "../config";
import { successHandler } from "./succes.response.handler";

describe("error.response.handler", () => {
  it("should be true", async () => {
    const data: AxiosResponse = {
      config: {
        ...config,
      } as InternalAxiosRequestConfig,
      data: {},
      status: 200,
      statusText: "",
      headers: {},
    }
    const result = await successHandler(data);
    expect(JSON.stringify(result.data)).toBe("{}");
  });
  it("should be true", async () => {
    const data: AxiosResponse = {
      config: {
        ...config,
        url: "/api/auth/v1/sso/login"
      } as InternalAxiosRequestConfig,
      data: { "result": "success" },
      status: 200,
      statusText: "",
      headers: {},
    }
    const result = await successHandler(data);
    expect(result.data.result).toBe("success");
  });
  it("should be true", async () => {
    const data: AxiosResponse = {
      config: {
        ...config,
        url: "/api/auth/v2/sso/login"
      } as InternalAxiosRequestConfig,
      data: { "result": "success" },
      status: 200,
      statusText: "",
      headers: {},
    }
    const result = await successHandler(data);
    expect(result.data.result).toBe("success");
  });
  it("should be true", async () => {
    const data: AxiosResponse = {
      config: {
        ...config,
        url: "/api/auth/v3/sso/login"
      } as InternalAxiosRequestConfig,
      data: { "result": "success" },
      status: 200,
      statusText: "",
      headers: {},
    }
    const result = await successHandler(data);
    expect(result.data.result).toBe("success");
  });
  it("should be true", async () => {
    const data: AxiosResponse = {
      config: {
        ...config,
        url: "/api/auth/v1/sso/relogin"
      } as InternalAxiosRequestConfig,
      data: { "result": "success" },
      status: 200,
      statusText: "",
      headers: {},
    }
    const result = await successHandler(data);
    expect(result.data.result).toBe("success");
  });
  it("should be true", async () => {
    const data: AxiosResponse = {
      config: {
        ...config,
        url: "/api/auth/v2/sso/relogin"
      } as InternalAxiosRequestConfig,
      data: { "result": "success" },
      status: 200,
      statusText: "",
      headers: {},
    }
    const result = await successHandler(data);
    expect(result.data.result).toBe("success");
  });
  it("should be true", async () => {
    const data: AxiosResponse = {
      config: {
        ...config,
        url: "/api/auth/v2/sso/refreshtoken"
      } as InternalAxiosRequestConfig,
      data: { "result": "success" },
      status: 200,
      statusText: "",
      headers: {},
    }
    const result = await successHandler(data);
    expect(result.data.result).toBe("success");
  });
  it("should be true", async () => {
    const data: AxiosResponse = {
      config: {
        ...config,
        url: "/api/auth/v2/sso/extend"
      } as InternalAxiosRequestConfig,
      data: { "result": "success" },
      status: 200,
      statusText: "",
      headers: {},
    }
    const result = await successHandler(data);
    expect(result.data.result).toBe("success");
  });
  it("should be true", async () => {
    const data: AxiosResponse = {
      config: {
        ...config,
        url: "/api/auth/v1/sso/user"
      } as InternalAxiosRequestConfig,
      data: { "userInfo": "{\"sub\":\"1243644\",\"iss\":\"single-ui-bff\",\"entitlement\":\"{\\\"role\\\":\\\"FMO_OPS_SUP\\\",\\\"actions\\\":[\\\"RATAN_TRADE_BLOTTER:F_Custom_Query_Builder\\\",\\\"RATAN_TRADE_BLOTTER:F_Custom_View_Builder_Private\\\",\\\"RATAN_TRADE_BLOTTER:F_Custom_View_Builder_Public\\\",\\\"RATAN_TRADE_BLOTTER:F_Export_Data\\\",\\\"RATAN_TRADE_BLOTTER:F_Match_Confirmed_Status_Change\\\",\\\"RATAN_TRADE_BLOTTER:F_Retrigger_Confirmation_Dispatch\\\",\\\"RATAN_TRADE_BLOTTER:F_Trade_Affirmation_Status_Change\\\",\\\"RATAN_TRADE_BLOTTER:F_View_Confirmation\\\",\\\"RATAN_TRADE_BLOTTER:UI_Read_Access\\\",\\\"RATAN_TRADE_BLOTTER:UI_View_Brokerage_Detail\\\",\\\"RATAN_TRADE_BLOTTER:UI_View_Cashflow_Status\\\",\\\"RATAN_TRADE_BLOTTER:UI_View_Confirmation_Status\\\",\\\"RATAN_TRADE_BLOTTER:UI_View_Counterparty_Data\\\",\\\"RATAN_TRADE_BLOTTER:UI_View_Instrument_Detail\\\",\\\"RATAN_TRADE_BLOTTER:UI_View_SSI_Data\\\",\\\"RATAN_TRADE_BLOTTER:UI_View_Trade_Audit_History\\\",\\\"RATAN_TRADE_BLOTTER:UI_View_Trade_Data\\\",\\\"RATAN_TRADE_BLOTTER:UI_View_Trade_Version_Differences\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_Nostro_Initiate\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_Nostro_Verify\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_SSI_Initiate\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_SSI_Verify\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Ad_Hoc_Suppress\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Add_Settlement_Comment\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Cashflow_Affirmation_Status_Change\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Cashflow_Status_Change_Release\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Custom_Query_Builder\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Custom_View_Builder_Private\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Custom_View_Builder_Public\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Export_Data\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Modify_Settlement_Means\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Perform_Ad_Hoc_Netting\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Perform_Cashflow_Split\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Perform_Un_Net_Initiate\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Perform_Un_Net_Verify\\\",\\\"RATAN_CASHFLOW_BLOTTER:F_Reinstate\\\",\\\"RATAN_CASHFLOW_BLOTTER:UI_Read_Access\\\",\\\"RATAN_CASHFLOW_BLOTTER:UI_View_Cashflow_Data\\\",\\\"RATAN_CASHFLOW_BLOTTER:UI_View_Cashflow_Status\\\",\\\"RATAN_CASHFLOW_BLOTTER:UI_View_Counterparty_Data\\\",\\\"RATAN_CASHFLOW_BLOTTER:UI_View_SSI_Data\\\",\\\"RATAN_MO_EXCEPTION:F_Custom_View_Builder_Private\\\",\\\"RATAN_MO_EXCEPTION:UI_Read_Access\\\",\\\"RATAN_VALIDATION_EXCEPTION:F_Custom_View_Builder_Private\\\",\\\"RATAN_VALIDATION_EXCEPTION:F_Custom_View_Builder_Public\\\",\\\"RATAN_VALIDATION_EXCEPTION:F_Manually_Close_Exception\\\",\\\"RATAN_VALIDATION_EXCEPTION:F_Replay_Exception\\\",\\\"RATAN_VALIDATION_EXCEPTION:F_Trade_Affirmation_Status_Change\\\",\\\"RATAN_VALIDATION_EXCEPTION:UI_Read_Access\\\",\\\"RATAN_SETTLEMENT_EXCEPTION:F_Custom_View_Builder_Private\\\",\\\"RATAN_SETTLEMENT_EXCEPTION:F_Custom_View_Builder_Public\\\",\\\"RATAN_SETTLEMENT_EXCEPTION:F_Input_Delete_Modify_SI_Initiate\\\",\\\"RATAN_SETTLEMENT_EXCEPTION:F_Input_Delete_Modify_SI_Verify\\\",\\\"RATAN_SETTLEMENT_EXCEPTION:F_Manual_Fix\\\",\\\"RATAN_SETTLEMENT_EXCEPTION:F_Manually_Close_Exception\\\",\\\"RATAN_SETTLEMENT_EXCEPTION:F_Replay_Exception\\\",\\\"RATAN_SETTLEMENT_EXCEPTION:UI_Read_Access\\\",\\\"RATAN_WORKFLOW:UI_Read_Access\\\",\\\"RATAN_SUPPRESSION_RULE:F_Input_Delete_Modify_Initiate\\\",\\\"RATAN_SUPPRESSION_RULE:F_Input_Delete_Modify_Verify\\\",\\\"RATAN_SUPPRESSION_RULE:UI_View_Rule_Audit_History\\\",\\\"RATAN_SUPPRESSION_RULE:UI_View_Suppression_Rule_Table\\\",\\\"RATAN_SETTLEMENT_STP_RULE:F_Input_Delete_Modify_Initiate\\\",\\\"RATAN_SETTLEMENT_STP_RULE:F_Input_Delete_Modify_Verify\\\",\\\"RATAN_SETTLEMENT_STP_RULE:UI_View_Rule_Audit_History\\\",\\\"RATAN_SETTLEMENT_STP_RULE:UI_View_STP_Rule_Table\\\",\\\"RATAN_CURRENCY_NSTP_RULE:F_Input_Delete_Modify_Initiate\\\",\\\"RATAN_CURRENCY_NSTP_RULE:F_Input_Delete_Modify_Verify\\\",\\\"RATAN_CURRENCY_NSTP_RULE:UI_View_NSTP_Rule_Table\\\",\\\"RATAN_CURRENCY_NSTP_RULE:UI_View_Rule_Audit_History\\\",\\\"RATAN_ISO_CURRENCY_MAPPING:UI_View_Currency_Mapping_Table\\\",\\\"RATAN_ISO_CURRENCY_MAPPING:UI_View_Rule_Audit_History\\\",\\\"RATAN_NETTING_RULE:F_Input_Delete_Modify_Initiate\\\",\\\"RATAN_NETTING_RULE:F_Input_Delete_Modify_Verify\\\",\\\"RATAN_NETTING_RULE:UI_View_Netting_Rule_Table\\\",\\\"RATAN_NETTING_RULE:UI_View_Rule_Audit_History\\\",\\\"RATAN_CURRENCY_CUTOFF:F_Input_Delete_Modify_CUTOFF_Initiate\\\",\\\"RATAN_CURRENCY_CUTOFF:F_Input_Delete_Modify_CUTOFF_Verify\\\",\\\"RATAN_CURRENCY_CUTOFF:UI_Read_Access\\\",\\\"PORTAL_CDU_ISLAMIC:UI_Read_Access\\\"],\\\"dataEntitlementRoles\\\":\\\"\\\"}\",\"exp\":1679066095,\"iat\":1679037295,\"userLoginTime\":\"2023-03-17T07:14:55.997Z[GMT]\",\"jti\":\"single-ui-bff-id\"}" },
      status: 200,
      statusText: "",
      headers: {},
    }
    const result = await successHandler(data);
    const userInfo = JSON.parse(result?.data?.userInfo);
    expect(userInfo.sub).toBe("1243644");
  });
  it("should be true", async () => {
    const data: AxiosResponse = {
      config: {
        ...config,
        url: "/api/ratan/"
      } as InternalAxiosRequestConfig,
      data: { "result": "success" },
      status: 200,
      statusText: "",
      headers: {},
    }
    const result = await successHandler(data);
    expect(result.result).toBe("success");
  });
});
