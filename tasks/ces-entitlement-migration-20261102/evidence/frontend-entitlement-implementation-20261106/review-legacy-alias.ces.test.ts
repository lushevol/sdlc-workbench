import * as baseline from "./baseline-container-authenticator";
import * as candidate from "../../../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator";
import captured from "./review-legacy-alias-fixture.json";
let mockStore = captured;
jest.mock("../../../../repos/ui/mfe-ratan-container/src/Root/import", () => ({Hooks:{getHooks: () => ({store:mockStore})}}));
test("captured EMS2 human-readable subject preserves its normalized public permission code", () => {
 const code = "FSS_SERVICES_PEREGRINE:View";
 expect(baseline.hasPermission(code)).toBe(true);
 expect(candidate.hasPermission(code)).toBe(true);
});
