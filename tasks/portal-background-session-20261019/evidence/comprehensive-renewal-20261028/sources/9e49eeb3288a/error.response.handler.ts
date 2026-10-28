import { AxiosError } from "axios";
import { getHooksBase } from "../../HooksBase";
import { ActionType } from "../../reducer/util/ActionType";
import { clearStorageWhenLogout } from "../../../utils/common";

export const errorHandler = (error: AxiosError): unknown => {
  const { baseDispatch } = getHooksBase();
  if (
    error.code !== "ERR_CANCELED" &&
    !error?.config?.url?.includes("/logout") &&
    !error?.config?.url?.includes("/api/analytics/") &&
    !error?.config?.url?.includes("/api/sse/")
  ) {
    let msg = `${error?.config?.url} : ${error.message}`;
    if (
      error?.response?.data ||
      error.message === "Network Error" ||
      error.message === "Request failed with status code 401"
    ) {
      let data: any = error?.response?.data;
      msg =
        data?.message ||
        data?.errorMessage ||
        `Error happened, service is unavailable, pls check with support team: ${error?.config?.url}: API request failed`;
      if (typeof data === "string") {
        msg = data;
      }
    }
    if (msg?.includes("TOKEN_INVALID_EXPIRED")) {
      clearStorageWhenLogout(baseDispatch);
      msg = "Expired Session, please login again.";
    }
    if (msg?.includes("AuthenticationException")) {
      console.info(error?.config);
      msg =
        "Invalid username and password combination or SSO service is unavailable.";
    }
    baseDispatch({ type: ActionType.SET_ERRORMSG, data: { errorMsg: msg } });
  }
  baseDispatch({ type: ActionType.SET_IS_LOADING, data: { isLoading: false } });
  return Promise.reject({ ...error });
};
