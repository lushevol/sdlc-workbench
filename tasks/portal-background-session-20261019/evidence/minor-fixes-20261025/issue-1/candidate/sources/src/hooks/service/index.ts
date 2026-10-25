import { AxiosPromise, AxiosRequestConfig, AxiosResponse } from "axios";
import { getHooksBase } from "../HooksBase";
import { getJWTPayload } from "../../utils/common";
import service from "./config";
import { getEndPoint } from "./util/getEndpoint";
import { currentSessionEpoch } from "../../utils/sessionEpoch";

export interface ConfigProps {
  signal?: any;
  headers?: any;
}

type ServiceWithBody = <T = any, D = any, P = any>(
  path: string,
  data: D,
  config?: AxiosRequestConfig<D, P>
) => AxiosPromise<T, D, P>;

type ServiceWithoutBody = <T = any, D = any, P = any>(
  path: string,
  config?: AxiosRequestConfig<D, P>
) => AxiosPromise<T, D, P>;

export const signal = {
  getRefreshToken: undefined as AbortController | undefined,
  relogin: undefined as any,
};

const REFRESH_TOKEN_REUSE_WINDOW_MS = 3 * 60 * 60 * 1000;
let refreshTokenRequest:
  | {
      accessToken: string | undefined;
      epoch: number;
      controller: AbortController;
      promise: Promise<void>;
    }
  | undefined;

export const getRefreshToken = () => {
  const { store } = getHooksBase();
  const epoch = currentSessionEpoch();
  if (store.refreshToken) {
    try {
      const payload = getJWTPayload(store.refreshToken);
      if (
        payload &&
        typeof payload.exp === "number" &&
        Number.isFinite(payload.exp * 1000) &&
        payload.exp * 1000 - Date.now() > REFRESH_TOKEN_REUSE_WINDOW_MS
      ) {
        return;
      }
    } catch {
      // An unreadable expiry cannot establish that the token is reusable.
    }
  }
  if (
    refreshTokenRequest &&
    refreshTokenRequest.epoch === epoch &&
    refreshTokenRequest.accessToken === store.token &&
    !refreshTokenRequest.controller.signal.aborted
  ) {
    return refreshTokenRequest.promise;
  }

  signal.getRefreshToken?.abort();
  const controller = new AbortController();
  signal.getRefreshToken = controller;
  const promise = service
    .post(
      getEndPoint("/auth/v2/sso/refreshtoken"),
      { singleUIAuthorization: store.token },
      {
        signal: controller.signal,
      }
    )
    .then(() => undefined)
    .catch((e) => {
      console.error("e", e);
    })
    .finally(() => {
      if (refreshTokenRequest?.controller === controller) {
        refreshTokenRequest = undefined;
      }
      if (signal.getRefreshToken === controller) {
        signal.getRefreshToken = undefined;
      }
    });
  refreshTokenRequest = {
    accessToken: store.token,
    epoch,
    controller,
    promise,
  };
  return promise;
};

export const relogin = () => {
  if (signal?.relogin) {
    signal?.relogin?.abort();
  }
  signal.relogin = new AbortController();
  service
    .post(
      getEndPoint("/auth/v2/sso/relogin"),
      {},
      {
        signal: signal.relogin.signal,
      }
    )
    .catch((e) => {
      console.error("e", e);
    });
};

const putService: ServiceWithBody = <T = any, D = any, P = any>(
  path: string,
  data: D,
  config?: AxiosRequestConfig<D, P>
) => {
  return service.put<T, AxiosResponse<T, D, {}, P>, D, P>(
    getEndPoint(path),
    data,
    config
  );
};

const postService: ServiceWithBody = <T = any, D = any, P = any>(
  path: string,
  data: D,
  config?: AxiosRequestConfig<D, P>
) => {
  return service.post<T, AxiosResponse<T, D, {}, P>, D, P>(
    getEndPoint(path),
    data,
    config
  );
};

const getService: ServiceWithoutBody = <T = any, D = any, P = any>(
  path: string,
  config?: AxiosRequestConfig<D, P>
) => {
  return service.get<T, AxiosResponse<T, D, {}, P>, D, P>(
    getEndPoint(path),
    config
  );
};

const deleteService: ServiceWithoutBody = <T = any, D = any, P = any>(
  path: string,
  config?: AxiosRequestConfig<D, P>
) => {
  return service.delete<T, AxiosResponse<T, D, {}, P>, D, P>(
    getEndPoint(path),
    config
  );
};

const patchService: ServiceWithBody = <T = any, D = any, P = any>(
  path: string,
  data: D,
  config?: AxiosRequestConfig<D, P>
) => {
  return service.patch<T, AxiosResponse<T, D, {}, P>, D, P>(
    getEndPoint(path),
    data,
    config
  );
};

export {
  putService,
  postService,
  getService,
  deleteService,
  patchService,
  service,
};
