Backup of information from main page

| Entitlement role | Location | Branches | Comments |
| --- | --- | --- | --- |
| GBS | IN | All except PK , TZ , BD , LK | IN users are holding GBS profile access, able view all countries cashflow details. |
| GBS | KL | All including PK & Indonesia | KL users are holding GBS profile access, able view all countries cashflow details. |
| On shore | Any | Only specific country branch access based on the user domicile. | Eg : LK branch data can be accessed only by users in LK. Other country based users cannot view the same. |
| PSS / Dev | China | Read only access for All branches. | |
| PO | India | Read only access for All branches excluding PK | |
| PO | SG | Read only access for All branches including PK. | |
| On shore | Dubai | Read only access for Egypt and Saudi branches | |

| S.No | Entitlement role | Location | Test scenario | UAT Status | UAT Evidence. | Current PROD status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | GBS | IN | User able to view the cash flows in RATAN for London, DE, New York, Dubai branches. | | | able view those countries access, due to IN users are holding GBS profile access | ![image-2025-12-11_14-16-50.png](attachments/image-2025-12-11_14-16-50.png) 📎 [RE_ THING TO DO_ RATAN - Data entitlement test cases (1).msg](attachments/RE_ THING TO DO_ RATAN - Data entitlement test cases (1).msg) 📎 [RE_ THING TO DO_ RATAN - Data entitlement test cases.msg](attachments/RE_ THING TO DO_ RATAN - Data entitlement test cases.msg) 📎 [____Ratan Cash Flow___.msg](attachments/____Ratan Cash Flow___.msg) |
| 2 | GBS | IN | User able to view the cash flows in RATAN for Mauritius, Bahrain , Qatar, South Africa branches. | | | able view those countries access, due to IN users are holding GBS profile access |
| 3 | GBS | IN | User able to view the cash flows in RATAN for Botswana, Kenya, Zambia, Uganda branches. | | | able view those countries access, due to IN users are holding GBS profile access |
| 4 | GBS | IN | User able to view the cash flows in RATAN for Ghana ,Nigeria, Iraq ,Oman branches. | | | PASSED - able view those countries access, due to IN users are holding GBS profile access |
| 5 | GBS | IN | User able to view the cash flows in RATAN for Japan, India, Philippines, Thailand branches. | | | able view those countries access, due to IN users are holding GBS profile access |
| 6 | GBS | IN | User able to view the cash flows in RATAN for SG, Malaysia, Taiwan, branches. | | | able view those countries access, due to IN users are holding GBS profile access |
| 7 | GBS | IN | User able to view the cash flows in RATAN for Hong Kong branch. | | | able view those countries access, due to IN users are holding GBS profile access |
| 8 | GBS | IN | User able to view the cash flow data in RATAN for China - Shanghai , Shenzhen, Guangzhou branches. | | | able view those countries access, due to IN users are holding GBS profile access |
| 9 | GBS | IN | IN user should not be able to view cash flows for PK , Tanzania , Bangladesh & Sri Lanka branch. | | | due to able view those countries access, due to IN users are holding GBS access |
| 10 | GBS | IN | IN users to be able to view cash flows for Saudi & Egypt branch. | | | able view those countries access, due to IN users are holding GBS profile access |
| | GBS | IN | BCS - IN to view | | | | |
| 11 | GBS | KL | User able to view the cash flows in RATAN for London, DE, New York, Dubai branches. | | | able view those countries access, due to KL users are holding GBS profile access | Users Ratan profile downloaded from OneCert 📎 [Ratan entitlement profile_GBS KL.xlsx](attachments/Ratan entitlement profile_GBS KL.xlsx) Profile RATAN ID access existed in MyIT. ![image-2025-12-11_14-23-36.png](attachments/image-2025-12-11_14-23-36.png) ![image-2025-12-11_14-24-37.png](attachments/image-2025-12-11_14-24-37.png) Ratan blotter access 📎 [Ratan Blotter access 1.docx](attachments/Ratan Blotter access 1.docx) 📎 [Ratan Blotter access 2.docx](attachments/Ratan Blotter access 2.docx) |
| 12 | GBS | KL | User able to view the cash flows in RATAN for Mauritius, Bahrain , Qatar, South Africa branches. | | | able view those countries access, due to KL users are holding GBS profile access |
| 13 | GBS | KL | User able to view the cash flows in RATAN for Botswana, Kenya, Zambia, Uganda branches. | | | able view those countries access, due to KL users are holding GBS profile access |
| 14 | GBS | KL | User able to view the cash flows in RATAN for Ghana ,Nigeria, Iraq ,Oman branches. | | | able view those countries access, due to KL users are holding GBS profile access |
| 15 | GBS | KL | User able to view the cash flows in RATAN for Japan, India, Philippines, Thailand branches. | | | able view those countries access, due to KL users are holding GBS profile access |
| 16 | GBS | KL | User able to view the cash flows in RATAN for SG, Malaysia, Taiwan, branches. | | | able view those countries access, due to KL users are holding GBS profile access |
| 17 | GBS | KL | User able to view the cash flows in RATAN for Hong Kong branch. | | | able view those countries access, due to KL users are holding GBS profile access |
| 18 | GBS | KL | User able to view the cash flow data in RATAN for China - Shanghai , Shenzhen, Guangzhou branches | | | able view those countries access, due to KL users are holding GBS profile access |
| 19 | GBS | KL | User able to view the cash flows in RATAN for Indonesia branch. | | | able view those countries access, due to KL users are holding GBS profile access |
| 20 | GBS | KL | User able to view the cash flows in RATAN for Pakistan branch. | | | able view those countries access, due to KL users are holding GBS profile access |
| 21 | GBS | KL | KL user should not be able to view cash flows for Tanzania , Bangladesh & Sri Lanka branch. | | | able view those countries access, due to KL users are holding GBS profile access |
| | GBS | KL | User to view BCS blotter. | | | | |
| 22 | On shore | LK | User able to view the cash flow details in RATAN for Sri Lanka branch. | | | | |
| 23 | On shore | NP | User able to view the cash flow details in RATAN for Nepal branch. | | | | |
| 24 | On shore | TZ | User able to view the cash flow details in RATAN for Tanzania branch. | | | | |
| 25 | On shore | BD | User able to view the cash flow details in RATAN for Bangladesh branch. | | | | |
| 26 | On Shore | ID | ID user should be unable to view any data in BCS blotter. | | | | |
| 27 | On Shore | ID | ID user should be able to view only ID data and not other country data. | | | | |
| 28 | GBS | IN & KL | Trade blotter - data in cash flow schedule tile should be viewed by MO user. | | | | |
| 29 | GBS | IN | SSDR - no PK , LK , NP, BD, TZ | | | | |
| 30 | GBS | KL | SSDR - All except BD, NP, and TZ | | | | |
| 31 | On Shore | | SSDR - BD , NP , TZ, LK data to view | | | | |
| 32 | Dev / PSS - Read only | China | Dev & PSS users to be able to view cash flows in RATAN for all branches. | | | | |
| 33 | PO - Read only | India | IN PO users to be able to view data in RATAN for all branches except Pakistan branch. | | | | |
| 34 | PO - Read only | SG | Global PO users to be able to view cash flow information in RATAN for all branches. | | | | |
| 35 | On shore - Read only | Dubai | On shore users to view the data for Egypt and Saudi branches. | | | | |
| 36 | On shore | France, AU | Users should not be able to view any data in RATAN due to their domicile. | | | | |