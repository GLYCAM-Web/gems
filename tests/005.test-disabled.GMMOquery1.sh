#!/bin/bash
THISPYTHON='python3'
##################### Test 5 ########################
echo "Testing GMMO query 1..."
##Tests one of the commands that this script has
python3 ../testbin/query1_ExtractOntologyInfoByNameOfGlycan.py > test5_output
DIFF=$(diff test5_output correct_outputs/test5_output)
if [ "$DIFF" != "" ]; then
    echo "Test FAILED!"
    return 1;
else
    echo "Test passed."
    rm test5_output
    return 0;
fi
