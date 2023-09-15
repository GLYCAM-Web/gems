#!/bin/bash
THISPYTHON='python3'
testNumber=017
echo "Testing $0..."

ACT_CFG="$GEMSHOME/instance_config.json"
EX_CFG="$ACT_CFG.example"

DELEGATE_TEST_INPUT="$GEMSHOME/gemsModules/mmservice/mdaas/tests/inputs/run_md.json"

function test() {
    response="$(cat $DELEGATE_TEST_INPUT | $GEMSHOME/bin/delegate)"
    notices="$(echo $response | $GEMSHOME/tests/utilities/json_ripper.py notices)"
    echo $notices
    # notices should equal "{}" if there is no error, lets return 0 then
    if [ "$notices" == "{}" ]; then
        return 0
    else
        return 1
    fi
}

# if ACT_CFG doesn't exist, warn and fail
if ! [ -f $ACT_CFG ]; then
    printf "Test FAILED! No instance_json to use!\n%s does not exist\n\tPlease copy %s there." $ACT_CFG $EX_CFG
    return 1
fi


# test with the config that exists.
SUCCESS=test 
if ! diff $ACT_CFG $EX_CFG > /dev/null 2>&1; then
    # If they're different, we need to swap them and test the default config.
    mv $ACT_CFG $ACT_CFG.bak
    cp $EX_CFG $ACT_CFG

    SUCCESS=$SUCCESS && test

    # Swap them back
    rm $ACT_CFG
    mv $ACT_CFG.bak $ACT_CFG
fi

if ! $SUCCESS; then
    printf "Test FAILED! \n"
    return 1
fi
