#

# 1、Utilization Response Enrich

```
{
  "Utilization": {
    "Utilization_Id": "71110111971",
    "Response": "ACK",
    "Error_Reason": null
  },
  "Request_Info": {
    "Utilization": {
      "Utilization_Id": "71110111971",
      "Orig_Utilization_Id": null,
      "Util_Type": "EARLY-FULL-UTIL",
      "AACode_Comments": "FX",
      "Util_Payment_Ref": "1",
      "Maker_ID": "1642375",
      "Checker_ID": "1376381",
      "Trade": {
        "Trade_Id": "7111011197",
        "Trade_Lake_Trade_Major_Version": "1",
        "Swap_Leg_ID": "",
        "Exchanged_Currency1_Payment_Amount_Currency": "USD",
        "Exchanged_Currency1_Util_Amount": "200.0",
        "Exchanged_Currency2_Payment_Amount_Currency": "SAR",
        "Exchanged_Currency2_Util_Amount": "749.98"
      }
    }
  }
}


```

# 2、Auto Utilization Response

```
 {
    "Utilization_Id": "fxu.1711101119712.6721092670",
	"Trade": {
        "Trade_Id": "6721092670",
        "Swap_Leg_ID": "",
        "Exchanged_Currency1_Payment_Amount_Currency": "USD",
	    "Exchanged_Currency1_Util_Amount": 100.0,
        "Exchanged_Currency1_Remaining_Amount": 0,
 	    "Exchanged_Currency2_Payment_Amount_Currency": "EGO",
	    "Exchanged_Currency2_Util_Amount": 10000.0,
        "Exchanged_Currency2_Remaining_Amount": 0
     }
  }
```

# 3、Tech Failed Response

- Invalid Request Data

When the utilization request data is not JSON well-formatted, utilization will response below.

```
{
  "Utilization": {
    "Utilization_Id": "",
    "Response": "NACK",
    "Error_Reason": "Raw message error."
  },
  "Request_Info": {
    "Raw_Request": "{\n  \"Utilization\": {\n    \"Utilization_Id\": \"6721092670\",\n    \"Util_Type\": \"VDATE-FULL-UTIL\",\n    \"AACode_Comments\": \"AACode_Comments\",\n    \"Util_Payment_Ref\": \"Util_Payment_Ref\",\n    \"Maker_ID\": \"8220478\",\n    \"Checker_ID\": \"1633330\",\n    \"Trade\": {\n      \"Trade_Id\": \"6721092670\",\n      \"Trade_Lake_Trade_Major_Version\": \"1\",\n      \"Swap_Leg_ID\": \"\",\n      \"Exchanged_Currency1_Payment_Amount_Currency\": \"USD\",\n      \"Exchanged_Currency1_Util_Amount\": 30.0\n    }\n  }"
  }
} 
```

- Ratan Internal Error

When utilization request encounter a Ratan Internal Error, utilization service will use DLQ to retry 5 times at most and then response:

```
{
  "Utilization": {
    "Utilization_Id": "7721092670",
    "Response": "NACK",
    "Error_Reason": "Ratan internal error."
  },
  "Request_Info": {
    "Utilization": {
      "Utilization_Id": "7721092670",
      "Orig_Utilization_Id": null,
      "Util_Type": "EARLY-PART-UTIL",
      "AACode_Comments": "FX",
      "Util_Payment_Ref": "1",
      "Maker_ID": "1642375",
      "Checker_ID": "1376381",
      "Trade": {
        "Trade_Id": "7721092670",
        "Trade_Lake_Trade_Major_Version": "1",
        "Swap_Leg_ID": "",
        "Exchanged_Currency1_Payment_Amount_Currency": "USD",
        "Exchanged_Currency1_Util_Amount": "50"
      }
    }
  }
}
```

# 4、Manual Settlement Method GROSS↔UTIL

[Story 11834223 [FXU] Move from Utilization to Gross settlement](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11834223)

This design is related to settlement method field value change with value GROSS and UTIL in bidirectional in cashflow data. While UITL means these cashflows belongs to FXU scope and GROSS means they are in GROSS scope. So the entry point is in utilization service.

The key points list below:

- This function takes effective **immediately **in trade level after manual action.
- When UTIL to GROSS, the pastdue accounting **reversal **event should be generated immediately if exists pastdue accounting.
- The '**Withdrawal**' event's settlement method value **overwrite **by the latest '**New**' event field value to support the settlement method keep consistent after settlement method change action.
- Support batch operation.

## Settlement Method Change Action Flow

## GROSS→ UTIL + Withdraw with GROSS

if no utilization → CANCELLED( )

if utilized → ERROR( )

## UTIL→GROSS + Withdraw with UTIL

if cashflow not released → CANCELLED( )

if cashflow released → READY + Utilization( )

## Related Service:

1. Group Service 1. Forbid UTIL Settlement Method restamp
2. Utilization Service 1. Add UTIL↔GROSS Controller And Service 2. Add SettlementMethod=UTIL validator 3. Pastdue reverse handle

```
POST /v1/utilization/cashflow/settlementMethod/stamping
Req:
{   
    "trades": [
         {
            "tradeId": "123",
            "cashflowIds": ["007300894620", "007300894621"]
         },
         {
            "tradeId": "456",
            "cashflowIds": ["007300894623", "007300894624"]
         },
         {
            "tradeId": "789",
            "cashflowIds": ["007300894625", "007300894626"]
         },
         {
            "tradeId": "112",
            "cashflowIds": ["007300894627", "007300894628"]
         }     
    ],
	"settlementMethod": "GROSS|UTIL",
    "comment": ""
}

Resp:
 [
        {
          "tradeId": "123",
          "cashflowIds": ["007300894620", "007300894621"],
          "success": true, 
          "errorMessage": "" 
       },
       {
          "tradeId": "456",
          "cashflowIds": ["007300894623", "007300894624"] 
          "success": true,
	      "errorMessage": "" 
       },
        {
          "tradeId": "789",
          "cashflowIds": ["007300894625", "007300894626"]  
          "success": false,
	      "errorMessage": "Action not allowed." 
       } ,
        {
          "tradeId": "112",
          "cashflowIds": ["007300894627", "007300894628"]  
          "success": false,
	      "errorMessage": "Action not allowed." 
       } 
]
```