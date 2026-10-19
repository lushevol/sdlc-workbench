*** Settings ***
Documentation        Writer: NI MING
...                  Created: 2023-07-18
...                  comment: Create For RatanOne
Library              Browser  show_keyword_call_banner=True  enable_playwright_debug=disabled  #auto_closing_level=MANUAL
Library              Collections
Library              String
Library              OperatingSystem
Library              DateTime
#Library              Dialogs

Library              CommonUtils.py
Resource             commonUtils.resource
Resource             playwrightExt.resource


*** Keywords ***
Browser Initial
    [Documentation]  This Keyword is used for General Browser Initial.
    ...              General put on Suite Setup
    [Tags]  Browser
    ${TIMEOUT}  Get Variable Value  ${TIMEOUT}  30
    Set Browser Timeout  ${TIMEOUT}
    Set Retry Assertions For  ${TIMEOUT}
    ${browser}  Get Variable Value  ${BROWSER}  chrome
    ${browser}  set variable  ${{"chromium" if "${browser}"=="chrome" else "${browser}"}}
    ${realEnable}  Get Variable Value  ${REALENABLE}  ${False}
    ${headlessEnable}  Get Variable Value  ${HEADLESSENABLE}  ${False}
    ${RecordEnable}  Get Variable Value  ${RECORDENABLE}  ${False}
    ${proxyEnable}  Get Variable Value  ${proxyEnable}  ${False} 
    ${TimeZone}  Get Variable Value  ${TIMEZONE}  Asia/Shanghai
    ${vrTest}  Get Variable Value  ${VRTEST}  0
    ${downloadPath}  CommonUtils.Get Download Path  ${BIZ}  ${ENV}
    ${uploadPath}  CommonUtils.Get Upload Path  ${BIZ}  ${ENV}
    ${validatePath}  CommonUtils.Get Validate Path  ${BIZ}  ${ENV}
    Set Suite Variable  ${DOWNLOAD_PATH}  ${downloadPath}
    Set Suite Variable  ${UPLOAD_PATH}  ${uploadPath}
    Set Suite Variable  ${VALIDATE_PATH}  ${validatePath}
    ${videoPath}  CommonUtils.Get Video Path  ${BIZ}  ${ENV}
    ${PROXY_URL}  Get Variable Value  ${PROXY_URL}  ${EMPTY} 
    ${PROXY_PORT}  Get Variable Value  ${PROXY_PORT}  ${EMPTY} 
    ${proxy}  Create Dictionary  server=http://${PROXY_URL}:${PROXY_PORT}

    Browser.New Browser  browser=${browser}  headless=${headlessEnable}  downloadsPath=${downloadPath}  args=["--start-maximized"]
    IF  "${vrTest}"=="0"
    #IF  "${vrTest}"=="0"
        ${viewport}  Create Dictionary  width=1980  height=1080
        ${startPayload}  Create Dictionary  ignoreHTTPSErrors=${TRUE}  acceptDownloads=True  locale=en-US  timezoneId=${TimeZone}  viewport=${viewport}
    ELSE IF  "${vrTest}"=="3"
        ${startPayload}  Create Dictionary  ignoreHTTPSErrors=${TRUE}  acceptDownloads=True  locale=en-US  timezoneId=${TimeZone}  viewport=${None}
    # IF  "${vrTest}"=="0" or "${vrTest}"=="3"
    #     ${startPayload}  Create Dictionary  ignoreHTTPSErrors=${TRUE}  acceptDownloads=True  locale=en-US  timezoneId=${TimeZone}  viewport=${None}
    # ELSE
    #     ${viewport}  Create Dictionary  width=1980  height=2300
    #     ${startPayload}  Create Dictionary  ignoreHTTPSErrors=${TRUE}  acceptDownloads=True  locale=en-US  timezoneId=${TimeZone}  viewport=${viewport} 
    END
    IF  ${RecordEnable}
        ${size}  Create Dictionary  width=1980  height=1080
        #${video}  Create Dictionary  dir=${videoPath}  size=${size}
        ${video}  Create Dictionary  size=${size}
        Set To Dictionary  ${startPayload}  recordVideo=${video}
    END
    IF  ${proxyEnable}  Set To Dictionary  ${startPayload}  proxy=${proxy}
    Set Global Variable  ${Payload}  ${startPayload}
    Lang Variable Initial

    Create Directory    ${downloadPath}${/}before
    Create Directory    ${downloadPath}${/}after
    IF  '${vrTest}'=='1'  
        Empty Directory  ${downloadPath}${/}before
    ELSE IF  '${vrTest}'=='2'
        ${count}  Count Files In Directory  ${downloadPath}${/}before
        IF  '${count}'=='0'
            FAIL  No Source Screenshot. Please change VRTEST to 1 to generate source screenshot firstly.
        ELSE
            Empty Directory  ${downloadPath}${/}after
        END
        # ${FileList}  List Files In Directory  ${downloadPath}
        # FOR  ${element}  IN  @{FileList}
        #     IF  "before_" in $element
        #         Continue For Loop
        #         #${vrTest}  Set Variable  1
        #         #Empty Directory  ${downloadPath}
        #     END
        # END
    ELSE
        Log  No Need VRTEST    
    END
    Set Global Variable  ${vrTest}  ${vrTest}
    # ${size}  Create Dictionary  width=1980  height=3080
    # Set To Dictionary  ${startPayload}  viewport=${size}

