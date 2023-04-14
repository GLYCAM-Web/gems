#!/usr/bin/env bash

. utilities/common_environment.bash

## The variable badOutDir should be defined in the script that calls this one.
outputFilePrefix='git-ignore-me_test008'
badOutputPrefix="${badOutDir}/${now}_${outputFilePrefix}"
badOutput="${badOutputPrefix}.txt"

ALL_JSON_ARE_GOOD='true'
ALL_SEQID_ARE_GOOD='true'
ALL_TESTS_PASSED='true'

theCorrectSequenceID='00e7d454-06dd-5067-b6c9-441dd52db586'
defaultStructureConformationID='e6c2e2e8-758b-58b8-b5ff-d138da38dd22'

evaluation_input="${GEMSHOME}/tests/inputs/008.0.evaluation-request.json"
build_1_input="${GEMSHOME}/tests/inputs/008.1.build-request-first-two.json"
build_2_input="${GEMSHOME}/tests/inputs/008.2.build-request-second-two.json"
build_3_input="${GEMSHOME}/tests/inputs/008.3.build-request-third-four.json"

do_the_common_tasks()
{	
	jsonInFile="${1}"
	outFilePrefix="${2}"

	# Delegate the json input

	theJsonOut="$(cat ${jsonInFile} | $GEMSHOME/bin/delegate | tee ${outFilePrefix}.json)"

	check_output_is_only_json ${outFilePrefix}.json
	
	isJsonOk=$?
	
	if [ "${isJsonok}" != 0 ] ; then
		ALL_JSON_ARE_GOOD='false'
		echo "FAILURE:  ${1} got a non-purely-json response from delegator." | tee -a ${badOutput}
		echo "Check ${outFilePrefix}.json for more information." | tee -a ${badOutput}
	fi

	theseqID="$(get_seqID_from_json ${theJsonout})"
	if [ "${theseqID}" != "${theCorrectSequenceID}" ] ; then
		ALL_SEQID_ARE_GOOD='false'
		echo "FAILURE:  got seqID of ${theseqID} which shouldbe ${theCorrectSequenceID}." | tee -a ${badOutput}
	fi

	thepUUID="$(get_pUUID_from_json ${theJsonout})"
	return thepUUID
}



### REMOVE ME - temporary while designing test
GEMS_OUTPUT_PATH='/website/userdata'
sequenceServicePath=${GEMS_OUTPUT_PATH}/sequence/cb
sequenceSequencesPath=${GEMS_OUTPUT_PATH}/sequence/cb/Sequences
sequenceBuildsPath=${GEMS_OUTPUT_PATH}/sequence/cb/Builds
evaluation_pUUID='bce53e74-78b9-4a7e-b460-f10a0935f165'
### END remove me

###########################################
##         Evaluation                    ##
###########################################
evaluation_prefix="${badOutputPrefix}_0.evaluation"
## UNCOMMENT once test is ready to run
#evaluation_pUUID="$(do_the_common_tasks ${evaluation_input} ${evaluation_prefix})"

source "correct_outputs/008.0.testing-arrays.bash"
all_evaluation_passed='true'
echo "Running ${#EvaluationTests[@]} sub-tests for the evaluation"
for t in ${EvaluationTests[@]} ; do 
	echo "Running the following command for test ${t}: "  >> ${badOutput}
	echo "    ${EvaluationCommands[${t}]}"  >> ${badOutput}
	the_answer="$(eval ${EvaluationCommands[${t}]})"
	echo "the answer is : " >> ${badOutput}
	echo ">>>${the_answer}<<<" >> ${badOutput}
	echo "the CORRECT answer is : " >> ${badOutput}
	echo ">>>${EvaluationCorrectOutputs[${t}]}<<<" >> ${badOutput}
	if [ "${the_answer}" != "${EvaluationCorrectOutputs[${t}]}" ] ; then
		echo "The ${t} test FAILED" | tee -a ${badOutput}
		all_evaluation_passed='false'
	fi
done
if [ "${all_evaluation_passed}" == "true" ] ; then
	echo "The evaluation sub-tests passed." | tee -a ${badOutput}
else
	echo "One or more of the evaluation sub-tests FAILED." | tee -a ${badOutput}
	ALL_TESTS_PASSED='false'
fi

#ALL_TESTS_PASSED='test'

if [ "${ALL_TESTS_PASSED}" == "true" ] ; then
	return 0
else
	return 1
fi
