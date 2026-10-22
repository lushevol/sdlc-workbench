# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: admin-expanded.spec.ts >> UI-ADM-GRD-005 actual administration UI with step evidence
- Location: e2e/audit-specs/admin-expanded.spec.ts:15:3

# Error details

```
Test timeout of 30000ms exceeded.
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
      - generic [ref=e27]: 05:30 UTC
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
                - cell [ref=e114]: Fixture Category 101
                - cell [ref=e115]: TEST_OWNER
                - cell [ref=e116]
                - cell [ref=e119]:
                  - generic [ref=e120]: Oct 22, 2026, 12:05:00 AM
                - cell [ref=e121]: UI-ADMIN-01
                - cell [ref=e122]: "101"
                - cell [ref=e123]: "7"
              - row [ref=e125]:
                - cell [ref=e126]:
                  - menu [ref=e127]:
                    - menuitem [ref=e128] [cursor=pointer]
                    - menuitem [ref=e131] [cursor=pointer]
                    - menuitem [disabled]
                    - menuitem [ref=e134] [cursor=pointer]
                - cell [ref=e137]: Fixture Category 102
                - cell [ref=e138]: TEST_OWNER
                - cell [ref=e139]
                - cell [ref=e142]:
                  - generic [ref=e143]: Oct 22, 2026, 12:05:00 AM
                - cell [ref=e144]: UI-ADMIN-01
                - cell [ref=e145]: "102"
                - cell [ref=e146]: "7"
          - generic [ref=e150]:
            - paragraph [ref=e151]: "Rows per page:"
            - generic [ref=e152]:
              - combobox [ref=e153] [cursor=pointer]: "20"
              - textbox [aria-hidden]: "20"
            - paragraph [ref=e154]: 1–2 of 2
            - generic [ref=e155]:
              - button [disabled]
              - button [disabled]
        - dialog [ref=e158]:
          - heading [level=2] [ref=e159]:
            - generic [ref=e160]:
              - generic [ref=e161]: Audit
              - generic [ref=e162]:
                - button [ref=e163] [cursor=pointer]: Maximize
                - button [ref=e166] [cursor=pointer]:
                  - generic [ref=e167]: Close
          - grid [ref=e171]:
            - generic [ref=e172]:
              - rowgroup [ref=e173]:
                - row [ref=e174]:
                  - columnheader [ref=e175] [cursor=pointer]:
                    - generic [ref=e176]: Audit ID
                  - columnheader [ref=e178] [cursor=pointer]:
                    - generic [ref=e179]: Transaction Mode
                  - columnheader [ref=e181] [cursor=pointer]:
                    - generic [ref=e182]: Category ID
                  - columnheader [ref=e184] [cursor=pointer]:
                    - generic [ref=e185]: Category Label
                  - columnheader [ref=e187] [cursor=pointer]:
                    - generic [ref=e188]: Verified?
                  - columnheader [ref=e190] [cursor=pointer]:
                    - generic [ref=e191]: Created At
                  - columnheader [ref=e193] [cursor=pointer]:
                    - generic [ref=e194]: Created By
                  - columnheader [ref=e196] [cursor=pointer]:
                    - generic [ref=e197]: Updated At
                  - columnheader [ref=e199] [cursor=pointer]:
                    - generic [ref=e200]: Updated By
              - rowgroup [ref=e202]:
                - row [ref=e203]:
                  - cell [ref=e204]: "9001"
                  - cell [ref=e205]: maker
                  - cell [ref=e206]: "101"
                  - cell [ref=e207]: Fixture Category 101
                  - cell [ref=e208]
                  - cell [ref=e211]: Oct 21, 2026, 12:05:00 AM
                  - cell [ref=e212]: UI-ADMIN-01
                  - cell [ref=e213]: Oct 22, 2026, 12:05:00 AM
                  - cell [ref=e214]: UI-ADMIN-01
            - generic [ref=e217]:
              - paragraph [ref=e218]: "Rows per page:"
              - generic [ref=e219]:
                - combobox [ref=e220] [cursor=pointer]: "20"
                - textbox [aria-hidden]: "20"
              - paragraph [ref=e221]: 1–1 of 1
              - generic [ref=e222]:
                - button [disabled]
                - button [disabled]
          - button [ref=e223]
```