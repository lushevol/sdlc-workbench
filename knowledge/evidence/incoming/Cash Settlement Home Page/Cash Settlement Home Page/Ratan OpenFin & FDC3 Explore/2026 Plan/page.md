##

## ![image-2025-12-2_12-0-35.png](attachments/image-2025-12-2_12-0-35.png)

**2026 Platform Delivery Roadmap**

**Stream A: UX Transformation (Global Design System)**

*The Foundation: Establishing a unified visual language and architecture.*

- **A.1: Design System Artifacts (Ratan)**
- **A.2: Component Library (Ratan UI)**
- **A.3: Platform Shell 2.0**

**Timeline:**

- **Feb:** Design System definition (Tokens/Palettes) & Artifact creation.
- **Mar:** Prototype validation & Stakeholder approval.
- **Apr:** **[Critical Milestone]** Platform Shell 2.0 POC (Login, Landing, Admin).
- **Apr:** Component Library v1.0 Release.
- **May:** Tenant Engagement & Migration Workshops.
- **Jun - Aug:** Tenant Application Migration (Business Logic Integration).
- **Aug:** Platform Shell 2.0 General Availability (GA).

**Resources**

- UX: 30MD

- UI: 40MD

- QA: 20MD

**Stream B: User Activity Monitoring (Telemetry & Insights)**

*The Feedback Loop: Data-driven operational visibility.*

- **B.1: Telemetry Instrumentation**
- **B.2: Ops Insight Dashboard**
- **B.3: Predictive Monitoring (ML)**

**Timeline:**

- **Mar:** Data schema & Dashboard solution design.
- **Apr:** Telemetry implementation (via Component Library) & Dashboard POC.
- **May:** ML Model design & training strategy.
- **Jun - Jul:** ML Service POC (Anomaly Detection).
- **Aug:** ML Service GA.

**Resources**

- UX: 10MD

- UI: 40MD
- BE: 40MD

- QA: 10MD

**Stream C: Interoperability (FDC3 Standards)**

*The Connective Tissue: Enabling seamless app-to-app communication.*

- **C.1: Context & Intent Definition**
- **C.2: App Directory (Registry)**
- **C.3: API (The Broker)**
- **C.4: Developer Experience (Hooks)**
- **C.5: Tenant Integration**
- **C.6: OpenFin Integration**

**Timeline:**

- **Jan:** Desktop Agent & Registry POC.
- **Mar:** Desktop Agent GA (Intent Registration & Resolution).
- **Apr:** CDUPS Integration.
- **Apr:** OpenFin Adapter GA.
- **Jun - Jul:** Tenant Migration (Legacy to Intent-based workflows).
- **Aug:** Expansion of Intent capabilities.

**Resources**

- UI: 80MD
- BE: 30MD

- QA: 20MD

**Stream E: AI-Powered Interoperability**

*The Orchestrator: Natural Language Interface for Platform Actions.*

- **E.1: Conversational Interface (Chat Widget)**
- **E.2: Intent Translator (NLP Logic)**

**Timeline:**

- **Apr:** Architecture alignment with AI Factory.
- **May:** Chatbot UI Prototyping.
- **Jun - Jul:** Functional Showcase (NLP to FDC3 execution).
- **Sep:** AI Assistant GA.

**Resources**

- UX: 10MD

- UI: 20MD
- BE: 50MD

- QA: 20MD

## OpenFin On-Boarding Estimation

| Phase | Activity | Effort (MD) | Resource | Rationale/Notes |
| --- | --- | --- | --- | --- |
| 0. Setup | Project Inception & Environment | 25 | | |
| Team Onboarding, Access, Tooling & OpenFin Training | 5 | All | Getting Repo access, OpenFin training, dev env setup. |
| Architecture & Security Review | 10 | SE | |
| CI/CD Pipeline Setup for OpenFin | 5 | SE | Setup Pipelines for team work and ADO stages. |
| 1. Design | Design & Architecture | 20 | | |
| Technical Design & FDC3 Strategy | 10 | SE | Defining FDC3 strategy of portal. |
| UX/UI Design (Shell & Workspace) | 5 | UI | Designing splashing image, icons, window layout, etc. |
| Test Strategy & Plan Creation | 5 | QA | Defining scope for regression and automation, especially for OpenFin. |
| 2. Dev | Core Platform Foundation | 30 | | |
| OpenFin Installer & Update Logic | 5 | SE | Pushing & confirming of portal installer selection, RVM upgrading strategy, license renewing. |
| Development | 20 | UI | 1. setup manifests for portal. 2. implement central fdc3 broker. 3. implement routing logics for intents in platform provider. 4. implement use case for trade ticket. |
| 3. Integration | Multi-App Integration | 5 | | |
| Governance & Team Coordination | 5 | SE | Coordinating with all tenant team for wrapping their apps. |
| 4. QA | Quality Assurance & Hardening | 30 | | |
| Acceptance & Regression Testing | 10 | QA | Integration testing with blade. |
| Performance & Memory Profiling | 10 | QA | OpenFin can be memory-heavy; needs specific testing. |
| QA Automation Scripting | 10 | QA | Writing automation scripts for openfin container. |
| 5. UAT/Train | User Acceptance & Training | 25 | | |
| User Training & UAT supporting | 10 | UI | guide users from none to installing to BAU. |
| PSS Training | 5 | SE | |
| Documentation (Tech & User Guide) | 5 | SE | Expanded for technical handover. |
| 6. Release | Release & BAU | 15 | | |
| Release Coordination & Deployment | 5 | SE | |
| TOTAL | | 115 | | |

