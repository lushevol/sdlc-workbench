Env: Dev

| cashflows count | for each(old) | key holder (batch_size=1000, column={message_id, version}) | key holder (batch_size=200,column={message_id, version}) | key holder((manual batch SQL)) (batch_size=200,column={message_id, version}) | select after insert |
| --- | --- | --- | --- | --- | --- |
| **net** | **unet** | **net** | **unet** | **net** | **unet** | **net** | **unet** | **net** | **unet** |
| 596 (2025.07.14) | 30.78s | 28.06s | 33.13s | 27.93s | 24.03s | 21.09s | | | 32.13s | 23.17s |
| 1999 (2025.07.14) | 54.33s | 42.84s | 54.41s DB: 10244ms | 45.98s DB: 8947ms | 58.85s DB: 10825ms | 54.92s DB: 9068ms | | | 1.3min DB: 9125ms | 44.28s DB: 9946ms |
| |
| 1999 (2025.07.15) | 40.7s | 36.19s | 40.08s DB: 5947ms | 38.28s DB: 5714ms | 33.75s DB: 5190ms (DB one batch: 568ms) | 31.62s DB: 5424ms (DB one batch: 569ms) | 36.42s DB: 6717ms (DB one batch: 595ms) | 35.06s DB: 7109ms (DB one batch: 674ms) | 38.75s DB: 5002ms (DB one batch: 496ms, DB one batch query: 5ms) | 38.78s DB: 5097ms (DB one batch: 451ms, DB one batch query: 3ms) |