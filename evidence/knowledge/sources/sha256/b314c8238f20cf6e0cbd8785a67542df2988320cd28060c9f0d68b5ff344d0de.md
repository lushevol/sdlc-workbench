📎 [Netting Story Board - Ratan S2BNG.pdf](attachments/Netting Story Board - Ratan S2BNG.pdf)

# Ratan Only

- Maker / checker Profile and Limits for FMO users
- Manual release of net cashflow with maker checker workflow
- Consume Netting information from GTSS
- Net to Gross requests by Netting Client to go to exception Queue(NSTP)
- No net or un-net action on > Released cashflow (Razor>FMSRE)- Soft block - incremental to be posted
- GIVE UP CLIENTS: Validation logic same SWIFT BIC/same Currency/same SCB entity/same value date/same Settlement method/same product (CFI code)
- TLM should auto-match many trade to one cashflow for Bridge suspense reconcilaiton based on common Net ID
- Support workflows for CLS netting
- Support for inter-entity netting (LCM)

# Both S2BNG and Ratan

- FMO Users should be able to select two or more cashflow for netting
- TCRM Workflow trigger for Netting to Gross requests for Netting Clients (UK & US)
- Ability to Net as long as cashflow is not released
- Ability to configure threshold for net to gross to trigger TCRM approval (UK & US)
- For Default Netting Clients, the net amount should be shown by default with option to drill down into trades
- Validation Logic- If a deal is DVP, system should not allow to move into netting
- Net within and across Products
- Perform Ad hoc netting of Gross Cashflows
- For unreleased net cashflow if a trade is amended impacting a component cashflow, an exception should be created for users to manually review and accept the new net cashflow prior to release
- Ability to config netting at product(CFI lowest level) , instrument currency level for a specific client
- Ability to Net cashflows generated via Split
- Display on screen notification for netting success/fail
- One side of a FX trade can be independently netted, but the other side must follow NET settlement method
- Netting must be allowed only within the same SCB Entity
- Send affirmation email for netting set validation. Ability for clients to set notification preferences. CADM to be source of client (TBC)
- View component net cashflow
- Ability to Filter and view net cashflow from the cashflow blotter
- Display net cashflow
- Display netting activity in audit trail
- Un-net and re-net functionality
- Allow SI amend on net cashflow prior to release status
- Batch process netting for auto-function at X date
- Ability to configure the timing of netting scriipt at a client level - FMID or LEI
- NON GIVE UP: Validation logic same FMID/same Currency/same SCB entity/same value date/same Settlement method/same product (CFI code)