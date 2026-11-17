# Local renewal investigation

Historical execution, 24 October 2026; local fixture, source revision ui-42.

Mouse events every 100 ms during a 15-second observation produced zero renewal requests.
Inspected ui-42 code schedules runExtend after 5,000 ms. This delay describes implementation, not intended policy.
The fixture used a controlled clock and a stub issuer. It did not test UAT or continuous real-duration renewal.
