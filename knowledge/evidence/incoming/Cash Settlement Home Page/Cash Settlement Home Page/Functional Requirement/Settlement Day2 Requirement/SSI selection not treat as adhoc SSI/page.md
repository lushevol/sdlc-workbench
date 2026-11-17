# Background

SWIFT generation follows different logic for auto‑stamped SI versus manually entered SSI in some scenarios . Users expect SSI selection to follow the same process as auto‑stamped SI.

Additionally, the SSI+ team reviews “unused” SSI and performs data cleanup; any SSI ID not stored in RATAN is treated as unused.

We also highlight 70/72 updates because:

- In some cases, 70/72 carries payment‑specific details (e.g., invoice numbers) while the SSI itself remains unchanged.
- More importantly, a single account can be shared by multiple funds. For example, the beneficiary may be Citibank SG, and field 70/72 must specify the ultimate beneficiary (e.g., “Prudential Life Amundi Fund,” “Prudential Life Emerging Fund”).

Accurate 70/72 content is therefore critical to avoid payment failure.

# ADO

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13438079](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/13438079)

# Requirement Details

### AS-IS:

- system auto stamped SI: SSI Id is populated
- user manually enter vostro SI: SSI Id is blank
- *user select from available SI: SSI Id is blank regardless of whether any values are changed. *
- *user approve the cashflow when vostro SSI is in edit mode, SSI id is blank*
- *the process related to 70/72 updates：70/72 field value are not part of dual-blind validation*

### TO BE

- User select from available SI and submit without any changes: system set the SSI Id value with the selected SI Id.
- User select from available SI, - update only 70/72 values, - system will keep the SSI Id - Add text box (refer to mocked UI) - only highlight 70/72 update when SSI id exist and user updated 70/72; if no SSI ID, no need to highlight 70/72 changes. - In this scenario, the page shows that the SSI ID is empty, while the Reference ID displays the corresponding SSI ID value - update values other than 70/72 fields, system will remove the SSI Id
- User select from available SI, update any field, then manually update back to original values, remove SSI id as user manually updated the SI, even the value is the same as original
- if maker select from available SI, checker manually input the same value, system will consider this as different input and popup validation error
- if maker select SSI, checker will not see the SSI Id maker selected
- user approve the cashflow when vostro SI in edit mode, SSI id should not be impacted if user does not update SI

### UI Change

![image-2026-5-20_14-35-38.png](attachments/image-2026-5-20_14-35-38.png)

After adding reference id, it will be like

![image-2026-7-30_11-40-58.png](attachments/image-2026-7-30_11-40-58.png)

### Business Use Case

