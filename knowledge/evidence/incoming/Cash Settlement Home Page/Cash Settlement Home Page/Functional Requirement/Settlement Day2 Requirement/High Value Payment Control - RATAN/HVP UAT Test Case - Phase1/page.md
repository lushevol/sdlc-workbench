## 1. Scope

### 1.1 In Scope

- BCS cashflow authorization-limit behavior for Phase 1.
- Add authorization limit check for NSTP Checker Approval. - Confirm Release -> Accept Release.
- Add authorization limit check for single-level Update Affirmation Status.
- Add authorization limit check for Release Failed Cashflow.
- Boundary validation against configured profile limits.

### 1.2 Out of Scope

- Downstream message fields: - stpFlag - lastUser
- FMRP cashflow scenarios.

## 2. Assumptions

- BCS uses the same authorization-limit framework as existing static profile limits.
- BCS non-USD limit conversion uses the same FX conversion service/rules/configuration as FMRP (no logic fork).
- Limit comparison operator is strict < (equal to threshold is not allowed).
- Test users and roles (maker/checker per profile) are pre-provisioned and active.
- UAT environment contains sufficient BCS cashflow data (including failed cashflow scenarios).

## 3. Profile Limits(USD)

| Profile | Limitation |
| --- | --- |
| FMO_OPS_BOC | < 30 Million |
| FMO_OPS_BO | < 100 Million |
| FMO_OPS_BOS | < 500 Million |
| FMO_OPS_BOL | < 1 Billion |
| FMO_OPS_BOM | < 4 Billion |

## 4. Test Cases

