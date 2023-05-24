#!/bin/sh
THISPYTHON='python3'
##################### Test 4 ########################
echo "Testing test_installation.py..."
#Tests one of the commands that this script has
${THISPYTHON} ../test_installation.py "--help" > test4_output
DIFF=$(diff test4_output correct_outputs/test4_output 2>&1)
if [ "$DIFF" != "" ]; then
    echo "Test FAILED!"
    return 1;
else
    echo "Test passed."
    rm test4_output
    return 0;
fi

