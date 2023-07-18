#!/bin/sh
THISPYTHON='python3'
testNumber=016
echo "Testing $0..."

preprocess_file="${GEMSHOME}/tests/016.AmberMDPrep.4mbzEdit.pdb"
PDB_tests_dir="${GEMSHOME}/gemsModules/structurefile/PDBFile/tests_in"
test_request="${PDB_tests_dir}/explicit_test.json" 
test_output=test${testNumber}_output


# clean up from previous runs
if [ -f $preprocess_file ]; then
    rm "${preprocess_file}"
fi
if [ -f test${testNumber}_output ]; then
    rm test${testNumber}_output
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

echo "Sleeping for 3 seconds to allow for file creation..."
sleep 3

# echo -e "\nRipped Output Message Bytes: $(wc -c < test${testNumber}_output) (Expected $(wc -c < correct_outputs/test${testNumber}_output))"
if ! cmp ${test_output} correct_outputs/${test_output} > /dev/null 2>&1; then
    printf "Test FAILED! Output file %s different from %s \n" outputs/${test_output} correct_outputs/${test_output}
    return 1
fi
rm $test_output

if ! [ -f $preprocess_file ]; then
    echo "Test partially FAILED! Did not create '${preprocess_file}'! Is gmml.cds_PdbFile.Write working?"
    return 0
fi

echo "Test passed."
rm $preprocess_file
return 0