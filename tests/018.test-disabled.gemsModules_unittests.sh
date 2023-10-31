#!/bin/bash
THISPYTHON='python3'
testNumber=018
echo "Testing $0..."

# This test aggregates specific python unittests from the gemsModules package into a pre-push test.

tests=(
    $GEMSHOME/gemsModules/systemoperations/instance_config/tests/test_instance_ops.py
)

for test in ${tests[@]}; do
    $THISPYTHON $test
    if [ $? -ne 0 ]; then
        printf "%s FAILED! \n" $test
        return 1
    fi
done