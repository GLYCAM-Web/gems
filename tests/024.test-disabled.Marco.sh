#!/usr/bin/env bash

#####################
#####################
## Disabled until IC settles
#####################
#####################

# If GEMS_KEEP_BAD_OUTPUTS is set to "True", badOutputs will not be removed after testing

. './utilities/common_environment.bash'
. './utilities/functions.bash'

## The variable badOutDir should be defined in the script that calls this one.
outputFilePrefix='git-ignore-me_test024'
badOutputPrefix="${badOutDir}/${now}_${outputFilePrefix}"
badOutputDir="${badOutDir}/${now}_${outputFilePrefix}_Files"
correctFilesPath="correct_outputs"
STATUSFILE="${badOutputPrefix}.txt"
LOGFILE="${badOutputPrefix}_details.txt"

mkdir -p "${badOutputDir}"

ALL_TESTS_PASSED='true'

echo "Testing Marco for Delegator as the Entity."

DELEGATE="$GEMSHOME/bin/delegate"
inputJSON="inputs/024.marco_delegator_explicit.json"
outputJSON="${badOutputDir}/marco_delegator_full_output.json"
compare_outputJSON="${badOutputDir}/marco_delegator_full_output_id_mask.json"
correct_outputJSON="${correctFilesPath}/024.marco_delegator_explicit_output.json"

COM="${DELEGATE} ${inputJSON} > ${outputJSON}"
rclr "Requesting Marco with Delegator as the Entity." "${COM}" "Delegator Marco"
theUUID="$(cat ${outputJSON} | utilities/json_ripper.py entity.services.Marco.myUuid)"
if ! is_string_a_uuid "${theUUID}" ; then
        echo "ERROR : Delegator Marco returned invalid response" | tee -a ${STATUSFILE}
        echo "ERROR : Unable to extract UUID from the delegator response" | tee -a ${LOGFILE}
	ALL_TESTS_PASSED='false'
else
	COM="sed 's/${theUUID}/theUUID/g' ${outputJSON} > ${compare_outputJSON}"
	rclr "Generating response with UUID removed." "${COM}" "UUID removal"
	diff_result="$(diff ${compare_outputJSON} ${correct_outputJSON})"
	if [ "${diff_result}" != "" ] ; then
        	echo "ERROR : Delegator Marco FAILED" | tee -a ${STATUSFILE}
        	echo "ERROR : Delegator Marco diff result was not empty" | tee -a ${LOGFILE}
		echo "The following are the diffs:" >> ${LOGFILE}
		echo "${diff_result}" >> ${LOGFILE}
		echo "See this file for more info: ${LOGFILE}"
		ALL_TESTS_PASSED='false'
	fi
fi


if [ "${ALL_TESTS_PASSED}" != 'true' ] ; then
	return 1
fi

return 0

