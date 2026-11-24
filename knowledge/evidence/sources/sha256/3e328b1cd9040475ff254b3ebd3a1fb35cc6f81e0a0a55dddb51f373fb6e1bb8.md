# Background

If client hold account in SCB entity and they expect SCB could debit their account directly on behalf of them, currently MT202Flip will be generated for such scenario.

But for some cross border debit cases, client account is located with other SCB entities which is different from booking entity, the swift instruction is not allowed by the regulator.

This requirement is to generate ~~MT103 or~~ MT202 as an alternative way for the scenario which MT202Flip cannot cover with above reasons.

# Requirement Details

- New settlement account CCY CROSSDEBIT will be used for this case when create Vostro SI in SSI+
- ![](https://confluence.global.standardchartered.com/rest/gliffy/1.0/embeddedDiagrams/30d57e50-4c94-4b16-9ddc-5e940d0e4706.png?utm_medium=live&utm_source=confluence)
- For <u>receive</u> flow, if settlement account is in format “CCY CROSSDEBIT” (such as USD CROSSDEBIT), then generate message as below:

**MT202 CROSSDEBIT**: detailed mapping logic updated to [FMRP Swift Generation - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FMRP+Swift+Generation)

- MT103 CROSSDEBIT - exclude from the requirement
- No impact to accounting process
- Need to send the cross border debit feed to LMS

| Tag | Field Name | Mandatory | Proposed MT202 CROSSDEBIT SI mapping | Comment | current MT202Flip (for reference) |
| --- | --- | --- | --- | --- | --- |
| Block1 | Message sender | Y | Vostro SI 57BIC | | legal entity BIC |
| Block2 | Message receiver | Y | Vostro SI 57BIC | | Nostro agent BIC |
| 52 | Ordering Institution | Y | Vostro SI Bene detail (58) | - if BIC exists, generate 52A, - else generate 52D | Vostro SI Bene detail (58) |
| 53 | Sender's Correspondent | Y | bene Account in vostro (58) | 53B: (58 account number) | bene Account in vostro (58) |
| 57 | Account With Institution | Y | Nostro agent BIC (53) | 57A: (53 BIC) | Account with Institution BIC(57) |
| 58 | Beneficiary Institution | Y | Legal entity BIC(hardcode mapping from sender bic) | 58: account from nostro (optional) BIC from backend static for sender | Legal entity BIC(hardcode mapping from 58 static bic) |

**Mocked sample SI and swift**:

![image-2026-1-14_11-1-12.png](attachments/image-2026-1-14_11-1-12.png)![image-2026-1-14_11-1-54.png](attachments/image-2026-1-14_11-1-54.png)![image-2026-1-14_11-2-16.png](attachments/image-2026-1-14_11-2-16.png)

# Business Use Case

| | Function | Scenario | Expected Result |
| --- | --- | --- | --- |
| 1 | SCB receive cross debit cashflow generate MT202 and follow the cross debit mapping | | - swift generated with expected mapping - accounting generated follow as-is process - cashflow feed send to LMS |
| 2 | SCB pay cross debit cashflow follow normal MT103/MT202 mapping | | - swift generated with expected mapping - accounting generated follow as-is process - cashflow feed send to LMS |

# Open Questions

| | | Description | Comment | Evidence? | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | 2025-11-29 | New settlement account CCY CROSSDEBIT - can we use settlement means instead | 2025-12-04 proposal is using 'Nostro' as settlement means and use 'Settlement account' to control the cross debit 2025-12-15 if both settlement means = Over account and settlement account like %CROSSDEBIT matches, it will be considered as 202 Flip instead of Cross debit case ? 2026-01-12 check the cross debit firstly | 📎 [RE_ Requirement Clarification_ Cross Border Debit.msg](attachments/RE_ Requirement Clarification_ Cross Border Debit.msg) | |
| 2 | 2025-11-29 | tag 57 in MT202 Cross Debit need map nostro bic or 57 bic? | 2025-12-04 confirmed to use nostro bic | |
| 3 | 2025-11-29 | it was mentioned if nostro bic is same as vostro 57 bic , then GMO bic should be use, other wise legal entity bic to be use – is this confirmed? | 2025-12-04 GMO BIC is not required to be used, but Beneficiary BIC + account number to be quoted | |
| 4 | 2025-12-07 | Weng Hien proposed to stick with MT202, to be confirmed with Dinesh | 2026-01-12 only focus on MT202 | 📎 [RE_ RAZOR _ RATAN Enhancement Idea for Cross Border Debit.msg](attachments/RE_ RAZOR _ RATAN Enhancement Idea for Cross Border Debit.msg) | |
| 5 | 2025-12-07 | Weng Hien proposed to set extra info in field 72, to be confirmed with Dinesh | 2026-01-12 no extra logic required, rely on the SSI setup | |
| 6 | 2025-12-07 | Impact to LMS | | | |

# Tech Design