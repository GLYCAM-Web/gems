#!/bin/bash
# This test passes each of the invalid sequence input payloads in $GEMSHOME/tests/inputs/010.input.txt through the delegator.
# For the test to pass, each output must contain the appropriate error message.
runInvalidSequenceInputTest()
{
	invalidSequenceJson=$1
	expectedOutput="$2"
	cat $invalidSequenceJson | $GEMSHOME/bin/delegate > 010.output.json 
	noticeMessage=\"$(grep "noticeMessage" 010.output.json | cut -d \" -f4)\"
	if [ "$expectedOutput" = "$noticeMessage" ]; then
		rm 010.output.json
	    return 0
	else
		echo "noticeMessage is:$noticeMessage"
		echo "expectedOutput is:$expectedOutput"
		return 1
	fi
}

inputs=$GEMSHOME/tests/inputs/010.input.txt
# E.g. invalidSequence=gemsModules/deprecated/delegator/test_in/sequence/minimal_invalid_payload.json
#for input in `cat $inputs` 
while IFS= read -r line;
do
	invalidSequenceJson=$GEMSHOME/$(echo $line | cut -d , -f1)
	expectedOutput=$(echo $line | cut -d , -f2)
	# echo "invalidSequenceJson=$invalidSequenceJson"
	# echo "expectedOutput=$expectedOutput"
	if runInvalidSequenceInputTest $invalidSequenceJson "$expectedOutput"; then
		echo "Test passed with input: $invalidSequenceJson"
	else
		echo "Test failed with input: $invalidSequenceJson"
		exit 1
	fi
done < "$inputs"

echo "All Tests passed"
exit 0

