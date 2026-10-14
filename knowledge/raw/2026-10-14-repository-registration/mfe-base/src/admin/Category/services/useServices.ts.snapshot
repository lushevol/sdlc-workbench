import React from 'react';
import { AdminRecord } from '../../common/interface';
import useAdminRequest from '../../common/services/useAdminRequest';

type AdminPayload = AdminRecord;

const useServices = () => {
  const request = useAdminRequest();

  const getCategory = React.useCallback(
    (entitlementsToken: string | undefined) =>
      request<AdminRecord[]>(
        'getCategory',
        '/auth/v1/fmo/admin/category/data',
        { entitlementsToken },
        [],
      ),
    [request],
  );
  const getCategoryAudit = React.useCallback(
    (entitlementsToken: string | undefined, data: AdminPayload) =>
      request<AdminRecord[]>(
        'getCategoryAudit',
        '/auth/v1/fmo/admin/category/audit',
        { entitlementsToken, ...data },
        [],
      ),
    [request],
  );
  const updateCategory = React.useCallback(
    (entitlementsToken: string | undefined, data: AdminPayload) =>
      request<AdminPayload>(
        'updateCategory',
        '/auth/v1/fmo/admin/category/update',
        { entitlementsToken, ...data, mode: 'maker' },
        {},
      ),
    [request],
  );
  const verifyCategory = React.useCallback(
    (entitlementsToken: string | undefined, data: AdminPayload) =>
      request<AdminPayload>(
        'verifyCategory',
        '/auth/v1/fmo/admin/category/update',
        { entitlementsToken, ...data, mode: 'checker' },
        {},
      ),
    [request],
  );
  const deactivateCategory = React.useCallback(
    (entitlementsToken: string | undefined, data: AdminPayload) =>
      request<AdminPayload>(
        'deactivateCategory',
        '/auth/v1/fmo/admin/category/update',
        { entitlementsToken, ...data, mode: 'deactivate' },
        {},
      ),
    [request],
  );
  const createCategory = React.useCallback(
    (entitlementsToken: string | undefined, data: AdminPayload) =>
      request<AdminPayload>(
        'createCategory',
        '/auth/v1/fmo/admin/category/create',
        { entitlementsToken, ...data },
        {},
      ),
    [request],
  );
  return {
    getCategory,
    updateCategory,
    verifyCategory,
    createCategory,
    deactivateCategory,
    getCategoryAudit,
  };
};

export default useServices;
