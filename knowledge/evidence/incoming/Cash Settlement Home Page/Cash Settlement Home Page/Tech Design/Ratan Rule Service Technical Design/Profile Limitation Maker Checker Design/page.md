1. Table design
2. Status Machine Status of profile limitation, ADD_PENDING,EDIT_PENDING,DELETE_PENDING,CONFIRMED,ADD_REJECTED. 1). if ADD_CONFIRMED or EDIT_PENDING, the profile limitation will be disabled, the API will not able to get the profile limitation via interface. 2), Reject action: when ADD_PENDING: change status to ADD_REJECTED delete the record directly, record checker and time. when EDIT_PENDING: change status to CONFIRMED, restore the profile limitation to the old value, record checker and time. when DELETE_PENDING : change status to CONFIRMED, restore the profile limitation to the old value ,record checker and time. 3). CONFIRM action: when ADD_PENDING: change status to CONFIRMED, record checker and time. when EDIT_PENDING: change status to CONFIRMED, record checker and time. when DELETE_PENDING : change status to CONFIRMED, change is delete to true, change status to CONFIRMED.

3. Check Limitation

request url: GET /v1/staticLimitation/checkLimitation/{profile}/{currency}/{amount}
reponse

`{`
`    ``"reason"``: ``""``,`
`    ``"success"``: ``true`
`}`