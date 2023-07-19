#!/bin/bash
THISPYTHON='python3'
testNumber=016
echo "Testing $0..."

PDB_tests_dir="${GEMSHOME}/gemsModules/structurefile/PDBFile/tests_in"
test_request="${PDB_tests_dir}/explicit_test.json" 
out_file="${GEMSHOME}/tests/016.AmberMDPrep.4mbzEdit.pdb" # Base path needs to match the json outputDirPath
test_output=test${testNumber}_output


# clean up from previous runs
if [ -f $out_file ]; then
    rm "${out_file}"
fi
if [ -f $test_output ]; then
    rm $test_output
fi

# sanity check due to bs bug
# echo "ENV CHECK:"
# echo "$GEMSHOME"
# echo "$(which ${THISPYTHON})"
# pwd 


if ! [ -f $test_request ]; then
    printf "Test FAILED! File %s does not exist \n" $test_request
    return 1
fi

# jq would be more convenient but it's not installed in the GRPC container.
# Because some directories change on every run, we strip just the output we want to test for now.
cat $test_request | ${GEMSHOME}/bin/delegate |\
    $GEMSHOME/tests/utilities/json_ripper.py entity.responses.any_amber_prep.outputs.ppinfo > test${testNumber}_output

echo "Sleeping for 1 second to allow for file creation..."
sleep 1

# echo -e "\nRipped Output Message Bytes: $(wc -c < test${testNumber}_output) (Expected $(wc -c < correct_outputs/test${testNumber}_output))"
if ! cmp ${test_output} correct_outputs/${test_output} > /dev/null 2>&1; then
    printf "Test FAILED! Output file %s different from %s \n" outputs/${test_output} correct_outputs/${test_output}
    return 1
fi
rm $test_output

if ! [ -f $out_file ]; then
    echo "Test partially FAILED! Did not create '${out_file}'!"
    return 1
fi

echo "Test passed."
rm $out_file
return 0