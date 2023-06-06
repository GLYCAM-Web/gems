#!/bin/bash

# Tests the ability to preprocess 1BUY 
# Compare the preprocessing output to known valid output.

echo "013: Testing pdb preprocessor output."

runTest()
{
	# JSON INPUTS
    jsonInputFile=$GEMSHOME/gemsModules/deprecated/delegator/test_in/pdb/preprocessPdbForAmber_file.json
    if [ ! -f "$jsonInputFile" ]; then 
        echo "Test 013 failed: Failed to find request input: $jsonInputFile"
        return 1
    fi
    echo "Found test input: $jsonInputFile"
    ## Correct outputs ref
    outputRefFile=${GEMSHOME}/tests/correct_outputs/test013_output.pdb
    if [ ! -f "$outputRefFile" ]; then 
        echo "Test 013 failed: Failed to find the correct_outputs reference: $outputRefFile"
        return 1
    fi
    testResponse="${GEMSHOME}/tests/bad_outputs/${now}_git-ignore-me_test_response_013.json"
    echo "testResponse filename will be: $testResponse"
    cat $jsonInputFile | python $GEMSHOME/bin/delegate > $testResponse
    line=$( cat $testResponse| grep "project_dir" )
    #echo "line: $line"
    preface=$( echo $line | sed -n -e 's/^.*project_dir\": \"//p' )
    projectDir=$( echo $preface | sed -n -e 's/\",.*//p' )
    outputFile="${projectDir}/updated_pdb.pdb"
    # Updated pdb
    if [ ! -f "$outputFile" ]; then 
        echo "Test 013 failed: Failed to find the outputFile:"
        echo "$outputFile"
        return 1
    fi
    echo "Comparing $outputFile $outputRefFile"
    if ! cmp -s $outputFile $outputRefFile; then
        now=$(date "+%Y-%m-%d-%H-%M-%S")
        errorFile="${GEMSHOME}/tests/bad_outputs/${now}_git-ignore-me_test_error_013.txt"
        echo "Test failed: unexpected response. Look for details in $errorFile"
        echo "Test failed, these files are different: $outputFile $outputRefFile"
        echo $( diff $outputFile $outputRefFile ) > $errorFile
        return 1
    fi
    echo "Test passed."
    rm $outputFile
    rm $testResponse
    return 0
}

if ! runTest; then
	return 1
fi
echo "013 -- passed"
return 0
