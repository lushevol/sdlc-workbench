# Background

The dashboard is for user to check categorized cashflow/exception status.

# Requirement ADO

[[RATAN-14764] [CN-Cash Settlement-Dev] - Dashboard MVP - Jira (standardchartered.com)](https://jira.global.standardchartered.com/browse/RATAN-14764)

# Dashboard UI

![image2024-7-10_16-54-10.png](attachments/image2024-7-10_16-54-10.png)

## Quick Search

to support user to refresh the dashboard with search criteria

![image2024-7-11_10-50-33.png](attachments/image2024-7-11_10-50-33.png)

- **Country: **mapped country list | Value in dropdown | Mapped query condition | | --- | --- | | China | | **Booking Entity:** hard coded list from FE. list of in scope booking entity FMCODE
- **Client Type: **hard coded list from FE. List of in scope client type
- **Status: **hard coded list from FE. list of in scope cashflow status
- **Sub Status: ** - Pending Operator - Pending Verification

## Counting Banner

![image2024-7-11_10-51-3.png](attachments/image2024-7-11_10-51-3.png)

- **Waiting VD Today**: Cashflow State = "WAITING" and Payment Date = Current Date
- **Failed VD Today**: Cashflow State = "FAILED" and Payment Date = Current Date
- **Error: **Cashflow State = "Error" and Payment Date >=Current Date and Payment Date<=Current Date + 7D
- **Accounting Error:** Accounting Status in ('SENT', 'DISABLED','HOLDING','REJECTED','MISSING_INFO')
- **Swift Error: **Swift Status in ('AMH Error', 'FMSGW Error', 'FMSRE Error', 'MX Generation Error', 'Ratan Internal Error', 'SCPAY Error')
- **Queued**:
- **Hold**:
- **Group Pending** : Group State ='PENDING'
- **Group Error**: Group State ='ERROR'

## Cashflow Pending Settlement

![image2024-7-11_11-10-39.png](attachments/image2024-7-11_11-10-39.png)