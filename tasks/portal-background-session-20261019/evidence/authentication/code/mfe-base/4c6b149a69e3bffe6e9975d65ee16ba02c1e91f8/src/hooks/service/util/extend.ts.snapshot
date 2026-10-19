import { getHooksBase } from "../../HooksBase";
import service from "../config";
import { getEndPoint } from "./getEndpoint";

export const signal = {
  extendToken: undefined as AbortController | undefined,
};
export const extend = async (
  expiredIn: number | undefined,
  isOnLogout: boolean | undefined,
  token: string | undefined
) => {
  if (signal?.extendToken) {
    signal?.extendToken?.abort();
  }
  const difftime = 1000 * (expiredIn ?? 0) - new Date().getTime();
  if (isOnLogout || difftime < 25000) {
    return;
  }
  signal.extendToken = new AbortController();
  service
    .post(
      getEndPoint("/auth/v2/sso/extend"),
      { singleUIAuthorization: token },
      {
        signal: signal.extendToken.signal,
      }
    )
    .catch((e) => {
      console.error("e", e);
    });
};
export const extendToken = () => {
  const { store } = getHooksBase();
  extend(store.expiredIn, store.isOnLogout, store.token);
};
