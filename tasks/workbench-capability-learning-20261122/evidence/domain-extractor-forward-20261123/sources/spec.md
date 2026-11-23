# BuildVault API v2
Synthetic vendor specification revision vendor-v2.
GET /v2/packages accepts required project (string), optional branch (string), and optional cursor (string). It returns 200 JSON with packages (array of objects requiring id and name). The optional next cursor is string or null. The specification does not describe authentication, errors, defaults, or total counts.
