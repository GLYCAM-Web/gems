#!/bin/bash


#Manually change this number as you add tests:
number_of_tests=1
tests_passed=0

##################### Test 1 ########################
echo "Testing Glycoprotein Builder..."
./bin/gp_builder tests/simple > test1_output
cd - >> /dev/null 2>&1 #return now to reduce chance of forgetting later
DIFF=$(diff test1_output tests/simple/output.txt)
if [ "$DIFF" != "" ]; then
    echo "Test FAILED!"
else
    echo "Test passed."
    ((tests_passed++))
    rm test1_output
fi

############# Allow git Pushes ###################
if [[ $tests_passed == $number_of_tests ]]; then
    exit 0
    echo "All tests passed"
else
    exit 1
fi
