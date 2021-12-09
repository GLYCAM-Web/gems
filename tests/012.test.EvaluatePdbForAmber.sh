#!/bin/bash

# Tests response to requests for evaluating a version of 1BUY that has been edited
# to give results for all tables used by the frontend. The valid response will represent
# error-level responses that are not themselves actually code-errors, but rather evaluation
# reports with an alert-level of error. 

echo "
Testing pdb evaluation response.
" 


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

    if [ $(cat $jsonFile | $GEMSHOME/bin/delegate | grep -c '/website/TESTS/pdb/test_in/1BUY_modified.pdb') = '0' ] ; then
        echo "Test 012 failed: Response failed to echo the expected PDB input file."
        exit 1
    fi

    if [ $(cat $jsonFile | $GEMSHOME/bin/delegate | grep -c 'unrecognizedAtoms') = '0' ] ; then
        echo "Test 012 failed: Response failed to list unrecognizedAtoms." 
        exit 1
    fi

    if [ $(cat $jsonFile | $GEMSHOME/bin/delegate | grep -c "unrecognizedMolecules") = '0' ] ; then
        echo "Test 012 failed: Response failed to list unrecognizedMolecules."
        exit 1
    fi

    if [ $(cat $jsonFile | $GEMSHOME/bin/delegate | grep -c 'missingResidues') = '0' ] ; then
        echo "Test 012 failed: Response failed to list missingResidues." 
        exit 1
    fi
    
    if [ $(cat $jsonFile | $GEMSHOME/bin/delegate | grep -c 'histidineProtonations') = '0' ] ; then
        echo "Test 012 failed: Response failed to list histidineProtonations." 
        exit 1
    fi

    if [ $(cat $jsonFile | $GEMSHOME/bin/delegate | grep -c 'disulfideBonds') = '0' ] ; then
        echo "Test 012 failed: Response failed to list disulfideBonds." 
        exit 1
    fi
    
    if [ $(cat $jsonFile | $GEMSHOME/bin/delegate | grep -c 'chainTerminations') = '0' ] ; then
        echo "Test 012 failed: Response failed to list chainTerminations." 
        exit 1
    fi

    if [ $(cat $jsonFile | $GEMSHOME/bin/delegate | grep -c 'replacedHydrogens') = '0' ] ; then
        echo "Test 012 failed: Response failed to list replacedHydrogens." 
        exit 1
    fi

    return 0
}

if runTest; then
    echo "012 -- passed"
    exit 0
fi

