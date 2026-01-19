#!/usr/bin/env bash

## This file should be sourced from the directory above

theCorrectSequenceID='fc6085c0-822c-5655-b5be-88da496814cb'
build_6_prefix="${badOutputPrefix}_6.build"
do_the_common_tasks ${build_6_input} ${build_6_prefix}
build_6_pUUID=${thepUUID}

source "correct_outputs/008.6.testing-arrays.bash"

check_files="""${sequenceBuildsPath}/${build_6_pUUID}/New_Builds/structure/min-gas.pdb"""
echo "About to wait for output files to appear." | tee -a ${badOutput}
echo "the file(s) we await : ${check_files}" >> ${badOutput}
wait_for_files ${check_files}
result=$?
if [ "${result}" -ne "0" ] ; then
	echo "Timed out before files appeared.  Test FAILED." | tee -a ${badOutput}
	all_build_6_passed='false'
	ALL_TESTS_PASSED='false'
	return 1
fi

all_build_6_passed='true'
echo "Running ${#Build6Tests[@]} sub-tests for the third build of four structures"
for t in ${Build6Tests[@]} ; do 
	echo "Running the following command for test ${t}: "  >> ${badOutput}
	echo "    ${Build6Commands[${t}]}"  >> ${badOutput}
	the_answer="$(eval ${Build6Commands[${t}]})"
	echo "the answer is : " >> ${badOutput}
	echo ">>>${the_answer}<<<" >> ${badOutput}
	echo "the CORRECT answer is : " >> ${badOutput}
	echo ">>>${Build6CorrectOutputs[${t}]}<<<" >> ${badOutput}
	if [ "${the_answer}" != "${Build6CorrectOutputs[${t}]}" ] ; then
		echo "The ${t} test FAILED" | tee -a ${badOutput}
		all_build_6_passed='false'
	fi
done
if [ "${all_build_6_passed}" == "true" ] ; then
	echo "sub-tests passed." | tee -a ${badOutput}
else
	echo "One or more of the sub-tests FAILED." | tee -a ${badOutput}
	ALL_TESTS_PASSED='false'
fi

