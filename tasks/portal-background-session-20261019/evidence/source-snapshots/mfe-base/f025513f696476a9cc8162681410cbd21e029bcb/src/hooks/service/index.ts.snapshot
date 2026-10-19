import { AxiosPromise, AxiosRequestConfig, AxiosResponse } from "axios";
import { getHooksBase } from "../HooksBase";
import service from "./config";
import { getEndPoint } from "./util/getEndpoint";

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
