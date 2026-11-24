## A) Outbound Email Automation - Elimination of EUC (NFR)

### High Level Requirements

| Proposed System | Area | Requirement | Details | Comments |
| --- | --- | --- | --- | --- |
| RATAN | **Cashflow Scope & Publishing ** | - RATAN to publish the cashflow including SI to CDUPS based on specific scope - Ability to configure the publishing criteria at a granular level based on any of cashflow / Trade (post UBER) values | - Configuration table for Booking Entity + Client (FMID/BIC)+ Client + Product (Granular levels) + Portfolio + Source (LoanIQ) + Payment Type + Settlement Method - In Scope Cashflow status to be able to configure based on scenarios - Scenario 1: Exclude STP flows (i.e., send only WAITING + Pending Operator status) - Exclude statuses which is still under processing (Pending fixing / another leg) - Scenario 2: Include all valid cashflows of client (Even STP’d ones) - Exclude specific Portfolios / Product Granular levels (example: Strategies) - Include Client’s SSI information - Include SCB Nostro information - For Netting scenario need to include the net amount as well as breakdown of cashflow | - For Eclipse clients send based on client type (corp / bank) and portfolio - SIP trades identified via strategy - SLT-CUST & LOAN related cashflows to be excluded - Swap Agent - only specific Payment Types are bilaterally affirmed and settled - CCIL Settlement Method - Explore inclusion of calculation details for IRS/CCS |
| RATAN | ** Audit & Filtering** | - Consume from CDUPS & Update Cashflows with email dispatch date & time - Ability to filter cashflows where Email Sent Successfully / Failed / Pending Response | | |
| RATAN | ** Adhoc handling** | - Ability to manual trigger when new / revised cashflows received - Exclude cashflows from publish (manual stop) | | |
| RATAN | **Trigger Times** | - Ability to publish the cashflow at pre-defined times (configurable) | - Single trigger time for multiple booking entities - Release time for a specific booking Entity - Single release time across Clients of a booking entity - Multiple release times for different clients of a booking entity | Example: East sites require publishing at 1pm MYT |
| CDUPS | **Maintenance of Email Templates** | - Ability to maintain Email Templates - Ability to trigger Chasers utilizing original email (Phase 2) | - Standard Template for Email - Different templates by type of settlement Gross, Bilateral Netting, BIC Netting - Configurable by country / product / other parameters - Configurable by specific client (changes via email subject / body) | Location information to be included in the email based on Strategy |
| CDUPS | **Maintenance of Client contacts** | - Ability to setup email contacts (with maker+checker) for counterparties. - Client contacts to be setup at FMID / BIC level (BIC netting). - Copy of Email to be sent to SCB Contacts (configurable Booking Entity + Product level) | - Client contacts might be different based on product taxonomy granularity. - Single mail id for a client across multiple products - Same email id used, but two emails expected to be sent (1 for rates and another for commodity) - Multiple mail ids for a client based on product - Need to support Murex as well as FMRP product granularity. - Maintenance via Maker+Checker - Client contacts may be different from existing contacts used for Confirmation / FX netting hence it should be stored in a separate table | |
| CDUPS | **Email dispatch, Audit & Exception Handling** | - Generate Email and send via MDIS - Attachments should be encrypted as per Bank standards - Store Audit Information & feed back to RATAN - Ability to track successful dispatch / failures | - After email is successfully dispatched, feed information back to RATAN of success / failure - Email delivery failure to be intimated to SCB Contacts (esp. 1 email Nack out of multiple client ids) - Highlight CDUPS email dispatch issues to users (Email Id not configured as an example) | **What will be sender email id?** (this is what clients will reply back to) |

Sample mail ID's

| **Cpty** | **Group/Products ** | **Email receipient** |
| --- | --- | --- |
| UOB | OPT | [CommoditiesDerivatives@UOBgroup.com](mailto:CommoditiesDerivatives@UOBgroup.com) |
| UOB | FX | [TCMOPreciousMetals@UOBgroup.com](mailto:TCMOPreciousMetals@UOBgroup.com) |
| Nomura | OPT | [otcsettlements@nomura.com](mailto:otcsettlements@nomura.com) |
| Nomura | FX | [fxopssettlements@nomura.com](mailto:fxopssettlements@nomura.com) |

