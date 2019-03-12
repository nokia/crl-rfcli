# Copyright (C) 2019, Nokia

*** Settings ***
Resource          test_common.robot
Library           TestPythonpath


*** Test Cases ***
Keyword from library in 'testcases\...' folder should work
    [Tags]    test-pythonpath
    ${name}=    TestPythonpath.Get Name

Keyword from resource in 'resources\...' folder should work
    [Tags]    test-pythonpath
    Resource keyword 1

