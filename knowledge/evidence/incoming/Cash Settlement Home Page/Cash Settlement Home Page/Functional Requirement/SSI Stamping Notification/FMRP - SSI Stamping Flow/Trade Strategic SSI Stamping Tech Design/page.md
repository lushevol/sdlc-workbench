API reference: **[Attachments - Trade SSI Stamping - Product templates - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpageattachments.action?pageId=2599261958&metadataLink=true)**

# Stamping flow

Notes:

It's expected to hit graphql query by design. Generally, CDU uses their latest trade snapshot for ssi stamping, which should also be found in graphql api with same tradeId and major version.

We'll build graphql request from requested fields, by re-creating the structure:

```groovy
{
  trades(filter: [], searchFilter: "Trade_Id = '6648567050' and Trade_Lake_Trade_Major_Version=1", page: 0, size: 1) {
    results {
Entity {
  Booking_Entity_SCI_FMID
  Counterparty_SCI_FMID
}
Trade_Lake_Trade_Major_Version
Trade_Lake_Trade_Minor_Version
Swap_Instrument {
  IR_Leg {
    First_Leg {
      Notional_Amount_Currency
      Payer_Party_Reference
    }
  }
}
Instrument_Common {
  Financial_Instrument_Code
}
Trade_Id
Settlement_Method

    }
  }
}
```

So only requested trade fields will be populated. If we fallback to historical query, then we'll query all trade fields.