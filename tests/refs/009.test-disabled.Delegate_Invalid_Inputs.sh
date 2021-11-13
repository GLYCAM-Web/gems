#!/bin/bash

# Tests should be about passing invalid inputs to the delegator

# python script that will determine is json is valid
is_Valid_JSON_py=$GEMSHOME/testbin/isvalidjson.py

# JSON INPUTS
invalid_Payload=$GEMSHOME/gemsModules/delegator/test_in/sequence/minimal_invalid_payload.json
invalid_Json=$GEMSHOME/gemsModules/delegator/test_in/sequence/invalid_json.json

# invoke delegator script with an invalid json object string
# response should be a valid json object with an error message
run_Invalid_Json_Input_Response_Test()
{
	# pipe .json to the delegator script
	# pipe reponse from delegator to grep
	# grep for "brief" : "NotAJSONObject"
	# grep is returning a count (-c flag)
	if [ $(cat $invalid_Json | $GEMSHOME/bin/delegate | grep -c '"brief" : NotAJSONObject') != '0' ] ; then
		return 1
	fi

	if [ $(cat $invalid_Json | $GEMSHOME/bin/delegate | grep -c '"brief" : "NotAJSONObject"') != '0' ] ; then
		return 1
	fi
	
	return 0
}

# invoke delegator script with a json string containing a known invalid payload
# gmml should detect the invalid payload and abort
# gems should return a valid json object with an error message
run_Invalid_Payload_Response_Test()
{
	# pipe .json to the delegator script, redirect to file f
	# invoke json validator script 
	cat $invalid_Payload | $GEMSHOME/bin/delegate > f
	$is_Valid_JSON_py f
	# exit code from is_Valid_JSON_py
	isValid=$?
	rm f

	if [ $isValid  != '0' ] ; then
		return 1
	fi
	
	## TODO: check for a specific error message
	## currently this test is a false positive
	return 0
}

# test to ensure that gmml doesn't attempt to build /w invalid payload
# issue is described in github ticket #41
# invoke delegator script with a .json containing a known bad payload
# gmml should detect the bad payload and 
# return a valid json response containing: "sequenceIsValid": "false"#  
run_Invalid_Payload_Test()
{
	# pipe .json to the delegator script
	# pipe reponse from delegator to grep
	# grep for sequenceIsValid : true
	# grep is returning a count (-c flag)
	if [ $(cat $invalid_Payload | $GEMSHOME/bin/delegate | grep -c '"sequenceIsValid": true') != '0' ] ; then
		#echo "009a -- sequenceIsValid is True with known bad payload"
		return 1
	fi

	if [ $(cat $invalid_Payload | $GEMSHOME/bin/delegate | grep -c '"sequenceIsValid": "true"') != '0' ] ; then
		#echo "009a -- sequenceIsValid is True with known bad payload"
		return 1
	fi
	
	return 0
}

# if ! run_Bad_Payload_Test; then
# 	echo "009a -- sequenceIsValid is True with known bad payload"
# 	echo "009a -- exiting"
# 	exit 1
# else
# 	echo "009a -- passed"
# fi

if ! run_Invalid_Payload_Response_Test; then
	echo "009b -- delegator returned an error as a non-valid json response"
	echo "009b -- exiting"
	exit 1
else 
	echo "009b -- passed"
fi

if run_Invalid_Json_Input_Response_Test; then
	echo "009c -- grep did not find: brief : NotAJSONObject in response"
	echo "009c -- exiting"
	exit 1
else
	echo "009c -- passed"
fi

echo "All 009 tests passed"
exit 0