Browser Open
    [Documentation]  This Keyword is used for Open Browser Page.
    ...              General put on Test Setup or Setup
    ...              Arguments:
    ...              - ``url``: access url
    ...              Example:
    ...              a. Browser Open  http://www.baidu.com
    ...              b. Browser Open  ${LOGIN_URL}
    [Tags]  Browser
    [Arguments]  ${url}
    #[Arguments]  ${url}
    ${mWebEnable}  Get Variable Value  ${MWEBENABLE}  ${False} 
    ${startPayload}  Get Variable Value  ${Payload}  ${EMPTY}
    ${device}  Get Device  Galaxy S8
    IF  ${mWebEnable}  Set To Dictionary  ${startPayload}  &{device}
    #IF  ${mWebEnable}  Remove From Dictionary  ${startPayload}  viewport

    ${ContextPath}  ${LoginFlg}  ContextExist
    IF  ${LoginFlg}  Set To Dictionary  ${startPayload}  storageState=${ContextPath}
    Set Suite Variable  ${LoginFlg}  ${LoginFlg}
    Set Suite Variable  ${ContextPath}  ${ContextPath}
    VAR  ${startPayload}  ${startPayload}  scope=Global
    #IF  not ${storage}  Empty Directory  ${ContextPath}
    Browser.New Context  &{startPayload}  ignoreHTTPSErrors=True
    Browser.New Page  ${url}
    # ${Handle}  Get Handle
    # RETURN  ${Handle}

ContextExist
    [Documentation]  This Keyword is used for Check context exist or not on credential folders
    ...              Arguments:
    ...              - ``Project``: Project Name
    ...              Return:
    ...              - ``ContextPath``: If exist return contextpath
    ...              - ``LoginFlg``: Return login Bool
    [Tags]  Browser
    ${ContextDir}  CommonUtils.Get Credential Path  ${BIZ}  ${ENV} 
    ${ContextFile}  Set Variable  LoginContext_${BIZ}_${ENV}.json
    ${ContextPath}  Set Variable  ${ContextDir}${/}${ContextFile}
    ${FileList}  OperatingSystem.List Files In Directory  ${ContextDir}
    ${LoginFlg}  Run Keyword And Return Status  Should Contain  ${FileList}  ${ContextFile}
    IF  ${LoginFlg} 
        ${CreateDate}  Get Modified Time  ${ContextPath}  epoch
        ${CurrentDate}  Get Time  epoch
        ${LoginFlg}   Evaluate  (${CurrentDate}-${CreateDate})<600
        # ${TimeoutFlg}  Evaluate  (${CurrentDate}-${CreateDate})<3600
        # ${LoginFlg}  Set Variable  ${TimeoutFlg}
    END
    ${storage}  Get Variable Value  ${STORAGE}  ${True} 
    RETURN  ${ContextPath}  ${{$LoginFlg and $storage}}

