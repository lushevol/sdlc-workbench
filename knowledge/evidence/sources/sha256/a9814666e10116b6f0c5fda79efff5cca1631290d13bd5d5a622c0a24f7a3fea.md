# Uber Filter logic

1. Ratan will process Uber message for Entity.Booking_Entity_SCI_FMID in (“400007847”, “401036553”, “400991880”) on March. 28th.
2. Uber will carry additional block, RATAN will validate if the value is true, otherwise RATAN will drop the particular uber message.
{
"TDS3Data": {
"tradeRecord": {
...
},
"cashflowCheckResult": {
"passed": true # true , false
}
}

1. TDSX confirmed that for Mar.28th release they will only check cashflow validation flag for EG, NP, SA(Entity.Booking_Entity_SCI_FMID in (“400007847”, “401036553”, “400991880”)), and others will hardcode value as “true”, which means they need additional configuration change before we go-live for all other entities.

# Integration Test case

| Case # | Scenario | Test Data | Test Result | Screenshot |
| --- | --- | --- | --- | --- |
| 1 | FMID not in target FMID list, Validation result should default to ValidationPassed = true | Trade ID: 7467972524 FMID: 400899993 | Pass | Not filtered by MB, the testing env is open for all entities, so the message will be accepted. But payments are all SUSPENDED status and already processed by RATAN. So we can treat it as Pass directly. The prove of MB filter will be covered by @Yonghua Li |
| 2 | FMID in target FMID list. Cashflow is incomplete. ValidationPassed = false | Trade ID: 7418067031 FMID: 400007847 Cashflow ID: 017418067032 | Pass | ![image-2026-3-11_22-34-33.png](attachments/image-2026-3-11_22-34-33.png) |
| 3 | FMID in target FMID. Cashflow is complete. ValidationPassed = true | Trade ID: 7418067031 FMID: 400007847 Cashflow ID: 017418067032; 017418067033 | Pass | ![image-2026-3-11_22-35-51.png](attachments/image-2026-3-11_22-35-51.png) ![image-2026-3-11_22-44-9.png](attachments/image-2026-3-11_22-44-9.png) |