| | Scenarios | UI Snapshot |
| --- | --- | --- |
| 1 | Auto Stamped SI, SSI Id is populated | ![image-2026-7-8_14-27-22.png](attachments/image-2026-7-8_14-27-22.png) ![image-2026-7-8_14-31-48.png](attachments/image-2026-7-8_14-31-48.png) |
| 2 | Auto stamped SI, user manually update any value other than 70/72, SSI Id is blank | ![image-2026-7-8_14-32-43.png](attachments/image-2026-7-8_14-32-43.png) |
| 3 | Auto stamped SI, user manually update 70/72, SSI Id is populated,70/72 customized tag show up in cashflow details After adding reference id, the Reference ID displays the corresponding SSI ID value. | Before: ![image-2026-6-10_16-5-14.png](attachments/image-2026-6-10_16-5-14.png) After adding reference id: ![image-2026-7-30_11-44-31.png](attachments/image-2026-7-30_11-44-31.png) |
| 4 | Auto stamped SI, user manually update any value other than 70/72, and update it back to original value, SSI Id is blank if user manually select the SI again, the SSI Id is populated | ![image-2026-7-8_14-34-35.png](attachments/image-2026-7-8_14-34-35.png) ![image-2026-7-8_14-35-13.png](attachments/image-2026-7-8_14-35-13.png) |
| 5 | Auto stamped SI, user select SI without any update and submit, SSI Id is populated | |
| 6 | Auto stamped SI, user select SI and update 70/72, SSI Id is populated, 70/72 customized tag show up in cashflow details After adding reference id, the Reference ID displays the corresponding SSI ID value. | Before: ![image-2026-7-8_14-37-30.png](attachments/image-2026-7-8_14-37-30.png) ![image-2026-7-8_14-37-57.png](attachments/image-2026-7-8_14-37-57.png) After adding reference id: ![image-2026-7-30_11-49-5.png](attachments/image-2026-7-30_11-49-5.png) ![image-2026-7-30_11-49-45.png](attachments/image-2026-7-30_11-49-45.png) |
| 7 | Auto stamped SI, user select SI, update any field other than 70/72 and submit, SSI Id is blank | ![image-2026-7-8_14-35-13.png](attachments/image-2026-7-8_14-35-13.png) ![image-2026-7-8_14-32-43.png](attachments/image-2026-7-8_14-32-43.png) |
| 8 | Auto stamped SI, user select SI, update any field other than 70/72, then update back to the original value, SSI Id is blank if user manually select the SI again, the SSI Id is populated | |
| 9 | Auto stamped SI, user select SI, update any 70/72 field and submit， SSI Id is populated After adding reference id and processing the same steps above, 'Reference ID' displays the corresponding SSI ID value. | |
| 10 | no SSI stamped, user manually enter values, SSI Id is blank | |
| 11 | no SSI stamped, user select SI without any update and submit, SSI Id is populated | |
| 12 | no SSI stamped, user select SI, update 70/72 field, SSI Id is populated, 70/72 customized tag show up in cashflow details After adding reference id, processing the same steps above, 'Reference ID' displays the corresponding SSI ID value. | |
| 13 | no SSI stamped,, user select SI, update any field other than 70/72 and submit, SSI Id is blank | |
| 14 | no SSI stamped, user select SI, update any field other than 70/72, then update back to the original value, SSI Id is blank if user manually select the SI again, the SSI Id is populated | |
| 15 | if maker select from available SI, checker manually input the same value and click approve, system will populate validation error | |
| 16 | If the maker selects from the available SI and modifies field 7072 then tag should highlight and SSID populate. Checker opens the dialog, the 7072 highlight tag will be displayed and field 7072 will be auto-populated in the UI, while the SSID should not auto populated. After adding reference id, processing the same steps above, 'Reference ID' displays the corresponding SSI ID value. When checker opens the dialog, the 7072 highlight tag will be displayed and field 7072 will be auto-populated in the UI, while the SSID should not auto populated and don't show 'Reference ID'. | ![image-2026-6-22_15-57-24.png](attachments/image-2026-6-22_15-57-24.png) After adding reference id: ![image-2026-7-30_12-6-16.png](attachments/image-2026-7-30_12-6-16.png) |
| 17 | Auto stamped SI,If the maker selects from the available SI and modifies field 7072 Checker opens the dialog, the 7072 highlight tag will be displayed and field 7072 will be auto-populated in the UI, while the SSID will populate stamped SSI ID. After adding reference id, processing the same steps above, when checker opens the dialog, the 7072 highlight tag will be displayed and field 7072 will be auto-populated in the UI, while 'Reference ID' displays the stamped SSI ID. | After adding reference id Auto stamped SSI: ![image-2026-7-30_12-19-17.png](attachments/image-2026-7-30_12-19-17.png) Maker selects a candidate SSI and modify 70/72 field ![image-2026-7-30_12-19-53.png](attachments/image-2026-7-30_12-19-53.png) ![image-2026-7-30_12-20-11.png](attachments/image-2026-7-30_12-20-11.png) Checker opens the dialog ![image-2026-7-30_12-22-4.png](attachments/image-2026-7-30_12-22-4.png) ![image-2026-7-30_12-22-24.png](attachments/image-2026-7-30_12-22-24.png) |
| 18 | ~~If checker approve existing Cashflow which pending manual Adhoc SSI, then except to be successfully once all information matched. ~~ | |
| 19 | When the user selects SSI data, input new 7072 field and re-enters field 7072 with the value matching SSI data, field 7072 remains highlighted after the update. After adding reference id, processing the same steps above, field 7072 remains highlighted after the update, while 'Reference ID' displays the stamped SSI ID. | Step1: choose SSI with 7072 field blank. ![image-2026-7-2_14-9-8.png](attachments/image-2026-7-2_14-9-8.png) ![image-2026-7-2_14-9-33.png](attachments/image-2026-7-2_14-9-33.png) Step2: update 7072 field with highlight ![image-2026-7-2_14-10-59.png](attachments/image-2026-7-2_14-10-59.png) ![image-2026-7-2_14-11-15.png](attachments/image-2026-7-2_14-11-15.png) Step3:Remove 7072 field and keep same as SSI details with blank. Still highlight as it has been changed before. ![image-2026-7-2_14-10-59.png](attachments/image-2026-7-2_14-10-59.png) ![image-2026-7-2_14-12-26.png](attachments/image-2026-7-2_14-12-26.png) After adding reference id Step1: choose SSI with 7072 field blank. ![image-2026-7-30_12-27-19.png](attachments/image-2026-7-30_12-27-19.png) ![image-2026-7-30_12-27-33.png](attachments/image-2026-7-30_12-27-33.png) Step2: update 7072 field with highlight ![image-2026-7-30_12-28-7.png](attachments/image-2026-7-30_12-28-7.png) ![image-2026-7-30_12-28-28.png](attachments/image-2026-7-30_12-28-28.png) Step3:Remove 7072 field and keep same as SSI details with blank. Still highlight as it has been changed before. ![image-2026-7-30_12-27-19.png](attachments/image-2026-7-30_12-27-19.png) ![image-2026-7-30_12-27-33.png](attachments/image-2026-7-30_12-27-33.png) |
| 20 | Auto Stamped SI, maker only update 58a address only then ssid should be removed. After submit, checker open will show the stamped ssid by system and 58a address will auto populate as is, in this case checker didn't change anything. Auto stamped SSID should be blank. After adding reference id, processing the same steps above, when checker opens the dialog, it will show the stamped ssid by system and 58a address will auto populate as is, in this case checker didn't change anything. Auto stamped SSID should be blank and don't show 'Reference ID'. | Before ![image-2026-7-6_16-28-4.png](attachments/image-2026-7-6_16-28-4.png) After adding reference id ![image-2026-7-30_12-36-33.png](attachments/image-2026-7-30_12-36-33.png) |