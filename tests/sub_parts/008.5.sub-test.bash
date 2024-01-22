#!/usr/bin/env bash

## This file should be sourced from the directory above

build_5_prefix="${badOutputPrefix}_5.build"
do_the_common_tasks ${build_5_input} ${build_5_prefix}
build_5_pUUID=${thepUUID}

source "correct_outputs/008.5.testing-arrays.bash"

check_files="""${sequenceBuildsPath}/${build_5_pUUID}/New_Builds/6009ea31-3ded-57b9-aee3-2b65fe1071be/min-gas.pdb"""
echo "About to wait for output files to appear." | tee -a ${badOutput}
echo "the file(s) we await : ${check_files}" >> ${badOutput}
wait_for_files ${check_files}
result=$?
if [ "${result}" -ne "0" ] ; then
	echo "Timed out before files appeared.  Test FAILED." | tee -a ${badOutput}
	all_build_5_passed='false'
	ALL_TESTS_PASSED='false'
	return 1
fi

all_build_5_passed='true'
echo "Running ${#Build5Tests[@]} sub-tests for the third build of four structures"
for t in ${Build5Tests[@]} ; do 
	echo "Running the following command for test ${t}: "  >> ${badOutput}
	echo "    ${Build5Commands[${t}]}"  >> ${badOutput}
	the_answer="$(eval ${Build5Commands[${t}]})"
	echo "the answer is : " >> ${badOutput}
	echo ">>>${the_answer}<<<" >> ${badOutput}
	echo "the CORRECT answer is : " >> ${badOutput}
	echo ">>>${Build5CorrectOutputs[${t}]}<<<" >> ${badOutput}
	if [ "${the_answer}" != "${Build5CorrectOutputs[${t}]}" ] ; then
		echo "The ${t} test FAILED" | tee -a ${badOutput}
		all_build_5_passed='false'
	fi
done
if [ "${all_build_5_passed}" == "true" ] ; then
	echo "sub-tests passed." | tee -a ${badOutput}
else
	echo "One or more of the sub-tests FAILED." | tee -a ${badOutput}
	ALL_TESTS_PASSED='false'
fi

