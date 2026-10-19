*** Settings ***
Documentation        Writer: NI MING
...                  Created: 2024-09-08
...                  comment: Create For RATANONE
... 
# Suite Setup          Browser Initial
Suite Setup          Run Keywords  Disable Warnings  AND  SUITE Initial  AND  Browser Initial  AND  Login RatanOne  ${USERNAME_MO}  ${PASSWORD_MO}
Resource             __import__.resource
# Library              DataDriver  file=TR-UI-tb-cases.xlsx  sheet_name=${SUITE NAME.lower()}

*** Variables ***
${sleeptime}          960

*** Test Cases ***
BAU-UI-RP-LOGIN-001-001
    [Documentation]  Login System and check Tile click success
    [Tags]  RATAN  POSTTRADEPORTAL
    When I click <Trade Blotter> Tile
    Then I should see the tile page success

BAU-UI-RP-LOGIN-001-002
    [Documentation]  check profile success
    [Tags]  RATAN  POSTTRADEPORTAL
    Given I am on ratan webpage
    When I click User Profiles icon
    Then I should see <Sylvia Chen> login success

BAU-UI-RP-LOGIN-001-003
    [Documentation]  check profile details success
    [Tags]  RATAN  POSTTRADEPORTAL
    Given I am on ratan webpage
    When I click <Sylvia Chen> profile
    Then I should see <Liyun.Chen@sc.com> profile detail

BAU-UI-RP-LOGIN-001-004
    [Documentation]  logout success
    [Tags]  RATAN  POSTTRADEPORTAL
    Given I am on ratan webpage
    And I click User Profiles icon
    When I click logout btn
    Then I should see <Sign In> success

BAU-UI-RP-LOGIN-001-005
    [Documentation]  relogin system success
    [Tags]  RATAN  POSTTRADEPORTAL
    Given I am on ratan webpage
    AND I login with username <${USERNAME_MO}> and password <${PASSWORD_MO}>
    When I click <Trade Blotter> Tile
    Then I should see the tile page success

BAU-UI-RP-LOGIN-001-006
    [Documentation]  extend system success
    [Tags]  RATAN  POSTTRADEPORTAL
    Given I am on ratan webpage
    When Wait for more than 15 mins and Click Entend btn on Your session has been expired window
    AND I click <MO Rules> Tile
    Then I should see <LIVE> success

BAU-UI-RP-LOGIN-001-007
    [Documentation]  extend system success
    [Tags]  RATAN  POSTTRADEPORTAL
    comment  ======Step1: Creat CrashFlow Testdata for CN Systerm======
    ${cflist}  Generate Cashflows data
    comment  ======Step2: Open Browser1======
    # Open Browser1
    Login RatanOne and Goto Tile
    ...  username=${USERNAME_FMO_CN_CHECKER1}  
    ...  password=${PASSWORD_FMO_CN_CHECKER1}  
    ...  tile="Cashflow Blotter" >> nth=1
    Wait For Elements State  selector=${_common_currentTab} >> "Search"
    Waiting for Element Hidden  "Please wait..."
    ${cashflowIds}=    Evaluate    ','.join(${cfList})
    Element Operate  
    ...  Cashflow ID=1||${cashflowIds}
    Click  selector=${_common_currentTab} >> "Search"
    sleep  5s
    ${TABLE_DICT}  DivTableWheel  view=M  nth=-1
    Log To Console    ${TABLE_DICT}
    ${first_item}  Set Variable  ${TABLE_DICT}[0]
    ${Cashflow State}  Set Variable  ${first_item['Cashflow Sub State Type']}
    Run Keyword And Continue On Failure  Should Be Equal  ${Cashflow State}  Pending Exception
    ${Cashflow Amount}  Set Variable  ${first_item['Amount']}
    Run Keyword And Continue On Failure  Should Be Equal   ${Cashflow Amount}  0.01  


BAU-UI-RP-LOGIN-001-008
    [Documentation]  extend system success
    [Tags]  RATAN  POSTTRADEPORTAL
    comment  ======Step1: Open Browser1======
    Browser Open  url=${LOGIN_URL}
    # Open Browser1
    Element Operate  
    ...  Username=1||${USERNAME_NO}
    ...  Password=1||${PASSWORD_NO}
    ...  Sign In||-1=0
    Wait For Elements State  selector="${MARKETS_OPERATIONS_ONE}"
    Click    "New Tile"
    Sleep    3S
    Wait For Elements State    xpath=//section[@class='MicroWebUI_Base_drawer-body']//div[@class='MuiBox-root css-1ant923']
    ${text}=    Get Text    xpath=//section[@class='MicroWebUI_Base_drawer-body']//div[@class='MuiBox-root css-1ant923']
    Should Be Equal As Strings    ${text.strip()}    ${EMPTY}


# BAU-UI-RP-LOGIN-001-004
#     [Documentation]  Normal Logout
#     I am on the RATAN login page
#     I login with username <${USERNAME_MO}> and passwoed <${PASSWORD_MO}>
#     I Click <Trade Blotter> Tile
#     I should see the tile page success
#     I should see <Sylvia Chen> login success
#     # Clicks  "Close"  //*[@alt='Avatar']  "Logout"  data-testid=Logout_Btn
#     # # ...  data-testid="Logout_Btn"
#     # # ...  
#     # # ...  "Logout"
#     # Wait For Elements State  selector="Sign In" >> nth=0
#     # # Given I have login success
#     # # When I Click <Logout> Button on 
#     # # Then I should see logout success

