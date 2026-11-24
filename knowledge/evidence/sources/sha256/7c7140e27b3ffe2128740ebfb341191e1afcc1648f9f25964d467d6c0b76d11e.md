| |
| --- |
| Target release | |
| Epic | [Story 8414445 [RATAN UI Form] Principles for UI form](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/8414445) |
| Document status | DRAFT |
| Document owner | |
| Designer | |
| Developers | |
| QA | |
| Changes | 2025-05-12 1. Draft |

# Background

Recently found issues:

1. Some UI form allow submitting action before whole page rendered
2. Validation does not take effect when mandatory fields disabled for editing
3. Validation takes effect only for frontend or backend, ideally both should apply same validation rules

# Principles

1. Action allowed only post form rendering completed
2. Both frontend and backend need validation on submitted UI form
3. UI form validation should take effect no matter fields enabled or disabled
4. Validation rules to be centrally maintained