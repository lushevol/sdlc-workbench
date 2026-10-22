# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-ux.spec.ts >> UX-016 administration boundary with step screenshots
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
        - generic [ref=e27]: 05:40 UTC
        - checkbox "Time Switch" [checked] [ref=e30] [cursor=pointer]
      - button "User Profiles" [ref=e34] [cursor=pointer]:
        - generic [ref=e35]: A
      - button "Share Feedback" [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist "workspaces" [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region "Tile" [ref=e48]:
          - textbox "Workspace Name" [ref=e52]: Tile
      - button "Add Workspace" [ref=e54] [cursor=pointer]
    - tabpanel [ref=e59]:
      - generic [ref=e61]:
        - generic [ref=e62]:
          - generic [ref=e64]:
            - generic [ref=e65]: Application Category
            - generic [ref=e66]:
              - combobox "Application Category" [ref=e67]
              - button "Open" [ref=e69] [cursor=pointer]
          - button "refresh" [disabled]
        - generic [ref=e72]:
          - button "Create New Tile" [disabled]
          - grid [ref=e74]:
            - button "Export" [ref=e76] [cursor=pointer]
            - generic [ref=e80]:
              - rowgroup [ref=e81]:
                - row [ref=e82]:
                  - columnheader "Actions" [ref=e83]
                  - columnheader "Tile Name" [ref=e86] [cursor=pointer]
                  - columnheader "Description" [ref=e89] [cursor=pointer]
                  - columnheader "Image URL for Dark Theme" [ref=e92] [cursor=pointer]
                  - columnheader "Image URL for Light Theme" [ref=e95] [cursor=pointer]
                  - columnheader "Container" [ref=e98] [cursor=pointer]
                  - columnheader "Module Path" [ref=e101] [cursor=pointer]
                  - columnheader "Tile Path" [ref=e104] [cursor=pointer]
                  - columnheader "Role Subject" [ref=e107] [cursor=pointer]
                  - columnheader "Role Entities" [ref=e110] [cursor=pointer]
              - rowgroup [ref=e113]:
                - row [ref=e114]:
                  - cell [ref=e115]:
                    - menu [ref=e116]:
                      - menuitem "Edit" [ref=e117] [cursor=pointer]
                      - menuitem "Verify" [ref=e120] [cursor=pointer]
                      - menuitem "Deactivate" [disabled]
                      - menuitem "Audit" [ref=e123] [cursor=pointer]
                  - cell "Fixture Tile" [ref=e126]
                  - cell "Demo" [ref=e127]
                  - cell "darkIcons/icon01.svg" [ref=e128]
                  - cell "lightIcons/icon01.svg" [ref=e129]
                  - cell "@fm/test" [ref=e130]
                  - cell "/test" [ref=e131]
                  - cell "/test-entry" [ref=e132]
                  - cell "TEST_SUBJECT" [ref=e133]
                  - cell "TEST_ENTITY" [ref=e134]
            - generic [ref=e137]:
              - paragraph [ref=e138]: "Rows per page:"
              - generic [ref=e139]:
                - 'combobox "Rows per page: 20" [ref=e140] [cursor=pointer]': "20"
                - textbox [aria-hidden]: "20"
              - paragraph [ref=e141]: 1–1 of 1
              - generic [ref=e142]:
                - button "Go to previous page" [disabled]
                - button "Go to next page" [disabled]
```