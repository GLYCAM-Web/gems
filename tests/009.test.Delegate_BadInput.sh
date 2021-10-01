#!/bin/bash

# comment this code

# python script that will determine is json is valid
is_Valid_JSON_py=$GEMSHOME/testbin/isvalidjson.py
bad_Payload=$GEMSHOME/gemsModules/delegator/test_in/sequence/minimal_bad_payload.json
bad_Payload_Response=""



# invoke delegator script with a .json containing a known bad payload
# gmml should detect the bad payload and return a valid json object 
# with an error message
run_Valid_Json_Response_Test()
{
	# pipe .json to the delegator script, redirect to file f
	# invoke json validator script 
	cat $bad_Payload | $GEMSHOME/bin/delegate > f
	$is_Valid_JSON_py f
	# exit code from is_Valid_JSON_py
	isValid=$?
	rm f
	if [ $isValid  =! '0' ] ; then
		return 1
	fi

	return 0
}

# invoke delegator script with a .json containing a known bad payload
# gmml should detect the bad payload and 
# return a valid json response containing: "sequenceIsValid": "false"
run_Bad_Payload_Test()
{
	# pipe .json to the delegator script
	# pipe reponse from delegator to grep
	# grep for sequenceIsValid : true
	# grep is returning a count (-c flag)
	if [ $(cat $bad_Payload | $GEMSHOME/bin/delegate | grep -c '"sequenceIsValid": true') != '0' ] ; then
		#echo "009a -- sequenceIsValid is True with known bad payload"
		return 1
	fi

	if [ $(cat $bad_Payload | $GEMSHOME/bin/delegate | grep -c '"sequenceIsValid": "true"') != '0' ] ; then
		#echo "009a -- sequenceIsValid is True with known bad payload"
		return 1
	fi
	
	return 0
}

if ! run_Bad_Payload_Test; then
	echo "009a -- sequenceIsValid is True with known bad payload"
	echo "009a -- exiting"
	exit 1;
else
	echo "009a -- passed"
fi

if ! run_Valid_Json_Response_Test; then
	echo "009b -- delegator returned an error as a non-valid json response"
	echo "009b -- exiting"
else 
	echo "009b -- passed"
fi

echo "009 passed"
exit 0