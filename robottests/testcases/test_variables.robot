# Copyright (C) 2019, Nokia

*** Test Cases ***

Variables from target_file.ini should be exposed to Robot Framework
    [Tags]  requires-ini-target
    Should Be Equal As Strings  ${RFCLI_TARGET_1}                       target_file
    Should Be Equal As Strings  ${RFCLI_TARGET_1.IP}                    1.2.3.4
    Should Be Equal As Strings  ${RFCLI_TARGET_1.USER}                  user4
    Should Be Equal As Strings  ${RFCLI_TARGET_1.PASS}                  pass4
    Should Be Equal As Strings  ${RFCLI_TARGET_1.HOST_USERNAME}         user4
    Should Be Equal As Strings  ${RFCLI_TARGET_1.HOST_PASSWORD}         pass4
    Should Be Equal As Strings  ${RFCLI_TARGET_1.NTP_SERVERS}           1.9.5.3
    Should Be Equal As Strings  ${RFCLI_TARGET_1.DNS_FORWARDERS}        1.9.2.52
    Should Be Equal As Strings  ${RFCLI_TARGET_1.TZREGION}              Europe/Helsinki
    Should Be Equal As Strings  ${RFCLI_TARGET_1.EXT0_NET_ID}           vlan-2
    Should Be Equal As Strings  ${RFCLI_TARGET_1.EXT0_NET_IP_AND_MASK}  11.9.5.3


Variables from target_file.yaml should be exposed to Robot Framework
    [Tags]  requires-yaml-target
    Should Be Equal As Strings  ${RFCLI_TARGET_1}                                           target_file
    Should Be Equal As Strings  ${RFCLI_TARGET_1.PROTOCOL}                                  https
    Should Be Equal As Strings  ${RFCLI_TARGET_1.IP}                                        1.2.3.4
    Should Be Equal As Strings  ${RFCLI_TARGET_1.USER}                                      hranuser11
    Should Be Equal As Strings  ${RFCLI_TARGET_1.PASS}                                      system123
    Should Be Equal As Strings  ${RFCLI_TARGET_1.HOST_USERNAME}                             hranuser11
    Should Be Equal As Strings  ${RFCLI_TARGET_1.HOST_PASSWORD}                             system123
    Should Be Equal As Strings  ${RFCLI_TARGET_1.ENV.PARAMETERS.EXTERNAL_NETWORKS.EXT0}     cae23478-8bc7-48ee-946f-cd86ebb799f1
    Should Be Equal As Strings  ${RFCLI_TARGET_1.ENV.PARAMETERS.NTP_SERVERS}                10.20.110.16,10.20.110.17,10.171.8.4
    Should Be Equal As Strings  ${RFCLI_TARGET_1.ENV.PARAMETERS.NUMBER_OF_IPS.EXT0_IPS}     2

Variables given on CLI should be exposed to Robot Framework
    [Tags]  requires-var-from-cli
    Should Be Equal As Integers    ${VAR_FROM_CLI}    3

Variables specified via variable file should be exposed to Robot Framework
    [Tags]  requires-variable-file
    Should Be Equal As Strings    ${VAR_FROM_VARIABLE_FILE}    TEST
