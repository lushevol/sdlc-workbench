# Agenda

- The background and logic to populate field 20 for Murex 2.11 derivative products
- The logic to generate swift block 1 in Murex 2.11
- The auto split function in Murex 2.11
- Settlement business exception scenarios (e.g. missing SSI)

# MOM

- Field 20 explanation - Format in Murex 2.11 is: MX+00+BRANCH+10 DIGIT+A OR B - These name conversions are set long time ago, CN ops are not aware of detail - Prefix is to be defined in FMRP like FX in Razor, need to engage with CMO to check if there's any routing logic with the prefix - Can check with CMO on the last character A or B. - To reuse the Murex 2.11 logic or not, keep this as open questions with Srini
- Bock 1 generation process: - There're trades booked with agency profile & portfolio, but no payment generated in the China agent queued & no swift generated on the agency profile - Current logic is using the portfolio to identify these payments. - No settlement accounting generated on these portfolios. - Field 72 has the indicator telling us it's agency payment. - No live case test yet in prod, but need to implement the same logic to cater to the future requirement. - Cang, Yuanyuan <Yuanyuan.Cang@[sc.com](http://sc.com)> is the SPOC from front office, can check the booking requirement with her.
- Auto Split function in Murex 2.11 - In Razor BAU there's auto split function if the payment exceeding the pre-defined threshold, applicable for particular countries & currencies - the Razor threshold static data defined on currency level - In Razor swift generation, the post splitted payment would have the linkage to the parent payments in field 72. - There's no auto split requirement in Murex 2.11 derivative, it's product related. - For Murex 2.11 derivative products, manual split from Opics as per client's request. There's no linkage between the original payments & splitted payments.
- Business exceptions for Murex 2.11 CN derivative products - Missing Vostro & Nostro is the main business exceptions. - There're some portfolios(P2P) won't generate trade/settlement accounting. The exception is just happening in pre-trade process not reflected in payment queue. - Next Action: Check with Divya for these exceptions she mentioned
- Trade/Payment volume for Murex 2.11 derivative products & Countries: - CN 150 as NSTP daily

**Next Actions:**

- Check with CMO for the Field 20 format: The 'MX' prefix and the ending 'A'/'B'/'C'.
- To check with Cang, Yuanyuan <Yuanyuan.Cang@[sc.com](http://sc.com)> for the booking model of agency booking model. - @Arockia Dinesh
- To check with Srinivas/Asther if implement the field 20 logic related to agency booking. - @Arockia Dinesh
- To check with Srinivas/Asther if auto split is out of scope for FMRP CN Settlement. - @Arockia Dinesh
- Check the 'Reasons' field from Murex 2.11 payment queues. - @Yi Li