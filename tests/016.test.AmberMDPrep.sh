#!/bin/sh
THISPYTHON='python3'
testNumber=016
echo "Testing $0..."

preprocess_file="/programs/gems/tests/outputs/016.AmberMDPrep.4mbzEdit-git-ignore-me.prepared.pdb"

if [ -f $preprocess_file ]; then
    rm "${preprocess_file}"
fi
if [ -f test${testNumber}_output ]; then
    rm test${testNumber}_output
fi

# Note, json_ripper will throw up if you don't give it a valid JSON object, 
# so the test will fail in that case too. jq would be more convenient...
cat $GEMSHOME/gemsModules/ambermdprep/tests_in/explicit.json | $GEMSHOME/bin/delegate |\
    $GEMSHOME/tests/utilities/json_ripper.py entity.responses.any_amber_prep.outputs.message > test${testNumber}_output

if ! cmp test${testNumber}_output correct_outputs/test${testNumber}_output > /dev/null 2>&1; then
    printf "Test FAILED! Output file %s different from %s \n" test${testNumber}_output correct_outputs/test${testNumber}_output
    return 1
fi
if ! [ -f $preprocess_file ]; then
    echo "Test FAILED! Did not create preprocessed.pdb"
    return 1
fi
echo "Test passed."
rm test${testNumber}_output $preprocess_file
return 0