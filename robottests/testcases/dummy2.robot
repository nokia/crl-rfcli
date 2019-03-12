# Copyright (C) 2019, Nokia

*** Settings ***
Resource          resources/test_common.robot
Library           TestPythonpath2


*** Test Cases ***
Keyword from library in 'libraries\...' folder should work
    [Tags]    test-pythonpath
    ${nimi}=    TestPythonpath2.Get Name2

Keyword from resource in 'resources\...' folder should work
    [Tags]    test-pythonpath
    Resource keyword 2
