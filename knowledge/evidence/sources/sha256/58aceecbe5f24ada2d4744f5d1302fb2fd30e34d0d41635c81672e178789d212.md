## Related Story

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7147811](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/7147811)

[SSI Validation Rule for UI Form]

# Background

## Case

Changing on rules order will cause to some rules not working. In this case, 57a account institution bic will not validate the format when MT202. e.g. this field will be bypassed even inputs invalid characters.

| Expected | Not Validated |
| --- | --- |
| ![image-2025-4-16_10-18-2.png](attachments/image-2025-4-16_10-18-2.png) | ![image-2025-4-16_10-18-29.png](attachments/image-2025-4-16_10-18-29.png) |

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5378530](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/5378530)

## Impact Scope

All UI form used “CustomForm” in container,

| Description | Snapshot |
| --- | --- |
| vostro/nostro ssi form in cashfloe details of cashfloe blotter. | ![image-2025-4-16_10-16-25.png](attachments/image-2025-4-16_10-16-25.png) |
| | |

## When it happens

When we updated rule content, the response order changed due to its sorting by rule created time.

## Root Causes

Using **isNumber** function incorrectly, this function is implemented to return false if input 0.

```js
isNumber(0) == false 
```

![image-2025-4-16_10-20-3.png](attachments/image-2025-4-16_10-20-3.png)

*mfe-base\src\utils\common.ts*

so when judging if rule is working, this function will always returns false on ruleid 0.

![image-2025-4-16_10-12-51.png](attachments/image-2025-4-16_10-12-51.png)

*mfe-ratan-container\src\ratancomponents\CustomForm\item\ItemsUtils.ts*

In another word, the first rule will always execute regexp sub rules, ignoring mandatory config.

## Why prod is working?

This is the most tricky part, prod is working because 57a bic is on the first place of rules. It will validate bic format when not empty, regardless swift type. If 57a bic not on the first place, it will not validate when MT202, that is thr testing result we got in CASE section.

So even if we fixed the isNumber issue, the validation bug exist. (But if we force put it on the first place, it will working).

## Validation Rule parser bug

To me it’s a bug in rule validation, it’s not working as expected. Mandatory check should not coupled with format validation.

But I need further check on the design to figure out how it works.

# Solution

## Short Term

Force 57a bic rule to be the first place

## Long Term

Enhance the rule

Find a better form validation solution