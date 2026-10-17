# Controls: Approved Requirements (Functional & Non-Functional)

---

## Control Attributes

| **Control Name** | Approved Requirements (Functional & Non-Functional) |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** |<br/>- Business context for a solution is understood and agreed<br/>- Solution Requirements are documented and analysed to ensure Solution implemented through acquisition or creation<br/>- Ensure Business context for a solution is understood and agreed and refined as functional and non-functional requirements.<br/>- Comply with Bank's rules and regulations; and<br/>- Realise their defined benefits.<br/>- Solution Requirements are validated with Stakeholders<br/>- Solution Requirements are baselined and change managed. |
| **Control Requirements** |<br/>- No requirements are missing, ambiguous or incorrect that could lead to a material impact to functionality of the designated Technology Service.<br/>- Functional and Non-Functional Requirements (NFRs) are defined with acceptance criteria, prioritized based on the importance to the business, and impact on the user experience.<br/>- NFRs are defined using objective, measurable criteria/use pre-defined template to evaluate them against specific performance metrics of the application. **Note:** Standard NFRs comprise of: Availability, Performance, Capacity, Service Level Agreements, Data, Security/Threat Modeling, Privacy & Monitoring<br/>- Business cases approvals and investment governance are managed under WoW standards.<br/>- This control is applicable only for the tech changes.<br/>- Flow of activities to assess, decompose, prioritize, track delivery risks, managing & reporting outcomes(benefits) can be referenced in SOP. |
| **Control Tasks** |<br/>1. Perform Business Impact assessment and agree on the<br/>&emsp;- QPR Goals<br/>&emsp;- Scope<br/>&emsp;- Approach (MVP) and<br/>&emsp;- Prioritization based on Business roadmap.<br/>2. Perform technical, architecture Impact assessment on the system capabilities to understand material & Architecture impacts and determine KPIs for standard NFR:<br/>3. Identified Nonfunctional requirements are defined as acceptance criteria against each Epic or Feature and are consolidated centrally at application level in the predefined template to enable verification (through (automated) NFT)<br/>4. Review standard NFRs regularly to ensure they remain relevant and compliant.<br/>5. Baseline the requirements and manage changes to the approved requirements. **Note:**<br/>&emsp;- Standard NFRs must be defined for every Business Application and Application Service<br/>&emsp;- This control is applicable only for requirements which are directly required for the delivery of a Technology Solution.<br/>&emsp;- Control Tasks must be carried out using the Banks standard processes and tools.<br/>&emsp;- Business Case approvals and Investment Governance are managed under WoW standards (not part of this control)<br/>&emsp;- For API related releases, please refer to the API Guidelines listed below<br/>&emsp;- Flow of activities to assess, decompose, prioritize, track delivery risks, managing & reporting outcomes(benefits) can be referenced in SOP. |
| **Evidences** | When using the bank's standard engineering pipeline: |

| **Sl.No** | **What** | **Format** | **When** | **Scope** | **Approver** | **Update/Review Frequency** | **Evidence- ADO** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Approved Solution Requirements (Functional) |<br/>- BRD Document, or<br/>- Epics, Features, Stories (using built-in feature of "ADO") |<br/>- Before or as part of Solution Intent Signoff<br/>- As and when the requirements get rebase lined | Functional Requirements | Product Owner . | Create / Update based on evolving Business requirement, initiative or change | Prioritised Requirements as part of the User Stories / Bugs must be tagged in the Release Workitem. |
| 2 | Approved Solution Requirements (Non-Functional) |<br/>- Document based on NFR Confluence template |<br/>- Before or as part of the Solution Intent Signoff<br/>- Review annually or As and when the requirements get rebase lined | Non-Functional Requirements | Product Owner | Create / Update after performing an impact assessment based on Business requirements, initiatives, changes. | NFR documented in the prescribed template and uploaded as part of Application Workitem |

## Relationships

### Qualified References

- **Disciplines**
  - [Requirements](../disciplines/requirements.md)

- **Tasks**
  - [Identify and Capture Functional Requirements](../disciplines/requirements/identify-and-capture-functional-requirements.md)
  - [Refine Functional Requirements](../disciplines/requirements/refine-functional-requirements.md)
  - [Identify and Capture Non-Functional Requirements](../disciplines/requirements/identify-and-capture-non-functional-requirements.md)
  - [Refine Non Functional Requirements](../disciplines/requirements/refine-non-functional-requirements.md)
  - [Define Acceptance Criteria](../disciplines/design-and-architecture/define-acceptance-criteria.md)
  - [Conduct Product Backlog Grooming](../disciplines/requirements/conduct-product-backlog-grooming.md)

