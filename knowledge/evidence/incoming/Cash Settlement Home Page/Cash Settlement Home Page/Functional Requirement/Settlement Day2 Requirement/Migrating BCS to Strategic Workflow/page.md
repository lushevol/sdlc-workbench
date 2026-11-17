| Feature | Description | Dependency | Comment |
| --- | --- | --- | --- |
| Cashflow consumption | need to consume the cashflow in strategic flow - message bridge filter | reply on Stella to send the cashflow in strategic format | |
| Business rules | Need to review existing rules and confirm if any exclusion/inclusion to be considered - NSTP rules - Suppression rule （Swift/Cashflow） | | |
| User Profile | FMO_OPS is used for legacy flow, user need to switch the profile | | |
| Static data | NA Legacy flow and strategic flow share the same static - Nostro static - currency cut off - branch code mapping to be configured in FMRP process: - bridge account - swift related BIC (sender, 53, 58) | | |
| SSI stamping | - FMRP will have ****** in the query condition while current BCS not - FMRP SCB receive will pick primary nostro if no vostro, BCS does not have such logic | | |
| Swift Generation | if any specific logic from Razor side - to be analyzed or replay BCS prod data and recon - if we can use common DV prefix for BCS data instead of EQ prefix? impact to LMS as well, | | |
| Accounting | country scope: SG, UK, HK(fmid =2), JE EBBS accounting only? static data (bridge account) | | |
| CDU confirmation | - currently BCS cashflow is consuming the match status from CDU instead of TDS3 trade info - currently BCS STP process only enabled for internal clients (configured white list) | | |
| LMS integration | currently BCS will send LMS feed after cashflow stamped while FMRP will only send once cashflow released/settled | | |
| Available field for cash | BCS process will query trade to additionally get below field value and set to cashflow blotter Equity Instrument Reference Parent Trade Instrument ![image-2025-11-12_10-49-0.png](attachments/image-2025-11-12_10-49-0.png) | | |
| Historical data migration | | | |