import { AxiosPromise, AxiosRequestConfig, AxiosResponse } from "axios";
import { getHooksBase } from "../HooksBase";
import service from "./config";
import { getEndPoint } from "./util/getEndpoint";

export interface ConfigProps {
  signal?: any;
  headers?: any;
}

export const signal = {
  getRefreshToken: undefined as any,
  relogin: undefined as any,
};

export const getRefreshToken = () => {
  if (signal?.getRefreshToken) {
    signal?.getRefreshToken?.abort();
  }
  signal.getRefreshToken = new AbortController();
  const { store } = getHooksBase();
  service
    .post(
      getEndPoint("/auth/v2/sso/refreshtoken"),
      { singleUIAuthorization: store.token },
      {
        signal: signal.getRefreshToken.signal,
      }
    )
    .catch((e) => {
      console.error("e", e);
    });
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

const putService = <T = unknown, D = unknown>(
  path: string,
  data: D,
  config?: AxiosRequestConfig<D>
): AxiosPromise<T, D> => {
  return service.put<T, AxiosResponse<T, D>, D>(getEndPoint(path), data, config);
};

const postService = <T = unknown, D = unknown>(
  path: string,
  data: D,
  config?: AxiosRequestConfig<D>
): AxiosPromise<T, D> => {
  return service.post<T, AxiosResponse<T, D>, D>(
    getEndPoint(path),
    data,
    config
  );
};

const getService = <T = unknown, D = unknown>(
  path: string,
  config?: AxiosRequestConfig<D>
): AxiosPromise<T, D> => {
  return service.get<T, AxiosResponse<T, D>, D>(getEndPoint(path), config);
};

const deleteService = <T = unknown, D = unknown>(
  path: string,
  config?: AxiosRequestConfig<D>
): AxiosPromise<T, D> => {
  return service.delete<T, AxiosResponse<T, D>, D>(getEndPoint(path), config);
};

const patchService = <T = unknown, D = unknown>(
  path: string,
  data: D,
  config?: ConfigProps
): AxiosPromise<T, D> => {
  return service.patch(getEndPoint(path), data, config);
};

export {
  putService,
  postService,
  getService,
  deleteService,
  patchService,
  service,
};