- **Roles**
  - [Product Owner](../practices/impact-assessment-on-system-and-on-downstream/roles/product-owner.md)

- **Artifacts**
  - [Product Backlog](../practices/impact-assessment-on-system-and-on-downstream/work-products/product-backlog.md)
  - [API Technical Specification](../work-products/analysis-amp-design/api-technical-specification.md)

- **Tools**
  - [Next Gen Pipeline-ADO](../tools/next-gen-pipeline-ado.md)
  - [Understanding Application Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-application-work-item-in-ado.md)
  - [Understanding Bug Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-bug-work-item-in-ado.md)
  - [Understanding EPIC Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-epic-work-item-in-ado.md)
  - [Understanding Feature Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-feature-work-item-in-ado.md)
  - [Understanding Initiative Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-initiative-work-item-in-ado.md)
  - [Understanding Release Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-release-work-item-in-ado.md)
  - [Understanding Story Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-story-work-item-in-ado.md)
  - [How to do application control evidencing in ADO](../appendix/guidance/how-to-do-application-control-evidencing-in-ado.md)

- **Templates**
  - [Non-Functional Requirements Template](../templates/non-functional-requirements-template.md)
  - [Business Requirements Definition (BRD)](../templates/business-requirements-definition-brd.md)
  - [API Technical Specification](../templates/api-technical-specification.md)

- **Guidelines**
  - [Bug Management Pipeline Controls User Guide](../guidance/guidelines-by-discipline/testing/Bug-Management-Pipeline-Controls-User-Guide.md)
  - [User Story Acceptance Criteria Guidelines](../guidance/guidelines-by-discipline/requirements/user-story-acceptance-criteria-guidelines.md)
  - [User Story Guidelines](../guidance/guidelines-by-discipline/requirements/user-story-guidelines.md)
  - [API Guidelines](../guidance/guidelines-by-discipline/testing/api-guidelines.md)
  - [Mandatory Non Functional Epics and User Stories Guidelines](../guidance/guidelines-by-discipline/analysis-and-design/mandatory-non-functional-epics-and-user-stories.md)
  - [User Story Definition of Done Guidelines](../guidance/guidelines-by-discipline/requirements/user-story-definition-of-done-guidelines.md)
  - [User Story Definition of Ready Guidelines](../guidance/guidelines-by-discipline/requirements/user-story-definition-of-ready-guidelines.md)
  - [Discover and Clarify Requirements with Storyboarding](../guidance/all-guidelines/discover-and-clarify-requirements-with.md)
  - [Effective Requirement Reviews](../guidance/all-guidelines/effective-requirement-reviews.md)
  - [Identify Stakeholders](../guidance/all-guidelines/identify-stakeholders.md)
  - [Non Functional Requirements Template Guidelines](../guidance/all-guidelines/non-functional-requirements-template-guidelines.md)
  - [Requirement Pitfalls](../guidance/all-guidelines/requirement-pitfalls.md)
  - [Requirements Gathering Techniques](../guidance/all-guidelines/requirements-gathering-techniques.md)
  - [Writing Requirements Statements](../guidance/all-guidelines/writing-requirements-statements.md)
  - [API Classifications](../guidance/guidelines-by-discipline/testing/api-classifications.md)
  - [Flow of Work - Standardization](../guidance/all-guidelines/flow-of-work-standardization.md)
  - [Change Delivery Standard (CDS) and guidance](../guidance/all-guidelines/change-delivery-standard-cds-and-guidance.md)
  - [Quarterly Performance Review (QPR)](../guidance/all-guidelines/quarterly-performance-review-qpr.md)
  - [Refinement Forum (RF)](../guidance/all-guidelines/refinement-forum-rf.md)
  - [ESDLC Control Checks in ADO Pipelines](../guidance/supporting-materials/esdlc-control-checks-in-ado-pipelines.md)
  - [Internal Digital Certificate Management: Guidelines and Procedures](../guidance/all-guidelines/internal-digital-certificate-management.md)

- **Checklists**
  - [Release Compliance Controls â€” Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)