#!/bin/sh
THISPYTHON='python3'
##################### Test 6 ########################
echo "Testing GMMO query 2..."
##Tests one of the commands that this script has
python3 ../testbin/query3_ExtractOntologyInfoByPDBID.py > test6_output
DIFF=$(diff test6_output correct_outputs/test6_output)
if [ "$DIFF" != "" ]; then
    echo "Test FAILED!"
    return 1;
else
    echo "Test passed."
    rm test6_output
    return 0;
fi

