import { Hooks } from "../Root/import"
import { hasPermission } from "./authenticator"


test("User has X_RATANONE entitlement", () => {
  jest.spyOn(Hooks, "getHooks").mockImplementation(()=>{
    return {
      store: {
        user: {
          id: "1000",
          fullName: "test",
          entitlements: {
            "X_RATANONE:TEST": {
              "SUBJECT_TEST": ["TEST_ACTION"]
            }
          }
        }
      }
    }
  })
  expect(hasPermission("SUBJECT_TEST:TEST_ACTION")).toBe(true);
  expect(hasPermission("SUBJECT_TEST:WRONG_ACTION")).toBe(false);
});

test("User entitlements has outstanding", () => {
  jest.spyOn(Hooks, "getHooks").mockImplementation(()=>{
    return {
      store: {
        user: {
          id: "1000",
          fullName: "test",
          entitlements: {
            "SUBJECT_TEST": {
              "Subject Test": ["TEST_ACTION"]
            },
            "RATAN_SETTLEMENT_STP_RULE": {
              "RATAN Settlement NSTP Rule" : ["TEST_ACTION"]
            },
            "WRONG_SUBJET": {
              "Subject Wrong Word": ["TEST_ACTION"]
            },
          }
        }
      }
    }
  })
  expect(hasPermission("SUBJECT_TEST:TEST_ACTION")).toBe(true);
  expect(hasPermission("SUBJECT_TEST:MISSING_ACTION")).toBe(false);
  expect(hasPermission("RATAN_SETTLEMENT_STP_RULE:TEST_ACTION")).toBe(true);
  expect(hasPermission("WRONG_ENTITY:TEST_ACTION")).toBe(false);
  expect(hasPermission("WRONG_SUBJET:TEST_ACTION")).toBe(false);
  
})
