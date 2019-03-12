# Copyright (C) 2019, Nokia

*** Variables ***
${LOG_TAG}         [Get Name]

*** Keywords ***
Log
    [Arguments]     ${msg}
    BuiltIn.Log     ${LOG_TAG} ${msg}     console=no

Resource keyword 1
    Log    Here we are...

Resource keyword 2
    Log    Again.
