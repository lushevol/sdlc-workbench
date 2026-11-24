## Background

[Cash Settlement - Accounting - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+-+Accounting)

## High level design

[RATANONE Cash Settlement Technical Design - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2560471970)

## Principle

1. Event driven EBBS feed generation
2. Value date is the cutoff for feed publishing 1. Hold if VD not arrived 2. Publish directly if VD already arrived 3. Retry max to 3 times on validate error codes
3. Withdrawal will be generated as reversal direction of the New instead of totally new generated feed

## Status Machine

## Detailed level Design

*Note：

1. Reinstate on Reversal. For reversal flag, it has 2 possible values: 1. Status changed from FAILED, then reinstate action, On this reinstate action message, it will have reversal tag= reinstate 2. Status changed from SWIFT_SUPPRESSED, then approve action on unsuppressed, On this approve action message, it will have reversal tag=SwiftUnSuppressed 3. This filter includes reversal flag=reinstate & last published balance<0

SOD job statistics

| Condition | Task Sum | Cost | |
| --- | --- | --- | --- |
| Just publish | 4002 | 40.2s | ![publish start.jpg](attachments/publish start.jpg) ![publish end.jpg](attachments/publish end.jpg) |
| Generate JSON and publish | 4000 | 40.7s | ![gen start.jpg](attachments/gen start.jpg) ![gen end.jpg](attachments/gen end.jpg) |

new version for UK