| ID | Module | Preconditions | Steps | Expected Result |
| --- | --- | --- | --- | --- |
| TC-001 | NSTP Checker Approval (Confirm Release -> Accept Release) | BCS cashflow is pending Confirm Release; checker profile=FMO_OPS_BOC; test amounts are 29,999,999 and 30,000,000 USD | 1) Maker submits release. 2) Checker clicks Accept Release for amount 29,999,999. 3) Checker clicks Accept Release for amount 30,000,000. | Amount 29,999,999 is accepted; amount 30,000,000 is rejected because BOC limit is less than 300,000,00. |
| TC-002 | NSTP Checker Approval (Confirm Release -> Accept Release) | Checker profile=FMO_OPS_BO; test amounts are 99,999,999 and 100,000,000 USD | 1) Maker submits release. 2) Checker clicks Accept Release for amount 99,999,999. 3) Checker clicks Accept Release for amount 100,000,000. | Amount 99,999,999 is accepted; amount 100,000,000 is rejected. |
| TC-003 | NSTP Checker Approval (Confirm Release -> Accept Release) | Checker profile=FMO_OPS_BOS; test amounts are 499,999,999 and 500,000,000 USD | 1) Maker submits release. 2) Checker clicks Accept Release for amount 499,999,999. 3) Checker clicks Accept Release for amount 500,000,000. | Amount 499,999,999 is accepted; amount 500,000,000 is rejected. |
| TC-004 | NSTP Checker Approval (Confirm Release -> Accept Release) | Checker profile=FMO_OPS_BOL; test amounts are 999,999,999 and 1,000,000,000 USD | 1) Maker submits release. 2) Checker clicks Accept Release for amount 999,999,999. 3) Checker clicks Accept Release for amount 1,000,000,000. | Amount 999,999,999 is accepted; amount 1,000,000,000 is rejected. |
| TC-005 | NSTP Checker Approval (Confirm Release -> Accept Release) | Checker profile=FMO_OPS_BOM; test amounts are 3,999,999,999 and 4,000,000,000 USD | 1) Maker submits release. 2) Checker clicks Accept Release for amount 3,999,999,999. 3) Checker clicks Accept Release for amount 4,000,000,000. | Amount 3,999,999,999 is accepted; amount 4,000,000,000 is rejected. |
| TC-006 | NSTP Checker Approval Cross Profile | One BCS cashflow amount is 550,000,000 USD; checker users from FMO_OPS_BOS and FMO_OPS_BOL are available | 1) BOS checker clicks Accept Release for amount 550,000,000. 2) BOL checker clicks Accept Release for amount 550,000,000. | BOS checker is rejected; BOL checker is accepted. |
| TC-007 | NSTP Checker Approval Missing Limit Mapping | BCS cashflow is pending Confirm Release; checker has no valid approval limit mapping | Checker clicks Accept Release. | Action is blocked with authorization or limit error; transaction state remains pending. |
| TC-008 | Cashflow Affirmation Update Affirmation Status BOC Boundary | BCS cashflow is eligible for Update Affirmation Status; user profile=FMO_OPS_BOC; amounts are 29,999,999 and 30,000,000 USD | User executes Update Affirmation Status for amount 29,999,999 and 30000000. | Amount 29,999,999 succeeds; amount 30,000,000 is blocked by authorization limit check. |
| TC-009 | Cashflow Affirmation Update Affirmation Status BO Boundary | User profile=FMO_OPS_BO; amounts are 99,999,999 and 100,000,000 USD | User executes Update Affirmation Status for amount 99,999,999 and 100,000,000. | Amount 99,999,999 succeeds; amount 100,000,000 fails. |
| TC-010 | Cashflow Affirmation Update Affirmation Status BOS Boundary | User profile=FMO_OPS_BOS; amounts are 499,999,999 and 500,000,000 USD | User executes Update Affirmation Status for amount 499,999,999 and 500,000,000. | Amount 499,999,999 succeeds; amount 500,000,000 fails. |
| TC-011 | Cashflow Affirmation Update Affirmation Status BOL Boundary | User profile=FMO_OPS_BOL; amounts are 999,999,999 and 1,000,000,000 USD | User executes Update Affirmation Status for amount 999,999,999 and1,000,000,000. | Amount 999,999,999 succeeds; amount 1,000,000,000 fails. |
| TC-012 | Cashflow Affirmation Update Affirmation Status BOM Boundary | User profile=FMO_OPS_BOM; amounts are 3,999,999,999 and 4,000,000,000 USD | User executes Update Affirmation Status for amount 3,999,999,999 and 4,000,000,000. | Amount 3,999,999,999 succeeds; amount 4,000,000,000 fails. |
| TC-013 | Cashflow Affirmation Cross Profile | One BCS cashflow eligible for Update Affirmation Status; amount is 1,500,000,000 USD; users from FMO_OPS_BOL and FMO_OPS_BOM are available | 1) BOL user executes Update Affirmation Status for amount 1,500,000,000. 2) BOM user executes Update Affirmation Status for amount 1,500,000,000. | BOL user is rejected due to limit; BOM user succeeds. |
| TC-014 | Release Failed Cashflow Checker Limit BOC | Checker profile=FMO_OPS_BOC; amounts are 29,999,999 and 30,000,000 USD | Checker confirms failed release for amount 29,999,999 and 30000000. | Amount 29,999,999 succeeds; amount 30,000,000 fails. |
| TC-015 | Release Failed Cashflow Checker Limit BO | Checker profile=FMO_OPS_BO; amounts are 99,999,999 and 100,000,000 USD | Checker confirms failed release for amount 99,999,999 and 100,000,000. | Amount 99,999,999 succeeds; amount 100,000,000 fails. |
| TC-016 | Release Failed Cashflow Checker Limit BOS | Checker profile=FMO_OPS_BOS; amounts are 499,999,999 and 500,000,000 USD | Checker confirms failed release for amount 499,999,999 and 500,000,000. | Amount 499,999,999 succeeds; amount 500,000,000 fails. |
| TC-017 | Release Failed Cashflow Checker Limit BOL | Checker profile=FMO_OPS_BOL; amounts are 999,999,999 and 1,000,000,000 USD | Checker confirms failed release for amount 999,999,999 and 1000000000. | Amount 999,999,999 succeeds; amount 1,000,000,000 fails. |
| TC-018 | Release Failed Cashflow Checker Limit BOM | Checker profile=FMO_OPS_BOM; amounts are 3,999,999,999 and 4,000,000,000 USD | Checker confirms failed release for amount 3,999,999,999 and 4000000000. | Amount 3,999,999,999 succeeds; amount 4,000,000,000 fails. |
| TC-019 | Release Failed Cashflow Cross Profile | Failed cashflow amount is 550,000,000 USD; checkers from FMO_OPS_BOS and FMO_OPS_BOL | 1) BOS checker confirms failed release for amount 550,000,000. 2) BOL checker confirms failed release for amount 550,000,000. | BOS checker is rejected; BOL checker is approved. |
| TC-020 | Non-USD Smoke for NSTP Accept Release | Non-USD BCS cashflow exists for example HKD; valid FX rate is available; converted USD amount case includes one below limit and one at or above limit | Execute Confirm Release -> Accept Release for both non-USD test records. | System converts to USD equivalent and applies the same limit rule correctly for both records. |
| TC-021 | Non-USD Smoke for Update Affirmation Status | Non-USD BCS cashflow exists for example HKD; valid FX rate is available; converted USD amount case includes one below limit and one at or above limit | Execute Update Affirmation Status for both non-USD test records. | System converts to USD equivalent and applies the same authorization limit rule correctly. |