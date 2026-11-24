# Motivation

Creating testing data of cashflow is always necessary for our daily development and testing, but it's not easy:

- You need to understand the basics of cashflow data structure,
- You need a correct template of existing cashflow, and you know exactly the fields that you should modify
- You need to know where you should put the data

Even for experienced developers, creating mock data is boring and boilerplate. I created a tool to generate Murex cashflow when testing trade SSI stamping:

![image-2025-7-25_16-33-47.png](attachments/image-2025-7-25_16-33-47.png)

However it's client based and not friendly to share to others. As we've the requirement to create mock cashflows to supporting testing, so we decided to create a web-based mock up tool as a successor.

# Getting started

You can access <u>[RATAN Cashflow Mock Test Tool](http://10.198.199.160:3001/)</u> to create cashflow.

## Generate cashflows

> **INFO**
> Only UAT1 is supported currently. Make sure to use cashflow ID in UAT1, and the generated data will be produced to UAT1.

### Mock Murex cashflow

The murex cashflow mockup functionality could help to generate MXML message, which is the cashflow format of Murex system. To create a new Murex cashflow, follow the bellow steps:

1. Switch to “Murex cashflow generator”
2. Load a existing cashflow by input a Murex cashflow ID and click "Load cashflow". The MXML file sent from Murex will be loaded as an template for you to modify properties. If you're not sure about what cashflow to use, just use the default cashflow.
3. Generate a new cashflow ID by clicking "Generate", a random cashflow ID will be generated. By default, the cashflow IDs will be out of order each time you generate, if you wish to generate sequential cashflow IDs, check the "Incremental" button.
4. Modify cashflow properties in the left panel. For example, you can change Currency to EUR and payment date to current date.
5. Click "Send" and if success, the cashflow will be published to RATAN.

![image-2025-7-25_17-18-51.png](attachments/image-2025-7-25_17-18-51.png)

After you send, you could search the cashflow by cashflow ID in [FMO Post Trade Portal](https://fmo-mfe.uk.dev.net:8453/):

> **INFO**
> For Murex cashflow, RATAN will automatically append M00 to cashflow ID. For example, if you generated cashflow ID is "R60725828" , you need to search with "M00R60725828", which is also displayed bellow the cashflow ID.

![image-2025-7-25_17-20-39.png](attachments/image-2025-7-25_17-20-39.png)

### Mock Stella cashflow

Mocking Stella cashflow has exactly same steps with Murex one. Please refer to "Mock Murex cashflow“ chapter, and make sure to input existing cashlow from Stella, eg. "005566581627".

![image-2025-7-28_11-21-45.png](attachments/image-2025-7-28_11-21-45.png)

### Manual send

The mockup tool is simple and straightforward, but it could not fulfill all testing scenarios. The last option is to modify the cashflows manually, and use "Manual send" feature to publish it. You could:

1. Load cashflows from Murex or Stella, and copy the content. You could modify available fields first in left panel.
2. Manually edit anything you want in an editor, eg. Vscode or Notepad++
3. Open "Manual Send" tab, paste and send the content

![image-2025-7-28_11-27-3.png](attachments/image-2025-7-28_11-27-3.png)

The tool will automatically detect the content and determine it's SCBML or MXML and send to correspondent topic.

![image-2025-7-28_11-30-40.png](attachments/image-2025-7-28_11-30-40.png)

## How it works

RATAN is integrated with Stella and Murex with messages, each system has a dedicated topic. The mockup tool generates message and publish to those topics, works similar with real Murex or Stella. The basic process could be illustrated as bellow diagram:

Be aware that this mockup tool is not able to understand business requirements and generate cashflows as a real system, it just modify an existing message with find-replace pattern instead.

# Developer's guide & Trouble shotting

## Developer's guide

Source code of this mockup tool could be found in bellow repositories:

- Frontend UI: React based web app <u>[51358-ratan-test-helper-ui - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-test-helper-ui)</u>
- Backend: Springboot app <u>[51358-ratan-test-helper-api - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-test-helper-api)</u>

## Known issues

This mockup tool is developed with minimal effort, there're some know issues:

- Murex batch cashflows are not supported
- Withdraw cashflows are not supported

However, you're still able to modify the cashflow files manually and use "Manual send" option.

## FAQ

### I cannot open the mock up tool, what happened?

The mockup tool is deployed in dev server manually, and it's not guaranteed to be stable. If you cannot open the page, please try to start it:

SSH into 10.198.199.160

The application binaries are located in /apps/ratanrt/quill-shared:

![image-2025-7-28_11-17-39.png](attachments/image-2025-7-28_11-17-39.png)

### I've sent the cashflow successfully, but I cannot find it in cashflow blotter, how can I diagnose it?

There's complex workflow for cashflow processing, so it might happen that you cannot find the cashflows due to:

- Cashflow does not flow into RATAN
- Cashflow is ignored by some rules or validation

You can use the following steps to diagnose it:

1. Make sure you're using a correct payment date.
2. Check if the cashflow has been sent to group service, open group blotter and confirm if it could be found:

![image-2025-7-28_9-28-58.png](attachments/image-2025-7-28_9-28-58.png)

If you could see it in group blotter, then it means that the cashflow has been successfully sent and processed, it might be some data issue that the cashflow got ignored in RATAN.

Otherwise if you cannot see it in group blotter, then there might be an issue between mockup tool and Kafka, you should check if the cashflow is in Kafka:

- For Murex cashflows, check <u>[Cash_Settlement_Mxg_Inbound](http://10.198.199.160:9090/ui/uat-1/topic/Cash_Settlement_Mxg_Inbound/data?sort=Oldest&partition=All)</u>
- For Stella cashflows, check <u>[Cash_Settlement_Group_Message_Inbound](http://10.198.199.160:9090/ui/uat-1/topic/Cash_Settlement_Group_Message_Inbound/data?sort=Oldest&partition=All)</u>

You can search message by value that contains the cashflow ID:

# ![image-2025-7-28_10-47-27.png](attachments/image-2025-7-28_10-47-27.png)

If you still have issue with your cashflow, you may take a look at the logs and try to find the reason: Discover - Elastic

![image-2025-7-28_11-10-18.png](attachments/image-2025-7-28_11-10-18.png)

In above case, the cashflow is not forwarded by group service and remains pending because the the SCBML has a batch size of 2, the group service will not send it until the other cashflow arrives. To solve this issue, you should load a cashflow that only contains batch size 1.

![image-2025-7-28_11-11-7.png](attachments/image-2025-7-28_11-11-7.png)