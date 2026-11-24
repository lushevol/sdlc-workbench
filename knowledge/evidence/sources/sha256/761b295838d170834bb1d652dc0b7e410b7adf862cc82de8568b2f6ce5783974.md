**Strategic SSI stamping**

- [x] current status: dev done, integrating with CDUPS on DEV. Code is NOT merged to UAT yet.
- [x] branch: feature/8447356
- [x] document: [Trade SSI Stamping - Product templates - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Trade+SSI+Stamping+-+Product+templates). The API schema is attached as attachment of this page.
- [ ] Contacts: Paricherla, Vasu, Reddy, Vennapusa Madhava Kesava, Reddy, Vennapusa Madhava Kesava

- [ ] **next: wait for CDU and test in UAT1**

**UBER integration**

- [x] current status: dev done, deployed to DEV for test manually packaged
- [x] branch: feature/7881144
- [ ] **ISSUE: should call "status/move" to update lifecycle status**
- [ ] Xpath3 parser on foundation

Note: this branch is based on above "Strategic SSI stamping" feature, and should always merge code change of feature/8447356

**EMS3 / data entitlement**

- [ ] current status: waiting for EMS3 to provide API schema and guidance, their confluence page: [FM-CES - Downstream Integration Changes - FM Operations Technology - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?spaceKey=FXRCCPE&title=FM-CES+-+Downstream+Integration+Changes)
- [ ] **CES onboarding session **[**SOS** - FM-CES Onboarding | Meeting-Join | Microsoft Teams](https://teams.microsoft.com/l/meetup-join/19%3ameeting_YWZiNDMxYjItNzRmNS00ZTUzLTk5ZDUtNGM1N2RiMTg4NTk5%40thread.v2/0?context=%7b%22Tid%22%3a%22b44900f1-2def-4c3b-9ec6-9020d604e19e%22%2c%22Oid%22%3a%22959ab8b4-6fa2-409f-8c0a-e6214b7f04fd%22%7d)
- [x] Alternative: using our data entitlement solution, completed analysis
- [x] document: [Data entitlement solution (draft) - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3414465801)
- [ ] Add integration test in static data service to test entitlement cases: not completed, committed some code:

commit d7002610eff4f5896e2a24120b19f06c660f6186 (HEAD -> feature/test-data-entitlements)
Author: Li, Quill <2022123@[zone1.scb.net](http://zone1.scb.net)>
Date:   Mon Aug 18 17:15:31 2025 +0800

#7177438: (imcomplete) added integration test for data entitlement api

- [x] use real entitlement api in query service instead of mock

commit d6bba744aa058814791d612353da1b47d27040e3 (HEAD -> feature/7177438-entitlement-tranche, origin/feature/7177438-entitlement-tranche)
Author: Quill Li <2022123@[zone1.scb.net](http://zone1.scb.net)>
Date:   Mon Mar 24 18:07:59 2025 +0800

#7177438: added demo of using embedded-postgres for jpa test

commit a1934d19ee2fc8d5606beb143f167e991d2729a1
Author: Quill Li <2022123@[zone1.scb.net](http://zone1.scb.net)>
Date:   Wed Mar 12 17:10:03 2025 +0800

#7177438: use real entitlement endpoint instead of mock

**ENTRA**

- [ ] current status: low priority, just started spiking
- [x] confirmed that client credential flow could be used as RATAN-EMS3 authentication, ref: [OAuth 2.0 client credentials flow on the Microsoft identity platform - Microsoft identity platform | Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-client-creds-grant-flow)
- [ ] document: [ENTRA integration (draft) - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3436971784)
- [ ] ENTRA contact: [Auth-SvcsAppOn-Boarding@sc.com](mailto:Auth-SvcsAppOn-Boarding@sc.com), [Suganya.S@sc.com](mailto:Suganya.S@sc.com)

**Trade validation/Cashflow affirmation**

- [x] current status: kicked off and gathering information
- [ ] **ongoing: [Trade Validation Automation Use case - Sample documents walkthrough - Session 2 - Series | Meeting-Join | Microsoft Teams](https://teams.microsoft.com/l/meetup-join/19%3ameeting_MGZhMDNjZWQtNzViYy00Njc4LWIxZWUtNDVlMzBiODYwMTQ3%40thread.v2/0?context=%7b%22Tid%22%3a%22b44900f1-2def-4c3b-9ec6-9020d604e19e%22%2c%22Oid%22%3a%22fe2f9819-a746-417c-a4df-670c216f4512%22%7d) from 19 Aug - 22 Aug**