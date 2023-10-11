#!/bin/bash
THISPYTHON='python3'
testNumber=017
echo "Testing $0..."

ACTUAL_CONFIG="$GEMSHOME/instance_config.json"
EXAMPLE_CONFIG="$ACTUAL_CONFIG.example"

DELEGATE_TEST_INPUT="$GEMSHOME/gemsModules/mmservice/mdaas/tests/inputs/run_md.json"

function test_runmd() {    
    response="$(cat $DELEGATE_TEST_INPUT | $GEMSHOME/bin/delegate)"
    notices="$(echo $response | $GEMSHOME/tests/utilities/json_ripper.py notices)"
    
    if [ "$notices" != "{}" ]; then
        echo "Failure: Notices are not empty."
        return 1
    fi

    project_dir="$(echo $response | grep -Po '"projectDir"\s*:\s*"\K[^"]*')"
    echo $project_dir

    retries=5
    while [ $retries -gt 0 ]; do
        # Check for the existence of 10.produ.o and status.log
        if [ -f "${project_dir}/10.produ.o" ] && [ -f "${project_dir}/status.log" ]; then
            echo "FOUND 10.produ.o and status.log"
            return 0
        else
            retries=$(($retries - 1))
            if [ $retries -eq 0 ]; then
                echo "DID NOT FIND ${project_dir}/10.produ.o and ${project_dir}/status.log after multiple checks"
                break
            else
                sleep 3
            fi
        fi
    done


    return 1
}


# if ACTUAL_CONFIG doesn't exist, warn and fail
if ! [ -f $ACTUAL_CONFIG ]; then
    printf "\nThe instance configuration test requires a configuration to be placed in your \$GEMSHOME!\n'$ACTUAL_CONFIG' does not exist!\n\n" 
    printf "\tThe easiest way to get a configuration is restart the DevEnv, possibly setting GEMS_FORCE_INSTANCE_RECONFIGURATION=True.\n\n"
    # printf "\tIf you are in a DevEnv, you can use the example configuration:\n\t  \`cp $EXAMPLE_CONFIG $ACTUAL_CONFIG\`\n\n" 
    # return 1
fi

# Using RunMD will generate a default configuration if one does not exist.
test_runmd
FAILURE=$?

# # This no longer works because the example config isn't configured by default. Instead,
# # The DevEnv calls $GEMSHOME/bin/setup-instance.py to generate a working config. Because this
# # GEMS test cannot possibly know about the DevEnv, it cannot necessarily set up the example
# # config any better.
# # In fact, generating an instance_config.json outside of the DevEnv will likely cause problems
# # for anything depending on it. TODO: Come up with a better default generation. Right now, best
# # we can do is delete and restart the dev env.
# if [ -f $ACTUAL_CONFIG ] && ! [ diff $ACTUAL_CONFIG $EXAMPLE_CONFIG > /dev/null 2>&1 ]; then
#     # If they're different, we need to swap them and test the default config.
#     mv $ACTUAL_CONFIG $ACTUAL_CONFIG.bak.test017
#     cp $EXAMPLE_CONFIG $ACTUAL_CONFIG

#     test_runmd
#     FAILURE=$(($FAILURE + $?))

#     # Swap them back
#     rm $ACTUAL_CONFIG
#     mv $ACTUAL_CONFIG.bak.test017 $ACTUAL_CONFIG
# fi

if [ $FAILURE -ne 0 ]; then
    printf "Instance configuration test failed, if you are in a development environment, please try deleting the instance config and restarting your DevEnv!\nIf you are running in production, please check your configuration!\n"
    return 1
fi
