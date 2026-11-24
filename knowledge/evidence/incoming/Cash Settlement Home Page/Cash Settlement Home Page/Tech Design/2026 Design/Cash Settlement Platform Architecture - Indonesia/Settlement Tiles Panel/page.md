# Background

We have a better layout to avoid making OPS got a feeling so many duplicated tiles. Separate tiles required on below:

1. Settlement

1. 1. Cashflow Blotter 2. Group Blotter 3. Cashflow Dashboard

2. Business Rule

1. 1. Settlement NSTP Rules New 2. Suppression Rules [Swift] 3. Suppression Rules [Cashflow] 4. Authorization Limits

3. Static

1. 1. Netting Static 2. Nostro Static 3. BIC Netting Static 4. Nostro Threshold Static 5. Utilization Static

UX Figma Link: [Market Operation One UI/UX Design – Figma](https://www.figma.com/design/ez8biR6RJvb1Dy2bbIvkuN/Market-Operation-One-UI-UX-Design?node-id=1319-17&p=f&t=gjo0pLT4iozIe1Wb-0)

| **Tile** | **User** | **Entitlements** | **User View** | **User Behaviour** | **User Id** |
| --- | --- | --- | --- | --- | --- |
| Cashflow Blotter (Same pattern for all other tiles that contains ID and Global) | user-1 | Global | ![1.png](attachments/1.png) | Click the card or the icon only button to open the this tile | 1462616 |
| user-2 | Indonesia | ![2.png](attachments/2.png) | Click the card or the icon only button to open the this tile（the tile in the workspace tab will contain an ID flag to show It’s ID tile） | 1140336 |
| user-3 | Global & Indonesia | ![3.png](attachments/3.png) | Click the card or the global button to open the gobal cashflow blotter tile Click the Indonesia button to open the ID tile（the ID tile in the workspace tab will contain an ID flag to show It’s ID tile） | 1129381 |
| user-4 | - | Can’t see, can’t access | | |
| Trade Blotter (Same pattern for all other none region switch tiles) | user-5 | Global or Indonesia or Global & Indonesia | ![4.png](attachments/4.png) | Click the card or the icon only button to open the this tile | |

# Design

## Overall Diagram

## Detail

**Admin Module**

| UI Name | DB Name | Type | GDC Tile | ID Tile | Default Value | UI Example Snapshot |
| --- | --- | --- | --- | --- | --- | --- |
| Tile Name | title | Input | Cashflow Blotter | Cashflow Blotter | Required | |
| Group Blotter | Group Blotter |
| ...... | ...... |
| Suppression Rules | Suppression Rules |
| Description | subtitle | Input | [Swift] | [Swift] | "" | |
| **Filter Rule** | filter_rule | Input | { "filterType": "ems3", "parameters": { "appId": "51358", "appName": "RATAN_ENTITLEMENT_RULE" }, "expression": "!#root['Entity.Booking_Entity_SCI_FMID'].?[#this != '8'].isEmpty()" } | { "filterType": "ems3", "parameters": { "appId": "51358", "appName": "RATAN_ENTITLEMENT_RULE" }, "expression": "#root['Entity.Booking_Entity_SCI_FMID'].contains('8')" } | null | ![image-2026-9-2_17-56-43.png](attachments/image-2026-9-2_17-56-43.png) |
| **Entry Name** | entry_name | Input | Global | Indonesia | null | ![image-2026-9-2_17-57-17.png](attachments/image-2026-9-2_17-57-17.png) |

**Tiles Panel(mfe-base drawer component)**

****