**SE**: 40 → 2M

**UI**: 35 → 2M

**QA**: 40 → 2M

Total Duration: 2M

Total Cost: 63.25K

![image-2026-2-6_10-9-32.png](attachments/image-2026-2-6_10-9-32.png)

<details>
<summary>Expand Details</summary>

```
gantt
    title Project Plan: OpenFin On Boarding
    dateFormat  YYYY-MM-DD
    excludes weekends

    section Hiring Phase
    Recruiting & Interviews      :done,    des1, 2026-03-01, 2026-03-31
    Offer & Background Checks    :active,  des2, 2026-04-01, 2026-04-30

    section 0. Setup (May)
    Team Onboarding (All)        :crit,    s1, 2026-05-01, 5d
    Arch & Security Review (SE)  :         s2, after s1, 10d
    CI/CD Setup (SE)             :         s3, after s2, 10d
    
    section 1. Design (May/Jun)
    Technical Design (SE)        :         d1, after s3, 15d
    UX/UI Design (UI)            :         d2, after s1, 5d
    Test Strategy (QA)           :         d3, after s1, 5d

    section 2. Dev (May/Jun/Jul)
    OpenFin Installer Logic (SE) :         dv1, after d1, 15d
    Core Development (UI)        :         dv2, after s2, 30d
    In-Sprint Testing (QA)       :         dv3, after s2, 30d

    section 3. Integration (Jul/Aug)
    Governance & Coord (SE)      :         i1, after dv1, 30d
    Multi-App Integration (UI/SE):         i2, after dv2, 30d

    section 4. QA (Aug/Sep/Oct)
    QA Automation Scripting (QA) :         q1, after dv3, 30d
    Acceptance Testing (QA)      :         q2, after i2, 10d
    Full Regression (QA)         :         q3, after q2, 20d
    Perf & Memory Profiling (QA) :         q4, after q3, 10d
    Security & Pen-Testing (SE)  :         q5, after i1, 10d

    section 5. UAT/Training (Sep/Oct)
    Documentation (SE)           :         u1, 2026-09-10, 15d
    User Training & Demos (UI)   :         u2, 2026-09-17, 10d
    PSS Training (UI)            :         u3, 2026-10-07, 10d
    UAT Support (QA)             :         u4, 2026-10-07, 10d
    UAT Bug Fixing (UI)          :         u5, after u4, 10d

    section 6. Release (Nov)
    Release                      :crit,    milestone, 2026-11-16, 1d
    Release Coordination (SE)    :         r1, 2026-11-03, 10d
    Entra Adoption (UI)          :         r2, 2026-10-20, 20d
    BAU Handover (UI)            :         r3, after r2, 15d
    Post-Go-Live Support (All)   :         r4, after r2, 10d
```

</details>

**Roughly Planning**

| **Month** | **Phase** | **SE Focus** | **UI Focus** | **QA Focus** |
| --- | --- | --- | --- | --- |
| May | Setup | Onboarding & Tooling & Training, Architecture & Security Review, CI/CD | Onboarding & Tooling & Training | Onboarding & Tooling & Training |
| May/Jun | Design | Technical Design, FDC3 Strategy | UX/UI design | Test Strategy & Planning |
| Jun/Jul | Development | Installer, Platform Provider, FDC3 Broker | Core Portal Development, Trade Ticket | In-Sprint Testing |
| Jul | Integration | Governance, Multi-App Coordination | Support Tenant App Wrapping | |
| Aug/Sep | QA & Hardening | Security Testing & Fixes Support | | Regression, Automation, Performance |
| Oct | UAT & Training | Documentation, Tech Handover | User Training, UAT Fixes | UAT Support |
| Oct/Nov | Release & BAU | Release Coordination | Entra Adoption, BAU Handover | Post-Go-Live Support |

