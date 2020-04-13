*** settings ***
Library           SeleniumLibrary

*** Variables ***
${SERVER}         localhost:8080
${BROWSER}        Chrome 
${DELAY}          0
${VALID USER}      admin
${VALID PASSWORD}  admin
${LOGIN URL}      http://${SERVER}/log
${WELCOME URL}    http://${SERVER}/
${ERROR URL}      http://${SERVER}/redirect

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be   Login

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Input Username
    [Arguments]    ${username}
    Input Text    username          ${username}

Input Password
    [Arguments]    ${password}
    Input Text    passwordinput          ${password}

Submit Credentials
    Click Button    login_button

Welcome Page Should Be Open
    Location Should Be    ${WELCOME URL}
    Title Should Be    Welcome
