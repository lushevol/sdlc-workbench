# Assumption & Background:

**Refer to the attached email:  <u></u>**

# Reproduce:

### 1. No dump running, alter table time cost: 266ms

![image-2025-7-28_14-18-33.png](attachments/image-2025-7-28_14-18-33.png)

### 2. drop column

### 3. Dump start

Run command:

![image-2025-7-28_14-20-27.png](attachments/image-2025-7-28_14-20-27.png)

Can see many locks for pg_dump:

![image-2025-7-28_14-20-6.png](attachments/image-2025-7-28_14-20-6.png)

### 4. alter table again (blocked 42s +)

![image-2025-7-28_14-24-5.png](attachments/image-2025-7-28_14-24-5.png)

### 5. Kill the dump request, lock released, alter success(1m 37s)

![image-2025-7-28_14-25-16.png](attachments/image-2025-7-28_14-25-16.png)

# **Conclusion:**

**pg_dump job lasts too long blocked alter script result in release issue.**