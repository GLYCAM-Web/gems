#!/bin/sh
THISPYTHON='python3'
testNumber=016
echo "Testing $0..."
${THISPYTHON} ../bin/AmberMDPrep.py inputs/016.AmberMDPrep.4mbzEdit.pdb > test${testNumber}_output

if ! cmp test${testNumber}_output correct_outputs/test${testNumber}_output > /dev/null 2>&1; then
    printf "Test FAILED! Output file %s different from %s \n" test${testNumber}_output correct_outputs/test${testNumber}_output
    echo "Exit Code: 1"
    return 1
    exit 1
fi
if ! [ -f preprocessed.pdb ]; then
    echo "Test FAILED! Did not create preprocessed.pdb"
    echo "Exit Code: 1"
    return 1
    exit 1
fi
echo "Test passed."
rm test${testNumber}_output preprocessed.pdb
echo "Exit Code: 0"
return 0
exit 0