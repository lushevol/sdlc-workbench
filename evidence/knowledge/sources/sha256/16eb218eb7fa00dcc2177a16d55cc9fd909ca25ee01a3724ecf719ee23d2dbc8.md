#

# User Access

RATAN user with profile FMO_STA_CKR/FMO_STA_MKR is able to add/delete/update in BIC Netting Static Tile.

[How to apply for RATAN ONE access - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/How+to+apply+for+RATAN+ONE+access)

# BIC Netting Static Tile

BIC Netting Static tile is under Static - BIC Netting Static

![image2024-8-30_17-13-29.png](attachments/image2024-8-30_17-13-29.png)

# Add BIC Netting Static

Go to Create button on the left top, fill in details according to requirement from settlement operation team.

Need to avoid blank in front or end of the value.

![image2024-8-30_10-53-50.png](attachments/image2024-8-30_10-53-50.png)

![image2024-8-30_10-54-59.png](attachments/image2024-8-30_10-54-59.png)![image2024-8-30_10-56-57.png](attachments/image2024-8-30_10-56-57.png)

Then Checker can refresh the page and find the new added record.

![image2024-8-30_10-58-9.png](attachments/image2024-8-30_10-58-9.png)

![image2024-8-30_10-58-33.png](attachments/image2024-8-30_10-58-33.png)

# Update BIC Netting Static

For existing record, maker can update it with double click or right click.

![image2024-8-30_11-0-7.png](attachments/image2024-8-30_11-0-7.png)

After maker save the update, checker can either approve or reject the update with double click or right click.

![image2024-9-4_10-31-4.png](attachments/image2024-9-4_10-31-4.png)

![image2024-9-4_10-32-7.png](attachments/image2024-9-4_10-32-7.png)

# Delete BIC Netting Static

For save_confirmed record, maker can delete it.

![image2024-8-30_11-0-4.png](attachments/image2024-8-30_11-0-4.png)

# Bulk Approve/Reject/Delete

Maker can select multi records to delete in batch for save_confirmed data.

![image2024-9-4_10-33-54.png](attachments/image2024-9-4_10-33-54.png)

Checker can select multi records to Approve/reject in batch after verifying details.

![image2024-9-4_10-35-15.png](attachments/image2024-9-4_10-35-15.png)

# Static Data Status List

| | Status | Comment |
| --- | --- | --- |
| 1 | ADD_PENDING | Maker added static record |
| 2 | UPDATE_PENDING | Maker updated static record |
| 3 | DELETE_PENDING | Maker deleted static record |
| 4 | SAVE_CONFIRMED | Checker approved adding/updating static record, which will take effect. Checker rejected updating static record, original version of the static will take effect. |
| 5 | DELETE_CONFIRMED | Checker approved deleting static record. Record can be seen in audit only, which not be shown in static list. |
| 6 | DISCARDED | Checker rejected adding static record, record will be discarded, and not take effect. |

For data extraction, please click on all the pages, then extract data.