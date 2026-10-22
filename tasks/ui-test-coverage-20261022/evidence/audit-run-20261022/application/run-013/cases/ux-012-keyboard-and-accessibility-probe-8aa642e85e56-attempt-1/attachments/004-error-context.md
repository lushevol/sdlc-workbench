# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: ux-shell.spec.ts >> UX-012 keyboard and accessibility probe
- Location: e2e/audit-specs/ux-shell.spec.ts:39:3

# Error details

```
Test timeout of 30000ms exceeded.
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - generic [ref=e5]:
    - main [ref=e7]:
      - heading "Sign In" [level=3] [ref=e8]
      - generic [ref=e9]:
        - generic [ref=e10]:
          - generic [ref=e11]: Username
          - textbox "Enter Username" [ref=e17]
        - generic [ref=e18]:
          - generic [ref=e19]: Password
          - textbox "Enter Password" [ref=e25]
        - button "Sign In" [ref=e26] [cursor=pointer]
        - separator [ref=e27]
      - link "Sign In With SSO" [ref=e29] [cursor=pointer]:
        - /url: https://login.microsoftonline.com/cd823f6b-31c5-4241-b504-3707cbc03fb7/oauth2/v2.0/authorize?client_id=80c8b904-1b64-443b-a651-7548764d534d&response_type=code&redirect_uri=http://localhost:8128/mfa/callback&response_mode=query&scope=openid+profile+offline_access+email
    - main [ref=e31]:
      - tabpanel [ref=e32]:
        - generic [ref=e33]:
          - heading "Markets Operations One" [level=2] [ref=e34]
          - paragraph [ref=e35]: Markets Operations One Portal (MO1) is a single, evolving workspace for Operations processing, integrating post-trade applications, and progressively delivering a more connected, intelligent, and efficient processing.
      - tablist "login tabs" [ref=e39]:
        - tab "login-tabpanel" [selected] [ref=e40] [cursor=pointer]
  - alert [ref=e42]:
    - alert [ref=e47]:
      - generic [ref=e48]: Expired Session, please login again.
    - button "Close" [ref=e50] [cursor=pointer]
```