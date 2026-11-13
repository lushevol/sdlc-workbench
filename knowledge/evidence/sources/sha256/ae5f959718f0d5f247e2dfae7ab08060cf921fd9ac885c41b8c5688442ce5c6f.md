**UTIL - Gross**
For Settlement method='UTIL' cashflow, and cashflow status in (WAITING, READY, PASTDUE)

1. When user right-click (Settlement Method Update) then cashflow settlement method will be set as gross and reinstate for gross settlement.
2. Update remaining amount to 0/remove pasdue as cashflow sub status .
3. For PASTDUE cashflow, post settle as gross, reversed accounting entry would be generated and sent out.
4. This action will be on cashflow level.
5. No special NSTP rule would be required for this scenario.

**Gross -UTIL**
For Settlement method in ('GROSS'."") cashflow, and cashflow status in (WAITING, READY+NA+NA) and data_source_system != Ratan and ISDA_Taxonomy in ('ForeignExchange:Forward','ForeignExchange:Spot','ForeignExchange:Swap') and event reason !='reversal'

1. When user right-click (Settlement Method Update) then cashflow settlement method will be set as Util and reinstate for util settlement.
2. Update payment amount to remaining amount.
3. Post settle as util, settlement means will be stamped per client static data setup.

**For Settlement method stamping**, condition also would be ISDA_Taxonomy in ('ForeignExchange:Forward','ForeignExchange:Spot','ForeignExchange:Swap'), then backend code would check utilization static for eligible entities FMID

If user only selected 1 cashflow in cashflow blotter, system will automatically display all cashflows under the same trade.

Limitation for bulk update is 100 trade/cashflow

Front end will order by trade ID, and filter out by cashflow status (+ERROR)                
                
Warning with condition: selected cashflow count  != feedback from frontend cashflow count                
Warning: System automatically selected all cashflow under trade T01, T02

![image-2026-4-9_18-24-3.png](attachments/image-2026-4-9_18-24-3.png)

Response:    
Response for success/failure would be on trade level