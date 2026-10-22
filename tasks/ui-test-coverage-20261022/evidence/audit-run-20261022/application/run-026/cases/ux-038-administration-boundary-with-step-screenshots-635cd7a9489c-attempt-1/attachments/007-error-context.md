# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-ux.spec.ts >> UX-038 administration boundary with step screenshots
- Location: e2e/audit-specs/admin-ux.spec.ts:12:3

# Error details

```
Test timeout of 30000ms exceeded.
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
        - generic [ref=e27]: 05:34 UTC
        - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
      - button "User Profiles" [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button "Share Feedback" [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist "workspaces" [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region "Category" [ref=e48]:
          - textbox "Workspace Name" [ref=e52]: Category
          - button "refresh" [ref=e53]
      - button "Add Workspace" [ref=e57] [cursor=pointer]
    - tabpanel [ref=e62]:
      - generic [ref=e65]:
        - button "Create New Category" [ref=e66] [cursor=pointer]
        - grid [ref=e68]:
          - button "Export" [ref=e70] [cursor=pointer]
          - generic [ref=e74]:
            - rowgroup [ref=e75]:
              - row [ref=e76]:
                - columnheader "Actions" [ref=e77]
                - columnheader "Category Label" [ref=e80] [cursor=pointer]
                - columnheader "Owner" [ref=e83] [cursor=pointer]
                - columnheader "Verified?" [ref=e86] [cursor=pointer]
                - columnheader "Updated At" [ref=e89] [cursor=pointer]
                - columnheader "Updated By" [ref=e92] [cursor=pointer]
                - columnheader "Record Id" [ref=e95] [cursor=pointer]
                - columnheader "Order No" [ref=e98] [cursor=pointer]
            - rowgroup [ref=e101]:
              - row [ref=e102]:
                - cell [ref=e103]:
                  - menu [ref=e104]:
                    - menuitem "Edit" [active] [ref=e105] [cursor=pointer]
                    - menuitem "Verify" [ref=e108] [cursor=pointer]
                    - menuitem "Deactivate" [disabled]
                    - menuitem "Audit" [ref=e111] [cursor=pointer]
                - cell "<script>alert(1)</script>" [ref=e114]
                - cell "TEST_OWNER" [ref=e115]
                - cell [ref=e116]
                - cell "Oct 22, 2026, 12:05:00 AM" [ref=e119]
                - cell "UI-ADMIN-01" [ref=e121]
                - cell "101" [ref=e122]
                - cell "7" [ref=e123]
          - generic [ref=e127]:
            - paragraph [ref=e128]: "Rows per page:"
            - generic [ref=e129]:
              - 'combobox "Rows per page: 20" [ref=e130] [cursor=pointer]': "20"
              - textbox [aria-hidden]: "20"
            - paragraph [ref=e131]: 1–1 of 1
            - generic [ref=e132]:
              - button "Go to previous page" [disabled]
              - button "Go to next page" [disabled]
```