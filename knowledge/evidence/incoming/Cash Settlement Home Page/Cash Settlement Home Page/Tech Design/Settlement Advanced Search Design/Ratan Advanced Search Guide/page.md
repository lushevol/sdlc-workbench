# Background

Referring to requirement [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7529554](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7529554)

# Comparison

| Compare | Before | After |
| --- | --- | --- |
| Snapshot | ![image-2025-3-19_9-35-43.png](attachments/image-2025-3-19_9-35-43.png) | ![image-2025-3-19_9-35-47.png](attachments/image-2025-3-19_9-35-47.png) |
| Fields Selection | **Not allow** duplicate fields | **Allow** duplicate fields in different groups |
| Operators & Values Selector | No Change |
| Combinator | All filter items combined with AND, means results should match all filter items. | Logic of filter items regard to the combinator for the level, supporting AND and OR. |
| Group | Only one single Root Group | Multiple group, can be nested. Maximum nested deep is 3. |
| Filter Records | No Change |
| Create/Modify/Delete Filter | No Change |
| Permission Control | No Change |

# Usage Guide