<details>
<summary>Expand Details</summary>

</details>

**Resource Capacity Per Sprint:**

- **🎨**** UX (0.2 FTE):** **~2 MD**. *Strict Focus: High-level Logic, Critical Reviews, Design Sign-off.*
- **💻**** UI (1.5 FTE):** **~15 MD**. *Focus: The heavy lifting for Frontend, FDC3 Logic, and Visuals.*
- **☕**** JAVA (1.0 FTE):** **10 MD** *(Starting Sprint 5 - March).* *Focus: Backend APIs, Telemetry, ML, NLP.*

**Q1 Focus: FDC3 Connectivity & Design Foundation**

*Key Goals: Get the Interop Broker live and define the "New Look" tokens without backend support.*

| **Sprint** | **Dates** | **Key Milestones** | **🎨**** UX Focus (2 MD)** | **💻**** UI Focus (15 MD)** | **☕**** JAVA Focus (0-10 MD)** | **Activity Summary** |
| --- | --- | --- | --- | --- | --- | --- |
| **S1** | Jan 12 - 23 | **Project Kickoff** | **Audit:** Review current screens & flows (2MD) | **FDC3:** Init Broker (Client-side) & App Directory UI (15MD) | **N/A** (0 MD) | Kickoff; UI builds the FDC3 Desktop Agent skeleton (JS only); UX reviews existing flows. |
| **S2** | Jan 26 - Feb 6 | | **Design:** Define Tokens (Color/Font) (2MD) | **FDC3:** App Directory Logic & Broker Routing (15MD) | **N/A** (0 MD) | UX freezes tokens; UI implements Broker Context/Intent routing logic; QA preps FDC3 test cases. |
| **S3** | Feb 9 - 20 | **POC: FDC3 Broker** | **Review:** Broker Flow Review (2MD) | **FDC3:** Polish Broker API; **UX:** Init NPM Lib (15MD) | **N/A** (0 MD) | **POC Demo: FDC3 Broker.** UI sets up Component Library repo; QA validates Broker messaging. |
| **S4** | Feb 23 - Mar 6 | | **Design:** Monitor Dashboard Wireframe (2MD) | **FDC3:** Hardening; **UX:** Core Components (Btn/Inp) (15MD) | **N/A** (0 MD) | UI finalizes Broker for release; Starts building basic Ratan components. |
| **S5** | Mar 9 - 20 | | **Review:** CDUPS Integration Plan (2MD) | **FDC3:** Integration Support; **CDUPS:** Assist Integration (15MD) | **FDC3:** App Directory Backend API (10MD) | **Java Joins.** Tenant integration begins immediately. |

**Q2 Focus: Ecosystem Expansion & Observability**

*Key Goals: OpenFin adoption, Shell 2.0 POC, and releasing the Monitoring Dashboard.*

| **Sprint** | **Dates** | **Key Milestones** | **🎨**** UX Focus (2 MD)** | **💻**** UI Focus (15 MD)** | **☕**** JAVA Focus (10 MD)** | **Activity Summary** |
| --- | --- | --- | --- | --- | --- | --- |
| **S6** | Mar 23 - Apr 3 | **Tenant Integ. Start** | **Design:** Shell Nav Concepts (2MD) | **OpenFin:** Config & Manifest; **FDC3:** Tenant Support (15MD) | **Monitor:** Telemetry API Design & Database (10MD) | Java designs Telemetry DB; UI configures OpenFin manifest; Support FDC3 tenants. |
| **S7** | Apr 6 - 17 | **REL: FDC3 Broker** | **Review:** OpenFin Launch Flow (2MD) | **Shell:** Scaffold (Login/Auth); **OpenFin:** Adapter Logic (15MD) | **Monitor:** Telemetry Ingestion Service (10MD) | **Release: FDC3 Broker & App Directory.** UI starts Shell 2.0 structure; Java builds Telemetry ingestion. |
| **S8** | Apr 20 - May 1 | **REL: OpenFin Adapter** | **Design:** Dashboard Visuals (2MD) | **Shell:** Landing Page & Menu; **Monitor:** Dashboard UI (15MD) | **Monitor:** Metric Aggregation Logic (10MD) | **Release: OpenFin Adapter.** UI builds Shell Landing & Monitor Charts; Java connects metrics API. QA tests OpenFin. |
| **S9** | May 4 - 15 | **POC: Shell 2.0** | **Review:** Shell POC Feedback (2MD) | **Shell:** Polish & Demo; **UX:** DataGrid Component (15MD) | **ML:** Data Pipeline Setup (10MD) | **POC Demo: Shell 2.0.** Java starts ML data piping; UI focuses on complex components (Grid). |
| **S10** | May 18 - 29 | | **Design:** ML Insight Cards (2MD) | **Monitor:** Dashboard Polish & Integration (15MD) | **ML:** Data Cleaning & Storage (10MD) | UI connects Dashboard to real Telemetry API; Java ensures data flow for future ML. |
| **S11** | Jun 1 - 12 | **REL: Monitoring** | **Review:** Dashboard Final Look (2MD) | **Monitor:** Final Bugfix; **Shell:** Tenant Migration Guide (15MD) | **ML:** Anomaly Detection Model R&D (10MD) | **Release: Ops Monitoring Dashboard.** UI writes migration docs for Shell. |

