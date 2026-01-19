#!/bin/bash
THISPYTHON='python3'
testNumber=017
echo "Testing $0..."

ACTUAL_CONFIG="$GEMSHOME/instance_config.json"
EXAMPLE_CONFIG="$ACTUAL_CONFIG.example"

TEST_INPUTS=(
    "$GEMSHOME/gemsModules/mmservice/mdaas/tests/inputs/017.test.with-all-resources-list.json"
    "$GEMSHOME/gemsModules/mmservice/mdaas/tests/inputs/017.test.json" 
    "$GEMSHOME/gemsModules/mmservice/mdaas/tests/inputs/017.test.with-unmin-gas-and-options.json"
)

# with args now
function test_runmd() {
    DELEGATE_TEST_INPUT=$1
    echo "Running test with input: $DELEGATE_TEST_INPUT"

    response="$(cat $DELEGATE_TEST_INPUT | $GEMSHOME/bin/delegate)"
    notices="$(echo $response | $GEMSHOME/tests/utilities/json_ripper.py notices)"
    
    if [ "$notices" != "{}" ]; then
        # TODO/N.B: This will not be a reliable test for much longer.
        printf "Failure: Notices are not empty.\n$notices\n\n"
        return 1
    fi

    project_dir="$(echo $response | grep -Po '"project_dir"\s*:\s*"\K[^"]*')"
    if [ -z "$project_dir" ]; then
        printf "Failure: project_dir is empty.\n\n"
        printf "The Response:\n$response\n\n"
        return 1
    fi

    retries=20
    sleeptime=3
    sleepsofar=0
    echo "waiting a maximum of $((sleeptime*retries)) seconds for the project to finish."
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
                sleep $sleeptime
		        sleepsofar="$((sleepsofar+sleeptime))"
                if [ $((retries % 3)) -eq 0 ]; then
                    echo "waiting up to $((sleeptime*retries)) more seconds for the project to finish."
                fi
            fi
        fi
    done

    return 1
}

# if ACTUAL_CONFIG doesn't exist, warn and fail
if ! [ -f $ACTUAL_CONFIG ]; then
    printf "\n\nThe instance configuration test requires a configuration to be placed in your \$GEMSHOME!\n'$ACTUAL_CONFIG' does not exist!\n\n" 
    printf "\tThe easiest way to get a configuration is restart the DevEnv, possibly setting GEMS_FORCE_INSTANCE_RECONFIGURATION=True.\n\n"
    # printf "\tIf you are in a DevEnv, you can use the example configuration:\n\t  \`cp $EXAMPLE_CONFIG $ACTUAL_CONFIG\`\n\n" 
    # return 1
fi

FAILED=false
for TEST_INPUT in "${TEST_INPUTS[@]}"; do
    test_runmd $TEST_INPUT
    FAILURE=$?
    if [ $FAILURE -ne 0 ]; then
        printf "MDaaS tests failed with input: $TEST_INPUT\n"
        FAILED=true
    fi
done

if [ $FAILED = true ]; then
    printf "One or more MDaaS tests failed.\n"
    return 1
fi