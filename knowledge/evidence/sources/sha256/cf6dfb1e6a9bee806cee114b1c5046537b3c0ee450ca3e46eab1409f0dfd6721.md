| | | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INFRA/DEVOPS | Production Setup | | | | | | ~~Prod Server handover~~ ~~2026.6.11~~ | Prod Server handover 2026.7.16 Clear DOD | 1. Internal Traffic 2. Production Pipelines build 3. Infra components deployment, Kafka, Redis, DB, etc | External Traffic | Application service deployments Technical integration verification | CPT | |
| Project delivery | Infra setup DB Common Services | Kafka, Redis, ELK, DB, etc. | | | | | | | | |
| Design | | | | | | | | | | | | |
| Development & Deployment | | | | | | | | | | | | |
| SIT | | | | | Ratan Settlement Verification Integration with all surrounding systems | | | | | | |
| UAT | | | | | | | | | | | | |
| NFR | | | | | | | | | PT | | | |
| Rehearsal & Go live | | | | | | | | | | | | Go Live 2026.12.05 |
| Post Care | | | | | | | | | | | | |

DoD of Prod Server handover:

- VM ready with application OS customization requirement, OS version, user group/permission, storage
- PostgreSQL DB ready
- Generic network and firewall accessibility
- ITRS configurability
- PSS support permission and sign-off

DoD of Aug tasks:

- SSH and connectivity with ADO, Hashicorp, GDCW/GDCE network
- Production pipeline build up and verification
- DNS/VIP and certification generation
- Infra component deployment, redis, ELK, Kafka, OpenSearch

DoD of Sep tasks:

- generic service account creation
- Hashicorp vaulting
- connection setup with up streams/down streams
- message channel setup, FileIT, FM Solace, Enterprise Solace, Kong

DoD of Oct tasks:

- application service deployment
- integration verification
- issue fixing

# **Architecture**

**![image-2026-1-19_17-28-33.png](attachments/image-2026-1-19_17-28-33.png)**

# **Surrounding System Integration**

****

**[RATAN - Indonesia Onshoring - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/RATAN+-+Indonesia+Onshoring)**

<u>**List of in scope applications and key points discussed **</u>

# **Dependencies**

| ** ** | **Expectation** |
| --- | --- |
| NFR | OLA, SLA |
| | DR Testing |
| | ADO Pipeline Integration |
| | DB Initialization |
| Integration | MB integration between Global and ID |
| | |

# **Reference**

[Indonesia Contingency Plan - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/Indonesia+Contingency+Plan)

[RATAN Indonesia Instance - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+Indonesia+Instance)

[RATAN ONE Indonesia Env Overview - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+ONE+Indonesia+Env+Overview)

RAID & Surrounding systems: [RATAN - Indonesia Onshoring - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/RATAN+-+Indonesia+Onshoring)

# **Contact**

| System | Dev SPOC | PSS SPOC | |
| --- | --- | --- | --- |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |