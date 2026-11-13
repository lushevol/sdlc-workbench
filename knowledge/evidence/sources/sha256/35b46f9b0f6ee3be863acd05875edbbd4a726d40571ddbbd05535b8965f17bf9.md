## Plan

| | Option 1 Ratan/EBBS tech live together | Option 2 Ratan tech live on Solace integration only |
| --- | --- | --- |
| Details | Ratan to tech go live accounting service. Then the front to back processing could be verified, such as Ratan processing, Solace integration and EBBS setup 1. Lifecycle service 2. Accounting Service 3. Static Data service 4. Message bridge 5. Query service 6. Service Properties 7. Static 1. Nostro 2. Static (transaction/bridge) 3. Rules (keep production version, no change) | Ratan tech go live the integration with Solace only, and mock dummy ebbs feed to verify solace integration and EBBS setup only 1. Message bridge 2. Service Properties |
| CPT plan | 1. Ratan to mock a dummy payment with cashflow id CPTCF0000001, trade id, CPTTRADE0001 for IN entity, with a back value date 2. User manual fail the payment 3. Expectation 1. Ratan generate & publish accounting feed to EBBS 2. EBBS ACK back to Ratan 3. Accounting update on the dummy cashflow | 1. Ratan to mock a dummy EBBS feed (json) directly and publish to the solace topic 1. CFID: 00 2. Trade id: 00 2. Post new and reversal 3. Expect EBBS ACK back and Ratan consume the ACK |
| CPT condition | Amount < 0.001 2024-05-27 check with Karthick whether amount is OK Entity FMID for IN | |
| Progress | 2024-05-24 Deployed on UAT 2024-05-27 Regression in progress | |
| | | |

##