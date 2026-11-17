# CES function entitlement test request

- Source: User message in the current Codex conversation.
- Date: 2026-11-17, Asia/Singapore.
- Scope: Draft value tests and discuss additional cases. API schema validation is excluded.

## Exact user input

The CES team agreed to add a function_entitlement field in their API response to ship all role names in X_RATANONE Please generate the corresponding test cases to verify whether this change works. We don’t need any schema validation; we only need to validate the value of this function entitlement.
Here are the test cases I can think of:
1. All current user roles must satisfy the values in our X_RATANONE security matrix.
2. The function entitlement of a general account must be the row corresponding to RATAN_FUNC.
3. If a user switches from one role to another, their function entitlement value should also change accordingly.
4. If a user previously had no X_RATANONE profile at all, when they are onboarded to an entitlement rule in CES, their function entitlement should change from empty to the corresponding profile.
5. If a user currently has a functional role in their CES entitlement roles, but is now off-boarded from that entitlement role, their function entitlement should be empty.
6. General accounts and user accounts cannot be mutually assigned. That is, a user cannot have both a functional entitlement and a profile for a general account, and a general account cannot have a user profile.
Please think of additional test cases and discuss them with me.

## Authority and limits

This message authorizes test specification and discussion.
The CES agreement is user-reported. No new-field response or deployed revision was supplied.
Implementation, account changes, live execution, publication, and deployment are not requested.
Additional proposed expectations require discussion where the source does not settle their meaning.
