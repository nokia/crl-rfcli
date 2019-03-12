# Copyright (C) 2019, Nokia

*** Settings ***
Resource          test_common.robot
Library           TestPythonpath3


*** Test Cases ***
Keyword from library in 'testcases\...' folder following symlink should work
    [Tags]    test-pythonpath
    ${name}=    TestPythonpath3.Get Name3
