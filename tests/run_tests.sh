#!/bin/bash

#Manually change this number as you add tests:
required_passing_tests=3
tests_passed=0

run_test() 
{
    sh $1
    return $?
}

# Comment out tests you don't want to run. Add additional tests at the bottom. 
# Change required_passing_tests to equal number of tests.

#if run_test 001.test.detectSugar.sh; then tests_passed=$(($tests_passed + 1)); fi
#if run_test 002.test.PDBSugarID.sh; then tests_passed=$(($tests_passed + 1)); fi
if run_test 003.test.InstallationBash.sh; then tests_passed=$(($tests_passed + 1)); fi
if run_test 004.test.InstallationPy.sh; then tests_passed=$(($tests_passed + 1)); fi
#if run_test 005.test.GMMOquery1.sh; then tests_passed=$(($tests_passed + 1)); fi
#if run_test 006.test.GMMOquery2.sh; then tests_passed=$(($tests_passed + 1)); fi
if run_test 007.test.DrawGlycan.sh; then tests_passed=$(($tests_passed + 1)); fi

echo "$tests_passed tests passed of $required_passing_tests"

if [[ "$tests_passed" -ge "$required_passing_tests" ]]; then
    exit 0
    echo "All tests passed"
else
    exit 1
fi