Below have been incorporated into requirements table

- ~~RATAN to export the cashflow data <u>for specific entities</u> including SI to email application. The timing will be different for different countries / group of countries~~ - ~~East: 1pm MYT~~ - ~~West: TBC~~ - ~~Other countries - NA~~
- ~~Ability to setup email contacts (with maker+checker) for counterparties. Client contacts to be setup at FMID / BIC level (BIC netting). Client contacts will be different based on product taxonomy granularity. Need to support Murex as well as FMRP product granularity.~~
- ~~Copy of email must be sent to Settlements team - configurable table required based on countries / teams~~
- ~~Client contacts may be different from Confirmation / FX netting client contacts~~
- ~~Email application to dispatch the email to clients using a standard email template with cashflow + SI data (design to factor in ability to customize the template for different countries if required)~~
- ~~Email to be encrypted if required as per bank policy~~
- ~~Scenario includes Gross & Net affirmation, including BIC netting~~
- ~~Intimation to be sent back to RATAN on Initial Ack and subsequent successful email dispatch to Clients~~
- ~~In RATAN - information to be added onto cashflows on date & time when email was sent to Clients~~
- ~~Ability to filter and differentiate between Clients where settlement affirmation has been sent vs others~~
- ~~Chaser capability is required utilizing previous mail ~~
- ~~Any other requirements from team maintaining the client contacts? - Sathya Priya to confirm~~

Most of below have been incorporated in some shape or form where relevant. Others not in scope.

09th March: Granular scope of affirmation (from Mazween)

1. Stop outbound email for Eclipse clients (corporate) but send only for Interbank (Portfolio wise)
2. Stop outbound email for SIP trades, but send only for the rest (Strategy wise)
3. Ability to send affirmation to different rrecipient based on product types
4. Send affirmation based on transaction ID instead of only trades who fail stp
5. Generate email affirmation at specified time
6. Ability to re-generate email affirmation with new details whenever there is revised cash flow booked.

20 March: Input from Babu:

- Cashflows with Pending Another Leg needs to be excluded from Affirmation.
- SLT-CUST & Loan related cashflows should be excluded from Affirmation
- Swap Agent Trades (Payment type - Coupon & Interim MTM) needs to be excluded

25 March: Input from Meha:

- NDF deals split between Razor and Ratan.
- CCIL deals should not be included for this email trigger.
- All Corporate clients are NSTP in India due to docs check/cross conversion settlement involved.
- Bank clients may have product wise emails contacts.

01 Apr: Input from Synthia:

- Ability to send emails to different recipient if trade is islamic (identifier - Portfolio starts with 'ISL' )- TBC if feasible. To explore in FMRP taxonomy.
- Ability to stop trigger of emails on adhoc basis (client starts to book Islamic deals)

Other Considerations:

- Stopping Outbound Email to specific Clients if - Where Ops sent email manually due to adhoc demand (or) - The client has initiated affirmation email to us - Inform clients that we would trigger the Affirmation Email (or) - Exclude clients who would initiate Email to us - Data sent from RATAN to CDUPS: Possible to support by providing special profile for Settlement team to login to CDUPS and stop the outbound email - David / Weng Hien to decide if this is required - Data not yet sent from RATAN to CDUPS: No viable solution at this point as there is no data point available to RATAN to exclude the specific client data from sending to CDUPS
- Handling of new cashflows flown into RATAN post the previous dataset sent to CDUPS - May have to be handled manually as need to link back to the previous email sent

## B) Inbound Email Automation - Artificial Intelligence (AI) use case (Markets Efficiency)

### High Level Requirements

- Inbound Client response must be routed to an AI layer to determine if the response is positive or negative / ambiguous
- AI layer to feed the response outcome (Positive - Y/N) to RATAN
- Audit trail to capture information that email has been sent to client and response received
- For positive affirmations, RATAN to capture a special indicator for checker that the affirmation is based on AI response
- RATAN to automate the maker part by removing the pending affirmation check. Cashflow will remain as NSTP if there are other outstanding exceptions on the cashflow
- For Negative / ambiguous response, RATAN to capture an indicator for maker that affirmation response is received but needs Maker intervention