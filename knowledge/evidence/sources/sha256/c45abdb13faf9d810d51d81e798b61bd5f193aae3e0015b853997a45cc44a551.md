## Background:

users can upload a csv file to update nostro records.

## API:

| Function | URL | Method | Params | Successful Response | Fail Response | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| Upload Nostro File | /v2/static/nostros/upload | POST | file | { "status": 200, "errorCode": null, "errorMessage": "10", //10 means upload successful nostros count "metadata": null } | { "status": 400, "errorMessage": "there are some error value found at line 2. legalEntityFmId, currency, settlementMeans, settlementAccount, startDate, endDate combination already exists ", "errorCode": "800400117", "metadata": {} } | if there is a error value in the upload file all data will be failed. directConfirm: true: nostro will be save_confirmed false: nostro will be update_pending |
| directConfirm（true/false) |