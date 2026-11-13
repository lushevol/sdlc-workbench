## 1. Issue location line number wrong

Fixed

## 2. Review results various for same pr

Fixed

## 3. Either 3 issues or no issue

Fixed

## 4. Reported issues which is not in code.

Agent may got incorrect code changes.

### solution:

use HierarchyQuery instead,

### evidence:

I compared 20 pr code changes, most of them are the same, and those not the same, HierarchyQuery returns the right changes.

#### git diff:

![image-2025-8-20_20-24-39.png](attachments/image-2025-8-20_20-24-39.png)

#### HierarchyQuery:

![image-2025-8-20_20-25-6.png](attachments/image-2025-8-20_20-25-6.png)

#### Real Changes:

![image-2025-8-20_20-25-27.png](attachments/image-2025-8-20_20-25-27.png)