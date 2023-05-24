#!/bin/bash

# Tests should be about passing invalid inputs to the delegator

# JSON INPUTS
invalid_Json=$GEMSHOME/gemsModules/deprecated/delegator/test_in/sequence/invalid_json.json

# invoke delegator script with an invalid json object string
# response should be a valid json object with an error message
run_Invalid_Json_Input_Response_Test()
{
	# pipe .json to the delegator script
	# pipe reponse from delegator to grep
	# grep for "brief" : "NotAJSONObject"
	# grep is returning a count (-c flag)
	if [ $(cat $invalid_Json | $GEMSHOME/bin/delegate | grep -c '"brief" : "NotAJSONObject"') != '0' ] ; then
		return 1
	fi
	return 0
}

if run_Invalid_Json_Input_Response_Test; then
	echo "009a -- grep did not find: brief : NotAJSONObject in response"
	echo "009a -- exiting"
	return 1
else
	echo "009a -- passed"
fi

echo "All subtests of 009.test passed"
return 0