**Q3 Focus: Intelligence & Migration**

*Key Goals: Migrating tenants to the new Shell and introducing ML/AI capabilities.*

| **Sprint** | **Dates** | **Key Milestones** | **🎨**** UX Focus (2 MD)** | **💻**** UI Focus (15 MD)** | **☕**** JAVA Focus (10 MD)** | **Activity Summary** |
| --- | --- | --- | --- | --- | --- | --- |
| **S12** | Jun 15 - 26 | | **Design:** Chatbot Widget (2MD) | **Shell:** Tenant Migration Support; **ML:** Insight UI (15MD) | **ML:** Model Training & Validation (10MD) | Java trains Anomaly model; UI helps tenants move to Shell 2.0. |
| **S13** | Jun 29 - Jul 10 | **POC: ML Service** | **Review:** ML Accuracy (2MD) | **Shell:** Final Polish; **AI:** Chatbot UI Skeleton (15MD) | **ML:** Serving Layer API (10MD) | **POC Demo: ML Service.** Java exposes ML API; UI builds Chatbot frame. |
| **S14** | Jul 13 - 24 | | **Design:** Chat Interaction (2MD) | **Shell:** Regression Fixes; **AI:** Connect Chat UI (15MD) | **AI:** Intent Translator Logic (NLP) (10MD) | Java starts NLP logic; UI finalizes Shell 2.0 for release. |
| **S15** | Jul 27 - Aug 7 | **REL: Platform Shell** | **Review:** Shell GA Sign-off (2MD) | **Shell:** Release Prep; **AI:** Chat Response UI (15MD) | **AI:** Intent Resolution Service (10MD) | **Release: Platform Shell 2.0 GA.** Major milestone. Java connects NLP to FDC3. |
| **S16** | Aug 10 - 21 | | **Review:** AI Safety Rules (2MD) | **AI:** Chatbot Polish; **ML:** Feedback Loop UI (15MD) | **AI:** Chatbot Context Awareness (10MD) | Post-Shell support. Focus shifts entirely to AI/Chatbot logic. |

**Q4 Focus: AI & Finalization**

*Key Goals: Releasing the AI Assistant and wrapping up the year.*

| **Sprint** | **Dates** | **Key Milestones** | **🎨**** UX Focus (2 MD)** | **💻**** UI Focus (15 MD)** | **☕**** JAVA Focus (10 MD)** | **Activity Summary** |
| --- | --- | --- | --- | --- | --- | --- |
| **S17** | Aug 24 - Sep 4 | **POC: AI Assistant** | **Review:** Chat Experience (2MD) | **AI:** End-to-End Chat Flow; **ML:** Refine Models (15MD) | **AI:** Action Execution Logic (10MD) | **POC Demo: AI Assistant.** Show text-to-action workflows. |
| **S18** | Sep 7 - 18 | | **Design:** 2027 Vision (2MD) | **AI:** Hardening & Edge Cases; **Shell:** Maintains (15MD) | **AI:** Performance Tuning (10MD) | QA hammers the Chatbot; Devs fix bugs and optimize latency. |
| **S19** | Sep 21 - Oct 2 | **REL: ML Service** | **N/A** | **ML:** Visualizations in Dashboard (15MD) | **ML:** Retraining Pipeline (10MD) | **Release: ML/Anomaly Service GA.** (Follow up to Monitor Release). |
| **S20** | Oct 5 - 16 | **REL: AI Assistant** | **N/A** | **AI:** Final Polish (10MD) | **AI:** Security Audit Fixes (10MD) | **Release: AI Assistant / Chatbot GA.** |
| **S21** | Oct 19 - 30 | **Project Closure** | **Review:** Retro & Handoff (2MD) | **Doc:** Tech Docs & Handover (5MD) | **Doc:** API Docs & Handoff (5MD) | Year-end cleanup, documentation, and 2027 planning. |

