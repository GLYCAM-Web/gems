#!/bin/bash
THISPYTHON='python3'
##################### Test 3 ########################
echo "Testing test_installation.bash..."
cd $GEMSHOME
./test_installation.bash > $GEMSHOME/tests/test3_output
cd - >> /dev/null 2>&1
DIFF=$(diff test3_output correct_outputs/test3_output 2>&1)
if [ "$DIFF" != "" ]; then
    echo "Test FAILED!"
    return 1;
else
    echo "Test passed."
    rm test3_output
    return 0;
fi
