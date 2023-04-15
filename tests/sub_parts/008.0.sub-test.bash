#!/usr/bin/env bash

## This file should be sourced from the directory above

###########################################
##   008.0 - Evaluation                  ##
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

