#!/bin/bash
THISPYTHON='python3'

##################### Test 2 ########################
echo "Testing PDBSugarID..."
##runs the script with a functional argument
cd $GEMSHOME
${THISPYTHON} ./bin/PDBSugarID $GEMSHOME/tests/inputs/1NXC.pdb $GEMSHOME/tests/test2_output
cd - >> /dev/null 2>&1
tail -n +18 test2_output > tmp2
DIFF=$(diff tmp2 correct_outputs/test2_output 2>&1)
echo "DIFF:  >>>$DIFF<<<"
if [ "$DIFF" != "" ]; then
    echo "Test FAILED!"
    return 1;
else
    echo "Test passed."
    rm test2output tmp2 ../ring_conformations.txt
    return 0;
fi

