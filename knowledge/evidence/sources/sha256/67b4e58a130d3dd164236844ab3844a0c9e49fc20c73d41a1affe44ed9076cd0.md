# Background

Ratan need a common exception handling and compensation mechanism. Main ask is how to handle those messages reached out to the max retry times on any cases.

One case we found that in group management, 400+ payments exist under same trade id and the processing competing with the trade status flow from another topic on the trade id lock authorization.

While the cashflows are being processed, trade status cannot obtain the lock authorization after 5 times retry and eventually moved to dead letter queue and dropped, which caused the payments pending trade validation.

Though manual STP can solve the problem, but we need a graceful way of handling it.