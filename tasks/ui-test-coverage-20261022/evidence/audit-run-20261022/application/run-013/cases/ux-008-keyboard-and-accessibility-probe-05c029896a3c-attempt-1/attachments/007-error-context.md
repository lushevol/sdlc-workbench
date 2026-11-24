# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: ux-shell.spec.ts >> UX-008 keyboard and accessibility probe
- Location: e2e/audit-specs/ux-shell.spec.ts:39:3

# Error details

```
Error: page.evaluate: SyntaxError: Unexpected token 'l', "light" is not valid JSON
    at JSON.parse (<anonymous>)
    at eval (eval at evaluate (:370:30), <anonymous>:3:23)
    at UtilityScript.evaluate (<anonymous>:372:16)
    at UtilityScript.<anonymous> (<anonymous>:1:44)
```

# Page snapshot

```yaml
- generic [ref=e4]:
  - generic [ref=e7]:
    - img "Markets Operations One logo" [ref=e9]
    - generic [ref=e10]:
      - generic [ref=e11] [cursor=pointer]:
        - img "new tile" [ref=e13]
        - generic [ref=e14]: New Tile
      - generic [ref=e20]:
        - text: light
        - checkbox "Theme Switch" [checked] [active] [ref=e23] [cursor=pointer]
      - group [ref=e27]:
        - generic [ref=e28]: 05:19 UTC
        - checkbox "Time Switch" [checked] [ref=e31] [cursor=pointer]
      - button "User Profiles" [ref=e35] [cursor=pointer]:
        - generic [ref=e36]: A
      - button "Share Feedback" [ref=e38] [cursor=pointer]
  - main [ref=e42]:
    - tablist "workspaces" [ref=e46]:
      - tab [selected] [ref=e48] [cursor=pointer]:
        - region "Workspace 1" [ref=e49]:
          - textbox "Workspace Name" [ref=e53]: Workspace 1
      - button "Add Workspace" [ref=e55] [cursor=pointer]
    - tabpanel [ref=e60]:
      - generic [ref=e64]:
        - paragraph [ref=e66]: Start customizing your workspace
        - paragraph [ref=e67]: find out what workspace preference options you have and how those options work.
        - button [ref=e68] [cursor=pointer]
```