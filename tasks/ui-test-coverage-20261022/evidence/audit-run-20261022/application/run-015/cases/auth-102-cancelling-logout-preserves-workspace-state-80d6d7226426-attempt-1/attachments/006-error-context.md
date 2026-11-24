# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-session-expanded.spec.ts >> AUTH-102 cancelling logout preserves workspace state
- Location: e2e/audit-specs/auth-session-expanded.spec.ts:227:1

# Error details

```
Test timeout of 30000ms exceeded.
```

# Page snapshot

```yaml
- generic [ref=e1]:
  - generic [ref=e4]:
    - generic [ref=e10]:
      - generic [ref=e11] [cursor=pointer]: New Tile
      - generic [ref=e19]:
        - text: dark
        - checkbox [ref=e22] [cursor=pointer]
      - group [ref=e26]:
        - generic [ref=e27]: 00:00 UTC
        - checkbox [checked] [ref=e30] [cursor=pointer]
      - button [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button [ref=e37] [cursor=pointer]
    - main [ref=e41]:
      - tablist [ref=e45]:
        - tab [selected] [ref=e47] [cursor=pointer]:
          - region [ref=e48]:
            - textbox [ref=e52]: WS-A
        - button [ref=e54] [cursor=pointer]
      - tabpanel [ref=e59]:
        - generic [ref=e63]:
          - paragraph [ref=e65]: Start customizing your workspace
          - paragraph [ref=e66]: find out what workspace preference options you have and how those options work.
          - button [ref=e67] [cursor=pointer]: Find tile
  - menu [ref=e74]:
    - menuitem [ref=e75] [cursor=pointer]:
      - paragraph [ref=e76]: Audit User A
      - generic [ref=e77]: Click to view user profile details
    - separator [ref=e78]
    - menuitem [ref=e79] [cursor=pointer]:
      - paragraph [ref=e80]: Logout
    - separator [ref=e81]
    - menuitem [ref=e82]:
      - generic [ref=e83]: "Root Config Version: PACKAGE_VERSION"
      - generic [ref=e84]: "Base Container Version: PACKAGE_VERSION"
  - dialog [ref=e87]:
    - heading "Leave Now?" [level=2] [ref=e88]
    - paragraph [ref=e90]:
      - text: To provide better service, please
      - button "Share Feedback" [ref=e91] [cursor=pointer]
    - generic [ref=e92]:
      - button "Share Feedback & Logout" [active] [ref=e93] [cursor=pointer]
      - button "Logout" [ref=e94] [cursor=pointer]
      - button "Cancel" [ref=e95] [cursor=pointer]
```