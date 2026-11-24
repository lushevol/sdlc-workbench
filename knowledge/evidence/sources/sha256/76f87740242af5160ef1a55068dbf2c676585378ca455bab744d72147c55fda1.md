# Testing Approach:

- Follow the Tranche 2 testing scope
- Env: - Primary: [Markets Operations One](https://fmo-mfe-fmrp1.pi.dev.net:8453/?show_normal_login=y&survey=no) (FMRP1) / [Markets Operations One](https://fmo-mfe-fmrp2.pi.dev.net:8453/)(FMRP2) - Secondary: [FMO Post Trade Portal](https://fmo-mfe-dev.uk.dev.net:8453/) (DEV)

# UAT Team

| UAT TEAM | User PSID | User Name | User Access |
| --- | --- | --- | --- |
| Data Ops | 1434424 | Shankar M, Shiva | As per confirmation from Shiva, data Ops users do not require any specific ID-based access; all users should be granted GDC and ID access |
| Data Ops | 1528028 | Ramakrishnan, Yogentar |
| Settlement Ops | 1140336 | Eliana, Eliana | ID only |
| Settlement Ops | 1129381 | K Thirunavukarasu, Cordelia Sumita | Both GDC and ID |
| Settlement Ops | 1462616 | Ali, Shaukat | GDC only |

# **New Trade/Trade Migration**

# **MX211:**

# **RATAN:**

# **FMSGW:**

# **LMS:**

Together with Ratan Released/Settled test cases.

![image2024-10-23_17-39-39.png](attachments/image2024-10-23_17-39-39.png)

# **EBBS & TLM (Accounting)**

~~1-2 days of PROD data loading, is it required? As this is not the first time go live, believe it could be integration only?~~

2026-07-08  Suppose only integration required that no feature change and to be tested along with FMSGW testing, then corresponding feed will be generated to TLM.

Aspire should be out of scope. Thanks Karthick will setup a call with GRU team to align the testing strategy. @Karthick Manickam Ramasamy @Jingjing Yang @Arockia Dinesh @Xinmiao Huang

# **Aspire (Out of Scope)**

# **SSDR (via DQSL) & FMMIS**

1. Reporting: Follow the settlement UAT process which includes the manual touch point, SSDR could fetch data and show the report to the users
2. Data Entitlement: Only users applied with FMCES along with Indonesia access will be able to view the data

# **Market UDP **

![image-2026-9-3_17-37-33.png](attachments/image-2026-9-3_17-37-33.png)OSV - Feng, Jerry, SIT is enough. Query ID data with T-35 to T+10

UAT - Utilize the UAT test cases above.

Recon -

1. @Jerry Bin Feng will confirm the time of production dump to be secured for query recon. @Xinmiao Huang please take note.
2. @Jerry Bin Feng mentioned that UDP need the testing of Recon and need RATAN to provide 2-4 weeks prod data including GDC data. Initially agreed that ID can be provided, will follow up to see whether GDC data could be retrieved, which should not be a blocker.

# **FMRP - STELLA / TL **