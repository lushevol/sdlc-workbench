#

# Install Copilot

1. Apply for the access to github copilot, ask for LM's approve.

<u>[Onboarding Steps](https://confluence.global.standardchartered.com/display/GHCP/Onboarding+Steps)</u>

2. Login to github enterprise account  of SCB, <u>[https://github.com/enterprises/scenggcb](https://github.com/enterprises/scenggcb)</u>. **Please ensure you have get in the home page.**

![image-2025-7-4_15-18-3.png](attachments/image-2025-7-4_15-18-3.png)

**3. (IMPORTANT) set your ide proxy to "[http://gateway.zscloud.net:443](http://gateway.zscloud.net:443)"**

![image-2025-3-7_14-19-22.png](attachments/image-2025-3-7_14-19-22.png)

some staffs encountered with "Github Copilot Extension Download issue" and "Copilot is not stable issue". After use this proxy link, will be fixed.

If this proxy is not working, please try "sc-cli -get-proxy" to get a proxy url.

If you don't have sc-cli installed, please follow the guide of SCB. <u>[Getting proxy details](https://confluence.global.standardchartered.com/display/GHCP/Getting+proxy+details)/</u>

*NOTICE: Seems that this proxy not working for IntellJ. Please use <u>10.24.89.13:443</u> instead.*

4. Install Github Copilot, (Github Copilot Chat will be auto installed too)

![image-2025-3-7_14-21-0.png](attachments/image-2025-3-7_14-21-0.png)

**IntelliJ IDEA**

![image-2025-7-4_15-19-58.png](attachments/image-2025-7-4_15-19-58.png)

5. Get your account logged to IDE. (If you see <bankid>_scenggcb on the account setting, then logged successfully), **this step depends on STEP 2 login status, please make sure you are logged and staying on the dashboard.**

![image-2025-3-7_14-17-31.png](attachments/image-2025-3-7_14-17-31.png)

**IntelliJ IDEA**

**EXPAND: IntellJ Setup Steps**

1. After install CHCP extension, you will find the icon on the right bottom of IDE, click "Login to Github". Before go to the following steps, *<u>please ensure you have logged in on STEP 2</u>*.

![image-2025-7-7_13-54-51.png](attachments/image-2025-7-7_13-54-51.png)

2. Copy the device code and click "Copy and Open".

![image-2025-7-7_13-58-0.png](attachments/image-2025-7-7_13-58-0.png)

3. Login with SCB account (Not your personal account)

![image-2025-7-7_13-58-50.png](attachments/image-2025-7-7_13-58-50.png)

![image-2025-7-7_13-58-57.png](attachments/image-2025-7-7_13-58-57.png)

4. After authorization done, go back to IntelliJ IDEA, you will have the sign in successfully alert.

![image-2025-7-7_13-59-39.png](attachments/image-2025-7-7_13-59-39.png)

![image-2025-7-7_13-59-42.png](attachments/image-2025-7-7_13-59-42.png)

**EXPAND_END**

# Recommend Dependencies

<u>**It's high recommended that you install the latest supporting vs code or IntelliJ and nodejs for better experience.**</u>

## VSCode v1.99.0

install from following link,

[https://scbnow01.service-now.com/myit?id=sc_cat_item&sys_id=24ac81563bd96250e9dd5d0b16e45a43](https://scbnow01.service-now.com/myit?id=sc_cat_item&sys_id=24ac81563bd96250e9dd5d0b16e45a43)

## IntelliJ IDEA Community Edition 2024

install from following link

[https://scbnow01.service-now.com/myit?id=sc_cat_item&sys_id=51e8d2f42b602a10ad51f95fee91bf7a&table=sc_cat_item&searchTerm=IntelliJ](https://scbnow01.service-now.com/myit?id=sc_cat_item&sys_id=51e8d2f42b602a10ad51f95fee91bf7a&table=sc_cat_item&searchTerm=IntelliJ)

## Node.js v20.18.2

install from following link,

[https://scbnow01.service-now.com/myit?id=sc_cat_item&sys_id=f59f90762b80ae54b6bbffa1fe91bf09](https://scbnow01.service-now.com/myit?id=sc_cat_item&sys_id=f59f90762b80ae54b6bbffa1fe91bf09)

# Error Troubleshooting

If you have encountered errors while chat with Copilot, please follow the steps to troubleshooting,

1. Make sure you can access to <u>[https://github.com/enterprises/scenggcb](https://github.com/enterprises/scenggcb)</u> and logged in successfully.

- go to [https://github.com/settings/copilot/features](https://github.com/settings/copilot/features)
- check if Github Copilot Business is active for your account
- ![image-2025-7-22_21-6-1.png](attachments/image-2025-7-22_21-6-1.png)

2. Make sure your proxy is right (see above).

3. Make sure BOTH Github and Github Copilot Chat account is in logged-in status.

- if you can't see Chat account state, please check logs from OUTPUT,
- ![image-2025-7-2_11-36-12.png](attachments/image-2025-7-2_11-36-12.png)
- Or you can use "Github Copilot Chat Diagnostics" to check if connection is blocked.
- ![image-2025-7-9_10-51-20.png](attachments/image-2025-7-9_10-51-20.png)
- ![image-2025-7-7_14-6-32.png](attachments/image-2025-7-7_14-6-32.png)

4. Say "hi" to Copilot to test if connection back to normal.

5. mentioned by @Jeremy Li, If you encountered "Models not found" issue, please try to restart vscode or reboot your PC.

- ![](https://confluence.global.standardchartered.com/download/attachments/3266184800/image-2025-11-7_14-45-47.png?version=1&modificationDate=1762497947000&api=v2)

**If you can't fix issue from steps above, please try official solutions,**

- [GHCP Troubleshooting](https://confluence.global.standardchartered.com/display/GHCP/GHCP+Troubleshooting)
- [Known Issues](https://confluence.global.standardchartered.com/display/GHCP/Known+Issues)

Otherwise, please contact to support team from link below,

- [GHCP Community Hub](https://confluence.global.standardchartered.com/display/GHCP/GHCP+Community+Hub)

![image-2025-7-22_21-16-8.png](attachments/image-2025-7-22_21-16-8.png)

# A very useful cook book for Copilot

I learned a lot from it. Highly recommend all of you to read.

[https://docs.github.com/en/copilot](https://docs.github.com/en/copilot)

# Generate Unit Testing

Select "Generate Tests", will generate testing cases for this function.

![image-2025-3-7_14-22-7.png](attachments/image-2025-3-7_14-22-7.png)

You can specify more details on how to generate testing by submit with prompts below,

```
@workspace /tests generate unit testing code for this function, Validate both success and failure, and include edge cases, should cover all conditions.
```

Then more test cases will be generated. And you can click "Apply the Edit" to apply changes on files.

![image-2025-3-7_14-30-1.png](attachments/image-2025-3-7_14-30-1.png)

![image-2025-3-7_14-39-57.png](attachments/image-2025-3-7_14-39-57.png)

## Better Generation

For better testing code generation, please follow the principles below,

1. make a meaningful function name and input/output type definition.
2. better to write description for the function, what's expected functionality.
3. For react project, to generate accurate testing, *<u>**normal function > react hooks > react component**</u>*. So split the code into separate code blocks will be better.

# Generate Doc

![image-2025-3-26_9-39-48.png](attachments/image-2025-3-26_9-39-48.png)

# Fix Issue

![image-2025-3-26_9-40-49.png](attachments/image-2025-3-26_9-40-49.png)

# Explain Code

![image-2025-3-26_9-41-6.png](attachments/image-2025-3-26_9-41-6.png)

# Generate Commit Message

Copilot can generate commit message base on your **staged files**.

![image-2025-6-5_18-1-38.png](attachments/image-2025-6-5_18-1-38.png)

step1: go to "Source Control", stage your changes, then click the star icon on the right of message input.

![image-2025-6-5_18-2-8.png](attachments/image-2025-6-5_18-2-8.png)

step2: waiting for message generation.

![image-2025-6-5_18-2-41.png](attachments/image-2025-6-5_18-2-41.png)

step3: commit message generated base your code. **Please notice that you should manually add #WorkitemId on the top of message to make it a valid commit in current git policy.**

# Code Review

Copilot can do code review base on **all uncommitted changes**.

![image-2025-6-5_18-12-14.png](attachments/image-2025-6-5_18-12-14.png)

step1: go to "Source Control", click the dialog icon on the status bar of CHANGES.

![image-2025-6-5_18-6-48.png](attachments/image-2025-6-5_18-6-48.png)

step2: wait for code review done

![image-2025-6-5_18-10-35.png](attachments/image-2025-6-5_18-10-35.png)

![image-2025-6-5_18-14-46.png](attachments/image-2025-6-5_18-14-46.png)

step3: go though code review suggestions. Apply or discard depends on your choice.

# Commander Line

You can generate commander lines in VSCode.

step1. click on shell commander line

step2. press ctrl+i, it will show a widget for you to type the request.

![image-2025-7-23_9-44-48.png](attachments/image-2025-7-23_9-44-48.png)

step3. press enter to generate the commander.

![image-2025-7-23_9-45-46.png](attachments/image-2025-7-23_9-45-46.png)

step4. press "Run" to execute the commander.