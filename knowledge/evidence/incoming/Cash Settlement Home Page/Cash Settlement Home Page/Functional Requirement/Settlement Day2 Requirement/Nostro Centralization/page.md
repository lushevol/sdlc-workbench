# Background

Currently Nostro static are maintained in each TP system with different format which is expected to be consolidated in NAMS. After that, data ops will create/amend/close the static in SSI+ and TP system need to integrate and consume data with SSI+.

# ADO

# Requirement Details

Rough Estimation: 170

1. **Nostro Stamping**: - 30+15 1. set up new connection with SSI+ to query nostro data 2. message format and mappings to be confirmed 3. Ratan impacted feature: 1. cashflow/ trade stamping nostro query 2. accounting nostro query
2. **Nostro Notification**: 20+15 1. consume nostro static event (New/Update/Delete) and trigger the nostro refresh 2. message format and mapping to be confirmed 3. if any other event beyond new/update/delete... 4. impacted function
3. data format changes 1. for example: Ratan use "NOS" in settlement means while Razor use "Nostro"
4. NFR: 20
5. Data migration support 20 1. historical cashflow linked nostro ID should be refreshed or ?
6. QA: function/regression/automation -50
7. Overlap with other requirement: 1. RFI stamping: need to add portfolio and nostro mapping 2. Keystone (plan to be live in Feb.2026)