# LLM API Cost Estimation for PR Review

## Overview

This document provides a detailed estimation of LLM API usage and associated costs for automated pull request (PR) reviews.

## Token Usage Analysis

- **Total Code Changes (characters):** 61,456,367
- **Total Tokens from Code Changes:** 61,456,367 / 4 = 15,364,091.75

## Prompt Token Breakdown

- **PR Review Prompt:** 3,383 / 4 = 845 tokens
- **PR Description Prompt:** 960 / 4 = 240 tokens

## Pull Request Volume

- **Total PRs Reviewed:** 530
- ![image-2025-9-29_15-25-49.png](attachments/image-2025-9-29_15-25-49.png)

## Average Token Consumption per Review

- **Input Tokens per Review:** - (15,364,091.75 / 530 + 845) + (15,364,091.75 / 530 + 240) = 59,062
- **Output Tokens per Review:** - 900 (700 for review result, 200 for description)

## Review Duration

- **Total Duration:** 2 months (approximately 40 days)

## Query Rate

- **Queries per Minute:** - 530 / (40 × 24 × 60) = 0.0092

# Cost Estimation

## Original Model Cost

- **Monthly Cost:** $142.12

![image-2025-9-29_15-40-52.png](attachments/image-2025-9-29_15-40-52.png)![](https://file+.vscode-resource.vscode-cdn.net/c:/Users/1639796/Code/SCB/ratan-ultra-monitor/51358-mfe-ratan-graphql-ui-poc/download/attachments/3489595931/image-2025-9-29_15-40-52.png?version=1&modificationDate=1759131653000&api=v2)

## Final Cost Calculation

The final cost incorporates a 25% discount, a 25% supporting/foundation cost, and an 18% cloud engineering cost:

**$142.12 × (0.75 + 0.25 + 0.18) = $167.70 per month **

---

This estimation provides a comprehensive view of LLM API usage and costs for PR review automation, supporting informed budgeting and operational planning. **142.12 * (0.75 + 0.25 + 0.18) = 167.7 USD / Month**