#!/bin/bash

# 1. Evaluate request
EVALUATE_REQUEST="/programs/gems/gemsModules/complex/GpBuilder/tests/inputs/explicit_evaluate.json"

# 2. Build Request 
BUILD_REQUEST="/programs/gems/gemsModules/complex/GpBuilder/tests/inputs/explicit_build_paramaterized.json"

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