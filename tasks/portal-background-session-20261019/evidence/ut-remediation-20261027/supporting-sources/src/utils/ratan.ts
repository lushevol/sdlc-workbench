import { AxiosResponse } from "axios";

export const handleStandardResponse = (response: AxiosResponse) => {
  return new Promise<any>((resolve, reject) => {
    if (response.status && response.status === 200) {
      resolve(response.data);
    } else {
      reject(response.data);
    }
  });
};