![image-2026-1-21_14-53-15.png](attachments/image-2026-1-21_14-53-15.png)

**EXPAND: FDC3 Estimation**

### **FDC3 Delivery**

| Main Module | Development Sprint | Function | Location |
| --- | --- | --- | --- |
| FDC3 Broker | UI/1.5 sprints | Provides DA APIs with security control - intent raising and resolving - channel - entitlement control | mfe-base |
| FDC3 Admin Module (alia App Directory) | UI/1 sprints | Register intent and context subscription so that system can route intent to target app. | mfe-base |
| FDC3 Service (alia App Directory Service) | Java/2 sprints | Provides CURD for FDC3 intents and context. | single-ui-bff |
| FDC3 OpenFin Adapter | UI/1 sprints | Bridging OpenFin and FDC3 broker, enable - Inbound intent from OpenFin to Portal - Outbound intent from Portal to OpenFin | mfe-base & mfe-openfin |

**OpenFin On boarding estimation**

**![image-2026-1-21_13-58-55.png](attachments/image-2026-1-21_13-58-55.png)**

| | | |
| --- | --- | --- |
| Requirements | 1. Ratan on board to OpenFin 2. Ratan can open Blade without login | |
| Use Case | Trade Tickets | |
| Estimation | 1. Clarify Use Case Details (0.5 sprint) 2. Design & Development 1. FDC3 Broker (1UI/2 sprints) 2. FDC3 OpenFin Adapter (1UI/1 sprints) 3. Ratan Application FDC3 Integration (1 sprints) 4. Ratan → Blade bypass authentication (?) 3. Verification & Regression (1 sprints) 4. Stockholders agreements (SLA/OLA) (2 sprints) | Day 1 ETA: 1UI, 5.5 sprints, release date Apr 25 (buff 1 sprint). Day 2 ETA: ? |
| Risk | 1. Business buy-in 2. VAT required 3. Ratan → Blade auth bypass | |

#### Blade Login Process

| User Type | Endpoint | Required Inputs | Authentication Source | FMAA Token Used? | JWT Token Generation |
| --- | --- | --- | --- | --- | --- |
| Internal | `/internal-login` | Username, Password, OTP (if MFA required) | FMAA (internal system) | Yes | `tokenFactory.createTokenForInternalUser(principal, FMAA token)` |
| External | `/silent-login` | S2B JWT token (in header) | S2B (external system) | No | `tokenFactory.createTokenForExternalUser(principal, termsAccepted)` |

**Process Details:**

- **Internal Login:** 1. UI sends username, password, and OTP (if required) to `/internal-login`. 2. Backend validates credentials with FMAA. 3. If successful, FMAA returns an access token. 4. Backend generates a JWT token using user details and FMAA token.
- **External Login:** 1. UI sends a silent login request with S2B JWT token in the header to `/silent-login`. 2. Backend validates the S2B JWT token. 3. If successful, backend generates a JWT token for the session (no FMAA token involved).

**Notes:**

- Internal users require credential validation and may need MFA.
- External users rely on an existing S2B JWT token for authentication.
- JWT tokens are set as cookies for session management after successful login.

### FDC3 web estimation

| | | |
| --- | --- | --- |
| Requirements | [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11829853](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11829853) 1. Ratan trade blotter can open CDUPS confirmation status. 2. CDUPS confirmation can open Ratan trades & cashflows. | |
| Use Case | CDUPS On Boarding | |
| Estimation | 1. Clarify Use Case Details (0.5 sprint) 2. Design & Development 1. FDC3 Broker (1UI/2 sprints) 2. FDC3 Admin Module (1UI/1 sprints) 3. FDC3 Service (1Java/2 sprints) 4. Ratan Application FDC3 Integration (1.5 sprints) 3. Verification & Regression (1 sprints) | ETA: 1UI, 6 sprints, 1Java, 2 sprints, release date May 9th (buff 1 sprint). |
| Risk | | |

**EXPAND_END**

<details>
<summary>Expand Details</summary>

## 1. Key Deliveries

### A. UX Transformation (GDS)

**Final Deliveries:** Figma Prototypes, Elements/Components Packages, Platform Shell 2.0

#### Breakdown

