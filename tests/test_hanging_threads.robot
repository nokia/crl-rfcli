# Copyright (C) 2019, Nokia

*** Settings ***

Library  ThreadHanger.py

*** Test Case ***

Hang Threads
   ThreadHanger.Start

Dummy
   Log To Console    Dummy
