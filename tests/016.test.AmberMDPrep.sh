#!/bin/sh
THISPYTHON='python3'
testNumber=016
echo "Testing $0..."
preprocess_file="/programs/gems/tests/outputs/016.AmberMDPrep.4mbzEdit.pdb"
PDB_tests_dir="${GEMSHOME}/gemsModules/structurefile/PDBFile/tests_in"

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


if ! [ -f "${PDB_tests_dir}/explicit.json" ]; then
    printf "Test FAILED! File %s does not exist \n" ${PDB_tests_dir}/explicit.json
    return 1
fi

# jq would be more convenient but it's not installed in the GRPC container.
# Because some directories change on every run, we strip just the output we want to test for now.
cat ${PDB_tests_dir}/explicit.json | ${GEMSHOME}/bin/delegate |\
    $GEMSHOME/tests/utilities/json_ripper.py entity.responses.any_amber_prep.outputs.ppinfo > test${testNumber}_output

# echo -e "\nRipped Output Message Bytes: $(wc -c < test${testNumber}_output) (Expected $(wc -c < correct_outputs/test${testNumber}_output))"
if ! cmp test${testNumber}_output correct_outputs/test${testNumber}_output > /dev/null 2>&1; then
    printf "Test FAILED! Output file %s different from %s \n" outputs/test${testNumber}_output correct_outputs/test${testNumber}_output
    return 1
fi
if ! [ -f $preprocess_file ]; then
    echo "Test FAILED! Did not create $preprocess_file"
    return 1
fi

echo "Test passed."
rm test${testNumber}_output $preprocess_file
return 0