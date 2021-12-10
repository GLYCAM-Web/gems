#!/bin/bash

# Tests response to requests for evaluating a version of 1BUY that has been edited
# to give results for all tables used by the frontend. The valid response will represent
# error-level responses that are not themselves actually code-errors, but rather evaluation
# reports with an alert-level of error. 

echo "
Testing pdb evaluation response.
" 
declare -a tableNames=( \
    "unrecognizedAtoms" \
    "unrecognizedMolecules" \
    "missingResidues" \
    "histidineProtonations" \
    "disulfideBonds" \
    "chainTerminations" \
    "replacedHydrogens")


runTest()
{
    # JSON INPUTS
    jsonFile=$GEMSHOME/gemsModules/delegator/test_in/pdb/evaluateTestPdbFile.json

    if [ -f "$jsonFile" ]; then 
        echo "Found test input: $jsonFile"
    else
        echo "Test 012 failed: Failed to find request input: $jsonFile"
        exit 1
    fi

    response=$(cat $jsonFile | $GEMSHOME/bin/delegate)
    echo "response: $response"

    if [ $( echo "$response" | grep -c "$GEMSHOME/tests/inputs/1BUY_modified.pdb" ) = '0' ] ; then
        echo "Test 012 failed: Response failed to echo the expected PDB input file."
        exit 1
    fi

    for table in $tableNames; do
        if [ $( echo "$response" | grep -c "$table" ) = '0' ]; then 
            echo "Test 012 failed: $table not found in response"
            exit 1
        fi
    done

    return 0
}

if runTest; then
    echo "012 -- passed"
    exit 0
fi

