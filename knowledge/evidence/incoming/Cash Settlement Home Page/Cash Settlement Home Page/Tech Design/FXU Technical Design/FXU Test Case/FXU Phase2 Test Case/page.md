Background: This change is related to settlement method field value change with value GROSS and UTIL in bidirectional in cashflow data.

Right menu(**Settlement Method Update**) condition: 1& (2 || 3)

1. profile: RATAN_STRATEGIC_CASHFLOW_BLOTTER:F_Cashflow_Status_Change_Release
2. Settlement Method in ('GROSS','') and cashflow status in (WAITING, READY+NA+NA) and data_source_system != Ratan and ISDA_Taxonomy in ('ForeignExchange:Forward','ForeignExchange:Spot','ForeignExchange:Swap')
3. Settlement method='UTIL', and cashflow status in (WAITING, READY, PASTDUE) and data_source_system != Ratan and ISDA_Taxonomy in ('ForeignExchange:Forward','ForeignExchange:Spot','ForeignExchange:Swap')

Dialog fields includes:

- Cashflow Id
- Trade Id
- Settlement Method
- Payment Amount
- Cashflow Status
- Booking Entity
- Counterparty FMCODE
- Currency
- Pay/Receive
- Value Date

| No | Scenario | Evidence |
| --- | --- | --- |
| 1 | When cashflow satisfies update condition, will display "**Settlement Method Update**" menu | ![image-2026-4-30_13-36-14.png](attachments/image-2026-4-30_13-36-14.png) cf:007373080220,007372108581,007372675350,007372675460,007372516507,007301243277,007336027907 |
| 2 | Click Settlement Method Update menu, consistency validation 1. settlement method value not same 2. limitation for bulk update is 100 cashflow | ![image-2026-4-30_16-39-47.png](attachments/image-2026-4-30_16-39-47.png) ![image-2026-4-30_16-40-52.png](attachments/image-2026-4-30_16-40-52.png) ![image-2026-5-20_23-20-28.png](attachments/image-2026-5-20_23-20-28.png) |
| 3 | If user only selected 1 cashflow in cashflow blotter, will query all cashflows under the same trade, then will display on dialog. | cf:007372135160 trade:7150119619 ![image-2026-5-8_10-40-39.png](attachments/image-2026-5-8_10-40-39.png) |
| 4 | Warning :**System automatically selected all cashflows under trades** **condition: selected cashflow count != by trade id query cashflow count** | cf:007372135160 trade:7150119619 ![image-2026-4-30_17-2-16.png](attachments/image-2026-4-30_17-2-16.png) No warning ![image-2026-4-30_17-17-3.png](attachments/image-2026-4-30_17-17-3.png) |
| 6 | GROSS <=>"" | ![image-2026-4-30_17-29-51.png](attachments/image-2026-4-30_17-29-51.png) |
| 7 | If Trade id include not eligible update condition cashflow under, will display these not eligible cashflows on insufficient cashflow | trade:7150557500 ![image-2026-4-30_17-28-1.png](attachments/image-2026-4-30_17-28-1.png) |
| 8 | Sort by Trade Id ASC | ![image-2026-5-20_23-28-35.png](attachments/image-2026-5-20_23-28-35.png) |
| 9 | Response for success/fail would be trade level and notification | ![image-2026-5-20_23-33-34.png](attachments/image-2026-5-20_23-33-34.png) ![image-2026-5-20_23-33-51.png](attachments/image-2026-5-20_23-33-51.png) ![image-2026-5-20_23-38-24.png](attachments/image-2026-5-20_23-38-24.png) |
| | | ![image-2026-5-21_11-41-5.png](attachments/image-2026-5-21_11-41-5.png) |