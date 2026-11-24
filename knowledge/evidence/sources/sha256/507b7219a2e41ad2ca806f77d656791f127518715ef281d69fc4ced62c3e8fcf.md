# Background

Microsoft Entra is the bank approved IDP solutions that help secure access to everything for everyone by providing identity governance, access management, and identity protection. Application integration in Microsoft Entra involves connecting various applications to Microsoft Entra services, such as Azure Active Directory (Azure AD), to enable secure single sign-on (SSO) and MFA.

# Prerequisites

- [x] ITAM App Instance ID (51358)
- [ ] Onboard ADO

# Adoption

## Technical solution

Microsoft recommends to use <u>[MSAL library](https://learn.microsoft.com/en-us/entra/identity-platform/sample-v2-code?tabs=apptype)</u> to require tokens, which is available for Java spring and front end app.