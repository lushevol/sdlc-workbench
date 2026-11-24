# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-ux.spec.ts >> UX-058 administration boundary with step screenshots
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
        - generic [ref=e27]: 05:35 UTC
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
              - combobox "Application Category" [ref=e67]: Fixture Category
              - button "Open" [ref=e69] [cursor=pointer]
          - button "refresh" [ref=e72] [cursor=pointer]
        - generic [ref=e75]:
          - button "Create New Tile" [ref=e76] [cursor=pointer]
          - grid [ref=e78]:
            - button "Export" [ref=e80] [cursor=pointer]
            - generic [ref=e84]:
              - rowgroup [ref=e85]:
                - row [ref=e86]:
                  - columnheader "Actions" [ref=e87]
                  - columnheader "Tile Name" [ref=e90] [cursor=pointer]
                  - columnheader "Description" [ref=e93] [cursor=pointer]
                  - columnheader "Image URL for Dark Theme" [ref=e96] [cursor=pointer]
                  - columnheader "Image URL for Light Theme" [ref=e99] [cursor=pointer]
                  - columnheader "Container" [ref=e102] [cursor=pointer]
                  - columnheader "Module Path" [ref=e105] [cursor=pointer]
                  - columnheader "Tile Path" [ref=e108] [cursor=pointer]
                  - columnheader "Role Subject" [ref=e111] [cursor=pointer]
                  - columnheader "Role Entities" [ref=e114] [cursor=pointer]
              - rowgroup [ref=e117]:
                - row [ref=e118]:
                  - cell [ref=e119]:
                    - menu [ref=e120]:
                      - menuitem "Edit" [active] [ref=e121] [cursor=pointer]
                      - menuitem "Verify" [ref=e124] [cursor=pointer]
                      - menuitem "Deactivate" [disabled]
                      - menuitem "Audit" [ref=e127] [cursor=pointer]
                  - cell "ABC" [ref=e130]
                  - cell "Before" [ref=e131]
                  - cell "darkIcons/icon01.svg" [ref=e132]
                  - cell "lightIcons/icon01.svg" [ref=e133]
                  - cell "@fm/test" [ref=e134]
                  - cell "/test" [ref=e135]
                  - cell "/test-entry" [ref=e136]
                  - cell "TEST_SUBJECT" [ref=e137]
                  - cell "TEST_ENTITY" [ref=e138]
            - generic [ref=e141]:
              - paragraph [ref=e142]: "Rows per page:"
              - generic [ref=e143]:
                - 'combobox "Rows per page: 20" [ref=e144] [cursor=pointer]': "20"
                - textbox [aria-hidden]: "20"
              - paragraph [ref=e145]: 1–1 of 1
              - generic [ref=e146]:
                - button "Go to previous page" [disabled]
                - button "Go to next page" [disabled]
```