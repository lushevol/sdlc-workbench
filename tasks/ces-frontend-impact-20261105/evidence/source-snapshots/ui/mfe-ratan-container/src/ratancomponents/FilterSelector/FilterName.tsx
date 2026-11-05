import React, { FC, memo, useContext, useMemo } from "react";
import { Checkbox, Popconfirm } from "antd";
import Input from "../../LazyAntd/Input";
import Select from "../../LazyAntd/Select";
import { LoadingButton } from "../../Root/import";
import { Context } from "./store";

import { MessageInstance } from "antd/es/message/interface";
import useFieldNameController from "./common/useFieldNameController";
import { getEnable } from "../../ratanutils/componentEnabling";
import { getUser } from "../../ratanutils/authenticator";
import Root from "./FilterNameStyles";

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

interface FilterNameProps {
  filterFieldType: string;
  onRemove: Function;
  messageApi: MessageInstance;
  onSavedFilter?: (filters: {
    sql: string;
    localFilterBody: LocalFilter[];
    json: Object;
  }) => void;
}

export const FilterName: FC<FilterNameProps> = memo((props) => {
  const {
    saveBuilder,
    isLoading,
    isModify,
    isReadOnly,
    removeBuilder,
    isRemoveLoading,
    compareFilterName,
    compareFilterRole,
    cancel,
  } = useFieldNameController(props);

  const { state } = useContext(Context);
  const { temporaryFilter } = state;
  const { name = "", assigneeList = "" } = temporaryFilter;
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

  return (
    <Root>
      <Input
        className="text-input"
        placeholder="Filter Name"
        disabled={isLoading || isRemoveLoading}
        value={name}
        allowClear={true}
        onChange={(e) => compareFilterName(e.target.value)}
        data-testid="filterNameInput"
      />
      {getEnable("Filter_Builder_POC", props.filterFieldType) && (
        <Select
          className="role-select"
          disabled={(isModify && isReadOnly) || isLoading || isRemoveLoading}
          data-testid={"filterNameTargetRoleSelect"}
          placeholder="Select Role"
          value={assigneeList ? assigneeList.split(",") : []}
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
          onChange={compareFilterRole}
          dropdownMatchSelectWidth={false}
        />
      )}
      <Checkbox
        className="check"
        checked={!assigneeList}
        onChange={(e) => e.target.checked && compareFilterRole("")}
        disabled={
          !getEnable("Filter_Builder_POC", props.filterFieldType) ||
          (isModify && isReadOnly) ||
          isLoading ||
          isRemoveLoading
        }
      >
        Is Private
      </Checkbox>
      <LoadingButton
        className="save-btn"
        disabled={
          (getEnable("Filter_Builder_POC", props.filterFieldType) &&
            isModify &&
            isReadOnly) ||
          name.length < 2 ||
          isLoading ||
          isRemoveLoading
        }
        loading={isLoading}
        onClick={saveBuilder}
        variant="contained"
      >
        {isModify ? "Modify Filter" : "Create Filter"}
      </LoadingButton>
      {isModify && (
        <Popconfirm
          title="Are you sure to remove this filter?"
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
            color="error"
            variant="outlined"
          >
            Remove
          </LoadingButton>
        </Popconfirm>
      )}
    </Root>
  );
});
