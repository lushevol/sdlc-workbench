### Data flow of NSTP exception:

### Notes:

1. Add "nstp_exception" field to data model of "cashflow_data", "cashflow_data_history".
2. DomainEvents (Topic: cash_settlement_cashflow_domain_events) : 1. includes Create/Amend/Status update, else? 2. query nstp exception every time when events meet the condition?
3. "nstp_exception" db value e.g. "Missing Vostro; Net Cashflow; Pending Affirmation; CORP Client; Back Value Date".
4. Frontend → Backend: 1. API refs to: /graphql {query：cashflowsNew & graphCashFlowDetails} 2. "${RegExp_String}" format. (Postgres support "POSIX" Regular expression).
5. query service → exception platform: 1. query params: cashflow_id 2. get all exception_code and order by exception_time.

DomainEvent example:

```js
{
  "messageId": "4cecb6d45f6b47a68a96c9500aa0a023",
  "aggregateId": "007690235374",
  "aggregateType": "Cashflow",
  "type": "CashflowStatusUpdateEvent",
  "payload": {
    "cashflow": {
      "cashflowId": "007690235374",
      "cashflowBusinessVersion": "3",
      "cashflowVersion": "0",
      "cashflowMinorVersion": "2",
      "cashflowStatus": "WAITING",
      "cashflowSubStatus": "Pending Verification",
      "cashflowSubStatusType": "Pending Exception",
      "cashflowSubStatusUpdater": "1289935",
      "action": "SsiStamped",
      "cashflowEvent": "NetNew",
      "actionTime": [
        2024,
        8,
        13,
        8,
        30,
        21,
        446952080
      ],
      "nettingId": "042a72db-5949-11ef-ad31-005056ac98cc",
      "splittingId": null,
      "comment": "",
      "reversalTag": null,
      "accountingStatus": null,
      "accountingReason": null,
      "swiftStatus": null,
      "swiftReason": null,
      "swiftMessageStandard": null,
      "currency": "USD",
      "bookingFmid": "10075222",
      "amount": "435500.0000",
      "tradeOriginalSourceSystemName": null,
      "cashflowRowData": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!-- edited with XMLSpy v2013 (x64) (http://www.altova.com) by Amit Kumar Singh (STANDARD CHARTERED BANK) -->\n<scb:SCBML xmlns:scb=\"http://www.sc.com/SCBML-1\"\n ..."
    }
  },
  "version": 4009360,
  "revision": 5,
  "timestamp": 1723537821446,
  "metadata": {
    "traceId": "w-7caf1ee75dbe4ab29f8dfc29ca37bf0e"
  },
  "status": "PUBLISHED"
}
```

### Q&A:

1. Detail History page already exists a field "NSTP Code"?
2. "cashflow_data" contains a column named"cashflow__nstp_reason"?

### FMO portal scenario:

Cashflow Blotter Customer View:

![image2024-8-20_16-21-37.png](attachments/image2024-8-20_16-21-37.png)

Cashflow Blotter List Horizon Filter:

![image2024-8-20_16-12-32.png](attachments/image2024-8-20_16-12-32.png)

Cashflow Blotter Detail History:

![image2024-8-20_16-11-50.png](attachments/image2024-8-20_16-11-50.png)

### Add RESTful API schema:

#### Exception platform service (for GUI):

- Post: /v1/rep/exceptions/nstpExceptionCodes/byStatus
- Request payload: e.g. [ "PENDING_OPERATOR", "PENDING_VERIFICATION" ]
- Response payload: e.g. [ { label: "Pending Affirmation", value: "Pending Affirmation", exceptionCategory: "NSTP" },{ label: "Missing Vostro", value: "Missing Vostro", exceptionCategory: "NSTP" } ]