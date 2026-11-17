# Open Questions 251015

1. What's the users from ratan to blade (trade control) ? What's the users from blade to ratan (MO) ?
2. Should those users share the same sso ? How users entitled cross 2 system ?
3. Ratan should own an openfin desktop client ourself.
4. A proper workflow from blade to ratan: blade get FMAA token then pass request with token, ratan doesn't login, FDC3 broker check token is valid and open a public tile of remaining amount.

---

# Plan

| Project Initiative | Feature | Description | Priority | ETA (MD) | Plan |
| --- | --- | --- | --- | --- | --- |
| BAU | Revisit the Tenant Onboarding Process and Mandatory Steps Guide | - build the check list for tenant onboarding, summary key steps and check points. - build the dev support model includes early engagement, effort tracking, dev support, go live support etc - Broadcast process update to each tenant | 1 | 10 | 25Q3 |
| BAU | Admin Module Enhancement and Go live | - Layout enhancement for tile, category and import map management - Setup EMS2 roles - Business Go live | 1 | 20 | 26Q1 |
| BAU | Entra Id Integration | - Technical Assessment of Entra integration solution - Implement Entra Id as a new user login approach - Implement M2M login via Entra Id to replace FMAA - Build feature flag to control the login entry - Integration testing and UAT signoff - Business Go live - Decommission oneMFA and FMAA | 2 | 50 - analysis + poc: 10 - impl ui: 5, impl backend: 10 - integration & testing: 10 - UAT: 5 - DevOps: 5 - Decom: 5 | 26Q1 |
| FM Enabler | OneFM UI: Blade - Ratan integration | - FDC3 Interoperability solution of Post Trade Portal - FDC3 internal & external (Blade) integration - Build "Counterparty Detail" and allow open by Intent - Build "Blade to Cashflow Blotter FXU" and allow open by intent | 1 | 80 | 25Q4 |
| BAU | Post Trade Portal Layout Strategy (UX Branding) | - Align the design patten with SC brand - build prototype of current layout - collect feedback for further enhancement | 3 | 10 | 26Q1 |
| BAU | Post Trade Portal BAU enhancement | - Enhance loading performance of initialing resource - <collecting new> | 3 | TBD | TBD |

### Appendix

FDC3 ETA

![image-2025-8-25_15-4-9.png](attachments/image-2025-8-25_15-4-9.png)

# OpenFin Discussion

## Open Questions

| # | Category | Question / Topic | Owner / Stakeholder | Notes / Next Steps |
| --- | --- | --- | --- | --- |
| 1 | Installer Ownership | - Who will own the OpenFin installer? - Where is it maintained? - Who can apply changes? | TBD | Define owner and access policy |
| 2 | Runtime Maintenance | - Who maintains RVM and runtime updates? - How will the update strategy be managed (frequency, approval, deployment) ? | TBD | Establish update/rollback process |
| 3 | Rollback/Restore | - What is the rollback plan if there is an issue with a new version? - What is the restore plan if the installation fails? | TBD | Document rollback/restore steps |
| 4 | Onboarding Process | - How does PTP onboard to OpenFin ? - How do business users onboard ? - (Question for us) How do tenant apps onboard ? | TBD | Clarify onboarding workflow |
| 5 | OneFM Scope | - What is the OneFM concept and scope? - Which businesses are included? | TBD | Define scope and business list |
| 6 | Support Responsibility | - What are the support responsibilities for OpenFin/OneFM/PTP/Tenant when issues occur ? - How to identify the issue ? | TBD | Assign support roles |
| 7 | Authentication | - What is the solution for authentication alignment? - How does OneFM login and pass credentials to PTP when opening (first launch)? - How are credentials renewed for both OneFM and PTP? | TBD | Design auth flow and renewal logic |
| 8 | Auth Error Impact | - If one application encounters an authentication error (e.g., token expired), will it impact other applications? | TBD | Assess isolation and impact |
| 9 | Authorization | - How is authorization alignment handled? - How do we ensure users are controlled by the same entitlements across applications? | TBD | Align entitlement management |
| 10 | FDC3/Observability | - How is FDC3 Intent observability handled? - How are apps launched (blade to ratan)? | TBD | Define observability/launch flow |

## User Story

| | User Story | Use Case | Detail Description | Technical Design | Wireframe or Logic Diagram |
| --- | --- | --- | --- | --- | --- |
| 1 | Ratan on board to OpenFin | - User can login to Ratan via OpenFin. - User can view and select tiles - User can perform business in tiles | - Authentication should be the same with MFE. - Authorization should be the same with MFE. - Permission control should be the same with MFE. - Other approach should be the same with MFE. | | |
| 2 | Ratan extends interoperability with FDC3 in OpenFin | - Migrate existing internal invoke to FDC3 | - Collect existing ratan internal interop actions. - Design and implement - Add authorization control | | |
| 3 | In Openfin blade can call post trade portal functions via Intent | | A central broker for FDC3 inbound and outbound requests, handle intent properly. | FDC3 Broker | |
| 4 | | Could open tiles and route intent to target tiles. | Routing logic | |
| 5 | | Handle intent with time sensitive reaction. | Tile Listener design | |
| 6 | In post trade portal, application can register there Intents and allow other system to invoke | | | Admin Module | |
| 7 | Authentication & Permission Control to Intents | | | | |
| 8 | Frameless Component Call | Able to call a frameless component instead of whole mfe shell or entire app. | | | |

## Internal & External FDC3

## Frameless Components