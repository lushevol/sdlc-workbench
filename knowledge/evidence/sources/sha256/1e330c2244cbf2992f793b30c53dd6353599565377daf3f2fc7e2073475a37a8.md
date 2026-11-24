##

## 1.Mock cashflow message

This page is to guide you how to mock a cashflow testing data .

1.Click the link [Topics | akhq.io](http://uklvadapp1340.uk.dev.net:9090/ui/uat-2/topic?search=group&topicListView=HIDE_INTERNAL&page=1).

2.Select the corresponding enviroment on the left as you want, we can select dev ,uat1,uat2 and others.

![image-2025-6-8_10-13-24-1.png](attachments/image-2025-6-8_10-13-24-1.png)

3.Input the topic name in the search box ,here we input "Cash_Settlement_Group_Message_Inbound" as an example. We can find the searching result on the top .

![image-2025-6-8_10-19-4.png](attachments/image-2025-6-8_10-19-4.png)

4.Double click the topic of "Cash_Settlement_Group_Message_Inbound" , there are many messages in the list .

![image-2025-6-8_10-22-17.png](attachments/image-2025-6-8_10-22-17.png)

5.Click one of them ,the message detail will be there .Copy the whole message.

![image-2025-6-8_10-23-56.png](attachments/image-2025-6-8_10-23-56.png)

6.Open the notepad++ and paste the message, then modify the "trackingId" and "cashflowId" with a new different value to avoid duplicated records.

**Note:Please remember the new value of the "cashflowId" because we need to search it on the FMO Post Trade Portal.**

![image-2025-6-8_10-27-49.png](attachments/image-2025-6-8_10-27-49.png)

![image-2025-6-8_10-28-54.png](attachments/image-2025-6-8_10-28-54.png)

7.Copy the message in the Notepad++ and click the "Produce to topic " button in the right bottom.

![image-2025-6-8_10-32-6.png](attachments/image-2025-6-8_10-32-6.png)

8.Paste the modified message in the red box below and click "Produce" button

![image-2025-6-8_10-34-4.png](attachments/image-2025-6-8_10-34-4.png)

9.There is a popup message on the right top means the cashflow message produce successfully.

![image-2025-6-8_10-35-55.png](attachments/image-2025-6-8_10-35-55.png)

10.Login in the FMO Post Trade Portal ,input the cashflowId with the new value,then  we can find a new cashflow with the new cashflowId we created .

![image-2025-6-8_10-42-56.png](attachments/image-2025-6-8_10-42-56.png)

## 2.Mock trade message from BCS

1.Open [Sabre Trade Admin Tool Overview - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/Sabre+Trade+Admin+Tool+Overview) link ,and a select a testing env

2.Click UAT link as an example, refer to below screenshot,choose Replay,select "BCS" from Source System

Paste message sample in the Input box,please  don't forget to modify "tradeId" and "trackingId" ,then click "SUMBIT" button

![image-2025-6-12_16-20-52.png](attachments/image-2025-6-12_16-20-52.png)

3.Will get transformed result in result box, if we can see this result ,means the trade booked successed, then we can search the cashflow via searching "tradeId"

![image-2025-6-13_8-56-1.png](attachments/image-2025-6-13_8-56-1.png)

4.Search "tradeId" in FMO Post Trade Portal -Cashflow Blotter[FX&Equity].

**Note:Please add 'BCS_' in prefix the trade , **we can find the new cashflow in Cashflow Blotter[FX&Equity].

![image-2025-6-13_13-56-12.png](attachments/image-2025-6-13_13-56-12.png)

## 3.Mock trade confirmation status message from CDU

1.Get message samples from CDU, modify the below fields in the messagepayload

"legalEntityFmId": "new value from cashflow",

"counterpartFmId": "new value from cashflow",

"tradeId": "new value from cashflow",

"tradeVersion": "new value from cashflow",

2.Open Kafka and find topic of  "CDU_Trade_Confirmation_Process_In" , produce CDU trade event message

Related kafka topic：( 第一个收trade，第二个收conf status，第三个发event)

TDS3_Trade_Message_Process_In: Receive Trade

CDU_Trade_Confirmation_Process_In:Receive confirmation status

Trade_Service_Trade_Events:Publish event