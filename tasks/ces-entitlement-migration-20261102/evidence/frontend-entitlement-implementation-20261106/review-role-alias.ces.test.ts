import {isRoleOwnershipPending} from "../../../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator";
import {saveView} from "../../../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/store";
import * as api from "../../../../repos/ui/mfe-ratan-container/src/ratanutils/http/api";
const mockStore = {user:{id:"1481696"},entities:[],entitlementRouting:[
 {tileId:"1",source:"EMS2",entityNames:["X_RATANONE"],features:["RATAN_CASHFLOW_BLOTTER"]},
 {tileId:"2",source:"EMS2",entityNames:["X_RATANONE"],features:["RATAN_STRATEGIC_CASHFLOW_BLOTTER"]},
 {tileId:"3",source:"EMS3",applicationId:"51358",entityNames:["RATAN_ENTITLEMENT_RULE"],features:["RATAN_STRATEGIC_CASHFLOW_BLOTTER"]}
]};
jest.mock("../../../../repos/ui/mfe-ratan-container/src/Root/import", () => ({Hooks:{getHooks:() => ({store:mockStore})}}));
jest.mock("../../../../repos/ui/mfe-ratan-container/src/ratanutils/utils", () => ({deepClone:x => JSON.parse(JSON.stringify(x))}));
jest.mock("../../../../repos/ui/mfe-ratan-container/src/ratanutils/componentEnabling", () => ({getEnable:() => true}));
jest.mock("../../../../repos/ui/mfe-ratan-container/src/ratanutils/http/api", () => ({postSaveView:jest.fn(params => Promise.resolve(params))}));
test("an unresolved configured CES alias keeps cashflow role ownership pending", () => {
 expect(isRoleOwnershipPending("CASHFLOW_VIEW_BUILDER")).toBe(true);
});
test("an ambiguous cashflow builder sends no role-owned create request", async () => {
 let rejection;
 try { await saveView({rowKey:"",name:"Role View",assigneeList:"OPS",moduleOwner:"OPS",body:[],viewFieldType:"CASHFLOW_VIEW_BUILDER",chooseAuthority:false}); }
 catch(error) {rejection=error;}
 expect(api.postSaveView).not.toHaveBeenCalled();
 expect(rejection?.message).toMatch(/CES role ownership is pending/);
});
