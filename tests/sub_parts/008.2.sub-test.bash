#!/usr/bin/env bash

## This file should be sourced from the directory above

###########################################
##   008.2 - Build second two            ##
###########################################
build_2_prefix="${badOutputPrefix}_2.build"
## UNCOMMENT once test is ready to run
#build_2_pUUID="$(do_the_common_tasks ${build_2_input} ${build_2_prefix})"

source "correct_outputs/008.2.testing-arrays.bash"
all_build_2_passed='true'
echo "Running ${#Build2Tests[@]} sub-tests for the second build of two structures"
for t in ${Build2Tests[@]} ; do 
	echo "Running the following command for test ${t}: "  >> ${badOutput}
	echo "    ${Build2Commands[${t}]}"  >> ${badOutput}
	the_answer="$(eval ${Build2Commands[${t}]})"
	echo "the answer is : " >> ${badOutput}
	echo ">>>${the_answer}<<<" >> ${badOutput}
	echo "the CORRECT answer is : " >> ${badOutput}
	echo ">>>${Build2CorrectOutputs[${t}]}<<<" >> ${badOutput}
	if [ "${the_answer}" != "${Build2CorrectOutputs[${t}]}" ] ; then
		echo "The ${t} test FAILED" | tee -a ${badOutput}
		all_build_2_passed='false'
	fi
done
if [ "${all_build_2_passed}" == "true" ] ; then
	echo "The first build sub-tests passed." | tee -a ${badOutput}
else
	echo "One or more of the first build sub-tests FAILED." | tee -a ${badOutput}
	ALL_TESTS_PASSED='false'
fi

