| Date | 2024-06-05 |
| --- | --- |
| Participants | Cao, Geoffrey Ruiheng ; Feng, Lina; Guiling, Wang; Huang, Caroline Xinmiao; Li, Eddie Chongxuan; Lu, Shuai; Ma, Shimeng; Wang, Elena; Wang, Wayne Weichao; Yang3, Chen ; Zhong, Rex; Li, Pengpeng; Meng1, Fanjing |

Happiness Index:

Complaints Points we have gone through:

| No. | New or Follow-up | Complaints Points | Comments from Dev | Solution | Follow-up |
| --- | --- | --- | --- | --- | --- |
| 1 | New | Deploy to uat needing the following info: pipeline + ticket number (bug/story num) - if re-deploy, pls mark reason | | 1. Dev need to let the qa know about the deployment related story/bug ticket. 2. if re-deploy caused by pre-chk, qa and devops can help to click 3. if same/new version with new pipeline for same story, need to let qa know the reason. | |
| 2 | New | when we have more than 2 uat pipelines, the version of package may cover each other. And env not enough. | no dev env use for CN. Current dev env is used for EBBS uat. | 1. dev needs to check the services version on Eureka manually before each deploy. 2. Geoffrey is discussed with user to move EBBS test to UAT1 env from June 21th | |
| 3 | New | regression test cases too thin to cover all old req. and our regression time is too stress to do a full test for the release and this cases lot of hidden risks. | Geoffrey will schedule another meeting to discuss for this. and we need more regression test and dailty regression | 1. change to full-regression | |