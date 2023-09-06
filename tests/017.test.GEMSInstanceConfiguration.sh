#!/bin/bash
THISPYTHON='python3'
testNumber=017
echo "Testing $0..."

ACT_CFG="$GEMSHOME/instance_config.json"
EX_CFG="$ACT_CFG.example"

DELEGATE_TEST_INPUT="$GEMSHOME/gemsModules/mmservice/mdaas/tests/inputs/run_md.json"

function test() {
    response="$(cat $DELEGATE_TEST_INPUT | $GEMSHOME/bin/delegate)"
    echo $response | $GEMSHOME/tests/utilities/json_ripper.py notices
    echo 
}


# test with the config we have
test 

if ! diff $ACT_CFG $EX_CFG > /dev/null 2>&1; then
    # If they're different, we need to swap them and test the default config.
    mv $ACT_CFG $ACT_CFG.bak
    cp $EX_CFG $ACT_CFG

    # test with the default config
    test

    # Swap them back
    rm $ACT_CFG
    mv $ACT_CFG.bak $ACT_CFG
fi