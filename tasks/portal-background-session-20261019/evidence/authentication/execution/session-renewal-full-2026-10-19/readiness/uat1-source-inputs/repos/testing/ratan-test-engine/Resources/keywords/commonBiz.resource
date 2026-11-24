*** Settings ***
Documentation        Writer: NI MING
...                  Created: 2023-07-18
...                  comment: Create For RatanOne
... 
Library              FakerLibrary  en_US    #en_US    #zh_CN  
Library              Collections
Library              String
Library              OperatingSystem
Library              DateTime
Library              json
Library              CommonUtils.py
Library              JSONLibrary
Library              RequestsLibrary
Library              DatabaseLibrary
Library              SSHLibrary
Library              Process
Resource             commonUtils.resource
Library              ConfluentKafkaLibrary
# Resource             business_common.resource
Variables            ../data/config/config.py

*** Keywords ***
SUITE INITIAL
    [Documentation]    Helper keyword SUITE INITIAL:
    ...    run CERTIFICATE INITIAL -> Cmd Variable Dictionary; then VAR; verify expected system behavior after execution;
    ...    confirm execution result matches business expectation.
    CERTIFICATE INITIAL
    ${cmd_dict}  Cmd Variable Dictionary
    VAR  ${cmd_dict}  ${cmd_dict}  scope=global
    
CERTIFICATE INITIAL
    [Documentation]    Helper keyword CERTIFICATE INITIAL:
    ...    run RequestsLibrary.Create Session -> RequestsLibrary.Get On Session; then jsonGetObject; verify expected system
    ...    behavior after execution; confirm execution result matches business expectation.
    TRY
        IF  $SECURITY_SOURCE=='portal'
            RequestsLibrary.Create Session  website  url=${TEST_PORTAL_URL}
            ${response}  RequestsLibrary.Get On Session  website  url=${TEST_PORTAL_CERTIFICATE_ENDPOINT}  timeout=2
            ${status}  ${result}  jsonGetObject  ${response.json()}  $.data
            FOR  ${dict}  IN  @{result}
                Set Suite Variable  ${${dict}[key]}  ${dict}[value]
            END
        END
    EXCEPT
        log to console  test portal can't connected. use local certificate files
    END

Format Parameter
    [Documentation]  Create Data with param. rf format or python format
    ...  Format Parameter
    ...  cashflowId=PERF-[randomString|12|umn]
    ...  uuid="PERF-"+"[UUID 4]".replace("-","") 
    [Arguments]  &{param}
    FOR  ${key}  ${value}  IN  &{param}
        #log to console  ${value}
        ${matches}  Get Regexp Matches    ${value}    \\[(.+?)\\]
        FOR    ${index}    ${match}    IN ENUMERATE    @{matches}
            ${cmd}  Split String    ${match}[1:-1]  |
            ${val}  Run Keyword  @{cmd}
            ${value}  Replace String  ${value}  ${match}  ${val}
            ${status}  Run Keyword And Return status  Evaluate  ${value}
            IF  ${status}
                ${value}  Evaluate  ${value}  
            END
            Set To Dictionary  ${param}  ${key}=${value}
        END
    END
    log to console  ${param}
    RETURN  ${param}

Send Kafka With Parameter
    [Documentation]  Send Kafka With Parameter
    ...  topic=OPENSEARCH.INBOUND.CASHFLOW  
    ...  template=example.json  
    ...  cashflowId=PERF-[randomString|12|umn]
    ...  uuid="PERF-"+"[UUID 4]".replace("-","") 
    [Arguments]  ${producerId}  ${topic}  ${template}  ${formatFlg}=${True}  &{param}
    IF  ${formatFlg}
        ${param}  Format Parameter  &{param}
    END
    # log many  ${param}
    # VAR  ${param}  ${param}  scope=global
    ${message}  String.Format String  ${demo_root}${/}Resources${/}data${/}template${/}kafka${/}${template}  &{param}
    # log many  ${message}
	# Run Keyword  KAFKA Command By ${METHOD.upper()}  ${topic}  ${message}  
    Produce  group_id=${producerId}  topic=${topic}  value=${message}
    # Flush    group_id=${PRODUCER_ID}
    RETURN  ${param}

