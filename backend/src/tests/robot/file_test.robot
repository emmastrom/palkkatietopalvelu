*** Settings ***
Resource  resource.robot
Suite Setup  Setup With Existing User And Client
Suite Teardown  Close Browser

*** Test Cases ***
Adding File Succeeds
    Log Out
    Login As New Client
    Choose File  id=file-upload  ${CURDIR}/files_for_robot_tests/test.pdf
    Page Should Contain  Tiedosto lisätty onnistuneesti

Deleting File Succeeds
    Click Button  1              
    Alert Should Be Present
    Page Should Contain  Tiedosto poistettu onnistuneesti

Adding Wrong Filetype Fails
    Choose File  id=file-upload  ${CURDIR}/files_for_robot_tests/not_a_pdf.txt
    Alert Should Be Present  Lataathan vain PDF, Word, Excel, tai CSV tiedostoja.

*** Keywords ***
Set Confirm Password
    [Arguments]  ${confirmPassword}
    Input Password  confirmPassword  ${confirmPassword}