- **A.1: The North Star Spec (Design Artifact)** - **Deliverable:** High-fidelity Figma/Sketch <u>prototypes</u> for design tokens (Font stacks, Color palettes (light/dark modes), Spacing units, etc) critical screens (Login, Shell, Menu, etc.) approved by stakeholders. - **Success Criteria:** Stakeholder sign-off on the "New Look."
- **A.2: The "Smart" Component Library (NPM Package)** - **Deliverable:** An internal NPM package containing UI components (Inputs, Buttons, Data Grids, Form Controls, etc). - **(Enabler) Migration "Starter Kit": **A code repository template + Documentation site + Migration CLI tool (optional) for Ratan and pilot teams.
- **A.3: Core Platform Shell 2.0 (Code Artifact)** - **Deliverable:** The deployable host container that implements the layout, navigation, and auth flow. - **Require Go Live:** yes

> Resources: 1 UX / 30MD, 1 UI / 40MD, 1 QA / 15MD

#### Sprint Planning

### B. User Activity Monitoring (Telemetry & Insights)

**Final Deliveries:** Telemetry SDK, Ops Dashboard.

#### Breakdown

- **B.1: The Metrics Definition** - **Deliverable:** A finalized document defining standard events, business benefits and clear actionable insights. get signoff.
- **B.2: Telemetry Hook** - **Deliverable:** The instrumentation logic that captures events and sends them to monitoring service. - **Note:** Possible to merge into implementation in **A.2**. - **Require Go Live:** yes
- **B.3: The Ops Insight Dashboard** - **Deliverable:** A live dashboard visualizing the specific metrics defined in B.1. - **Require Go Live:** yes

> Resources: 1 UX / 10MD, 1 UI / 30MD, 1 JAVA / 20MD, 1 QA / 10MD.

### C. Interoperability (FDC3)

**Final Deliveries:** FDC3 Adoption Standard/Implement for Browser (Internal),

#### Breakdown

- **C.1: Intent & Context Definition** - **Deliverable:** Define existing interaction scenarios and ongoing workflows. (e.g. trade - cashflow, dashboard - cashflow, etc.)

- **C.2: The Intent Registry** - **Deliverable:** A searchable database listing which apps handle which intents, built in Admin Module. - **Require Go Live:** yes
- **C.3: The FDC3 Desktop Agent (Broker)** - **Deliverable:** The background service running in Platform Shell (A.2) that routes messages between apps. - **Note:** No dependency on GDS Shell v2, as it does not reply on the GDS Shell UX. - **Require Go Live:** yes
- **C.4: FDC3 Hooks** - **Deliverable:** React hooks (e.g., `useFDC3Context`) exposed so tenants can easily "listen" and trigger for context changes. - **Require Go Live:** yes
- **C.5: Tenant Migration & Integration** - **Goal:** Migrate existing in applications interaction to intent based. Integrate new tiles capabilities. - **Benefit:** Evolves manual workflows into intent-based instructions, serving as a precondition for AI automation. - **Require Go Live:** yes

> Resources: 1 UI / 60MD, 1 JAVA / 30MD, 1 QA / 15MD

### D. Desktop Strategy (OpenFin Integration)

**Final Deliveries:** OpenFin manifest, Post Trade Portal FDC3 Broker (external), Platform Broker

#### Breakdown

- **D.1: Ratan OpenFin Manifest** - **Deliverable:** `manifest` for Ratan, platform provider to manage and route intents. - **Goal:** Enable ratan to launch within OpenFin runtime environment. - **Dependency:** Rely on clear business stories and roadmaps. - **Require Go Live:** yes
- **D.2: Custom Layout *** - **Deliverable:** Custom code that handles the "Snap and Dock" logic. - **Note:** Depends on requirements. - **Require Go Live:** yes

> Resources: 1 UI / 10 MD

### E. AI Powered Interoperability

**Final Deliveries:** Chatbot UI

#### Breakdown

- **E.1: The Chatbot Widget UI** - **Deliverable:** The visual chat interface embedded in the Shell (A.2). - **Dependency:** AI Factory policy - **Note:** The chatbot UX can be covered by A.2 - **Require Go Live:** yes
- **E.2: The "Intent Translator" (AI Logic)** - **Deliverable:** The logic layer that converts Natural Language ("open trade 34982745") into an FDC3 Context Object (`{ type: "scb.fmptp.trade", id: { tradeId: "34982745" } }`). - **Dependency:** Requires clear workflow definition cross business. Requires **C.1 (Registry)** to know what commands are possible. Requires **C.4 (Migration)** for tenant adoption/implementation. - **Require Go Live:** yes

