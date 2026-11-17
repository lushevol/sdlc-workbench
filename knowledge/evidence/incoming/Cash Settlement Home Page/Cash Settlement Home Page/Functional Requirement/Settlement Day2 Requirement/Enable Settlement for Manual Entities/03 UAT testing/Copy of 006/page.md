| Test Case | Expected Results | Cash flow Id |
| --- | --- | --- |
| Corporate Client with 57 BIC | MT103/pacs.008 is generated with 57A(Account with institution BIC exists) | M00127113405 |
| Bank Client | MT 202 is generated as per expected format and successfully Ackd. | M00127114420 |
| Serial MT103 payment | MT103/pacs.008 SERIAL is generated as per expected format and successfully Ackd. Local CCY have field 53 populated | M00127114719 |
| MT103 with different charge types | MT103/pacs.008 SHA/BEN/OUR is generated as per expected format and successfully Ackd | M00127114725 |
| MT103 with field 70 | MT103/pacs.008 with field 70 is generated as per expected format and successfully Ackd | M00127114721 |
| MT103 with field 72 | MT103/pacs.008 with field 72 is generated as per expected format and successfully Ackd | M00127114412 |
| MT202 with field 72 | MT 202 with field 72 is generated as per expected format and successfully Ackd | M00127114416 |
| MT202 with field 56 | MT202/pacs.009 is generated with 56A (Intermediary Institution BIC exists). Successfully Ack'd | M00127114416 |
| MT202 with field 57 BIC | MT202/pacs.009 is generated with 57A (Account with institution BIC exists). Successfully Ack'd | M00127114420 |
| MT202 with field 57 name | MT202/pacs.009 is generated with 57D (Account with institution BIC not exists). Successfully Ack'd | M00127114444 |
| MT202 with Bene BIC | MT202/pacs.009 is generated with 58A (Beneficiary Customer BIC exists). Successfully Ack'd | M00127114420 |
| MT103+202COV format | MT103/pacs.008+202COV/pacs.009COV is generated as per expected format and successfully Ackd. 202 has field 53 populated with debit account number | M00127114713 |
| MT192 | MT192/camt.056 (Corp client) is generated as per expected format. Successfully Ack'd | M00127113405 |
| MT292 | MT292/camt.056 (Bank client) is generated as per expected format. Successfully Ack'd | M00127114420 |
| MT192+292 | MT192/camt.056+292/camt.056 (Corp client) is generated as per expected format. Successfully Ack'd | M00127114719 |
| MT292 | MT292/camt.057 for MT210 is generated as per expected format. Successfully Ack'd | M00127115303 |
| SWIFT Generation | New Tile>Cashflow Blotter>Released/Settled Status of FCY | M00127115528 |
| SWIFT Generation | New Tile>Cashflow Blotter>Released/Settled Status of FCY | M00127115530 |