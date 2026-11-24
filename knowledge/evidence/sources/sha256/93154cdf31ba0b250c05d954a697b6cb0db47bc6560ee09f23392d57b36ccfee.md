1.  API Endpoint (new)

POST   /v1/profileLimitation/checkLimitationsBatch

2. Request:

Request Body

{
  "items": [
    {
      "referenceId": "MD100",
      "currency": "USD",
      "amount": 9999
    },
    {
      "referenceId": "MD101",
      "currency": "CNY",
      "amount": 4000
    },
    {
      "referenceId": "MD102",
      "currency": "EPT",
      "amount": 8888
    }
  ]
}

| Field | | Type | Required | Description |
| --- | --- | --- | --- | --- |
| items | | List | Yes | List of check items |
| | referenceId | String | Yes | cashflowId |
| | currency | String | Yes | Currency code |
| | amount | BigDecimal | Yes | Amount to check |

3.  Response:

{
    "results": [
        {
            "referenceId": "MD100",
            "currency": "USD",
            "amount": 9999,
            "success": false,
            "reason": "cannot get limitation for profile: USER_A, currency: USD"
        },
        {
            "referenceId": "MD101",
            "currency": "CNY",
            "amount": 4000,
            "success": true,
            "reason": ""
        },
        {
            "referenceId": "MD102",
            "currency": "EPT",
            "amount": 8888,
            "success": true,
            "reason": ""
        }
    ],
    "success": true,
    "reason": ""
}

or

when params is null  , success filed return false

{
    "results": null,
    "success": false,
    "reason": "Request items cannot be empty"
}

| Field | | Type | Description |
| --- | --- | --- | --- |
| results | | List | List of check results |
| | referenceId | String | cashflowId |
| | currency | String | Currency code |
| | amount | BigDecimal | Amount to check |
| | success | Boolean | Whether check is passed |
| | reason | String | Failure reason (if any) |
| success | | Boolean | Whether check is passed |
| reason | | String | Failure reason (if any) |

4. Example

Request:

POST /v1/profileLimitation/checkLimitationsBatch
Content-Type: application/json

{
  "items": [
    {
      "cashflowId": "MD100",
      "currency": "USD",
      "amount": 9999
    },
    {
      "cashflowId": "MD101",
      "currency": "CNY",
      "amount": 4000
    },
    {
      "cashflowId": "MD102",
      "currency": "EPT",
      "amount": 8888
    }
  ]
}

Response:

{
    "results": [
        {
            "cashflowId": "MD100",
            "currency": "USD",
            "amount": 9999,
            "success": false,
            "reason": "cannot get limitation for profile: USER_A, currency: USD"
        },
        {
            "cashflowId": "MD101",
            "currency": "CNY",
            "amount": 4000,
            "success": true,
            "reason": ""
        },
        {
            "cashflowId": "MD102",
            "currency": "EPT",
            "amount": 8888,
            "success": true,
            "reason": ""
        }
    ],
    "success": true,
    "reason": ""
}