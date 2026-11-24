# Scene 1

Send the Uber messages from FMRP1 to UAT4 in completely reverse order; that is, FMRP1 consumes messages in majorVersion2->5 order, and UAT4 consumes messages in majorVersion5->2 order.

tradeId: 8000606638

result:  pass

fmrp1 major_version details:

![image-2026-6-8_14-9-8.png](attachments/image-2026-6-8_14-9-8.png)

| | fmrp1 | uat4 | remark |
| --- | --- | --- | --- |
| group status | ![image-2026-6-5_16-31-30.png](attachments/image-2026-6-5_16-31-30.png) | ![image-2026-6-5_16-31-59.png](attachments/image-2026-6-5_16-31-59.png) | |
| group message status | ![image-2026-6-5_16-33-33.png](attachments/image-2026-6-5_16-33-33.png) | ![image-2026-6-5_16-33-52.png](attachments/image-2026-6-5_16-33-52.png) | |
| lifecycle final status | ![image-2026-6-5_16-35-11.png](attachments/image-2026-6-5_16-35-11.png) | ![image-2026-6-5_16-34-36.png](attachments/image-2026-6-5_16-34-36.png) | If the New event arrives first, the status will continue to progress, but if the Withdrawal event arrives first, it will immediately result in an ERROR. |
| lifecycle status details | ![image-2026-6-5_16-36-16.png](attachments/image-2026-6-5_16-36-16.png) | ![image-2026-6-5_16-36-37.png](attachments/image-2026-6-5_16-36-37.png) | |

# Scene 2

Send the Uber messages from FMRP1 to UAT4 in completely disorder order; that is, FMRP1 consumes messages in major version 1->3 order, and UAT4 consumes messages in major version 3->1->2 order.

tradeId: 8010059425

result:  pass

fmrp1 major_version details:

📎 [8010059425_cashflow_summary.xlsx](attachments/8010059425_cashflow_summary.xlsx)

| | fmrp1 | uat4 | remark |
| --- | --- | --- | --- |
| group status | ![image-2026-6-8_13-30-16.png](attachments/image-2026-6-8_13-30-16.png) | ![image-2026-6-8_13-26-34.png](attachments/image-2026-6-8_13-26-34.png) | |
| group message status | ![image-2026-6-8_13-30-57.png](attachments/image-2026-6-8_13-30-57.png) | ![image-2026-6-8_13-27-18.png](attachments/image-2026-6-8_13-27-18.png) | |
| lifecycle final status | ![image-2026-6-8_13-31-45.png](attachments/image-2026-6-8_13-31-45.png) | ![image-2026-6-8_13-27-58.png](attachments/image-2026-6-8_13-27-58.png) | |

# Scene 3

Send the Uber messages from FMRP1 to UAT4 in completely disorder order; that is, FMRP1 consumes messages in major version 1->3 order, and UAT4 consumes messages in major version 2->1->3 order.

tradeId: 8004668433, cashflowId: 008036000372

result:   pass

fmrp1 major_version details:

📎 [8004668433_cashflow_summary.xlsx](attachments/8004668433_cashflow_summary.xlsx)

| | fmrp1 | uat4 | remark |
| --- | --- | --- | --- |
| group status | ![image-2026-6-8_16-15-42.png](attachments/image-2026-6-8_16-15-42.png) | ![image-2026-6-8_16-19-9.png](attachments/image-2026-6-8_16-19-9.png) | |
| lifecycle final status | ![image-2026-6-8_16-16-21.png](attachments/image-2026-6-8_16-16-21.png) | ![image-2026-6-8_16-20-24.png](attachments/image-2026-6-8_16-20-24.png) | When the withdrawal message arrives first, all cashflows status is ERROR ![image-2026-6-8_16-17-54.png](attachments/image-2026-6-8_16-17-54.png) |