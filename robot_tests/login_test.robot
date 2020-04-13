*** settings ***
Resource          resource.robot

*** Test Cases ***
Valid Login
    Open Browser To Login Page
    Input Username    admin 
    Input Password    admin 
    Submit Credentials
    Welcome Page Should Be Open
    [Teardown]    Close Browser
