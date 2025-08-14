#!/bin/bash

set -euo pipefail


# 1. Evaluate request
EVALUATE_REQUEST="/programs/gems/gemsModules/complex/GpBuilder/tests/inputs/explicit_evaluate.json"
# EVALUATE_REQUEST="/programs/gems/gemsModules/complex/GpBuilder/tests/inputs/explicit_evaluate_rcsb.json"

# 2. Build Request 
BUILD_REQUEST="/programs/gems/gemsModules/complex/GpBuilder/tests/inputs/explicit_build_parameterized.json"
# Really, glycan mappings should be produced from Eval request and some sequences


echo "We are using these requests:"
echo "EVALUATE: $EVALUATE_REQUEST"
echo "BUILD: $BUILD_REQUEST"

EVALUATE_RESPONSE=$($GEMSHOME/bin/delegate $EVALUATE_REQUEST)
echo "EVALUATE_RESPONSE:"
echo "$EVALUATE_RESPONSE"

# since BUILD_REQUEST is paramed, replace <pUUID> with the actual value from EVALUATE_RESPONSE by getting basename of the project_dir field without using jq.
BUILD_REQUEST_JSON=$(cat $BUILD_REQUEST | sed "s/<pUUID>/$(basename $(echo $EVALUATE_RESPONSE | grep -o '"project_dir": *"[^"]*' | cut -d'"' -f4))/")
echo "BUILD_REQUEST_JSON:" 
echo "$BUILD_REQUEST_JSON"

BUILD_RESPONSE=$(echo $BUILD_REQUEST_JSON | $GEMSHOME/bin/delegate)
echo "BUILD_RESPONSE:"
echo "$BUILD_RESPONSE"

# Find "Success" and echo the line if it exists by using json.tool to format the JSON response
if echo "$BUILD_RESPONSE" | python3 -m json.tool | grep success; then
    echo "Build was successful."
else
    echo "Build failed. Response:"
    echo "$BUILD_RESPONSE" | python3 -m json.tool
    exit 1
fi