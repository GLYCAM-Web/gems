#!/usr/bin/env bash

## This file should be sourced from the directory above

###########################################
##   008.4 - Re-Evaluation               ##
###########################################
evaluation_prefix="${badOutputPrefix}_4.evaluation"
do_the_common_tasks ${evaluation_input} ${evaluation_prefix}
# This test relies on the other tests having been run, but is oddly decoupled from them. Here we go:
eval_1_pUUID=$(grep -m 1  pUUID ${sequenceSequencesPath}/${theCorrectSequenceID}/evaluation.json | cut -d '"' -f4)
eval_2_pUUID=${thepUUID}

source "correct_outputs/008.4.testing-arrays.bash"

check_file="${sequenceBuildsPath}/${eval_2_pUUID}/logs/response.json"
echo "About to wait for output files to appear." | tee -a ${badOutput}
echo "the file(s) we await : ${check_file}" >> ${badOutput}
wait_for_files ${check_file}
result=$?
if [ "${result}" -ne "0" ] ; then
	echo "Timed out before files appeared.  Test FAILED." | tee -a ${badOutput}
	all_evaluation_passed='false'
	ALL_TESTS_PASSED='false'
	return 1
fi

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
	return 0
else
	echo "One or more of the evaluation sub-tests FAILED." | tee -a ${badOutput}
	ALL_TESTS_PASSED='false'
	return 1
fi

