import { createContext, useContext, useEffect, useMemo } from "react";
import { RatanFieldConfig, RatanRawFieldConfig } from "../../RatanOne/type";
import { ratanRawField2RQBField } from "../../ReactQueryBuilder/utils";
import type {
  FilterRecord,
  QueryFilterDetails,
  SaveFilter,
  CreateFilter,
  DeleteFilter,
  QueryFilterList,
} from "../common/types";
import {
  defaultGetOperators,
  generateTemplateFilterRecord,
} from "../common/utiles";
import { DEFAULT_CREATING_FILTER_KEY } from "../common/const";
import type { DefaultOperator } from "react-querybuilder";
import { getUser } from "../../../../ratanutils/authenticator";
import type { Mode } from "../../ReactQueryBuilder/types";

type AdvancedSearchContextProps = {
  appliedFilter: FilterRecord | null;
  setAppliedFilter: (f: FilterRecord | null) => Promise<void>;
  filterList: FilterRecord[];
  setFilterList: (
    fs: FilterRecord[] | ((r: FilterRecord[]) => FilterRecord[])
  ) => void;
  displayFilter: FilterRecord;
  setDisplayFilter: (
    f: FilterRecord | ((r: FilterRecord) => FilterRecord)
  ) => void;
};

export const AdvancedSearchContext = createContext<AdvancedSearchContextProps>({
  appliedFilter: null,
  setAppliedFilter: async () => undefined,
  filterList: [],
  setFilterList: () => undefined,
  displayFilter: generateTemplateFilterRecord(),
  setDisplayFilter: () => undefined,
});

export const AdvancedSearchStaticContext = createContext<{
  type?: string;
  filterMode?: Mode;
  fields: RatanRawFieldConfig[];
  queryFilterList: QueryFilterList;
  queryFilterDetails: QueryFilterDetails;
  createFilter: CreateFilter;
  saveFilter: SaveFilter;
  deleteFilter: DeleteFilter;
  getOperators: (field: RatanFieldConfig) => DefaultOperator[];
}>({
  fields: [],
  type: "",
  queryFilterList: async () => [],
  queryFilterDetails: async () => generateTemplateFilterRecord(),
  createFilter: async () => generateTemplateFilterRecord(),
  saveFilter: async () => generateTemplateFilterRecord(),
  deleteFilter: async () => undefined,
  getOperators: defaultGetOperators,
});

export const useFilterBuilderContext = () => {
  const { role, id } = getUser();
  const {
    appliedFilter,
    setAppliedFilter,
    filterList,
    setFilterList,
    displayFilter,
    setDisplayFilter,
  } = useContext(AdvancedSearchContext);
  const {
    type,
    filterMode,
    fields,
    queryFilterList,
    queryFilterDetails,
    createFilter,
    saveFilter,
    deleteFilter,
    getOperators,
  } = useContext(AdvancedSearchStaticContext);

  const classifiedFilterList = useMemo(() => {
    const publicFilterList: FilterRecord[] = [];
    const privateFilterList: FilterRecord[] = [];
    filterList.forEach((f) => {
      if (f.isPublic) publicFilterList.push(f);
      else privateFilterList.push(f);
    });
    publicFilterList.sort((a, b) => a.name.localeCompare(b.name));
    privateFilterList.sort((a, b) => a.name.localeCompare(b.name));
    return [
      ...(privateFilterList.length
        ? [
            {
              key: "private",
              title: "Private",
              options: privateFilterList,
            },
          ]
        : []),
      ...(publicFilterList.length
        ? [
            {
              key: "public",
              title: "Public",
              options: publicFilterList,
            },
          ]
        : []),
    ];
  }, [filterList]);

  const completeFilterBody = async (f: FilterRecord) => {
    if (!f.body && f.rowKey !== DEFAULT_CREATING_FILTER_KEY) {
      try {
        const resp = await queryFilterDetails?.(f);
        if (resp) {
          setFilterList((list) => {
            const targetIndex = list.findIndex((i) => i.rowKey === f.rowKey);
            list[targetIndex] = resp;
            return [...list];
          });
        }
        return resp;
      } catch (error) {}
    }
  };

  const findFilterByKey = (rowKey: string) => {
    return filterList.find((f) => f.rowKey === rowKey) as FilterRecord;
  };

  const onSelectFilter = async (f: FilterRecord) => {
    setDisplayFilter(f);
    const latestFilter = await completeFilterBody(f);
    if (latestFilter) setDisplayFilter(latestFilter);
    return latestFilter;
  };

  const onApplyFilter = async (f: FilterRecord) => {
    const latestFilter = await completeFilterBody(f);
    await setAppliedFilter(latestFilter ?? f);
  };

  const onSelectFilterByKey = async (rowKey: string) => {
    const f = findFilterByKey(rowKey);
    const latestFilter = await onSelectFilter(f);
    return latestFilter ?? f;
  };

  const onApplyFilterByKey = async (rowKey: string) => {
    const f = findFilterByKey(rowKey);
    const latestFilter = await completeFilterBody(f);
    await setAppliedFilter(latestFilter ?? f);
  };

  const onClearAppliedFilter = async () => {
    await setAppliedFilter(null);
  };

  const RQBFields = useMemo(() => {
    return fields.map((f) =>
      ratanRawField2RQBField(f, {
        getOperators,
      })
    );
  }, [fields]);

  return {
    type,
    filterMode,
    userId: id,
    userRole: role,
    fields: RQBFields,
    appliedFilter,
    setAppliedFilter,
    filterList,
    classifiedFilterList,
    displayFilter,
    setDisplayFilter,
    onSelectFilter,
    onSelectFilterByKey,
    onApplyFilter,
    onApplyFilterByKey,
    onClearAppliedFilter,
    setFilterList,
    queryFilterList,
    queryFilterDetails,
    saveFilter,
    createFilter,
    deleteFilter,
  };
};

export const useFilterList = () => {
  const { setFilterList } = useContext(AdvancedSearchContext);
  const { queryFilterList } = useContext(AdvancedSearchStaticContext);

  useEffect(() => {
    (async () => {
      try {
        const resp = await queryFilterList?.();
        resp && setFilterList(resp);
      } catch (error) {}
    })();
  }, []);
};
