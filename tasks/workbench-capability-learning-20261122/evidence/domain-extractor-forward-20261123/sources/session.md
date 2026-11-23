# Retained synthetic engineering session
Date: 2026-11-23. Environment: lab. Pipeline: alpha.
Goal: resolve a package for an exact source commit.
The source commit is compared against package.commit when that field is available. A missing commit prevents exact selection.
A request using release/* returned an empty page; an exact release/2 branch returned one package. Only these requests were tried.
Changing an access token followed a 403. No follow-up request was retained. The cause remains unknown.
The package download and deployment were not executed.
No pagination request beyond the first returned cursor was retained.
