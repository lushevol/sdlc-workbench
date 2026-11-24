| fmid | country | Hot Data(Production Database) 6 months | Warm Data(Archival Database) 6 months - 5 Years | Cold Data(Offline) 5 Years - Country Retention Schedule | Purged | | |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 400001378 | CN | | | | | | |
| 10020899 | CN | | | | | | |
| 235003861 | CN | | | | | | |
| 10078716 | CN | | | | | | |
| 10036642 | CN | | | | | | |
| 10062461 | CN | | | | | | |
| 10032025 | CN | | | | | | |
| 400054708 | CN | | | | | | |
| 400054737 | CN | | | | | | |
| 400054741 | CN | | | | | | |
| 400057714 | CN | | | | | | |
| 400075752 | CN | | | | | | |
| 400085753 | CN | | | | | | |
| 400090093 | CN | | | | | | |
| 400095464 | CN | | | | | | |
| 400130180 | CN | | | | | | |
| 400130178 | CN | | | | | | |
| 400185419 | CN | | | | | | |
| 400193370 | CN | | | | | | |
| 400209000 | CN | | | | | | |
| 400218197 | CN | | | | | | |
| 400220273 | CN | | | | | | |
| 400229749 | CN | | | | | | |
| 400516443 | CN | | | | | | |
| 400516442 | CN | | | | | | |
| 400667486 | CN | | | | | | |
| 400677737 | CN | | | | | | |
| 400683682 | CN | | | | | | |
| 400798477 | CN | | | | | | |
| 400899993 | CN | | | | | | |
| 401053411 | CN | | | | | | |
| 10038345 | TW | | | | | | |
| 300011345 | TW | | | | | | |
| 300075472 | HK | | | | | | |
| 2 | HK | | | | | | |
| 300036368 | SG | | | | | | |
| 3 | SG | | | | | | |
| 400452428 | SG | | | | | | |
| 400451508 | SG | | | | | | |
| 9 | MY | | | | | | |
| 400093619 | MY | | | | | | |
| 4 | IN | | | | | | |
| 400960089 | IN | | | | | | |
| 5 | AE | | | | | | |
| 400045551 | AE | | | | | | |
| 400906330 | DE | | | | | | |
| 400041070 | GB | | | | | | |
| 10075222 | GB | | | | | | |
| 6 | TH | | | | | | |
| 400018439 | MU | | | | | | |
| 8 | ID | | | | | | |
| 10036428 | PH | | | | | | |
| 10036382 | JP | | | | | | |
| 400032489 | ZA | | | | | | |
| 7 | US | | | | | | |
| 300089409 | PH | | | | | | |
| 400007847 | NP | | | | | | |
| 400991880 | SA | | | | | | |
| 401036553 | EG | | | | | | |
| 400910415 | JE | | | | | | |
| 10036430 | | | | | | Bahrain | BAHRAIN |
| 10036775 | | | | | | Botswana | BOTSWANA |
| 300011525 | | | | | | Kenya | KENYA |
| 10041903 | | | | | | Zambia | ZAMBIA |
| 10041902 | | | | | | Uganda | UGANDA |
| 10040387 | | | | | | Tanzania | TANZANIA |
| 10037477 | | | | | | Ghana | GHANA |
| 300084297 | | | | | | Nigeria | NIGERIA |
| 10036647 | | | | | | Sri Lanka | 1.SRI LANKA |
| 10022098 | | | | | | 2.FCBUSLANKA |
| 10041530 | | | | | | Vietnam | HANOI |
| 10036655 | | | | | | Pakistan | KARACHI |
| 300011470 | | | | | | Bangladesh | DHAKA |
| 400058959 | | | | | | Hong Kong | 2.HKGCT |
| 400107029 | | | | | | UK | FINVENTURE |
| 401037180 | | | | | | Luxembourg | SARAH_UK |
| 400327728 | | | | | | Singapore | 1.PFK_SCPESG |
| 400568282 | | | | | | Singapore | 2.SCREALESTA |
| 400931959 | | | | | | Hong Kong | SC NEA |
| 300010782 | | | | | | Qatar | 1.DOHA |
| 401081696 | | | | | | SLATE_QFC |
| 400011581 | | | | | | Cote D'lvoire | COTEDIVOIR |
| 400991880 | | | | | | Saudi Arabia | SAUDI |
| 400625349 | | | | | | Iraq | IRAQ |
| 300010730 | | | | | | Oman | OMAN |
| 400013557 | | | | | | UK | SCBPLC |
| 400044944 | | | | | | UK | GCT |

| Questions | Answer |
| --- | --- |
| What is hot data duration for each countries? | |
| What is warm data duration for each countries? | |
| What is cold data duration for each countries? | |
| What is Purged requirement for each countries ? | |
| What is SLA requirement? | |
| Can we split into different tiles for querying hot data and warm data? - value date>= current-6month:hot data -Current cashflow blotter - value date <current-6month:warm data–Create new tile +value date range query condition | |
| Moving of cashflow from hot to warm data can happen only post 15 months of trade expiry ![image-2026-1-22_16-17-2.png](attachments/image-2026-1-22_16-17-2.png) How to define hot data ? | |
| Remove the limitation of 30 days search and apply limitation based on results exceeding a threshold - After remove the imitation of 30 days,how many days we should support? - What kind of limitation? - How to define the exceeding threshold? | |
| Can we prevent cashflow data updates if the value date past six months? | |
| | |
| | |