> Resources: 1 UX / 10MD, 1 UI / 20MD, 1 JAVA / 50MD, 1 QA / 10MD

### F. On Boarding Self Service

**Final Deliveries:** Admin Module go live,

#### Breakdown

> Resources: 1 UX / 5MD, 1 UI / 10MD, 1 DevOps / 10MD

## 2. Risks & Mitigations: Refinement

**Tenant Team Adoption**

- *The Risk:* The success of GDS (Visuals), Telemetry (Monitoring), FDC3 (Interop) relies heavily on decentralized tenant teams updating their codebases.
- *Mitigation:* - **"Trojan Horse" Approach:** Bundle the Telemetry hook and FDC3 listeners *inside* the GDS UI components. If they want the new modern look, they automatically get the tracking and interop capabilities. - **Developer Experience (DX):** Provide a copy-paste "Starter Kit" and dedicated office hours to help tenant developers migrate. - **Leadership Mandate:** Utilize the "Future of Operations" vision to set a hard deadline for compliance, supported by senior leadership.

**Performance Overhead (Risk):**

- *The Risk:* Bundling GDS + Telemetry + FDC3 listeners into every component might make the apps heavy or slow to render.
- *Mitigation:* Strict bundle-size budgets for the Component Library (A.3).

**The "AI Factory" Delay (Risk):**

- *The Risk:* Topic E relies on AI Factory. If they are late, your Chatbot is just an empty UI.
- *Mitigation:* Decouple the UI. Build the Chatbot interface (E.1) to handle simple Regex commands first, then upgrade to LLM when the Factory is ready.

## 3. The Master Roadmap

- **Goal:** Evolve the platform from a fragmented UI into an interoperable, AI-ready ecosystem.
- **Strategy:** **Build** (Q1 Foundation) -> **Connect** (Q2 Data/FDC3) -> **Migrate** (Q3 Adoption) -> **Automate** (Q4 AI).

#### **Phase 1: The Foundation (Q1)**

Theme: Visual Transformation & Containerization

Focus: Establishing the "New Look" and deploying the host container (Shell) so it is ready to receive apps.

| **ID** | **Initiative** | **Key Deliverable** | **Dependency** | **Resource** |
| --- | --- | --- | --- | --- |
| **A.1** | **North Star Spec** | Design System Tokens (Figma), Critical Screen Prototypes. | Stakeholder Buy-in | 1 UX |
| **A.4** | **Platform Shell 2.0** | **[KEY GO LIVE]** The Host Container. Handles Layout, Auth, Nav. | A.1 | 1 UI, 1 QA |
| **A.2** | **Smart Comp. Lib** | Internal NPM Package (Grids, Inputs, Buttons). | A.1 | 1 UI |
| **B.1** | **Metrics Def.** | Document defining events and business KPIs. | None | 0.5 BA/UX |

#### **Phase 2: Connectivity & Insights (Q2)**

Theme: The Nervous System (Telemetry & Interop)

Focus: Wiring up the backend infrastructure (FDC3/Telemetry) before mass migration.

| **ID** | **Initiative** | **Key Deliverable** | **Dependency** | **Resource** |
| --- | --- | --- | --- | --- |
| **B.3** | **Telemetry Hook** | Instrumentation logic to route events to monitoring. | A.4 | 1 Java, 0.5 UI |
| **B.2** | **Ops Dashboard** | **[KEY GO LIVE]** Live visualization of adoption/performance. | B.1, B.3 | 1 UI |
| **C.3** | **FDC3 Agent** | **[KEY GO LIVE]** Background Service (Broker) for message routing. | None | 1 Java |
| **C.2** | **Intent Registry** | Admin DB listing app capabilities/intents. | C.1 | 0.5 Java |
| **A.3** | **Starter Kit** | Migration CLI, Docs, and Templates for Tenants. | A.2, A.4 | 1 UI |

#### **Phase 3: Expansion & Migration (Q3)**

Theme: Adoption & Desktop Strategy

Focus: The heaviest lift of the year—moving tenants to the new stack and enabling the desktop wrapper.

| **ID** | **Initiative** | **Key Deliverable** | **Dependency** | **Resource** |
| --- | --- | --- | --- | --- |
| **C.5** | **Tenant Migration** | **[KEY GO LIVE]** Migrating apps to use Intents & New Shell. | A.3, C.3 | 1 UI, 1 QA |
| **C.4** | **FDC3 Hooks** | `useFDC3Context` React hooks for developer ease. | C.3 | 0.5 UI |
| **D.1** | **OpenFin Manifest** | **[KEY GO LIVE]** Ratan config for OpenFin Runtime. | A.4 | 0.5 UI |
| **D.2** | **Custom Layout** | Snap & Dock window management logic. | D.1 | 0.5 UI |