Close
    [Documentation]  This Keyword is used for Close Browser. General no need use.  it will close browser automaticly.
    [Tags]  Browser
    ${debug}  Get Variable Value  ${ROBOTDEBUG}  ${False}
    #Run Keyword If  '${debug}'=='True' and '${SUITE_STATUS}'=='FAIL'  Dialogs.Pause Execution  Pause exection due to failure, click OK to continute
    # [Teardown]  Run Keyword IF  '${SUITE_STATUS}'=='FAIL'  Browser.Take Screenshot  fullPage=True  fileType=png  timeout=30s

GoTo
    [Documentation]  This Keyword is used for Goto Url
    ...              Arguments:
    ...              - ``url``: goto url
    [Tags]  Browser
    [Arguments]  ${url}
    Browser.Go To  ${url}

GetHandler
    [Documentation]  Get Page Handler
    ...              Return:
    ...              - ``Handle``: page handler
    [Tags]  Browser
    ${CurrentBrowser}  Browser.Switch Browser  CURRENT
    ${CurrentContext}  Browser.Switch Context  CURRENT
    ${CurrentPage}  Browser.Switch Page  CURRENT
    ${handler}  Create List  ${CurrentPage}  ${CurrentContext}  ${CurrentBrowser}  
    RETURN  ${handler}

SwitchHandler
    [Documentation]  Switch Page Handler
    ...              Arguments:
    ...              - ``Handle``: page handler
    [Tags]  Browser
    [Arguments]  ${handler}
    Browser.Switch Browser  ${handler}[2]
    Browser.Switch Context  ${handler}[1]
    Browser.Switch Page  ${handler}[0]

CloseHandler
    [Documentation]  Close Page Handler
    ...              Arguments:
    ...              - ``Handle``: page handler
    [Tags]  Browser
    [Arguments]  ${handler}
    Browser.Close Page  ${handler}[0]  ${handler}[1]  ${handler}[2]

FindExistElementP
    [Documentation]  This Keyword is used for Check element is existed or not
    ...              Arguments:
    ...              - ``elements``: check element exist
    ...              Return:
    ...              - ``findElementFlg``: element exist bool
    ...              - ``element``: if exist return element locator
    [Tags]  Element  ExpandsKeyword
    [Arguments]  ${selector}
    log many  ${selector}
    ${findElementFlg}  Set Variable  ${False}
    ${elements}  String.Split String  ${selector}  ||
    # ${eles}  Browser.Get Elements  ${elements} 
    # ${ele_count}  Get Length  ${eles}
    FOR  ${element}  IN  @{elements}
        ${result}  Run Keyword And Return Status  Browser.Wait For Elements State  ${element}  stable
        ${findElementFlg}  Run Keyword If  ${result}  Set Variable  ${True}
        ...  ELSE  Set Variable  ${False}
        Exit For Loop If  ${result}
    END
    #IF  not ${findElementFlg}  Browser.Take Screenshot  fullPage=True  fileType=png  timeout=30s  #quality=50        IF  not ${findElementFlg}  FAIL  Element does not find for ${elements}!
    #Browser.Wait For Elements State  css=.ant-spin-dot-spin  detached
    Browser.Highlight Elements  ${element}  duration=100ms  width=4px  style=dotted  color=pink
    RETURN  ${findElementFlg}  ${element}
   # [Teardown]  Run Keyword If Test Failed  Browser.Take Screenshot  fullPage=True  fileType=jpeg  timeout=30s  quality=50 

Right Click
    [Documentation]  This Keyword is used for Right Click Element
    ...              Arguments:
    ...              - ``elements``: Right Click Element
    #Right Click to 
    [Tags]  Element
    [Arguments]  ${selector}
    ${findElementFlg}  ${element}  findExistElementP  ${selector}
    Run Keyword If  ${findElementFlg}  Browser.Click With Options   
    ...  selector=${selector}   
    ...  button=right

