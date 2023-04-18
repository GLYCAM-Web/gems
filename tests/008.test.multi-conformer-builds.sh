#!/usr/bin/env bash

. './utilities/common_environment.bash'
. './utilities/functions.bash'

echo "The output path is: ${GEMS_OUTPUT_PATH}"

## The variable badOutDir should be defined in the script that calls this one.
outputFilePrefix='git-ignore-me_test008'
badOutputPrefix="${badOutDir}/${now}_${outputFilePrefix}"
badOutput="${badOutputPrefix}.txt"

ALL_JSON_ARE_GOOD='true'
ALL_TESTS_PASSED='true'

theCorrectSequenceID='00e7d454-06dd-5067-b6c9-441dd52db586'
defaultStructureConformationID='e6c2e2e8-758b-58b8-b5ff-d138da38dd22'

evaluation_input="${GEMSHOME}/tests/inputs/008.0.evaluation-request.json"
build_1_input="${GEMSHOME}/tests/inputs/008.1.build-request-first-two.json"
build_2_input="${GEMSHOME}/tests/inputs/008.2.build-request-second-two.json"
build_3_input="${GEMSHOME}/tests/inputs/008.3.build-request-third-four.json"

do_the_common_tasks() {	
	jsonInFile="${1}"
	outFilePrefix="${2}"
	theJsonFile=${outFilePrefix}.json
	#echo "the out file is : ${theJsonFile}"

	# Delegate the json input

	theJsonOut="$(cat ${jsonInFile} | $GEMSHOME/bin/delegate | tee ${theJsonFile})"

	check_output_is_only_json ${theJsonFile}
	
	isJsonOk=$?
	
	if [ "${isJsonOk}" != 0 ] ; then
		ALL_JSON_ARE_GOOD='false'
		echo "FAILURE:  ${1} got a non-purely-json response from delegator." | tee -a ${badOutput}
		echo "Check ${theJsonFile} for more information." | tee -a ${badOutput}
	fi

	get_seqID_from_json ${theJsonFile}
	if [ "${theseqID}" != "${theCorrectSequenceID}" ] ; then
		ALL_SEQID_ARE_GOOD='false'
		echo "FAILURE:  got seqID of ${theseqID} which shouldbe ${theCorrectSequenceID}." | tee -a ${badOutput}
	fi
	export theseqID

	get_pUUID_from_json ${theJsonFile}
	export thepUUID
	return 0
}

################### MAIN #########################
#
# First remove all outputs in Builds and Sequences to test New_Builds functionality
echo "Checking for sequence service path"
if [ -d "${sequenceServicePath}" ] ; then
        echo "Removing Sequences and Builds from ${sequenceServicePath}" >> $badOutput
        ( cd ${sequenceServicePath} && rm -rf Sequences Builds )
else
        mkdir -p ${sequenceServicePath}
fi
if [ ! -d "${sequenceServicePath}" ] ; then
        echo "Unable to create output directory.  Exiting." | tee -a $badOutput
        exit 1
fi


echo """
########################################
## Sub test 0:  Evaluation
########################################"""

source './sub_parts/008.0.sub-test.bash'

if [ "${ALL_TESTS_PASSED}" == "true" ] ; then
	echo """
########################################
## Sub test 1:  build first two
########################################"""
	source './sub_parts/008.1.sub-test.bash'
fi

if [ "${ALL_TESTS_PASSED}" == "true" ] ; then
	echo """
########################################
## Sub test 2:  build second two
########################################"""

	source './sub_parts/008.2.sub-test.bash'
fi

if [ "${ALL_TESTS_PASSED}" == "true" ] ; then
	echo """
########################################
## Sub test 3:  build third four
########################################"""

	source './sub_parts/008.3.sub-test.bash'
fi

exit 0

if [ "${ALL_JSON_ARE_GOOD}" == "false" ] ; then
        echo "The builds worked, but one or more JSON delegations FAILED."
	ALL_TESTS_PASSED='false'
fi
#ALL_TESTS_PASSED='test'
if [ "${ALL_TESTS_PASSED}" == "true" ] ; then
        ## Remove what we made
        ( cd ${sequenceServicePath} && rm -rf Sequences Builds )
        remove_file_if_found ${badOutput}
        return 0;
else
	return 1
fi
