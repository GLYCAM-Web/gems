#!/bin/sh
##
##   To disable a test:
##
##        Change the filename so that it 
##        doesn't match the pattern *.test.*.sh
##
##   To run a single test (even a disabled one):
##
##        Use the filename for the test as a command-lin argument.
##        You can use this method to run disabled tests.
##
export badOutDir='bad_outputs'
START=$SECONDS
run_test() 
{
#    sh $1
    source $1
    return $?
}
if [ ! -d ${badOutDir} ] ; then
	mkdir -p ${badOutDir}
fi

##  If there is a command line argument, run that test
if [ "${1}zzz" != "zzz" ] ; then
	echo "Found this command-line argument : '${1}'"
	echo "Attempting to run that single test."
	echo ""
	if [ ! -f "${1}" ] ; then
		echo "The argument '${1}' is not a file.  Exiting."
		exit 1
	fi
	if run_test ${1} ; then 
		echo "The test passed."
    		echo "removing bad outputs directory"
    		rm -rf ${badOutDir}
    		exit 0
	else
    		echo "The test failed."
		echo "Check this directory for more information:"
		echo "        ${badOutDir}"
    		exit 1
	fi
fi

##
## If this is a regular testing session, do these things
##

required_passing_tests=$(/bin/ls -1 *.test.*.sh | wc -l)
echo """
Number of tests found: ${required_passing_tests}
Beginning testing.
"""
tests_attempted=0
tests_passed=0
for i in $(/bin/ls *.test.*.sh) ; do 
    printf "Using test file:  ${i} \n"
    tests_attempted=$((tests_attempted+1))
    if run_test ${i} ; then tests_passed=$((tests_passed+1)); fi
done

END=$SECONDS
TESTING_TIME=$((END - START))
MIN=$((TESTING_TIME/60%60))
SEC=$((TESTING_TIME%60))

echo """
$tests_attempted tests were attempted
$tests_passed tests passed 
$required_passing_tests were required"
echo "
Testing time: "$MIN:$SEC




if [ "$tests_passed" -ge "$required_passing_tests" ]; then 
    echo "The required number of tests passed"
    echo "removing bad outputs directory"
    rm -rf ${badOutDir}
    exit 0
else
    echo "Some required tests did not pass."
    exit 1
fi