Double Click
    [Documentation]  This Keyword is used for DoubleClick Element
    ...              Arguments:
    ...              - ``elements``: DoubleClick Element
    [Tags]  Element
    [Arguments]  ${selector}
    ${findElementFlg}  ${element}  findExistElementP  ${selector}
    Run Keyword If  ${findElementFlg}  Browser.Click With Options  
    ...  selector=${element}  
    ...  delay=100ms  
    ...  clickCount=2

Click
    [Documentation]  This Keyword is used for Click Element
    ...              Arguments:
    ...              - ``elements``: Click Element
    [Tags]  Element
    [Arguments]  ${selector}  ${pre_sleeptime}=0  ${post_sleeptime}=0
    sleep  ${pre_sleeptime}
    ${findElementFlg}  ${element}  findExistElementP  ${selector}

    #Set Global Variable  ${vrTest}  3
    # IF  "${vrTest}"=="3"
    #     Run Keyword And Ignore Error  Screenshot
    # END
    #Run Keyword And Ignore Error  VRTest  ${True}
    #sleep   0.5s
    Run Keyword If  ${findElementFlg}  Browser.Click  ${element}  #force=${True}
    sleep  ${post_sleeptime}

Clicks
    [Documentation]  This Keyword is used for Click Element
    ...              Arguments:
    ...              - ``elements``: Click Element
    [Tags]  Element
    [Arguments]   @{selectors}  
    FOR  ${selector}  IN  @{selectors}
        Click  ${selector}   #  pre_sleeptime=${pre_sleeptime}  post_sleeptime=${post_sleeptime}
        Sleep  1.5
    END


Type
    [Documentation]  This Keyword is used for Input Text
    ...              Arguments:
    ...              - ``elements``: Type Element
    ...              - ``value``: Type content
    ...              - ``delay``: delay input. default is 0ms. not delay
    ...              - ``ClearFlg``: False/True. If clear text, default is True
    [Tags]  Element
    [Arguments]  ${selector}  ${value}  ${delay}=0ms  ${ClearFlg}=True
    ${findElementFlg}  ${element}  findExistElementP  ${selector}
    Run Keyword If  ${findElementFlg}  Browser.Type Text  ${element}  ${value}  delay=${delay}  clear=${ClearFlg}

# Select
#     [Documentation]  This Keyword is used for Select on Dropdown
#     ...              Arguments:
#     ...              - ``elements``: Select Element
#     ...              - ``value``: Select content
#     [Tags]  Element
#     [Arguments]  ${element}  ${value}
#     #Browser.Select From List By Value  ${element}  ${value}
#     log  maintance later

Select Radio Btn
    [Documentation]  Select By radio Button
    ...              Arguments:
    ...              - ``elements``: css, xpath, id, name support. format is css=.abc or xpath=//abc
    [Tags]  Element
    [Arguments]  ${selector}
    #${findElementFlg}    ${element}    findExistElement    ${elements}
    ${findElementFlg}  ${element}  findExistElementP  ${selector}
    IF  ${findElementFlg}  Browser.Check Checkbox  ${element}

Hover Click
    [Documentation]  Hover ParentMenu and Click ChildMenu
    ...              Arguments:
    ...              - ``ParentMenu``: the first class menu
    ...              - ``ChildMenu``: the second class menu
    [Tags]  Element
    [Arguments]  ${ParentMenu}  ${ChildMenu}
    Browser.Hover  "${ParentMenu}"
    Browser.Click  "${ChildMenu}"

Checkbox Select
    [Tags]  Element
    [Documentation]  Select check box
    ...              Arguments:
    ...              - ``elements``: css, xpath, id, name support. format is css=.abc or xpath=//abc
    [Arguments]  ${selector}  ${selectFlg}=True
    ${findElementFlg}  ${element}  findExistElementP  ${selector}
    IF  ${findElementFlg}
        #Browser.Check Checkbox  ${element} >> input
        Run Keyword  Browser.${{'' if '${selectFlg}'=='True' or '${selectFlg}'=='Y' else 'un'}}Check Checkbox  ${element} >> input
    END

