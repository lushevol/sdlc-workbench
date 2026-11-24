- [2024-04-24 CN Retrospective](https://confluence.global.standardchartered.com/display/DSP/2024-04-24+CN+Retrospective)
- [2024-05-08 CN Retrospective](https://confluence.global.standardchartered.com/display/DSP/2024-05-08+CN+Retrospective)
- [2024-05-22 CN Retrospective](https://confluence.global.standardchartered.com/display/DSP/2024-05-22+CN+Retrospective)
- [2024-06-05 CN Retrospective](https://confluence.global.standardchartered.com/display/DSP/2024-06-05+CN+Retrospective)
- [2024-06-19 CN Retrospective](https://confluence.global.standardchartered.com/display/DSP/2024-06-19+CN+Retrospective)
- [2024-07-03 CN Retrospective](https://confluence.global.standardchartered.com/display/DSP/2024-07-03+CN+Retrospective)
- [2024-07-18 CN Retrospective](https://confluence.global.standardchartered.com/display/DSP/2024-07-18+CN+Retrospective)
- [2025-01-09 Cash Settlement Post UBER Retrospective](https://confluence.global.standardchartered.com/display/DSP/2025-01-09+Cash+Settlement+Post+UBER+Retrospective)
: Waiting for discussing in future retro meeting
2. : Gone through and discussed in meeting

3. : Need more discussion on it.

4. : Review the discussed item after 1 month and confirm the issue has fixed.

| No, | Title | Status | Go-through Date | Go-through Link | Follow-up Date | Action owner | Raised by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Adhoc task without clearly requirements and only been informed by DL(Delivery Lead) or BA in word, and no related story been created. QA also confused after the dev created task directly and Dev cannot give the business background and critical level for the task which needs QA to double confirm with DL | | 2024-04-24 | [2024-04-24 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-04-24+CN+Retrospective) | 2024-05-22 2024-06-19 | | @Xinmiao Huang |
| 2 | 1. CR go-live too frequently and sometimes we do a fix, but PO and user have no idea on what we fixed, why we fix these, and have we fixed what issue they really care about. 2. CR size to small or too large | | 2024-04-24 | [2024-04-24 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-04-24+CN+Retrospective) | 2024-06-19 | | @Zeyu Zhou |
| 3 | The ownership of **API** Performance Test is not clearly. Currently, Dev owns the performance test not QA | | 2024-05-08 | [2024-05-08 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-05-08+CN+Retrospective) | 2024-09-11 | @Shimeng Ma | @Guiling Wang |
| 4 | No regular code review from team level | | 2024-05-08 | [2024-05-08 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-05-08+CN+Retrospective) | | | @Xinmiao Huang |
| 5 | 1. ~~FE internal dependency management not so clear.~~ 2. FE e2e testing is not enough. 3. ownership of FE e2e not clear | | 2024-05-08 | [2024-05-08 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-05-08+CN+Retrospective) | | | @Shuai Lu |
| | 1. No version or tag on front to back API . (swag) (need openapi doc) | | 2024-05-08 | | 2024-09-11 | @Ruiheng Cao (need openapi doc) | @Shuai Lu |
| 6 | Deploy to uat needing the following info: pipeline + ticket number (bug/story num) - if re-deploy, pls mark reason | | 2024-06-05 | [2024-06-05 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-06-05+CN+Retrospective) | 2024-06-19 | | @Kuan Wang |
| 7 | Not all the CR steps can be verified matched we need. UVT not overall cover the steps | | 2024-05-22 | [2024-05-22 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-05-22+CN+Retrospective) | | @Zeyu Zhou | @liam li |
| 8 | when we have more than 2 uat pipelines, the version of package may cover each other. And env not enough. | | 2024-06-05 | [2024-06-05 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-06-05+CN+Retrospective) | | @Zeyu Zhou | @Xinmiao Huang |
| | review meeting schedule | | | | | | |
| 9 | regression test cases too thin to cover all old req. and our regression time is too stress to do a full test for the release and this cases lot of hidden risks. | | 2024-06-05 | [2024-06-05 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-06-05+CN+Retrospective) | 2024-09-11 | @Ruiheng Cao | @Kuan Wang |
| 10 | important req should have an enough design review and discussion. And the conclusion should be confirmed from user and PO. Currently, we always been challenged or been raised concern after we go-live. | | 2024-06-19 | [2024-06-19 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-06-19+CN+Retrospective) | | | @Xinmiao Huang |
| 11 | ADO workflow always scan out the security issue at the last time, and sometimes we get another security issue reminder after we fix the original security issue. | | | | | | |
| 12 | Pls create a story to list shortage part of regression testing and then QA can add step by step based on priority. - verify msg send to razor | | | | | | @Kuan Wang |
| 13 | Only few people can be the mandatory pr review but normally we need more people to check and review it. This part only can rely on team members' conscientious. | | | | | | @Kuan Wang |
| 14 | No arrangement foundation upgrade, CN related services are using different foundation version | | | | | | @Chen Yang |
| 15 | Currently QA and DEV share same task, after developer done, assign it to QA, sometimes the status not updated in time will block testing, mostly QA will only have less tasks at sprint beginning and more tasks in the middle and late stages of sprint, that is not good for QA workload tracking and planning | | 2024-05-22 | [2024-05-22 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-05-22+CN+Retrospective) | | | @Xinmiao Huang |
| 16 | Function change may impact existing production data, how to assess the impact scope to avoid unexpected issues. | | | | | | @Xinmiao Huang |
| 17 | Go-live date not clearly. scope related stories cannot be found. | | 2024-06-19 | [2024-06-19 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-06-19+CN+Retrospective) | | | @Chen Yang |
| 18 | story don't have one-time clearly requirements | | 2024-06-19 | [2024-06-19 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-06-19+CN+Retrospective) | | | @Chongxuan Li |
| 19 | package version cover each other | | | | | | |
| 20 | rerun pipeline after all packages prepared | | 2024-07-03 | [2024-07-03 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-07-03+CN+Retrospective) | | | |
| 21 | Prepare release too long 1. dependency with upstream and downstream effects test 2. new reqs after code freeze 3. release scope to large, could we split it | | 2024-07-03 | [2024-07-03 CN Retrospective - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/2024-07-03+CN+Retrospective) | | | |
| 22 | issue tracking, bug or new enhancement? | | | | | | |
| 23 | grooming meeting don't have clearly idea and no clearly stories cannot come into next sprint | | | | | | |
| 24 | When front to back api developing, there is no certain bridge to clarify or describe the api with url/request body/response body/expect exceptions. Can we make it swift using tool like Swagger ? | | | | | | @Shuai Lu |
| 25 | Any plan for business training, especially basic knowledge for new joiners. E.g. 1~2 sessions (30mins) / week | | 2024-07-18 | | | | @Song Wan |
| 26 | uat test cases define not valid or clearly. Causes User not familiar with system | | | | | | @Wayne Wang |
| 27 | demo scope , involve whom in the demo? demo existed func/ demo new or half-new func | | | | | | @Xinmiao Huang |
| 28 | clearly release workflow book clearly plan-dev-golive workflow graph | | 2024-07-18 | | | @Zeyu Zhou | @Xinmiao Huang |
| 29 | Pls assess the workload/conflict when assign tasks to members e.g.: no bindwith to support drop2.1 uat & trade validation uat at the same time, plus new feature testing + on-going(0810) release regression. Recently, big changes because of swift & accounting / bulk process / trade validation etc. Automation code have to be updated accordingly. | | 2024-08-01 | | | | @Kuan Wang |
| 30 | We should settle down go-live list ahead and not add new requirements to this list again and again except any emergent requirements. e.g. H2 go-live on 13th Oct. Add a non-emergency new requirement [Story 5765156 [BIC Netting Static] Enhancement- Limit SWIFT BIC to 11 characters & Auto remove Space (azure.com)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5765156) in 1 week from go-live date. | | 2024-10-07 | | | | @Kuan Wang |
| 31 | | | | | | | |
| 32 | | | | | | | |
| 33 | | | | | | | |
| 34 | | | | | | | |
| 35 | | | | | | | |
| 36 | | | | | | | |