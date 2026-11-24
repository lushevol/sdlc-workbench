import { extractProfileBySubject, getBrowserFingerprint } from "./utils";

it("extractProfileBySubject", () => {
    expect(
        extractProfileBySubject(
            {
                "TEST_SUBJECT:TEST_PROFILE": {
                    "TEST_APPLICATION": ["TEST_ACTION"]
                }
            },
            "TEST_SUBJECT"
        )).toBe("TEST_PROFILE");
});

it("getBrowserFingerprint", () => {
    expect(getBrowserFingerprint()).toEqual(getBrowserFingerprint());
});