Select Checkbox
    [Tags]  Element
    [Documentation]  Select check box
    ...              Arguments:
    ...              - ``elements``: css, xpath, id, name support. format is css=.abc or xpath=//abc
    [Arguments]  ${selector}
    ${findElementFlg}  ${element}  findExistElementP  ${selector}
    IF  ${findElementFlg}  Browser.Check Checkbox  ${element} >> input

UnSelect Checkbox
    [Documentation]  UnSelect check box
    ...              Arguments:
    ...              - ``elements``: css, xpath, id, name support. format is css=.abc or xpath=//abc
    [Tags]  Element
    [Arguments]  ${selector}
    ${findElementFlg}  ${element}  findExistElementP  ${selector}
    IF  ${findElementFlg}  Browser.Uncheck Checkbox  ${element} >> input

SendKeys
    [Documentation]  SendKeys to element
    ...              Arguments:
    ...              - ``element``: css, xpath, id, name support. format is css=.abc or xpath=//abc
    ...              - ``value``: key
    [Tags]  Element
    [Arguments]  ${selector}  ${value}
    Browser.Press Keys  ${selector}  ${value}

Wheel
    [Arguments]  ${selector}  ${direction}=V  ${step}=250  ${times}=10
    [Documentation]  section upload file Horizontal/Vertical H/V
    ...              Arguments:
    ...              - ``selector``: fix selector
    ...              - ``direction``: H/V, means Horizontal or Vertical
    # //div[@role='row'][@row-index][descendant::div[@col-id!='0']] >> nth=0
    Hover  ${selector}
    FOR  ${i}  IN RANGE  0  ${times}
        IF  "${direction.upper()}"=="V"
            Mouse Wheel  0  ${step}
        ELSE
            Mouse Wheel  ${step}  0
        END
    END

    # Wheel  
    # ...    selector=//div[@role='row'][@row-index][descendant::div[@col-id!='0']] >> nth=0
    # ...    direction=H
    # ...    step=200
    # ...    times=6

GetTableCell
    [Documentation]  Get Table Cell
    ...              Arguments:
    ...              - ``table``: table locator
    ...              - ``column``: column from 0
    ...              - ``row``: row from 0
    [Tags]  Table
    [Arguments]  ${table}  ${column}  ${row}
    ${element}  Browser.Get Table Cell Element  ${table}  ${column}  ${row}
    ${innerHTML}  Evaluate JavaScript  ${element}  el=>el.innerHTML
    IF  '<input' in $innerHTML
        ${value}  Get Attribute    ${element} >> input    value
    ELSE
        ${value}  Browser.Get Text  ${element}
        #${value}  GetElementText  ${element}
    END
    #${value}  Evaluate JavaScript  ${element}  el=>el.value
    RETURN  ${value}

# GetElementText
#     [Documentation]  Get Element Cell
#     [Arguments]  ${element} 
#     Set Browser Timeout    0.5
#     log many  ${element} 
#     Set Browser Timeout    ${TIMEOUT}
#     ${elements}  Create List  ${element}
#     ${value}  Set Variable
#     FOR    ${ele}    IN    @{elements}
#         ${value1}  get text  ${ele}
#         IF  $value1=='${EMPTY}'
#            ${value1}  Get Attribute    ${ele}    value
#         END
#         ${value}  Set Variable  ${value}${value1}
#     END
#     RETURN  ${value}

