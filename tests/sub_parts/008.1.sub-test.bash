#!/usr/bin/env bash

## This file should be sourced from the directory above

###########################################
##   008.1 - Build first two             ##
###########################################
build_1_prefix="${badOutputPrefix}_1.build"
## UNCOMMENT once test is ready to run
#build_1_pUUID="$(do_the_common_tasks ${build_1_input} ${build_1_prefix})"

source "correct_outputs/008.1.testing-arrays.bash"
all_build_1_passed='true'
echo "Running ${#Build1Tests[@]} sub-tests for the first build of two structures"
for t in ${Build1Tests[@]} ; do 
	echo "Running the following command for test ${t}: "  >> ${badOutput}
	echo "    ${Build1Commands[${t}]}"  >> ${badOutput}
	the_answer="$(eval ${Build1Commands[${t}]})"
	echo "the answer is : " >> ${badOutput}
	echo ">>>${the_answer}<<<" >> ${badOutput}
	echo "the CORRECT answer is : " >> ${badOutput}
	echo ">>>${Build1CorrectOutputs[${t}]}<<<" >> ${badOutput}
	if [ "${the_answer}" != "${Build1CorrectOutputs[${t}]}" ] ; then
		echo "The ${t} test FAILED" | tee -a ${badOutput}
		all_build_1_passed='false'
	fi
done
if [ "${all_build_1_passed}" == "true" ] ; then
	echo "The first build sub-tests passed." | tee -a ${badOutput}
else
	echo "One or more of the first build sub-tests FAILED." | tee -a ${badOutput}
	ALL_TESTS_PASSED='false'
fi