*** Keywords ***
I am on the RATAN login page
    [Documentation]    Helper keyword I am on the RATAN login page:
    ...    run Browser Open; verify expected system behavior after execution; confirm execution result matches business;
    ...    expectation.
    #Browser Initial 
    Browser Open  url=${LOGIN_URL}

I login with username <${USERNAME}> and password <${PASSWORD}>
    [Documentation]    Helper keyword I login with username <${USERNAME}> and password <${PASSWORD}>:
    ...    run Element Operate -> Wait For Elements State; verify expected system behavior after execution; execution;
    ...    result matches business expectation.
    # Login Ratanone
    Element Operate  
    ...  Username=1||${USERNAME}
    ...  Password=1||${PASSWORD}
    ...  Sign In||-1=0
    Wait For Elements State  selector="${MARKETS_OPERATIONS_ONE}"

I click <${TILE NAME}> Tile
    [Documentation]    Helper keyword I click <${TILE NAME}> Tile:
    ...    run Click Tile; verify expected system behavior after execution; confirm execution result matches business;
    ...    expectation.
    # Open Tile
    Click Tile  "${TILE NAME}"

I should see the tile page success
    [Documentation]    Helper keyword I should see the tile page success:
    ...    run Wait For Elements State -> Waiting for Element Hidden; verify expected system behavior after execution;
    ...    confirm execution result matches business expectation.
    Wait For Elements State  selector=${_common_currentTab} >> "Search"
    Waiting for Element Hidden  text=/loading...|Please wait.../
    #Wait For Elements State  selector="Quick Search" >> nth=0
    
I am on ratan webpage
    [Documentation]    Helper keyword I am on ratan webpage:
    ...    run Log to console; verify expected system behavior after execution; confirm execution result matches business;
    ...    expectation.
    Log to console  I am on ratan webpage

I click User Profiles icon
    [Documentation]    Helper keyword I click User Profiles icon:
    ...    run Click; verify expected system behavior after execution; confirm execution result matches business;
    ...    expectation.
    Click  //*[@alt='Avatar']

I should see <${USERNAME}> login success
    [Documentation]    Helper keyword I should see <${USERNAME}> login success:
    ...    run Account Assertion; verify expected system behavior after execution; confirm execution result matches;
    ...    business expectation.
    Account Assertion  username=${USERNAME}
    
I click <${PROFILE NAME}> profile
    [Documentation]    Helper keyword I click <${PROFILE NAME}> profile:
    ...    run Click; verify expected system behavior after execution; confirm execution result matches business;
    ...    expectation.
    Click  "${PROFILE NAME}"

I should see <${PROFILE NAME}> profile detail
    [Documentation]    Helper keyword I should see <${PROFILE NAME}> profile detail:
    ...    run Wait For Elements State -> Click; verify expected system behavior after execution; confirm execution result;
    ...    matches business expectation.
    Wait For Elements State  selector="${PROFILE NAME}"
    Click  "Close"

I click logout btn
    [Documentation]    Helper keyword I click logout btn:
    ...    run Clicks; verify expected system behavior after execution; confirm execution result matches business;
    ...    expectation.
    Clicks   "Logout"  data-testid=Logout_Btn  #"Close"  //*[@alt='Avatar'] 
    #Wait For Elements State  selector="Sign In" >> nth=0

I should see <${TEXT}> success
    [Documentation]    Helper keyword I should see <${TEXT}> success:
    ...    run Wait For Elements State; verify expected system behavior after execution; confirm execution result matches;
    ...    business expectation.
    Wait For Elements State  selector="${TEXT}" >> nth=0    #

Wait for more than 15 mins and Click Entend btn on Your session has been expired window
    [Documentation]    Helper keyword Wait for more than 15 mins and Click Entend btn on Your session has been expired window:
    ...    run Set Variable -> Wait For Elements State; then Click; verify expected system behavior after execution;
    ...    confirm execution result matches business expectation.
    ${time}  Set Variable  ${sleeptime}
    Wait For Elements State  selector="Your session has been expired"  timeout=${time}
    Click  data-testid=Extend_Btn


Generate Cashflows data
    [Documentation]    Helper keyword Generate Cashflows data:
    ...    run Create List -> GenCashFlowCN; then Append To List; verify expected system behavior after execution;
    ...    execution result matches business expectation.
    ${cfList}    Create List
    ${cashflowId}  GenCashFlowCN  template=new  upstream=murex  isCredit=N  transactionFamily=COM  transactionGroup=SWAP
    ...    counterpartyFMID=400899993  entityFMID=400085753  currency=CNO    validationLevel=TRAD    counterpartyFlag=NOTINTERNAL
    Append To List    ${cfList}    ${cashflowId}
    Log To Console    ${cashflowId}
    Log To Console    ${cfList}
    Sleep    0.5s   
    RETURN  ${cfList}