GetElementText
    [Documentation]  Get Element Cell
    [Arguments]  ${element} 
    Set Browser Timeout    0.1
    log many  ${element} 
    ${value}  Get Text  ${element}
    IF  $value==''
        # ${result}  Run Keyword And Return Status  log  ${element} >> input
        ${status}  Run Keyword And Return Status  Browser.Get Element  ${element} >> input
        IF  ${status}
            ${value_status}  Run Keyword And Return Status  Get Attribute  ${element} >> input  value
            IF  ${value_status}
                ${value}  Get Attribute  ${element} >> input  value
            ELSE
                VAR  ${value}  ${EMPTY}
            END
        ELSE
            ${value}  Get Text  ${element}
        END
    ELSE
        ${value}  Get Text  ${element}
    END

    # Set Browser Timeout    ${TIMEOUT}
    # ${elements}  Create List  ${element}
    # ${value}  Set Variable
    # FOR    ${ele}    IN    @{elements}
    #     ${value1}  get text  ${ele}
    #     IF  $value1=='${EMPTY}'
    #        ${value1}  Get Attribute    ${ele}    value
    #     END
    #     ${value}  Set Variable  ${value}${value1}
    # END
    RETURN  ${value}

GetElementTexts
    [Documentation]  Get Element Cell
    [Arguments]  ${element} 
    ${attrs}  Get Attribute Names  ${element}
    IF  "value" in $attrs
        ${value}  Get Attribute  ${element}  value
    ELSE
        ${value}  Get Text  ${element}
    END

    # Set Browser Timeout    0.5
    # log many  ${element} 
    # IF  "element=" in $element
    #     ${elements}  Browser.Get Elements    ${element} >> //descendant-or-self::*[string-length(text())>0][not(contains(@class,"placeholder"))] 
    # ELSE
    #     #${elements}  Browser.Get Elements    (${element})//*[string-length(text())>0][not(contains(@class,"placeholder"))] | (${element})//input
    #     ${elements}  Browser.Get Elements    (${element})//descendant-or-self::*[string-length(text())>0][not(contains(@class,"placeholder"))] | (${element})//input
    # END
    # Set Browser Timeout    ${TIMEOUT}
    # ${value}  Set Variable
    # FOR    ${ele}    IN    @{elements}
    #     ${value1}  get text  ${ele}
    #     IF  $value1=='${EMPTY}'
    #        ${value1}  Get Attribute    ${ele}    value
    #     END
    #     ${value}  Set Variable  ${value}${value1}
    # END
    RETURN  ${value}
    
    # ${innerHTML}  Evaluate JavaScript  ${element}  el=>el.innerHTML
    # #log many  ${innerHTML} 
    # ${value}  Set Variable
    # IF  '<input' in $innerHTML
    #         ${lists}  Browser.Get Elements  ${element} >> input
    #         FOR    ${list}    IN    @{lists}
    #             ${value1}  Get Attribute    ${list}    value
    #             ${value}  Set Variable  ${value}${value1}
    #         END
    # END


    # ${innerHTML}  Evaluate JavaScript  ${element}  el=>el.innerHTML
    # log many  ${innerHTML} 
    # ${value}  Set Variable

    # IF  '<input' not in $innerHTML and 'title=' not in $innerHTML
    #     ${value}  Browser.Get Text  ${element}
    # ELSE
    #     IF  '<input' in $innerHTML
    #         ${lists}  Browser.Get Elements  ${element} >> input
    
    #         FOR    ${list}    IN    @{lists}
    #             ${value1}  Get Attribute    ${list}    value
    #             ${value}  Set Variable  ${value}${value1}
    #         END
    #     END

    #     Get Table Cell Element    table    column    row
    
    #     IF  'title=' in $innerHTML
    #         ${lists}  Browser.Get Elements  ${element} >> //*[@title]
    #         FOR    ${list}    IN    @{lists}
    #             ${value1}  Get Attribute    ${list}    title
    #             ${value}  Set Variable  ${value}${value1}
    #         END
    #     END
    # END

Upload Attachment
    [Documentation]  Upload Attachment
    ...              Arguments:
    ...              - ``element``: locator of upload input
    ...              - ``filename``: upload file name.  upload file in project/data/upload
    [Arguments]  ${selector}  ${filename}
    [Tags]  Element
    # ${path}  CommonUtils.Get Attachment File Path    filename=${filename}   env_type=${ENV}   biz_type=${BIZ}
    Browser.Upload File By Selector  ${selector}  ${filename}

