#!/bin/bash
THISPYTHON='python3'
testNumber=017
echo "Testing $0..."

ACTUAL_CONFIG="$GEMSHOME/instance_config.json"
EXAMPLE_CONFIG="$ACTUAL_CONFIG.example"

DELEGATE_TEST_INPUT="$GEMSHOME/gemsModules/mmservice/mdaas/tests/inputs/run_md.json"

function test() {
    response="$(cat $DELEGATE_TEST_INPUT | $GEMSHOME/bin/delegate)"
    notices="$(echo $response | $GEMSHOME/tests/utilities/json_ripper.py notices)"
    # notices should equal "{}" if there is no error, indicating we were able to destructure a valid response, and nothing unusual happened.
    if [ "$notices" == "{}" ]; then
        return 0
    else
        return 1
    fi
}

# if ACTUAL_CONFIG doesn't exist, warn and fail
if ! [ -f $ACTUAL_CONFIG ]; then
    printf "\nThe instance configuration test requires a configuration to be placed in your \$GEMSHOME!\n'$ACTUAL_CONFIG' does not exist!\n\n" 
    printf "\tThe impending test will automatically generate a default configuration for you.\n\n"
    # printf "\tIf you are in a DevEnv, you can use the example configuration:\n\t  \`cp $EXAMPLE_CONFIG $ACTUAL_CONFIG\`\n\n" 
    # return 1
fi

# Using RunMD will generate a default configuration if one does not exist.
SUCCESS=test 


if [ -f $ACTUAL_CONFIG ] && ! [ diff $ACTUAL_CONFIG $EXAMPLE_CONFIG > /dev/null 2>&1 ]; then
    # If they're different, we need to swap them and test the default config.
    mv $ACTUAL_CONFIG $ACTUAL_CONFIG.bak.test017
    cp $EXAMPLE_CONFIG $ACTUAL_CONFIG

    SUCCESS=$SUCCESS && test

    # Swap them back
    rm $ACTUAL_CONFIG
    mv $ACTUAL_CONFIG.bak.test017 $ACTUAL_CONFIG
fi

if ! $SUCCESS; then
    printf "Instance configuration test failed, if you are in a development environment, please try the example configuration!\nIf you are running in production, please check your configuration!\n"
    return 1
fi
