import { getUser } from "../../../ratanutils/authenticator";

export const generateViewSelectorOptions = (list: any, type: string) => {
  const publicOptions: { label: string; value: string }[] = [];
  const privateOptions: { label: string; value: string }[] = [];
  const finalOptions: { label: string; options: any }[] = [];

  list[type]?.forEach((item: any, _index: number) => {
    if (type === item.type) {
      if (item.isPublic) {
        publicOptions.push({
          label: item.name,
          value: item.rowKey,
        });
      } else {
        privateOptions.push({
          label: item.name,
          value: item.rowKey,
        });
      }
    }
  });

  if (privateOptions.length > 0) {
    finalOptions.push({ label: "Private", options: privateOptions });
  }
  if (publicOptions.length > 0) {
    finalOptions.push({ label: "Public", options: publicOptions });
  }

  return finalOptions;
};

export const generateViewSelectorOptionsForRole = (list: any, type: string) => {
  const { role } = getUser();
  const privateOptions: any = {
    label: "Private",
    options: [],
  };
  const publicOptions: any = {
    label: "Public",
    options: [],
  };
  const myRoleOptions: any = {
    label: "My Role",
    options: [],
  };
  const assignToOptions: any = {
    label: "Assigned To",
    options: [],
  };
  const assignByOptions: any = {
    label: "Assigned By",
    options: [],
  };

  list[type]?.forEach((item: any, index: number) => {
    if (item.type === type) {
      if (item.isPublic) {
        publicOptions.options.push({
          label: item.name,
          value: item.rowKey,
        });
      } else if (!item.assigneeList) {
        privateOptions.options.push({
          label: item.name,
          value: item.rowKey,
        });
      } else if (item.assigneeList === item.moduleOwner) {
        myRoleOptions.options.push({
          label: item.name,
          value: item.rowKey,
        });
      } else if (item.moduleOwner === role) {
        assignToOptions.options.push({
          label: `${item.name} - ${item.assigneeList}`,
          value: item.rowKey,
        });
      } else {
        assignByOptions.options.push({
          label: `${item.name} - ${item.moduleOwner}`,
          value: item.rowKey,
        });
      }
    }
  });
  let newOptions: any[] = [];
  privateOptions.options.length && newOptions.push(privateOptions);
  publicOptions.options.length && newOptions.push(publicOptions);
  myRoleOptions.options.length && newOptions.push(myRoleOptions);
  assignByOptions.options.length && newOptions.push(assignByOptions);
  assignToOptions.options.length && newOptions.push(assignToOptions);
  return newOptions;
};
