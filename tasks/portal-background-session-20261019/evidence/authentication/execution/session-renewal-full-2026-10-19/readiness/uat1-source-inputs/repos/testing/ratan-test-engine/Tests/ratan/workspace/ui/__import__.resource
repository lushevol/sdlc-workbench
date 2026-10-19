*** Settings ***
Documentation        Writer: NI MING
...                  Created: 2023-07-18
...                  comment: Create For RatanOne

# Common Resource
Library              FakerLibrary  zh_CN    #en_US
Library              urllib3
Library              RequestsLibrary
Library              AsyncLibrary
Library              String

# Util Resource
Library              ../../../../Resources/keywords/CommonUtils.py
Resource             ../../../../Resources/keywords/commonUtils.resource

# Keyword Resource
Resource             ../../../../Resources/keywords/playwright.resource
Resource             ../../../../Resources/keywords/playwrightExt.resource
Resource             ../../../../Resources/keywords/business_common.resource
Resource             ../../../../Resources/keywords/commonBiz.resource
Resource             ../../../../Resources/keywords/commonUtils.resource

# Plugin Resource
Resource             ../../plugin/api/keyword-api-common.resource
Resource             ../../plugin/api/keyword-api-cn.resource
Resource             ../../plugin/api/keyword-api-trade-review.resource
Resource             ../../plugin/api/keyword-api-loaniq.resource
Resource             ../../plugin/api/keyword-api-bau-manual.resource
Resource             ../../plugin/api/keyword-api-bau.resource
Resource             ../../plugin/api/keyword-api-iso.resource
Resource             ../../plugin/api/keyword-api-cn-checkResult.resource

# Locator Resource
Resource             ../../../../Resources/locators/locators_common.resource
Resource             ../../../../Resources/locators/locators_business.resource
Resource             ../../../../Resources/locators/locators_cn.resource

# Data
Variables            ../../data/properties.yaml
Variables            ../../data/certificate.yaml
Variables            ../../data/env_${ENV}_${SECRET}.yaml
Variables            ../../../../Resources/data/language.yaml

# Cryp Resource
Library              CryptoLibrary  variable_decryption=True  key_path=${EXECDIR}${/}Resources${/}data${/}keypair

*** Variables ***
${ENV}               stg
${BIZ}               ratan
${LANG}              1
${ROBOTDEBUG}        ${True}   
${BROWSER}           chrome
${STORAGE}           ${True}
# ${REALENABLE}        ${True}
# ${HEADLESSENABLE}    ${True}
# ${PROXYENABLE}       ${True}
${RECORDENABLE}      ${False}
# ${MWEBENABLE}        ${True}
# ${TIMEZONE}          Asia/Shanghai
${TIMEOUT}           30
${AutoClosingLevel}    SUITE