RATAN LOGIN NEW
	[Arguments]  ${USERNAME}  ${PASSWORD}
	[Documentation]  Ratan Login
	...              REQ: 
	comment  ======Step1.1:Login to get maker token
	${req_host}  Set Variable  ${URL}
	${expected_status}  Set Variable  200
	${req_body}  json.Loads  {\"username\":\"${USERNAME}\",\"${CREDENTIAL}\":\"${PASSWORD}\",\"entities\": [\"X_RATANONE\",\"RATAN_TRADE_BLOTTER\",\"RATAN_CASHFLOW_BLOTTER\",\"RATAN_STRATEGIC_CASHFLOW_BLOTTER\",\"RATAN_CASHFLOW_GROUP_BLOTTER\",\"RATAN_VALIDATION_EXCEPTION\",\"RATAN_SETTLEMENT_EXCEPTION\",\"RATAN_PROFILE_LIMITS\",\"RATAN_SETTLEMENT_STP_RULE\",\"RATAN_SUPPRESSION_RULE\",\"RATAN_NETTING_RULE\",\"RATAN_ENTITLEMENT_RULE\",\"RATAN_NOSTRO_BLOTTER\",\"SSIPLUS\",\"FSS_PAYMENTS_SERVICES_TH\"]}
	FOR  ${i}  IN RANGE  1
		RequestsLibrary.Create Session  website  url=${req_host}
		${response}  RequestsLibrary.Post On Session    website    url=/api/auth/v2/sso/login    json=${req_body}	expected_status=${expected_status}	allow_redirects=${False}
	END
	${status}  ${result}  jsonGetObject  ${response.json()}  $.result
	${assert}  Create List  success  ${True}
	Should Contain Any   ${assert}  ${result}
	RequestsLibrary.Delete All Sessions
	${token}  Set Variable  ${response.headers['Single-UI-Authorization']}
	${runstatus}  Run Keyword And Ignore Error  Set Global Variable  ${token}  ${token}
	Run Keyword And Ignore Error  Set Suite Variable  ${Req_RATAN LOGIN NEW_Step1.1}  ${req_body}
	Run Keyword And Ignore Error  Set Suite Variable  ${Resp_RATAN LOGIN NEW_Step1.1}  ${response.json()}

RATAN LOGIN
	[Arguments]  ${USERNAME}  ${PASSWORD}
	[Documentation]  Ratan Login
	...              REQ: 
	comment  ======Step1.1:Login to get maker token
	${req_host}  Set Variable  ${URL}
	${expected_status}  Set Variable  200
	${req_body}  json.Loads  {\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\",\"entities\": [\"X_RATANONE\",\"RATAN_TRADE_BLOTTER\",\"RATAN_CASHFLOW_BLOTTER\",\"RATAN_STRATEGIC_CASHFLOW_BLOTTER\",\"RATAN_CASHFLOW_GROUP_BLOTTER\",\"RATAN_VALIDATION_EXCEPTION\",\"RATAN_SETTLEMENT_EXCEPTION\",\"RATAN_PROFILE_LIMITS\",\"RATAN_SETTLEMENT_STP_RULE\",\"RATAN_SUPPRESSION_RULE\",\"RATAN_NETTING_RULE\",\"RATAN_ENTITLEMENT_RULE\",\"RATAN_NOSTRO_BLOTTER\",\"SSIPLUS\",\"FSS_PAYMENTS_SERVICES_TH\"]}
	FOR  ${i}  IN RANGE  1
		RequestsLibrary.Create Session  website  url=${req_host}
		${response}  RequestsLibrary.Post On Session    website    url=/api/auth/v2/sso/login    json=${req_body}	expected_status=${expected_status}	allow_redirects=${False}
	END
	${status}  ${result}  jsonGetObject  ${response.json()}  $.result
	${assert}  Create List  success  ${True}
	Should Contain Any   ${assert}  ${result}
	RequestsLibrary.Delete All Sessions
	${token}  Set Variable  ${response.headers['Single-UI-Authorization']}
    RETURN  ${token}

Get RATAN Tokens For All Environments
    [Documentation]  Login to each environment in env_dict and extract RATAN token using RATAN LOGIN keyword
    [Arguments]  ${USERNAME}  ${PASSWORD}  &{env_dict}
    ${tokens}    Create Dictionary
    FOR    ${env}    ${url}    IN    &{env_dict}
        # Log    Logging in to ${env} at ${url}
        Set Global Variable    ${URL}    ${url}
        ${token}    RATAN LOGIN    ${USERNAME}    ${PASSWORD}
        Set To Dictionary    ${tokens}    ${env}    ${token}
        Log To Console    Token for ${env}: ${token}
    END
    RETURN    ${tokens}

GET RATAN TOKEN
	[Arguments]  &{FieldDict}
	[Documentation]  Ratan Login format is $variablename=$username|$password
	...              REQ:    
    FOR  ${Key}  ${value}  IN  &{FieldDict}
        Log  ${Key}
        ${username}  ${password}  Split String   ${value}  |
        ${token}  Ratan Login  ${username}  ${password}
        Set Global Variable  ${${Key}}  ${token}
    END

# GET RATAN TOKEN EVERY 15 MINS
# 	[Arguments]  &{FieldDict}
# 	[Documentation]  Ratan Login format is $variablename=$username|$password
# 	...              REQ:
#     WHILE  ${TRUE}
#         GET RATAN TOKEN  &{FieldDict}
#         Sleep  1 minutes
#         log  GET RATAN TOKEN EVERY 15 MINS
#     END    

Listen Postgre Channel
    [Documentation]    Helper keyword Listen Postgre Channel:
    ...    run vpa_listen_postgre_channel -> RETURN; verify expected system behavior after execution; confirm execution;
    ...    result matches business expectation.
    [Arguments]   ${tradeId}  ${db}=vpa
    ${notification}   vpa_listen_postgre_channel  ${tradeId}  ${db_host_${db}}  ${db_port_${db}}  ${db_database_${db}}  ${db_username_${db}}  ${db_password_${db}}
    RETURN  ${notification}
    
CallIndexedAPI
    [Documentation]    Helper keyword CallIndexedAPI:
    ...    run GetInternalApiUrl -> json.Loads; then RequestsLibrary.Create Session; verify expected system behavior after
    ...    execution; confirm execution result matches business expectation.
    [Arguments]  ${xml}
	# ${req_host}  Set Variable  http://10.198.199.160:8079
    ${req_host}  GetInternalApiUrl  ratanone-suppression-service  ${True}
	${req_body}  json.Loads  {\"scbml\":\"${xml}\"}
	FOR  ${i}  IN RANGE  1
		RequestsLibrary.Create Session  website  url=${req_host}
		${response}  RequestsLibrary.Post On Session    website    url=/v1/modelling/scbml/indexed    json=${req_body}	allow_redirects=${False}
	END
    ${content}  Create Dictionary  tradeRecord=${response.json()}
	RequestsLibrary.Delete All Sessions
	Run Keyword And Ignore Error  Set Suite Variable  ${Req_TC-BAU-API-RULESERVICE1-CASHFLOW-NSTP-RULE-000-001}  ${req_body}
	Run Keyword And Ignore Error  Set Suite Variable  ${Resp_TC-BAU-API-RULESERVICE1-CASHFLOW-NSTP-RULE-000-001}  ${response.json()}
    RETURN  ${content}

CallConversionAPI
    [Arguments]  ${type}=trade  ${xml}=${EMPTY}
    [Documentation]  type=trade/cashflow
    # ${internalApiName}  Set Variable  ratanone-rule-service
    # ${internalApi}  GetInternalApiUrl  ${internalApiName}  forceDev=${True}
	# ${req_host}  Set Variable  ${internalApi}
    ${req_host}  Set Variable  http://10.198.199.160:8868
    # ${req_host}  Set Variable  ${URL}
	${req_body}  json.Loads  {\"message\":\"${xml}\"}
	FOR  ${i}  IN RANGE  1
		RequestsLibrary.Create Session  website  url=${req_host}
        ${response}  RequestsLibrary.Post On Session  website  url=/v2/conversion/trade    json=${req_body}	allow_redirects=${False}
		# ${response}  RequestsLibrary.Post On Session  website  url=/api/ratan/v2/conversion/trade    json=${req_body}	allow_redirects=${False}
	END
    ${jsomMap}  jsonGetObjects  ${response.json()}  $.map
    ${content}  Create Dictionary  tradeRecord=${jsomMap}[1][0]
    ${content}  jsonToStr  ${content}
	RequestsLibrary.Delete All Sessions
    RETURN  ${content}

GetInternalApiUrl
	[Documentation]  Get Internal API lists
	...              REQ: 
	[Tags]  bau
    [Arguments]  ${serviceName}=AUTHENTICATION  ${forceDev}=${False}
	comment  ======Step1: Get all ports
    ${EUREKA_URL}  Set Variable If  ${forceDev}  http://uklvadapp1340.uk.dev.net:8763  ${EUREKA_URL}
	${req_host}  Set Variable  ${EUREKA_URL}
	FOR  ${i}  IN RANGE  1
		RequestsLibrary.Create Session  website  url=${req_host}
		${response}  RequestsLibrary.Get On Session    website    url=/eureka/apps    	allow_redirects=${False}
	END
	RequestsLibrary.Delete All Sessions
	${dict}  xmlStringToJson  ${response.content}
    log many  ${dict}
	${instance}  jsonGetObject  ${dict}  $.applications.application[?(@.name='${serviceName.upper()}')].instance
	${type}  Evaluate  type($instance[1])

    IF  "${ENV.lower()}"=="dev" or ${forceDev}
        VAR  ${path}  healthCheckUrl
    ELSE
        VAR  ${path}  secureHealthCheckUrl
    END

	IF  "${type}"=="<class 'list'>"
	    ${Url}  jsonGetObject  ${dict}  $.applications.application[?(@.name='${serviceName.upper()}')].instance[0].${path}
	ELSE
	    ${Url}  jsonGetObject  ${dict}  $.applications.application[?(@.name='${serviceName.upper()}')].instance.${path}
	END

    VAR  ${Url}  ${Url[1].replace("/actuator/health","")}
    RETURN  ${Url}

getAuthentication
	[Documentation]  
	...              REQ: 
	[Tags]  
	${req_host}  Set Variable  https://fmaauat.gdc.standardchartered.com
	${req_header}  Create Dictionary  authorization=Basic UkFUQU5fUFJPRDpkWDdCTipxbkVWOUxBQWg2MlE0aEZObTF4
	${expected_status}  Set Variable  200
	${req_body}  Create Dictionary  grant_type=client_credentials  app_id=RatanOne_localhost
	FOR  ${i}  IN RANGE  1
		RequestsLibrary.Create Session  website  url=${req_host}
		${response}  RequestsLibrary.Post On Session    website    url=/v1/fmaa/oauth2/access_token    data=${req_body}	headers=${req_header}	expected_status=${expected_status}	allow_redirects=${False}
	END
	RequestsLibrary.Delete All Sessions
	${status}  ${token}  jsonGetObject  ${response.json()}  $.access_token
    RETURN  ${token}

Get gRPC Response
    [Arguments]  ${proto}=RatanBusinessDataProvider.proto  ${method}=RatanBusinessDataProvideService.queryCashflowExternally  ${request}={"sql":"select * from cashflow limit 1"}
    [Documentation]  Get gRPC Response method=RatanBusinessDataProvideService.queryCashflowExternally or RatanBusinessDataProvideService.queryCashflowInternally
    ${token}  getAuthentication
	${response}  Run Process  grpcurl  -H  FMAA-UserId: RATAN_PROD  -H  FMAA-AppId: RatanOne_localhost  -H  FMAA-Token: ${token}  -d  ${request}  -proto  ${proto}  -insecure  ${URL.replace("https://","").replace("http://","").replace("/?show_normal_login=y","")}  ${method}
	...  cwd=Tests${/}ratan${/}data${/}tools    #C:\\Users\\2011047\\Downloads\\foundation
	...  stdout=PIPE  
	...  stderr=PIPE
	# log to console  ${response.stderr}
	RETURN  ${response.stdout}

TDS3_Trade_Confirmation
    [Arguments]    ${template}=TDS3_Trade_Confirmation    &{FieldDict}
    [Documentation]    trade confirmation from TDS3
    &{DefaultDict}    Create Dictionary    tradeWorkflowStatus=CONFIRMED    majorVersion=1    trackingVersion=0
    IF    "majorVersion" in $FieldDict.keys() and "trackingVersion" not in $FieldDict.keys()
        ${majorVersion}    Set Variable    ${FieldDict}[majorVersion]
        ${trackingVersion}    Set Variable    ${${majorVersion}-1}
        Set To Dictionary    ${FieldDict}    trackingVersion=${trackingVersion}
    END
    Set To Dictionary    ${DefaultDict}    &{FieldDict}
    Log To Console    \n ********** start to write trade confrimatin from TDS3 by kafka with para: ${DefaultDict}
    ${message}  TemplateHandler  ${template}  &{DefaultDict}
    Run Keyword  KAFKA Command By ${METHOD.upper()}  topic=TDS3_Trade_Message_Process_In    message=${message}
    log many  ${message}

CDU_Affirmation
    [Documentation]  Please use trade_id,confirmation_status set into FieldDict
    ...      - ``trade_id``: trade id
    ...      - ``confirmation_status[BCS]``: Inbound Completed - Match Completed|Inbound Completed - Inbound Not Required|Inbound Completed - Match Outside CDU
    ...      - ``confirmation_status[EG]``: Confirm|Affirm|Confirmed|Affirmed
    ...      - ``booking_fmid: default 400452428
    ...      - ``counterparty_fmid: default 400118989
    [Arguments]  ${template}=affirmation_body.json    &{FieldDict}
    IF  "booking_fmid" not in $FieldDict.keys()
        ${booking_fmid}  Set Variable  400452428
        Set To Dictionary  ${FieldDict}  booking_fmid=${booking_fmid}
    END
    IF  "counterparty_fmid" not in $FieldDict.keys()
        ${counterparty_fmid}  Set Variable  400118989
        Set To Dictionary  ${FieldDict}  counterparty_fmid=${counterparty_fmid}
    END
    ${uuid}  Uuid 4
    Set To Dictionary  ${FieldDict}  uuid=${uuid}    
    Send_Kafka_Template_Message  topic=CDU_Trade_Confirmation_Process_In  template=${template}  &{FieldDict}

Send_Kafka_Template_Message
    [Documentation]    Helper keyword Send_Kafka_Template_Message:
    ...    run String.Format String -> Log Many; then Run Keyword; verify expected system behavior after execution;
    ...    execution result matches business expectation.
    [Arguments]  ${topic}  ${template}  &{FieldDict}
    ${message}  String.Format String  ${demo_root}${/}Resources${/}data${/}template${/}${template}  &{FieldDict}
    Log Many  ${message}
    Run Keyword  KAFKA Command By ${METHOD.upper()}  topic=${topic}  message=${message}

Send_Kafka_Template_Message_Advance
    [Documentation]    Helper keyword Send_Kafka_Template_Message_Advance:
    ...    run String.Format String -> Log Many; then Run Keyword; verify expected system behavior after execution;
    ...    execution result matches business expectation.
    [Arguments]  ${topic}  ${template}  ${msgCompressFlg}=${True}  ${headerDict}=${{{}}}  &{FieldDict}
    ${message}  String.Format String  ${demo_root}${/}Resources${/}data${/}template${/}${template}  &{FieldDict}
    Log Many  ${message}
    Run Keyword  KAFKA Command By ${METHOD.upper()}  topic=${topic}  message=${message}    headers=${headerDict}  msgCompressFlg=${msgCompressFlg}
    RETURN    ${message}

KAFKA Command By API
    [Documentation]    Helper keyword KAFKA Command By API:
    ...    run XmlCompress -> log many; then VAR; verify expected system behavior after execution; confirm execution;
    ...    result; matches business expectation.
    [Arguments]  ${topic}=${EMPTY}  ${message}=${EMPTY}  ${headers}=${{{}}}  ${msgCompressFlg}=${True}  ${key}=${EMPTY}
    IF  ${msgCompressFlg}
        ${message}  XmlCompress  ${message}
        log many  ${message}
        VAR  ${xmlmessage}  ${message}  scope=GLOBAL
    END
    ${headers}  Evaluate  [{"key": k, "value": v} for k, v in $headers.items()]
    ${headers}  JSONLibrary.Convert Json To String  ${headers} 
    IF  '${headers}'=='[]'  VAR  ${headers}  {"":""}

    ${current_time}  Datetime.Get Current Date  result_format=%Y-%m-%dT%H:%M:%S.%fZ
    IF  '${message}[0]'=='{' and '${message[0:3].replace('\n','').strip()}'!='{1:'
        ${message}  json.dumps  ${message}
        ${message}  Set Variable  ${message}[1:-1]
    END
    # log many  {"clusterId":"${ENV.lower()}-kafka-server","topicId":"${topic}","partition":null,"key":"","timestamp":"${current_time}","keySchema":"","valueSchema":"","value":"${message}","headers":${headers}}
	# ${request}  json.Loads  {"clusterId":"${ENV.lower()}-kafka-server","topicId":"${topic}","partition":null,"key":"","timestamp":"${current_time}","keySchema":"","valueSchema":"","value":"${message}","headers":${headers}}
    #log many  {"clusterId":"${ENV.lower()}-kafka-server","topicId":"${topic}","partition":null,"key":"","timestamp":"${current_time}","keySchema":"","valueSchema":"","value":"${message}","headers":${headers},"multiMessage":false}
    #log many  {"clusterId":"${{$KAFKA_API_URL.split("/")[-1]}}","topicId":"${topic}","partition":null,"key":"","timestamp":"${current_time}","keySchema":"","valueSchema":"","value":"${message}","headers":${headers},"multiMessage":false}
	${request}  json.Loads  {"clusterId":"${{$KAFKA_API_URL.split("/")[-1]}}","topicId":"${topic}","partition":null,"key":"${key}","timestamp":"${current_time}","keySchema":"","valueSchema":"","value":"${message}","headers":${headers},"multiMessage":false}

	${expected_status}    BuiltIn.Set Variable    200
    RequestsLibrary.Create Session    website    url=${KAFKA_API_URL}
	${response}    RequestsLibrary.Post On Session    website    
    ...    url=/topic/${topic}/data    
    ...    json=${request}
    ...	   expected_status=${expected_status}
    ...	   allow_redirects=${False}

KAFKA Command By SSH
    [Documentation]    Helper keyword KAFKA Command By SSH:
    ...    run Open Connection -> login; then Set Client Configuration; verify expected system behavior after execution;
    ...    confirm authentication context is created and usable.
    [Arguments]  ${topic}=${EMPTY}  ${message}=${EMPTY}  ${headers}=${EMPTY}
    Open Connection  10.198.199.160    #ratanrt@
    # login  ratanrt  Sc0pe123@456
    login  ${usernameOfRatanSer}  ${passwordOfRatanSer}
    Set Client Configuration  prompt=$
    Read  delay=3s
    Write  cd jeffrey/cnTestData
    Read Until Prompt    #Read Until  $
    Create File  ${demo_root}${/}Resources${/}data${/}template${/}temp.auto  ${message.replace("\n","")}
    Put File  ${demo_root}${/}Resources${/}data${/}template${/}temp.auto  /apps/ratanrt/jeffrey/cnTestData/ReadyStatus.auto	 mode=0755
    Read  delay=3s
    write  /apps/ratanrt/utilities/kafka/live/bin/kafka-console-producer.sh --bootstrap-server ${KAFKA_SSH_URL} --topic ${topic} < ReadyStatus.auto 
    #Read Until Prompt
    Read  delay=5s
    Close Connection

KAFKA Command By KAFKA
    [Documentation]    Helper keyword KAFKA Command By KAFKA:
    ...    run Create Producer -> Produce; then Flush; verify expected system behavior after execution; confirm execution;
    ...    result matches business expectation.
    [Arguments]  ${topic}=${EMPTY}  ${message}=${EMPTY}  ${headers}=${{{}}}
    ${PRODUCER_ID}  Create Producer
    ...  server=${{",".join(${KAFKA_HOSTS})}}
    ...  port=${KAFKA_PORT}
    Produce  group_id=${PRODUCER_ID}  topic=${topic}  value=${message}  headers=${headers}
    Flush    group_id=${PRODUCER_ID} 

KAFKA Command BATCH
    [Documentation]    Helper keyword KAFKA Command BATCH:
    ...    run Create Producer -> Produce; then Flush; verify expected system behavior after execution; confirm execution;
    ...    result matches business expectation.
    [Arguments]  ${topic}=${EMPTY}  ${message}=${EMPTY}  ${headers}=${{{}}}
    ${PRODUCER_ID}  Create Producer
    ...  server=${{",".join(${KAFKA_HOSTS})}}
    ...  port=${KAFKA_PORT}
    Produce  group_id=${PRODUCER_ID}  topic=${topic}  value=${message}  headers=${headers}
    Flush    group_id=${PRODUCER_ID} 

TemplateHandler
    [Documentation]    Helper keyword TemplateHandler:
    ...    run OperatingSystem.Get File -> Log Many; then String.Format String; verify expected system behavior after
    ...    execution; confirm file content is parsed into expected line structure.
    [Arguments]  ${template}  &{FieldDict}
    ${xml}  OperatingSystem.Get File  ${demo_root}${/}Resources${/}data${/}template${/}${template}.xml
    # Step 2: 打印调试信息
    Log Many  FieldDict: &{FieldDict}
	${xml}  String.Format String  ${xml}  &{FieldDict}
    # ${xml}  XmlCompress  ${xml}
    RETURN  ${xml}

MurexKRTemplateHandler
    [Documentation]    Same functionality as TemplateHandler, but the template is in MurexKR folder
    [Arguments]  ${template}  &{FieldDict}

    ${msgType}    Get From Dictionary    ${FieldDict}    msgType
    ${msgTypeMap}    Create Dictionary    MT103=pacs.008.001.08    MT202=pacs.009.001.08    MT202Cov=pacs.009.001.08    
    ...    MT210=210    MT192=camt.056    MT292=camt.056
    
    IF    '${msgType}'=='MT210'
        ${topic}    Set Variable    Cash_Settlement_Swift_MT_Enisis_Ack
    ELSE
        ${topic}    Set Variable    Cash_Settlement_Swift_MX_Enisis_Ack
    END

    ${mappedMsgTypeValue}    Get From Dictionary    ${msgTypeMap}    ${msgType}
    Set To Dictionary    ${FieldDict}    msgType=${mappedMsgTypeValue}

    ${xml}  OperatingSystem.Get File  ${demo_root}${/}Resources${/}data${/}template${/}MurexKR${/}${template}.xml
    # Step 2: 打印调试信息
    Log Many  FieldDict: &{FieldDict}
	${xml}  String.Format String  ${xml}  &{FieldDict}
    # ${xml}  XmlCompress  ${xml}
    RETURN  ${xml}

XmlCompress
    [Documentation]    Helper keyword XmlCompress:
    ...    run Split String -> Set List Value; then Catenate; verify expected system behavior after execution; file;
    ...    content is parsed into expected line structure.
    [Arguments]  ${xml}

    ${list}  Split String    ${xml}  \n
    #Log To Console    ${list}
    FOR    ${index}    ${element}    IN ENUMERATE    @{list}
        #Log    ${index}: ${element}
        IF  ">NULL<" in $element
            Set List Value    ${list}    ${index}    ${EMPTY}
            #Log to console   ${element}
        END
    END
    ${xml}    Catenate    SEPARATOR=\n    @{list}

    # Compress the xml
    IF  "${METHOD.lower()}"=="api"
        #${formator}  Create Dictionary  \n=${EMPTY}  \r=${EMPTY}  \t=${EMPTY}  "=\\"
        ${formator}  Create Dictionary  \n=\\r\\n  \t=${EMPTY}  "=\\"  \r=${EMPTY}  
    ELSE
        #${formator}  Create Dictionary  \n=${EMPTY}  \r=${EMPTY}  \t=${EMPTY}
        ${formator}  Create Dictionary  \n=\\r\\n  \t=${EMPTY}  #\r=${EMPTY}  
    END
    FOR  ${key}  ${value}  IN  &{formator}
        ${xml}  String.Replace String  ${xml}  ${key}  ${value}
    END
    RETURN  ${xml}

JumpWeekendDate
    [Arguments]  ${offset_time}=0/0/0  ${output_format}=%Y-%m-%d
    [Documentation]  Return Offset Date through Jumping weekend

    ${dateWith}  Offset Time  offset_time=${offset_time}  output_format=%Y-%m-%d
    #log to console  ${dateWith}
    ${weekday}  Evaluate  datetime.datetime.strptime($dateWith,"%Y-%m-%d").weekday()
    IF  $weekday == 5
        #Log To Console    the date is Saturday, need to Jump to next Monday
        ${dateWith}  Offset Time  offset_time=0/0/2  output_format=${output_format}  input_time=${dateWith}  input_format=%Y-%m-%d
    END
    IF  $weekday == 6
        #Log To Console    the date is Sunday, need to Jump to next Monday
        ${dateWith}  Offset Time  offset_time=0/0/1  output_format=${output_format}  input_time=${dateWith}  input_format=%Y-%m-%d
    END
    RETURN  ${dateWith}

# Trade Blotter Counterparty Legal Name Detail Dictionary
#     ${blocks}  Browser.Get Elements  selector=${_common_tradeblotter_tradedetail_counterpartylegalname_block}
#     ${dict}  Create Dictionary
#     FOR  ${block}  IN  @{blocks}
#         ${key}  Get Text  selector=${block} >> .label-details-pop-name
#         ${value}  ElementDict
#         ...  ElementKey=${block} >> //tr/td[not(@colspan)][position()=1 or position()=3]
#         ...  ElementValue=${block} >> //tr/td[not(@colspan)][position()=2 or position()=4]
#         Set To Dictionary  ${dict}  ${key}=${value}
#     END
#     RETURN  ${dict}


Get Kafka Msg Return Dictionary
    [Arguments]  ${topic}=Econ_Affirmation_Out  ${searchTxt}=${EMPTY}  ${directFlg}=${False}  ${nth}=-1
    [Documentation]  Return Topic content from AKHQ for searchTxt. 
    ...    if DirectFlg is ${False}, it will change xml and json to dictionary. 
    ...    if DirectFlg is ${True}, it will return value directly. 
    ${Msg}  AKHQ Msg Search  ${KAFKA_API_URL}/topic/${topic}/data/search?sort=Newest&partition=All&searchByValue=${searchTxt}_C  #dev    3774508136
    IF  '${Msg}'!='${EMPTY}'
        ${Msg}  Convert String To Json  ${Msg}
        log many  ${Msg}
        ${value}  jsonGetObject  ${Msg}  $.records[${nth}].value
        IF  not ${directFlg}
            IF  '${value[1]}[0]'=='<'
                ${value}  xmlStringToJson  ${value[1]}
            ELSE IF  '${value[1]}[1:-1][0]'=='{'
                ${value}  Convert String To Json  ${value[1]}
                ${value}  json.Loads  ${value}
            ELSE
                ${value}  Set Variable  ${value}
            END
        ELSE
            ${value}  Set Variable  ${value[1]}
        END
    ELSE
        ${value}  Set Variable  ${EMPTY}
    END
    RETURN  ${value}

Get Kafka Msg Header Return Dictionary
    [Arguments]  ${topic}=Econ_Affirmation_Out  ${searchTxt}=${EMPTY}  ${directFlg}=${False}  ${nth}=-1
    [Documentation]  Return Topic message headers from AKHQ for searchTxt.
    ...    if DirectFlg is ${False}, it will return headers as dictionary.
    ...    if DirectFlg is ${True}, it will return raw headers value directly.
    
    ${Msg}  AKHQ Msg Search  ${KAFKA_API_URL}/topic/${topic}/data/search?sort=Newest&partition=All&searchByValue=${searchTxt}_C
    
    IF  '${Msg}'!='${EMPTY}'
        ${Msg}  Convert String To Json  ${Msg}
        ${headers}  jsonGetObject  ${Msg}  $.records[${nth}].headers

        IF  not ${directFlg}
            &{headerDict}  Create Dictionary

            IF  $headers[1] != '${EMPTY}'
                ${headerType}  Evaluate  type($headers[1]).__name__

                IF  '${headerType}'=='str'
                    ${headerList}  Convert String To Json  ${headers[1]}
                    ${headerList}  json.Loads  ${headerList}
                ELSE
                    ${headerList}  Set Variable  ${headers[1]}
                END

                FOR  ${header}  IN  @{headerList}
                    ${status}  ${key}  jsonGetObject  ${header}  $.key
                    ${status}  ${value}  jsonGetObject  ${header}  $.value
                    Set To Dictionary  ${headerDict}  ${key}=${value}
                END
            END

            ${returnValue}  Set Variable  ${headerDict}
        ELSE
            ${returnValue}  Set Variable  ${headers[1]}
        END
    ELSE
        IF  not ${directFlg}
            &{returnValue}  Create Dictionary
        ELSE
            ${returnValue}  Set Variable  ${EMPTY}
        END
    END
    
    RETURN  ${returnValue}

Get Kafka Msg Return Dictionary By Element
    [Arguments]    ${topic}    ${searchTxt}    ${element}    ${elementTxt}
    [Documentation]    Return Topic content from AKHQ by searchTxt and element value. 
    @{actualRecordList}    Create List
    ${allRecords}    Get Kafka Msg Return Dictionary All    ${topic}    ${searchTxt}
    FOR    ${record}    IN   @{allRecords}
        ${actualMsg}    Convert String To Json    ${record}
        IF    "${elementTxt}" == "${actualMsg}[${element}]"
            Append To List    ${actualRecordList}    ${actualMsg}
        END
    END
    RETURN    ${actualRecordList}

Get Kafka Msg Return Dictionary By Elements
    [Arguments]    ${topic}    ${searchTxt}    ${element}    ${elementTxt}
    [Documentation]    Return Topic content from AKHQ by searchTxt and element value. 
    ...    different with "Get Kafka Msg Return Dictionary By Element" is : this can search by json path
    @{actualRecordList}    Create List
    ${allRecords}    Get Kafka Msg Return Dictionary All    ${topic}    ${searchTxt}
    FOR    ${record}    IN   @{allRecords}
        ${actualMsg}    Convert String To Json    ${record}
        ${status}  ${actualText}  jsonGetObject    ${actualMsg}    ${element}
        IF    "${elementTxt}" == "${actualText}"
            Append To List    ${actualRecordList}    ${actualMsg}
        END
    END
    RETURN    ${actualRecordList}

Get Kafka Msg Return Dictionary All
    [Arguments]  ${topic}=Econ_Affirmation_Out  ${searchTxt}=${EMPTY}  ${directFlg}=${False}  ${searchByHeaderFlg}=${False}
    [Documentation]  Return Topic content from AKHQ for searchTxt. 
    ...    if DirectFlg is ${False}, it will change xml and json to dictionary. 
    ...    if DirectFlg is ${True}, it will return value directly. 
    
    ${text}  Evaluate  "Header" if $searchByHeaderFlg else ""
    ${searchTxt}    Evaluate    urllib.parse.quote('${searchTxt}', safe='')
    #log many  ${KAFKA_API_URL}/topic/${topic}/data/search?sort=Newest&partition=All&searchBy${text}Value=${searchTxt}_C
    ${Msg}  AKHQ Msg Search All  ${KAFKA_API_URL}/topic/${topic}/data/search?sort=Newest&partition=All&searchBy${text}Value=${searchTxt}_C
    #${Msg}  AKHQ Msg Search All  ${KAFKA_API_URL}/topic/${topic}/data/search?sort=Newest&partition=All&searchByValue=${searchTxt}_C  #dev    3774508136
    log many  ${Msg}
    ${return}  Create List

    IF  $Msg!=[]
        #${Msg}  Convert String To Json  ${Msg}
        ${valuelist}  jsonGetObjects  ${Msg}  $..records[*].value
        #${value}  jsonGetObject  ${Msg}  $.records[${nth}].value
        FOR  ${value}  IN  @{valuelist[1]}
            IF  not ${directFlg}
                IF  $value[0]=='<'
                    ${value}  xmlStringToJson  ${value}
                ELSE IF  $value[1:-1][0]=='{'
                    ${value}  Convert String To Json  ${value}
                    ${value}  json.Loads  ${value}
                ELSE
                    ${value}  Set Variable  ${value}
                END
            ELSE
                ${value}  Set Variable  ${value}
            END
            Append To List  ${return}  ${value}
        END
    ELSE
        ${return}  Set Variable  ${Msg}
    END
    RETURN  ${return}

Get Kafka Header Return Dictionary
    [Arguments]  ${topic}=Econ_Affirmation_Out  ${searchTxt}=${EMPTY}  ${directFlg}=${False}  ${nth}=-1
    [Documentation]  Return Topic content from AKHQ for searchTxt. 
    ...    if DirectFlg is ${False}, it will change xml and json to dictionary. 
    ...    if DirectFlg is ${True}, it will return value directly. 
    ${Msg}  AKHQ Msg Search  ${KAFKA_API_URL}/topic/${topic}/data/search?sort=Newest&partition=All&searchByValue=${searchTxt}_C  #dev    3774508136
    IF  '${Msg}'!='${EMPTY}'
        ${Msg}  Convert String To Json  ${Msg}
        ${value}  jsonGetObject  ${Msg}  $.records[${nth}].headers
        IF  not ${directFlg}
            IF  '${value[1]}[0]'=='<'
                ${value}  xmlStringToJson  ${value[1]}
            ELSE IF  '${value[1]}[1:-1][0]'=='{'
                ${value}  Convert String To Json  ${value[1]}
                ${value}  json.Loads  ${value}
            ELSE
                ${value}  Set Variable  ${value}
            END
        ELSE
            ${value}  Set Variable  ${value[1]}
        END
    ELSE
        ${value}  Set Variable  ${EMPTY}
    END
    RETURN  ${value}

Get Kafka Msg Return elementTxt count for xml
    [Documentation]    Helper keyword Get Kafka Msg Return elementTxt count for xml:
    ...    run akhq Msg Search Muti Lines -> Get Length; then Log To Console; verify expected system behavior after
    ...    execution; confirm execution result matches business expectation.
    [Arguments]  ${topic}=Econ_Affirmation_Out  ${searchTxt}=${EMPTY}    ${element}=event    ${elementTxt}=Released    ${expectedMaxLength}=10    ${isXml}=true    ${noNeedElement}=false    ${isContentCheck}=${False}
    ${msgList}  akhq Msg Search Muti Lines  ${KAFKA_API_URL}/topic/${topic}/data/search?sort=Newest&partition=All&searchByValue=${searchTxt}_C
    ${msgListLength}    Get Length    ${msgList}
    Log To Console    \n****** MsgList Length: ${msgListLength},\n msgList: ${msgList}
    ${count}    Set Variable    0
    @{actualRecords}    Create List
    FOR    ${msg}    IN    @{msgList}
        ${msg}  Convert String To Json  ${msg}
        ${status}    ${allRecords}  jsonGetObject  ${msg}  $.records[*].value
        ${allRecordsLength}    Get Length    ${allRecords}
        Log To Console    \n****** allRecordsLength: ${allRecordsLength},\n allRecords:${allRecords}
        IF    "${noNeedElement}" == "true"
            IF    ${isContentCheck}
                RETURN    ${allRecords}
            ELSE
                IF    ${allRecordsLength} > ${expectedMaxLength}
                    RETURN    ${{1}}
                ELSE
                    RETURN    ${allRecordsLength}
                END
            END
        END
        # if all Records not a list
        IF    ${allRecordsLength} > ${expectedMaxLength}
            IF    "${isXml}" == "true"
                ${xml}    Parse Xml    ${allRecords}
                ${text}=    XML.Get Element Text   ${xml}    ${element}
            ELSE
                ${allRecords}  Convert String To Json  ${allRecords}
                ${status}    ${text}  jsonGetObject  ${allRecords}  $.${element}
            END

            IF    "${text}" == "${elementTxt}"
                ${count}    Set Variable    ${${count}+1}
                IF    "${isXml}" == "true"
                    Append To List    ${actualRecords}    ${xml}
                ELSE
                    Append To List    ${actualRecords}    ${allRecords}
                END
            END
        ELSE
            FOR    ${record}    IN   @{allRecords}
                IF    "${isXml}" == "true"
                    ${xml}    Parse Xml    ${record}
                    ${text}=    XML.Get Element Text   ${xml}    ${element}
                ELSE
                    ${record}  Convert String To Json  ${record}
                    ${status}    ${text}  jsonGetObject  ${record}  $.${element}
                END

                IF    "${text}" == "${elementTxt}"
                    ${count}    Set Variable    ${${count}+1}
                    Append To List    ${actualRecords}    ${record}
                END
            END
        END
    END
    Log To Console    \n******element show times:${count}
    IF    ${isContentCheck}
        RETURN  ${count}    ${actualRecords}
    ELSE
        RETURN  ${count}
    END

OffsetTimeJumpWeekendReturn2Format
    [Arguments]    ${offset_time}=0/0/0  ${output_format}=%Y-%m-%d    ${input_time}=NOW    ${input_format}=%Y-%m-%d %H:%M:%S    ${currency}=USD
    [Documentation]    0 Monday; 1 Tuesday; 2 Wednesday; 3 Thursday; 4	Friday; 5 Saturday; 6	Sunday; return 2 formats
    IF    "${currency}" == "CNO" or "${currency}" == "CNH"
            ${currency}    Set Variable    CNY
    END
    ${dateWith}  Offset Time  ${offset_time}  %Y-%m-%d    ${input_time}    ${input_format}
    ${weekday}  Evaluate  datetime.datetime.strptime($dateWith,"%Y-%m-%d").weekday()
    IF  $weekday == 5
        Log To Console    the date is Saturday, need to Jump to next Monday
        ${offset_time}    Set Variable    ${offset_time}[:-1]${${offset_time}[-1]+2}
        ${dateWith}  Offset Time  ${offset_time}  %Y-%m-%d    ${input_time}    ${input_format}
    END
    IF  $weekday == 6
        Log To Console    the date is sunday, need to Jump to next Monday
        ${offset_time}    Set Variable    ${offset_time}[:-1]${${offset_time}[-1]+1}
        ${dateWith}  Offset Time  ${offset_time}  %Y-%m-%d    ${input_time}    ${input_format}
    END
    ${output}    PostgreSQLToJson    SELECT event_name FROM ratanone.ratan_static_cashflow_currency_holiday x WHERE event_date_timestamp='${dateWith}' and iso_currency_code ='${currency}'
    ${len}    Get Length    ${output}
    WHILE    ${len}!=0
        Log To Console    \n*********holiday: ${output}, need to jump
        ${offset_time}    Set Variable    ${offset_time}[:-1]${${offset_time}[-1]+1}
        ${dateWith}  Offset Time  ${offset_time}  %Y-%m-%d    ${input_time}    ${input_format}
        ${output}    PostgreSQLToJson    SELECT event_name FROM ratanone.ratan_static_cashflow_currency_holiday x WHERE event_date_timestamp = '${dateWith}' and iso_currency_code ='${currency}'
        ${len}    Get Length    ${output}
    END
    ${date}  Offset Time  ${offset_time}  ${output_format}    ${input_time}    ${input_format}
    Log To Console    \n**********date: ${date}
    RETURN    ${date}    ${dateWith}