Download Promise
    [Documentation]  Download Attachment Promise。  Used after click download link
    ...              Arguments:
    ...              - ``element``: click element to donwload
    ...              - ``saveAsPath``: download path. download file in project/data/download
    [Arguments]  ${selector}  ${saveAsPath}
    ${dl_promise}  Browser.Promise To Wait For Download  saveAs=${saveAsPath}
    Click  ${selector}
    ${file_obj}  Browser.Wait For  ${dl_promise}
    OperatingSystem.File Should Exist   ${file_obj}[saveAs]  download file fail.

Expand Element
    [Documentation]  Expand element
    ...              Arguments:
    ...              - ``element``: locator of expand element
    [Arguments]  ${selector}
    [Tags]  Element
    ${class}  Get Attribute  ${selector}  class
    IF  "collapsed" in "${class}"
        Browser.Click  ${selector}
    END

Collapsed Element
    [Documentation]  Collapsd element
    ...              Arguments:
    ...              - ``element``: locator of Collapsed element
    [Arguments]  ${selector}
    [Tags]  Element
    ${class}  Get Attribute  ${selector}  class
    IF  "expand" in "${class}"
        Browser.Click  ${selector}
    END    

Select Switch
    [Documentation]  Select SP Switch Btn
    ...              Arguments:
    ...              - ``locator``: element xpath
    ...              - ``status``: True or False
    [Tags]  Element Advance
    [Arguments]  ${locator}  ${status}
    FindExistElementP    ${locator}
    ${element}  Set Variable  ${locator} >> nth=-1 >> button
    ${current_status}  Get Attribute  ${element}  aria-checked
    IF  "${current_status}"!="${status}"  playwright.Click  ${locator} >> nth=-1 >> button

# Select Single Date With Time
#    [Arguments]    ${class}      ${date_time}
#    [Tags]   DatePicker
#    ${date_time_ele}   Split String  ${date_time}
#    ${date}  ${time}   Set Variable  ${date_time_ele}
#    Select Single Date  ${class}  ${date}
#    Select Single Time  ${class}  ${time}
#    ${locator}    String.Format String    ${_single_date_picker_footer}    class=${class}
#    Click Button  ${locator}   OK

# Select Date Period With Time
#    [Arguments]    ${class}      ${start_date_time}       ${end_date_time}
#    [Tags]   DatePicker
#    FOR  ${date_element}  IN  ${start_date_time}  ${end_date_time}
#        ${date_time_ele}   Split String  ${date_element}
#        ${date}  ${time}   Set Variable  ${date_time_ele}
#        Select Single Date  ${class}  ${date}
#        Select Single Time  ${class}  ${time}
#        ${locator}  Set Variable   //ul[@class='${class}-ranges']
#        Click Button  ${locator}  OK
#    END

# Select Single Time
#    [Arguments]    ${class}      ${time}
#    [Tags]   DatePicker
#    ${time_element}  Split String  ${time}  :
#    ${hour}  ${mintue}  ${second}  Set Variable  ${time_element}
#    ${index}  Set Variable  ${1}
#    FOR  ${ele}  IN  ${hour}  ${mintue}  ${second}
#         ${time_locator}  String.Format String    ${_single_time_locator}     class=${class}    index=${index}  time=${ele}
#         LoggingToConsole  ${time_locator}
#         Hover  ${time_locator}
#         Click  ${time_locator}
#         ${index}  Set Variable   ${${index}+${1}}
#    END

# Get Current TimeStamp
#    [Tags]   Date
#    ${date}   Get Current Date
#    ${datestamp}   Convert Date	${date}	epoch
#    RETURN  ${datestamp}

# SendNotificationEdit
#    [Arguments]    ${locator}   ${subject}=${None}    ${content}=${None}
#    [Tags]   SendNotificationEdit
#    IF  ${subject} != ${None}
#         ${user_notification_subject}  String.Format String    ${_user_notification_subject}   locator=${locator}
#         Fill Text    ${user_notification_subject}    ${subject}
#    END
#    ${count}  Get Length   ${content}
#    IF  ${count} > 0
#         ${text}  Set Variable  ${EMPTY}
#         FOR    ${element}    IN    @{content}
#               ${text}  Catenate  SEPARATOR=\n	  ${text}   ${element}
#         END
#         ${user_notification_content}  String.Format String    ${_user_notification_content}   locator=${locator}
#         Fill Text    ${user_notification_content}    ${text}
#    END
#    Browser Screenshot   name=SendNotificationEdit   status=success

