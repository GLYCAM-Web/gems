#!/bin/sh

# Tests the ability to preprocess 1BUY 
# Compare the preprocessing output to known valid output.

## TODO: think of more meaningful tests. 
##	1BUY is known to give quick results, but warning and error-level
##	options will not be tested. Also not tested here is
##	the ability to accept user-set options.

echo "
013: Testing pdb preprocessor output.
"

runTest()
{
	# JSON INPUTS
    jsonInputFile=$GEMSHOME/gemsModules/deprecated/delegator/test_in/pdb/preprocessPdbForAmber_file.json
    if [ -f "$jsonInputFile" ]; then 
        echo "Found test input: $jsonInputFile"
    else
        echo "Test 013 failed: Failed to find request input: $jsonInputFile"
        return 1
    fi


    ## Correct outputs ref
    outputRefFile=${GEMSHOME}/tests/correct_outputs/test013_output.pdb
    if [ -f "$outputRefFile" ]; then 
        echo "Found correct_outputs reference: $outputRefFile"
    else
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
 
    if [ -f "$outputFile" ]; then 
        echo "Found outputFile:"
        echo "$outputFile"
        echo "comparing to outputRefFile:"
        echo "$outputRefFile"
    else
        echo "Test 013 failed: Failed to find the outputFile:"
        echo "$outputFile"
        return 1
    fi


    if $( diff $outputFile  $outputRefFile ); then
        echo "Test passed."
        rm $outputFile
        rm $testResponse
    else
        now=$(date "+%Y-%m-%d-%H-%M-%S")
        errorFile="${GEMSHOME}/tests/bad_outputs/${now}_git-ignore-me_test_error_013.txt"
        echo "
Test failed: unexpected response
Look for details in $errorFile
"
        echo "Test failed: unexpected response"
        echo $( diff $outputFile  $outputRefFile ) > $errorFile
        return 1
    fi

    return 0



}

if runTest; then
	echo "013 -- passed"
	return 0
fi
