import React from 'react';
import { postService } from '../../../hooks/service';

type AdminPayload = Record<string, unknown>;

interface AdminResponse<T> {
  data?: T;
}

const useAdminRequest = (clearError?: () => void) => {
  const controllers = React.useRef(new Map<string, AbortController>());

  React.useEffect(
    () => () => {
      controllers.current.forEach((controller) => controller.abort());
      controllers.current.clear();
    },
    [],
  );

  return React.useCallback(
    async <T>(key: string, path: string, payload: AdminPayload, fallback: T): Promise<T> => {
      clearError?.();
      controllers.current.get(key)?.abort();

      const controller = new AbortController();
      controllers.current.set(key, controller);

      try {
        const response = await postService<AdminResponse<T>>(path, payload, {
          signal: controller.signal,
        });
        return response.data?.data ?? fallback;
      } catch (error: unknown) {
        if (controller.signal.aborted) {
          return fallback;
        }
        throw error;
      } finally {
        if (controllers.current.get(key) === controller) {
          controllers.current.delete(key);
        }
      }
    },
    [clearError],
  );
};

export default useAdminRequest;
