# Base source excerpts

Historical source evidence. These excerpts establish base behavior, without recording runtime execution.

## auth-03-base-role-handling

Commit: `7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee`.
Path: `/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems2EntitlementService.java`.
Lines: 137-156.
Source SHA-256: `9d6691b90af5b48e5ac954bca8cb52ca98479deaed952ae25d3c6e66df1bebcd`.

```text
137:             userEntitlements.forEach((key, value) -> value.getEntitlements().forEach(a -> {
138:                 ratanEntitlement.appendAction(a.getAction().getEntity().getName() + ":" + a.getAction().getName());
139:                 if (Objects.nonNull(a.getRole())) {
140:                     // this 'if' is not a good practice, but for a quick demo purpose
141:                     if (!"RATAN_ENTITLEMENT_SUP_USER".equalsIgnoreCase(a.getRole().getName())) {
142:                         roleSet.add(a.getRole().getName());
143:                     }
144:                 }
145:             }));
146: 
147:             if (roleSet.size() < 1) {
148:                 throw new NoRoleException(String.format("Not Authorized, no entitlement setting for your account %s.", userId));
149:             }
150: 
151: //            if (roleSet.size() > 1) {
152: //                throw new MultipleRoleException(
153: //                    String.format("Multiple roles [%s] detected for your account %s", roleSet.toString(), userId));
154: //            }
155: 
156:             ratanEntitlement.setRole(roleSet.stream().collect(Collectors.joining(",")));
```

## auth-01-base-data-read

Commit: `7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee`.
Path: `/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems2EntitlementService.java`.
Lines: 221-239.
Source SHA-256: `9d6691b90af5b48e5ac954bca8cb52ca98479deaed952ae25d3c6e66df1bebcd`.

```text
221:     public RatanEntitlement queryDataEntitlementRoles(String userId) {
222: 
223:         String ratanEntitlementString;
224:         RatanEntitlement ratanEntitlement = new RatanEntitlement();
225:         ///////// data entitlement control //////////
226:         ResponseEntity<String> responseEntity = restTemplate.getForEntity(String.format(ems2Configuration.getUserRoles(), userId),
227:             String.class);
228:         if (StringUtils.isNotBlank(responseEntity.getBody())) {
229:             Ems2RoleResult result = JSON.parseObject(responseEntity.getBody(), Ems2RoleResult.class);
230:             log.info("Get response from EMS2: {} for user: {}", result, userId);
231:             if (!CollectionUtils.isEmpty(result.getEntitlementTypes())) {
232:                 String roleNames = result.getEntitlementTypes().stream()
233:                     .filter(Objects::nonNull)
234:                     .filter(element -> StringUtils.isNotBlank(element.getRoleName()))
235:                     .filter(element -> element.getUniqueName().contains(ems2Configuration.getDataEntitlementEntity()))
236:                     .map(Ems2RoleResult.EntitlementType::getRoleName)
237:                     .collect(Collectors.joining(","));
238:                 ratanEntitlement.setDataEntitlementRoles(roleNames);
239:                 log.info("retrieved entitlement role: {}", roleNames);
```

## auth-02-base-response-validation

Commit: `7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee`.
Path: `/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/repo/Ems3Repository.java`.
Lines: 83-100.
Source SHA-256: `50adedeaf06bc546fb3a2214b50ec559297f65294fe4ae0e49fc189f1d54c556`.

```text
83:             log.error("Failed to parse error response body: {}", responseBody, ex);
84:             return "Unknown error occurred";
85:         }
86:     }
87: 
88:     private Ems3DataEntitlementDto validateAndGetEms3Response(String userId, List<Ems3DataEntitlementDto> response) {
89:         if (CollectionUtils.isEmpty(response)) {
90:             throw Ems3UnRetryableException.invalidResponse("Response is empty");
91:         }
92:         Ems3DataEntitlementDto result = response.stream()
93:                 .filter(e -> e.getUserData().getUserId().equals(userId))
94:                 .findFirst()
95:                 .orElseThrow(() -> Ems3UnRetryableException.invalidResponse("Failed to get data entitlements for user:" + userId));
96:         if (result.getEntitlements() == null || CollectionUtils.isEmpty(result.getEntitlements().getDataEntitlements())) {
97:             throw Ems3UnRetryableException.invalidResponse("Empty data entitlements detected");
98:         }
99:         return result;
100:     }
```

## auth-07-base-controller

Commit: `7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee`.
Path: `/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/controller/AuthenticationController.java`.
Lines: 207-210.
Source SHA-256: `5d227baf629361cf792568b1db10e947eb67cdd05cf5c28efb19400ad177c95b`.

```text
207:     @GetMapping("/v4/kong/token")
208:     public ResponseEntity<String> getKongTokenV4(String scope) {
209:         return ResponseEntity.ok().contentType(MediaType.APPLICATION_JSON).body(kongGatewayAuthService.fetchAccessToken(scope));
210:     }
```

## auth-07-base-controller-test

Commit: `7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee`.
Path: `/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/controller/AuthenticationControllerTest.java`.
Lines: 59-66.
Source SHA-256: `cc28c803d900c1641daec9b170325fac5f9903feebf45396a055d2c74631d3e7`.

```text
59:         MvcResult result = mockMvc.perform(get("/v4/kong/token")
60:             .contentType(MediaType.APPLICATION_JSON)
61:             .accept(MediaType.APPLICATION_JSON)
62:             .param("scope", "testScope"))
63:             .andExpect(MockMvcResultMatchers.status().isOk())
64:             .andReturn();
65: 
66:         assertThat(result.getResponse().getStatus()).isEqualTo(HttpStatus.OK.value());
```

## auth-07-base-scope-test

Commit: `7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee`.
Path: `/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/service/KongGatewayAuthServiceTest.java`.
Lines: 74-83.
Source SHA-256: `154ae7216e1002e7d75e036ffeabb005660a3f6f8d575d3319f71a50587ea58b`.

```text
74:         String token = kongGatewayAuthService.fetchAccessToken("custom.scope");
75: 
76:         assertEquals("token-123", token);
77:         verify(restTemplate, never()).exchange(eq(CLIENT_ENDPOINT), eq(HttpMethod.GET), any(HttpEntity.class), eq(String.class));
78: 
79:         ArgumentCaptor<HttpEntity<String>> tokenRequestCaptor = httpEntityCaptor();
80:         verify(certRestTemplate).exchange(eq(TOKEN_ENDPOINT), eq(HttpMethod.POST), tokenRequestCaptor.capture(), eq(String.class));
81: 
82:         HttpEntity<String> requestEntity = tokenRequestCaptor.getValue();
83:         assertEquals("grant_type=client_credentials&scope=custom.scope", requestEntity.getBody());
```
