import React from 'react';
import { getHooksBase } from '../../../hooks/HooksBase';
import { ActionType } from '../../../hooks/reducer/util/ActionType';
import { AdminRecord } from '../../common/interface';
import useAdminRequest from '../../common/services/useAdminRequest';

type AdminPayload = AdminRecord;

const useServices = () => {
  const { baseDispatch } = getHooksBase();
  const clearErrorMessage = React.useCallback(() => {
    baseDispatch({
      type: ActionType.SET_ERRORMSG,
      data: { errorMsg: undefined },
    });
  }, [baseDispatch]);
  const request = useAdminRequest(clearErrorMessage);

  const getImportMap = React.useCallback(
    (entitlementsToken: string | undefined) =>
      request<AdminRecord[]>(
        'getImportMap',
        '/auth/v1/fmo/admin/importmap/data',
        { entitlementsToken },
        [],
      ),
    [request],
  );
  const getImportMapAudit = React.useCallback(
    (entitlementsToken: string | undefined, data: AdminPayload) =>
      request<AdminRecord[]>(
        'getImportMapAudit',
        '/auth/v1/fmo/admin/importmap/audit',
        { entitlementsToken, ...data },
        [],
      ),
    [request],
  );
  const updateImportMap = React.useCallback(
    (entitlementsToken: string | undefined, data: AdminPayload) =>
      request<AdminPayload>(
        'updateImportMap',
        '/auth/v1/fmo/admin/importmap/update',
        { entitlementsToken, ...data, mode: 'maker' },
        {},
      ),
    [request],
  );
  const verifyImportMap = React.useCallback(
    (entitlementsToken: string | undefined, data: AdminPayload) =>
      request<AdminPayload>(
        'verifyImportMap',
        '/auth/v1/fmo/admin/importmap/update',
        { entitlementsToken, ...data, mode: 'checker' },
        {},
      ),
    [request],
  );
  const deactivateImportMap = React.useCallback(
    (entitlementsToken: string | undefined, data: AdminPayload) =>
      request<AdminPayload>(
        'deactivateImportMap',
        '/auth/v1/fmo/admin/importmap/update',
        { entitlementsToken, ...data, mode: 'deactivate' },
        {},
      ),
    [request],
  );
  const createImportMap = React.useCallback(
    (entitlementsToken: string | undefined, data: AdminPayload) =>
      request<AdminPayload>(
        'createImportMap',
        '/auth/v1/fmo/admin/importmap/create',
        { entitlementsToken, ...data },
        {},
      ),
    [request],
  );

  return {
    getImportMap,
    updateImportMap,
    verifyImportMap,
    createImportMap,
    deactivateImportMap,
    getImportMapAudit,
  };
};

export default useServices;
