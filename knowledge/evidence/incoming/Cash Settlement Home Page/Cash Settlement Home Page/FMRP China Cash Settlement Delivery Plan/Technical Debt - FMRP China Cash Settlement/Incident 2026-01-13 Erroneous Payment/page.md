# **Event List**

| **Event Time** | **M00123425789(Receipt)** | **M00124791186(****Payment****)** | **N00000202445(****Netting resultant cashflow****)** |
| --- | --- | --- | --- |
| 1/2/2026 0:52:14 | Cashflow reached to RATAN in ‘PROJECTED’ status | | |
| 1/6/2026 2:02:18 | System automatically materialized the cashflow and moved to ‘READY’ status without any NSTP exceptions, wating for cutoff to auto release | | |
| 1/8/2026 10:20:14 | | Cashflow reached to RATAN and captured by NSTP rule with Exceptions:** Pending Affirmation** and **High Value** | |
| 1/9/2026 6:45:54 | | Trade confirmed and the underlying payments’ exceptions in RATAN auto closed. The payment moved to ‘READY’ status and wating for cutoff to auto release | |
| 1/12/2026 11:00:00 | Cutoff reached, no swift generated after check the ‘Notice to receive’ | Cutoff reached, swift generated and sent to FM swift gateway | |
| 1/12/2026 11:00:34 | User(1597657 -Lew, Chian Lih) performed manual netting (**M00123425789 M00124791186 ) **post release cutoff, N00000202445 was generated and catch by NSTP rule with exceptions: **Net Cashflow** and **Ad hoc Netting** |
| 1/12/2026 11:03:02 | | | Maker(1597657 -Lew, Chian Lih) submit |
| 1/13/2026 1:19:10 | | | Checker(1589184-Wong, Siew Peng) Approve |
| 1/13/2026 1:19:11 | | | Released to FM swift gateway as release cutoff past |

# **Alert on the release cutoff past**

![image-2026-1-15_12-16-1.png](attachments/image-2026-1-15_12-16-1.png)

# **Detailed cashflow audit history**

![image-2026-1-15_12-10-2.png](attachments/image-2026-1-15_12-10-2.png)![image-2026-1-15_12-9-2.png](attachments/image-2026-1-15_12-9-2.png)![image-2026-1-15_12-11-2.png](attachments/image-2026-1-15_12-11-2.png)