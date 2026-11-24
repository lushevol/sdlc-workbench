import React, { FC, memo, useEffect, useContext, useMemo } from "react";
import { message, Popconfirm, Select } from "antd";
import Input from "../../LazyAntd/Input";
import { LoadingButton } from "../../Root/import";
import Checkbox from "../../LazyAntd/Checkbox";
import { GridReadyEvent } from "ag-grid-community";
import { Context } from "./store";
import debounce from "lodash/debounce";
import {
  getUser,
  hasPrivatePermission,
  hasPublicPermission,
} from "../../ratanutils/authenticator";
import { getEnable } from "../../ratanutils/componentEnabling";

import useViewNameController from "./common/useViewNameController";
import Root from "./ViewNameStyles";

const assigneeRoleOptions = [
  { value: "FMO_OPS", label: "FMO_OPS" },
  { value: "FMO_OPS_SUP", label: "FMO_OPS_SUP" },
  { value: "FMO_RO", label: "FMO_RO" },
  { value: "NON_FMO_RO", label: "NON_FMO_RO" },
  { value: "PSS_RO", label: "PSS_RO" },
  { value: "FMO_BR_APR", label: "FMO_BR_APR" },
  { value: "FMO_BR_MKR", label: "FMO_BR_MKR" },
  { value: "FMO_OPS_BO", label: "FMO_OPS_BO" },
  { value: "FMO_OPS_BOC", label: "FMO_OPS_BOC" },
  { value: "FMO_OPS_BOL", label: "FMO_OPS_BOL" },
  { value: "FMO_OPS_BOM", label: "FMO_OPS_BOM" },
  { value: "FMO_OPS_MKR", label: "FMO_OPS_MKR" },
  { value: "FMO_STA_CKR", label: "FMO_STA_CKR" },
  { value: "FMO_STA_MKR", label: "FMO_STA_MKR" },
  { value: "FMO_MO_RO", label: "FMO_MO_RO" },
  { value: "FMO_MO_TV", label: "FMO_MO_TV" },
  { value: "FMO_MO_TV_SUP", label: "FMO_MO_TV_SUP" },
  { value: "FMO_MO_TE", label: "FMO_MO_TE" },
  { value: "FMO_MO_TE_SUP", label: "FMO_MO_TE_SUP" },
];

export const judgmentAuthority = (
  viewFieldType,
  ems2Subject,
  assigneeList,
  isPublic
) => {
  if (getEnable("View_Builder_POC", viewFieldType)) {
    return !assigneeList;
  } else if (!hasPrivatePermission(ems2Subject ?? viewFieldType)) {
    return false;
  } else if (!hasPublicPermission(ems2Subject ?? viewFieldType)) {
    return true;
  }
  return !isPublic;
};

interface ViewNameProps {
  viewFieldType: string;
  ems2Subject?: string;
  onSearch: Function;
  tradeGridReady?: GridReadyEvent;
}

export const ViewName: FC<ViewNameProps> = memo((props) => {
  const { viewFieldType, ems2Subject, onSearch } = props;
  const [messageApi, messageContextHolder] = message.useMessage();
  const {
    saveBuilder,
    removeBuilder,
    setChooseAuthority,
    thisViewHasPermission,
    newName,
    setNewName,
    isLoading,
    isRemoveLoading,
    chooseAuthority,
    isModify,
    isReadOnly,
    newRole,
    cancel,
    compareViewRole,
  } = useViewNameController(props, messageApi);
  const { state } = useContext(Context);
  const { currentView } = state;
  const { name = "", assigneeList = "", isPublic }: any = currentView || {};
  const { role } = getUser();

  const roleSettings = useMemo(() => {
    return [...assigneeRoleOptions];
  }, []);

  const myRoleName = useMemo(() => {
    const idx = roleSettings.findIndex((roleItem) => roleItem.value == role);
    if (idx >= 0) {
      return ` (${roleSettings[idx].label})`;
    } else {
      return "";
    }
  }, [roleSettings, role]);

  const changePrivate = (e) => {
    if (getEnable("View_Builder_POC", props.viewFieldType)) {
      e.target.checked && compareViewRole("");
    } else {
      setChooseAuthority(e.target.checked);
    }
  };

  useEffect(() => {
    if (thisViewHasPermission()) {
      setNewName(name);
      compareViewRole(assigneeList);
    }
    setChooseAuthority(
      judgmentAuthority(viewFieldType, ems2Subject, assigneeList, isPublic)
    );
  }, [name, assigneeList, isPublic, viewFieldType, ems2Subject]);

  return (
    <Root>
      <Input
        className="search-field"
        allowClear={true}
        placeholder="Search Field"
        data-testid="searchField"
        onChange={debounce((e) => onSearch(e.target.value), 300)}
      />
      <div className="baffle"></div>
      <Input
        className="text-input"
        placeholder="View Name"
        disabled={isLoading || isRemoveLoading}
        value={newName}
        allowClear={true}
        onChange={(e) => setNewName(e.target.value)}
        data-testid="viewName"
      />
      {getEnable("View_Builder_POC", props.viewFieldType) && (
        <Select
          className="role-select"
          disabled={(isModify && isReadOnly) || isLoading || isRemoveLoading}
          data-testid={"filterNameTargetRoleSelect"}
          placeholder="Select Role"
          value={newRole ? newRole.split(",") : []}
          showSearch
          mode="multiple"
          maxTagCount="responsive"
          options={[
            {
              label: "For My Role" + myRoleName,
              value: role,
            },
            {
              label: "Assignee",
              options: roleSettings.filter((item) => item.value !== role),
            },
          ]}
          onChange={compareViewRole}
        />
      )}
      <Checkbox
        className="check"
        checked={chooseAuthority}
        onChange={changePrivate}
        disabled={
          getEnable("View_Builder_POC", props.viewFieldType)
            ? (isModify && isReadOnly) || isLoading || isRemoveLoading
            : !hasPrivatePermission(viewFieldType) ||
              !hasPublicPermission(viewFieldType)
        }
      >
        Is Private
      </Checkbox>
      <LoadingButton
        className="save-btn"
        disabled={
          (getEnable("View_Builder_POC", props.viewFieldType) &&
            isModify &&
            isReadOnly) ||
          newName.length < 2 ||
          isLoading ||
          isRemoveLoading
        }
        loading={isLoading}
        onClick={saveBuilder}
        data-testid="customView-save-btn"
        variant="contained"
      >
        {isModify ? "Modify View" : "Create View"}
      </LoadingButton>
      {isModify && (
        <Popconfirm
          title="Are you sure to remove this view?"
          onConfirm={removeBuilder}
          onCancel={cancel}
          okText="Yes"
          cancelText="No"
          disabled={isLoading || isRemoveLoading}
        >
          <LoadingButton
            className="remove-btn"
            disabled={(isModify && isReadOnly) || isLoading || isRemoveLoading}
            loading={isRemoveLoading}
            data-testid="customView-remove-btn"
            variant="outlined"
            color="error"
          >
            Remove
          </LoadingButton>
        </Popconfirm>
      )}
      {messageContextHolder}
    </Root>
  );
});
