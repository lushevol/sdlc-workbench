# Workflow

![image2023-1-16_15-15-5.png](attachments/image2023-1-16_15-15-5.png)

# Show Message

![image2023-1-16_15-41-12.png](attachments/image2023-1-16_15-41-12.png)

# View Notification History

![image2023-1-16_15-42-21.png](attachments/image2023-1-16_15-42-21.png)

# Close Notification Drawer

![image2023-1-16_15-45-30.png](attachments/image2023-1-16_15-45-30.png)

# View Notification Detail Option 1

![image2023-1-16_15-52-4.png](attachments/image2023-1-16_15-52-4.png)

# View Notification Detail Option 2

![image2023-1-16_15-54-14.png](attachments/image2023-1-16_15-54-14.png)

# Strategy of Connection

1. Connect to Cluster Based on web socket cluster, test the reconnection that when one node is <u>down or rest</u>, client side can <u>auto reconnect</u> to other server in cluster
2. Error Any block error when connect to notification service, use error code "400 series" first ( will make a further definition according to "The Error Code Standard" ), and client will show error message when disconnected, will not connect. Empty token, expire token, error of token's signature may cause the block error.
3. Header Place the JWT token to header "Single-UI-Authorization"
4. Entitlement FE pass token to BE, backend will get the user's entitlement and judge what kind of message should push to client side