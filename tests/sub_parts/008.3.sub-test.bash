#!/usr/bin/env bash

## This file should be sourced from the directory above

###########################################
##   008.3 - Build third four            ##
###########################################
build_3_prefix="${badOutputPrefix}_2.build"
do_the_common_tasks ${build_3_input} ${build_3_prefix}
build_3_pUUID=${thepUUID}

source "correct_outputs/008.3.testing-arrays.bash"

check_files="""${sequenceBuildsPath}/${build_3_pUUID}/New_Builds/b90a4d30-822c-5aba-ae5a-10a9ddb1a227/min-gas.pdb
${sequenceBuildsPath}/${build_3_pUUID}/New_Builds/c408f40d-28e0-5e8d-86a3-221b74da42f7/min-gas.pdb"""
echo "About to wait for output files to appear." | tee -a ${badOutput}
echo "the file(s) we await : ${check_files}" >> ${badOutput}
wait_for_files ${check_files}
result=$?
if [ "${result}" -ne "0" ] ; then
	echo "Timed out before files appeared.  Test FAILED." | tee -a ${badOutput}
	all_build_3_passed='false'
	ALL_TESTS_PASSED='false'
	return 1
fi

all_build_3_passed='true'
echo "Running ${#Build3Tests[@]} sub-tests for the third build of four structures"
for t in ${Build3Tests[@]} ; do 
	echo "Running the following command for test ${t}: "  >> ${badOutput}
	echo "    ${Build3Commands[${t}]}"  >> ${badOutput}
	the_answer="$(eval ${Build3Commands[${t}]})"
	echo "the answer is : " >> ${badOutput}
	echo ">>>${the_answer}<<<" >> ${badOutput}
	echo "the CORRECT answer is : " >> ${badOutput}
	echo ">>>${Build3CorrectOutputs[${t}]}<<<" >> ${badOutput}
	if [ "${the_answer}" != "${Build3CorrectOutputs[${t}]}" ] ; then
		echo "The ${t} test FAILED" | tee -a ${badOutput}
		all_build_3_passed='false'
	fi
done
if [ "${all_build_3_passed}" == "true" ] ; then
	echo "The third build sub-tests passed." | tee -a ${badOutput}
else
	echo "One or more of the third build sub-tests FAILED." | tee -a ${badOutput}
	ALL_TESTS_PASSED='false'
fi

