| Updated by | Last Updated Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @SenJian Zou | 2026-07-20 | PO: @Arockia Dinesh Ops: @Prakash Gopi A/L Nayagam Gopi /@David George Thomas Dev: @Liam.Li @Long Wang PSS: @Zhen Shao @Zhenzhen Liu | 2026-07-21 | |

****Purpose****

---

This process defines the governance, ownership, and control requirements for situations where PSS is required to perform temporary technical recovery for tech failure exceptions in RATAN. The purpose is to ensure that such recovery remains strictly controlled, exceptional, and temporary, while permanent remediation is prioritized and delivered by Dev.

**Scope**

---

- Only strategic flow cashflows failed due to technical reasons will be following this process.
- BCS flow excluded, and process remain as it is for Ops team to replay(strategic solution is under discussion)
- Data issue and business exceptions excluded, the process remain unchanged as per Ops team's current BAU or MO to correct business data when required

**Exception-only principle**

---

Any technical recovery performed by PSS must be treated as a temporary and exceptional measure. It must not become part of the standard BAU operating model or a substitute for permanent technical remediation.

**Ownership and Responsibilities**

- Ownership must remain clearly separated as follows: - **PSS**: may execute temporary technical recovery only where this has been explicitly scoped, agreed and documented. - **Development**: owns root cause analysis, recovery design, permanent fix delivery, and automation. - **Ops**: validates replay or recovery outcome where business confirmation is required. This model is intended to preserve clear accountability and prevent temporary operational workarounds from becoming enduring support responsibilities.

**Risk awareness**

---

Where PSS is required to perform temporary technical recovery, the relevant Business Owner and/or Product Owner is fully aware of that this represents a temporary, risk-bearing workaround pending permanent remediation.

Email approval to be attached here:

**Recovery steps approval**

---

All temporary recovery steps must:

- be documented in Confluence
- be reviewed and approved by the relevant Product Owner before use
- be executed only in line with the approved procedure

Confluence reference: [RATAN - UR KB - How to reinstate FMRP cashflows - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+UR+KB+-+How+to+reinstate+FMRP+cashflows)

**Prioritization Rules for Permanent Fix**

---

Permanent fix prioritization should follow the rules below:

- If the issue results in a **P4 or higher incident(using the Impact Assessment Matrix)**, or the **same issue occurs twice within one week, **a root cause analysis must be completed, and a remediation plan (including estimated delivery date) must be presented to stakeholders by the end of the week, the fix must be targeted for the next available deployment window
- If manual replay or recovery is required **more than three times within one month**, a permanent fix must be prioritized for the next major release cycle.
- In all other cases, if PSS repeatedly performs the same technical recovery, the issue must be reclassified as **resilience / control debt and** prioritized within the development backlog based on its impact (using the Impact Assessment Matrix) and effort required, with a strong preference for addressing it before new low priority enhancements. Ownership of the resolution process (including identifying an automation solution) should be clearly assigned, development team for RCA and design, with PSS support for validation

**Review cadence**

---

All tracked technical recovery exceptions, together with the related permanent fix items, must be reviewed during the **KTLO prioritization call every two weeks**.

**Escalation path**
If the agreed target date for the permanent fix slips, the issue must be escalated to:  **Development Head / ****PSS Head / CPO**

**Tracking Mechanism**

---

Each technical failure exception that requires temporary PSS recovery must be tracked with the following minimum controls:

- an **ADO ticket**
- a named **Development owner**
- a committed **ETA for permanent fix**

This is to ensure that all temporary recoveries remain visible, governed, and actively tracked to closure.

**Expected End State**

---

The target end state is that recurring technical failure exceptions are addressed through permanent technical fixes or automation, such that PSS no longer needs to perform temporary technical recovery.

**Management Intention**
This process is intended to provide a controlled interim mechanism for service continuity while ensuring that recurring technical failures are resolved at source. It is not intended to transfer long-term technical recovery ownership to PSS.

---