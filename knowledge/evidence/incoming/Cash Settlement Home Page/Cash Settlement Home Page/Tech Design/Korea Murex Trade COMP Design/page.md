# Background

[Story 12660021 [Korea]Comp status to drive STP process](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12660021)

# Design Diagram

DB Change

New table:   Mxg_Korea_Trade_Confirmation_Message

| Column | Comment | Type |
| --- | --- | --- |
| id | unique id | id (seq) |
| trade_id | Trade Id | text |
| action | action in trade xml /events/mainEvent/action | text |
| raw_message | original message | text |
| created_at | create timestamp | timestamp |
| updated_at | update timestamp | timestamp |