# ClickDrawerLinkOnTableRows
#    [Arguments]      ${locator}       ${match_value}=${None}
#    [Tags]   Table
#    Wait For List Elements State  ${locator}
#    @{table_list}  Get Table List   ${locator}
#    LoggingToConsole    ${table_list}
#    ${length}  Get Length  ${table_list}
#    Should Be True   ${length} > 0   search table result is empty.
#    ${row_index}  Set Variable  ${1}
#    ${cell_index}  Set Variable  ${-1}
#    IF  '${match_value}'!='None'
#        FOR  ${table_row_list}  IN  @{table_list}
#          ${cell_index}   Get Index From List   ${table_row_list}	${match_value}
#          IF  ${cell_index} > 0    BREAK
#          ${row_index}  Set Variable   ${${row_index}+${1}}
#        END
#        IF  ${cell_index} > 0
#             ${link}   String.Format String    ${_table_link}  locator=${locator}   row_index=${row_index}  cell_index=${${cell_index}+${1}}
#             Click  ${link}
#        END
#    END

# ClickPaginationPrev
#   [Arguments]    ${class}
#   ${pagination_prev}   String.Format String   ${_click_pagination_prev}    class=${class}
#   Click   ${pagination_prev}

# ClickPaginationNext
#   [Arguments]    ${class}
#   ${pagination_next}   String.Format String   ${_click_pagination_next}    class=${class}
#   Click   ${pagination_next}

# ClickPaginationItem
#   [Arguments]    ${class}   ${index}
#   ${pagination_item}   String.Format String   ${_click_pagination_item}    class=${class}   index=${index}
#   Click   ${pagination_item}

# ClickPaginationEllipsis
#   [Arguments]    ${class}  ${index}=1
#   ${pagination_ellipsis}   String.Format String   ${_click_pagination_ellipsis}    class=${class}  index=${index}
#   Click   ${pagination_ellipsis}

# InputPaginationJumperPage
#   [Arguments]    ${class}   ${page}
#   ${pagination_jumper}   String.Format String   ${_input_pagination_jumper}    class=${class}
#   Fill Text   ${pagination_jumper}    ${page}
#   Click   ${pagination_jumper}

# ClickPaginationOption
#   [Arguments]    ${class}   ${index}
#   ${pagination_options}   String.Format String   ${_click_pagination_options}    class=${class}
#   Click   ${pagination_options}
#   ${page}      CommonUtils.Get Text By Language     ${LANGUAGE}     page
#   ${pagination_options_detail}   String.Format String   ${_click_pagination_options_list}    class=${class}   index=${index}  page=${page}
#   Click   ${pagination_options_detail}

# ClickAttchmentTableDownloadIcon
#   [Arguments]   ${locator}    ${row_index}    ${cell_index}    ${filename}
#   ${download_locator}  String.Format String   ${_attachment_first_img_locator}    locator=${locator}  row=${row_index}   cell=${cell_index}
#   Download File    locator=${download_locator}    filename=${filename}

# ClickAttchmentTableDeleteIcon
#   [Arguments]   ${locator}    ${row_index}    ${cell_index}
#   ${delete_locator}  String.Format String   ${_attachment_delete_locator}    locator=${locator}  row=${row_index}   cell=${cell_index}
#   Click  ${delete_locator}

# ClickAttchmentTableViewIcon
#   [Arguments]   ${locator}    ${row_index}    ${cell_index}
#   ${view_locator}  String.Format String   ${_attachment_first_img_locator}    locator=${locator}  row=${row_index}   cell=${cell_index}
#   Click   ${view_locator}
#   Click   ${_click_close_btn}
