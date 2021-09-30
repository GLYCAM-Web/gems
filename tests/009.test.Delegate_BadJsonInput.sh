# tests that are correctly formatted json objects, but have bad inputs

bad_Payload=$GEMSHOME/gemsModules/delegator/test_in/sequence/minimal_bad_payload.json
bad_Payload_Response=""

# invoke delegator script with a .json containing a known bad payload
# gmml should detect the bad payload and 
# return a response containing: "sequenceIsValid": "false"
run_bad_Payload_test()
{

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

if ! run_bad_Payload_test; then
	echo "009a -- sequenceIsValid is True with known bad payload"
	exit 1
fi

echo "009 passed"
exit 0