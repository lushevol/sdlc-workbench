# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: preferences.spec.ts >> UI-PREF-004 time display uses the selected clock mode
- Location: e2e/audit-specs/preferences.spec.ts:45:3

# Error details

```
Error: clock.pauseAt: Error: Cannot fast-forward to the past
    at ClockController._innerFastForwardTo (<anonymous>:202:13)
    at ClockController.pauseAt (<anonymous>:133:16)
    at async <anonymous>:396:30
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
      - generic [ref=e15]:
        - img "dark" [ref=e17]
        - generic [ref=e19]:
          - text: dark
          - checkbox "Theme Switch" [ref=e22] [cursor=pointer]
      - group [ref=e26]:
        - generic [ref=e27]: 00:05 UTC
        - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
      - button "User Profiles" [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button "Share Feedback" [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist "workspaces" [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region "Workspace 1" [ref=e48]:
          - textbox "Workspace Name" [ref=e52]: Workspace 1
      - button "Add Workspace" [ref=e54] [cursor=pointer]
    - tabpanel [ref=e59]
```