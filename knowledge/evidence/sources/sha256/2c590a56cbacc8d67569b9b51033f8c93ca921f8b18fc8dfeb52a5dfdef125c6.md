# Background

Razor will write back to Ratan on below message/status:

1. ACK/NACK
2. RELEASED
3. SETTLED

Ratan need to update cashflow status and sync back to STELLA or Murex2.11

# Process Flow

# Integration

## Ratan → Adaptor

```
//For netted cashflows, all component cashflows will be updated by a batch
{
    "Cashflow__Cashflow_State": "RELEASED", //RELEASED or SETTLED
	"Cashflow__Netting_Id": "100000001", //Nullable
    "Cashflow__Cashflow_Id": [
        "M00087755146","M00087755147","M00087755148"
    ]
}

//For gross cashflow, only one cashflow will be updated
{
    "Cashflow__Cashflow_State": "RELEASED", //RELEASED or SETTLED
	"Cashflow__Netting_Id": "", //Nullable
    "Cashflow__Cashflow_Id": [
        "M00087755146"
    ]
}
```

## Adaptor → Murex

Section 2 in page: [CN Settlement - Murex2.11 Technical Design - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/CN+Settlement+-+Murex2.11+Technical+Design)