#### **Phase 4: Automation (Q4)**

Theme: AI Orchestration

Focus: Leveraging the registry and structured intents to enable Natural Language commands.

| **ID** | **Initiative** | **Key Deliverable** | **Dependency** | **Resource** |
| --- | --- | --- | --- | --- |
| **E.1** | **Chatbot Widget** | Visual Chat Interface embedded in Shell. | A.4 | 1 UI |
| **E.2** | **Intent Translator** | **[KEY GO LIVE]** Logic converting NLP to FDC3 Contexts. | C.2, C.5 | 1 BA, 1 Java |
| **-** | **Year-End Polish** | Tech debt cleanup, perf tuning, final QA. | All | All Hands |

## 3. Visual Timeline

![2026 roadmap.png](attachments/2026 roadmap.png)

## 4. Consolidated Resource Plan

*Total Squad Size Recommendation: 6 FTE*

| **Role** | **Count** | MD | Main Scopes |
| --- | --- | --- | --- |
| **UI Devs** | 1 | 160 (8M) | |
| **Java/Backend** | 1 | 100 (5M) | |
| **UX Designer** | 1 | 50 (2.5M) | |
| **QA Automation** | 1 | 50 (2.5M) | |

## 5. Critical Risks & Dependencies

1. **The "Chicken and Egg" of Migration (C.5):** - **Risk:** Tenants cannot migrate in Q3 if the **Starter Kit (A.3)** and **Components (A.2)** aren't solid in Q2. - **Mitigation:** The Starter Kit must be treated as a product with its own release cycle in late Q2.
2. **AI Data Prerequisites (E.2):** - **Risk:** AI cannot "translate" commands if the **Intent Registry (C.2)** is empty. - **Mitigation:** Enforce that every app migrated in Q3 *must* register their intents in the Registry as part of their Definition of Done.

</details>

| Tasks | Oct | Nov | Dec | Comments |
| --- | --- | --- | --- | --- |
| MO1 BAU Supporting | 5 MD | 5 MD | 5 MD | PROD issue / Env stability / Enhancement & Release |
| MO1 new tiles on boarding | 5 MD | 5 MD | 5 MD | Supporting new tiles on boarding activities (SSDR, CDUPS, VPA) |
| CES (EMS3) migration | 10 MD | 10 MD | 10 MD | Migrate EMS2 to CES |

| **Phase** | **Activity** | **Effort (MD)** | **Resource** | **Rationale/Notes** |
| --- | --- | --- | --- | --- |
| **0. Setup** | **Project Inception & Environment** | **10** | | |
| Architecture & Security Review | 5 | Me | InfoSec review is critical for desktop containers. |
| CI/CD Pipeline Setup for OpenFin | 5 | DevOps | Setup Pipelines for teamwork and ADO stages. |
| **1. Design** | **Design & Architecture** | **5** | | |
| Technical Design & FDC3 Strategy | 5 | Me | Defining FDC3 strategy of portal. |
| **2. Dev** | **Core Platform Foundation** | **15** | | |
| OpenFin Manifest Preparation | 5 | Me | Pushing & finalizing of portal installer selection, RVM upgrading strategy, license renewing. |
| Development | 10 | Me | 1. setup manifests for portal. 2. implement central fdc3 broker. 3. implement routing logics for intents in platform provider. 4. implement use case for trade ticket. |
| **4. QA** | **Quality Assurance & Hardening** | **25** | | |
| Acceptance Testing | 5 | QA | Integration testing with blade. |
| Full Regression Testing | 10 | QA | Manual execution of all existing cases. |
| Performance & Memory Profiling | 10 | QA | OpenFin can be memory-heavy; needs specific testing. |
| **5. UAT/Train** | **User Acceptance & Training** | **10** | | |
| User Training & Documentation | 5 | Me | guide users from none to installing to BAU. |
| PSS Training | 5 | Me | |
| **6. Release** | **Release & BAU** | **15** | | |
| Release Coordination & Deployment | 10 | DevOps | |
| BAU / Maintenance Handover | 5 | Me | |
| **TOTAL** | | **80** | **Me: 40MD** **QA: 25MD** **DevOps: 15MD** | With 10% buffer time: Total 89 MD Me: 44 MD QA: 28 MD DevOps: 17 MD |