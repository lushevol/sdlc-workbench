# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-expanded.spec.ts >> UI-ADM-FLD-004 actual administration UI with step evidence
- Location: e2e/audit-specs/admin-expanded.spec.ts:15:3

# Error details

```
Error: browserContext._wrapApiCall: file data stream has unexpected number of bytes
```

# Page snapshot

```yaml
- generic [ref=e4]:
  - generic [ref=e10]:
    - generic [ref=e11] [cursor=pointer]: New Tile
    - generic [ref=e19]:
      - text: dark
      - checkbox [ref=e22] [cursor=pointer]
    - group [ref=e26]:
      - generic [ref=e27]: 05:29 UTC
      - checkbox [checked] [ref=e30] [cursor=pointer]
    - button [ref=e34] [cursor=pointer]:
      - generic [ref=e35]: A
    - button [ref=e37] [cursor=pointer]
  - main [ref=e41]:
    - tablist [ref=e45]:
      - tab [selected] [ref=e47] [cursor=pointer]:
        - region [ref=e48]:
          - textbox [ref=e52]: Category
          - button [ref=e53]
      - button [ref=e57] [cursor=pointer]
    - tabpanel [ref=e62]:
      - generic [ref=e65]:
        - button [ref=e66] [cursor=pointer]: Create New Category
        - generic [ref=e67]:
          - grid [ref=e68]:
            - button [ref=e70] [cursor=pointer]: Export
            - generic [ref=e74]:
              - rowgroup [ref=e75]:
                - row [ref=e76]:
                  - columnheader [ref=e77]:
                    - generic [ref=e78]: Actions
                  - columnheader [ref=e80] [cursor=pointer]:
                    - generic [ref=e81]: Category Label
                  - columnheader [ref=e83] [cursor=pointer]:
                    - generic [ref=e84]: Owner
                  - columnheader [ref=e86] [cursor=pointer]:
                    - generic [ref=e87]: Verified?
                  - columnheader [ref=e89] [cursor=pointer]:
                    - generic [ref=e90]: Updated At
                  - columnheader [ref=e92] [cursor=pointer]:
                    - generic [ref=e93]: Updated By
                  - columnheader [ref=e95] [cursor=pointer]:
                    - generic [ref=e96]: Record Id
                  - columnheader [ref=e98] [cursor=pointer]:
                    - generic [ref=e99]: Order No
              - rowgroup [ref=e101]:
                - row [ref=e102]:
                  - cell [ref=e103]:
                    - menu [ref=e104]:
                      - menuitem [ref=e105] [cursor=pointer]
                      - menuitem [ref=e108] [cursor=pointer]
                      - menuitem [disabled]
                      - menuitem [ref=e111] [cursor=pointer]
                  - cell [ref=e114]: Fixture Category
                  - cell [ref=e115]: TEST_OWNER
                  - cell [ref=e116]
                  - cell [ref=e119]:
                    - generic [ref=e120]: Oct 22, 2026, 12:05:00 AM
                  - cell [ref=e121]: UI-ADMIN-01
                  - cell [ref=e122]: "101"
                  - cell [ref=e123]: "7"
            - generic [ref=e127]:
              - paragraph [ref=e128]: "Rows per page:"
              - generic [ref=e129]:
                - combobox [ref=e130] [cursor=pointer]: "20"
                - textbox [aria-hidden]: "20"
              - paragraph [ref=e131]: 1–1 of 1
              - generic [ref=e132]:
                - button [disabled]
                - button [disabled]
          - dialog [ref=e135]:
            - heading [level=2] [ref=e136]:
              - generic [ref=e137]:
                - generic [ref=e138]: "edit ID: 101"
                - generic [ref=e139]:
                  - button [ref=e140] [cursor=pointer]: Maximize
                  - button [disabled]:
                    - generic: Close
            - generic [ref=e145]:
              - generic [ref=e146]:
                - generic [ref=e147]: Category Label
                - textbox [ref=e149]:
                  - /placeholder: Type here
                  - text: Fixture Category
              - generic [ref=e150]:
                - generic [ref=e151]: Owner
                - textbox [ref=e153]:
                  - /placeholder: Type here
                  - text: TEST_OWNER
              - generic [ref=e154]:
                - generic [ref=e155]: Verified?
                - textbox [disabled] [ref=e157]:
                  - /placeholder: Type here
                  - text: "false"
              - generic [ref=e158]:
                - generic [ref=e159]: Created At
                - textbox [disabled] [ref=e161]:
                  - /placeholder: Type here
                  - text: 2026-10-21T00:05:00Z
              - generic [ref=e162]:
                - generic [ref=e163]: Created By
                - textbox [disabled] [ref=e165]:
                  - /placeholder: Type here
                  - text: UI-ADMIN-01
              - generic [ref=e166]:
                - generic [ref=e167]: Updated At
                - textbox [disabled] [ref=e169]:
                  - /placeholder: Type here
                  - text: 2026-10-22T00:05:00Z
              - generic [ref=e170]:
                - generic [ref=e171]: Updated By
                - textbox [disabled] [ref=e173]:
                  - /placeholder: Type here
                  - text: UI-ADMIN-01
              - generic [ref=e174]:
                - generic [ref=e175]: Record Id
                - textbox [disabled] [ref=e177]:
                  - /placeholder: <<will be auto generated>>
                  - text: "101"
              - generic [ref=e178]:
                - generic [ref=e179]: Order No
                - spinbutton [ref=e181]: "7"
            - generic [ref=e182]:
              - button [ref=e183] [cursor=pointer]: Update
              - button [ref=e184] [cursor=pointer]: Reset
              - button [ref=e185] [cursor=pointer]: Close
            - button [ref=e186]
```