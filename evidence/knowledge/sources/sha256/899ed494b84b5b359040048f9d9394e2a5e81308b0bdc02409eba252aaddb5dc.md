###

### 1、5000 cashflow netting

time cost: 1.9min

![image-2025-7-1_13-14-33.png](attachments/image-2025-7-1_13-14-33.png)

Resultant Cashflow:

![image-2025-7-1_13-16-10.png](attachments/image-2025-7-1_13-16-10.png)

Move cashflowN00000013565 to TechFailed because of Either booking entity or counterparty fmcode is missing

Resultant Cashflow Event：

![image-2025-7-1_13-18-14.png](attachments/image-2025-7-1_13-18-14.png)

3 of 5000 component Cashflow Event:

![image-2025-7-1_13-24-13.png](attachments/image-2025-7-1_13-24-13.png)

### 2、1994 cashflow netting

time cost: 47.3s

![image-2025-7-1_13-48-48.png](attachments/image-2025-7-1_13-48-48.png)

Resultant Cashflow:

![image-2025-7-1_13-52-35.png](attachments/image-2025-7-1_13-52-35.png)

Resultant Cashflow Event:

![image-2025-7-1_13-54-13.png](attachments/image-2025-7-1_13-54-13.png)

3 of 1994 component Cashflow Events:

![image-2025-7-1_13-56-0.png](attachments/image-2025-7-1_13-56-0.png)

### 3、retry on duplicate UNIQE index

test cashflowId：M01750766262,M01750767483

test interface:

```
curl --location 'localhost:8991/v2/ratan/lifecycle/update/status/batch/transactional' \
--header 'Content-Type: application/json' \
--data '{
    "lifecycleRequests": [
        {
            "cashflowId": "M01750766262",
            "businessVersion": "0",
            "minorVersion": "23",
            "ratanAction": "Comment",
            "nettingId": "10000023",
            "comment": "wufengke"
        },
        {
            "cashflowId": "M01750767483",
            "businessVersion": "0",
            "minorVersion": "23",
            "ratanAction": "Comment",
            "nettingId": "10000023",
            "comment": "wufengke"
        }
    ]
}'
```

Debug mode:

hold before db execute

![image-2025-7-2_9-3-4.png](attachments/image-2025-7-2_9-3-4.png)

update M01750767483 to 26 in db client  before program execute

![image-2025-7-2_9-5-31.png](attachments/image-2025-7-2_9-5-31.png)

continue debug,the duplicate one failed only return one saved domain event.

![image-2025-7-2_9-6-14.png](attachments/image-2025-7-2_9-6-14.png)

program trigger retry, and revision update to 27 finally

![image-2025-7-2_9-7-45.png](attachments/image-2025-7-2_9-7-45.png)

retry success

![image-2025-7-2_9-8-29.png](attachments/image-2025-7-2_9-8-29.png)