/** @jest-environment jsdom */
import { renderHook, act, waitFor } from "@testing-library/react";
import useController from "../../../../repos/ui/mfe-ratan-container/src/ratancomponents/FilterSelector/useController";
import * as api from "../../../../repos/ui/mfe-ratan-container/src/ratanutils/http/api";
let mockConfirm;
const mockStore = {
 user: {id: "1481696", fullName: "Review User"},
 entities: [{applicationId: "51358", name: "RATAN_ENTITLEMENT_RULE", roleList: ["OPS"], subjects: [{entitlementSource: "EMS3"}]}],
 entitlementRouting: [{tileId:"101", source:"EMS3", applicationId:"51358", entityNames:["RATAN_ENTITLEMENT_RULE"], features:["RATAN_TRADE_BLOTTER"]}]
};
jest.mock("../../../../repos/ui/mfe-ratan-container/src/Root/import", () => ({Hooks: {getHooks: () => ({store:mockStore})}}));
jest.mock("../../../../repos/ui/mfe-ratan-container/src/ratanutils/utils", () => ({deepClone: (x) => JSON.parse(JSON.stringify(x))}));
jest.mock("../../../../repos/ui/mfe-ratan-container/src/ratanutils/componentEnabling", () => ({getEnable: () => true}));
jest.mock("../../../../repos/ui/mfe-ratan-container/src/ratancomponents/FilterSelector/FilterBuilderNext", () => ({getSearchFilter: () => [], handleNullValue: x => x}));
jest.mock("react-querybuilder", () => ({formatQuery: () => ""}), {virtual:true});
jest.mock("antd", () => ({
 message:{useMessage: () => [{error:jest.fn(),success:jest.fn()}, null]},
 Modal:{confirm: p => {mockConfirm = p}}
}), {virtual:true});
jest.mock("../../../../repos/ui/mfe-ratan-container/src/ratanutils/http/api", () => ({
 getFilterList:jest.fn(() => Promise.resolve([{rowKey:"role-owned", name:"Role filter", moduleOwner:"OPS", assigneeList:"OPS", body:"[]"}])),
 getFilterDetails:jest.fn(() => Promise.resolve({rowKey:"role-owned", moduleOwner:"OPS", assigneeList:"OPS", body:"{bad json"})),
 deleteFilter:jest.fn(() => Promise.resolve())
}));

test("CES malformed role-owned filter deletion remains pending", async () => {
 const {result} = renderHook(() => useController({filterFieldType:"TRADE_FILTER_BUILDER", bodyDefaultValue:[], searchFunction:jest.fn(), switchSearch:"filterSelector", FILTER_FIELDS:[]}));
 await waitFor(() => expect(result.current.filterList.TRADE_FILTER_BUILDER).toHaveLength(1));
 expect(result.current.currentFilter).toBeNull();
 await act(async () => {result.current.changeFilter("role-owned");});
 expect(mockConfirm).toBeDefined();
 await act(async () => {mockConfirm.onOk();});
 expect(api.deleteFilter).not.toHaveBeenCalled();
});
