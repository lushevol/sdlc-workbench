# Background

vd will highly impact the response time, query with limited vd will optimize the response time times.

## Evidence

Time Range: From 2025-04-01 to now

![image-2025-6-5_17-26-19.png](attachments/image-2025-6-5_17-26-19.png)

# Proposal

We recommend to add VD as default query criteria for all search triggered by users.

When user search non-id relevant cashflow data from cashflow blotter, UI will check if query criteria contains VD, if not, will automatically add VD=Today as additional query criteria in Quick Filter.

VD range within 1 month will get the best performance, so we restrict the vd range to less than 1 month.

# Principles

The following principles are set up for better performance when query

1. If query criteria contains id like fields, like cashflow id, trade id, netting id, etc, then the same as production behaviours.
2. If user trigger search from quick search, advanced search or quick filter without id like fields, if they don't set "value date", then put value date = today as default.
3. If user search criteria contains value date and total range more than 1 month, then pop up an alert to show warning and prevent searching untill the range is acceptable.
4. User can remove the value date criteria manually. If so, give a warning.

# Cases

| Category | User Actions | Final Triggered Search Criteria | Mockup Screenshot |
| --- | --- | --- | --- |
| Search criteria contains id like fields, e.g. cashflow id, trade id, original trade id, netting id, etc. | - User search cashflow id in quick search - User search trade id in custom search | - Cashflow.Cashflow_Id = "M01749108487" - Trade.Trade_Id = "xxx" | No Impact, same like before. |
| Search criteria contains non-id like fields. | User search Taxonomy and Booking Entities in quick search. | Taxonomy = "ForeignExchange:Forward" and Booking Entity = "SCB SHANGH*SHA" and VD = TODAY | ![image-2025-6-5_16-45-47.png](attachments/image-2025-6-5_16-45-47.png) |
| User search Taxonomy and Booking Entities with temporary filter in custom search. | Taxonomy = "ForeignExchange:Forward" and Booking Entity = "SCB SHANGH*SHA" and VD = TODAY | ![image-2025-6-5_16-52-51.png](attachments/image-2025-6-5_16-52-51.png) |
| User search Taxonomy and Booking Entities with saved filter in custom search. | Taxonomy = "ForeignExchange:Forward" and Booking Entity = "SCB SHANGH*SHA" and VD = TODAY | ![image-2025-6-5_16-56-5.png](attachments/image-2025-6-5_16-56-5.png) ![image-2025-6-5_16-56-32.png](attachments/image-2025-6-5_16-56-32.png) |
| User search Taxonomy and Booking Entities in quick filter. | Taxonomy = "ForeignExchange:Forward" and Booking Entity = "SCB SHANGH*SHA" and VD = TODAY | ![image-2025-6-5_16-58-15.png](attachments/image-2025-6-5_16-58-15.png) |
| Mixed search criteria contains non-id like fields. | User search Taxonomy in quick search and search Entities in quick filter. | Taxonomy = "ForeignExchange:Forward" and Booking Entity = "SCB SHANGH*SHA" and VD = TODAY | ![image-2025-6-5_17-1-22.png](attachments/image-2025-6-5_17-1-22.png) |
| Cancel VD criteria manually | User can manually remove VD criteria after auto set up. | Taxonomy = "ForeignExchange:Forward" and Booking Entity = "SCB SHANGH*SHA" | ![image-2025-6-16_11-0-23.png](attachments/image-2025-6-16_11-0-23.png) |
| VD range more than 1 month | User search Taxonomy, Entities in quick search. Set VD range from "2025-06-01" to "2025-07-02". | NOT SEARCHED | ![image-2025-6-16_11-2-28.png](attachments/image-2025-6-16_11-2-28.png) |
| User in Advanced Search. Set VD range from "2025-06-01" to "2025-07-02". | NOT SEARCHED | ![image-2025-6-19_22-43-11.png](attachments/image-2025-6-19_22-43-11.png) |

# Proposal B

1. Using pg extension to support hint: pg_hint_plan [https://github.com/ossc-db/pg_hint_plan](https://github.com/ossc-db/pg_hint_plan)

![1.png](attachments/1.png)