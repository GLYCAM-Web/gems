#!/bin/sh

# Tests response to requests for evaluating a version of 1BUY that has been edited
# to give results for all tables used by the frontend. The valid response will represent
# error-level responses that are not themselves actually code-errors, but rather evaluation
# reports with an alert-level of error. 

echo "
012: Testing pdb evaluation response.
" 



runTest()
{
    # JSON INPUTS
    jsonInputFile=$GEMSHOME/gemsModules/deprecated/delegator/test_in/pdb/evaluateTestPdbFile.json
    if [ -f "$jsonInputFile" ]; then 
        echo "Found test input: $jsonInputFile"
    else
        echo "Test 012 failed: Failed to find request input: $jsonInputFile"
        return 1
    fi

    outputRefFile=$GEMSHOME/tests/correct_outputs/test012_output
    if [ -f "$outputRefFile" ]; then 
        echo "Found correct_outputs reference: $outputRefFile"
    else
        echo "Test 012 failed: Failed to find the correct_outputs reference: $outputRefFile"
        return 1
    fi

    ## Timestamps and projects will be different.
    correctOutput=$( sed '/project/q' $outputRefFile | grep -v "timestamp" )


    ## TODO: Move this output file to bad_outputs.
    cat $jsonInputFile | $GEMSHOME/bin/delegate > ${badOutDir}git-ignore-me_test_out_012
    response=$( sed '/project/q' ${badOutDir}git-ignore-me_test_out_012| grep -v "timestamp" )
    
    # response=$(cat $jsonInputFile | $GEMSHOME/bin/delegate | grep -v "timestamp" | grep -B "project")

    if [ "$response" = "$correctOutput" ]; then
        echo "Test passed."
        rm ${badOutDir}git-ignore-me_test_out_012
    else
        echo "
Test failed: unexpected response
correctOutput: 
$correctOutput
        
~~~~~~~~~~~~~~~
Failed to match 
~~~~~~~~~~~~~~~

response: 
$response
"
        echo "Test failed: unexpected response"
        return 1
    fi


    return 0
}

if runTest; then
    echo "012 -- passed"
    return 0
fi

