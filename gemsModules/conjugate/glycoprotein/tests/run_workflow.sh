#!/bin/bash

set -euo pipefail
bash $GEMSHOME/logs/clearLogs.sh

# 1. Evaluate request
EVALUATE_REQUEST="/programs/gems/gemsModules/conjugate/glycoprotein/tests/inputs/explicit_evaluate.json"
# EVALUATE_REQUEST="/programs/gems/gemsModules/conjugate/glycoprotein/tests/inputs/explicit_evaluate_rcsb.json"

# 2. Build Request 
BUILD_REQUEST="/programs/gems/gemsModules/conjugate/glycoprotein/tests/inputs/explicit_build_parameterized.json"
STATUS_REQUEST="/programs/gems/gemsModules/conjugate/glycoprotein/tests/inputs/explicit_status_parameterized.json"
# Really, glycan mappings should be produced from Eval request and some sequences


echo "We are using these requests:"
echo "EVALUATE: $EVALUATE_REQUEST"
echo "BUILD: $BUILD_REQUEST"

EVALUATE_RESPONSE=$($GEMSHOME/bin/delegate $EVALUATE_REQUEST)
echo "EVALUATE_RESPONSE:"
echo "$EVALUATE_RESPONSE"

# since BUILD_REQUEST is paramed, replace <pUUID> with the actual value from EVALUATE_RESPONSE by getting basename of the project_dir field without using jq.
PUUID=$(basename $(echo $EVALUATE_RESPONSE | grep -o '"project_dir": *"[^"]*' | cut -d'"' -f4))
BUILD_REQUEST_JSON=$(cat $BUILD_REQUEST | sed "s/<pUUID>/$PUUID/")
STATUS_REQUEST_JSON=$(cat $STATUS_REQUEST | sed "s/<pUUID>/$PUUID/")
echo "BUILD_REQUEST_JSON:" 
echo "$BUILD_REQUEST_JSON"

BUILD_RESPONSE=$(echo $BUILD_REQUEST_JSON | $GEMSHOME/bin/delegate)
echo "BUILD_RESPONSE:"
echo "$BUILD_RESPONSE"

# Find "Success" and echo the line if it exists by using json.tool to format the JSON response
if echo "$BUILD_RESPONSE" | python3 -m json.tool | grep "execution started"; then
    echo "Build was started."
    echo "STATUS_REQUEST_JSON: $STATUS_REQUEST_JSON"
    while true; do
        sleep 3
        STATUS_RESPONSE=$(echo $STATUS_REQUEST_JSON | $GEMSHOME/bin/delegate)
        echo
        
        if echo "$STATUS_RESPONSE" | python3 -m json.tool | grep "All complete"; then
            echo "Build completed successfully."
            break
        elif echo "$STATUS_RESPONSE" | python3 -m json.tool | grep "with errors"; then
            echo "Build failed. Check the logs for more details."
            exit 1
        else
            #clear
            #echo "$STATUS_RESPONSE" | show-sub-dict
            # only show sub dictionary that matches {"explicit_Status":.*}
            echo "$STATUS_RESPONSE" | python3 -m json.tool | grep -e '"explicit_Status":' -A 10 -B 10
            echo "Waiting for build to complete..."
        fi
    done
else
    echo "Build failed. Response:"
    echo "$BUILD_RESPONSE" | python3 -m json.tool
    exit 1
fi
