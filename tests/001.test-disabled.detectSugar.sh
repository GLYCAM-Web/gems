#!/bin/bash

THISPYTHON='python3'
##################### Test 1 ########################
echo "Testing detect_sugar..."
#Runs the script that is being tested
cd $GEMSHOME #detect sugars has hardcoded path to apps/BFMP/detect_shape in GMML::Assembly.ExtractSugars.
if [ -f gmmo.ttl ]; then
   mv gmmo.ttl gmmoBeforeTests.ttl > /dev/null 2>&1
fi
${THISPYTHON} ./bin/detect_sugars $GEMSHOME/tests/inputs/1NXC.pdb > /dev/null 2>&1
cd - >> /dev/null 2>&1 #return now to reduce chance of forgetting later
DIFF=$(diff ../gmmo.ttl correct_outputs/test1_output 2>&1)
echo "DIFF:  >>>$DIFF<<<"
if [ "$DIFF" != "" ]; then
    echo "Test FAILED!  Please see test1gmmo.ttl in the tests directory to see what went wrong."
    mv ../gmmo.ttl test1gmmo.ttl > /dev/null 2>&1
    return 1;
else
    echo "Test passed."
    rm ../ring_conformations.txt ../gmmo.ttl
    return 0;
fi
