---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Browser runtime feasibility

> **Apply WebKit results only to the recorded automation build.**
> Action: Retain this limit with compatibility results. Consequence: These checks cannot establish installed Safari behavior. Owner: Codex evidence maintainer.
> Evidence: [connected launches](connected-launch/result.json) and [offline launches](offline-launch/result.json).

The installed Playwright package supports both browsers on this macOS platform.
The dry run selected Firefox 157.0, revision 1555, and WebKit 27.2, revision 2370.
The initial check found neither browser executable in the configured local cache.
That read-only check downloaded no browser files and tested no download connectivity.
The later explicit installation succeeded. Evidence: [installation result](install-result.json) and [installation log](install.log).

At inspection, the root harness selected Chromium or Edge only.
The browser adapter also selected Chromium or Edge only.
Bundle preparation provisions Chromium explicitly and copies existing browser cache files.
Provision extra engines before preparing a bundle that must include them.

The existing bundle preparation and offline installation both passed.
Evidence: [preparation](bundle-prepare-result.json), [offline installation](bundle-offline-install-result.json), and [compressed bundle manifest](prepared-browser-manifest.json.gz).
The offline installer used its prepared package cache with browser downloads disabled.
Firefox and WebKit launched successfully from both installation locations.
Both engines rendered the synthetic page and changed its counter from zero to one.
Each launch retained a fresh screenshot and its SHA-256.
Matching executable hashes connect the copied engines to the original installation.

These checks establish local runtime readiness only.
They establish no business application behavior, provider acceptance, or installed Safari result.
Firefox uses the Playwright browser build.

The [result](result.json) retains commands, exit codes, output hashes, platform details, and inspected source hashes.
All four read-only commands and both installation commands returned exit code zero.
All four synthetic engine launches passed.
ASD review remains pending.
