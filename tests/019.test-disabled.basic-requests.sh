#!/bin/bash
THISPYTHON='python3'
testNumber=016
echo "Testing $0..."


### MARCO ###
response=$(cat "${GEMSHOME}/gemsModules/delegator/tests/inputs/marco_explicit.json" | $GEMSHOME/bin/delegate)

# Polo should be somewhere in the response json, just grep it
if ! echo $response | grep -q "Polo"; then
    echo "1 Test FAILED! Did not find 'Polo' in response."
    return 1
fi

# lets test implicit too
response=$(cat "${GEMSHOME}/gemsModules/delegator/tests/inputs/default.json" | $GEMSHOME/bin/delegate)

if ! echo $response | grep -q "Polo"; then
    echo "2 Test FAILED! Did not find 'Polo' in response."
    return 1
fi

### ##### ###

echo "Test passed."
return 0